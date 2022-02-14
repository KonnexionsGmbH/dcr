"""Module inbox: Check and distribute incoming documents.

New documents are made available in the file directory inbox.
These are then checked and moved to the accepted or
rejected file directories depending on the result of the check.
Depending on the file format, the accepted documents are then
converted into the pdf file format either with the help of Pandoc
or with the help of Tesseract OCR.
"""
import inspect
import os
import pathlib
import shutil
from typing import Callable

import fitz
from libs import cfg
from libs import db
from libs import utils


# -----------------------------------------------------------------------------
# Check the inbox file directories and create the missing ones.
# -----------------------------------------------------------------------------
def check_and_create_directories() -> None:
    """Check the inbox file directories and create the missing ones.

    The file directory inbox must exist. The two file directories
    inbox_accepted and inbox_rejected are created if they do not
    already exist.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    cfg.directory_inbox = cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX]
    if not os.path.isdir(cfg.directory_inbox):
        utils.terminate_fatal(
            "The inbox directory with the name "
            + cfg.directory_inbox
            + " does not exist - error="
            + str(OSError),
        )

    cfg.directory_inbox_accepted = cfg.config[
        cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    ]
    create_directory("the accepted documents", cfg.directory_inbox_accepted)

    cfg.directory_inbox_rejected = cfg.config[
        cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED
    ]
    create_directory("the rejected documents", cfg.directory_inbox_rejected)

    db.update_dbt_id(
        db.DBT_RUN,
        cfg.run_id,
        {
            db.DBC_INBOX_ABS_NAME: str(
                pathlib.Path(cfg.directory_inbox).absolute()
            ),
            db.DBC_INBOX_CONFIG: cfg.directory_inbox,
            db.DBC_INBOX_ACCEPTED_ABS_NAME: str(
                pathlib.Path(cfg.directory_inbox_accepted).absolute()
            ),
            db.DBC_INBOX_ACCEPTED_CONFIG: cfg.directory_inbox_accepted,
            db.DBC_INBOX_REJECTED_ABS_NAME: str(
                pathlib.Path(cfg.directory_inbox_rejected).absolute()
            ),
            db.DBC_INBOX_REJECTED_CONFIG: cfg.directory_inbox_rejected,
        },
    )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create a new file directory if it does not already exist..
# -----------------------------------------------------------------------------
def create_directory(directory_type: str, directory_name: str) -> None:
    """Create a new file directory if it does not already exist.

    Args:
        directory_type (str): Directory type.
        directory_name (str): Directory name - may include a path.
    """
    if not os.path.isdir(directory_name):
        try:
            os.mkdir(directory_name)
            utils.progress_msg(
                "The file directory for "
                + directory_type
                + " was "
                + "newly created under the name "
                + directory_name,
            )
        except OSError as err:
            utils.terminate_fatal(
                " : The file directory for "
                + directory_type
                + " can "
                + "not be created under the name "
                + directory_name
                + " - error code="
                + str(err.errno)
                + " message="
                + err.strerror,
            )


# -----------------------------------------------------------------------------
# Prepare a new pdf document for further processing..
# -----------------------------------------------------------------------------
def prepare_pdf() -> None:
    """Prepare a new pdf document for further processing."""
    cfg.logger.debug(cfg.LOGGER_START)

    try:
        extracted_text = "".join(
            [
                page.get_text()
                for page in fitz.open(utils.get_file_name_inbox())
            ]
        )

        if bool(extracted_text):
            action: str = cfg.JOURNAL_ACTION_11_003
            status: str = cfg.STATUS_PARSER_READY
        else:
            action: str = cfg.JOURNAL_ACTION_11_005
            status: str = cfg.STATUS_TESSERACT_PDF_READY

        process_inbox_accepted(
            db.update_document_status(
                action,
                inspect.stack()[0][3],
                __name__,
                status,
            ),
            utils.get_file_name_inbox_accepted(),
        )
    except RuntimeError as err:
        process_inbox_rejected(
            db.update_document_status(
                cfg.JOURNAL_ACTION_01_904.replace(
                    "{source_file}", utils.get_file_name_inbox()
                ).replace("{error_msg}", str(err)),
                inspect.stack()[0][3],
                __name__,
                cfg.STATUS_REJECTED_NO_PDF_FORMAT,
            ),
        )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Accept a new document.
# -----------------------------------------------------------------------------
def process_inbox_accepted(
    update_document_status: Callable[[str, str, str, str], None],
    target_file_name: str,
) -> None:
    """Accept a new document.

    Args:
        target_file_name (str): File name in the directory inbox_accepted.
        update_document_status (db.update_document_status): Function to update
                    the document status and create a new journal entry.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    try:
        shutil.move(utils.get_file_name_inbox(), target_file_name)

        # pylint: disable=pointless-statement
        update_document_status

        cfg.total_accepted += 1
    except PermissionError as err:
        db.update_document_status(
            cfg.JOURNAL_ACTION_01_905.replace(
                "{source_file}", utils.get_file_name_inbox()
            )
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror),
            inspect.stack()[0][3],
            __name__,
            cfg.STATUS_REJECTED_FILE_PERMISSION,
        )
        remove_optional_file(target_file_name)
    except shutil.Error as err:
        cfg.total_erroneous += 1
        db.update_document_status(
            cfg.JOURNAL_ACTION_01_902.replace(
                "{source_file}", utils.get_file_name_inbox()
            )
            .replace("{target_file}", target_file_name)
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror),
            inspect.stack()[0][3],
            __name__,
            cfg.STATUS_REJECTED_ERROR,
        )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise a new document in the database and in the journal.
