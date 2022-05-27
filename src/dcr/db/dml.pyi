"""Library Stub."""
import os
import pathlib
from typing import Dict
from typing import Tuple
from typing import TypeAlias

import sqlalchemy.engine

Columns: TypeAlias = Dict[str, bool | int | None | os.PathLike[str] | str]

ColumnValues: TypeAlias = Tuple[bool | int | None | os.PathLike[str] | str]

def delete_dbt_id(
    table_name: str,
    id_where: int,
) -> None: ...
def insert_dbt_row(
    table_name: str,
    columns: Columns,
) -> int: ...
def load_db_data_from_json(initial_database_data: pathlib.Path) -> None: ...
def update_dbt_id(
    table_name: str,
    id_where: int,
    columns: Columns,
) -> None: ...
