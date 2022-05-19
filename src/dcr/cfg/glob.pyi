"""Library Stub."""
from __future__ import annotations

import logging
import os
from typing import Dict
from typing import List
from typing import Type

import cfg.cls_setup
import db.cls_action
import db.cls_document
import db.cls_language
import db.cls_run
import nlp.cls_line_type
import psycopg2.extensions
import sqlalchemy

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
DB_DIALECT_POSTGRESQL: str

DBC_ACTION_CODE: str
DBC_ACTION_CODE_LAST: str
DBC_ACTION_TEXT: str
DBC_ACTION_TEXT_LAST: str
DBC_ACTIVE: str
DBC_CODE_ISO_639_3: str
DBC_CODE_PANDOC: str
DBC_CODE_SPACY: str
DBC_CODE_TESSERACT: str
DBC_CREATED_AT: str
DBC_DIRECTORY_NAME: str
DBC_DIRECTORY_NAME_INBOX: str
DBC_DIRECTORY_TYPE: str
DBC_DURATION_NS: str
DBC_ERROR_CODE: str
DBC_ERROR_CODE_LAST: str
DBC_ERROR_MSG: str
DBC_ERROR_MSG_LAST: str
DBC_ERROR_NO: str
DBC_FILE_NAME: str
DBC_FILE_SIZE_BYTES: str
DBC_ID: str
DBC_ID_DOCUMENT: str
DBC_ID_LANGUAGE: str
DBC_ID_PARENT: str
DBC_ID_RUN: str
DBC_ID_RUN_LAST: str
DBC_ISO_LANGUAGE_NAME: str
DBC_MODIFIED_AT: str
DBC_NO_CHILDREN: str
DBC_NO_PDF_PAGES: str
DBC_PAGE_DATA: str
DBC_PAGE_NO: str
DBC_SHA256: str
DBC_STATUS: str
DBC_TOTAL_ERRONEOUS: str
DBC_TOTAL_PROCESSED_OK: str
DBC_TOTAL_PROCESSED_TO_BE: str
DBC_VERSION: str

DBT_ACTION: str
DBT_DOCUMENT: str
DBT_TOKEN: str
DBT_LANGUAGE: str
DBT_RUN: str
DBT_VERSION: str

DCR_ARGV_0: str

DOCUMENT_DIRECTORY_TYPE_INBOX: str
DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED: str
DOCUMENT_DIRECTORY_TYPE_INBOX_REJECTED: str

DOCUMENT_ERROR_CODE_REJ_FILE_DUPL: str
DOCUMENT_ERROR_CODE_REJ_FILE_EXT: str
DOCUMENT_ERROR_CODE_REJ_FILE_OPEN: str
DOCUMENT_ERROR_CODE_REJ_NO_PDF_FORMAT: str
DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE: str
DOCUMENT_ERROR_CODE_REJ_TESSERACT: str

DOCUMENT_FILE_TYPE_JPEG: str
DOCUMENT_FILE_TYPE_JPG: str
DOCUMENT_FILE_TYPE_JSON: str
DOCUMENT_FILE_TYPE_PANDOC: List[str]
DOCUMENT_FILE_TYPE_PDF: str
DOCUMENT_FILE_TYPE_PNG: str
DOCUMENT_FILE_TYPE_TESSERACT: List[str]
DOCUMENT_FILE_TYPE_TIF: str
DOCUMENT_FILE_TYPE_TIFF: str
DOCUMENT_FILE_TYPE_XML: str

DOCUMENT_LINE_TYPE_BODY: str
DOCUMENT_LINE_TYPE_FOOTER: str
DOCUMENT_LINE_TYPE_HEADER: str

DOCUMENT_STATUS_END: str
DOCUMENT_STATUS_ERROR: str
DOCUMENT_STATUS_START: str

ERROR_01_901: str
ERROR_01_903: str
ERROR_01_905: str
ERROR_01_906: str

ERROR_21_903: str

ERROR_31_902: str
ERROR_31_903: str

ERROR_41_901: str
ERROR_41_903: str
ERROR_41_904: str

ERROR_51_901: str
ERROR_51_904: str

FILE_ENCODING_DEFAULT: str

INFORMATION_NOT_YET_AVAILABLE: str

JSON_NAME_API_VERSION: str
JSON_NAME_COLUMN_NAME: str
JSON_NAME_COLUMN_VALUE: str
JSON_NAME_DATA: str
JSON_NAME_DOCUMENT_FILE_NAME: str
JSON_NAME_DOCUMENT_ID: str
JSON_NAME_LINE_INDEX_PAGE: str
JSON_NAME_LINE_INDEX_PARA: str
JSON_NAME_LINE_TEXT: str
JSON_NAME_LINE_TYPE: str
JSON_NAME_LINES: str
JSON_NAME_NO_LINES_IN_PAGE: str
JSON_NAME_NO_PAGES_IN_DOC: str
JSON_NAME_NO_PARAS_IN_PAGE: str
JSON_NAME_NO_TOKENS_IN_PAGE: str
JSON_NAME_PAGE_NO: str
JSON_NAME_PAGE_TEXT: str
JSON_NAME_PAGES: str
JSON_NAME_PARA_INDEX_PAGE: str
JSON_NAME_ROW: str
JSON_NAME_ROWS: str
JSON_NAME_TABLES: str
JSON_NAME_TABLE_NAME: str

