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
FILE_TYPE_RTF: str = "rtf"
FILE_TYPE_TIFF: str = "tiff"
FILE_TYPE_TXT: str = "txt"
FILE_TYPE_WEBP: str = "webp"

JOURNAL_ACTION_01_001: str = (
    "01.001 New document detected in the 'inbox' file directory"
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
JOURNAL_ACTION_11_005: str = (
    "11.005 Ready to prepare the pdf document for Tesseract OCR"
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
STATUS_REJECTED_ERROR: str = "rejected_error"
STATUS_REJECTED_FILE_ERROR: str = "rejected_file_error"
STATUS_REJECTED_FILE_EXTENSION: str = "rejected_file_extension"
STATUS_REJECTED_FILE_PERMISSION: str = "rejected_file_permission"
STATUS_REJECTED_NO_PDF_FORMAT: str = "rejected_no_pdf_format"
STATUS_START: str = "start"
STATUS_TESSERACT_ERROR: str = "tesseract_error"
STATUS_TESSERACT_READY: str = "tesseract_ready"
STATUS_TESSERACT_PDF_ERROR: str = "tesseract_pdf_error"
STATUS_TESSERACT_PDF_READY: str = "tesseract_pdf_ready"


# -----------------------------------------------------------------------------
# Global Type Definitions.
# -----------------------------------------------------------------------------
Columns: TypeAlias = list[Dict[str, Union[PathLike[str], str]]]

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
config: Dict[str, PathLike[str] | str] = {}

directory_inbox: PathLike[str] | str | None = None
directory_inbox_accepted: PathLike[str] | str | None = None
directory_inbox_rejected: PathLike[str] | str | None = None
document_id: sqlalchemy.Integer | None = None

engine: Engine | None = None

file_extension: str = ""
file_name: str = ""
file_type: str = ""

logger: logging.Logger | None = None

metadata: MetaData | None = None

run_id: sqlalchemy.Integer | None = None

stem_name: str = ""

total_accepted: int
total_erroneous: int
total_new: int
total_rejected: int
