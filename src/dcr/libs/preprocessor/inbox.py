"""Module libs.preprocessor.inbox: Check, distribute and process incoming
documents.

New documents are made available in the file directory inbox. These are
then checked and moved to the accepted or rejected file directories
depending on the result of the check. Depending on the file format, the
accepted documents are then converted into the pdf file format either
with the help of Pandoc and TeX Live or with the help of Tesseract OCR.
"""
import inspect
import os
import pathlib
import shutil
import time

import fitz
import libs.cfg
import libs.db.cfg
import libs.db.orm
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
            "The file directory for "
            + directory_type
            + " was "
            + "newly created under the name "
            + directory_name,
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
            libs.db.cfg.DBC_LANGUAGE_ID: libs.cfg.language_id,
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

    # pylint: disable=expression-not-assigned
    libs.db.orm.insert_journal(
        __name__,
        inspect.stack()[0][3],
        libs.cfg.document_id,
        libs.db.cfg.JOURNAL_ACTION_01_001.replace("{file_name}", libs.cfg.document_file_name),
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
        libs.cfg.document_sha256 = libs.utils.compute_sha256(file)

    libs.cfg.document_status = libs.db.cfg.DOCUMENT_STATUS_START

    # Example: pdf_scanned_ok
    libs.cfg.document_stem_name = pathlib.PurePath(file).stem


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
            if libs.cfg.document_file_type != libs.db.cfg.DOCUMENT_FILE_TYPE_TIF
            else libs.db.cfg.DOCUMENT_FILE_TYPE_TIFF
        )
    )

    libs.cfg.document_child_file_type = libs.cfg.document_file_type
    libs.cfg.document_child_id_base = libs.cfg.document_id
    libs.cfg.document_child_id_parent = libs.cfg.document_id
    libs.cfg.document_child_next_step = None
    libs.cfg.document_child_status = libs.db.cfg.DOCUMENT_STATUS_START

    libs.cfg.document_child_stem_name = (
        libs.cfg.document_stem_name + "_" + str(libs.cfg.document_id)
    )


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

        prepare_document_child_accepted()

        if bool(extracted_text):
            journal_action: str = libs.db.cfg.JOURNAL_ACTION_11_003
            next_step: str = libs.db.cfg.DOCUMENT_NEXT_STEP_PDFLIB
            libs.cfg.language_ok_processed_pdflib += 1
            libs.cfg.total_ok_processed_pdflib += 1
        else:
            journal_action: str = libs.db.cfg.JOURNAL_ACTION_01_003.replace(
                "{file_name}", libs.cfg.document_child_file_name
            ).replace("{type}", libs.cfg.pdf2image_type)
            next_step: str = libs.db.cfg.DOCUMENT_NEXT_STEP_PDF2IMAGE
            libs.cfg.language_ok_processed_pdf2image += 1
            libs.cfg.total_ok_processed_pdf2image += 1

        process_inbox_accepted(next_step, journal_action)
    except RuntimeError as err:
        process_inbox_rejected(
            libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_NO_PDF_FORMAT,
            libs.db.cfg.JOURNAL_ACTION_01_903.replace(
                "{source_file}", libs.cfg.document_file_name
            ).replace("{error_msg}", str(err)),
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
        libs.db.cfg.DBT_LANGUAGE,
        libs.db.cfg.db_orm_metadata,
        autoload_with=libs.db.cfg.db_orm_engine,
    )

    with libs.db.cfg.db_orm_engine.connect() as conn:
        for row in libs.utils.select_language(conn, dbt):
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
def process_inbox_accepted(next_step: str, journal_action: str) -> None:
    """Accept a new document.

    Args:
        next_step (str): Next processing step.
        journal_action (str): Journal action data.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

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

    if os.path.exists(target_file):
        libs.utils.report_document_error(
            module_name=__name__,
            function_name=inspect.stack()[0][3],
            error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            journal_action=libs.db.cfg.JOURNAL_ACTION_01_906.replace("{file_name}", target_file),
        )
        libs.cfg.language_erroneous += 1
    else:
        shutil.move(source_file, target_file)

        libs.utils.initialise_document_child(journal_action)

        libs.db.orm.update_dbt_id(
            libs.db.cfg.DBT_DOCUMENT,
            libs.cfg.document_id,
            {
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_END,
            },
        )

        # pylint: disable=expression-not-assigned
        libs.db.orm.insert_journal(
            __name__,
            inspect.stack()[0][3],
            libs.cfg.document_id,
            libs.db.cfg.JOURNAL_ACTION_01_002.replace("{source_file}", source_file).replace(
                "{target_file}", target_file
            ),
        )

        libs.cfg.language_ok_processed += 1
        libs.cfg.total_ok_processed += 1

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the next inbox file.
# -----------------------------------------------------------------------------
def process_inbox_file(file: pathlib.Path) -> None:
    """Process the next inbox file.

    Args:
        file (pathlib.Path): Inbox file.
    """
    libs.cfg.session = Session(libs.db.cfg.db_orm_engine)

    initialise_document_base(file)

    if not libs.cfg.is_ignore_duplicates:
        file_name = libs.db.orm.select_document_file_name_sha256(
            libs.cfg.document_id, libs.cfg.document_sha256
        )
    else:
        file_name = None

    if file_name is not None:
        process_inbox_rejected(
            libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            libs.db.cfg.JOURNAL_ACTION_01_905.replace("{file_name}", file_name),
        )
    elif libs.cfg.document_file_type == libs.db.cfg.DOCUMENT_FILE_TYPE_PDF:
        prepare_pdf(file)
    elif libs.cfg.document_file_type in libs.db.cfg.DOCUMENT_FILE_TYPE_PANDOC:
        prepare_document_child_accepted()
        process_inbox_accepted(
            libs.db.cfg.DOCUMENT_NEXT_STEP_PANDOC, libs.db.cfg.JOURNAL_ACTION_11_001
        )
        libs.cfg.language_ok_processed_pandoc += 1
        libs.cfg.total_ok_processed_pandoc += 1
    elif libs.cfg.document_file_type in libs.db.cfg.DOCUMENT_FILE_TYPE_TESSERACT:
        prepare_document_child_accepted()
        process_inbox_accepted(
            libs.db.cfg.DOCUMENT_NEXT_STEP_TESSERACT, libs.db.cfg.JOURNAL_ACTION_11_002
        )
        libs.cfg.language_ok_processed_tesseract += 1
        libs.cfg.total_ok_processed_tesseract += 1
    else:
        process_inbox_rejected(
            libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_EXT,
            libs.db.cfg.JOURNAL_ACTION_01_901.replace("{extension}", file.suffix[1:]),
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
        "Start of processing for language " + libs.cfg.language_iso_language_name,
    )

    libs.utils.reset_statistics_language()

    for file in sorted(pathlib.Path(libs.cfg.language_directory_inbox).iterdir()):
        if file.is_file():
            if file.name == "README.md":
                libs.utils.progress_msg(
                    "Attention: All files with the file name 'README.md' " + "are ignored"
                )
                continue

            libs.cfg.language_to_be_processed += 1
            libs.cfg.total_to_be_processed += 1

            libs.cfg.start_time_document = time.perf_counter_ns()
            process_inbox_file(file)

    libs.utils.show_statistics_language()

    libs.utils.progress_msg(
        "End   of processing for language " + libs.cfg.language_iso_language_name,
    )


# -----------------------------------------------------------------------------
# Reject a new document that is faulty.
# -----------------------------------------------------------------------------
def process_inbox_rejected(error_code: str, journal_action: str) -> None:
    """Reject a new document that is faulty.

    Args:
        error_code (str):     Error code.
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

    if os.path.exists(target_file):
        libs.db.orm.insert_journal(
            __name__,
            inspect.stack()[0][3],
            libs.cfg.document_id,
            libs.db.cfg.JOURNAL_ACTION_01_906.replace("{file_name}", target_file),
        )
        libs.cfg.language_erroneous += 1
    else:
        shutil.move(source_file, target_file)

        libs.utils.initialise_document_child(journal_action)

        libs.db.orm.update_dbt_id(
            libs.db.cfg.DBT_DOCUMENT,
            libs.cfg.document_id,
            {
                libs.db.cfg.DBC_ERROR_CODE: error_code,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
            },
        )

        libs.cfg.language_erroneous += 1
        libs.cfg.total_erroneous += 1

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
