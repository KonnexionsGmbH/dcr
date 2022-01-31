"""Check and distribute incoming documents.

New documents are made available in the file directory inbox.
These are then checked and moved to the accepted or
rejected file directories depending on the result of the check.
Depending on the file format, the accepted documents are then
converted into the pdf file format either with the help of Pandoc
or with the help of Tesseract OCR.
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
    """Create a new file directory if it does not already exist.

    Args:
        logger (logging.Logger): Current logger.
        directory_type (str): Directory type.
        directory_name (str): Directory name - may include a path.
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
                + str(OSError.errno)
                + " message="
                + OSError.strerror,
            )


# -----------------------------------------------------------------------------
# Process the new document input in the file directory inbox.
# -----------------------------------------------------------------------------
def process_inbox(logger: logging.Logger) -> None:
    """Process the new document input in the file directory inbox.

    1. Documents of type doc, docx or txt are converted to pdf format
       and copied to the inbox_accepted directory.
    2. Documents of type pdf that do not consist only of a scanned image are
       copied unchanged to the inbox_accepted directory.
    3. Documents of type pdf consisting only of a scanned image are copied
       unchanged to the inbox_ocr directory.
    4. All other documents are copied to the inbox_rejected directory.
    5. For each document an new entry is created in the database table
       document.

    Args:
        logger (logging.Logger): Current logger.
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

    inbox_accepted = CONFIG[DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    create_directory(logger, "the accepted documents", inbox_accepted)

    inbox_rejected = CONFIG[DCR_CFG_DIRECTORY_INBOX_REJECTED]
    create_directory(logger, "the rejected documents", inbox_rejected)

    process_new_input(logger, inbox, inbox_accepted, inbox_rejected)

    print(
        LOGGER_PROGRESS_UPDATE,
        str(datetime.datetime.now()),
        " : The new documents in the inbox file directory are checked and ",
        "prepared for further processing",
        sep="",
    )

    logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Process the new document input.
# -----------------------------------------------------------------------------
def process_new_input(
    logger: logging.Logger,
    inbox: str,
    inbox_accepted: str,
    inbox_rejected: str,
) -> None:
    """Process the new document input.

    1. Documents of type doc, docx or txt are converted to pdf format
       and copied to the inbox_accepted directory.
    2. Documents of type pdf that do not consist only of a scanned image are
       copied unchanged to the inbox_accepted directory.
    3. Documents of type pdf consisting only of a scanned image are copied
       unchanged to the inbox_ocr directory.
    4. All other documents are copied to the inbox_rejected directory.
    5. For each document an new entry is created in the database table
       document.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(LOGGER_START)

    files = pathlib.Path(inbox)
    for file in files.iterdir():
        if file.is_file():
            extension = file.suffix.lower()
            if extension == FILE_EXTENSION_PDF:
                shutil.move(
                    inbox / file.name,
                    inbox_accepted / file.name,
                )
            else:
                logger.info(
                    "files_2_pdfs(): unsupported file type: '%s'", file.name
                )
                shutil.move(
                    inbox / file.name,
                    inbox_rejected / file.name,
                )

    logger.debug(LOGGER_END)
