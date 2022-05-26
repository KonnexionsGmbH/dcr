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
import nlp.cls_text_parser
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

FILE_ENCODING_DEFAULT: str

INFORMATION_NOT_YET_AVAILABLE: str

LOGGER_END: str
LOGGER_FATAL_HEAD: str
LOGGER_FATAL_TAIL: str
LOGGER_PROGRESS_UPDATE: str
LOGGER_START: str

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

text_parser: Type[nlp.cls_text_parser.TextParser]

token_0_token: Dict[str, bool | str]
token_1_tokens: List[Dict[str, bool | str]]
token_2_page: Dict[str, int | str | List[Dict[str, bool | str]]]
token_3_pages: List[Dict[str, int | str | List[Dict[str, bool | str]]]]
token_4_document: Dict[str, int | str | List[Dict[str, int | str | List[Dict[str, bool | str]]]]]
