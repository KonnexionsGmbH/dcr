"""Library Stub."""
from __future__ import annotations

import logging
import os
from typing import Type

import cfg.cls_setup
import db.cls_action
import db.cls_document
import db.cls_language
import db.cls_run
import nlp.cls_line_type
import nlp.cls_text_parser
import nlp.cls_tokenize_spacy
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
DBC_CODE_ISO_639_3_DEFAULT: str
DBC_CODE_PANDOC: str
DBC_CODE_PANDOC_DEFAULT: str
DBC_CODE_SPACY: str
DBC_CODE_SPACY_DEFAULT: str
DBC_CODE_TESSERACT: str
DBC_CODE_TESSERACT_DEFAULT: str
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
DBC_ISO_LANGUAGE_NAME_DEFAULT: str
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

db_current_database: str
db_current_user: str
db_driver_conn: psycopg2.extensions.connection | None = None
db_driver_cur: psycopg2.extensions.cursor | None = None
db_orm_engine: sqlalchemy.engine.Engine | None = None
db_orm_metadata: sqlalchemy.MetaData | None = None

directory_inbox: os.PathLike[str] | str
directory_inbox_accepted: os.PathLike[str] | str
directory_inbox_rejected: os.PathLike[str] | str

document: Type[db.cls_document.Document]

language: Type[db.cls_language.Language]

line_type: Type[nlp.cls_line_type.LineType]

logger: logging.Logger

run: Type[db.cls_run.Run]

setup: Type[cfg.cls_setup.Setup]

start_time_document: int

text_parser: Type[nlp.cls_text_parser.TextParser]

tokenize_spacy: Type[nlp.cls_tokenize_spacy.TokenizeSpacy]
