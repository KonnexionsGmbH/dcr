"""### Module: **Definition of the Global Constants and Types**."""
from typing import Dict

from mypy.typeshed.stdlib.os import PathLike

ACTION_DB_CREATE_OR_UPGRADE: str = "d_c_u"
ACTION_NEW_COMPLETE: str = "new"
ACTION_PROCESS_INBOX: str = "p_i"
ACTION_PROCESS_INBOX_OCR: str = "p_i_o"

CONFIG: Dict[str, PathLike[str] | str] = {}

DCR_CFG_DATABASE_URL: str = "database_url"
DCR_CFG_DCR_VERSION: str = "dcr_version"
DCR_CFG_DIRECTORY_INBOX: str = "directory_inbox"
DCR_CFG_DIRECTORY_INBOX_ACCEPTED: str = "directory_inbox_accepted"
DCR_CFG_DIRECTORY_INBOX_OCR: str = "directory_inbox_ocr"
DCR_CFG_DIRECTORY_INBOX_OCR_ACCEPTED: str = "directory_inbox_ocr_accepted"
DCR_CFG_DIRECTORY_INBOX_OCR_REJECTED: str = "directory_inbox_ocr_rejected"
DCR_CFG_DIRECTORY_INBOX_REJECTED: str = "directory_inbox_rejected"
DCR_CFG_FILE: str = "setup.cfg"
DCR_CFG_SECTION: str = "dcr"

FILE_ENCODING_DEFAULT: str = "utf-8"
FILE_EXTENSION_PDF: str = ".pdf"

LOCALE: str = "de_CH.utf8"

LOGGER_CFG_FILE: str = "logging_cfg.yaml"
LOGGER_END: str = "End"
LOGGER_FATAL_HEAD: str = "FATAL ERROR: program abort =====> "
LOGGER_FATAL_TAIL: str = " <====="
LOGGER_PROGRESS_UPDATE: str = "Progress update "
LOGGER_START: str = "Start"
