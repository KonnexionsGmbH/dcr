"""Library stub."""
import logging
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
DCR_ARGV_0: str

DCR_CFG_DATABASE_FILE: str
DCR_CFG_DATABASE_URL: str
DCR_CFG_DB_CONNECTION_PORT: str
DCR_CFG_DB_CONNECTION_PREFIX: str
DCR_CFG_DB_CONTAINER_PORT: str
DCR_CFG_DB_DATABASE: str
DCR_CFG_DB_DATABASE_ADMIN: str
DCR_CFG_DB_DIALECT: str
DCR_CFG_DB_HOST: str
DCR_CFG_DB_PASSWORD: str
DCR_CFG_DB_PASSWORD_ADMIN: str
DCR_CFG_DB_SCHEMA: str
DCR_CFG_DB_USER: str
DCR_CFG_DB_USER_ADMIN: str
DCR_CFG_DCR_VERSION: str
DCR_CFG_DIRECTORY_INBOX: str
DCR_CFG_DIRECTORY_INBOX_ACCEPTED: str
DCR_CFG_DIRECTORY_INBOX_REJECTED: str
DCR_CFG_DB_DOCKER_CONTAINER: str
DCR_CFG_FILE: str
DCR_CFG_IGNORE_DUPLICATES: str
DCR_CFG_PDF2IMAGE_TYPE: str
DCR_CFG_PDF2IMAGE_TYPE_JPEG: str
DCR_CFG_PDF2IMAGE_TYPE_PNG: str
DCR_CFG_SECTION: str
DCR_CFG_SECTION_DEV: str
DCR_CFG_SECTION_PROD: str
DCR_CFG_SECTION_TEST: str
DCR_CFG_VERBOSE: str

DCR_ENVIRONMENT_TYPE: str

ENVIRONMENT_TYPE_DEV: str
ENVIRONMENT_TYPE_PROD: str
ENVIRONMENT_TYPE_TEST: str

FILE_ENCODING_DEFAULT: str

INFORMATION_NOT_YET_AVAILABLE: str

JOURNAL_ACTION_01_001: str
JOURNAL_ACTION_01_901: str
JOURNAL_ACTION_01_902: str
JOURNAL_ACTION_01_903: str
JOURNAL_ACTION_01_904: str
JOURNAL_ACTION_01_905: str
JOURNAL_ACTION_01_906: str
JOURNAL_ACTION_11_001: str
JOURNAL_ACTION_11_002: str
JOURNAL_ACTION_11_003: str
JOURNAL_ACTION_11_004: str
JOURNAL_ACTION_11_005: str
JOURNAL_ACTION_21_001: str
JOURNAL_ACTION_21_002: str
JOURNAL_ACTION_21_003: str
JOURNAL_ACTION_21_901: str
JOURNAL_ACTION_21_902: str

LOCALE: str
LOGGER_CFG_FILE: str
LOGGER_END: str
LOGGER_FATAL_HEAD: str
LOGGER_FATAL_TAIL: str
LOGGER_PROGRESS_UPDATE: str
LOGGER_START: str

OS_NT: str
OS_POSIX: str

RUN_ACTION_ALL_COMPLETE: str
RUN_ACTION_CREATE_DB: str
RUN_ACTION_PDF_2_IMAGE: str
RUN_ACTION_PROCESS_INBOX: str
RUN_ACTION_UPGRADE_DB: str

STATUS_COMPLETED: str
STATUS_END: str
STATUS_PANDOC_ERROR: str
STATUS_PANDOC_READY: str
STATUS_PARSER_ERROR: str
STATUS_PARSER_READY: str
STATUS_REJECTED_ERROR: str
STATUS_REJECTED_FILE_DUPL: str
STATUS_REJECTED_FILE_ERROR: str
STATUS_REJECTED_FILE_EXT: str
STATUS_REJECTED_FILE_PERMISSION: str
STATUS_REJECTED_NO_PDF_FORMAT: str
STATUS_START: str
STATUS_START_INBOX: str
STATUS_START_PDF2IMAGE: str
STATUS_TESSERACT_ERROR: str
STATUS_TESSERACT_PDF_END: str
STATUS_TESSERACT_PDF_ERROR: str
STATUS_TESSERACT_PDF_READY: str
STATUS_TESSERACT_READY: str

VERBOSE_TRUE: str

# -----------------------------------------------------------------------------
# Global Type Definitions.
# -----------------------------------------------------------------------------
Columns: TypeAlias = Dict[str, Union[PathLike[str], sqlalchemy.Integer, str]]

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
config: Dict[str, PathLike[str] | str]

db_current_database: str
db_current_user: str

directory_inbox: PathLike[str] | str
directory_inbox_accepted: PathLike[str] | str
directory_inbox_rejected: PathLike[str] | str

document_child_file_name: str
document_child_file_name_abs: str
document_child_file_name_orig: str
document_child_file_type: str
document_child_no: int
document_child_stem_name: str
document_file_extension: str
document_file_name: str
document_file_name_abs_orig: str
document_file_name_accepted_abs: str
document_file_name_rejected_abs: str
document_file_type: str
document_id: sqlalchemy.Integer
document_inbox_accepted_abs_name: str
document_sha256: str
document_status: str
document_stem_name: str
document_stem_name_orig: str

engine: Engine
environment_type: str

is_docker_container: bool
is_ignore_duplicates: bool
is_verbose: bool

logger: logging.Logger

metadata: MetaData | None

pdf2image_type: str

run_action: str
run_id: sqlalchemy.Integer
run_run_id: sqlalchemy.Integer

total_erroneous: int
total_generated: int
total_ok_processed: int
total_rejected: int
total_status_error: int
total_status_ready: int
total_to_be_processed: int