JSON_NAME_TOKEN_CLUSTER: str
JSON_NAME_TOKEN_DEP_: str
JSON_NAME_TOKEN_DOC: str
JSON_NAME_TOKEN_ENT_IOB_: str
JSON_NAME_TOKEN_ENT_KB_ID_: str
JSON_NAME_TOKEN_ENT_TYPE_: str
JSON_NAME_TOKEN_HEAD: str
JSON_NAME_TOKEN_I: str
JSON_NAME_TOKEN_IDX: str
JSON_NAME_TOKEN_IS_ALPHA: str
JSON_NAME_TOKEN_IS_ASCII: str
JSON_NAME_TOKEN_IS_BRACKET: str
JSON_NAME_TOKEN_IS_CURRENCY: str
JSON_NAME_TOKEN_IS_DIGIT: str
JSON_NAME_TOKEN_IS_LEFT_PUNCT: str
JSON_NAME_TOKEN_IS_LOWER: str
JSON_NAME_TOKEN_IS_OOV: str
JSON_NAME_TOKEN_IS_PUNCT: str
JSON_NAME_TOKEN_IS_QUOTE: str
JSON_NAME_TOKEN_IS_RIGHT_PUNCT: str
JSON_NAME_TOKEN_IS_SENT_END: str
JSON_NAME_TOKEN_IS_SENT_START: str
JSON_NAME_TOKEN_IS_SPACE: str
JSON_NAME_TOKEN_IS_STOP: str
JSON_NAME_TOKEN_IS_TITLE: str
JSON_NAME_TOKEN_IS_UPPER: str
JSON_NAME_TOKEN_LANG_: str
JSON_NAME_TOKEN_LEFT_EDGE: str
JSON_NAME_TOKEN_LEMMA_: str
JSON_NAME_TOKEN_LEX: str
JSON_NAME_TOKEN_LEX_ID: str
JSON_NAME_TOKEN_LIKE_EMAIL: str
JSON_NAME_TOKEN_LIKE_NUM: str
JSON_NAME_TOKEN_LIKE_URL: str
JSON_NAME_TOKEN_LOWER_: str
JSON_NAME_TOKEN_MORPH: str
JSON_NAME_TOKEN_NORM_: str
JSON_NAME_TOKEN_ORTH_: str
JSON_NAME_TOKEN_POS_: str
JSON_NAME_TOKEN_PREFIX_: str
JSON_NAME_TOKEN_PROB: str
JSON_NAME_TOKEN_RANK: str
JSON_NAME_TOKEN_RIGHT_EDGE: str
JSON_NAME_TOKEN_SENT: str
JSON_NAME_TOKEN_SENTIMENT: str
JSON_NAME_TOKEN_SHAPE_: str
JSON_NAME_TOKEN_SUFFIX_: str
JSON_NAME_TOKEN_TAG_: str
JSON_NAME_TOKEN_TENSOR: str
JSON_NAME_TOKEN_TEXT: str
JSON_NAME_TOKEN_TEXT_WITH_WS: str
JSON_NAME_TOKEN_VOCAB: str
JSON_NAME_TOKEN_WHITESPACE_: str

JSON_NAME_TOKENS: str

JSON_NAME_WORD_INDEX_LINE: str
JSON_NAME_WORD_TEXT: str
JSON_NAME_WORDS: str

LOCALE: str
LOGGER_CFG_FILE: str
LOGGER_END: str
LOGGER_FATAL_HEAD: str
LOGGER_FATAL_TAIL: str
LOGGER_PROGRESS_UPDATE: str
LOGGER_START: str

PARSE_NAME_SPACE: str

PARSE_TAG_ACTION: str
PARSE_TAG_ANNOTATIONS: str
PARSE_TAG_ATTACHMENTS: str
PARSE_TAG_AUTHOR: str
PARSE_TAG_BOOKMARKS: str
PARSE_TAG_BOX: str
PARSE_TAG_CELL: str
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
PARSE_TAG_ROW: str
PARSE_TAG_SIGNATURE_FIELDS: str
PARSE_TAG_TABLE: str
PARSE_TAG_TEXT: str
PARSE_TAG_TITLE: str
PARSE_TAG_WORD: str
PARSE_TAG_XFA: str

TESTS_INBOX_NAME: str

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
action_curr: Type[db.cls_action.Action]
action_next: Type[db.cls_action.Action]

document: Type[db.cls_document.Document]

