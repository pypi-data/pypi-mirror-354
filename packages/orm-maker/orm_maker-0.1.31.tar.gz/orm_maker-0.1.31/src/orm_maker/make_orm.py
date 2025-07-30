import getpass
from pathlib import Path
from uuid import uuid4

import click
import pendulum
import polars

from orm_maker.__app_name__ import APP_NAME
from orm_maker.__version__ import __version__
from orm_maker.configs import get_config
from orm_maker.library import click_secho_dataframe, get_next_file_name, replace_chars
from orm_maker.status_result import Status_Code


def get_tables(df: polars.DataFrame) -> set:
    return set(df.get_column("table"))


def get_table(table_name: str, df: polars.DataFrame) -> polars.DataFrame:
    return df.filter(polars.col("table") == table_name)


def validate_base_table(df: polars.DataFrame) -> polars.DataFrame:
    """
    check if there is a parent table defined by ! as the table name
    if there is, make sure no other table has a column name that will overrule
    """
    return df


def validate_linked_field_types(df: polars.DataFrame) -> list:
    """
    gather all linked fields in a set of tuples (table, column)
    if the column is defined in the ! table, check the type agains !
    else check the type against the table
    """
    fixes: list = list()
    result = df.clone()
    for row in result.iter_rows(named=True):
        # validate linked field types
        table = row["table"]
        column = row["column"]
        linked_field = row["linked_field"]

        if linked_field:
            lf_table = linked_field.split(".")[0]
            lf_field = linked_field.split(".")[1]

            link = result.filter(polars.col("table").is_in([lf_table])).head(1)
            if link.shape[0] == 0:
                fixes.append(
                    {
                        "fixtype": "linked_table_does_not_exist",
                        "schema": row["schema"],
                        "table": lf_table,
                        "column": "[does not exist]",
                        "old_value": "[does not exist]",
                        "new_value": lf_field,
                        "type": row["type"],
                        "note": f"linked table {lf_table} doesn't exist",
                    }
                )

            link = result.filter(polars.col("table").is_in([lf_table, "!"]), polars.col("column") == lf_field).head(1)
            if link.shape[0] == 0:
                fixes.append(
                    {
                        "fixtype": "linked_fields_missing_insert_column",
                        "schema": row["schema"],
                        "table": lf_table,
                        "column": "[does not exist]",
                        "old_value": "[does not exist]",
                        "new_value": lf_field,
                        "type": row["type"],
                        "note": f"linked to field does not exist: {linked_field}",
                    }
                )

            elif row["type"] != link[0].get_column("type")[0]:
                fixes.append(
                    {
                        "fixtype": "linked_fields_types",
                        "schema": row["schema"],
                        "table": row["table"],
                        "column": row["column"],
                        "old_value": row["type"],
                        "new_value": link["type"][0],
                        "note": f"linked field from {table}.{column} to {linked_field} has different types",
                    }
                )
            else:
                continue

    return fixes


def validate_input_file(
    input: Path, output: Path, accept_changes: bool = False, write_changes: bool = False, overwrite: bool = False
) -> polars.DataFrame | None:
    # TODO: Check for valid types on linked fields
    # TODO: Check for valid types on non-linked fields
    # TODO: Check for disallowed characters in table names, column names
    # TODO: Check for no duplicate table, column rows
    # TODO: Check for correct number of columns in the CSV

    # NOTE: validation error resolution ideas:
    # NOTE:     -categorize validation errors: automatically fixable or need user input
    # NOTE:     -automatically fixable, make all changes and present them to user for confirmation
    # NOTE:     -user input needed, find all of these errors and present to user, request changes in the imput file

    df = polars.read_csv(input)
    result = df.clone()
    fixes: list = list()

    fixes.extend(validate_linked_field_types(df))

    if len(fixes):
        fix = polars.DataFrame(fixes)
        click_secho_dataframe(fix)

        if not accept_changes:
            accept_changes = click.confirm("Do you accept these fixes, if not then abort.")

        if not accept_changes:
            return None

        if accept_changes:
            drop = ["old_value", "note", "fixtype", "column"]

            # inserting new rows to the result
            fix_lf_missing = fix.filter(polars.col("fixtype") == "linked_fields_missing_insert_column")
            if fix_lf_missing.shape[0] > 0:
                fix_lf_missing = fix_lf_missing.drop(drop)
                fix_lf_missing = fix_lf_missing.rename({"new_value": "column"})

            fix_lt_missing = fix.filter(polars.col("fixtype") == "linked_table_does_not_exist")
            if fix_lt_missing.shape[0] > 0:
                fix_lt_missing = fix_lt_missing.drop(drop)
                fix_lt_missing = fix_lt_missing.rename({"new_value": "column"})

            # updating existing rows in the result
            drop = ["old_value", "note", "fixtype"]
            if "type" in fix.columns:
                drop.append("type")

            fix_lf_types = fix.filter(polars.col("fixtype") == "linked_fields_types")
            if fix_lf_types.shape[0] > 0:
                fix_lf_types = fix_lf_types.drop(drop)
                fix_lf_types = fix_lf_types.rename({"new_value": "type"})

            result = result.update(fix_lf_types, on=["table", "column"])
            result = polars.concat([result, fix_lf_missing], how="diagonal")
            result = polars.concat([result, fix_lt_missing], how="diagonal")

        if write_changes:
            result.write_csv(input)

        if not write_changes:
            write_changes = click.confirm(f"Do you want to overwrite the input file {input} with these fixes?")

    result = result.unique()
    result = result.sort(by=["schema", "table", "column"])
    click_secho_dataframe(result)
    return result