# -----------------------------------------------------------------------------
def process_inbox_document_initial(file: pathlib.Path) -> None:
    """Initialise a new document in the database and in the journal.

    Analyses the file name and creates an entry in each of the two database
    tables document and journal.

    Args:
        file (pathlib.Path): File.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    cfg.file_extension = file.suffix[1:]
    cfg.file_name = file.name
    cfg.stem_name = pathlib.PurePath(file).stem
    cfg.file_type = file.suffix[1:].lower()

    db.insert_dbt_document_row()

    db.insert_dbt_journal_row(
        cfg.JOURNAL_ACTION_01_001,
        inspect.stack()[0][3],
        __name__,
    )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the files found in the inbox file directory..
# -----------------------------------------------------------------------------
def process_inbox_files() -> None:
    """Process the files found in the inbox file directory.

    1. Documents of type doc, docx or txt are converted to pdf format
       and copied to the inbox_accepted directory.
    2. Documents of type pdf that do not consist only of a scanned image are
       copied unchanged to the inbox_accepted directory.
    3. Documents of type pdf consisting only of a scanned image are copied
       unchanged to the inbox_ocr directory.
    4. All other documents are copied to the inbox_rejected directory.
    5. For each document a new entry is created in the database table
       document.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    cfg.total_accepted = 0
    cfg.total_erroneous = 0
    cfg.total_new = 0
    cfg.total_rejected = 0

    # Check the inbox file directories and create the missing ones.
    check_and_create_directories()

    for file in pathlib.Path(
        cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX]
    ).iterdir():
        if file.is_file():
            if file.name == "README.md":
                utils.progress_msg(
                    "Attention: All files with the file name 'README.md' "
                    + "are ignored"
                )
                continue

            cfg.total_new += 1

            process_inbox_document_initial(file)

            if cfg.file_type == cfg.FILE_TYPE_PDF:
                prepare_pdf()
            elif cfg.file_type in (
                cfg.FILE_TYPE_CSV,
                cfg.FILE_TYPE_DOC,
                cfg.FILE_TYPE_DOCX,
                cfg.FILE_TYPE_EPUB,
                cfg.FILE_TYPE_HTM,
                cfg.FILE_TYPE_HTML,
                cfg.FILE_TYPE_JSON,
                cfg.FILE_TYPE_MD,
                cfg.FILE_TYPE_ODT,
                cfg.FILE_TYPE_RST,
                cfg.FILE_TYPE_RTF,
                cfg.FILE_TYPE_TXT,
            ):
                process_inbox_accepted(
                    db.update_document_status(
                        cfg.JOURNAL_ACTION_11_001,
                        inspect.stack()[0][3],
                        __name__,
                        cfg.STATUS_PANDOC_READY,
                    ),
                    utils.get_file_name_inbox_accepted(),
                )
            elif cfg.file_type in (
                cfg.FILE_TYPE_BMP,
                cfg.FILE_TYPE_GIF,
                cfg.FILE_TYPE_JP2,
                cfg.FILE_TYPE_JPEG,
                cfg.FILE_TYPE_JPG,
                cfg.FILE_TYPE_PMG,
                cfg.FILE_TYPE_PMN,
                cfg.FILE_TYPE_TIFF,
                cfg.FILE_TYPE_WEBP,
            ):
                process_inbox_accepted(
                    db.update_document_status(
                        cfg.JOURNAL_ACTION_11_002,
                        inspect.stack()[0][3],
                        __name__,
                        cfg.STATUS_TESSERACT_READY,
                    ),
                    utils.get_file_name_inbox_accepted(),
                )
            else:
                process_inbox_rejected(
                    db.update_document_status(
                        cfg.JOURNAL_ACTION_01_901.replace(
                            "{extension}", cfg.file_extension
                        ),
                        inspect.stack()[0][3],
                        __name__,
                        cfg.STATUS_REJECTED_FILE_EXTENSION,
                    )
                )

    utils.progress_msg(f"Number documents new:       {cfg.total_new:6d}")

    if cfg.total_new > 0:
        utils.progress_msg(f"Number documents accepted:  {cfg.total_accepted:6d}")
        utils.progress_msg(f"Number documents erroneous: {cfg.total_erroneous:6d}")
        utils.progress_msg(f"Number documents rejected:  {cfg.total_rejected:6d}")
        utils.progress_msg(
            "The new documents in the inbox file directory are checked and "
            + "prepared for further processing",
        )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Reject a new document that is faulty.
