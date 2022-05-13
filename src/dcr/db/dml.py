"""Module db.dml: Database Manipulation Management."""
import json
import os
import pathlib
from typing import Dict
from typing import TypeAlias

import cfg.glob
import db.dml
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm

# -----------------------------------------------------------------------------
# Type declaration.
# -----------------------------------------------------------------------------
import utils

Columns: TypeAlias = Dict[
    str, bool | sqlalchemy.Boolean | int | sqlalchemy.Integer | str | os.PathLike[str] | sqlalchemy.String | None
]


# -----------------------------------------------------------------------------
# Delete a database row based on its id column.
# -----------------------------------------------------------------------------
def delete_dbt_id(
    table_name: str,
    id_where: int | sqlalchemy.Integer,
) -> None:
    """Delete a database row based on its id column.

    Args:
        table_name (str): sqlalchemy.Table name.
        id_where (int | sqlalchemy.Integer): Content of column id.
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
) -> sqlalchemy.Integer:
    """Insert a new row into a database table.

    Args:
        table_name (str): Table name.
        columns (cfg.glob.TYPE_COLUMNS_INSERT): Pairs of column name and value.

    Returns:
        sqlalchemy.Integer: The last id found.
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

        api_version = json_data[cfg.glob.JSON_NAME_API_VERSION]
        if api_version != cfg.glob.setup.dcr_version:
            utils.terminate_fatal(f"Expected api version is' {cfg.glob.setup.dcr_version}' " f"- got '{api_version}'")

        data = json_data[cfg.glob.JSON_NAME_DATA]
        for json_table in data[cfg.glob.JSON_NAME_TABLES]:
            table_name = json_table[cfg.glob.JSON_NAME_TABLE_NAME].lower()

            if table_name not in ["language"]:
                if table_name in [
                    "action",
                    "base",
                    "run",
                    "token",
                    "version",
                ]:
                    utils.terminate_fatal(f"The database table '{table_name}' must not be changed via the JSON file.")
                else:
                    utils.terminate_fatal(f"The database table '{table_name}' does not exist in the database.")

            for json_row in json_table[cfg.glob.JSON_NAME_ROWS]:
                db_columns = {}

                for json_column in json_row[cfg.glob.JSON_NAME_ROW]:
                    db_columns[json_column[cfg.glob.JSON_NAME_COLUMN_NAME]] = json_column[
                        cfg.glob.JSON_NAME_COLUMN_VALUE
                    ]

                db.dml.insert_dbt_row(
                    table_name,
                    db_columns,
                )


# -----------------------------------------------------------------------------
# Update a database row based on its id column.
# -----------------------------------------------------------------------------
def update_dbt_id(
    table_name: str,
    id_where: int | sqlalchemy.Integer,
    columns: Columns,
) -> None:
    """Update a database row based on its id column.

    Args:
        table_name (str): sqlalchemy.Table name.
        id_where (int | sqlalchemy.Integer): Content of column id.
        columns (Columns): Pairs of column name and value.
    """
    dbt = sqlalchemy.Table(table_name, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

    with cfg.glob.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(sqlalchemy.update(dbt).where(dbt.c.id == id_where).values(columns))
        conn.close()
