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
import comm.utils
import db.dml
import fitz
import sqlalchemy
import sqlalchemy.orm


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
        comm.utils.progress_msg(
            f"The file directory for '{directory_type}' " f"was newly created under the name '{directory_name}'",
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    prepare_document_base(file_path)

    db.dml.insert_document_base()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare the base document data.
# -----------------------------------------------------------------------------
def prepare_document_base(file_path: pathlib.Path) -> None:
    """Prepare the base document data.

    Args:
        file_path (pathlib.Path): File.
    """
    # Example: data\inbox
    cfg.glob.document_directory_name = str(file_path.parent)
    cfg.glob.document_directory_type = cfg.glob.DOCUMENT_DIRECTORY_TYPE_INBOX
    cfg.glob.document_error_code = None

    # Example: pdf_scanned_ok.pdf
    cfg.glob.document_file_name = file_path.name

    # Example: pdf
    cfg.glob.document_file_type = file_path.suffix[1:].lower()

    cfg.glob.document_id_base = None

    cfg.glob.document_id_parent = None
    cfg.glob.document_next_step = None

    if cfg.glob.setup.is_ignore_duplicates:
        cfg.glob.document_sha256 = None
    else:
        cfg.glob.document_sha256 = comm.utils.compute_sha256(file_path)

    cfg.glob.document_status = cfg.glob.DOCUMENT_STATUS_START

    # Example: pdf_scanned_ok
    cfg.glob.document_stem_name = pathlib.PurePath(file_path).stem


# -----------------------------------------------------------------------------
# Prepare the base child document data - from inbox to inbox_accepted.
# -----------------------------------------------------------------------------
def prepare_document_child_accepted() -> None:
    """Prepare the base child document data - from inbox to inbox_accepted."""
    cfg.glob.document_child_child_no = None
    cfg.glob.document_child_error_code = None

    cfg.glob.document_child_file_name = (
        cfg.glob.document_stem_name
        + "_"
        + str(cfg.glob.document_id)
        + "."
        + (
            cfg.glob.document_file_type
            if cfg.glob.document_file_type != cfg.glob.DOCUMENT_FILE_TYPE_TIF
            else cfg.glob.DOCUMENT_FILE_TYPE_TIFF
        )
    )

    cfg.glob.document_child_file_type = cfg.glob.document_file_type
    cfg.glob.document_child_id_base = cfg.glob.document_id
    cfg.glob.document_child_id_parent = cfg.glob.document_id
    cfg.glob.document_child_next_step = None
    cfg.glob.document_child_status = cfg.glob.DOCUMENT_STATUS_START

    cfg.glob.document_child_stem_name = cfg.glob.document_stem_name + "_" + str(cfg.glob.document_id)


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

        prepare_document_child_accepted()

        if bool(extracted_text):
            next_step: str = cfg.glob.DOCUMENT_STEP_PDFLIB
            cfg.glob.language_ok_processed_pdflib += 1
            cfg.glob.total_ok_processed_pdflib += 1
        else:
            next_step: str = cfg.glob.DOCUMENT_STEP_PDF2IMAGE
            cfg.glob.language_ok_processed_pdf2image += 1
            cfg.glob.total_ok_processed_pdf2image += 1

        process_inbox_accepted(next_step)
    except RuntimeError as err:
        process_inbox_rejected(
            cfg.glob.DOCUMENT_ERROR_CODE_REJ_NO_PDF_FORMAT,
            cfg.glob.ERROR_01_903.replace("{source_file}", cfg.glob.document_file_name).replace(
                "{error_msg}", str(err)
            ),
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
        comm.utils.progress_msg("Configuration: File duplicates are allowed!")
    else:
        comm.utils.progress_msg("Configuration: File duplicates are not allowed!")

    # Check the inbox file directories and create the missing ones.
    check_and_create_directories()

    comm.utils.reset_statistics_total()

    dbt = sqlalchemy.Table(
        cfg.glob.DBT_LANGUAGE,
        cfg.glob.db_orm_metadata,
        autoload_with=cfg.glob.db_orm_engine,
    )

    with cfg.glob.db_orm_engine.connect() as conn:
        for row in db.dml.select_language(conn, dbt):
            cfg.glob.language_id = row.id
            cfg.glob.language_directory_inbox = row.directory_name_inbox
            cfg.glob.language_iso_language_name = row.iso_language_name

            if cfg.glob.language_directory_inbox is None:
                cfg.glob.language_directory_inbox = pathlib.Path(
                    str(cfg.glob.setup.directory_inbox),
                    cfg.glob.language_iso_language_name.lower(),
                )

            if os.path.isdir(pathlib.Path(str(cfg.glob.language_directory_inbox))):
                process_inbox_language()

        conn.close()

    comm.utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Accept a new document.
# -----------------------------------------------------------------------------
def process_inbox_accepted(next_step: str) -> None:
    """Accept a new document.

    Args:
        next_step (str): Next processing step.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    cfg.glob.document_child_directory_name = cfg.glob.setup.directory_inbox_accepted
    cfg.glob.document_child_directory_type = cfg.glob.DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED
    cfg.glob.document_child_next_step = next_step
    cfg.glob.document_child_status = cfg.glob.DOCUMENT_STATUS_START

    source_file = os.path.join(cfg.glob.document_directory_name, cfg.glob.document_file_name)
    target_file = os.path.join(cfg.glob.document_child_directory_name, cfg.glob.document_child_file_name)

    if os.path.exists(target_file):
        db.dml.update_document_error(
            document_id=cfg.glob.document_id,
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=cfg.glob.ERROR_01_906.replace("{file_name}", target_file),
        )
    else:
        shutil.move(source_file, target_file)

        db.dml.insert_document_child()

        duration_ns = db.dml.update_document_statistics(
            document_id=cfg.glob.document_id, status=cfg.glob.DOCUMENT_STATUS_END
        )

        if cfg.glob.setup.is_verbose:
            comm.utils.progress_msg(
                f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                f"Document: {cfg.glob.document_id:6d} "
                f"[{db.dml.select_document_file_name_id(cfg.glob.document_id)}]"
            )

        cfg.glob.language_ok_processed += 1
        cfg.glob.total_ok_processed += 1

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the next inbox file.
# -----------------------------------------------------------------------------
def process_inbox_file(file_path: pathlib.Path) -> None:
    """Process the next inbox file.

    Args:
        file_path (pathlib.Path): Inbox file.
    """
    cfg.glob.session = sqlalchemy.orm.Session(cfg.glob.db_orm_engine)

    initialise_document_base(file_path)

    if not cfg.glob.setup.is_ignore_duplicates:
        file_name = db.dml.select_document_file_name_sha256(cfg.glob.document_id, cfg.glob.document_sha256)
    else:
        file_name = None

    if file_name is not None:
        process_inbox_rejected(
            cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            cfg.glob.ERROR_01_905.replace("{file_name}", file_name),
        )
    elif cfg.glob.document_file_type == cfg.glob.DOCUMENT_FILE_TYPE_PDF:
        prepare_pdf(file_path)
    elif cfg.glob.document_file_type in cfg.glob.DOCUMENT_FILE_TYPE_PANDOC:
        prepare_document_child_accepted()
        process_inbox_accepted(cfg.glob.DOCUMENT_STEP_PANDOC)
        cfg.glob.language_ok_processed_pandoc += 1
        cfg.glob.total_ok_processed_pandoc += 1
    elif cfg.glob.document_file_type in cfg.glob.DOCUMENT_FILE_TYPE_TESSERACT:
        prepare_document_child_accepted()
        process_inbox_accepted(cfg.glob.DOCUMENT_STEP_TESSERACT)
        cfg.glob.language_ok_processed_tesseract += 1
        cfg.glob.total_ok_processed_tesseract += 1
    else:
        process_inbox_rejected(
            cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_EXT,
            cfg.glob.ERROR_01_901.replace("{extension}", file_path.suffix[1:]),
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
    comm.utils.progress_msg(f"Start of processing for language '{cfg.glob.language_iso_language_name}'")

    comm.utils.reset_statistics_language()

    for file in sorted(pathlib.Path(cfg.glob.language_directory_inbox).iterdir()):
        if file.is_file():
            cfg.glob.start_time_document = time.perf_counter_ns()

            if file.name == "README.md":
                comm.utils.progress_msg("Attention: All files with the file name 'README.md' are ignored")
                continue

            cfg.glob.language_to_be_processed += 1
            cfg.glob.total_to_be_processed += 1

            process_inbox_file(file)

    comm.utils.show_statistics_language()

    comm.utils.progress_msg(
        f"End   of processing for language '{cfg.glob.language_iso_language_name}'",
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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    prepare_document_child_accepted()

    cfg.glob.document_child_directory_name = cfg.glob.setup.directory_inbox_rejected
    cfg.glob.document_child_directory_type = cfg.glob.DOCUMENT_DIRECTORY_TYPE_INBOX_REJECTED
    cfg.glob.document_child_error_code = error_code
    cfg.glob.document_child_status = cfg.glob.DOCUMENT_STATUS_ERROR

    source_file = os.path.join(cfg.glob.document_directory_name, cfg.glob.document_file_name)
    target_file = os.path.join(cfg.glob.document_child_directory_name, cfg.glob.document_child_file_name)

    # Move the document file from directory inbox to directory inbox_rejected - if not yet existing
    if os.path.exists(target_file):
        db.dml.update_document_error(
            document_id=cfg.glob.document_id,
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=cfg.glob.ERROR_01_906.replace("{file_name}", target_file),
        )
    else:
        shutil.move(source_file, target_file)

        db.dml.insert_document_child()

        db.dml.update_document_error(
            document_id=cfg.glob.document_id,
            error_code=error_code,
            error_msg=error_msg,
        )

        cfg.glob.language_erroneous += 1

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
