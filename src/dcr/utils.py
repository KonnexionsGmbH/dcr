"""Module utils: Helper functions."""
import datetime
import hashlib
import os
import pathlib
import sys
import traceback
from typing import Tuple

import cfg.glob
import db.dml
import db.driver
import PyPDF2
import PyPDF2.utils
import sqlalchemy.engine
import utils


# -----------------------------------------------------------------------------
# Check the inbox file directories.
# -----------------------------------------------------------------------------
def check_directories() -> None:
    """Check the inbox file directories.

    The file directory inbox_accepted must exist.
    """
    if not os.path.isdir(cfg.glob.setup.directory_inbox_accepted):
        utils.terminate_fatal(
            f"The inbox_accepted directory with the name "
            f"'{str(cfg.glob.setup.directory_inbox_accepted)}' "
            f"does not exist - error={str(OSError)}",
        )


# -----------------------------------------------------------------------------
# Compute the SHA256 hash string of a file.
# -----------------------------------------------------------------------------
def compute_sha256(file: pathlib.Path) -> str:
    """Compute the SHA256 hash string of a file.

    Args:
        file (: pathlib.Path): File.

    Returns:
        str: SHA256 hash string.
    """
    sha256_hash = hashlib.sha256()

    with open(file, "rb") as file_content:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file_content.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


# -----------------------------------------------------------------------------
# Delete the given auxiliary file.
# -----------------------------------------------------------------------------
def delete_auxiliary_file(file_name: str) -> None:
    """Delete the given auxiliary file.

    Args:
        file_name (str): File name.
    """
    if not cfg.glob.setup.is_delete_auxiliary_files:
        return

    # Don't remove the base document !!!
    if file_name == get_full_name(cfg.glob.action_curr.action_directory_name, utils.get_file_name_original):
        return

    if os.path.isfile(file_name):
        os.remove(file_name)
        utils.progress_msg(f"Auxiliary file '{file_name}' deleted")


# -----------------------------------------------------------------------------
# Finalise the file processing.
# -----------------------------------------------------------------------------
def finalize_file_processing() -> int:
    """Finalise the file processing."""
    duration_ns = db.dml.update_document_statistics(
        document_id=cfg.glob.base.base_id, status=cfg.glob.DOCUMENT_STATUS_END
    )

    cfg.glob.run.run_total_processed_ok += 1

    return duration_ns


# -----------------------------------------------------------------------------
# Get the file name of the original document.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def get_file_name_original() -> str:
    """Get the file name of the original document.

    Returns:
        str: File name of the original document.
    """
    return (
        cfg.glob.base.get_stem_name()
        + "_"
        + str(cfg.glob.base.base_id)
        + "."
        + (
            cfg.glob.base.get_file_type()
            if cfg.glob.base.get_file_type() != cfg.glob.DOCUMENT_FILE_TYPE_TIF
            else cfg.glob.DOCUMENT_FILE_TYPE_TIFF
        )
    )


# -----------------------------------------------------------------------------
# Get the file type from a file name.
# -----------------------------------------------------------------------------
def get_file_type(file_name: pathlib.Path | str | None) -> str:
    """Get the file type from a file name.

    Args:
        file_name (pathlib.Path | str | None): File name or file path.

    Returns:
        str | None: File type.
    """
    if file_name is None:
        return ""

    if isinstance(file_name, str):
        file_name = pathlib.Path(file_name)

    return file_name.suffix[1:].lower()


# -----------------------------------------------------------------------------
# Get the full file from a directory name or path and a file name or path.
# -----------------------------------------------------------------------------
def get_full_name(directory_name: pathlib.Path | str | None, file_name: pathlib.Path | str | None) -> str:
    """Get the full file from a directory name or path and a file name or path.

    Args:
        directory_name (pathlib.Path | str | None): Directory name or directory path.
        file_name (pathlib.Path | str | None): File name or file path.

    Returns:
        str: Full file name.
    """
    if directory_name is None and file_name is None:
        return ""

    if isinstance(directory_name, str):
        directory_name = pathlib.Path(directory_name)

    if isinstance(file_name, str):
        file_name = pathlib.Path(file_name)

    return os.path.join(directory_name, file_name)


