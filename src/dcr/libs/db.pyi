"""Library stub."""

from typing import Dict
from typing import List

import sqlalchemy.orm
from libs import cfg

def check_db_up_to_date() -> None: ...
def connect_db() -> None: ...
def connect_db_core() -> None: ...
def create_database() -> None: ...
def create_db_trigger_created_at(table_name: str) -> None: ...
def create_db_trigger_modified_at(table_name: str) -> None: ...
def create_db_triggers(table_names: List[str]) -> None: ...
def create_dbt_document(table_name: str) -> None: ...
def create_dbt_journal(table_name: str) -> None: ...
def create_dbt_run(table_name: str) -> None: ...
def create_dbt_version(
    table_name: str,
) -> None: ...
def disconnect_db() -> None: ...
def get_db_file_name() -> str: ...
def get_db_url() -> str: ...
def insert_dbt_document_row() -> None: ...
def insert_dbt_journal_row(
    action: str,
    function_name: str,
    module_name: str,
) -> None: ...
def insert_dbt_row(table: str, columns: cfg.Columns) -> None: ...
def insert_dbt_run_row() -> None: ...
def insert_dbt_version_row() -> None: ...
def select_dbt_id_last(table_name: str) -> sqlalchemy.Integer: ...
def select_version_version_unique() -> str: ...
def update_dbt_id(
    table_name: str,
    id_where: sqlalchemy.Integer,
    columns: Dict[str, str],
) -> None: ...
def update_document_status(
    action: str,
    function_name: str,
    module_name: str,
    status: str,
) -> None: ...
def upgrade_db() -> None: ...