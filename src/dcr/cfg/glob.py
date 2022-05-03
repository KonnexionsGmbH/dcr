"""Module cfg.glob: DCR Global Data."""
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
DB_DIALECT_POSTGRESQL: str = "postgresql"

DBC_ACTION: str = "action"
DBC_ACTIVE: str = "active"
DBC_CHILD_NO: str = "child_no"
DBC_CODE_ISO_639_3: str = "code_iso_639_3"
DBC_CODE_PANDOC: str = "code_pandoc"
DBC_CODE_SPACY: str = "code_spacy"
DBC_CODE_TESSERACT: str = "code_tesseract"
DBC_CREATED_AT: str = "created_at"
DBC_CURRENT_STEP: str = "current_step"
DBC_DIRECTORY_NAME: str = "directory_name"
DBC_DIRECTORY_NAME_INBOX: str = "directory_name_inbox"
DBC_DIRECTORY_TYPE: str = "directory_type"
DBC_DOCUMENT_ID: str = "document_id"
DBC_DOCUMENT_ID_BASE: str = "document_id_base"
DBC_DOCUMENT_ID_PARENT: str = "document_id_parent"
DBC_DURATION_NS: str = "duration_ns"
DBC_ERROR_CODE: str = "error_code"
DBC_ERROR_MSG: str = "error_msg"
DBC_ERROR_NO: str = "error_no"
DBC_FILE_NAME: str = "file_name"
DBC_FILE_SIZE_BYTES: str = "file_size_bytes"
DBC_FILE_TYPE: str = "file_type"
DBC_FUNCTION_NAME: str = "function_name"
DBC_ID: str = "id"
DBC_ISO_LANGUAGE_NAME: str = "iso_language_name"
DBC_LANGUAGE_ID: str = "language_id"
DBC_MODIFIED_AT: str = "modified_at"
DBC_MODULE_NAME: str = "module_name"
DBC_NEXT_STEP: str = "next_step"
DBC_PAGE_DATA: str = "page_data"
DBC_PAGE_NO: str = "page_no"
DBC_PDF_PAGES_NO: str = "pdf_pages_no"
DBC_RUN_ID: str = "run_id"
DBC_SENTENCE_TEXT: str = "sentence_text"
DBC_SHA256: str = "sha256"
DBC_STATUS: str = "status"
DBC_STEM_NAME: str = "stem_name"
DBC_TOTAL_ERRONEOUS: str = "total_erroneous"
DBC_TOTAL_OK_PROCESSED: str = "total_ok_processed"
DBC_TOTAL_TO_BE_PROCESSED: str = "total_to_be_processed"
DBC_VERSION: str = "version"

DBT_CONTENT_TETML_LINE: str = "content_tetml_line"
DBT_CONTENT_TETML_PAGE: str = "content_tetml_page"
DBT_CONTENT_TETML_WORD: str = "content_tetml_word"
DBT_CONTENT_TOKEN: str = "content_token"
DBT_DOCUMENT: str = "document"
DBT_LANGUAGE: str = "language"
DBT_RUN: str = "run"
DBT_VERSION: str = "version"

DCR_ARGV_0: str = "src/dcr/dcr.py"

DOCUMENT_DIRECTORY_TYPE_INBOX: str = "inbox"
DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED: str = "inbox_accepted"
DOCUMENT_DIRECTORY_TYPE_INBOX_REJECTED: str = "inbox_rejected"

DOCUMENT_ERROR_CODE_REJ_ERROR: str = "rejected_error"
DOCUMENT_ERROR_CODE_REJ_FILE_DUPL: str = "Duplicate file"
DOCUMENT_ERROR_CODE_REJ_FILE_ERROR: str = "rejected_file_error"
DOCUMENT_ERROR_CODE_REJ_FILE_EXT: str = "Unknown file extension"
DOCUMENT_ERROR_CODE_REJ_FILE_MOVE: str = "Issue with file move"
DOCUMENT_ERROR_CODE_REJ_FILE_OPEN: str = "Issue with file open"
DOCUMENT_ERROR_CODE_REJ_FILE_RIGHTS: str = "Issue with file permissions"
DOCUMENT_ERROR_CODE_REJ_NO_PDF_FORMAT: str = "No 'pdf' format"
DOCUMENT_ERROR_CODE_REJ_PANDOC: str = "Issue with Pandoc and TeX Live"
DOCUMENT_ERROR_CODE_REJ_PARSER: str = "Issue with parser"
DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE: str = "Issue with pdf2image"
DOCUMENT_ERROR_CODE_REJ_PDFLIB: str = "Issue with PDFlib TET"
DOCUMENT_ERROR_CODE_REJ_TESSERACT: str = "Issue with Tesseract OCR"