# -----------------------------------------------------------------------------
# Determine the number of pages in a pdf document.
# -----------------------------------------------------------------------------
def get_pdf_pages_no(
    file_name: str,
) -> int:
    """Determine the number of pages in a pdf document.

    Args:
        file_name (str): File name.

    Returns:
        int: The number of pages found.
    """
    if get_file_type(file_name) != cfg.glob.DOCUMENT_FILE_TYPE_PDF:
        return -1

    try:
        return PyPDF2.PdfFileReader(file_name).numPages
    except PyPDF2.utils.PdfReadError:
        return -1


# -----------------------------------------------------------------------------
# Get the stem name from a file name.
# -----------------------------------------------------------------------------
def get_stem_name(file_name: pathlib.Path | str | None) -> str:
    """Get the stem name from a file name.

    Args:
        file_name (pathlib.Path | str | None): File name or file path.

    Returns:
        str | None: Stem name.
    """
    if file_name is None:
        return ""

    if isinstance(file_name, str):
        file_name = pathlib.Path(file_name)

    return file_name.stem


# -----------------------------------------------------------------------------
# Prepare the document data for the next step.
# -----------------------------------------------------------------------------
def prepare_document_4_next_step(next_file_type: str, next_step: str) -> None:
    """Prepare the document data for the next step.

    Args:
        next_file_type (str): File type of next document
        next_step (str): Next processing step
    """
    cfg.glob.document_child_directory_name = cfg.glob.document_directory_name
    cfg.glob.document_child_directory_type = cfg.glob.document_directory_type
    cfg.glob.document_child_error_code = None
    cfg.glob.document_child_file_type = next_file_type
    cfg.glob.document_child_id_base = cfg.glob.base.base_id_base
    cfg.glob.document_child_id_parent = cfg.glob.base.base_id
    cfg.glob.document_child_id_language = cfg.glob.base.base_id_language
    cfg.glob.document_child_next_step = next_step
    cfg.glob.document_child_status = cfg.glob.DOCUMENT_STATUS_START


# -----------------------------------------------------------------------------
# Prepare the source and target file names.
# -----------------------------------------------------------------------------
def prepare_file_names(
    file_extension: str,
) -> Tuple[str, str]:
    """Prepare the source and target file names.

    Args:
        file_extension (str): File extension, default value 'pdf'.

    Returns:
        Tuple(str,str): Source file name and target file name.
    """
    source_file = os.path.join(
        cfg.glob.document_directory_name,
        cfg.glob.document_file_name,
    )

    target_file = os.path.join(
        cfg.glob.document_directory_name,
        cfg.glob.document_stem_name + "." + file_extension,
    )

    return source_file, target_file


