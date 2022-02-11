"""Definition of the Global Constants, Types and Variables."""
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

FILE_TYPE_BMP: str = "bmp"
FILE_TYPE_CSV: str = "csv"
FILE_TYPE_DOC: str = "doc"
FILE_TYPE_DOCX: str = "docx"
FILE_TYPE_EPUB: str = "epub"
FILE_TYPE_GIF: str = "gif"
FILE_TYPE_HTM: str = "htm"
FILE_TYPE_HTML: str = "html"
FILE_TYPE_JP2: str = "jp2"
FILE_TYPE_JPEG: str = "jpeg"
FILE_TYPE_JPG: str = "jpg"
FILE_TYPE_JSON: str = "json"
FILE_TYPE_MD: str = "md"
FILE_TYPE_ODT: str = "odt"
FILE_TYPE_PDF: str = "pdf"
FILE_TYPE_PMG: str = "png"
FILE_TYPE_PMN: str = "pnm"
FILE_TYPE_RST: str = "rst"
FILE_TYPE_RTF: str = "rdf"
FILE_TYPE_TIFF: str = "tiff"
FILE_TYPE_TXT: str = "txt"
FILE_TYPE_WEBP: str = "webp"

JOURNAL_ACTION_01_001: str = (
    "01.001 New document detected in the 'inbox' file directory"
)
JOURNAL_ACTION_11_001: str = (
    "11.001 Ready to convert the document to 'pdf' format using Pandoc"
)
JOURNAL_ACTION_11_002: str = (
    "11.002 Ready to convert the document to 'pdf' format using Tesseract OCR"
)
JOURNAL_ACTION_11_003: str = "11.003 Ready to parse the pdf document"
JOURNAL_ACTION_11_004: str = (
    "11.004 Ready to convert the document to 'pdf' format using Tesseract OCR"
    + " (after pdf2image processing)"
)
JOURNAL_ACTION_01_901: str = (
    "01.901 Document rejected because of unknown file extension='{extension}'"
)
JOURNAL_ACTION_01_902: str = (
    "01.902 Issue when moving '{source_file}' to '{target_file}' "
    + "- error: code='{error_code}' msg='{error_msg}'"
)
JOURNAL_ACTION_01_903: str = (
    "01.903 Issue with pdf2image processing of file '{source_file}' "
    + "- error: code='{error_code}' msg='{error_msg}'"
)
JOURNAL_ACTION_01_904: str = (
    "01.904 Runtime error with fitz.open() processing of file '{source_file}' "
    + "- error: msg='{error_msg}'"
)
JOURNAL_ACTION_01_905: str = (
    "01.905 Permission issue with file '{source_file}' "
    + "- error: code='{error_code}' msg='{error_msg}'"
)
JOURNAL_ACTION_01_906: str = (
    "01.905 File '{source_file}' can not be deleted"
    + "- error: code='{error_code}' msg='{error_msg}'"
)

LOCALE: str = "en_US.UTF-8"
LOGGER_CFG_FILE: str = "logging_cfg.yaml"
LOGGER_END: str = "End"
LOGGER_FATAL_HEAD: str = "FATAL ERROR: program abort =====> "
LOGGER_FATAL_TAIL: str = " <===== FATAL ERROR"
LOGGER_PROGRESS_UPDATE: str = "Progress update "
LOGGER_START: str = "Start"

OS_NT: str = "nt"
OS_POSIX: str = "posix"

RUN_ACTION_ALL_COMPLETE: str = "all"
RUN_ACTION_CREATE_DB: str = "db_c"
RUN_ACTION_PROCESS_INBOX: str = "p_i"

STATUS_COMPLETED: str = "completed"
STATUS_END: str = "end"
STATUS_INBOX: str = "inbox"
STATUS_PANDOC_ERROR: str = "pandoc_error"
STATUS_PANDOC_READY: str = "pandoc_ready"
STATUS_PARSER_ERROR: str = "parser_error"
STATUS_PARSER_READY: str = "parser_ready"
STATUS_PDF2IMAGE_ERROR: str = "pdf2image_error"
STATUS_REJECTED_ERROR: str = "rejected_error"
STATUS_REJECTED_FILE_ERROR: str = "rejected_file_error"
STATUS_REJECTED_FILE_EXTENSION: str = "rejected_file_extension"
STATUS_REJECTED_FILE_PERMISSION: str = "rejected_file_permission"
STATUS_START: str = "start"
STATUS_TESSERACT_ERROR: str = "tesseract_error"
STATUS_TESSERACT_READY: str = "tesseract_ready"


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

file_extension: str = ""
file_name: str = ""
file_type: str = ""

INBOX: PathLike[str] | str | None = None
inbox_accepted: PathLike[str] | str | None = None
inbox_rejected: PathLike[str] | str | None = None

logger: logging.Logger | None = None

metadata: MetaData | None = None

run_id: sqlalchemy.Integer | None = None

stem_name: str = ""

total_accepted: int = 0
total_erroneus: int = 0
total_new: int = 0
total_rejected: int = 0
