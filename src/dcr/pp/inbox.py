# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

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

import dcr_core.core_glob
import dcr_core.core_utils
import fitz
import sqlalchemy
import sqlalchemy.orm

import dcr.cfg.glob
import dcr.db.cls_action
import dcr.db.cls_document
import dcr.db.cls_language
import dcr.db.cls_run
import dcr.utils

# -----------------------------------------------------------------------------
# Class variables.
# -----------------------------------------------------------------------------
ERROR_01_901 = "01.901 Issue (p_i): Document rejected because of unknown file extension='{extension}'."
ERROR_01_903 = "01.903 Issue (p_i): Runtime error with fitz.open() processing of file '{file_name}' " + "- error: '{error_msg}'."
ERROR_01_905 = "01.905 Issue (p_i): The same file has probably already been processed " + "once under the file name '{file_name}'."
ERROR_01_906 = "01.906 Issue (p_i): The target file '{full_name}' already exists."


# -----------------------------------------------------------------------------
# Check the inbox file directories and create the missing ones.
# -----------------------------------------------------------------------------
def check_and_create_directories() -> None:
    """Check the inbox file directories and create the missing ones.

    The file directory inbox must exist. The two file directories
    inbox_accepted and inbox_rejected are created if they do not already
    exist.
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    create_directory("the accepted documents", str(dcr_core.core_glob.setup.directory_inbox_accepted))

    create_directory("the rejected documents", str(dcr_core.core_glob.setup.directory_inbox_rejected))

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create a new file directory if it does not already exist..
# -----------------------------------------------------------------------------
def create_directory(directory_type: str, directory_name: str) -> None:
    """Create a new file directory if it does not already exist.

    Args:
        directory_type (str): Directory type.
        directory_name (str): Directory name - may include a path.
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)
        dcr.utils.progress_msg(
            f"The file directory for '{directory_type}' " f"was newly created under the name '{directory_name}'",
        )

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise the next action in the database.
# -----------------------------------------------------------------------------
def initialise_action(
    action_code: str = "",
    directory_name: str = "",
    directory_type: str = "",
    file_name: str = "",
    id_parent: int = 0,
) -> dcr.db.cls_action.Action:
    """Initialise the next action in the database.

    Args:
        action_code (str, optional): Action code. Defaults to "".
        directory_name (str, optional): Directory name. Defaults to "".
        directory_type (str, optional): Directory type. Defaults to "".
        file_name (str, optional): File name. Defaults to "".
        id_parent (int, optional): File name. Defaults to "".

    Returns:
        type[dcr.db.cls_action.Action]: A new Action instance.
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    full_name = dcr_core.core_utils.get_full_name(directory_name, file_name)

    action = dcr.db.cls_action.Action(
        action_code=action_code,
        id_run_last=dcr.cfg.glob.run.run_id,
        directory_name=directory_name,
        directory_type=directory_type,
        file_name=file_name,
        file_size_bytes=os.path.getsize(full_name),
        id_document=dcr.cfg.glob.document.document_id,
        id_parent=id_parent,
        no_pdf_pages=dcr.utils.get_pdf_pages_no(full_name),
    )

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    return action


# -----------------------------------------------------------------------------
# Initialise the base document in the database.
# -----------------------------------------------------------------------------
def initialise_base(file_path: pathlib.Path) -> None:
    """Initialise the base document in the database.

    Args:
        file_path (pathlib.Path): File.
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    dcr.cfg.glob.document = dcr.db.cls_document.Document(
        action_code_last=dcr.cfg.glob.run.run_action_code,
        directory_name=str(file_path.parent),
        file_name=file_path.name,
        id_language=dcr.cfg.glob.language.language_id,
        id_run_last=dcr.cfg.glob.run.run_id,
    )

    if not dcr_core.core_glob.setup.is_ignore_duplicates:
        dcr.cfg.glob.document.document_sha256 = dcr.utils.compute_sha256(file_path)

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare a new pdf document for further processing..
# -----------------------------------------------------------------------------
def prepare_pdf(file_path: pathlib.Path) -> None:
    """Prepare a new pdf document for further processing.

    Args:
        file_path (pathlib.Path): Inbox file.
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    try:
        extracted_text = "".join([page.get_text() for page in fitz.open(file_path)])

        if bool(extracted_text):
            action_code = dcr.db.cls_run.Run.ACTION_CODE_PDFLIB
            dcr.cfg.glob.language.total_processed_pdflib += 1
            dcr.cfg.glob.run.total_processed_pdflib += 1
        else:
            action_code = dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE
            dcr.cfg.glob.language.total_processed_pdf2image += 1
            dcr.cfg.glob.run.total_processed_pdf2image += 1

        process_inbox_accepted(action_code)
    except RuntimeError as err:
        process_inbox_rejected(
            dcr.db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_NO_PDF_FORMAT,
            ERROR_01_903.replace("{file_name}", dcr.cfg.glob.document.document_file_name).replace("{error_msg}", str(err)),
        )

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


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
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    if dcr_core.core_glob.setup.is_ignore_duplicates:
        dcr.utils.progress_msg("Configuration: File duplicates are allowed!")
    else:
        dcr.utils.progress_msg("Configuration: File duplicates are not allowed!")

    # Check the inbox file directories and create the missing ones.
    check_and_create_directories()

    dcr.utils.reset_statistics_total()

    with dcr.cfg.glob.db_core.db_orm_engine.connect() as conn:
        for row in dcr.db.cls_language.Language.select_active_languages(conn):
            dcr.cfg.glob.language = dcr.db.cls_language.Language.from_row(row)
            if os.path.isdir(dcr.cfg.glob.language.language_directory_name_inbox):
                process_inbox_language()

        conn.close()

    dcr.utils.show_statistics_total()

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Accept a new document.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_inbox_accepted(action_code: str) -> None:
    """Accept a new document.

    Args:
        action_code (str): Action code.
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    full_name_curr = dcr.cfg.glob.document.get_full_name()
    full_name_next = dcr_core.core_utils.get_full_name(
        dcr_core.core_glob.setup.directory_inbox_accepted, dcr.cfg.glob.document.get_file_name_next()
    )

    dcr.cfg.glob.action_curr = initialise_action(
        action_code=dcr.cfg.glob.run.run_action_code,
        directory_name=dcr.cfg.glob.language.language_directory_name_inbox,
        directory_type=dcr.db.cls_document.Document.DOCUMENT_DIRECTORY_TYPE_INBOX,
        file_name=dcr.cfg.glob.document.document_file_name,
    )

    if os.path.exists(full_name_next):
        dcr.cfg.glob.action_curr.finalise_error(
            error_code=dcr.db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=ERROR_01_906.replace("{full_name}", full_name_next),
        )
    else:
        shutil.move(full_name_curr, full_name_next)

        dcr.cfg.glob.action_next = initialise_action(
            action_code=action_code,
            directory_name=dcr_core.core_glob.setup.directory_inbox_accepted,
            directory_type=dcr.db.cls_document.Document.DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED,
            file_name=dcr.cfg.glob.document.get_file_name_next(),
            id_parent=dcr.cfg.glob.action_curr.action_id,
        )

        dcr.cfg.glob.action_curr.finalise()

        dcr.cfg.glob.language.total_processed += 1
        dcr.cfg.glob.run.run_total_processed_ok += 1

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the next inbox file.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_inbox_file(file_path: pathlib.Path) -> None:
    """Process the next inbox file.

    Args:
        file_path (pathlib.Path):
                Inbox file.
    """
    dcr.cfg.glob.session = sqlalchemy.orm.Session(dcr.cfg.glob.db_core.db_orm_engine)

    initialise_base(file_path)

    if not dcr_core.core_glob.setup.is_ignore_duplicates:
        file_name = dcr.db.cls_document.Document.select_duplicate_file_name_by_sha256(
            dcr.cfg.glob.document.document_id, dcr.cfg.glob.document.document_sha256
        )
    else:
        file_name = None

    if not (file_name is None or file_name == ""):
        process_inbox_rejected(
            dcr.db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            ERROR_01_905.replace("{file_name}", file_name),
        )
    elif dcr.cfg.glob.document.get_file_type() == dcr_core.core_glob.FILE_TYPE_PDF:
        prepare_pdf(file_path)
    elif dcr.cfg.glob.document.get_file_type() in dcr_core.core_glob.FILE_TYPE_PANDOC:
        process_inbox_accepted(dcr.db.cls_run.Run.ACTION_CODE_PANDOC)
        dcr.cfg.glob.language.total_processed_pandoc += 1
        dcr.cfg.glob.run.total_processed_pandoc += 1
    elif dcr.cfg.glob.document.get_file_type() in dcr_core.core_glob.FILE_TYPE_TESSERACT:
        process_inbox_accepted(dcr.db.cls_run.Run.ACTION_CODE_TESSERACT)
        dcr.cfg.glob.language.total_processed_tesseract += 1
        dcr.cfg.glob.run.total_processed_tesseract += 1
    else:
        process_inbox_rejected(
            dcr.db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_EXT,
            ERROR_01_901.replace("{extension}", file_path.suffix[1:]),
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
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    dcr.utils.progress_msg(f"Start of processing for language '{dcr.cfg.glob.language.language_iso_language_name}'")

    for file in sorted(dcr.utils.get_path_name(dcr.cfg.glob.language.language_directory_name_inbox).iterdir()):
        if file.is_file():
            dcr.cfg.glob.start_time_document = time.perf_counter_ns()

            if file.name == "README.md":
                dcr.utils.progress_msg("Attention: All files with the file name 'README.md' are ignored")
                continue

            dcr.cfg.glob.language.total_processed_to_be += 1
            dcr.cfg.glob.run.run_total_processed_to_be += 1

            process_inbox_file(file_path=file)

    dcr.utils.show_statistics_language()

    dcr.utils.progress_msg(
        f"End   of processing for language '{dcr.cfg.glob.language.language_iso_language_name}'",
    )

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Reject a new document that is faulty.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_inbox_rejected(error_code: str, error_msg: str) -> None:
    """Reject a new document that is faulty.

    Args:
        error_code (str): Error code.
        error_msg (str):  Error message.
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    full_name_curr = dcr.cfg.glob.document.get_full_name()
    full_name_next = dcr_core.core_utils.get_full_name(
        dcr_core.core_glob.setup.directory_inbox_rejected,
        dcr.cfg.glob.document.get_file_name_next(),
    )

    dcr.cfg.glob.action_curr = initialise_action(
        action_code=dcr.cfg.glob.run.run_action_code,
        directory_name=dcr.cfg.glob.language.language_directory_name_inbox,
        directory_type=dcr.db.cls_document.Document.DOCUMENT_DIRECTORY_TYPE_INBOX,
        file_name=dcr.cfg.glob.document.document_file_name,
    )

    # Move the document file from directory inbox to directory inbox_rejected - if not yet existing
    if os.path.exists(full_name_next):
        dcr.cfg.glob.action_curr.finalise_error(
            error_code=dcr.db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=ERROR_01_906.replace("{full_name}", full_name_next),
        )
    else:
        shutil.move(full_name_curr, full_name_next)

        dcr.cfg.glob.action_curr.finalise_error(
            error_code=error_code,
            error_msg=error_msg,
        )

    dcr.cfg.glob.language.total_erroneous += 1
    dcr.cfg.glob.run.run_total_erroneous += 1

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)