# -----------------------------------------------------------------------------
# Create a progress message.
# -----------------------------------------------------------------------------
def progress_msg(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    if cfg.glob.setup.is_verbose:
        progress_msg_core(msg)


# -----------------------------------------------------------------------------
# Create a progress message: connected to database.
# -----------------------------------------------------------------------------
def progress_msg_connected() -> None:
    """Create a progress message: connected to database."""
    if cfg.glob.setup.is_verbose:
        print("")
        progress_msg(
            f"User '{cfg.glob.db_current_user}' is now connected " f"to database '{cfg.glob.db_current_database}'"
        )


# -----------------------------------------------------------------------------
# Create a progress message.
# -----------------------------------------------------------------------------
def progress_msg_core(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    final_msg: str = cfg.glob.LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg + "."

    print(final_msg)

    cfg.glob.logger.debug(final_msg)


# -----------------------------------------------------------------------------
# Create a progress message: disconnected from database.
# -----------------------------------------------------------------------------
def progress_msg_disconnected() -> None:
    """Create a progress message: disconnected from database."""
    if cfg.glob.setup.is_verbose:
        if cfg.glob.db_current_database is None and cfg.glob.db_current_user is None:
            print("")
            utils.progress_msg("Database is now disconnected")
            return

        database = (
            cfg.glob.INFORMATION_NOT_YET_AVAILABLE
            if cfg.glob.db_current_database is None
            else cfg.glob.db_current_database
        )

        user = cfg.glob.INFORMATION_NOT_YET_AVAILABLE if cfg.glob.db_current_user is None else cfg.glob.db_current_user

        print("")
        utils.progress_msg(f"User '{user}' is now disconnected from database '{database}'")

        cfg.glob.db_current_database = None
        cfg.glob.db_current_user = None


# -----------------------------------------------------------------------------
# Create a progress message with empty line before.
# -----------------------------------------------------------------------------
def progress_msg_empty_before(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    if cfg.glob.setup.is_verbose:
        print("")
        progress_msg(msg)


# -----------------------------------------------------------------------------
# Create a line_type progress message.
# -----------------------------------------------------------------------------
def progress_msg_line_type(msg: str) -> None:
    """Create a line_type progress message.

    Args:
        msg (str): Progress message.
    """
    if cfg.glob.setup.is_verbose_line_type:
        progress_msg_core(msg)


# -----------------------------------------------------------------------------
# Reset the total statistic counters.
# -----------------------------------------------------------------------------
def reset_statistics_total() -> None:
    """Reset the total statistic counters."""
    cfg.glob.run.run_total_erroneous = 0
    cfg.glob.run.run_total_processed_ok = 0
    cfg.glob.run.run_total_processed_to_be = 0

    cfg.glob.run.total_generated = 0
    cfg.glob.run.total_processed_pandoc = 0
    cfg.glob.run.total_processed_pdf2image = 0
    cfg.glob.run.total_processed_pdflib = 0
    cfg.glob.run.total_processed_tesseract = 0
    cfg.glob.run.total_status_error = 0
    cfg.glob.run.total_status_ready = 0


# -----------------------------------------------------------------------------
# Show the language related statistics of the run.
# -----------------------------------------------------------------------------
def show_statistics_language() -> None:
    """Show the language related statistics of the run."""
    utils.progress_msg("===============================> Summary Language")
    utils.progress_msg(f"Number documents to be processed:          {cfg.glob.language.total_processed_to_be:6d}")

    if cfg.glob.language.total_processed_to_be > 0:
        utils.progress_msg(
            f"Number documents accepted - " f"Pandoc:        {cfg.glob.language.total_processed_pandoc:6d}"
        )
        utils.progress_msg(
            f"Number documents accepted - " f"pdf2image:     {cfg.glob.language.total_processed_pdf2image:6d}"
        )
        utils.progress_msg(
            f"Number documents accepted - " f"PDFlib TET:    {cfg.glob.language.total_processed_pdflib:6d}"
        )
        utils.progress_msg(
            f"Number documents accepted - " f"Tesseract OCR: {cfg.glob.language.total_processed_tesseract:6d}"
        )
        utils.progress_msg(f"Number documents accepted - " f"Total:         {cfg.glob.language.total_processed:6d}")
        utils.progress_msg(f"Number documents rejected:                 {cfg.glob.language.total_erroneous:6d}")


# -----------------------------------------------------------------------------
# Show the total statistics of the run.
# -----------------------------------------------------------------------------
def show_statistics_total() -> None:
    """Show the total statistics of the run."""
    utils.progress_msg("==================================> Summary Total")
    utils.progress_msg(f"Number documents to be processed:          {cfg.glob.run.run_total_processed_to_be:6d}")

    if cfg.glob.run.run_total_processed_to_be > 0:
        if cfg.glob.run.total_status_ready > 0 or cfg.glob.run.total_status_error > 0:
            utils.progress_msg(f"Number with document status ready:         {cfg.glob.run.total_status_ready:6d}")
            utils.progress_msg(f"Number with document status error:         {cfg.glob.run.total_status_error:6d}")

        # noinspection PyUnresolvedReferences
        if cfg.glob.run.run_action_code == db.cls_run.Run.ACTION_CODE_INBOX:
            utils.progress_msg(
                f"Number documents accepted - " f"Pandoc:        {cfg.glob.run.total_processed_pandoc:6d}"
            )
            utils.progress_msg(
                f"Number documents accepted - " f"pdf2image:     {cfg.glob.run.total_processed_pdf2image:6d}"
            )
            utils.progress_msg(
                f"Number documents accepted - " f"PDFlib TET:    {cfg.glob.run.total_processed_pdflib:6d}"
            )
            utils.progress_msg(
                f"Number documents accepted - " f"Tesseract OCR: {cfg.glob.run.total_processed_tesseract:6d}"
            )
            utils.progress_msg(
                "Number documents accepted - " + f"Total:         {cfg.glob.run.run_total_processed_ok:6d}"
            )
        elif cfg.glob.run.run_action_code == db.cls_run.Run.ACTION_CODE_PDFLIB:
            utils.progress_msg(f"Number documents extracted:                {cfg.glob.run.run_total_processed_ok:6d}")
        else:
            utils.progress_msg(f"Number documents converted:                {cfg.glob.run.run_total_processed_ok:6d}")

        if cfg.glob.run.total_generated > 0:
            utils.progress_msg(f"Number documents generated:                {cfg.glob.run.total_generated:6d}")

        # noinspection PyUnresolvedReferences
        if cfg.glob.run.run_action_code == db.cls_run.Run.ACTION_CODE_INBOX:
            utils.progress_msg(f"Number documents rejected:                 {cfg.glob.run.run_total_erroneous:6d}")
        else:
            utils.progress_msg(f"Number documents erroneous:                {cfg.glob.run.run_total_erroneous:6d}")


# -----------------------------------------------------------------------------
# Start document processing.
# -----------------------------------------------------------------------------
def start_document_processing(document: sqlalchemy.engine.Row) -> None:
    """Start document processing.

    Args:
        document (Row):       Database row document.
    """
    cfg.glob.run.run_total_processed_to_be += 1

    cfg.glob.document_child_no_children = document.no_children
    cfg.glob.document_directory_name = document.directory_name
    cfg.glob.document_directory_type = document.directory_type
    cfg.glob.document_file_name = document.file_name
    cfg.glob.document_file_type = document.file_type
    cfg.glob.base.base_id = document.id
    cfg.glob.base.base_id_base = document.document_id_base
    cfg.glob.base.base_id_parent = document.document_id_parent
    cfg.glob.base.base_id_language = document.id_language
    cfg.glob.document_status = document.status
    cfg.glob.document_stem_name = document.stem_name

    db.dml.update_dbt_id(
        cfg.glob.DBT_DOCUMENT,
        cfg.glob.base.base_id,
        {
            cfg.glob.DBC_STATUS: cfg.glob.DOCUMENT_STATUS_START,
        },
    )

    if cfg.glob.document_status == cfg.glob.DOCUMENT_STATUS_ERROR:
        # not testable
        cfg.glob.run.total_status_error += 1
    else:
        cfg.glob.run.total_status_ready += 1


# -----------------------------------------------------------------------------
# Terminate the application immediately.
# -----------------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message.
    """
    db.driver.disconnect_db()

    terminate_fatal_setup(error_msg)


# -----------------------------------------------------------------------------
# Terminate the application immediately.
# -----------------------------------------------------------------------------
def terminate_fatal_setup(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message.
    """
    print("")
    print(cfg.glob.LOGGER_FATAL_HEAD)
    print(cfg.glob.LOGGER_FATAL_HEAD, error_msg, cfg.glob.LOGGER_FATAL_TAIL, sep="")
    print(cfg.glob.LOGGER_FATAL_HEAD)
    cfg.glob.logger.critical("%s%s%s", cfg.glob.LOGGER_FATAL_HEAD, error_msg, cfg.glob.LOGGER_FATAL_TAIL)

    traceback.print_exc(chain=True)

    sys.exit(1)
