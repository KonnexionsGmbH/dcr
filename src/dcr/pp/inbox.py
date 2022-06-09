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

import cfg.glob
import db.cls_action
import db.cls_document
import db.cls_language
import db.cls_run
import fitz
import sqlalchemy
import sqlalchemy.orm
import utils

# -----------------------------------------------------------------------------
# Class variables.
# -----------------------------------------------------------------------------
ERROR_01_901 = "01.901 Issue (p_i): Document rejected because of unknown file extension='{extension}'."
ERROR_01_903 = (
    "01.903 Issue (p_i): Runtime error with fitz.open() processing of file '{file_name}' " + "- error: '{error_msg}'."
)
ERROR_01_905 = (
    "01.905 Issue (p_i): The same file has probably already been processed " + "once under the file name '{file_name}'."
)
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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    create_directory("the accepted documents", str(cfg.glob.setup.directory_inbox_accepted))

    create_directory("the rejected documents", str(cfg.glob.setup.directory_inbox_rejected))

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create a new file directory if it does not already exist..
# -----------------------------------------------------------------------------
def create_directory(directory_type: str, directory_name: str) -> None:
    """Create a new file directory if it does not already exist.

    Args:
        directory_type (str): Directory type.
        directory_name (str): Directory name - may include a path.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)
        utils.progress_msg(
            f"The file directory for '{directory_type}' " f"was newly created under the name '{directory_name}'",
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise the next action in the database.
# -----------------------------------------------------------------------------
def initialise_action(
    action_code: str = "",
    directory_name: str = "",
    directory_type: str = "",
    file_name: str = "",
    id_parent: int = 0,
) -> db.cls_action.Action:
    """Initialise the next action in the database.

    Args:
        action_code (str, optional): Action code. Defaults to "".
        directory_name (str, optional): Directory name. Defaults to "".
        directory_type (str, optional): Directory type. Defaults to "".
        file_name (str, optional): File name. Defaults to "".
        id_parent (int, optional): File name. Defaults to "".

    Returns:
        type[db.cls_action.Action]: A new Action instance.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name = utils.get_full_name(directory_name, file_name)

    action = db.cls_action.Action(
        action_code=action_code,
        id_run_last=cfg.glob.run.run_id,
        directory_name=directory_name,
        directory_type=directory_type,
        file_name=file_name,
        file_size_bytes=os.path.getsize(full_name),
        id_document=cfg.glob.document.document_id,
        id_parent=id_parent,
        no_pdf_pages=utils.get_pdf_pages_no(full_name),
    )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    return action


