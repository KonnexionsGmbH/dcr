"""Library Stub."""
import logging
import os
import typing

import setup.config
import sqlalchemy

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
DCR_ARGV_0: str

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

TESTS_INBOX_NAME: str

VERBOSE_TRUE: str

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
config: typing.Type[setup.config.Config]

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
