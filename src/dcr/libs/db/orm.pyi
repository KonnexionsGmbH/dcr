"""Library stub."""

from typing import Dict

import sqlalchemy.orm
from libs import cfg

# from typing import List

DB_DIALECT_POSTGRESQL: str

DBC_ACTION: str
DBC_ACTION_CODE: str
DBC_ACTION_TEXT: str
DBC_CREATED_AT: str
DBC_DOCUMENT_ID: str
DBC_DOCUMENT_ID_PARENT: str
DBC_FILE_NAME: str
DBC_FILE_TYPE: str
DBC_FUNCTION_NAME: str
DBC_ID: str
DBC_INBOX_ABS_NAME: str
DBC_INBOX_ACCEPTED_ABS_NAME: str
DBC_INBOX_REJECTED_ABS_NAME: str
DBC_MODIFIED_AT: str
DBC_MODULE_NAME: str
DBC_PACKAGE: str
DBC_RUN_ID: str
DBC_SHA256: str
DBC_STATUS: str
DBC_STEM_NAME: str
DBC_TOTAL_ERRONEOUS: str
DBC_TOTAL_OK_PROCESSED: str
DBC_TOTAL_TO_BE_PROCESSED: str
DBC_VERSION: str

DBT_DOCUMENT: str
DBT_JOURNAL: str
DBT_RUN: str
DBT_VERSION: str

def check_db_up_to_date() -> None: ...
def connect_db() -> None: ...

# def create_db_trigger_created_at(table_name: str) -> None: ...
# def create_db_trigger_modified_at(table_name: str) -> None: ...
# def create_db_triggers(table_names: List[str]) -> None: ...
def create_dbt_document(table_name: str) -> None: ...
def create_dbt_journal(table_name: str) -> None: ...
def create_dbt_run(table_name: str) -> None: ...
def create_dbt_version(
    table_name: str,
) -> None: ...
def create_schema() -> None: ...
def disconnect_db() -> None: ...
def get_db_url() -> str: ...
def insert_dbt_row(
    table_name: str,
    columns: cfg.Columns,
) -> sqlalchemy.Integer: ...
def prepare_connect_db() -> None: ...
def select_dbt_id_last(table_name: str) -> int | sqlalchemy.Integer: ...
def select_document_file_name_sha256(
    document_id: sqlalchemy.Integer, sha256: str
) -> str | None: ...
def select_run_run_id_last() -> int | sqlalchemy.Integer: ...
def select_version_version_unique() -> str: ...
def update_dbt_id(
    table_name: str,
    id_where: sqlalchemy.Integer,
    columns: Dict[str, str],
) -> None: ...
def update_document_status(
    document_columns: cfg.Columns,
    journal_columns: cfg.Columns,
) -> None: ...
def update_version_version(
    version: str,
) -> None: ...