# -----------------------------------------------------------------------------
# Initialise the base document in the database.
# -----------------------------------------------------------------------------
def initialise_base(file_path: pathlib.Path) -> None:
    """Initialise the base document in the database.

    Args:
        file_path (pathlib.Path): File.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    cfg.glob.document = db.cls_document.Document(
        action_code_last=cfg.glob.run.run_action_code,
        directory_name=str(file_path.parent),
        file_name=file_path.name,
        id_language=cfg.glob.language.language_id,
        id_run_last=cfg.glob.run.run_id,
    )

    if not cfg.glob.setup.is_ignore_duplicates:
        cfg.glob.document.document_sha256 = utils.compute_sha256(file_path)

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare a new pdf document for further processing..
# -----------------------------------------------------------------------------
def prepare_pdf(file_path: pathlib.Path) -> None:
    """Prepare a new pdf document for further processing.

    Args:
        file_path (pathlib.Path): Inbox file.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    try:
        extracted_text = "".join([page.get_text() for page in fitz.open(file_path)])

        if bool(extracted_text):
            action_code = db.cls_run.Run.ACTION_CODE_PDFLIB
            cfg.glob.language.total_processed_pdflib += 1
            cfg.glob.run.total_processed_pdflib += 1
        else:
            action_code = db.cls_run.Run.ACTION_CODE_PDF2IMAGE
            cfg.glob.language.total_processed_pdf2image += 1
            cfg.glob.run.total_processed_pdf2image += 1

        process_inbox_accepted(action_code)
    except RuntimeError as err:
        process_inbox_rejected(
            db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_NO_PDF_FORMAT,
            ERROR_01_903.replace("{file_name}", cfg.glob.document.document_file_name).replace("{error_msg}", str(err)),
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    if cfg.glob.setup.is_ignore_duplicates:
        utils.progress_msg("Configuration: File duplicates are allowed!")
    else:
        utils.progress_msg("Configuration: File duplicates are not allowed!")

    # Check the inbox file directories and create the missing ones.
    check_and_create_directories()

    utils.reset_statistics_total()

    with cfg.glob.db_core.db_orm_engine.connect() as conn:
        for row in db.cls_language.Language.select_active_languages(conn):
            cfg.glob.language = db.cls_language.Language.from_row(row)
            if os.path.isdir(cfg.glob.language.language_directory_name_inbox):
                process_inbox_language()

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Accept a new document.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_inbox_accepted(action_code: str) -> None:
    """Accept a new document.

    Args:
        action_code (str): Action code.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name_curr = cfg.glob.document.get_full_name()
    full_name_next = utils.get_full_name(cfg.glob.setup.directory_inbox_accepted, cfg.glob.document.get_file_name_next())

    cfg.glob.action_curr = initialise_action(
        action_code=cfg.glob.run.run_action_code,
        directory_name=cfg.glob.language.language_directory_name_inbox,
        directory_type=db.cls_document.Document.DOCUMENT_DIRECTORY_TYPE_INBOX,
        file_name=cfg.glob.document.document_file_name,
    )

    if os.path.exists(full_name_next):
        cfg.glob.action_curr.finalise_error(
            error_code=db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=ERROR_01_906.replace("{full_name}", full_name_next),
        )
    else:
        shutil.move(full_name_curr, full_name_next)

        cfg.glob.action_next = initialise_action(
            action_code=action_code,
            directory_name=cfg.glob.setup.directory_inbox_accepted,
            directory_type=db.cls_document.Document.DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED,
            file_name=cfg.glob.document.get_file_name_next(),
            id_parent=cfg.glob.action_curr.action_id,
        )

        cfg.glob.action_curr.finalise()

        cfg.glob.language.total_processed += 1
        cfg.glob.run.run_total_processed_ok += 1

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


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
    cfg.glob.session = sqlalchemy.orm.Session(cfg.glob.db_core.db_orm_engine)

    initialise_base(file_path)

    if not cfg.glob.setup.is_ignore_duplicates:
        file_name = db.cls_document.Document.select_duplicate_file_name_by_sha256(
            cfg.glob.document.document_id, cfg.glob.document.document_sha256
        )
    else:
        file_name = None

    if not (file_name is None or file_name == ""):
        process_inbox_rejected(
            db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            ERROR_01_905.replace("{file_name}", file_name),
        )
    elif cfg.glob.document.get_file_type() == db.cls_document.Document.DOCUMENT_FILE_TYPE_PDF:
        prepare_pdf(file_path)
    elif cfg.glob.document.get_file_type() in db.cls_document.Document.DOCUMENT_FILE_TYPE_PANDOC:
        process_inbox_accepted(db.cls_run.Run.ACTION_CODE_PANDOC)
        cfg.glob.language.total_processed_pandoc += 1
        cfg.glob.run.total_processed_pandoc += 1
    elif cfg.glob.document.get_file_type() in db.cls_document.Document.DOCUMENT_FILE_TYPE_TESSERACT:
        process_inbox_accepted(db.cls_run.Run.ACTION_CODE_TESSERACT)
        cfg.glob.language.total_processed_tesseract += 1
        cfg.glob.run.total_processed_tesseract += 1
    else:
        process_inbox_rejected(
            db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_EXT,
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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    utils.progress_msg(f"Start of processing for language '{cfg.glob.language.language_iso_language_name}'")

    for file in sorted(utils.get_path_name(cfg.glob.language.language_directory_name_inbox).iterdir()):
        if file.is_file():
            cfg.glob.start_time_document = time.perf_counter_ns()

            if file.name == "README.md":
                utils.progress_msg("Attention: All files with the file name 'README.md' are ignored")
                continue

            cfg.glob.language.total_processed_to_be += 1
            cfg.glob.run.run_total_processed_to_be += 1

            process_inbox_file(file_path=file)

    utils.show_statistics_language()

    utils.progress_msg(
        f"End   of processing for language '{cfg.glob.language.language_iso_language_name}'",
    )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name_curr = cfg.glob.document.get_full_name()
    full_name_next = utils.get_full_name(
        cfg.glob.setup.directory_inbox_rejected,
        cfg.glob.document.get_file_name_next(),
    )

    cfg.glob.action_curr = initialise_action(
        action_code=cfg.glob.run.run_action_code,
        directory_name=cfg.glob.language.language_directory_name_inbox,
        directory_type=db.cls_document.Document.DOCUMENT_DIRECTORY_TYPE_INBOX,
        file_name=cfg.glob.document.document_file_name,
    )

    # Move the document file from directory inbox to directory inbox_rejected - if not yet existing
    if os.path.exists(full_name_next):
        cfg.glob.action_curr.finalise_error(
            error_code=db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=ERROR_01_906.replace("{full_name}", full_name_next),
        )
    else:
        shutil.move(full_name_curr, full_name_next)

        cfg.glob.action_curr.finalise_error(
            error_code=error_code,
            error_msg=error_msg,
        )

    cfg.glob.language.total_erroneous += 1
    cfg.glob.run.run_total_erroneous += 1

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