DOCUMENT_FILE_TYPE_JPG: str = "jpg"
DOCUMENT_FILE_TYPE_PANDOC: typing.List[str] = [
    "csv",
    "docx",
    "epub",
    "html",
    "odt",
    "rst",
    "rtf",
]
DOCUMENT_FILE_TYPE_PDF: str = "pdf"
DOCUMENT_FILE_TYPE_PNG: str = "png"
DOCUMENT_FILE_TYPE_TESSERACT: typing.List[str] = [
    "bmp",
    "gif",
    "jp2",
    "jpeg",
    "jpg",
    "png",
    "pnm",
    "tif",
    "tiff",
    "webp",
]
DOCUMENT_FILE_TYPE_TIF: str = "tif"
DOCUMENT_FILE_TYPE_TIFF: str = "tiff"
DOCUMENT_FILE_TYPE_XML: str = "xml"

DOCUMENT_LINE_TYPE_BODY: str = "b"
DOCUMENT_LINE_TYPE_FOOTER: str = "f"
DOCUMENT_LINE_TYPE_HEADER: str = "h"

DOCUMENT_STATUS_ABORT: str = "abort"
DOCUMENT_STATUS_END: str = "end"
DOCUMENT_STATUS_ERROR: str = "error"
DOCUMENT_STATUS_START: str = "start"

DOCUMENT_STEP_INBOX: str = "Inbox"
DOCUMENT_STEP_PANDOC: str = "Pandoc & TeX Live"
DOCUMENT_STEP_PARSER_LINE: str = "Parser Line"
DOCUMENT_STEP_PARSER_WORD: str = "Parser Word"
DOCUMENT_STEP_PDF2IMAGE: str = "pdf2image"
DOCUMENT_STEP_PDFLIB: str = "PDFlib TET"
DOCUMENT_STEP_PYPDF2: str = "PyPDF2"
DOCUMENT_STEP_TESSERACT: str = "Tesseract OCR"
DOCUMENT_STEP_TOKENIZE: str = "tokenize"

ERROR_01_901: str = "01.901 Issue (p_i): Document rejected because of unknown file extension='{extension}'."
ERROR_01_902: str = (
    "01.902 Issue (p_i): Moving '{source_file}' to '{target_file}' " + "- error: code='{error_code}' msg='{error_msg}'."
)
ERROR_01_903: str = (
    "01.903 Issue (p_i): Runtime error with fitz.open() processing of file '{source_file}' " + "- error: '{error_msg}'."
)
ERROR_01_904: str = (
    "01.904 Issue (p_i): File permission with file '{source_file}' " + "- error: code='{error_code}' msg='{error_msg}'."
)
ERROR_01_905: str = (
    "01.905 Issue (p_i): The same file has probably already been processed " + "once under the file name '{file_name}'."
)
ERROR_01_906: str = "01.906 Issue (p_i): The target file '{file_name}' already exists."

ERROR_21_901: str = (
    "21.901 Issue (p_2_i): The 'pdf' document '{file_name}' cannot be converted to an "
    + "image format - error: '{error_msg}'."
)
ERROR_21_902: str = (
    "21.902 Issue (p_2_i): The child image file number '{child_no}' with file name "
    + "'{file_name}' cannot be stored "
    + "- error: code='{error_code}' msg='{error_msg}'."
)
ERROR_21_903: str = "21.903 Issue (p_2_i): The target file '{file_name}' already exists."

