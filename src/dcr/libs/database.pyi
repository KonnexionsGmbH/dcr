"""Library stub."""
import logging
from os import PathLike
from typing import Dict
from typing import Union

import sqlalchemy.orm
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

Columns: list[Dict[str, Union[PathLike[str], str]]]

DB_ENGINE: str
DB_METADATA: str
DB_REFLECT: str

DBC_ACTION: str
DBC_CREATED_AT: str
DBC_DOCUMENT_ID: str
DBC_FUNCTION: str
DBC_ID: str
DBC_MODIFIED_AT: str
DBC_MODULE: str
DBC_PACKAGE: str
DBC_STATUS: str
DBC_VERSION: str

DBT_DOCUMENT: str
DBT_JOURNAL: str
DBT_VERSION: str

ENGINE: Engine

METADATA: MetaData

def check_database_version(logger: logging.Logger) -> None: ...
def create_database(logger: logging.Logger) -> None: ...
def create_or_upgrade_database(logger: logging.Logger) -> None: ...
def create_table_document() -> None: ...
def create_table_journal() -> None: ...
def create_table_version() -> sqlalchemy.Table: ...
def select_version_unique(logger: logging.Logger) -> str: ...
def insert_table(
    logger: logging.Logger, table: str, columns: Columns
) -> None: ...
def upgrade_database(logger: logging.Logger) -> None: ...