# -----------------------------------------------------------------------------
def process_inbox_rejected(
    update_document_status: Callable[[str, str, str, str], None],
) -> None:
    """Reject a new document that is faulty.

    Args:
        update_document_status (db.update_document_status): Function to update
                    the document status and create a new journal entry.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    try:
        cfg.total_erroneous += 1
        shutil.move(
            utils.get_file_name_inbox(), utils.get_file_name_inbox_rejected()
        )

        # pylint: disable=pointless-statement
        update_document_status

        cfg.total_rejected += 1
    except PermissionError as err:
        db.update_document_status(
            cfg.JOURNAL_ACTION_01_905.replace(
                "{source_file}", utils.get_file_name_inbox()
            )
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror),
            inspect.stack()[0][3],
            __name__,
            cfg.STATUS_REJECTED_FILE_PERMISSION,
        )
        remove_optional_file(utils.get_file_name_inbox_rejected())
    except shutil.Error as err:
        db.update_document_status(
            cfg.JOURNAL_ACTION_01_902.replace(
                "{source_file}", utils.get_file_name_inbox()
            )
            .replace("{target_file}", utils.get_file_name_inbox_rejected())
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror),
            inspect.stack()[0][3],
            __name__,
            cfg.STATUS_REJECTED_ERROR,
        )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Remove the given file if existing.
# -----------------------------------------------------------------------------
def remove_optional_file(file_name: str) -> None:
    """Remove the given file if existing.

    Args:
        file_name (str): Name of the file to be deleted.
    """
    if not os.path.isfile(file_name):
        return

    try:
        os.remove(file_name)
    except FileNotFoundError as err:
        db.update_document_status(
            cfg.JOURNAL_ACTION_01_906.replace("{source_file}", file_name)
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror),
            inspect.stack()[0][3],
            __name__,
            cfg.STATUS_REJECTED_ERROR,
        )
