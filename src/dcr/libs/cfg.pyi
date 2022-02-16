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
DCR_CFG_DCR_VERSION: str
DCR_CFG_DIRECTORY_INBOX: str
DCR_CFG_DIRECTORY_INBOX_ACCEPTED: str
DCR_CFG_DIRECTORY_INBOX_REJECTED: str
DCR_CFG_FILE: str
DCR_CFG_SECTION: str

FILE_ENCODING_DEFAULT: str

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
STATUS_INBOX: str
STATUS_PANDOC_ERROR: str
STATUS_PANDOC_READY: str
STATUS_PARSER_ERROR: str
STATUS_PARSER_READY: str
STATUS_REJECTED_ERROR: str
STATUS_REJECTED_FILE_ERROR: str
STATUS_REJECTED_FILE_EXTENSION: str
STATUS_REJECTED_FILE_PERMISSION: str
STATUS_REJECTED_NO_PDF_FORMAT: str
STATUS_START: str
STATUS_TESSERACT_ERROR: str
STATUS_TESSERACT_READY: str
STATUS_TESSERACT_PDF_ERROR: str
STATUS_TESSERACT_PDF_READY: str

# -----------------------------------------------------------------------------
# Global Type Definitions.
# -----------------------------------------------------------------------------
Columns: TypeAlias = list[Dict[str, Union[PathLike[str], str]]]

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
config: Dict[str, PathLike[str] | str]

directory_inbox: PathLike[str] | str
directory_inbox_accepted: PathLike[str] | str
directory_inbox_rejected: PathLike[str] | str
document_id: sqlalchemy.Integer

engine: Engine | None

file_extension: str
file_name: str
file_type: str

logger: logging.Logger | None
metadata: MetaData

run_action: str
run_id: sqlalchemy.Integer
run_run_id: sqlalchemy.Integer

sha256: str
stem_name: str

total_erroneous: int
total_ok_processed: int
total_rejected: int
total_status_error: int
total_status_ready: int
total_to_be_processed: int
