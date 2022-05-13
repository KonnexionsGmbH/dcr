"""Module cfg.glob: DCR Global Data."""
from __future__ import annotations

import logging
import os
from typing import Dict
from typing import List
from typing import Type

import cfg.cls_setup
import db.cls_action
import db.cls_base
import db.cls_language
import db.cls_run
import nlp.cls_line_type
import psycopg2.extensions
import sqlalchemy

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
DB_DIALECT_POSTGRESQL: str = "postgresql"

DBC_ACTION_CODE: str = "action_code"
DBC_ACTION_CODE_LAST: str = "action_code_last"
DBC_ACTION_TEXT: str = "action_text"
DBC_ACTION_TEXT_LAST: str = "action_text_last"
DBC_ACTIVE: str = "active"
DBC_CODE_ISO_639_3: str = "code_iso_639_3"
DBC_CODE_PANDOC: str = "code_pandoc"
DBC_CODE_SPACY: str = "code_spacy"
DBC_CODE_TESSERACT: str = "code_tesseract"
DBC_CREATED_AT: str = "created_at"
DBC_CURRENT_STEP: str = "current_step"
DBC_DIRECTORY_NAME: str = "directory_name"
DBC_DIRECTORY_NAME_INBOX: str = "directory_name_inbox"
DBC_DIRECTORY_TYPE: str = "directory_type"
DBC_DURATION_NS: str = "duration_ns"
DBC_ERROR_CODE: str = "error_code"
DBC_ERROR_CODE_LAST: str = "error_code_last"
DBC_ERROR_MSG: str = "error_msg"
DBC_ERROR_MSG_LAST: str = "error_msg_last"
DBC_ERROR_NO: str = "error_no"
DBC_FILE_NAME: str = "file_name"
DBC_FILE_SIZE_BYTES: str = "file_size_bytes"
DBC_ID: str = "id"
DBC_ID_BASE: str = "id_base"
DBC_ID_LANGUAGE: str = "id_language"
DBC_ID_PARENT: str = "id_parent"
DBC_ID_RUN: str = "id_run"
DBC_ID_RUN_LAST: str = "id_run_last"
DBC_ISO_LANGUAGE_NAME: str = "iso_language_name"
DBC_LAST_STEP: str = "last_step"
DBC_MODIFIED_AT: str = "modified_at"
DBC_NO_CHILDREN: str = "no_children"
DBC_NO_PDF_PAGES: str = "no_pdf_pages"
DBC_PAGE_DATA: str = "page_data"
DBC_PAGE_NO: str = "page_no"
DBC_SHA256: str = "sha256"
DBC_STATUS: str = "status"
DBC_TOTAL_ERRONEOUS: str = "total_erroneous"
DBC_TOTAL_PROCESSED_OK: str = "total_processed_ok"
DBC_TOTAL_PROCESSED_TO_BE: str = "total_processed_to_be"
DBC_VERSION: str = "version"