def make_module_comment(input: Path) -> list:
    result: list = list()

    result.append("'''")
    result.append(f"This module was made by {getpass.getuser()} on {pendulum.now()},")
    result.append(f"using {APP_NAME} v{__version__},")
    result.append(f"input file: {str(input.absolute)}")
    result.append("'''")
    return result


def make_module_imports(df: polars.DataFrame) -> list:
    result: list = list()

    types_set: set = set(df.get_column("type"))

    t: str = str()
    for t in types_set:
        if "(" in t:
            trimmed_t = t[: t.find("(")]
        else:
            trimmed_t = t

        if trimmed_t.lower() not in ["list", "dict", "dictionary"]:
            result.append(f"from sqlalchemy import {trimmed_t}")

        if trimmed_t == "Uuid":
            result.append("import uuid")
        if "date" in trimmed_t or "time" in trimmed_t:
            result.append("import datetime")

    if df.filter(polars.col("enumeration").is_not_null()).shape[0] > 0:
        result.append("import enum")

    result.append("import sqlalchemy")
    result.append("from sqlalchemy import create_engine")
    result.append("from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship")
    result.append("from sqlalchemy import ForeignKey")
    result.append("from typing import List, Optional, Dict, ClassVar, TypeAlias")
    result.append("import datetime")

    result = list(set(result))
    result = sorted(result)

    return result


def make_enums(df: polars.DataFrame) -> list:
    result: list = list()

    df_enum = df.filter(polars.col("enumeration").is_not_null()).select(
        ["schema", "table", "column", "type", "enumeration"]
    )

    for row in df_enum.iter_rows(named=True):
        table = row["table"].upper()

        if row["table"] == "!":
            table = "BASE"
        else:
            table = replace_chars(table)

        column = replace_chars(row["column"]).upper()

        result.append(f"class {table}_{column}(enum.Enum):")

        enums = row["enumeration"].split("|")
        enums = [replace_chars(enum) for enum in enums]
        enum: str
        cnt: int = 0
        for enum in enums:
            result.append(f"    {enum.upper()} = {cnt}")
            cnt += 1

        result.append("")

    result.pop()

    return result


def make_base_class(df: polars.DataFrame) -> list:
    result: list = list()
    result.append("class Base(DeclarativeBase):")
    df_base = df.filter(polars.col("table") == "!")
    if df_base.shape[0] == 0:
        result.append("    pass")
        return result

    type_map = get_config(["types_map"])

    for row in df_base.iter_rows(named=True):
        column = row["column"]
        dtype = row["type"]
        if dtype.find("(") > 0:
            dtype = dtype[: dtype.find("(")]

        nullable: bool = bool(row["nullable"])
        enum: bool = bool(row["enumeration"])
        key: bool = bool(row["key"])
        list_: bool = "list" in dtype.lower()
        dict_: bool = "dict" in dtype.lower()

        lhs: str = str()
        rhs: str = str()

        if enum:
            dtype = f"BASE_{column.upper()}"
            sadtype = dtype
        else:
            sadtype = type_map.get(dtype)

        # lhs first
        lhs = f"{column}: "
        if list_ or dict_:
            if dict_:
                sadtype = "dict"
            if list_:
                sadtype = "list"

            lhs += "ClassVar["
        else:
            lhs += "Mapped["

        if nullable:
            lhs += f"Optional[{sadtype}]]"
        else:
            lhs += f"{sadtype}]"

        # rhs
        rhs = "mapped_column("

        if key and "uuid" in dtype.lower():
            rhs += "primary_key=True, default=lambda: uuid.uuid4()"

        if key and "uuid" not in dtype.lower():
            rhs += "primary_key=True"

        if enum:
            rhs += f"sqlalchemy.Enum({dtype})"

        rhs += ")"

        if list_ or dict_:
            rhs = str()

        if rhs == str():
            result.append(lhs)
        else:
            result.append(f"    {lhs} = {rhs}")

    return result


