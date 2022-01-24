"""
### Module: **Check and distribute incoming documents**.

New documents are made available in one of the two file directories
input or input_ocr. These are then checked and moved to the accepted or
rejected file directories depending on the result of the check.
"""

import datetime
import logging
import logging.config
import os
import pathlib
import shutil

from globals import CONFIG
from globals import DCR_CFG_DIRECTORY_INBOX
from globals import DCR_CFG_DIRECTORY_INBOX_ACCEPTED
from globals import DCR_CFG_DIRECTORY_INBOX_REJECTED
from globals import FILE_EXTENSION_PDF
from globals import LOGGER
from globals import LOGGER_END
from globals import LOGGER_PROGRESS_UPDATE
from globals import LOGGER_START


# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Convert the files in the inbox.
# -----------------------------------------------------------------------------


def process_inbox() -> None:
    """
    #### Function: **Process the files in the inbox**.

    1. Documents of type `doc`, `docx` or `txt` are converted to `pdf` format
       and copied to the `inbox_accepted` directory.
    2. Documents of type `pdf` that do not consist only of a scanned image are
       copied unchanged to the `inbox_accepted` directory.
    3. Documents of type `pdf` consisting only of a scanned image are copied
       unchanged to the `inbox_ocr` directory.
    4. All other documents are copied to the `inbox_rejected` directory.
    5. For each document an new entry is created in the database table
       `document`.
    """
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(LOGGER_START)

    accepted = CONFIG[DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    try:
        os.mkdir(accepted)
    except OSError:
        pass

    inbox = CONFIG[DCR_CFG_DIRECTORY_INBOX]

    rejected = CONFIG[DCR_CFG_DIRECTORY_INBOX_REJECTED]
    try:
        os.mkdir(rejected)
    except OSError:
        pass

    files = pathlib.Path(inbox)
    for file in files.iterdir():
        if file.is_file():
            extension = file.suffix.lower()
            if extension == FILE_EXTENSION_PDF:
                shutil.move(
                    str(inbox) + "/" + file.name,
                    str(accepted) + "/" + file.name,
                )
            else:
                LOGGER.info(
                    "files_2_pdfs(): unsupported file type: '%s'", file.name
                )
                shutil.move(
                    str(inbox) + "/" + file.name,
                    str(rejected) + "/" + file.name,
                )

    print(
        LOGGER_PROGRESS_UPDATE,
        str(datetime.datetime.now()),
        " : The documents in the inbox file directory are checked and ",
        "prepared for further processing",
    )

    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(LOGGER_END)
