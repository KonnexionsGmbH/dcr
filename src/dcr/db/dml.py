"""Module db.dml: Database Manipulation Management."""
import json
import os
import pathlib
from typing import Dict
from typing import Tuple
from typing import TypeAlias

import cfg.glob
import db.dml
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
import utils

# -----------------------------------------------------------------------------
# Global constants.
# -----------------------------------------------------------------------------
JSON_NAME_API_VERSION: str = "apiVersion"
JSON_NAME_COLUMN_NAME: str = "columnName"
JSON_NAME_COLUMN_VALUE: str = "columnValue"
JSON_NAME_DATA: str = "data"
JSON_NAME_ROW: str = "row"
JSON_NAME_ROWS: str = "rows"
JSON_NAME_TABLES: str = "tables"
JSON_NAME_TABLE_NAME: str = "tableName"


# -----------------------------------------------------------------------------
# Type declaration.
# -----------------------------------------------------------------------------
Columns: TypeAlias = Dict[str, bool | int | None | os.PathLike[str] | str]

ColumnValues: TypeAlias = Tuple[bool | int | None | os.PathLike[str] | str]


# -----------------------------------------------------------------------------
# Delete a database row based on its id column.
# -----------------------------------------------------------------------------
def delete_dbt_id(
    table_name: str,
    id_where: int,
) -> None:
    """Delete a database row based on its id column.

    Args:
        table_name (str): sqlalchemy.Table name.
        id_where (int): Content of column id.
    """
    dbt = sqlalchemy.Table(table_name, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

    with cfg.glob.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(sqlalchemy.delete(dbt).where(dbt.c.id == id_where))
        conn.close()


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_dbt_row(
    table_name: str,
    columns: Columns,
) -> int:
    """Insert a new row into a database table.

    Args:
        table_name (str): Table name.
        columns (cfg.glob.TYPE_COLUMNS_INSERT): Pairs of column name and value.

    Returns:
        int: The last id found.
    """
    dbt = sqlalchemy.Table(table_name, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

    with cfg.glob.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        result = conn.execute(sqlalchemy.insert(dbt).values(columns).returning(dbt.columns.id))
        row = result.fetchone()
        conn.close()

    return row[0]


# -----------------------------------------------------------------------------
# Load database data from a JSON file.
# -----------------------------------------------------------------------------
def load_db_data_from_json(initial_database_data: pathlib.Path) -> None:
    """Load database data from a JSON file.

    Args:
        initial_database_data (Path): JSON file.
    """
    with open(initial_database_data, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
        json_data = json.load(file_handle)

        api_version = json_data[JSON_NAME_API_VERSION]
        if api_version != cfg.glob.setup.dcr_version:
            utils.terminate_fatal(f"Expected api version is' {cfg.glob.setup.dcr_version}' " f"- got '{api_version}'")

        data = json_data[JSON_NAME_DATA]
        for json_table in data[JSON_NAME_TABLES]:
            table_name = json_table[JSON_NAME_TABLE_NAME].lower()

            if table_name not in ["language"]:
                if table_name in [
                    "action",
                    "document",
                    "run",
                    "token",
                    "version",
                ]:
                    utils.terminate_fatal(f"The database table '{table_name}' must not be changed via the JSON file.")
                else:
                    utils.terminate_fatal(f"The database table '{table_name}' does not exist in the database.")

            for json_row in json_table[JSON_NAME_ROWS]:
                db_columns = {}

                for json_column in json_row[JSON_NAME_ROW]:
                    db_columns[json_column[JSON_NAME_COLUMN_NAME]] = json_column[JSON_NAME_COLUMN_VALUE]

                db.dml.insert_dbt_row(
                    table_name,
                    db_columns,
                )


# -----------------------------------------------------------------------------
# Update a database row based on its id column.
# -----------------------------------------------------------------------------
def update_dbt_id(
    table_name: str,
    id_where: int,
    columns: Columns,
) -> None:
    """Update a database row based on its id column.

    Args:
        table_name (str): sqlalchemy.Table name.
        id_where (int): Content of column id.
        columns (Columns): Pairs of column name and value.
    """
    dbt = sqlalchemy.Table(table_name, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

    with cfg.glob.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(sqlalchemy.update(dbt).where(dbt.c.id == id_where).values(columns))
        conn.close()