def make_classes(df: polars.DataFrame, make_update: bool = True) -> list:
    result: list = list()
    tables = (
        df.filter(polars.col("table") != "!").unique(["schema", "table"]).sort(["schema", "table", "key", "column"])
    )
    type_map = get_config(["types_map"])

    # create list of reprs for base attributes, will use to extend the repr list down below
    df_base = df.filter(polars.col("table") == "!", polars.col("repr") > 0)
    base_repr: list = list()
    for row in df_base.iter_rows(named=True):
        base_repr.append((row["repr"], f"{row['column']}={{self.{row['column']}}}"))

    for row_table in tables.iter_rows(named=True):
        schema = row_table["schema"]
        table = row_table["table"]

        repr: list = list()
        column: str = str()
        dtype: str = str()
        cols = df.filter(polars.col("table") == table)

        result.append(f"class {table.upper()}(Base):")

        result.append("")
        result.append(f"    __tablename__ = '{table.lower()}'")
        result.append(f"    __table_args__ = {{'schema': '{schema}'}}")

        for col in cols.iter_rows(named=True):
            column = col["column"]
            dtype = col["type"]
            if dtype.find("(") > 0:
                dtype = dtype[: dtype.find("(")]

            nullable: bool = bool(col["nullable"])
            enum: bool = bool(col["enumeration"])
            key: bool = bool(col["key"])
            link: bool = bool(col["linked_field"])
            list_: bool = "list" in dtype.lower()
            dict_: bool = "dict" in dtype.lower()

            lhs: str = str()
            rhs: str = str()

            if enum:
                dtype = f"{table.upper()}_{column.upper()}"
                sadtype = dtype
            elif list_ or dict_:
                sadtype = dtype
            else:
                sadtype = type_map[dtype]

            # lhs first
            lhs = f"{column}: "

            if list_ or dict_:
                if dict_:
                    sadtype = "dict"

                if list_:
                    sadtype = "list"

                lhs += "ClassVar["
            else:
                lhs += "Mapped["

            if nullable:
                lhs += f"Optional[{sadtype}]]"
            else:
                lhs += f"{sadtype}]"

            # rhs
            rhs = "mapped_column("

            if key and "uuid" in dtype.lower():
                rhs += "primary_key=True, default=lambda: uuid.uuid4()"

            if key and "uuid" not in dtype.lower():
                rhs += "primary_key=True"

            if enum:
                rhs += f"sqlalchemy.Enum({dtype}, schema='{schema}')"

            if link:
                rhs += f"{dtype}, ForeignKey('{col['schema']}.{col['linked_field']}', name='fk_{str(uuid4())}')"

            rhs += ")"

            if list_ or dict_:
                rhs = str()

            if rhs == str():
                result.append(f"    {lhs}")
            else:
                result.append(f"    {lhs} = {rhs}")

            if link:
                link_table = col["linked_field"].split(".")[0]
                # link_column = col["linked_field"].split(".")[1]
                result.append(f"    {link_table} = relationship('{link_table.upper()}' , foreign_keys=[{column}])")

            if col["repr"]:
                repr.append((col["repr"], f"{column}={{self.{column}}}"))

        repr.extend(base_repr)
        repr = sorted(repr)
        repr = [value for _, value in repr]
        result.append("")
        result.append("    def __repr__(self) -> str:")
        result.append(f"        return f'<{table.upper()}=({', '.join(repr)})>'")
        result.append("")

        table_cols = list(cols.get_column("column"))
        table_cols.extend(list(df.filter(polars.col("table") == "!").get_column("column")))

        prim_keys: list = list(df.filter(polars.col("table") == "!", polars.col("key") == 1).get_column("column"))
        prim_keys.extend(cols.filter(polars.col("key") == 1).get_column("column"))

        update_col = [col for col in table_cols if col not in prim_keys]

        result.append("    def update_object(self, obj) -> bool:")
        result.append(f"        if not isinstance(obj, {table.upper()}):")
        result.append("            return False")
        result.append("")
        for col in update_col:
            result.append(f"        if self.{col} != obj.{col}:")
            result.append(f"            self.{col} = obj.{col}")
        result.append("")
        result.append("        return True")

        if make_update:
            pass

        result.append("\n")

    # make a typealias for all of the classes above
    classes = [ormclass.upper() for ormclass in tables.get_column("table")]
    delim = "\n    |"
    ormclass_typealias = f"ORMClass: TypeAlias = ({delim.join(classes)})"
    result.append(ormclass_typealias)
    return result


def make_module_main() -> list:
    result: list = list()

    result.append("def make_db(connection_string):")
    result.append("    engine = create_engine(connection_string, echo=True)")
    result.append("    Base.metadata.create_all(engine)")

    return result


def make_orm_helper(
    input: Path,
    output: Path,
    accept_changes: bool = False,
    write_changes: bool = False,
    conn_str: str | None = None,
    overwrite: bool = False,
    make_update: bool = True,
) -> Status_Code:
    if not input.exists():
        raise FileExistsError(f"{str(input.absolute())} does not exist")

    if output.exists() and not overwrite:
        output = get_next_file_name(output)

    df = validate_input_file(input, output, accept_changes, write_changes, overwrite)
    if df is None:
        return Status_Code.CHANGES_NOT_ACCEPTED

    result: list = list()
    result.extend(make_module_comment(input))
    result.extend("\n")
    result.extend(make_module_imports(df))
    result.extend("\n")
    result.extend(make_enums(df))
    result.extend("\n")
    result.extend(make_base_class(df))
    result.extend("\n")
    result.extend(make_classes(df, make_update=make_update))
    result.extend("\n")
    result.extend(make_module_main())

    with open(output, "w") as f:
        f.write("\n".join(result))

    return Status_Code.OK