db_current_database: str
db_current_user: str
db_driver_conn: psycopg2.extensions.connection | None = None
db_driver_cur: psycopg2.extensions.cursor | None = None
db_orm_engine: sqlalchemy.engine.Engine | None = None
db_orm_metadata: sqlalchemy.MetaData | None = None

directory_inbox: os.PathLike[str] | str
directory_inbox_accepted: os.PathLike[str] | str
directory_inbox_rejected: os.PathLike[str] | str

language: Type[db.cls_language.Language]

languages_pandoc: Dict[sqlalchemy.Integer, str]
languages_spacy: Dict[sqlalchemy.Integer, str]
languages_tesseract: Dict[sqlalchemy.Integer, str]

line_type: Type[nlp.cls_line_type.LineType]

logger: logging.Logger

parse_result_line_0_line: Dict[str, int | str]
parse_result_line_1_lines: List[Dict[str, int | str]]
parse_result_line_2_page: Dict[str, int | str | List[Dict[str, int | str]]]
parse_result_line_3_pages: List[Dict[str, int | str | List[Dict[str, int | str]]]]
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
parse_result_page_0_paras: List[str]
# parse_result_page_1_page: Dict[str, int | str | List[str]]
parse_result_page_2_pages: List[Dict[str, int | str | List[str]]]
parse_result_page_3_document: Dict[str, int | str | List[Dict[str, int | str | List[str]]]]
parse_result_page_index_doc: int
parse_result_para_index_page: int
parse_result_text: str
# parse_result_word_0_word: Dict[str, int | str]
parse_result_word_1_words: List[Dict[str, int | str]]
# parse_result_word_2_page: Dict[str, int | str | List[Dict[str, int | str]]]
parse_result_word_3_pages: List[Dict[str, int | str | List[Dict[str, int | str]]]]
parse_result_word_4_document: Dict[str, int | str | List[Dict[str, int | str | List[Dict[str, int | str]]]]]
parse_result_word_index_line: int
parse_result_word_index_page: int
parse_result_word_index_para: int

run: Type[db.cls_run.Run]

setup: Type[cfg.cls_setup.Setup]

spacy_tkn_attr_cluster: bool
spacy_tkn_attr_dep_: bool
spacy_tkn_attr_doc: bool
spacy_tkn_attr_ent_iob_: bool
spacy_tkn_attr_ent_kb_id_: bool
spacy_tkn_attr_ent_type_: bool
spacy_tkn_attr_head: bool
spacy_tkn_attr_i: bool
spacy_tkn_attr_idx: bool
spacy_tkn_attr_is_alpha: bool
spacy_tkn_attr_is_ascii: bool
spacy_tkn_attr_is_bracket: bool
spacy_tkn_attr_is_currency: bool
spacy_tkn_attr_is_digit: bool
spacy_tkn_attr_is_left_punct: bool
spacy_tkn_attr_is_lower: bool
spacy_tkn_attr_is_oov: bool
spacy_tkn_attr_is_punct: bool
spacy_tkn_attr_is_quote: bool
spacy_tkn_attr_is_right_punct: bool
spacy_tkn_attr_is_sent_end: bool
spacy_tkn_attr_is_sent_start: bool
spacy_tkn_attr_is_space: bool
spacy_tkn_attr_is_stop: bool
spacy_tkn_attr_is_title: bool
spacy_tkn_attr_is_upper: bool
spacy_tkn_attr_lang_: bool
spacy_tkn_attr_left_edge: bool
spacy_tkn_attr_lemma_: bool
spacy_tkn_attr_lex: bool
spacy_tkn_attr_lex_id: bool
spacy_tkn_attr_like_email: bool
spacy_tkn_attr_like_num: bool
spacy_tkn_attr_like_url: bool
spacy_tkn_attr_lower_: bool
spacy_tkn_attr_morph: bool
spacy_tkn_attr_norm_: bool
spacy_tkn_attr_orth_: bool
spacy_tkn_attr_pos_: bool
spacy_tkn_attr_prefix_: bool
spacy_tkn_attr_prob: bool
spacy_tkn_attr_rank: bool
spacy_tkn_attr_right_edge: bool
spacy_tkn_attr_sent: bool
spacy_tkn_attr_sentiment: bool
spacy_tkn_attr_shape_: bool
spacy_tkn_attr_suffix_: bool
spacy_tkn_attr_tag_: bool
spacy_tkn_attr_tensor: bool
spacy_tkn_attr_text: bool
spacy_tkn_attr_text_with_ws: bool
spacy_tkn_attr_vocab: bool
spacy_tkn_attr_whitespace_: bool

start_time_document: int

token_0_token: Dict[str, bool | str]
token_1_tokens: List[Dict[str, bool | str]]
token_2_page: Dict[str, int | str | List[Dict[str, bool | str]]]
token_3_pages: List[Dict[str, int | str | List[Dict[str, bool | str]]]]
token_4_document: Dict[str, int | str | List[Dict[str, int | str | List[Dict[str, bool | str]]]]]
