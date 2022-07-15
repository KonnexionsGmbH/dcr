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

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
LOGGER_END = "End"
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

logger: logging.Logger

run: type[db.cls_run.Run]

setup: type[cfg.cls_setup.Setup]

start_time_document: int
