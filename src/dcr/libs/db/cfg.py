"""Database Configuration Data.

Returns:
    [type]: None.
"""
from typing import List

from psycopg2.extensions import connection
from psycopg2.extensions import cursor
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
DB_DIALECT_POSTGRESQL: str = "postgresql"

DBC_ACTION: str = "action"
DBC_ACTION_CODE: str = "action_code"
DBC_ACTION_TEXT: str = "action_text"
DBC_CHILD_NO: str = "child_no"
DBC_CREATED_AT: str = "created_at"
DBC_DIRECTORY_NAME: str = "directory_name"
DBC_DIRECTORY_TYPE: str = "directory_type"
DBC_DOCUMENT_ID: str = "document_id"
DBC_DOCUMENT_ID_BASE: str = "document_id_base"
DBC_DOCUMENT_ID_PARENT: str = "document_id_parent"
DBC_ERROR_CODE: str = "error_code"
DBC_FILE_NAME: str = "file_name"
DBC_FILE_TYPE: str = "file_type"
DBC_FUNCTION_NAME: str = "function_name"
DBC_ID: str = "id"
DBC_MODIFIED_AT: str = "modified_at"
DBC_MODULE_NAME: str = "module_name"
DBC_NEXT_STEP: str = "next_step"
DBC_RUN_ID: str = "run_id"
DBC_SHA256: str = "sha256"
DBC_STATUS: str = "status"
DBC_STEM_NAME: str = "stem_name"
DBC_TOTAL_ERRONEOUS: str = "total_erroneous"
DBC_TOTAL_OK_PROCESSED: str = "total_ok_processed"
DBC_TOTAL_TO_BE_PROCESSED: str = "total_to_be_processed"
DBC_VERSION: str = "version"

DBT_DOCUMENT: str = "document"
DBT_JOURNAL: str = "journal"
DBT_RUN: str = "run"
DBT_VERSION: str = "version"

DOCUMENT_DIRECTORY_TYPE_INBOX: str = "inbox"
DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED: str = "inbox_accepted"
DOCUMENT_DIRECTORY_TYPE_INBOX_REJECTED: str = "inbox_rejected"

DOCUMENT_ERROR_CODE_REJECTED_ERROR: str = "rejected_error"
DOCUMENT_ERROR_CODE_REJECTED_FILE_DUPL: str = "Duplicate file"
DOCUMENT_ERROR_CODE_REJECTED_FILE_ERROR: str = "rejected_file_error"
DOCUMENT_ERROR_CODE_REJECTED_FILE_EXT: str = "Unknown file extension"
DOCUMENT_ERROR_CODE_REJECTED_FILE_MOVE: str = "Issue with file move"
DOCUMENT_ERROR_CODE_REJECTED_FILE_RIGHTS: str = "Issue with file permissions"
DOCUMENT_ERROR_CODE_REJECTED_NO_PDF_FORMAT: str = "No 'pdf' format"
DOCUMENT_ERROR_CODE_REJECTED_PDF2IMAGE: str = "Issue with pdf2image"

DOCUMENT_FILE_TYPE_JPG: str = "jpg"
DOCUMENT_FILE_TYPE_PANDOC: List[str] = [
    "csv",
    "doc",
    "docx",
    "epub",
    "htm",
    "html",
    "json",
    "md",
    "odt",
    "rst",
    "rtf",
    "txt",
]
DOCUMENT_FILE_TYPE_PDF: str = "pdf"
DOCUMENT_FILE_TYPE_PNG: str = "png"
DOCUMENT_FILE_TYPE_TESSERACT: List[str] = [
    "bmp",
    "gif",
    "jfif",
    "jiff",
    "jpeg",
    "jpg",
    "pip",
    "pjpeg",
    "pmn",
    "png",
    "tif",
    "tiff",
    "webp",
]

DOCUMENT_NEXT_STEP_PANDOC: str = "Pandoc"
DOCUMENT_NEXT_STEP_PDF2IMAGE: str = "pdf2image"
DOCUMENT_NEXT_STEP_PDFLIB: str = "PDFlib TET"
DOCUMENT_NEXT_STEP_TESSERACT: str = "Tesseract OCR"

DOCUMENT_STATUS_ABORT: str = "abort"
DOCUMENT_STATUS_END: str = "end"
DOCUMENT_STATUS_ERROR: str = "error"
DOCUMENT_STATUS_START: str = "start"

JOURNAL_ACTION_01_001: str = (
    "01.001 Start (p_i): Document file '{file_name}' detected " + "in the 'inbox' file directory."
)
JOURNAL_ACTION_01_002: str = (
    "01.002 End   (p_i): Document file '{source_file}' successfully moved to file '{target_file}'."
)
JOURNAL_ACTION_01_003: str = (
    "01.003 Next  (p_i): Ready to convert document file '{file_name}' "
    + "to '{type}' format using pdf2image."
)
JOURNAL_ACTION_01_901: str = (
    "01.901 Issue (p_i): Document rejected because of unknown file extension='{extension}'."
)
JOURNAL_ACTION_01_902: str = (
    "01.902 Issue (p_i): Moving '{source_file}' to '{target_file}' "
    + "- error: code='{error_code}' msg='{error_msg}'."
)
JOURNAL_ACTION_01_903: str = (
    "01.903 Issue (p_i): Runtime error with fitz.open() processing of file '{source_file}' "
    + "- error: '{error_msg}'."
)
JOURNAL_ACTION_01_904: str = (
    "01.904 Issue (p_i): File permission with file '{source_file}' "
    + "- error: code='{error_code}' msg='{error_msg}'."
)
JOURNAL_ACTION_01_905: str = (
    "01.905 Issue (p_i): The same file has probably already been processed "
    + "once under the file name '{file_name}'."
)
JOURNAL_ACTION_11_001: str = "11.001 Ready to convert the document to 'pdf' format using Pandoc."
JOURNAL_ACTION_11_002: str = (
    "11.002 Ready to convert the document to 'pdf' format using Tesseract OCR."
)
JOURNAL_ACTION_11_003: str = "11.003 Ready to process the 'pdf' document using PDFlib TET."
JOURNAL_ACTION_21_001: str = (
    "21.001 Start (p_2_i): The document file '{file_name}' must be converted into image file(s) "
    + "for further processing."
)
JOURNAL_ACTION_21_002: str = (
    "21.002 End   (p_2_i): The document file '{file_name}' has been successfully converted "
    + "to {child_no} image file(s)."
)
JOURNAL_ACTION_21_003: str = (
    "21.003 Next  (p_2_i): The created image file '{file_name}' "
    + "is ready to be processed with Tesseract OCR."
)
JOURNAL_ACTION_21_901: str = (
    "21.901 Issue (p_2_i): The 'pdf' document '{file_name}' cannot be converted to an "
    + "image format - error: '{error_msg}'."
)
JOURNAL_ACTION_21_902: str = (
    "21.902 Issue (p_2_i): The child image file number '{child_no}' with file name "
    + "'{file_name}' cannot be stored "
    + "- error: code='{error_code}' msg='{error_msg}'."
)

RUN_STATUS_END: str = "end"
RUN_STATUS_START: str = "start"

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------

db_current_database: str
db_current_user: str
db_driver_conn: connection | None = None
db_driver_cur: cursor | None = None
db_orm_engine: Engine | None = None
db_orm_metadata: MetaData | None = None
