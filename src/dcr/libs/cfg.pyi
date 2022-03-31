"""Library Stub."""
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
DCR_CFG_DELETE_AUXILIARY_FILES: str
DCR_CFG_DIRECTORY_INBOX: str
DCR_CFG_DIRECTORY_INBOX_ACCEPTED: str
DCR_CFG_DIRECTORY_INBOX_REJECTED: str
DCR_CFG_FILE: str
DCR_CFG_IGNORE_DUPLICATES: str
DCR_CFG_INITIAL_DATABASE_DATA: str
DCR_CFG_PDF2IMAGE_TYPE: str
DCR_CFG_PDF2IMAGE_TYPE_JPEG: str
DCR_CFG_PDF2IMAGE_TYPE_PNG: str
DCR_CFG_SECTION: str
DCR_CFG_SECTION_DEV: str
DCR_CFG_SECTION_PROD: str
DCR_CFG_SECTION_TEST: str
DCR_CFG_TESSERACT_TIMEOUT: str
DCR_CFG_VERBOSE: str
DCR_CFG_VERBOSE_PARSER: str

DCR_ENVIRONMENT_TYPE: str

ENVIRONMENT_TYPE_DEV: str
ENVIRONMENT_TYPE_PROD: str
ENVIRONMENT_TYPE_TEST: str

FILE_ENCODING_DEFAULT: str

INFORMATION_NOT_YET_AVAILABLE: str

LOCALE: str
LOGGER_CFG_FILE: str
LOGGER_END: str
LOGGER_FATAL_HEAD: str
LOGGER_FATAL_TAIL: str
LOGGER_PROGRESS_UPDATE: str
LOGGER_START: str

OS_NT: str
OS_POSIX: str

PANDOC_PDF_ENGINE_LULATEX: str
PANDOC_PDF_ENGINE_XELATEX: str

PARSE_NAME_SPACE: str
PARSE_TAG_A: str
PARSE_TAG_ANNOTATIONS: str
PARSE_TAG_AUTHOR: str
PARSE_TAG_BOOKMARKS: str
PARSE_TAG_BOX: str
PARSE_TAG_CONTENT: str
PARSE_TAG_CREATION: str
PARSE_TAG_CREATION_DATE: str
PARSE_TAG_CREATOR: str
PARSE_TAG_CUSTOM: str
PARSE_TAG_DESTINATIONS: str
PARSE_TAG_DOCUMENT: str
PARSE_TAG_DOC_INFO: str
PARSE_TAG_FROM: int
PARSE_TAG_GRAPHICS: str
PARSE_TAG_LINE: str
PARSE_TAG_METADATA: str
PARSE_TAG_MOD_DATE: str
PARSE_TAG_OPTIONS: str
PARSE_TAG_PAGE: str
PARSE_TAG_PAGES: str
PARSE_TAG_PARA: str
PARSE_TAG_PLACED_IMAGE: str
PARSE_TAG_PRODUCER: str
PARSE_TAG_RESOURCES: str
PARSE_TAG_TABLE: str
PARSE_TAG_TET: str
PARSE_TAG_TEXT: str
PARSE_TAG_TITLE: str
PARSE_TAG_WORD: str

RUN_ACTION_ALL_COMPLETE: str
RUN_ACTION_CREATE_DB: str
RUN_ACTION_IMAGE_2_PDF: str
RUN_ACTION_NON_PDF_2_PDF: str
RUN_ACTION_PDF_2_IMAGE: str
RUN_ACTION_PROCESS_INBOX: str
RUN_ACTION_STORE_FROM_PARSER: str
RUN_ACTION_TEXT_FROM_PDF: str
RUN_ACTION_UPGRADE_DB: str

TESTS_INBOX_NAME: str

VERBOSE_TRUE: str

# -----------------------------------------------------------------------------
# Global Type Definitions.
# -----------------------------------------------------------------------------
Columns: TypeAlias = Dict[str, Union[PathLike[str], sqlalchemy.Integer, str]]

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
config: Dict[str, PathLike[str] | str]

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

is_delete_auxiliary_files: bool
is_ignore_duplicates: bool
is_verbose: bool
is_verbose_parser: bool

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

languages_tesseract: Dict[sqlalchemy.Integer, str]

logger: logging.Logger

parse_result_author: str
parse_result_creation_date: datetime
parse_result_mod_date: datetime
parse_result_line_in_para: int
parse_result_page_in_document: int
parse_result_para_in_page: int
parse_result_sentence_in_para: int
parse_result_token_in_line: int
parse_result_token_in_sentence: int

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
