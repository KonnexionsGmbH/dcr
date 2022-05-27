"""Module cfg.glob: DCR Global Data."""
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
DB_DIALECT_POSTGRESQL: str = "postgresql"

DBC_ACTION_CODE: str = "action_code"
DBC_ACTION_CODE_LAST: str = "action_code_last"
DBC_ACTION_TEXT: str = "action_text"
DBC_ACTION_TEXT_LAST: str = "action_text_last"
DBC_ACTIVE: str = "active"
DBC_CODE_ISO_639_3: str = "code_iso_639_3"
DBC_CODE_ISO_639_3_DEFAULT: str = "eng"
DBC_CODE_PANDOC: str = "code_pandoc"
DBC_CODE_PANDOC_DEFAULT: str = "en"
DBC_CODE_SPACY: str = "code_spacy"
DBC_CODE_SPACY_DEFAULT: str = "en_core_web_trf"
DBC_CODE_TESSERACT: str = "code_tesseract"
DBC_CODE_TESSERACT_DEFAULT: str = "eng"
DBC_CREATED_AT: str = "created_at"
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
DBC_ID_DOCUMENT: str = "id_document"
DBC_ID_LANGUAGE: str = "id_language"
DBC_ID_PARENT: str = "id_parent"
DBC_ID_RUN: str = "id_run"
DBC_ID_RUN_LAST: str = "id_run_last"
DBC_ISO_LANGUAGE_NAME: str = "iso_language_name"
DBC_ISO_LANGUAGE_NAME_DEFAULT: str = "English"
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
DBT_DOCUMENT: str = "document"
DBT_LANGUAGE: str = "language"
DBT_RUN: str = "run"
DBT_TOKEN: str = "token"
DBT_VERSION: str = "version"

FILE_ENCODING_DEFAULT: str = "utf-8"

INFORMATION_NOT_YET_AVAILABLE: str = "n/a"

LOGGER_END: str = "End"
LOGGER_FATAL_HEAD: str = "FATAL ERROR: program abort =====> "
LOGGER_FATAL_TAIL: str = " <===== FATAL ERROR"
LOGGER_PROGRESS_UPDATE: str = "Progress update "
LOGGER_START: str = "Start"

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
