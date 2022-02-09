"""Check and distribute incoming documents.

New documents are made available in the file directory inbox.
These are then checked and moved to the accepted or
rejected file directories depending on the result of the check.
Depending on the file format, the accepted documents are then
converted into the pdf file format either with the help of Pandoc
or with the help of Tesseract OCR.
"""
import inspect
import logging.config
import os
import pathlib
import shutil

from libs import cfg
from libs import db
from libs import utils


# -----------------------------------------------------------------------------
# Check the inbox file directories and create the missing ones.
# -----------------------------------------------------------------------------
def check_and_create_inboxes(logger: logging.Logger) -> None:
    """Check the inbox file directories and create the missing ones.

    The file directory inbox must exist. The two file directories
    inbox_accepted and inbox_rejected are created if they do not
    already exist.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    cfg.inbox = cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX]
    if not os.path.isdir(cfg.inbox):
        utils.terminate_fatal(
            logger,
            "The input directory with the name "
            + cfg.inbox
            + " does not exist - error="
            + str(OSError),
        )

    cfg.inbox_accepted = cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    create_directory(logger, "the accepted documents", cfg.inbox_accepted)

    cfg.inbox_rejected = cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]
    create_directory(logger, "the rejected documents", cfg.inbox_rejected)

    db.update_dbt_id(
        logger,
        cfg.DBT_RUN,
        cfg.run_id,
        {
            cfg.DBC_INBOX_ABS_NAME: str(pathlib.Path(cfg.inbox).absolute()),
            cfg.DBC_INBOX_CONFIG: cfg.inbox,
            cfg.DBC_INBOX_ACCEPTED_ABS_NAME: str(
                pathlib.Path(cfg.inbox_accepted).absolute()
            ),
            cfg.DBC_INBOX_ACCEPTED_CONFIG: cfg.inbox_accepted,
            cfg.DBC_INBOX_REJECTED_ABS_NAME: str(
                pathlib.Path(cfg.inbox_rejected).absolute()
            ),
            cfg.DBC_INBOX_REJECTED_CONFIG: cfg.inbox_rejected,
        },
    )

    logger.debug(cfg.LOGGER_END)


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
            utils.progress_msg(
                logger,
                "The file directory for "
                + directory_type
                + " was "
                + "newly created under the name "
                + directory_name,
            )
        except OSError:
            utils.terminate_fatal(
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
# Process the document action 'start'.
# -----------------------------------------------------------------------------
def process_document_action_start(
    logger: logging.Logger, file: pathlib.Path
) -> None:
    """Process the document action 'start'.

    Analyses the file name and creates an entry in each of the two database
    tables document and journal.

    Args:
        logger (logging.Logger): Current logger.
        file (pathlib.Path): File.
    """
    logger.debug(cfg.LOGGER_START)

    cfg.CURRENT_FILE_NAME = file.name
    cfg.CURRENT_STEM_NAME = pathlib.PurePath(file).stem
    cfg.CURRENT_FILE_TYPE = file.suffix[1:].lower()

    db.insert_dbt_document_row(logger)

    db.insert_dbt_journal_row(
        logger,
        cfg.JOURNAL_ACTION_01_001,
        __name__,
        inspect.stack()[0][3],
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Reject a new document that is faulty.
# -----------------------------------------------------------------------------
def process_document_rejected(
    logger: logging.Logger, action: str, module_name: str, function_name: str
) -> None:
    """Reject a new document that is faulty.

    Args:
        logger (logging.Logger): Current logger.
        action (str): Current action.
        module_name (str): Current module.
        function_name (str): Current function.
    """
    logger.debug(cfg.LOGGER_START)

    source_file = os.path.join(
        cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX], cfg.CURRENT_FILE_NAME
    )
    target_file = os.path.join(
        cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED],
        cfg.CURRENT_FILE_NAME + "_" + str(cfg.document_id),
    )

    try:
        shutil.move(source_file, target_file)
    except shutil.Error as err:
        utils.terminate_fatal(
            logger,
            "Issue when moving "
            + source_file
            + " to "
            + target_file
            + " - error="
            + str(err),
        )

    db.update_dbt_id(
        logger,
        cfg.DBT_DOCUMENT,
        cfg.run_id,
        {
            cfg.DBC_STATUS: cfg.STATUS_REJECTED,
        },
    )

    db.insert_dbt_journal_row(
        logger,
        action,
        module_name,
        function_name,
    )

    cfg.total_rejected += 1

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the new document input in the file directory inbox.
# -----------------------------------------------------------------------------
def process_inbox_new(logger: logging.Logger) -> None:
    """Process the new document input in the file directory inbox.

    1. Documents of type doc, docx or txt are converted to pdf format
       and copied to the inbox_accepted directory.
    2. Documents of type pdf that do not consist only of a scanned image are
       copied unchanged to the inbox_accepted directory.
    3. Documents of type pdf consisting only of a scanned image are copied
       unchanged to the inbox_ocr directory.
    4. All other documents are copied to the inbox_rejected directory.
    5. For each document a new entry is created in the database table
       document.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    # Check the inbox file directories and create the missing ones.
    check_and_create_inboxes(logger)

    for file in pathlib.Path(
        cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX]
    ).iterdir():
        if file.is_file():
            cfg.total_new += 1
            process_document_action_start(logger, file)
            if cfg.CURRENT_FILE_TYPE == cfg.FILE_TYPE_PDF:
                process_input_new_pdf(logger)
            elif cfg.CURRENT_FILE_TYPE == cfg.FILE_TYPE_TXT:
                process_input_new_pandoc(logger)
            else:
                process_document_rejected(
                    logger,
                    cfg.JOURNAL_ACTION_01_901,
                    __name__,
                    inspect.stack()[0][3],
                )

    # for file in pathlib.Path(inbox).iterdir():
    #     if file.is_file():
    #         TOTAL_NEW+1
    #         file.stat().
    #         extension = file.suffix.lower()
    #         if extension == FILE_EXTENSION_PDF:
    #             shutil.move(
    #                 inbox / file.name,
    #                 inbox_accepted / file.name,
    #             )
    #         else:
    #             logger.info(
    #                 "files_2_pdfs(): unsupported file type: '%s'", file.name
    #             )
    #             shutil.move(
    #                 inbox / file.name,
    #                 inbox_rejected / file.name,
    #             )

    utils.progress_msg(
        logger,
        "Number documents new      " + str(cfg.total_new)
    )
    utils.progress_msg(
        logger,
        "Number documents accepted " + str(cfg.total_accepted)
    )
    utils.progress_msg(
        logger,
        "Number documents rejected " + str(cfg.total_rejected)
    )
    utils.progress_msg(
        logger,
        "The new documents in the inbox file directory are checked and "
        + "prepared for further processing",
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare the new documents in the input for Pandoc.
# -----------------------------------------------------------------------------
def process_input_new_pandoc(logger: logging.Logger) -> None:
    """Prepare the new documents in the input for Pandoc.

    Args:
        logger (logging.Logger): [description]
    """
    logger.debug(cfg.LOGGER_START)

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the new pdf documents in the input file directory.
# -----------------------------------------------------------------------------
def process_input_new_pdf(logger: logging.Logger) -> None:
    """Process the new pdf documents in the input file directory.

    Args:
        logger (logging.Logger): [description]
    """
    logger.debug(cfg.LOGGER_START)

    logger.debug(cfg.LOGGER_END)