DBT_ACTION: str = "action"
DBT_BASE: str = "base"
DBT_LANGUAGE: str = "language"
DBT_RUN: str = "run"
DBT_TOKEN: str = "token"
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
DOCUMENT_FILE_TYPE_JSON: str = "json"
DOCUMENT_FILE_TYPE_PANDOC: List[str] = [
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
DOCUMENT_FILE_TYPE_TESSERACT: List[str] = [
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

ERROR_01_901: str = "01.901 Issue (p_i): Document rejected because of unknown file extension='{extension}'."
ERROR_01_903: str = (
    "01.903 Issue (p_i): Runtime error with fitz.open() processing of file '{file_name}' " + "- error: '{error_msg}'."
)
ERROR_01_905: str = (
    "01.905 Issue (p_i): The same file has probably already been processed " + "once under the file name '{file_name}'."
)
ERROR_01_906: str = "01.906 Issue (p_i): The target file '{full_name}' already exists."

ERROR_21_903: str = "21.903 Issue (p_2_i): The target file '{full_name}' already exists."

ERROR_31_902: str = (
    "31.902 Issue (n_2_p): The file '{full_name}' cannot be converted to an " + "'pdf' document - error: '{error_msg}'."
)
ERROR_31_903: str = "31.903 Issue (n_2_p): The target file '{full_name}' already exists."

ERROR_41_901: str = (
    "41.901 Issue (ocr): Converting the file '{full_name_curr}' to the file "
    + "'{full_name_next}' with Tesseract OCR failed - "
    + "error type: '{error_type}' - error: '{error}'."
)
ERROR_41_903: str = "41.903 Issue (ocr): The target file '{full_name}' already exists."
ERROR_41_904: str = "41.904 Issue (pypdf2): The target file '{full_name}' already exists."

ERROR_51_901: str = (
    "51.901 Issue (tet): Opening document '{full_name}' - "
    + "error no: '{error_no}' - api: '{api_name}' - error: '{error}'."
)
ERROR_51_903: str = (
    "51.903 Issue (tet): Extracting the text and metadata from file '{file_name}' to file "
    + "'{target_file}' failed: "
    + "error no: '{error_no}' - api: '{api_name}' - error: '{error}'."
)
ERROR_51_904: str = "51.904 Issue (pdflib): The target file '{full_name}' already exists."

ERROR_61_901: str = (
    "61.901 Issue (s_p_j): {function}: Unknown child tag '{child_tag}' - " + "in parent tag '{parent_tag}'."
)
ERROR_61_902: str = "61.902 Issue (s_p_j): Expected tag '{expected_tag}' - " + " but found tag '{found_tag}'."
ERROR_61_903: str = (
    "61.903 Issue (s_p_j): Text missing: document {document_id} page {page_no} " + "paragraph {para_no} line {line_no}."
)

FILE_ENCODING_DEFAULT: str = "utf-8"

INFORMATION_NOT_YET_AVAILABLE: str = "n/a"

JSON_NAME_API_VERSION: str = "apiVersion"
JSON_NAME_BASE_FILE_NAME: str = "baseFileName"
JSON_NAME_BASE_ID: str = "baseId"
JSON_NAME_COLUMN_NAME: str = "columnName"
JSON_NAME_COLUMN_VALUE: str = "columnValue"
JSON_NAME_DATA: str = "data"
JSON_NAME_LINE_INDEX_PAGE: str = "lineIndexPage"
JSON_NAME_LINE_INDEX_PARA: str = "lineIndexPara"
JSON_NAME_LINE_WORDS: str = "lineWords"
JSON_NAME_LINE_TEXT: str = "lineText"
JSON_NAME_LINE_TYPE: str = "lineType"
JSON_NAME_LINES: str = "lines"
JSON_NAME_NO_LINES_IN_PAGE: str = "noLinesInPage"
JSON_NAME_NO_LINES_IN_PARA: str = "noLinesInPara"
JSON_NAME_NO_PAGES_IN_DOC: str = "noPagesInDoc"
JSON_NAME_NO_PARAS_IN_PAGE: str = "noParasInPage"
JSON_NAME_NO_WORDS_IN_LINE: str = "noWordsInLine"
JSON_NAME_NO_WORDS_IN_PAGE: str = "noWordsInPage"
JSON_NAME_NO_WORDS_IN_PARA: str = "noWordsInPara"
JSON_NAME_PAGE_INDEX_DOC: str = "pageIndexDoc"
JSON_NAME_PAGE_LINES: str = "pageLines"
JSON_NAME_PAGE_NO: str = "pageNo"
JSON_NAME_PAGE_WORDS: str = "pageWords"
JSON_NAME_PAGES: str = "pages"
JSON_NAME_PARA_INDEX_PAGE: str = "paraIndexPage"
JSON_NAME_ROW: str = "row"
JSON_NAME_ROWS: str = "rows"
JSON_NAME_TABLES: str = "tables"
JSON_NAME_TABLE_NAME: str = "tableName"

JSON_NAME_TOKEN_CLUSTER: str = "tknCluster"
JSON_NAME_TOKEN_DEP_: str = "tknDep_"
JSON_NAME_TOKEN_DOC: str = "tknDoc"
JSON_NAME_TOKEN_ENT_IOB_: str = "tknEntIob_"
JSON_NAME_TOKEN_ENT_KB_ID_: str = "tknEntKbId_"
JSON_NAME_TOKEN_ENT_TYPE_: str = "tknEntType_"
JSON_NAME_TOKEN_HEAD: str = "tknHead"
JSON_NAME_TOKEN_I: str = "tknI"
JSON_NAME_TOKEN_IDX: str = "tknIdx"
JSON_NAME_TOKEN_IS_ALPHA: str = "tknIsAlpha"
JSON_NAME_TOKEN_IS_ASCII: str = "tknIsAscii"
JSON_NAME_TOKEN_IS_BRACKET: str = "tknIsBracket"
JSON_NAME_TOKEN_IS_CURRENCY: str = "tknIsCurrency"
JSON_NAME_TOKEN_IS_DIGIT: str = "tknIsDigit"
JSON_NAME_TOKEN_IS_LEFT_PUNCT: str = "tknIsLeftPunct"
JSON_NAME_TOKEN_IS_LOWER: str = "tknIsLower"
JSON_NAME_TOKEN_IS_OOV: str = "tknIsOov"
JSON_NAME_TOKEN_IS_PUNCT: str = "tknIsPunct"
JSON_NAME_TOKEN_IS_QUOTE: str = "tknIsQuote"
JSON_NAME_TOKEN_IS_RIGHT_PUNCT: str = "tknIsRightPunct"
JSON_NAME_TOKEN_IS_SENT_END: str = "tknIsSentEnd"
JSON_NAME_TOKEN_IS_SENT_START: str = "tknIsSentStart"
JSON_NAME_TOKEN_IS_SPACE: str = "tknIsSpace"
JSON_NAME_TOKEN_IS_STOP: str = "tknIsStop"
JSON_NAME_TOKEN_IS_TITLE: str = "tknIsTitle"
JSON_NAME_TOKEN_IS_UPPER: str = "tknIsUpper"
JSON_NAME_TOKEN_LANG_: str = "tknLang_"
JSON_NAME_TOKEN_LEFT_EDGE: str = "tknLeftEdge"
JSON_NAME_TOKEN_LEMMA_: str = "tknLemma_"
JSON_NAME_TOKEN_LEX: str = "tknLex"
JSON_NAME_TOKEN_LEX_ID: str = "tknLexId"
JSON_NAME_TOKEN_LIKE_EMAIL: str = "tknLikeEmail"
JSON_NAME_TOKEN_LIKE_NUM: str = "tknLikeNum"
JSON_NAME_TOKEN_LIKE_URL: str = "tknLikeUrl"
JSON_NAME_TOKEN_LOWER_: str = "tknLower_"
JSON_NAME_TOKEN_MORPH: str = "tknMorph"
JSON_NAME_TOKEN_NORM_: str = "tknNorm_"
JSON_NAME_TOKEN_ORTH_: str = "tknOrth_"
JSON_NAME_TOKEN_POS_: str = "tknPos_"
JSON_NAME_TOKEN_PREFIX_: str = "tknPrefix_"
JSON_NAME_TOKEN_PROB: str = "tknProb"
JSON_NAME_TOKEN_RANK: str = "tknRank"
JSON_NAME_TOKEN_RIGHT_EDGE: str = "tknRightEdge"
JSON_NAME_TOKEN_SENT: str = "tknSent"
JSON_NAME_TOKEN_SENTIMENT: str = "tknSentiment"
JSON_NAME_TOKEN_SHAPE_: str = "tknShape_"
JSON_NAME_TOKEN_SUFFIX_: str = "tknSuffix_"
JSON_NAME_TOKEN_TAG_: str = "tknTag_"
JSON_NAME_TOKEN_TENSOR: str = "tknTensor"
JSON_NAME_TOKEN_TEXT: str = "tknText"
JSON_NAME_TOKEN_TEXT_WITH_WS: str = "tknTextWithWs"
JSON_NAME_TOKEN_VOCAB: str = "tknVocab"
JSON_NAME_TOKEN_WHITESPACE_: str = "tknWhitespace_"

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
PARSE_TAG_CELL: str = "Cell"
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
PARSE_TAG_ROW: str = "Row"
PARSE_TAG_SIGNATURE_FIELDS: str = "SignatureFields"
PARSE_TAG_TABLE: str = "Table"
PARSE_TAG_TEXT: str = "Text"
PARSE_TAG_TITLE: str = "Title"
PARSE_TAG_WORD: str = "Word"
PARSE_TAG_XFA: str = "XFA"

TESTS_INBOX_NAME: str = "tests/__PYTEST_FILES__/"

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
action_curr: Type[db.cls_action.Action]
action_next: Type[db.cls_action.Action]

base: Type[db.cls_base.Base]

db_current_database: str
db_current_user: str
db_driver_conn: psycopg2.extensions.connection | None = None
db_driver_cur: psycopg2.extensions.cursor | None = None
db_orm_engine: sqlalchemy.engine.Engine | None = None
db_orm_metadata: sqlalchemy.MetaData | None = None

directory_inbox: os.PathLike[str] | str
directory_inbox_accepted: os.PathLike[str] | str
directory_inbox_rejected: os.PathLike[str] | str

document_child_no_children: sqlalchemy.Integer | None
document_child_directory_name: str
document_child_directory_type: str
document_child_error_code: str | None
document_child_file_name: str
document_child_file_type: str
document_child_id: sqlalchemy.Integer
document_child_id_base: sqlalchemy.Integer | None
document_child_id_parent: sqlalchemy.Integer | None
document_child_id_language: sqlalchemy.Integer
document_child_next_step: str | None
document_no_children: sqlalchemy.Integer | None
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
document_id_language: sqlalchemy.Integer
document_next_step: str | None
document_sha256: str | None
document_status: str
document_stem_name: str

language: Type[db.cls_language.Language]

languages_pandoc: Dict[sqlalchemy.Integer, str]
languages_spacy: Dict[sqlalchemy.Integer, str]
languages_tesseract: Dict[sqlalchemy.Integer, str]

line_type: Type[nlp.cls_line_type.LineType]

logger: logging.Logger

# {
#     "lineIndexPage": 0,
#     "paraIndexPage": 0,
#     "lineIndexPara": 0,
#     "lineText": "Start Document ...",
#     "lineType": "b"
# },
# parse_result_line_0_line: Dict[str, int | str]

parse_result_line_1_lines: List[Dict[str, int | str]]

# {
#     "pageNo": 1,
#     "noLinesInPage": 21,
#     "noParasInPage": 10,
#     "lines": [
#         {
# parse_result_line_2_page: Dict[str, int | str | List[Dict[str, int | str]]]

parse_result_line_3_pages: List[Dict[str, int | str | List[Dict[str, int | str]]]]

# {
#   "baseId": 3,
#   "baseFileName": "case_3_pdf_text_route_inbox_pdflib.pdf",
#   "noPagesInDoc": 3,
#   "pages": [
#     {
parse_result_line_4_document: Dict[str, int | str | List[Dict[str, int | str | List[Dict[str, int | str]]]]]

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
parse_result_page_words: Dict[str, int | List[Dict[str, int | str]]]
parse_result_pages_word: Dict[str, int | List[Dict[str, int | List[Dict[str, int | str]]]]]
parse_result_para_index_page: int
parse_result_text: str

# {
#     "lineIndexPage": 0,
#     "wordIndexLine": 0,
#     "wordText": "Start"
# },
# parse_result_word_0_word: Dict[str, int | str]

parse_result_word_1_words: List[Dict[str, int | str]]

# {
#     "pageNo": 1,
#     "lines": [
#         {
# parse_result_word_2_page: Dict[str, int | str | List[Dict[str, int | str]]]


parse_result_word_3_pages: List[Dict[str, int | str | List[Dict[str, int | str]]]]

# {
#   "baseId": 3,
#   "baseFileName": "case_3_pdf_text_route_inbox_pdflib.pdf",
#   "noPagesInDoc": 3,
#   "pages": [
#     {
parse_result_word_4_document: Dict[str, int | str | List[Dict[str, int | str | List[Dict[str, int | str]]]]]

parse_result_word_index_line: int
parse_result_word_index_page: int
parse_result_word_index_para: int

run: Type[db.cls_run.Run]

setup: Type[cfg.cls_setup.Setup]

spacy_tkn_attr_cluster: bool = False
spacy_tkn_attr_dep_: bool = False
spacy_tkn_attr_doc: bool = False
spacy_tkn_attr_ent_iob_: bool = False
spacy_tkn_attr_ent_kb_id_: bool = False
spacy_tkn_attr_ent_type_: bool = True
spacy_tkn_attr_head: bool = False
spacy_tkn_attr_i: bool = True
spacy_tkn_attr_idx: bool = False
spacy_tkn_attr_is_alpha: bool = False
spacy_tkn_attr_is_ascii: bool = False
spacy_tkn_attr_is_bracket: bool = False
spacy_tkn_attr_is_currency: bool = True
spacy_tkn_attr_is_digit: bool = True
spacy_tkn_attr_is_left_punct: bool = False
spacy_tkn_attr_is_lower: bool = False
spacy_tkn_attr_is_oov: bool = True
spacy_tkn_attr_is_punct: bool = True
spacy_tkn_attr_is_quote: bool = False
spacy_tkn_attr_is_right_punct: bool = False
spacy_tkn_attr_is_sent_end: bool = False
spacy_tkn_attr_is_sent_start: bool = False
spacy_tkn_attr_is_space: bool = False
spacy_tkn_attr_is_stop: bool = True
spacy_tkn_attr_is_title: bool = True
spacy_tkn_attr_is_upper: bool = False
spacy_tkn_attr_lang_: bool = False
spacy_tkn_attr_left_edge: bool = False
spacy_tkn_attr_lemma_: bool = True
spacy_tkn_attr_lex: bool = False
spacy_tkn_attr_lex_id: bool = False
spacy_tkn_attr_like_email: bool = True
spacy_tkn_attr_like_num: bool = True
spacy_tkn_attr_like_url: bool = True
spacy_tkn_attr_lower_: bool = False
spacy_tkn_attr_morph: bool = False
spacy_tkn_attr_norm_: bool = True
spacy_tkn_attr_orth_: bool = False
spacy_tkn_attr_pos_: bool = True
spacy_tkn_attr_prefix_: bool = False
spacy_tkn_attr_prob: bool = False
spacy_tkn_attr_rank: bool = False
spacy_tkn_attr_right_edge: bool = False
spacy_tkn_attr_sent: bool = False
spacy_tkn_attr_sentiment: bool = False
spacy_tkn_attr_shape_: bool = False
spacy_tkn_attr_suffix_: bool = False
spacy_tkn_attr_tag_: bool = True
spacy_tkn_attr_tensor: bool = False
spacy_tkn_attr_text: bool = True
spacy_tkn_attr_text_with_ws: bool = False
spacy_tkn_attr_vocab: bool = False
spacy_tkn_attr_whitespace_: bool = True

start_time_document: int
