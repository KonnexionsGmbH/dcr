"""Module libs.cfg: DCR Configuration Data."""
import logging
from datetime import datetime
from decimal import Decimal
from os import PathLike
from typing import Dict
from typing import TypeAlias
from typing import Union

import sqlalchemy

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
DCR_CFG_INITIAL_DATABASE_DATA: str = "initial_database_data"
DCR_CFG_PDF2IMAGE_TYPE: str = "pdf2image_type"
DCR_CFG_PDF2IMAGE_TYPE_JPEG: str = "jpeg"
DCR_CFG_PDF2IMAGE_TYPE_PNG: str = "png"
DCR_CFG_SECTION: str = "dcr"
DCR_CFG_SECTION_DEV: str = "dcr_dev"
DCR_CFG_SECTION_PROD: str = "dcr_prod"
DCR_CFG_SECTION_TEST: str = "dcr_test"
DCR_CFG_TESSERACT_TIMEOUT: str = "tesseract_timeout"
DCR_CFG_VERBOSE: str = "verbose"
DCR_CFG_VERBOSE_PARSER: str = "verbose_parser"

DCR_ENVIRONMENT_TYPE: str = "DCR_ENVIRONMENT_TYPE"

ENVIRONMENT_TYPE_DEV: str = "dev"
ENVIRONMENT_TYPE_PROD: str = "prod"
ENVIRONMENT_TYPE_TEST: str = "test"

FILE_ENCODING_DEFAULT: str = "utf-8"

INFORMATION_NOT_YET_AVAILABLE: str = "n/a"

LOCALE: str = "en_US.UTF-8"
LOGGER_CFG_FILE: str = "logging_cfg.yaml"
LOGGER_END: str = "End"
LOGGER_FATAL_HEAD: str = "FATAL ERROR: program abort =====> "
LOGGER_FATAL_TAIL: str = " <===== FATAL ERROR"
LOGGER_PROGRESS_UPDATE: str = "Progress update "
LOGGER_START: str = "Start"

OS_NT: str = "nt"
OS_POSIX: str = "posix"

PANDIOC_PDF_ENGINE_LULATEX: str = "lulatex"
PANDIOC_PDF_ENGINE_XELATEX: str = "xelatex"

PARSE_NAME_SPACE: str = "{http://www.pdflib.com/XML/TET5/TET-5.0}"
PARSE_TAG_A: str = "A"
PARSE_TAG_ANNOTATIONS: str = "Annotations"
PARSE_TAG_AUTHOR: str = "Author"
PARSE_TAG_BOOKMARKS: str = "Bookmarks"
PARSE_TAG_BOX: str = "Box"
PARSE_TAG_CONTENT: str = "Content"
PARSE_TAG_CREATION: str = "Creation"
PARSE_TAG_CREATION_DATE: str = "CreationDate"
PARSE_TAG_CREATOR: str = "Creator"
PARSE_TAG_CUSTOM: str = "Custom"
PARSE_TAG_DESTINATIONS: str = "Destinations"
PARSE_TAG_DOCUMENT: str = "Document"
PARSE_TAG_DOC_INFO: str = "DocInfo"
PARSE_TAG_FROM: int = len(PARSE_NAME_SPACE)
PARSE_TAG_GRAPHICS: str = "Graphics"
PARSE_TAG_LINE: str = "Line"
PARSE_TAG_METADATA: str = "Metadata"
PARSE_TAG_MOD_DATE: str = "ModDate"
PARSE_TAG_OPTIONS: str = "Options"
PARSE_TAG_PAGE: str = "Page"
PARSE_TAG_PAGES: str = "Pages"
PARSE_TAG_PARA: str = "Para"
PARSE_TAG_PLACED_IMAGE: str = "PlacedImage"
PARSE_TAG_PRODUCER: str = "Producer"
PARSE_TAG_RESOURCES: str = "Resources"
PARSE_TAG_TABLE: str = "Table"
PARSE_TAG_TET: str = "TET"
PARSE_TAG_TEXT: str = "Text"
PARSE_TAG_TITLE: str = "Title"
PARSE_TAG_WORD: str = "Word"

RUN_ACTION_ALL_COMPLETE: str = "all"
RUN_ACTION_CREATE_DB: str = "db_c"
RUN_ACTION_IMAGE_2_PDF: str = "ocr"
RUN_ACTION_NON_PDF_2_PDF: str = "n_2_p"
RUN_ACTION_PDF_2_IMAGE: str = "p_2_i"
RUN_ACTION_PROCESS_INBOX: str = "p_i"
RUN_ACTION_STORE_FROM_PARSER: str = "s_f_p"
RUN_ACTION_TEXT_FROM_PDF: str = "tet"
RUN_ACTION_UPGRADE_DB: str = "db_u"

VERBOSE_TRUE: str = "true"

# -----------------------------------------------------------------------------
# Global Type Definitions.
# -----------------------------------------------------------------------------
Columns: TypeAlias = Dict[str, Union[PathLike[str], sqlalchemy.Integer, str]]

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
config: Dict[str, PathLike[str] | str] = {}

directory_inbox: PathLike[str] | str
directory_inbox_accepted: PathLike[str] | str
directory_inbox_rejected: PathLike[str] | str

document_child_child_no: sqlalchemy.Integer | None
document_child_directory_name: str
document_child_directory_type: str
document_child_error_code: str | None
document_child_file_name: str
document_child_file_type: str
document_child_id: sqlalchemy.Integer
document_child_id_base: sqlalchemy.Integer | None
document_child_id_parent: sqlalchemy.Integer | None
document_child_language_id: sqlalchemy.Integer
document_child_next_step: str | None
document_child_no: sqlalchemy.Integer | None
document_child_status: str
document_child_stem_name: str
document_directory_name: str
document_directory_type: str
document_error_code: str | None
document_file_name: str
document_file_type: str
document_id: sqlalchemy.Integer
document_id_base: sqlalchemy.Integer | None
document_id_parent: sqlalchemy.Integer | None
document_language_id: sqlalchemy.Integer
document_next_step: str | None
document_sha256: str | None
document_status: str
document_stem_name: str

environment_type: str

is_ignore_duplicates: bool
is_verbose: bool = True
is_verbose_parser: bool = False

language_directory_inbox: PathLike[str]
language_erroneous: int
language_id: sqlalchemy.Integer
language_iso_language_name: str
language_ok_processed: int
language_ok_processed_pandoc: int
language_ok_processed_pdf2image: int
language_ok_processed_pdflib: int
language_ok_processed_tesseract: int
language_to_be_processed: int

logger: logging.Logger

parse_result_author: str
parse_result_creation_date: datetime
parse_result_mod_date: datetime
parse_result_no_line: int
parse_result_no_page: int
parse_result_no_para: int
parse_result_no_sentence: int
parse_result_no_word_in_line: int
parse_result_no_word_in_sentence: int

pdf2image_type: str

run_action: str
run_id: sqlalchemy.Integer
run_run_id: sqlalchemy.Integer

start_time_document: sqlalchemy.BigInteger

tesseract_timeout: Decimal

total_erroneous: int
total_generated: int
total_ok_processed: int
total_ok_processed_pandoc: int
total_ok_processed_pdf2image: int
total_ok_processed_pdflib: int
total_ok_processed_tesseract: int
total_status_error: int
total_status_ready: int
total_to_be_processed: int
