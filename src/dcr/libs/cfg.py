"""Module libs.cfg: DCR Configuration Data."""
import logging
import os
import typing

import nlp.line_type
import setup.config
import sqlalchemy

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------

DCR_ARGV_0: str = "src/dcr/dcr.py"

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

PARSE_NAME_SPACE: str = "{http://www.pdflib.com/XML/TET5/TET-5.0}"

PARSE_TAG_ACTION: str = "Action"
PARSE_TAG_ANNOTATIONS: str = "Annotations"
PARSE_TAG_ATTACHMENTS: str = "Attachments"
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
PARSE_TAG_ENCRYPTION: str = "Encryption"
PARSE_TAG_EXCEPTION: str = "Exception"
PARSE_TAG_FIELDS: str = "Fields"
PARSE_TAG_FROM: int = len(PARSE_NAME_SPACE)
PARSE_TAG_GRAPHICS: str = "Graphics"
PARSE_TAG_JAVA_SCRIPTS: str = "JavaScripts"
PARSE_TAG_LINE: str = "Line"
PARSE_TAG_METADATA: str = "Metadata"
PARSE_TAG_MOD_DATE: str = "ModDate"
PARSE_TAG_OPTIONS: str = "Options"
PARSE_TAG_OUTPUT_INTENTS: str = "OutputIntents"
PARSE_TAG_PAGE: str = "Page"
PARSE_TAG_PAGES: str = "Pages"
PARSE_TAG_PARA: str = "Para"
PARSE_TAG_PLACED_IMAGE: str = "PlacedImage"
PARSE_TAG_PRODUCER: str = "Producer"
PARSE_TAG_RESOURCES: str = "Resources"
PARSE_TAG_SIGNATURE_FIELDS: str = "SignatureFields"
PARSE_TAG_TABLE: str = "Table"
PARSE_TAG_TEXT: str = "Text"
PARSE_TAG_TITLE: str = "Title"
PARSE_TAG_WORD: str = "Word"
PARSE_TAG_XFA: str = "XFA"

RUN_ACTION_ALL_COMPLETE: str = "all"
RUN_ACTION_CREATE_DB: str = "db_c"
RUN_ACTION_IMAGE_2_PDF: str = "ocr"
RUN_ACTION_NON_PDF_2_PDF: str = "n_2_p"
RUN_ACTION_PDF_2_IMAGE: str = "p_2_i"
RUN_ACTION_PROCESS_INBOX: str = "p_i"
RUN_ACTION_STORE_FROM_PARSER: str = "s_f_p"
RUN_ACTION_TEXT_FROM_PDF: str = "tet"
RUN_ACTION_TOKENIZE: str = "tkn"
RUN_ACTION_UPGRADE_DB: str = "db_u"

TESTS_INBOX_NAME: str = "tests/__PYTEST_FILES__/"

VERBOSE_TRUE: str = "true"

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
