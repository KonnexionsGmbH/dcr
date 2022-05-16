"""Library Stub."""
import os
import pathlib
from typing import Dict
from typing import Tuple
from typing import TypeAlias

import sqlalchemy.engine

Columns: TypeAlias = Dict[
    str, bool | sqlalchemy.Boolean | int | sqlalchemy.Integer | str | os.PathLike[str] | sqlalchemy.String | None
]

ColumnValues: TypeAlias = Tuple[
    bool | sqlalchemy.Boolean | int | sqlalchemy.Integer | str | os.PathLike[str] | sqlalchemy.String | None
]

def delete_dbt_id(
    table_name: str,
    id_where: int | sqlalchemy.Integer,
) -> None: ...
def insert_dbt_row(
    table_name: str,
    columns: Columns,
) -> sqlalchemy.Integer: ...
def load_db_data_from_json(initial_database_data: pathlib.Path) -> None: ...
def update_dbt_id(
    table_name: str,
    id_where: int | sqlalchemy.Integer,
    columns: Columns,
) -> None: ...
