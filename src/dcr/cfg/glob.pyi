"""Library Stub."""
from __future__ import annotations

import logging
import os

import dcr.db.cls_action
import dcr.db.cls_db_core
import dcr.db.cls_document
import dcr.db.cls_language
import dcr.db.cls_run

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
FILE_ENCODING_DEFAULT: str

LOGGER_END: str
LOGGER_START: str

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
action_curr: dcr.db.cls_action.Action
action_next: dcr.db.cls_action.Action

db_core: dcr.db.cls_db_core.DBCore

directory_inbox: os.PathLike[str] | str
directory_inbox_accepted: os.PathLike[str] | str
directory_inbox_rejected: os.PathLike[str] | str

document: dcr.db.cls_document.Document

language: dcr.db.cls_language.Language

logger: logging.Logger

run: dcr.db.cls_run.Run

start_time_document: int
