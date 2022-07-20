"""Library Stub."""
from __future__ import annotations

import logging
import os

import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_language
import db.cls_run

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
FILE_ENCODING_DEFAULT: str

LOGGER_END: str
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

logger: logging.Logger

run: type[db.cls_run.Run]

start_time_document: int
