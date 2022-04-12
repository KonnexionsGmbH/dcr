"""Module pp.inbox: Check, distribute and process incoming documents.

New documents are made available in the file directory inbox. These are
then checked and moved to the accepted or rejected file directories
depending on the result of the check. Depending on the file format, the
accepted documents are then converted into the pdf file format either
with the help of Pandoc and TeX Live or with the help of Tesseract OCR.
"""
import os
import pathlib
import shutil
import time

import db.cfg
import db.orm.dml
import fitz
import libs.cfg
import libs.utils
from sqlalchemy import Table
from sqlalchemy.orm import Session


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

    create_directory("the accepted documents", str(libs.cfg.directory_inbox_accepted))

    create_directory("the rejected documents", str(libs.cfg.directory_inbox_rejected))

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


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
        os.mkdir(directory_name)
        libs.utils.progress_msg(
            f"The file directory for '{directory_type}' "
            f"was newly created under the name '{directory_name}'",
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise the base document in the database.
# -----------------------------------------------------------------------------
def initialise_document_base(file_path: pathlib.Path) -> None:
    """Initialise the base document in the database.

    Analyses the file name and creates an entry in each of the two database
    table 'document'.

    Args:
        file_path (pathlib.Path): File.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    prepare_document_base(file_path)

    db.orm.dml.insert_document_base()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare the base document data.
# -----------------------------------------------------------------------------
def prepare_document_base(file_path: pathlib.Path) -> None:
    """Prepare the base document data.

    Args:
        file_path (pathlib.Path): File.
    """
    # Example: data\inbox
    libs.cfg.document_directory_name = str(file_path.parent)
    libs.cfg.document_directory_type = db.cfg.DOCUMENT_DIRECTORY_TYPE_INBOX
    libs.cfg.document_error_code = None

    # Example: pdf_scanned_ok.pdf
    libs.cfg.document_file_name = file_path.name

    # Example: pdf
    libs.cfg.document_file_type = file_path.suffix[1:].lower()

    # Example: 07e21aeef5600c03bc111204a44f708d592a63703a027ea4272a246304557625
    libs.cfg.document_id_base = None

    libs.cfg.document_id_parent = None
    libs.cfg.document_next_step = None

    if libs.cfg.is_ignore_duplicates:
        libs.cfg.document_sha256 = None
    else:
        libs.cfg.document_sha256 = libs.utils.compute_sha256(file_path)

    libs.cfg.document_status = db.cfg.DOCUMENT_STATUS_START

    # Example: pdf_scanned_ok
    libs.cfg.document_stem_name = pathlib.PurePath(file_path).stem


# -----------------------------------------------------------------------------
# Prepare the base child document data - from inbox to inbox_accepted.
# -----------------------------------------------------------------------------
def prepare_document_child_accepted() -> None:
    """Prepare the base child document data - from inbox to inbox_accepted."""
    libs.cfg.document_child_child_no = None
    libs.cfg.document_child_error_code = None

    libs.cfg.document_child_file_name = (
        libs.cfg.document_stem_name
        + "_"
        + str(libs.cfg.document_id)
        + "."
        + (
            libs.cfg.document_file_type
            if libs.cfg.document_file_type != db.cfg.DOCUMENT_FILE_TYPE_TIF
            else db.cfg.DOCUMENT_FILE_TYPE_TIFF
        )
    )

    libs.cfg.document_child_file_type = libs.cfg.document_file_type
    libs.cfg.document_child_id_base = libs.cfg.document_id
    libs.cfg.document_child_id_parent = libs.cfg.document_id
    libs.cfg.document_child_next_step = None
    libs.cfg.document_child_status = db.cfg.DOCUMENT_STATUS_START

    libs.cfg.document_child_stem_name = (
        libs.cfg.document_stem_name + "_" + str(libs.cfg.document_id)
    )


# -----------------------------------------------------------------------------
# Prepare a new pdf document for further processing..
# -----------------------------------------------------------------------------
def prepare_pdf(file_path: pathlib.Path) -> None:
    """Prepare a new pdf document for further processing.

    Args:
        file_path (pathlib.Path): Inbox file.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    try:
        extracted_text = "".join([page.get_text() for page in fitz.open(file_path)])

        prepare_document_child_accepted()

        if bool(extracted_text):
            next_step: str = db.cfg.DOCUMENT_STEP_PDFLIB
            libs.cfg.language_ok_processed_pdflib += 1
            libs.cfg.total_ok_processed_pdflib += 1
        else:
            next_step: str = db.cfg.DOCUMENT_STEP_PDF2IMAGE
            libs.cfg.language_ok_processed_pdf2image += 1
            libs.cfg.total_ok_processed_pdf2image += 1

        process_inbox_accepted(next_step)
    except RuntimeError as err:
        process_inbox_rejected(
            db.cfg.DOCUMENT_ERROR_CODE_REJ_NO_PDF_FORMAT,
            db.cfg.ERROR_01_903.replace("{source_file}", libs.cfg.document_file_name).replace(
                "{error_msg}", str(err)
            ),
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the inbox directory (step: p_i).
# -----------------------------------------------------------------------------
def process_inbox() -> None:
    """Process the files found in the inbox file directory.

    1. Documents of type docx are converted to pdf format
       and copied to the inbox_accepted directory.
    2. Documents of type pdf that do not consist only of a scanned image are
       copied unchanged to the inbox_accepted directory.
    3. Documents of type pdf consisting only of a scanned image are copied
       unchanged to the inbox_ocr directory.
    4. All other documents are copied to the inbox_rejected directory.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.is_ignore_duplicates:
        libs.utils.progress_msg("Configuration: File duplicates are allowed!")
    else:
        libs.utils.progress_msg("Configuration: File duplicates are not allowed!")

    # Check the inbox file directories and create the missing ones.
    check_and_create_directories()

    libs.utils.reset_statistics_total()

    dbt = Table(
        db.cfg.DBT_LANGUAGE,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    with db.cfg.db_orm_engine.connect() as conn:
        for row in db.orm.dml.select_language(conn, dbt):
            libs.cfg.language_id = row.id
            libs.cfg.language_directory_inbox = row.directory_name_inbox
            libs.cfg.language_iso_language_name = row.iso_language_name

            if libs.cfg.language_directory_inbox is None:
                libs.cfg.language_directory_inbox = pathlib.Path(
                    str(libs.cfg.directory_inbox), libs.cfg.language_iso_language_name.lower()
                )

            if os.path.isdir(pathlib.Path(str(libs.cfg.language_directory_inbox))):
                process_inbox_language()

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Accept a new document.
# -----------------------------------------------------------------------------
def process_inbox_accepted(next_step: str) -> None:
    """Accept a new document.

    Args:
        next_step (str): Next processing step.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.document_child_directory_name = libs.cfg.config[
        libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    ]
    libs.cfg.document_child_directory_type = db.cfg.DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED
    libs.cfg.document_child_next_step = next_step
    libs.cfg.document_child_status = db.cfg.DOCUMENT_STATUS_START

    source_file = os.path.join(libs.cfg.document_directory_name, libs.cfg.document_file_name)
    target_file = os.path.join(
        libs.cfg.document_child_directory_name, libs.cfg.document_child_file_name
    )

    if os.path.exists(target_file):
        db.orm.dml.update_document_error(
            document_id=libs.cfg.document_id,
            error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=db.cfg.ERROR_01_906.replace("{file_name}", target_file),
        )
    else:
        shutil.move(source_file, target_file)

        db.orm.dml.insert_document_child()

        db.orm.dml.update_document_statistics(
            document_id=libs.cfg.document_id, status=db.cfg.DOCUMENT_STATUS_END
        )

        libs.cfg.language_ok_processed += 1
        libs.cfg.total_ok_processed += 1

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the next inbox file.
# -----------------------------------------------------------------------------
def process_inbox_file(file_path: pathlib.Path) -> None:
    """Process the next inbox file.

    Args:
        file_path (pathlib.Path): Inbox file.
    """
    libs.cfg.session = Session(db.cfg.db_orm_engine)

    initialise_document_base(file_path)

    if not libs.cfg.is_ignore_duplicates:
        file_name = db.orm.dml.select_document_file_name_sha256(
            libs.cfg.document_id, libs.cfg.document_sha256
        )
    else:
        file_name = None

    if file_name is not None:
        process_inbox_rejected(
            db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            db.cfg.ERROR_01_905.replace("{file_name}", file_name),
        )
    elif libs.cfg.document_file_type == db.cfg.DOCUMENT_FILE_TYPE_PDF:
        prepare_pdf(file_path)
    elif libs.cfg.document_file_type in db.cfg.DOCUMENT_FILE_TYPE_PANDOC:
        prepare_document_child_accepted()
        process_inbox_accepted(db.cfg.DOCUMENT_STEP_PANDOC)
        libs.cfg.language_ok_processed_pandoc += 1
        libs.cfg.total_ok_processed_pandoc += 1
    elif libs.cfg.document_file_type in db.cfg.DOCUMENT_FILE_TYPE_TESSERACT:
        prepare_document_child_accepted()
        process_inbox_accepted(db.cfg.DOCUMENT_STEP_TESSERACT)
        libs.cfg.language_ok_processed_tesseract += 1
        libs.cfg.total_ok_processed_tesseract += 1
    else:
        process_inbox_rejected(
            db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_EXT,
            db.cfg.ERROR_01_901.replace("{extension}", file_path.suffix[1:]),
        )


# -----------------------------------------------------------------------------
# Process the inbox directory (step: p_i).
# -----------------------------------------------------------------------------
def process_inbox_language() -> None:
    """Process the files found in the inbox file directory.

    1. Documents of type docx are converted to pdf format
       and copied to the inbox_accepted directory.
    2. Documents of type pdf that do not consist only of a scanned image are
       copied unchanged to the inbox_accepted directory.
    3. Documents of type pdf consisting only of a scanned image are copied
       unchanged to the inbox_ocr directory.
    4. All other documents are copied to the inbox_rejected directory.
    """
    libs.utils.progress_msg(
        f"Start of processing for language '{libs.cfg.language_iso_language_name}'"
    )

    libs.utils.reset_statistics_language()

    for file in sorted(pathlib.Path(libs.cfg.language_directory_inbox).iterdir()):
        if file.is_file():
            libs.cfg.start_time_document = time.perf_counter_ns()

            if file.name == "README.md":
                libs.utils.progress_msg(
                    "Attention: All files with the file name 'README.md' are ignored"
                )
                continue

            libs.cfg.language_to_be_processed += 1
            libs.cfg.total_to_be_processed += 1

            process_inbox_file(file)

    libs.utils.show_statistics_language()

    libs.utils.progress_msg(
        f"End   of processing for language '{libs.cfg.language_iso_language_name}'",
    )


# -----------------------------------------------------------------------------
# Reject a new document that is faulty.
# -----------------------------------------------------------------------------
def process_inbox_rejected(error_code: str, error_msg: str) -> None:
    """Reject a new document that is faulty.

    Args:
        error_code (str): Error code.
        error_msg (str):  Error message.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    prepare_document_child_accepted()

    libs.cfg.document_child_directory_name = libs.cfg.config[
        libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED
    ]
    libs.cfg.document_child_directory_type = db.cfg.DOCUMENT_DIRECTORY_TYPE_INBOX_REJECTED
    libs.cfg.document_child_error_code = error_code
    libs.cfg.document_child_status = db.cfg.DOCUMENT_STATUS_ERROR

    source_file = os.path.join(libs.cfg.document_directory_name, libs.cfg.document_file_name)
    target_file = os.path.join(
        libs.cfg.document_child_directory_name, libs.cfg.document_child_file_name
    )

    # Move the document file from directory inbox to directory inbox_rejected - if not yet existing
    if os.path.exists(target_file):
        db.orm.dml.update_document_error(
            document_id=libs.cfg.document_id,
            error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=db.cfg.ERROR_01_906.replace("{file_name}", target_file),
        )
    else:
        shutil.move(source_file, target_file)

        db.orm.dml.insert_document_child()

        db.orm.dml.update_document_error(
            document_id=libs.cfg.document_id,
            error_code=error_code,
            error_msg=error_msg,
        )

        libs.cfg.language_erroneous += 1

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