ERROR_31_901: str = (
    "31.901 Issue (n_2_p): Converting the file '{source_file}' to the file "
    + "'{target_file}' with Pandoc and TeX Live failed - output='{output}'."
)
ERROR_31_902: str = (
    "31.902 Issue (n_2_p): The file '{file_name}' cannot be converted to an " + "'pdf' document - error: '{error_msg}'."
)
ERROR_31_903: str = "31.903 Issue (n_2_p): The target file '{file_name}' already exists."

ERROR_41_901: str = (
    "41.901 Issue (ocr): Converting the file '{source_file}' to the file "
    + "'{target_file}' with Tesseract OCR failed - "
    + "error type: '{error_type}' - error: '{error}'."
)
ERROR_41_902: str = (
    "41.902 Issue (ocr): Converting the file '{source_file}' to the file "
    + "'{target_file}' with Tesseract OCR failed - "
    + "error status: '{error_status}' - error: '{error}'."
)
ERROR_41_903: str = "41.903 Issue (ocr): The target file '{file_name}' already exists."
ERROR_41_904: str = "41.904 Issue (ocr): The target file '{file_name}' already exists."

ERROR_51_901: str = (
    "51.901 Issue (tet): Opening document '{file_name}' - "
    + "error no: '{error_no}' - api: '{api_name}' - error: '{error}'."
)
ERROR_51_902: str = (
    "51.902 Issue (tet): TETML data could not be retrieved from document '{file_name}' - "
    + "error no: '{error_no}' - api: '{api_name}' - error: '{error}'."
)
ERROR_51_903: str = (
    "51.903 Issue (tet): Extracting the text and metadata from file '{file_name}' to file "
    + "'{target_file}' failed: "
    + "error no: '{error_no}' - api: '{api_name}' - error: '{error}'."
)

ERROR_61_901: str = (
    "61.901 Issue (s_f_p): {function}: Unknown child tag '{child_tag}' - " + "in parent tag '{parent_tag}'."
)
ERROR_61_902: str = "61.902 Issue (s_f_p): Expected tag '{expected_tag}' - " + " but found tag '{found_tag}'."
ERROR_61_903: str = (
    "61.903 Issue (s_f_p): Text missing: document {document_id} page {page_no} " + "paragraph {para_no} line {line_no}."
)

FILE_ENCODING_DEFAULT: str = "utf-8"

INFORMATION_NOT_YET_AVAILABLE: str = "n/a"

JSON_NAME_API_VERSION: str = "apiVersion"
JSON_NAME_COLUMN_NAME: str = "columnName"
JSON_NAME_COLUMN_VALUE: str = "columnValue"
JSON_NAME_DATA: str = "data"
JSON_NAME_LINE_INDEX_PAGE: str = "lineIndexPage"
JSON_NAME_LINE_INDEX_PARA: str = "lineIndexPara"
JSON_NAME_LINE_WORDS: str = "lineWords"
JSON_NAME_LINE_TEXT: str = "lineText"
JSON_NAME_LINE_TYPE: str = "lineType"
JSON_NAME_NO_LINES_IN_PAGE: str = "noLinesInPage"
JSON_NAME_NO_LINES_IN_PARA: str = "noLinesInPara"
JSON_NAME_NO_PAGES_IN_DOC: str = "noPagesInDoc"
JSON_NAME_NO_PARAS_IN_PAGE: str = "noParasInPage"
JSON_NAME_NO_WORDS_IN_LINE: str = "noWordsInLine"
JSON_NAME_NO_WORDS_IN_PAGE: str = "noWordsInPage"
JSON_NAME_NO_WORDS_IN_PARA: str = "noWordsInPara"
JSON_NAME_PAGE_INDEX_DOC: str = "pageIndexDoc"
JSON_NAME_PAGE_LINES: str = "pageLines"
JSON_NAME_PAGE_WORDS: str = "pageWords"
JSON_NAME_PARA_INDEX_PAGE: str = "paraIndexPage"
JSON_NAME_ROW: str = "row"
JSON_NAME_ROWS: str = "rows"
JSON_NAME_TABLES: str = "tables"
JSON_NAME_TABLE_NAME: str = "tableName"

