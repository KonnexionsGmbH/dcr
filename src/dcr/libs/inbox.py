"""Check and distribute incoming documents.

New documents are made available in the file directory inbox. These are
then checked and moved to the accepted or rejected file directories
depending on the result of the check. Depending on the file format, the
accepted documents are then converted into the pdf file format either
with the help of Pandoc or with the help of Tesseract OCR.

Returns:
    [type]: None.
"""
import inspect
import os
import pathlib
import shutil

import fitz
import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.utils
import pdf2image
from pdf2image.exceptions import PDFPopplerTimeoutError
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import and_


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
        libs.cfg.document_child_file_type = libs.db.cfg.DOCUMENT_FILE_TYPE_PNG
    else:
        libs.cfg.document_child_file_type = libs.db.cfg.DOCUMENT_FILE_TYPE_JPG

    # Check the inbox file directories.
    check_directories()

    dbt = Table(libs.db.cfg.DBT_DOCUMENT, libs.db.cfg.metadata, autoload_with=libs.db.cfg.engine)

    with libs.db.cfg.engine.connect() as conn:
        rows = conn.execute(
            select(
                dbt.c.id,
                dbt.c.directory_name,
                dbt.c.document_id_base,
                dbt.c.file_name,
                dbt.c.file_type,
                dbt.c.status,
                dbt.c.stem_name,
            )
            .where(
                and_(
                    dbt.c.next_step == libs.db.cfg.DOCUMENT_NEXT_STEP_PDF2IMAGE,
                    dbt.c.status.in_(
                        [
                            libs.db.cfg.DOCUMENT_STATUS_ERROR,
                            libs.db.cfg.DOCUMENT_STATUS_START,
                        ]
                    ),
                )
            )
            .order_by(dbt.c.id.desc())
        )

        for row in rows:
            libs.cfg.total_to_be_processed += 1

            libs.cfg.document_directory_name = row.directory_name
            libs.cfg.document_file_name = row.file_name
            libs.cfg.document_file_type = row.file_type
            libs.cfg.document_id = row.id
            libs.cfg.document_id_base = row.document_id_base
            libs.cfg.document_id_parent = row.document_id_parent
            libs.cfg.document_status = row.status
            libs.cfg.document_stem_name = row.stem_name

            libs.db.orm.update_document_status(
                {
                    libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_START,
                },
                libs.db.orm.insert_journal(
                    __name__,
                    inspect.stack()[0][3],
                    libs.db.cfg.JOURNAL_ACTION_21_001,
                ),
            )

            if libs.cfg.document_status == libs.db.cfg.DOCUMENT_STATUS_START:
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
    file_name_parent = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    try:
        # Convert the 'pdf' document
        images = pdf2image.convert_from_path(file_name_parent)

        prepare_document_child_pdf2image()

        # Store the image pages
        libs.cfg.document_child_no = 0
        for img in images:
            try:
                libs.cfg.document_child_no = +1

                libs.cfg.document_child_stem_name = (
                    libs.cfg.document_stem_name + "_" + str(libs.cfg.document_child_no)
                )

                libs.cfg.document_child_file_name = (
                    libs.cfg.document_child_stem_name + "." + libs.cfg.pdf2image_type
                )

                file_name_child = os.path.join(
                    libs.cfg.document_child_directory_name,
                    libs.cfg.document_child_file_name,
                )

                img.save(
                    file_name_child,
                    libs.cfg.pdf2image_type,
                )

                journal_action: str = libs.db.cfg.JOURNAL_ACTION_21_003.replace(
                    "{file_name}", libs.cfg.document_child_file_name
                )

                initialise_document_child(journal_action)

                libs.cfg.total_generated += 1
            except OSError as err:
                libs.cfg.total_erroneous += 1

                journal_action: str = (
                    libs.db.cfg.JOURNAL_ACTION_21_902.replace(
                        "{child_no}", str(libs.cfg.document_child_no)
                    )
                    .replace("{file_name}", libs.cfg.document_child_file_name)
                    .replace("{error_code}", str(err.errno))
                    .replace("{error_msg}", err.strerror)
                )
                libs.db.orm.update_document_status(
                    {
                        libs.db.cfg.DBC_ERROR_CODE: libs.db.cfg.DOCUMENT_ERROR_CODE_REJECTED_ERROR,
                        libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
                    },
                    libs.db.orm.insert_journal(
                        __name__,
                        inspect.stack()[0][3],
                        journal_action,
                    ),
                )

            # Document successfully converted to image format
            libs.cfg.total_ok_processed += 1

            journal_action: str = libs.db.cfg.JOURNAL_ACTION_21_002.replace(
                "{child_no}", str(libs.cfg.document_child_no)
            )
            libs.db.orm.update_document_status(
                {
                    libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_END,
                },
                libs.db.orm.insert_journal(
                    __name__,
                    inspect.stack()[0][3],
                    journal_action,
                ),
            )
    except PDFPopplerTimeoutError as err:
        libs.cfg.total_erroneous += 1

        journal_action: str = libs.db.cfg.JOURNAL_ACTION_21_901.replace(
            "{file_name}", libs.cfg.document_file_name
        ).replace("{error_msg}", str(err))
        libs.db.orm.update_document_status(
            {
                libs.db.cfg.DBC_ERROR_CODE: libs.db.cfg.DOCUMENT_ERROR_CODE_REJECTED_PDF2IMAGE,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
            },
            libs.db.orm.insert_journal(
                __name__,
                inspect.stack()[0][3],
                journal_action,
            ),
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
# Initialise the base document in the database and in the journal.
# -----------------------------------------------------------------------------
def initialise_document_base(file: pathlib.Path) -> None:
    """Initialise the base document in the database and in the journal.

    Analyses the file name and creates an entry in each of the two database
    tables document and journal.

    Args:
        file (pathlib.Path): File.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    prepare_document_base(file)

    libs.cfg.document_id = libs.db.orm.insert_dbt_row(
        libs.db.cfg.DBT_DOCUMENT,
        {
            libs.db.cfg.DBC_DIRECTORY_NAME: libs.cfg.document_directory_name,
            libs.db.cfg.DBC_DIRECTORY_TYPE: libs.cfg.document_directory_type,
            libs.db.cfg.DBC_FILE_NAME: libs.cfg.document_file_name,
            libs.db.cfg.DBC_FILE_TYPE: libs.cfg.document_file_type,
            libs.db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            libs.db.cfg.DBC_SHA256: libs.cfg.document_sha256,
            libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_START,
            libs.db.cfg.DBC_STEM_NAME: libs.cfg.document_stem_name,
        },
    )

    libs.cfg.document_id_base = libs.cfg.document_id

    libs.db.orm.update_dbt_id(
        libs.db.cfg.DBT_DOCUMENT,
        libs.cfg.document_id,
        {
            libs.db.cfg.DBC_DOCUMENT_ID_BASE: libs.cfg.document_id_base,
        },
    )

    libs.db.orm.insert_dbt_row(
        libs.db.cfg.DBT_JOURNAL,
        {
            libs.db.cfg.DBC_ACTION_CODE: libs.db.cfg.JOURNAL_ACTION_01_001[0:7],
            libs.db.cfg.DBC_ACTION_TEXT: libs.db.cfg.JOURNAL_ACTION_01_001[7:],
            libs.db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id,
            libs.db.cfg.DBC_FUNCTION_NAME: inspect.stack()[0][3],
            libs.db.cfg.DBC_MODULE_NAME: __name__,
            libs.db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
        },
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise a new child document of the base document.
# -----------------------------------------------------------------------------
def initialise_document_child(journal_action: str) -> None:
    """Initialise a new child document of the base document.

    Prepares a new document for one of the file directories
    'inbox_accepted' or 'inbox_rejected'.

    Args:
        journal_action (str): Journal action data.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.document_child_id = libs.db.orm.insert_dbt_row(
        libs.db.cfg.DBT_DOCUMENT,
        {
            libs.db.cfg.DBC_DIRECTORY_NAME: libs.cfg.document_child_directory_name,
            libs.db.cfg.DBC_DIRECTORY_TYPE: libs.cfg.document_child_directory_type,
            libs.db.cfg.DBC_DOCUMENT_ID_BASE: libs.cfg.document_child_id_base,
            libs.db.cfg.DBC_DOCUMENT_ID_PARENT: libs.cfg.document_child_id_parent,
            libs.db.cfg.DBC_ERROR_CODE: libs.cfg.document_child_error_code,
            libs.db.cfg.DBC_FILE_NAME: libs.cfg.document_child_file_name,
            libs.db.cfg.DBC_FILE_TYPE: libs.cfg.document_child_file_type,
            libs.db.cfg.DBC_NEXT_STEP: libs.cfg.document_child_next_step,
            libs.db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            libs.db.cfg.DBC_STATUS: libs.cfg.document_child_status,
            libs.db.cfg.DBC_STEM_NAME: libs.cfg.document_child_stem_name,
        },
    )

    libs.db.orm.insert_dbt_row(
        libs.db.cfg.DBT_JOURNAL,
        {
            libs.db.cfg.DBC_ACTION_CODE: journal_action[0:7],
            libs.db.cfg.DBC_ACTION_TEXT: journal_action[7:],
            libs.db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id,
            libs.db.cfg.DBC_FUNCTION_NAME: inspect.stack()[0][3],
            libs.db.cfg.DBC_MODULE_NAME: __name__,
            libs.db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
        },
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare the base document data.
# -----------------------------------------------------------------------------
def prepare_document_base(file: pathlib.Path) -> None:
    """Prepare the base document data.

    Args:
        file (pathlib.Path): File.
    """
    # Example: data\inbox
    libs.cfg.document_directory_name = str(file.parent)
    libs.cfg.document_directory_type = libs.db.cfg.DOCUMENT_DIRECTORY_TYPE_INBOX
    libs.cfg.document_error_code = None

    # Example: pdf_scanned_ok.pdf
    libs.cfg.document_file_name = file.name

    # Example: pdf
    libs.cfg.document_file_type = file.suffix[1:].lower()

    # Example: 07e21aeef5600c03bc111204a44f708d592a63703a027ea4272a246304557625
    libs.cfg.document_id_base = None

    libs.cfg.document_id_parent = None
    libs.cfg.document_next_step = None

    if libs.cfg.is_ignore_duplicates:
        libs.cfg.document_sha256 = None
    else:
        libs.cfg.document_sha256 = libs.utils.get_sha256(file)

    libs.cfg.document_status = libs.db.cfg.DOCUMENT_STATUS_START

    # Example: pdf_scanned_ok
    libs.cfg.document_stem_name = pathlib.PurePath(file).stem


# -----------------------------------------------------------------------------
# Prepare the base child document data - from inbox to inbox_accepted.
# -----------------------------------------------------------------------------
def prepare_document_child_accepted() -> None:
    """Prepare the base child document data - from inbox to inbox_accepted."""
    libs.cfg.document_child_error_code = None

    libs.cfg.document_child_file_name = (
        libs.cfg.document_stem_name
        + "_"
        + str(libs.cfg.document_id)
        + "."
        + libs.cfg.document_file_type
    )

    libs.cfg.document_child_file_type = libs.cfg.document_file_type
    libs.cfg.document_child_id_base = libs.cfg.document_id
    libs.cfg.document_child_id_parent = libs.cfg.document_id
    libs.cfg.document_child_next_step = None
    libs.cfg.document_child_sha256 = None
    libs.cfg.document_child_status = libs.db.cfg.DOCUMENT_STATUS_START

    libs.cfg.document_child_stem_name = (
        libs.cfg.document_stem_name + "_" + str(libs.cfg.document_id)
    )


# -----------------------------------------------------------------------------
# Prepare the base child document data - pdf2image.
# -----------------------------------------------------------------------------
def prepare_document_child_pdf2image() -> None:
    """Prepare the base child document data - pdf2image."""
    libs.cfg.document_child_directory_name = libs.cfg.document_directory_name
    libs.cfg.document_child_directory_type = libs.cfg.document_directory_type
    libs.cfg.document_child_error_code = None

    libs.cfg.document_child_file_type = libs.cfg.pdf2image_type

    libs.cfg.document_child_id_base = libs.cfg.document_id_base
    libs.cfg.document_child_id_parent = libs.cfg.document_id

    libs.cfg.document_child_next_step = libs.db.cfg.DOCUMENT_NEXT_STEP_TESSERACT
    libs.cfg.document_child_sha256 = None
    libs.cfg.document_child_status = libs.db.cfg.DOCUMENT_STATUS_START


# -----------------------------------------------------------------------------
# Prepare a new pdf document for further processing..
# -----------------------------------------------------------------------------
def prepare_pdf(file: pathlib.Path) -> None:
    """Prepare a new pdf document for further processing.

    Args:
        file (pathlib.Path): Inbox file.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    try:
        extracted_text = "".join([page.get_text() for page in fitz.open(file)])

        if bool(extracted_text):
            journal_action: str = libs.db.cfg.JOURNAL_ACTION_11_003
            next_step: str = libs.db.cfg.DOCUMENT_NEXT_STEP_PDFLIB
        else:
            journal_action: str = libs.db.cfg.JOURNAL_ACTION_11_004.replace(
                "{type}", libs.cfg.pdf2image_type
            )
            next_step: str = libs.db.cfg.DOCUMENT_NEXT_STEP_PDF2IMAGE

        process_inbox_accepted(next_step, journal_action)
    except RuntimeError as err:
        journal_action: str = libs.db.cfg.JOURNAL_ACTION_01_903.replace(
            "{source_file}", libs.cfg.document_file_name
        ).replace("{error_msg}", str(err))
        process_inbox_rejected(
            libs.db.cfg.DOCUMENT_ERROR_CODE_REJECTED_NO_PDF_FORMAT,
            journal_action,
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the inbox directory (step: p_i).
# -----------------------------------------------------------------------------
def process_inbox() -> None:
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

            process_inbox_file(file)

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
# Accept a new document.
# -----------------------------------------------------------------------------
def process_inbox_accepted(next_step: str, journal_action: str) -> None:
    """Accept a new document.

    Args:
        next_step (str): Next processing step.
        journal_action (str): Journal action data.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    prepare_document_child_accepted()

    libs.cfg.document_child_directory_name = libs.cfg.config[
        libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    ]
    libs.cfg.document_child_directory_type = libs.db.cfg.DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED
    libs.cfg.document_child_next_step = next_step
    libs.cfg.document_child_status = libs.db.cfg.DOCUMENT_STATUS_START

    source_file = os.path.join(libs.cfg.document_directory_name, libs.cfg.document_file_name)
    target_file = os.path.join(
        libs.cfg.document_child_directory_name, libs.cfg.document_child_file_name
    )

    try:
        shutil.move(source_file, target_file)

        initialise_document_child(journal_action)

        libs.db.orm.update_dbt_id(
            libs.db.cfg.DBT_DOCUMENT,
            libs.cfg.document_id,
            {
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_END,
            },
        )

        libs.cfg.total_ok_processed += 1

        return
    except PermissionError as err:
        # pylint: disable=expression-not-assigned
        journal_action: str = (
            libs.db.cfg.JOURNAL_ACTION_01_904.replace("{source_file}", source_file)
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        error_code_local = "File access rights issue"

        libs.db.orm.update_document_status(
            {
                libs.db.cfg.DBC_ERROR_CODE: error_code_local,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ABORT,
            },
            libs.db.orm.insert_journal(
                __name__,
                inspect.stack()[0][3],
                journal_action,
            ),
        ),
    except shutil.Error as err:
        # pylint: disable=expression-not-assigned
        journal_action: str = (
            libs.db.cfg.JOURNAL_ACTION_01_902.replace("{source_file}", source_file)
            .replace("{target_file}", target_file)
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        error_code_local = "File move issue"

        libs.db.orm.update_document_status(
            {
                libs.db.cfg.DBC_ERROR_CODE: error_code_local,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ABORT,
            },
            libs.db.orm.insert_journal(
                __name__,
                inspect.stack()[0][3],
                journal_action,
            ),
        ),

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the next inbox file.
# -----------------------------------------------------------------------------
def process_inbox_file(file: pathlib.Path) -> None:
    """Process the next inbox file.

    Args:
        file (pathlib.Path): Inbox file.
    """
    libs.cfg.session = Session(libs.db.cfg.engine)

    initialise_document_base(file)

    if not libs.cfg.is_ignore_duplicates:
        file_name = libs.db.orm.select_document_file_name_sha256(
            libs.cfg.document_id, libs.cfg.document_sha256
        )
    else:
        file_name = None

    if file_name is not None:
        process_inbox_rejected(
            libs.db.cfg.DOCUMENT_ERROR_CODE_REJECTED_FILE_DUPL,
            libs.db.cfg.JOURNAL_ACTION_01_905.replace("{file_name}", file_name),
        )
    elif libs.cfg.document_file_type == libs.db.cfg.DOCUMENT_FILE_TYPE_PDF:
        prepare_pdf(file)
    elif libs.cfg.document_file_type in libs.db.cfg.DOCUMENT_FILE_TYPE_PANDOC:
        process_inbox_accepted(
            libs.db.cfg.DOCUMENT_NEXT_STEP_PANDOC, libs.db.cfg.JOURNAL_ACTION_11_001
        )
    elif libs.cfg.document_file_type in libs.db.cfg.DOCUMENT_FILE_TYPE_TESSERACT:
        process_inbox_accepted(
            libs.db.cfg.DOCUMENT_NEXT_STEP_TESSERACT, libs.db.cfg.JOURNAL_ACTION_11_002
        )
    else:
        process_inbox_rejected(
            libs.db.cfg.DOCUMENT_ERROR_CODE_REJECTED_FILE_EXT,
            libs.db.cfg.JOURNAL_ACTION_01_901.replace("{extension}", file.suffix[1:]),
        )


# -----------------------------------------------------------------------------
# Reject a new document that is faulty.
# -----------------------------------------------------------------------------
def process_inbox_rejected(error_code: str, journal_action: str) -> None:
    """Reject a new document that is faulty.

    Args:
        error_code (str): Error code.
        journal_action (str): Journal action data.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    prepare_document_child_accepted()

    libs.cfg.document_child_directory_name = libs.cfg.config[
        libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED
    ]
    libs.cfg.document_child_directory_type = libs.db.cfg.DOCUMENT_DIRECTORY_TYPE_INBOX_REJECTED
    libs.cfg.document_child_error_code = error_code
    libs.cfg.document_child_status = libs.db.cfg.DOCUMENT_STATUS_ERROR

    source_file = os.path.join(libs.cfg.document_directory_name, libs.cfg.document_file_name)
    target_file = os.path.join(
        libs.cfg.document_child_directory_name, libs.cfg.document_child_file_name
    )

    # error_code_local: str | None = None
    try:
        libs.cfg.total_erroneous += 1

        shutil.move(source_file, target_file)

        initialise_document_child(journal_action)

        libs.db.orm.update_dbt_id(
            libs.db.cfg.DBT_DOCUMENT,
            libs.cfg.document_id,
            {
                libs.db.cfg.DBC_ERROR_CODE: error_code,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
            },
        )

        libs.cfg.total_rejected += 1

        return
    except PermissionError as err:
        # pylint: disable=expression-not-assigned
        journal_action: str = (
            libs.db.cfg.JOURNAL_ACTION_01_904.replace("{source_file}", source_file)
            .replace("{error_code}", str(err.errno))
            .replace("{error_msg}", err.strerror)
        )
        error_code_local = "File access rights issue"

        libs.db.orm.update_document_status(
            {
                libs.db.cfg.DBC_ERROR_CODE: error_code_local,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ABORT,
            },
            libs.db.orm.insert_journal(
                __name__,
                inspect.stack()[0][3],
                journal_action,
            ),
        ),
    except shutil.Error as err:
        # pylint: disable=expression-not-assigned
        journal_action: str = libs.db.cfg.JOURNAL_ACTION_01_902.replace(
            "{source_file}", source_file
        ).replace(
            "{target_file}",
            target_file.replace("{error_code}", str(err.errno)).replace(
                "{error_msg}", err.strerror
            ),
        )
        error_code_local = "File move issue"

        libs.db.orm.update_document_status(
            {
                libs.db.cfg.DBC_ERROR_CODE: error_code_local,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ABORT,
            },
            libs.db.orm.insert_journal(
                __name__,
                inspect.stack()[0][3],
                journal_action,
            ),
        ),

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
