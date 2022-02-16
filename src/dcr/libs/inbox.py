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
from typing import List

import fitz
from libs import cfg
from libs import db
from libs import utils
from sqlalchemy import Table
from sqlalchemy import select

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
FILE_TYPE_PANDOC: List[str] = [
    "csv",
    "doc",
    "docx",
    "epub",
    "htm",
    "html",
    "json",
    "md",
    "odt",
    "rst",
    "rtf",
    "txt",
]

FILE_TYPE_PDF: str = "pdf"

FILE_TYPE_TESSERACT: List[str] = [
    "bmp",
    "gif",
    "jfif",
    "jiff",
    "jpeg",
    "jpg",
    "pip",
    "pjpeg",
    "pmn",
    "png",
    "tif",
    "tiff",
    "webp",
]


# -----------------------------------------------------------------------------
# Check the inbox file directories.
# -----------------------------------------------------------------------------
def check_directories() -> None:
    """Check the inbox file directories.

    The file directory inbox_accepted must exist.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    cfg.directory_inbox = cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX]
    cfg.directory_inbox_accepted = cfg.config[
        cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    ]
    if not os.path.isdir(cfg.directory_inbox_accepted):
        utils.terminate_fatal(
            "The inbox_accepted directory with the name "
            + cfg.directory_inbox_accepted
            + " does not exist - error="
            + str(OSError),
        )
    cfg.directory_inbox_rejected = cfg.config[
        cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED
    ]

    cfg.logger.debug(cfg.LOGGER_END)


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

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image() -> None:
    """Convert scanned image pdf documents to image files.

    TBD
    """
    cfg.logger.debug(cfg.LOGGER_START)

    cfg.total_erroneous = 0
    cfg.total_ok_processed = 0
    cfg.total_status_error = 0
    cfg.total_status_ready = 0
    cfg.total_to_be_processed = 0

    # Check the inbox file directories and create the missing ones.
    check_and_create_directories()

    dbt = Table(db.DBT_DOCUMENT, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect() as conn:
        rows = conn.execute(
            select(dbt.c.file_name, dbt.c.id, dbt.c.status)
            .where(
                dbt.c.status.in_(
                    [
                        cfg.STATUS_TESSERACT_PDF_READY,
                        cfg.STATUS_TESSERACT_PDF_ERROR,
                    ]
                )
            )
            .order_by(dbt.c.id.desc())
        )

        for row in rows:
            cfg.total_to_be_processed += 1
            cfg.document_id = row.id
            cfg.file_name = row.file_name
            cfg.document_status = row.status

            if cfg.document_status == cfg.STATUS_TESSERACT_PDF_READY:
                cfg.total_status_ready += 1
            else:
                cfg.total_status_error += 1

            convert_pdf_2_image_file()

    utils.progress_msg(
        f"Number documents to be processed:  {cfg.total_to_be_processed:6d}"
    )

    if cfg.total_to_be_processed > 0:
        utils.progress_msg(
            f"Number status tesseract_pdf_ready: {cfg.total_status_ready:6d}"
        )
        utils.progress_msg(
            f"Number status tesseract_pdf_error: {cfg.total_status_error:6d}"
        )
        utils.progress_msg(
            f"Number documents converted:        {cfg.total_ok_processed:6d}"
        )
        utils.progress_msg(
            f"Number documents erroneous:        {cfg.total_erroneous:6d}"
        )
        utils.progress_msg(
            "The involved pdf documents in the file directory "
            + "'inbox_accepted' are converted to an image format "
            + "for further processing",
        )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image_file() -> None:
    """Convert scanned image pdf documents to image files.

    TBD
    """


# -----------------------------------------------------------------------------
# Create a new file directory if it does not already exist..
# -----------------------------------------------------------------------------
def create_directory(directory_type: str, directory_name: str) -> None:
    """Create a new file directory if it does not already exist.

    Args:
        directory_type (str): Directory type.
        directory_name (str): Directory name - may include a path.
    """
    cfg.logger.debug(cfg.LOGGER_START)

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

    cfg.logger.debug(cfg.LOGGER_END)


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
                {
                    db.DBC_INBOX_ACCEPTED_ABS_NAME: str(
                        pathlib.Path(cfg.directory_inbox_accepted).absolute()
                    ),
                    db.DBC_STATUS: status,
                },
                {
                    db.DBC_ACTION_CODE: action[0:7],
                    db.DBC_ACTION_TEXT: action[7:],
                    db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                    db.DBC_MODULE_NAME: __name__,
                },
            ),
            utils.get_file_name_inbox_accepted(),
        )
    except RuntimeError as err:
        action: str = cfg.JOURNAL_ACTION_01_904.replace(
            "{source_file}", utils.get_file_name_inbox()
        ).replace("{error_msg}", str(err))
        process_inbox_rejected(
            db.update_document_status(
                {
                    db.DBC_INBOX_REJECTED_ABS_NAME: str(
                        pathlib.Path(cfg.directory_inbox_rejected).absolute()
                    ),
                    db.DBC_STATUS: cfg.STATUS_REJECTED_NO_PDF_FORMAT,
                },
                {
                    db.DBC_ACTION_CODE: action[0:7],
                    db.DBC_ACTION_TEXT: action[7:],
                    db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                    db.DBC_MODULE_NAME: __name__,
                },
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

        cfg.total_ok_processed += 1
    except PermissionError as err:
        # pylint: disable=expression-not-assigned
        action: str = (
            cfg.JOURNAL_ACTION_01_905.replace(
                "{source_file}", utils.get_file_name_inbox()
            )
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        db.update_document_status(
            {
                db.DBC_INBOX_REJECTED_ABS_NAME: str(
                    pathlib.Path(cfg.directory_inbox_rejected).absolute()
                ),
                db.DBC_STATUS: cfg.STATUS_REJECTED_FILE_PERMISSION,
            },
            {
                db.DBC_ACTION_CODE: action[0:7],
                db.DBC_ACTION_TEXT: action[7:],
                db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                db.DBC_MODULE_NAME: __name__,
            },
        ),
        remove_optional_file(target_file_name)
    except shutil.Error as err:
        cfg.total_erroneous += 1
        # pylint: disable=expression-not-assigned
        action: str = (
            cfg.JOURNAL_ACTION_01_902.replace(
                "{source_file}", utils.get_file_name_inbox()
            )
            .replace("{target_file}", target_file_name)
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        db.update_document_status(
            {
                db.DBC_INBOX_REJECTED_ABS_NAME: str(
                    pathlib.Path(cfg.directory_inbox_rejected).absolute()
                ),
                db.DBC_STATUS: cfg.STATUS_REJECTED_ERROR,
            },
            {
                db.DBC_ACTION_CODE: action[0:7],
                db.DBC_ACTION_TEXT: action[7:],
                db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                db.DBC_MODULE_NAME: __name__,
            },
        ),

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
    cfg.sha256 = utils.get_sha256(utils.get_file_name_inbox())

    cfg.document_id = db.insert_dbt_row(
        db.DBT_DOCUMENT,
        {
            db.DBC_FILE_NAME: cfg.file_name,
            db.DBC_FILE_TYPE: cfg.file_type,
            db.DBC_INBOX_ABS_NAME: str(
                pathlib.Path(cfg.directory_inbox).absolute()
            ),
            db.DBC_RUN_ID: cfg.run_run_id,
            db.DBC_SHA256: cfg.sha256,
            db.DBC_STATUS: cfg.STATUS_INBOX,
            db.DBC_STEM_NAME: cfg.stem_name,
        },
    )

    db.insert_dbt_row(
        db.DBT_JOURNAL,
        {
            db.DBC_ACTION_CODE: cfg.JOURNAL_ACTION_01_001[0:7],
            db.DBC_ACTION_TEXT: cfg.JOURNAL_ACTION_01_001[7:],
            db.DBC_DOCUMENT_ID: cfg.document_id,
            db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
            db.DBC_MODULE_NAME: __name__,
            db.DBC_RUN_ID: cfg.run_id,
        },
    )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the inbox directory (step: p_i).
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
    """
    cfg.logger.debug(cfg.LOGGER_START)

    cfg.total_erroneous = 0
    cfg.total_ok_processed = 0
    cfg.total_rejected = 0
    cfg.total_to_be_processed = 0

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

            cfg.total_to_be_processed += 1

            process_inbox_document_initial(file)

            #

            if cfg.file_type == FILE_TYPE_PDF:
                prepare_pdf()
            elif cfg.file_type in FILE_TYPE_PANDOC:
                process_inbox_accepted(
                    db.update_document_status(
                        {
                            db.DBC_INBOX_ACCEPTED_ABS_NAME: str(
                                pathlib.Path(
                                    cfg.directory_inbox_accepted
                                ).absolute()
                            ),
                            db.DBC_STATUS: cfg.STATUS_PANDOC_READY,
                        },
                        {
                            db.DBC_ACTION_CODE: cfg.JOURNAL_ACTION_11_001[0:7],
                            db.DBC_ACTION_TEXT: cfg.JOURNAL_ACTION_11_001[7:],
                            db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                            db.DBC_MODULE_NAME: __name__,
                        },
                    ),
                    utils.get_file_name_inbox_accepted(),
                )
            elif cfg.file_type in FILE_TYPE_TESSERACT:
                process_inbox_accepted(
                    db.update_document_status(
                        {
                            db.DBC_INBOX_ACCEPTED_ABS_NAME: str(
                                pathlib.Path(
                                    cfg.directory_inbox_accepted
                                ).absolute()
                            ),
                            db.DBC_STATUS: cfg.STATUS_TESSERACT_READY,
                        },
                        {
                            db.DBC_ACTION_CODE: cfg.JOURNAL_ACTION_11_002[0:7],
                            db.DBC_ACTION_TEXT: cfg.JOURNAL_ACTION_11_002[7:],
                            db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                            db.DBC_MODULE_NAME: __name__,
                        },
                    ),
                    utils.get_file_name_inbox_accepted(),
                )
            else:
                action: str = cfg.JOURNAL_ACTION_01_901.replace(
                    "{extension}", cfg.file_extension
                )
                process_inbox_rejected(
                    db.update_document_status(
                        {
                            db.DBC_INBOX_REJECTED_ABS_NAME: str(
                                pathlib.Path(
                                    cfg.directory_inbox_rejected
                                ).absolute()
                            ),
                            db.DBC_STATUS: cfg.STATUS_REJECTED_FILE_EXTENSION,
                        },
                        {
                            db.DBC_ACTION_CODE: action[0:7],
                            db.DBC_ACTION_TEXT: action[7:],
                            db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                            db.DBC_MODULE_NAME: __name__,
                        },
                    ),
                )

    utils.progress_msg(
        f"Number documents to be processed:  {cfg.total_to_be_processed:6d}"
    )

    if cfg.total_to_be_processed > 0:
        utils.progress_msg(
            f"Number documents accepted:         {cfg.total_ok_processed:6d}"
        )
        utils.progress_msg(
            f"Number documents erroneous:        {cfg.total_erroneous:6d}"
        )
        utils.progress_msg(
            f"Number documents rejected:         {cfg.total_rejected:6d}"
        )
        utils.progress_msg(
            "The new documents in the file directory 'inbox' are checked and "
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
        # pylint: disable=expression-not-assigned
        action: str = (
            cfg.JOURNAL_ACTION_01_905.replace(
                "{source_file}", utils.get_file_name_inbox()
            )
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        db.update_document_status(
            {
                db.DBC_INBOX_REJECTED_ABS_NAME: str(
                    pathlib.Path(cfg.directory_inbox_rejected).absolute()
                ),
                db.DBC_STATUS: cfg.STATUS_REJECTED_FILE_PERMISSION,
            },
            {
                db.DBC_ACTION_CODE: action[0:7],
                db.DBC_ACTION_TEXT: action[7:],
                db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                db.DBC_MODULE_NAME: __name__,
            },
        ),
        remove_optional_file(utils.get_file_name_inbox_rejected())
    except shutil.Error as err:
        # pylint: disable=expression-not-assigned
        action: str = (
            cfg.JOURNAL_ACTION_01_902.replace(
                "{source_file}", utils.get_file_name_inbox()
            )
            .replace("{target_file}", utils.get_file_name_inbox_rejected())
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        db.update_document_status(
            {
                db.DBC_INBOX_REJECTED_ABS_NAME: str(
                    pathlib.Path(cfg.directory_inbox_rejected).absolute()
                ),
                db.DBC_STATUS: cfg.STATUS_REJECTED_ERROR,
            },
            {
                db.DBC_ACTION_CODE: action[0:7],
                db.DBC_ACTION_TEXT: action[7:],
                db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                db.DBC_MODULE_NAME: __name__,
            },
        ),

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Remove the given file if existing.
# -----------------------------------------------------------------------------
def remove_optional_file(file_name: str) -> None:
    """Remove the given file if existing.

    Args:
        file_name (str): Name of the file to be deleted.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    if not os.path.isfile(file_name):
        return

    try:
        os.remove(file_name)
    except FileNotFoundError as err:
        # pylint: disable=expression-not-assigned
        action: str = (
            cfg.JOURNAL_ACTION_01_906.replace("{source_file}", file_name)
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        db.update_document_status(
            {
                db.DBC_INBOX_REJECTED_ABS_NAME: str(
                    pathlib.Path(cfg.directory_inbox_rejected).absolute()
                ),
                db.DBC_STATUS: cfg.STATUS_REJECTED_ERROR,
            },
            {
                db.DBC_ACTION_CODE: action[0:7],
                db.DBC_ACTION_TEXT: action[7:],
                db.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                db.DBC_MODULE_NAME: __name__,
            },
        ),

    cfg.logger.debug(cfg.LOGGER_END)
