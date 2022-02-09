"""Definition of the Global Constants, Types and Variables."""

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
CURRENT_DOCUMENT_STATUS: str = "n/a"
CURRENT_FILE_NAME: str = "n/a"
CURRENT_FILE_TYPE: str = "n/a"
CURRENT_STEM_NAME: str = "n/a"

DBC_ACTION_CODE: str = "action_code"
DBC_ACTION_TEXT: str = "action_text"
DBC_CREATED_AT: str = "created_at"
DBC_DOCUMENT_ID: str = "document_id"
DBC_FILE_NAME: str = "file_name"
DBC_FILE_TYPE: str = "file_type"
DBC_FUNCTION_NAME: str = "function_name"
DBC_ID: str = "id"
DBC_INBOX_ABS_NAME: str = "inbox_abs_name"
DBC_INBOX_CONFIG: str = "inbox_config"
DBC_INBOX_ACCEPTED_ABS_NAME: str = "inbox_accepted_abs_name"
DBC_INBOX_ACCEPTED_CONFIG: str = "inbox_accepted_config"
DBC_INBOX_REJECTED_ABS_NAME: str = "inbox_rejected_abs_name"
DBC_INBOX_REJECTED_CONFIG: str = "inbox_rejected_config"
DBC_MODIFIED_AT: str = "modified_at"
DBC_MODULE_NAME: str = "module_name"
DBC_RUN_ID: str = "run_id"
DBC_STATUS: str = "status"
DBC_STEM_NAME: str = "stem_name"
DBC_TOTAL_ACCEPTED: str = "total_accepted"
DBC_TOTAL_NEW: str = "total_new"
DBC_TOTAL_REJECTED: str = "total_rejected"
DBC_VERSION: str = "version"

DBT_DOCUMENT: str = "document"
DBT_JOURNAL: str = "journal"
DBT_RUN: str = "run"
DBT_VERSION: str = "version"

DCR_ARGV_0: str = "src/dcr/dcr.py"
DCR_CFG_DATABASE_FILE: str = "database_file"
DCR_CFG_DATABASE_URL: str = "database_url"
DCR_CFG_DCR_VERSION: str = "dcr_version"
DCR_CFG_DIRECTORY_INBOX: str = "directory_inbox"
DCR_CFG_DIRECTORY_INBOX_ACCEPTED: str = "directory_inbox_accepted"
DCR_CFG_DIRECTORY_INBOX_REJECTED: str = "directory_inbox_rejected"
DCR_CFG_FILE: str = "setup.cfg"
DCR_CFG_SECTION: str = "dcr"

FILE_ENCODING_DEFAULT: str = "utf-8"
FILE_TYPE_DOC: str = "doc"
FILE_TYPE_DOCX: str = "docx"
FILE_TYPE_JPEG: str = "jpeg"
FILE_TYPE_JPG: str = "jpg"
FILE_TYPE_PDF: str = "pdf"
FILE_TYPE_TXT: str = "txt"

JOURNAL_ACTION_01_001: str = (
    "01.001 New document detected in the 'inbox' file directory"
)
JOURNAL_ACTION_01_901: str = (
    "01.901 Document rejected because of unknown extension"
)

LOCALE: str = "en_US.UTF-8"
LOGGER_CFG_FILE: str = "logging_cfg.yaml"
LOGGER_END: str = "End"
LOGGER_FATAL_HEAD: str = "FATAL ERROR: program abort =====> "
LOGGER_FATAL_TAIL: str = " <===== FATAL ERROR"
LOGGER_PROGRESS_UPDATE: str = "Progress update "
LOGGER_START: str = "Start"

RUN_ACTION_ALL_COMPLETE: str = "all"
RUN_ACTION_CREATE_DB: str = "db_c"
RUN_ACTION_PROCESS_INBOX: str = "p_i"

STATUS_END: str = "end"
STATUS_INVALID_FILE_TYPE: str = "invalid_file_type"
STATUS_NEW: str = "new"
STATUS_NEXT_PANDOC: str = "next_pandoc"
STATUS_NEXT_TESSERACT: str = "next_tesseract"
STATUS_REJECTED: str = "rejected"
STATUS_START: str = "start"

# -----------------------------------------------------------------------------
# Global Type Definitions.
# -----------------------------------------------------------------------------
Columns: TypeAlias = list[Dict[str, Union[PathLike[str], str]]]

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
config: Dict[str, PathLike[str] | str] = {}

document_id: sqlalchemy.Integer | None = None

engine: Engine | None = None

inbox: PathLike[str] | str | None = None
inbox_accepted: PathLike[str] | str | None = None
inbox_rejected: PathLike[str] | str | None = None

metadata: MetaData | None = None

run_id: sqlalchemy.Integer | None = None

total_accepted: int = 0
total_new: int = 0
total_rejected: int = 0
