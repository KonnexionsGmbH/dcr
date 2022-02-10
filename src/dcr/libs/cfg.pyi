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
DBC_ACTION_CODE: str
DBC_ACTION_TEXT: str
DBC_CREATED_AT: str
DBC_DOCUMENT_ID: str
DBC_FILE_NAME: str
DBC_FILE_TYPE: str
DBC_FUNCTION_NAME: str
DBC_ID: str
DBC_INBOX_ABS_NAME: str
DBC_INBOX_CONFIG: str
DBC_INBOX_ACCEPTED_ABS_NAME: str
DBC_INBOX_ACCEPTED_CONFIG: str
DBC_INBOX_REJECTED_ABS_NAME: str
DBC_INBOX_REJECTED_CONFIG: str
DBC_MODIFIED_AT: str
DBC_MODULE_NAME: str
DBC_PACKAGE: str
DBC_RUN_ID: str
DBC_STATUS: str
DBC_STEM_NAME: str
DBC_TOTAL_ACCEPTED: str
DBC_TOTAL_NEW: str
DBC_TOTAL_REJECTED: str
DBC_VERSION: str

DBT_DOCUMENT: str
DBT_JOURNAL: str
DBT_RUN: str
DBT_VERSION: str

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

FILE_TYPE_BMP: str
FILE_TYPE_CSV: str
FILE_TYPE_DOC: str
FILE_TYPE_DOCX: str
FILE_TYPE_EPUB: str
FILE_TYPE_GIF: str
FILE_TYPE_HTM: str
FILE_TYPE_HTML: str
FILE_TYPE_JP2: str
FILE_TYPE_JPEG: str
FILE_TYPE_JPG: str
FILE_TYPE_JSON: str
FILE_TYPE_MD: str
FILE_TYPE_ODT: str
FILE_TYPE_PDF: str
FILE_TYPE_PMG: str
FILE_TYPE_PMN: str
FILE_TYPE_RST: str
FILE_TYPE_RTF: str
FILE_TYPE_TIFF: str
FILE_TYPE_TXT: str
FILE_TYPE_WEBP: str

JOURNAL_ACTION_01_001: str
JOURNAL_ACTION_11_001: str
JOURNAL_ACTION_11_002: str
JOURNAL_ACTION_11_003: str
JOURNAL_ACTION_11_004: str
JOURNAL_ACTION_01_901: str
JOURNAL_ACTION_01_902: str
JOURNAL_ACTION_01_903: str

LOCALE: str
LOGGER_CFG_FILE: str
LOGGER_END: str
LOGGER_FATAL_HEAD: str
LOGGER_FATAL_TAIL: str
LOGGER_PROGRESS_UPDATE: str
LOGGER_START: str

RUN_ACTION_ALL_COMPLETE: str
RUN_ACTION_CREATE_DB: str
RUN_ACTION_PROCESS_INBOX: str

# STATUS_INVALID_FILE_TYPE: str
# STATUS_REJECTED: str

STATUS_COMPLETED: str
STATUS_END: str
STATUS_INBOX: str
STATUS_PANDOC_ERROR: str
STATUS_PANDOC_READY: str
STATUS_PARSER_ERROR: str
STATUS_PARSER_READY: str
STATUS_PDF2IMAGE_ERROR: str
STATUS_REJECTED_ERROR: str
STATUS_REJECTED_FILE_ERROR: str
STATUS_REJECTED_FILE_TYPE: str
STATUS_START: str
STATUS_TESSERACT_ERROR: str
STATUS_TESSERACT_READY: str

# -----------------------------------------------------------------------------
# Global Type Definitions.
# -----------------------------------------------------------------------------
Columns: TypeAlias = list[Dict[str, Union[PathLike[str], str]]]

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
config: Dict[str, PathLike[str] | str]

document_id: sqlalchemy.Integer

engine: Engine | None

file_name: str
file_type: str

INBOX: PathLike[str] | str
inbox_accepted: PathLike[str] | str
inbox_rejected: PathLike[str] | str

logger: logging.Logger | None
metadata: MetaData

run_id: sqlalchemy.Integer

stem_name: str

total_accepted: int
total_new: int
total_rejected: int
