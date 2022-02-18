"""Module inbox: Check and distribute incoming documents.

New documents are made available in the file directory inbox. These are
then checked and moved to the accepted or rejected file directories
depending on the result of the check. Depending on the file format, the
accepted documents are then converted into the pdf file format either
with the help of Pandoc or with the help of Tesseract OCR.
"""
import inspect
import os
import pathlib
import shutil
from typing import Callable
from typing import List

import fitz
import libs.cfg
import libs.db.orm
import libs.utils
import pdf2image
from pdf2image.exceptions import PDFPopplerTimeoutError
from sqlalchemy import Table
from sqlalchemy import select

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
FILE_TYPE_JPG: str = "jpg"
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
FILE_TYPE_PNG: str = "png"
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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.directory_inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    libs.cfg.directory_inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    if not os.path.isdir(libs.cfg.directory_inbox_accepted):
        libs.utils.terminate_fatal(
            "The inbox_accepted directory with the name "
            + libs.cfg.directory_inbox_accepted
            + " does not exist - error="
            + str(OSError),
        )
    libs.cfg.directory_inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Check the inbox file directories and create the missing ones.
# -----------------------------------------------------------------------------
def check_and_create_directories() -> None:
    """Check the inbox file directories and create the missing ones.

    The file directory inbox must exist. The two file directories
    inbox_accepted and inbox_rejected are created if they do not already
    exist.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.directory_inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    if not os.path.isdir(libs.cfg.directory_inbox):
        libs.utils.terminate_fatal(
            "The inbox directory with the name "
            + libs.cfg.directory_inbox
            + " does not exist - error="
            + str(OSError),
        )

    libs.cfg.directory_inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    create_directory("the accepted documents", libs.cfg.directory_inbox_accepted)

    libs.cfg.directory_inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]
    create_directory("the rejected documents", libs.cfg.directory_inbox_rejected)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image() -> None:
    """Convert scanned image pdf documents to image files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.total_erroneous = 0
    libs.cfg.total_generated = 0
    libs.cfg.total_ok_processed = 0
    libs.cfg.total_status_error = 0
    libs.cfg.total_status_ready = 0
    libs.cfg.total_to_be_processed = 0

    if libs.cfg.config[libs.cfg.DCR_CFG_PDF2IMAGE_TYPE] == libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_PNG:
        libs.cfg.document_child_file_type = FILE_TYPE_PNG
    else:
        libs.cfg.document_child_file_type = FILE_TYPE_JPG

    # Check the inbox file directories.
    check_directories()

    dbt = Table(libs.db.orm.DBT_DOCUMENT, libs.cfg.metadata, autoload_with=libs.cfg.engine)

    with libs.cfg.engine.connect() as conn:
        rows = conn.execute(
            select(
                dbt.c.file_name,
                dbt.c.file_type,
                dbt.c.id,
                dbt.c.inbox_accepted_abs_name,
                dbt.c.status,
                dbt.c.stem_name,
            )
            .where(
                dbt.c.status.in_(
                    [
                        libs.cfg.STATUS_TESSERACT_PDF_READY,
                        libs.cfg.STATUS_TESSERACT_PDF_ERROR,
                    ]
                )
            )
            .order_by(dbt.c.id.desc())
        )

        for row in rows:
            libs.cfg.total_to_be_processed += 1
            libs.cfg.document_file_name_accepted_abs = os.path.join(
                row.inbox_accepted_abs_name,
                row.file_name,
            )
            libs.cfg.document_id = row.id
            libs.cfg.document_status = row.status
            libs.cfg.document_inbox_accepted_abs_name = row.inbox_accepted_abs_name
            libs.cfg.document_stem_name = row.stem_name

            libs.db.orm.update_document_status(
                {
                    libs.db.orm.DBC_STATUS: libs.cfg.STATUS_START_PDF2IMAGE,
                },
                {
                    libs.db.orm.DBC_ACTION_CODE: libs.cfg.JOURNAL_ACTION_21_001[0:7],
                    libs.db.orm.DBC_ACTION_TEXT: libs.cfg.JOURNAL_ACTION_21_001[7:],
                    libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                    libs.db.orm.DBC_MODULE_NAME: __name__,
                },
            )

            if libs.cfg.document_status == libs.cfg.STATUS_TESSERACT_PDF_READY:
                libs.cfg.total_status_ready += 1
            else:
                libs.cfg.total_status_error += 1

            convert_pdf_2_image_file()

        conn.close()

    libs.utils.progress_msg(
        f"Number documents to be processed:  {libs.cfg.total_to_be_processed:6d}"
    )

    if libs.cfg.total_to_be_processed > 0:
        libs.utils.progress_msg(
            f"Number status tesseract_pdf_ready: {libs.cfg.total_status_ready:6d}"
        )
        libs.utils.progress_msg(
            f"Number status tesseract_pdf_error: {libs.cfg.total_status_error:6d}"
        )
        libs.utils.progress_msg(
            f"Number documents converted:        {libs.cfg.total_ok_processed:6d}"
        )
        libs.utils.progress_msg(f"Number documents generated:        {libs.cfg.total_generated:6d}")
        libs.utils.progress_msg(f"Number documents erroneous:        {libs.cfg.total_erroneous:6d}")
        libs.utils.progress_msg(
            "The involved 'pdf' documents in the file directory "
            + "'inbox_accepted' are converted to an image format "
            + "for further processing",
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image_file() -> None:
    """Convert scanned image pdf documents to image files."""
    try:
        # Convert the 'pdf' document
        images = pdf2image.convert_from_path(libs.cfg.document_file_name_accepted_abs)

        # Store the image pages
        libs.cfg.document_child_no = 0
        for img in images:
            try:
                libs.cfg.document_child_no = +1

                initialise_document_child()

                libs.cfg.document_child_file_name_abs = os.path.join(
                    libs.cfg.document_inbox_accepted_abs_name,
                    libs.cfg.document_child_file_name,
                )

                img.save(
                    libs.cfg.document_child_file_name_abs,
                    libs.cfg.config[libs.cfg.DCR_CFG_PDF2IMAGE_TYPE],
                )

                if not libs.cfg.is_ignore_duplicates:
                    libs.cfg.document_sha256 = libs.utils.get_sha256(
                        libs.cfg.document_child_file_name_abs
                    )

                    libs.db.orm.update_dbt_id(
                        libs.db.orm.DBT_DOCUMENT,
                        libs.cfg.document_child_id,
                        {
                            libs.db.orm.DBC_SHA256: libs.cfg.document_sha256,
                        },
                    )

                libs.cfg.total_generated += 1
            except OSError as err:
                libs.cfg.total_erroneous += 1
                action: str = (
                    libs.cfg.JOURNAL_ACTION_21_902.replace(
                        "{child_no}", str(libs.cfg.document_child_no)
                    )
                    .replace("{file_name}", libs.cfg.document_child_file_name)
                    .replace("{error_code}", str(err.errno))
                    .replace("{error_msg}", err.strerror)
                )
                libs.db.orm.update_document_status(
                    {
                        libs.db.orm.DBC_STATUS: libs.cfg.STATUS_TESSERACT_PDF_ERROR,
                    },
                    {
                        libs.db.orm.DBC_ACTION_CODE: action[0:7],
                        libs.db.orm.DBC_ACTION_TEXT: action[7:],
                        libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                        libs.db.orm.DBC_MODULE_NAME: __name__,
                    },
                )

            # Document successfully converted to image format
            libs.cfg.total_ok_processed += 1

            action: str = libs.cfg.JOURNAL_ACTION_21_002.replace(
                "{child_no}", str(libs.cfg.document_child_no)
            )
            libs.db.orm.update_document_status(
                {
                    libs.db.orm.DBC_STATUS: libs.cfg.STATUS_TESSERACT_PDF_END,
                },
                {
                    libs.db.orm.DBC_ACTION_CODE: action[0:7],
                    libs.db.orm.DBC_ACTION_TEXT: action[7:],
                    libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                    libs.db.orm.DBC_MODULE_NAME: __name__,
                },
            )
    except PDFPopplerTimeoutError as err:
        libs.cfg.total_erroneous += 1
        action: str = libs.cfg.JOURNAL_ACTION_21_901.replace(
            "{file_name}", libs.cfg.document_file_name_accepted_abs
        ).replace("{error_msg}", str(err))
        libs.db.orm.update_document_status(
            {
                libs.db.orm.DBC_STATUS: libs.cfg.STATUS_TESSERACT_PDF_ERROR,
            },
            {
                libs.db.orm.DBC_ACTION_CODE: action[0:7],
                libs.db.orm.DBC_ACTION_TEXT: action[7:],
                libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                libs.db.orm.DBC_MODULE_NAME: __name__,
            },
        )


# -----------------------------------------------------------------------------
# Create a new file directory if it does not already exist..
# -----------------------------------------------------------------------------
def create_directory(directory_type: str, directory_name: str) -> None:
    """Create a new file directory if it does not already exist.

    Args:
        directory_type (str): Directory type.
        directory_name (str): Directory name - may include a path.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if not os.path.isdir(directory_name):
        try:
            os.mkdir(directory_name)
            libs.utils.progress_msg(
                "The file directory for "
                + directory_type
                + " was "
                + "newly created under the name "
                + directory_name,
            )
        except OSError as err:
            libs.utils.terminate_fatal(
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

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise a new child document in the database and in the journal.
# -----------------------------------------------------------------------------
def initialise_document_child() -> None:
    """Initialise a new child document in the database and in the journal.

    Create an entry in each of the two database tables document and
    journal.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.document_child_id = libs.db.orm.insert_dbt_row(
        libs.db.orm.DBT_DOCUMENT,
        {
            libs.db.orm.DBC_DOCUMENT_ID_PARENT: libs.cfg.document_id,
            libs.db.orm.DBC_FILE_NAME: libs.cfg.INFORMATION_NOT_YET_AVAILABLE,
            libs.db.orm.DBC_FILE_TYPE: libs.cfg.document_child_file_type,
            libs.db.orm.DBC_INBOX_ACCEPTED_ABS_NAME: libs.cfg.document_inbox_accepted_abs_name,
            libs.db.orm.DBC_RUN_ID: libs.cfg.run_run_id,
            libs.db.orm.DBC_STATUS: libs.cfg.STATUS_TESSERACT_READY,
            libs.db.orm.DBC_STEM_NAME: libs.cfg.INFORMATION_NOT_YET_AVAILABLE,
        },
    )

    libs.cfg.document_child_stem_name = (
        libs.cfg.document_stem_name
        + "_"
        + str(libs.cfg.document_child_id)
        + "_"
        + str(libs.cfg.document_child_no)
    )
    libs.cfg.document_child_file_name = (
        libs.cfg.document_child_stem_name + "." + libs.cfg.document_child_file_type
    )

    libs.db.orm.update_dbt_id(
        libs.db.orm.DBT_DOCUMENT,
        libs.cfg.document_child_id,
        {
            libs.db.orm.DBC_FILE_NAME: libs.cfg.document_child_file_name,
            libs.db.orm.DBC_STEM_NAME: libs.cfg.document_child_stem_name,
        },
    )

    libs.db.orm.insert_dbt_row(
        libs.db.orm.DBT_JOURNAL,
        {
            libs.db.orm.DBC_ACTION_CODE: libs.cfg.JOURNAL_ACTION_21_003[0:7],
            libs.db.orm.DBC_ACTION_TEXT: libs.cfg.JOURNAL_ACTION_21_003[7:],
            libs.db.orm.DBC_DOCUMENT_ID: libs.cfg.document_child_id,
            libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
            libs.db.orm.DBC_MODULE_NAME: __name__,
            libs.db.orm.DBC_RUN_ID: libs.cfg.run_run_id,
        },
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise a new document in the database and in the journal.
# -----------------------------------------------------------------------------
def initialise_document_inbox(file: pathlib.Path) -> None:
    """Initialise a new document in the database and in the journal.

    Analyses the file name and creates an entry in each of the two database
    tables document and journal.

    Args:
        file (pathlib.Path): File.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.document_file_extension = file.suffix[1:]
    libs.cfg.document_file_name_orig = file.name
    libs.cfg.document_file_name_abs_orig = os.path.join(
        libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX],
        libs.cfg.document_file_name_orig,
    )
    libs.cfg.document_stem_name_orig = pathlib.PurePath(file).stem
    libs.cfg.document_file_type = file.suffix[1:].lower()

    if not libs.cfg.is_ignore_duplicates:
        libs.cfg.document_sha256 = libs.utils.get_sha256(libs.cfg.document_file_name_abs_orig)
    else:
        libs.cfg.document_sha256 = None

    libs.cfg.document_id = libs.db.orm.insert_dbt_row(
        libs.db.orm.DBT_DOCUMENT,
        {
            libs.db.orm.DBC_FILE_NAME: libs.cfg.INFORMATION_NOT_YET_AVAILABLE,
            libs.db.orm.DBC_FILE_TYPE: libs.cfg.document_file_type,
            libs.db.orm.DBC_INBOX_ABS_NAME: str(pathlib.Path(libs.cfg.directory_inbox).absolute()),
            libs.db.orm.DBC_RUN_ID: libs.cfg.run_run_id,
            libs.db.orm.DBC_SHA256: libs.cfg.document_sha256,
            libs.db.orm.DBC_STATUS: libs.cfg.STATUS_START_INBOX,
            libs.db.orm.DBC_STEM_NAME: libs.cfg.INFORMATION_NOT_YET_AVAILABLE,
        },
    )

    libs.cfg.document_stem_name = libs.cfg.document_stem_name_orig + "_" + str(libs.cfg.document_id)
    libs.cfg.document_file_name = libs.cfg.document_stem_name + "." + libs.cfg.document_file_type

    libs.db.orm.update_dbt_id(
        libs.db.orm.DBT_DOCUMENT,
        libs.cfg.document_id,
        {
            libs.db.orm.DBC_FILE_NAME: libs.cfg.document_file_name,
            libs.db.orm.DBC_STEM_NAME: libs.cfg.document_stem_name,
        },
    )

    libs.cfg.document_file_name_accepted_abs = os.path.join(
        libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED],
        libs.cfg.document_file_name,
    )

    libs.cfg.document_file_name_rejected_abs = os.path.join(
        libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED],
        libs.cfg.document_file_name,
    )

    libs.db.orm.insert_dbt_row(
        libs.db.orm.DBT_JOURNAL,
        {
            libs.db.orm.DBC_ACTION_CODE: libs.cfg.JOURNAL_ACTION_01_001[0:7],
            libs.db.orm.DBC_ACTION_TEXT: libs.cfg.JOURNAL_ACTION_01_001[7:],
            libs.db.orm.DBC_DOCUMENT_ID: libs.cfg.document_id,
            libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
            libs.db.orm.DBC_MODULE_NAME: __name__,
            libs.db.orm.DBC_RUN_ID: libs.cfg.run_run_id,
        },
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare a new pdf document for further processing..
# -----------------------------------------------------------------------------
def prepare_pdf() -> None:
    """Prepare a new pdf document for further processing."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    try:
        extracted_text = "".join(
            [page.get_text() for page in fitz.open(libs.cfg.document_file_name_abs_orig)]
        )

        if bool(extracted_text):
            action: str = libs.cfg.JOURNAL_ACTION_11_003
            status: str = libs.cfg.STATUS_PARSER_READY
        else:
            action: str = libs.cfg.JOURNAL_ACTION_11_005
            status: str = libs.cfg.STATUS_TESSERACT_PDF_READY

        process_inbox_accepted(
            libs.db.orm.update_document_status(
                {
                    libs.db.orm.DBC_INBOX_ACCEPTED_ABS_NAME: str(
                        pathlib.Path(libs.cfg.directory_inbox_accepted).absolute()
                    ),
                    libs.db.orm.DBC_STATUS: status,
                },
                {
                    libs.db.orm.DBC_ACTION_CODE: action[0:7],
                    libs.db.orm.DBC_ACTION_TEXT: action[7:],
                    libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                    libs.db.orm.DBC_MODULE_NAME: __name__,
                },
            ),
            libs.cfg.document_file_name_accepted_abs,
        )
    except RuntimeError as err:
        action: str = libs.cfg.JOURNAL_ACTION_01_904.replace(
            "{source_file}", libs.cfg.document_file_name_abs_orig
        ).replace("{error_msg}", str(err))
        process_inbox_rejected(
            libs.db.orm.update_document_status(
                {
                    libs.db.orm.DBC_INBOX_REJECTED_ABS_NAME: str(
                        pathlib.Path(libs.cfg.directory_inbox_rejected).absolute()
                    ),
                    libs.db.orm.DBC_STATUS: libs.cfg.STATUS_REJECTED_NO_PDF_FORMAT,
                },
                {
                    libs.db.orm.DBC_ACTION_CODE: action[0:7],
                    libs.db.orm.DBC_ACTION_TEXT: action[7:],
                    libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                    libs.db.orm.DBC_MODULE_NAME: __name__,
                },
            ),
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Accept a new document.
# -----------------------------------------------------------------------------
def process_inbox_accepted(
    update_document_status: Callable[[str, str, str, str], None],
    target_file_name: str,
) -> None:
    """Accept a new document.

    Args:
        update_document_status (Callable[[str, str, str, str], None]):
                                Function to update the document status
                                and create a new journal entry.
        target_file_name (str): File name in the directory inbox_accepted.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    try:
        shutil.move(libs.cfg.document_file_name_abs_orig, target_file_name)

        # pylint: disable=pointless-statement
        update_document_status

        libs.cfg.total_ok_processed += 1
    except PermissionError as err:
        # pylint: disable=expression-not-assigned
        action: str = (
            libs.cfg.JOURNAL_ACTION_01_905.replace(
                "{source_file}", libs.cfg.document_file_name_abs_orig
            )
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        libs.db.orm.update_document_status(
            {
                libs.db.orm.DBC_INBOX_REJECTED_ABS_NAME: str(
                    pathlib.Path(libs.cfg.directory_inbox_rejected).absolute()
                ),
                libs.db.orm.DBC_STATUS: libs.cfg.STATUS_REJECTED_FILE_PERMISSION,
            },
            {
                libs.db.orm.DBC_ACTION_CODE: action[0:7],
                libs.db.orm.DBC_ACTION_TEXT: action[7:],
                libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                libs.db.orm.DBC_MODULE_NAME: __name__,
            },
        ),
        remove_optional_file(target_file_name)
    except shutil.Error as err:
        libs.cfg.total_erroneous += 1
        # pylint: disable=expression-not-assigned
        action: str = (
            libs.cfg.JOURNAL_ACTION_01_902.replace(
                "{source_file}", libs.cfg.document_file_name_abs_orig
            )
            .replace("{target_file}", target_file_name)
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        libs.db.orm.update_document_status(
            {
                libs.db.orm.DBC_INBOX_REJECTED_ABS_NAME: str(
                    pathlib.Path(libs.cfg.directory_inbox_rejected).absolute()
                ),
                libs.db.orm.DBC_STATUS: libs.cfg.STATUS_REJECTED_ERROR,
            },
            {
                libs.db.orm.DBC_ACTION_CODE: action[0:7],
                libs.db.orm.DBC_ACTION_TEXT: action[7:],
                libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                libs.db.orm.DBC_MODULE_NAME: __name__,
            },
        ),

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.total_erroneous = 0
    libs.cfg.total_ok_processed = 0
    libs.cfg.total_rejected = 0
    libs.cfg.total_to_be_processed = 0

    # Check the inbox file directories and create the missing ones.
    check_and_create_directories()

    for file in pathlib.Path(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]).iterdir():
        if file.is_file():
            if file.name == "README.md":
                libs.utils.progress_msg(
                    "Attention: All files with the file name 'README.md' " + "are ignored"
                )
                continue

            libs.cfg.total_to_be_processed += 1

            initialise_document_inbox(file)

            if not libs.cfg.is_ignore_duplicates:
                file_name = libs.db.orm.select_document_file_name_sha256(
                    libs.cfg.document_id, libs.cfg.document_sha256
                )
            else:
                file_name = None

            if file_name is not None:
                action: str = libs.cfg.JOURNAL_ACTION_21_901.replace("{file_name}", file_name)
                process_inbox_rejected(
                    libs.db.orm.update_document_status(
                        {
                            libs.db.orm.DBC_INBOX_REJECTED_ABS_NAME: str(
                                pathlib.Path(libs.cfg.directory_inbox_rejected).absolute()
                            ),
                            libs.db.orm.DBC_STATUS: libs.cfg.STATUS_REJECTED_FILE_DUPL,
                        },
                        {
                            libs.db.orm.DBC_ACTION_CODE: action[0:7],
                            libs.db.orm.DBC_ACTION_TEXT: action[7:],
                            libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                            libs.db.orm.DBC_MODULE_NAME: __name__,
                        },
                    ),
                )
            elif libs.cfg.document_file_type == FILE_TYPE_PDF:
                prepare_pdf()
            elif libs.cfg.document_file_type in FILE_TYPE_PANDOC:
                process_inbox_accepted(
                    libs.db.orm.update_document_status(
                        {
                            libs.db.orm.DBC_INBOX_ACCEPTED_ABS_NAME: str(
                                pathlib.Path(libs.cfg.directory_inbox_accepted).absolute()
                            ),
                            libs.db.orm.DBC_STATUS: libs.cfg.STATUS_PANDOC_READY,
                        },
                        {
                            libs.db.orm.DBC_ACTION_CODE: libs.cfg.JOURNAL_ACTION_11_001[0:7],
                            libs.db.orm.DBC_ACTION_TEXT: libs.cfg.JOURNAL_ACTION_11_001[7:],
                            libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                            libs.db.orm.DBC_MODULE_NAME: __name__,
                        },
                    ),
                    libs.cfg.document_file_name_accepted_abs,
                )
            elif libs.cfg.document_file_type in FILE_TYPE_TESSERACT:
                process_inbox_accepted(
                    libs.db.orm.update_document_status(
                        {
                            libs.db.orm.DBC_INBOX_ACCEPTED_ABS_NAME: str(
                                pathlib.Path(libs.cfg.directory_inbox_accepted).absolute()
                            ),
                            libs.db.orm.DBC_STATUS: libs.cfg.STATUS_TESSERACT_READY,
                        },
                        {
                            libs.db.orm.DBC_ACTION_CODE: libs.cfg.JOURNAL_ACTION_11_002[0:7],
                            libs.db.orm.DBC_ACTION_TEXT: libs.cfg.JOURNAL_ACTION_11_002[7:],
                            libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                            libs.db.orm.DBC_MODULE_NAME: __name__,
                        },
                    ),
                    libs.cfg.document_file_name_accepted_abs,
                )
            else:
                action: str = libs.cfg.JOURNAL_ACTION_01_901.replace(
                    "{extension}", libs.cfg.document_file_extension
                )
                process_inbox_rejected(
                    libs.db.orm.update_document_status(
                        {
                            libs.db.orm.DBC_INBOX_REJECTED_ABS_NAME: str(
                                pathlib.Path(libs.cfg.directory_inbox_rejected).absolute()
                            ),
                            libs.db.orm.DBC_STATUS: libs.cfg.STATUS_REJECTED_FILE_EXT,
                        },
                        {
                            libs.db.orm.DBC_ACTION_CODE: action[0:7],
                            libs.db.orm.DBC_ACTION_TEXT: action[7:],
                            libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                            libs.db.orm.DBC_MODULE_NAME: __name__,
                        },
                    ),
                )

    libs.utils.progress_msg(
        f"Number documents to be processed:  {libs.cfg.total_to_be_processed:6d}"
    )

    if libs.cfg.total_to_be_processed > 0:
        libs.utils.progress_msg(
            f"Number documents accepted:         {libs.cfg.total_ok_processed:6d}"
        )
        libs.utils.progress_msg(f"Number documents erroneous:        {libs.cfg.total_erroneous:6d}")
        libs.utils.progress_msg(f"Number documents rejected:         {libs.cfg.total_rejected:6d}")
        libs.utils.progress_msg(
            "The new documents in the file directory 'inbox' are checked and "
            + "prepared for further processing",
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Reject a new document that is faulty.
# -----------------------------------------------------------------------------
def process_inbox_rejected(
    update_document_status: Callable[[str, str, str, str], None],
) -> None:
    """Reject a new document that is faulty.

    Args:
        update_document_status (Callable[[str, str, str, str], None]):
                      Function to update the document status and
                      create a new journal entry.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    try:
        libs.cfg.total_erroneous += 1
        shutil.move(libs.cfg.document_file_name_abs_orig, libs.cfg.document_file_name_rejected_abs)

        # pylint: disable=pointless-statement
        update_document_status

        libs.cfg.total_rejected += 1
    except PermissionError as err:
        # pylint: disable=expression-not-assigned
        action: str = (
            libs.cfg.JOURNAL_ACTION_01_905.replace(
                "{source_file}", libs.cfg.document_file_name_abs_orig
            )
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        libs.db.orm.update_document_status(
            {
                libs.db.orm.DBC_INBOX_REJECTED_ABS_NAME: str(
                    pathlib.Path(libs.cfg.directory_inbox_rejected).absolute()
                ),
                libs.db.orm.DBC_STATUS: libs.cfg.STATUS_REJECTED_FILE_PERMISSION,
            },
            {
                libs.db.orm.DBC_ACTION_CODE: action[0:7],
                libs.db.orm.DBC_ACTION_TEXT: action[7:],
                libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                libs.db.orm.DBC_MODULE_NAME: __name__,
            },
        ),
        remove_optional_file(libs.cfg.document_file_name_rejected_abs)
    except shutil.Error as err:
        # pylint: disable=expression-not-assigned
        action: str = (
            libs.cfg.JOURNAL_ACTION_01_902.replace(
                "{source_file}", libs.cfg.document_file_name_abs_orig
            )
            .replace("{target_file}", libs.cfg.document_file_name_rejected_abs)
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        libs.db.orm.update_document_status(
            {
                libs.db.orm.DBC_INBOX_REJECTED_ABS_NAME: str(
                    pathlib.Path(libs.cfg.directory_inbox_rejected).absolute()
                ),
                libs.db.orm.DBC_STATUS: libs.cfg.STATUS_REJECTED_ERROR,
            },
            {
                libs.db.orm.DBC_ACTION_CODE: action[0:7],
                libs.db.orm.DBC_ACTION_TEXT: action[7:],
                libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                libs.db.orm.DBC_MODULE_NAME: __name__,
            },
        ),

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Remove the given file if existing.
# -----------------------------------------------------------------------------
def remove_optional_file(file_name: str) -> None:
    """Remove the given file if existing.

    Args:
        file_name (str): Name of the file to be deleted.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if not os.path.isfile(file_name):
        return

    try:
        os.remove(file_name)
    except FileNotFoundError as err:
        # pylint: disable=expression-not-assigned
        action: str = (
            libs.cfg.JOURNAL_ACTION_01_906.replace("{source_file}", file_name)
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        libs.db.orm.update_document_status(
            {
                libs.db.orm.DBC_INBOX_REJECTED_ABS_NAME: str(
                    pathlib.Path(libs.cfg.directory_inbox_rejected).absolute()
                ),
                libs.db.orm.DBC_STATUS: libs.cfg.STATUS_REJECTED_ERROR,
            },
            {
                libs.db.orm.DBC_ACTION_CODE: action[0:7],
                libs.db.orm.DBC_ACTION_TEXT: action[7:],
                libs.db.orm.DBC_FUNCTION_NAME: inspect.stack()[0][3],
                libs.db.orm.DBC_MODULE_NAME: __name__,
            },
        ),

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
