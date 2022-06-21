"""Library Stub."""
from __future__ import annotations

import logging
import os

import cfg.cls_setup
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_language
import db.cls_run
import nlp.cls_line_type_headers_footers
import nlp.cls_line_type_heading
import nlp.cls_line_type_toc
import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
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
action_curr: type[db.cls_action.Action]
action_next: type[db.cls_action.Action]

db_core: type[db.cls_db_core.DBCore]

directory_inbox: os.PathLike[str] | str
directory_inbox_accepted: os.PathLike[str] | str
directory_inbox_rejected: os.PathLike[str] | str

document: type[db.cls_document.Document]

language: type[db.cls_language.Language]

line_type_headers_footers: type[nlp.cls_line_type_headers_footers.LineTypeHeaderFooters]
line_type_heading: type[nlp.cls_line_type_heading.LineTypeHeading]
line_type_toc: type[nlp.cls_line_type_toc.LineTypeToc]

logger: logging.Logger

run: type[db.cls_run.Run]

setup: type[cfg.cls_setup.Setup]

start_time_document: int

text_parser: type[nlp.cls_text_parser.TextParser]

tokenizer_spacy: type[nlp.cls_tokenizer_spacy.TokenizerSpacy]
