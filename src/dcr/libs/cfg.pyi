"""Library stub."""

from os import PathLike
from typing import Dict
from typing import TypeAlias
from typing import Union

import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
ACTION_ALL_COMPLETE: str
ACTION_CREATE_DB: str
ACTION_PROCESS_INBOX: str

DBC_ACTION: str
DBC_CREATED_AT: str
DBC_DOCUMENT_ID: str
DBC_FUNCTION: str
DBC_ID: str
DBC_INBOX_ABS_NAME: str
DBC_INBOX_CONFIG: str
DBC_INBOX_ACCEPTED_ABS_NAME: str
DBC_INBOX_ACCEPTED_CONFIG: str
DBC_INBOX_REJECTED_ABS_NAME: str
DBC_INBOX_REJECTED_CONFIG: str
DBC_MODIFIED_AT: str
DBC_MODULE: str
DBC_PACKAGE: str
DBC_RUN_ID: str
DBC_STATUS: str
DBC_STATUS_END: str
DBC_STATUS_START: str
DBC_TOTAL_ACCEPTED: str
DBC_TOTAL_NEW: str
DBC_TOTAL_REJECTED: str
DBC_VERSION: str

DBT_DOCUMENT: str
DBT_JOURNAL: str
DBT_RUN: str
DBT_VERSION: str

DCR_CFG_DATABASE: str
DCR_CFG_DATABASE_FILE: str
DCR_CFG_DATABASE_URL: str
DCR_CFG_DCR_VERSION: str
DCR_CFG_DIRECTORY_INBOX: str
DCR_CFG_DIRECTORY_INBOX_ACCEPTED: str
DCR_CFG_DIRECTORY_INBOX_REJECTED: str
DCR_CFG_FILE: str
DCR_CFG_SECTION: str

FILE_ENCODING_DEFAULT: str
FILE_EXTENSION_PDF: str

LOCALE: str
LOGGER_CFG_FILE: str
LOGGER_END: str
LOGGER_FATAL_HEAD: str
LOGGER_FATAL_TAIL: str
LOGGER_PROGRESS_UPDATE: str
LOGGER_START: str

# -----------------------------------------------------------------------------
# Global Type Definitions.
# -----------------------------------------------------------------------------
Columns: TypeAlias = list[Dict[str, Union[PathLike[str], str]]]

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
config: Dict[str, PathLike[str] | str]

engine: Engine

inbox: PathLike[str] | str
inbox_accepted: PathLike[str] | str
inbox_rejected: PathLike[str] | str

metadata: MetaData

run_id: sqlalchemy.Integer

total_accepted: int
total_new: int
total_rejected: int