JSON_NAME_TOKEN_DEP_: str = "tknDep"
JSON_NAME_TOKEN_ENT_IOB_: str = "tknEntIob"
JSON_NAME_TOKEN_ENT_KB_ID_: str = "tknEntKbId"
JSON_NAME_TOKEN_ENT_TYPE_: str = "tknEntType"
JSON_NAME_TOKEN_I: str = "tknI"
JSON_NAME_TOKEN_IS_ALPHA: str = "tknIsAlpha"
JSON_NAME_TOKEN_IS_CURRENCY: str = "tknIsCurrency"
JSON_NAME_TOKEN_IS_DIGIT: str = "tknIsDigit"
JSON_NAME_TOKEN_IS_OOV: str = "tknIsOov"
JSON_NAME_TOKEN_IS_PUNCT: str = "tknIsPunct"
JSON_NAME_TOKEN_IS_SENT_END: str = "tknIsSentEnd"
JSON_NAME_TOKEN_IS_SENT_START: str = "tknIsSentStart"
JSON_NAME_TOKEN_IS_STOP: str = "tknIsStop"
JSON_NAME_TOKEN_IS_TITLE: str = "tknIsTitle"
JSON_NAME_TOKEN_LANG_: str = "tknLang"
JSON_NAME_TOKEN_LEFT_EDGE: str = "tknLeftEdge"
JSON_NAME_TOKEN_LEMMA_: str = "tknLemma"
JSON_NAME_TOKEN_LIKE_EMAIL: str = "tknLikeEmail"
JSON_NAME_TOKEN_LIKE_NUM: str = "tknLikeNum"
JSON_NAME_TOKEN_LIKE_URL: str = "tknLikeUrl"
JSON_NAME_TOKEN_NORM_: str = "tknNorm"
JSON_NAME_TOKEN_RIGHT_EDGE: str = "tknRightEdge"
JSON_NAME_TOKEN_SHAPE_: str = "tknShape"
JSON_NAME_TOKEN_TEXT: str = "tknText"
JSON_NAME_TOKEN_TEXT_WITH_WS: str = "tknTextWithWs"
JSON_NAME_TOKEN_WHITESPACE_: str = "tknWhitespace"

JSON_NAME_WORD_INDEX_LINE: str = "wordIndexLine"
JSON_NAME_WORD_INDEX_PAGE: str = "wordIndexPage"
JSON_NAME_WORD_INDEX_PARA: str = "wordIndexPara"
JSON_NAME_WORD_TEXT: str = "wordText"

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

RUN_STATUS_END: str = "end"
RUN_STATUS_START: str = "start"

TESTS_INBOX_NAME: str = "tests/__PYTEST_FILES__/"

VERBOSE_TRUE: str = "true"

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

spacy_tkn_attr_dep_: bool = False
spacy_tkn_attr_ent_iob_: bool = False
spacy_tkn_attr_ent_kb_id_: bool = False
spacy_tkn_attr_ent_type_: bool = True
spacy_tkn_attr_i: bool = True
spacy_tkn_attr_is_alpha: bool = False
spacy_tkn_attr_is_currency: bool = True
spacy_tkn_attr_is_digit: bool = True
spacy_tkn_attr_is_oov: bool = True
spacy_tkn_attr_is_punct: bool = True
spacy_tkn_attr_is_sent_end: bool = False
spacy_tkn_attr_is_sent_start: bool = False
spacy_tkn_attr_is_stop: bool = True
spacy_tkn_attr_is_title: bool = True
spacy_tkn_attr_lang_: bool = False
spacy_tkn_attr_left_edge: bool = False
spacy_tkn_attr_lemma_: bool = True
spacy_tkn_attr_like_email: bool = True
spacy_tkn_attr_like_num: bool = True
spacy_tkn_attr_like_url: bool = True
spacy_tkn_attr_norm_: bool = True
spacy_tkn_attr_right_edge: bool = False
spacy_tkn_attr_shape_: bool = False
spacy_tkn_attr_text: bool = True
spacy_tkn_attr_text_with_ws: bool = False
spacy_tkn_attr_whitespace_: bool = True

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
