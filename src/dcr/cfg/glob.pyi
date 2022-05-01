"""Library Stub."""
import logging
import os
import typing

import cfg.setup
import nlp.line_type
import psycopg2.extensions
import sqlalchemy

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
DB_DIALECT_POSTGRESQL: str

DBC_ACTION: str
DBC_ACTIVE: str
DBC_CHILD_NO: str
DBC_CODE_ISO_639_3: str
DBC_CODE_PANDOC: str
DBC_CODE_SPACY: str
DBC_CODE_TESSERACT: str
DBC_CREATED_AT: str
DBC_CURRENT_STEP: str
DBC_DIRECTORY_NAME: str
DBC_DIRECTORY_NAME_INBOX: str
DBC_DIRECTORY_TYPE: str
DBC_DOCUMENT_ID: str
DBC_DOCUMENT_ID_BASE: str
DBC_DOCUMENT_ID_PARENT: str
DBC_DURATION_NS: str
DBC_ERROR_CODE: str
DBC_ERROR_MSG: str
DBC_ERROR_NO: str
DBC_FILE_NAME: str
DBC_FILE_SIZE_BYTES: str
DBC_FILE_TYPE: str
DBC_FUNCTION_NAME: str
DBC_ID: str
DBC_ISO_LANGUAGE_NAME: str
DBC_LANGUAGE_ID: str
DBC_MODIFIED_AT: str
DBC_MODULE_NAME: str
DBC_NEXT_STEP: str
DBC_PAGE_DATA: str
DBC_PAGE_NO: str
DBC_PDF_PAGES_NO: str
DBC_RUN_ID: str
DBC_SENTENCE_TEXT: str
DBC_SHA256: str
DBC_STATUS: str
DBC_STEM_NAME: str
DBC_TOTAL_ERRONEOUS: str
DBC_TOTAL_OK_PROCESSED: str
DBC_TOTAL_TO_BE_PROCESSED: str
DBC_VERSION: str

DBT_CONTENT_TETML_LINE: str
DBT_CONTENT_TETML_PAGE: str
DBT_CONTENT_TETML_WORD: str
DBT_CONTENT_TOKEN: str
DBT_DOCUMENT: str
DBT_LANGUAGE: str
DBT_RUN: str
DBT_VERSION: str

DCR_ARGV_0: str

DOCUMENT_DIRECTORY_TYPE_INBOX: str
DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED: str
DOCUMENT_DIRECTORY_TYPE_INBOX_REJECTED: str

DOCUMENT_ERROR_CODE_REJ_ERROR: str
DOCUMENT_ERROR_CODE_REJ_FILE_DUPL: str
DOCUMENT_ERROR_CODE_REJ_FILE_ERROR: str
DOCUMENT_ERROR_CODE_REJ_FILE_EXT: str
DOCUMENT_ERROR_CODE_REJ_FILE_MOVE: str
DOCUMENT_ERROR_CODE_REJ_FILE_OPEN: str
DOCUMENT_ERROR_CODE_REJ_FILE_RIGHTS: str
DOCUMENT_ERROR_CODE_REJ_NO_PDF_FORMAT: str
DOCUMENT_ERROR_CODE_REJ_PANDOC: str
DOCUMENT_ERROR_CODE_REJ_PARSER: str
DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE: str
DOCUMENT_ERROR_CODE_REJ_PDFLIB: str
DOCUMENT_ERROR_CODE_REJ_TESSERACT: str

DOCUMENT_FILE_TYPE_JPG: str
DOCUMENT_FILE_TYPE_PANDOC: typing.List[str]
DOCUMENT_FILE_TYPE_PDF: str
DOCUMENT_FILE_TYPE_PNG: str
DOCUMENT_FILE_TYPE_TESSERACT: typing.List[str]
DOCUMENT_FILE_TYPE_TIF: str
DOCUMENT_FILE_TYPE_TIFF: str
DOCUMENT_FILE_TYPE_XML: str

DOCUMENT_LINE_TYPE_BODY: str
DOCUMENT_LINE_TYPE_FOOTER: str
DOCUMENT_LINE_TYPE_HEADER: str

DOCUMENT_STATUS_ABORT: str
DOCUMENT_STATUS_END: str
DOCUMENT_STATUS_ERROR: str
DOCUMENT_STATUS_START: str

DOCUMENT_STEP_INBOX: str
DOCUMENT_STEP_PANDOC: str
DOCUMENT_STEP_PARSER_LINE: str
DOCUMENT_STEP_PARSER_WORD: str
DOCUMENT_STEP_PDF2IMAGE: str
DOCUMENT_STEP_PDFLIB: str
DOCUMENT_STEP_PYPDF2: str
DOCUMENT_STEP_TESSERACT: str
DOCUMENT_STEP_TOKENIZE: str

ERROR_01_901: str
ERROR_01_902: str
ERROR_01_903: str
ERROR_01_904: str
ERROR_01_905: str
ERROR_01_906: str

ERROR_21_901: str
ERROR_21_902: str
ERROR_21_903: str

ERROR_31_901: str
ERROR_31_902: str
ERROR_31_903: str

ERROR_41_901: str
ERROR_41_902: str
ERROR_41_903: str
ERROR_41_904: str

ERROR_51_901: str
ERROR_51_902: str
ERROR_51_903: str

ERROR_61_901: str
ERROR_61_902: str
ERROR_61_903: str

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

