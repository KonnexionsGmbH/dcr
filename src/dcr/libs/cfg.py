"""Module cfg: Definition of the Global Constants, Types and Variables."""
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
DCR_ARGV_0: str = "src/dcr/dcr.py"

DCR_CFG_DATABASE_FILE: str = "database_file"
DCR_CFG_DATABASE_URL: str = "database_url"
DCR_CFG_DB_CONNECTION_PORT: str = "db_connection_port"
DCR_CFG_DB_CONNECTION_PREFIX: str = "db_connection_prefix"
DCR_CFG_DB_CONTAINER_PORT: str = "db_container_port"
DCR_CFG_DB_DATABASE: str = "db_database"
DCR_CFG_DB_DATABASE_ADMIN: str = "db_database_admin"
DCR_CFG_DB_DIALECT: str = "db_dialect"
DCR_CFG_DB_HOST: str = "db_host"
DCR_CFG_DB_PASSWORD: str = "db_password"
DCR_CFG_DB_PASSWORD_ADMIN: str = "db_password_admin"
DCR_CFG_DB_SCHEMA: str = "db_schema"
DCR_CFG_DB_USER: str = "db_user"
DCR_CFG_DB_USER_ADMIN: str = "db_user_admin"
DCR_CFG_DCR_VERSION: str = "dcr_version"
DCR_CFG_DIRECTORY_INBOX: str = "directory_inbox"
DCR_CFG_DIRECTORY_INBOX_ACCEPTED: str = "directory_inbox_accepted"
DCR_CFG_DIRECTORY_INBOX_REJECTED: str = "directory_inbox_rejected"
DCR_CFG_FILE: str = "setup.cfg"
DCR_CFG_IGNORE_DUPLICATES: str = "ignore_duplicates"
DCR_CFG_PDF2IMAGE_TYPE: str = "pdf2image_type"
DCR_CFG_PDF2IMAGE_TYPE_JPEG: str = "JPEG"
DCR_CFG_PDF2IMAGE_TYPE_PNG: str = "PNG"
DCR_CFG_SECTION: str = "dcr"
DCR_CFG_VERBOSE: str = "verbose"

FILE_ENCODING_DEFAULT: str = "utf-8"

INFORMATION_NOT_YET_AVAILABLE: str = "n/a"

JOURNAL_ACTION_01_001: str = "01.001 New document detected in the 'inbox' file directory"
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
    + "- error: '{error_msg}'"
)
JOURNAL_ACTION_01_905: str = (
    "01.905 Permission issue with file '{source_file}' "
    + "- error: code='{error_code}' msg='{error_msg}'"
)
JOURNAL_ACTION_01_906: str = (
    "01.905 File '{source_file}' can not be deleted "
    + "- error: code='{error_code}' msg='{error_msg}'"
)
JOURNAL_ACTION_11_001: str = "11.001 Ready to convert the document to 'pdf' format using Pandoc"
JOURNAL_ACTION_11_002: str = (
    "11.002 Ready to convert the document to 'pdf' format using Tesseract OCR"
)
JOURNAL_ACTION_11_003: str = "11.003 Ready to parse the pdf document"
JOURNAL_ACTION_11_004: str = (
    "11.004 Ready to convert the document to 'pdf' format using Tesseract OCR "
    + "(after pdf2image processing)"
)
JOURNAL_ACTION_11_005: str = "11.005 Ready to prepare the pdf document for Tesseract OCR"
JOURNAL_ACTION_21_001: str = (
    "21.001 This 'pdf' document must be converted into an image format " + "for further processing"
)
JOURNAL_ACTION_21_002: str = (
    "21.002 The 'pdf' document has been successfully converted to " + "{child_no} image files."
)
JOURNAL_ACTION_21_003: str = (
    "21.003 Ready to convert the document to 'pdf' format using Tesseract OCR"
)
JOURNAL_ACTION_21_901: str = (
    "21.901 The 'pdf' document '{file_name}' cannot be converted to an "
    + "image format - error: '{error_msg}'"
)
JOURNAL_ACTION_21_902: str = (
    "21.902 The child image file number '{child_no}' with file name "
    + "'{file_name}' cannot be stored "
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
RUN_ACTION_PDF_2_IMAGE: str = "p_2_i"
RUN_ACTION_PROCESS_INBOX: str = "p_i"
RUN_ACTION_UPGRADE_DB: str = "db_u"

STATUS_COMPLETED: str = "completed"
STATUS_END: str = "end"  # run
STATUS_PANDOC_ERROR: str = "pandoc_error"
STATUS_PANDOC_READY: str = "pandoc_ready"
STATUS_PARSER_ERROR: str = "parser_error"
STATUS_PARSER_READY: str = "parser_ready"
STATUS_REJECTED_ERROR: str = "rejected_error"
STATUS_REJECTED_FILE_DUPL: str = "rejected_file_duplicate"
STATUS_REJECTED_FILE_ERROR: str = "rejected_file_error"
STATUS_REJECTED_FILE_EXT: str = "rejected_file_extension"
STATUS_REJECTED_FILE_PERMISSION: str = "rejected_file_permission"
STATUS_REJECTED_NO_PDF_FORMAT: str = "rejected_no_pdf_format"
STATUS_START: str = "start"  # run
STATUS_START_INBOX: str = "start_inbox"
STATUS_START_PDF2IMAGE: str = "start_pdf2image"
STATUS_TESSERACT_ERROR: str = "tesseract_error"
STATUS_TESSERACT_PDF_END: str = "tesseract_pdf_end"
STATUS_TESSERACT_PDF_ERROR: str = "tesseract_pdf_error"
STATUS_TESSERACT_PDF_READY: str = "tesseract_pdf_ready"
STATUS_TESSERACT_READY: str = "tesseract_ready"


# -----------------------------------------------------------------------------
# Global Type Definitions.
# -----------------------------------------------------------------------------
Columns: TypeAlias = Dict[str, Union[PathLike[str], sqlalchemy.Integer, str]]

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
config: Dict[str, PathLike[str] | str] = {}

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
document_child_stem_name_orig: str
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

engine: Engine

is_ignore_duplicates: bool
is_verbose: bool = True

logger: logging.Logger

metadata: MetaData | None = None

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
