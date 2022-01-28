"""
### Module: **Check and distribute incoming documents**.

New documents are made available in one of the two file directories
input or input_ocr. These are then checked and moved to the accepted or
rejected file directories depending on the result of the check.
"""

import datetime
import logging.config
import os
import pathlib
import shutil

from libs.globals import CONFIG
from libs.globals import DCR_CFG_DIRECTORY_INBOX
from libs.globals import DCR_CFG_DIRECTORY_INBOX_ACCEPTED
from libs.globals import DCR_CFG_DIRECTORY_INBOX_REJECTED
from libs.globals import FILE_EXTENSION_PDF
from libs.globals import LOGGER_END
from libs.globals import LOGGER_PROGRESS_UPDATE
from libs.globals import LOGGER_START
from libs.utils import terminate_fatal


# -----------------------------------------------------------------------------
# Create a new file directory if it does not already exist..
# -----------------------------------------------------------------------------


def create_directory(
    logger: logging.Logger, directory_type: str, directory_name: str
) -> None:
    """
    **Create a new file directory if it does not already exist**.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    - **directory_type (str)**:    Directory type.
    - **directory_name (str)**:    Directory name - may include a path.
    """
    if not os.path.isdir(directory_name):
        try:
            os.mkdir(directory_name)
            print(
                LOGGER_PROGRESS_UPDATE,
                str(datetime.datetime.now()),
                " : The file directory for " + directory_type + " was ",
                "newly created under the name ",
                directory_name,
                sep="",
            )
        except OSError:
            terminate_fatal(
                logger,
                " : The file directory for "
                + directory_type
                + " can "
                + "not be created under the name "
                + directory_name
                + " - error code="
                + OSError.errno
                + " message="
                + OSError.strerror,
            )


# -----------------------------------------------------------------------------
# Convert the files in the inbox.
# -----------------------------------------------------------------------------


def process_inbox(logger: logging.Logger) -> None:
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
    logger.debug(LOGGER_START)

    inbox = CONFIG[DCR_CFG_DIRECTORY_INBOX]
    if not os.path.isdir(inbox):
        terminate_fatal(
            logger,
            "The input directory with the name "
            + inbox
            + " does not exist - error="
            + str(OSError),
        )

    accepted = CONFIG[DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    create_directory(logger, "the accepted documents", accepted)

    rejected = CONFIG[DCR_CFG_DIRECTORY_INBOX_REJECTED]
    create_directory(logger, "the rejected documents", rejected)

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
        sep="",
    )

    logger.debug(LOGGER_END)