JSON_NAME_API_VERSION: str
JSON_NAME_COLUMN_NAME: str
JSON_NAME_COLUMN_VALUE: str
JSON_NAME_DATA: str
JSON_NAME_LINE_INDEX_PAGE: str
JSON_NAME_LINE_INDEX_PARA: str
JSON_NAME_LINE_WORDS: str
JSON_NAME_LINE_TEXT: str
JSON_NAME_LINE_TYPE: str
JSON_NAME_NO_LINES_IN_PAGE: str
JSON_NAME_NO_LINES_IN_PARA: str
JSON_NAME_NO_PAGES_IN_DOC: str
JSON_NAME_NO_PARAS_IN_PAGE: str
JSON_NAME_NO_WORDS_IN_LINE: str
JSON_NAME_NO_WORDS_IN_PAGE: str
JSON_NAME_NO_WORDS_IN_PARA: str
JSON_NAME_PAGE_INDEX_DOC: str
JSON_NAME_PAGE_LINES: str
JSON_NAME_PAGE_WORDS: str
JSON_NAME_PARA_INDEX_PAGE: str
JSON_NAME_ROW: str
JSON_NAME_ROWS: str
JSON_NAME_TABLES: str
JSON_NAME_TABLE_NAME: str
JSON_NAME_TOKEN_DEP: str
JSON_NAME_TOKEN_INDEX: str
JSON_NAME_TOKEN_IS_ALPHA: str
JSON_NAME_TOKEN_IS_STOP: str
JSON_NAME_TOKEN_LEMMA: str
JSON_NAME_TOKEN_POS: str
JSON_NAME_TOKEN_SHAPE: str
JSON_NAME_TOKEN_TAG: str
JSON_NAME_TOKEN_TEXT: str
JSON_NAME_WORD_INDEX_LINE: str
JSON_NAME_WORD_INDEX_PAGE: str
JSON_NAME_WORD_INDEX_PARA: str
JSON_NAME_WORD_TEXT: str

PARSE_NAME_SPACE: str

PARSE_TAG_ACTION: str
PARSE_TAG_ANNOTATIONS: str
PARSE_TAG_ATTACHMENTS: str
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
PARSE_TAG_ENCRYPTION: str
PARSE_TAG_EXCEPTION: str
PARSE_TAG_FIELDS: str
PARSE_TAG_FROM: int
PARSE_TAG_GRAPHICS: str
PARSE_TAG_JAVA_SCRIPTS: str
PARSE_TAG_LINE: str
PARSE_TAG_METADATA: str
PARSE_TAG_MOD_DATE: str
PARSE_TAG_OPTIONS: str
PARSE_TAG_OUTPUT_INTENTS: str
PARSE_TAG_PAGE: str
PARSE_TAG_PAGES: str
PARSE_TAG_PARA: str
PARSE_TAG_PLACED_IMAGE: str
PARSE_TAG_PRODUCER: str
PARSE_TAG_RESOURCES: str
PARSE_TAG_SIGNATURE_FIELDS: str
PARSE_TAG_TABLE: str
PARSE_TAG_TEXT: str
PARSE_TAG_TITLE: str
PARSE_TAG_WORD: str
PARSE_TAG_XFA: str

RUN_ACTION_ALL_COMPLETE: str
RUN_ACTION_CREATE_DB: str
RUN_ACTION_IMAGE_2_PDF: str
RUN_ACTION_NON_PDF_2_PDF: str
RUN_ACTION_PDF_2_IMAGE: str
RUN_ACTION_PROCESS_INBOX: str
RUN_ACTION_STORE_FROM_PARSER: str
RUN_ACTION_TEXT_FROM_PDF: str
RUN_ACTION_TOKENIZE: str
RUN_ACTION_UPGRADE_DB: str

RUN_STATUS_END: str
RUN_STATUS_START: str

TESTS_INBOX_NAME: str

VERBOSE_TRUE: str

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
db_current_database: str
db_current_user: str
db_driver_conn: psycopg2.extensions.connection | None = None
db_driver_cur: psycopg2.extensions.cursor | None = None
db_orm_engine: sqlalchemy.engine.Engine | None = None
db_orm_metadata: sqlalchemy.MetaData | None = None

directory_inbox: os.PathLike[str] | str
directory_inbox_accepted: os.PathLike[str] | str
directory_inbox_rejected: os.PathLike[str] | str

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

document_current_step: str
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

language_directory_inbox: os.PathLike[str]
language_erroneous: int
language_id: sqlalchemy.Integer
language_iso_language_name: str
language_ok_processed: int
language_ok_processed_pandoc: int
language_ok_processed_pdf2image: int
language_ok_processed_pdflib: int
language_ok_processed_tesseract: int
language_to_be_processed: int

languages_pandoc: typing.Dict[sqlalchemy.Integer, str]
languages_spacy: typing.Dict[sqlalchemy.Integer, str]
languages_tesseract: typing.Dict[sqlalchemy.Integer, str]

line_type: typing.Type[nlp.line_type.LineType]

logger: logging.Logger

parse_result_line_index_page: int
parse_result_line_index_para: int
parse_result_no_lines_in_page: int
parse_result_no_lines_in_para: int
parse_result_no_pages_in_doc: int
parse_result_no_paras_in_page: int
parse_result_no_words_in_line: int
parse_result_no_words_in_page: int
parse_result_no_words_in_para: int
parse_result_page_index_doc: int
parse_result_page_lines: typing.Dict[str, int | typing.List[typing.Dict[str, int | str]]]
parse_result_page_words: typing.Dict[str, int | typing.List[typing.Dict[str, int | str]]]
parse_result_para_index_page: int
parse_result_text: str
parse_result_word_index_line: int
parse_result_word_index_page: int
parse_result_word_index_para: int

run_action: str
run_id: sqlalchemy.Integer
run_run_id: sqlalchemy.Integer

setup: typing.Type[cfg.setup.Setup]

start_time_document: int

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