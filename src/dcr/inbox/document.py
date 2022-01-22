"""
### **Check and distribute incoming documents**.

New documents are made available in one of the two file directories
input or input_ocr. These are then checked and moved to the accepted or
rejected file directories depending on the result of the check.
"""

import logging
import logging.config
import os
import pathlib
import shutil
from datetime import datetime

import sqlalchemy
# -----------------------------------------------------------------------------
# Convert the files in the inbox.
# -----------------------------------------------------------------------------
from utils.constant import DCR_CFG_DIRECTORY_INBOX
from utils.constant import DCR_CFG_DIRECTORY_INBOX_ACCEPTED
from utils.constant import DCR_CFG_DIRECTORY_INBOX_REJECTED
from utils.constant import FILE_EXTENSION_PDF
from utils.constant import LOGGER_END
from utils.constant import LOGGER_PROGRESS_UPDATE
from utils.constant import LOGGER_START


def process_inbox(
    logger: logging.Logger,
    config: dict[str, str],
    _engine: sqlalchemy.engine.base.Engine,
) -> None:
    """
    **Process the files in the inbox**.

    1. Documents of type `doc`, `docx` or `txt` are converted to `pdf` format
       and copied to the `inbox_accepted` directory.
    2. Documents of type `pdf` that do not consist only of a scanned image are
       copied unchanged to the `inbox_accepted` directory.
    3. Documents of type `pdf` consisting only of a scanned image are copied
       unchanged to the `inbox_ocr` directory.
    4. All other documents are copied to the `inbox_rejected` directory.
    5. For each document an new entry is created in the database table
       `document`.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    - **config (dict[str, str])**: Configuration parameters.
    - **_engine (sqlalchemy.engine.base.Engine)**:
                                 Database state.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    accepted = pathlib.Path(config[DCR_CFG_DIRECTORY_INBOX_ACCEPTED])
    try:
        os.mkdir(accepted)
    except OSError:
        pass

    inbox = pathlib.Path(config[DCR_CFG_DIRECTORY_INBOX])

    rejected = pathlib.Path(config[DCR_CFG_DIRECTORY_INBOX_REJECTED])
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
                logger.info(
                    "files_2_pdfs(): unsupported file type: '"
                    + file.name
                    + "'"
                )
                shutil.move(
                    str(inbox) + "/" + file.name,
                    str(rejected) + "/" + file.name,
                )

    print(
        LOGGER_PROGRESS_UPDATE
        + str(datetime.now())
        + " : The documents in the inbox file directory are checked and "
        "prepared for further processing."
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)
