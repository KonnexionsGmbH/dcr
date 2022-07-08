# -*- coding: utf-8 -*-

"""Module cfg.glob: DCR Global Data."""
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
import nlp.cls_line_type_list_bullet
import nlp.cls_line_type_list_number
import nlp.cls_line_type_table
import nlp.cls_line_type_toc
import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
FILE_ENCODING_DEFAULT = "utf-16"

INFORMATION_NOT_YET_AVAILABLE = "n/a"

LOGGER_END = "End"
LOGGER_FATAL_HEAD = "FATAL ERROR: program abort =====> "
LOGGER_FATAL_TAIL = " <===== FATAL ERROR"
LOGGER_PROGRESS_UPDATE = "Progress update "
LOGGER_START = "Start"

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
line_type_list_bullet: type[nlp.cls_line_type_list_bullet.LineTypeListBullet]
line_type_list_number: type[nlp.cls_line_type_list_number.LineTypeListNumber]
line_type_table: type[nlp.cls_line_type_table.LineTypeTable]
line_type_toc: type[nlp.cls_line_type_toc.LineTypeToc]

logger: logging.Logger

run: type[db.cls_run.Run]

setup: type[cfg.cls_setup.Setup]

start_time_document: int

text_parser: type[nlp.cls_text_parser.TextParser]

tokenizer_spacy: type[nlp.cls_tokenizer_spacy.TokenizerSpacy]
