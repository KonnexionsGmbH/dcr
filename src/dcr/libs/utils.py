"""Module libs.utils: Helper functions."""
import datetime
import hashlib
import os
import pathlib
import sys
import traceback
from typing import Tuple

import db.cfg
import db.driver
import db.orm.dml
import libs.cfg
import libs.utils
from sqlalchemy import Table
from sqlalchemy.engine import Row


# -----------------------------------------------------------------------------
# Check the inbox file directories.
# -----------------------------------------------------------------------------
def check_directories() -> None:
    """Check the inbox file directories.

    The file directory inbox_accepted must exist.
    """
    if not os.path.isdir(libs.cfg.directory_inbox_accepted):
        libs.utils.terminate_fatal(
            f"The inbox_accepted directory with the name "
            f"'{str(libs.cfg.directory_inbox_accepted)}' "
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
    if not libs.cfg.is_delete_auxiliary_files:
        return

    # Don't remove the base document !!!
    if file_name == db.orm.dml.select_document_base_file_name():
        return

    if os.path.isfile(file_name):
        os.remove(file_name)
        libs.utils.progress_msg(f"Auxiliary file '{file_name}' deleted")


# -----------------------------------------------------------------------------
# Finalise the file processing.
# -----------------------------------------------------------------------------
def finalize_file_processing() -> None:
    """Finalise the file processing."""
    db.orm.dml.update_document_statistics(
        document_id=libs.cfg.document_id, status=db.cfg.DOCUMENT_STATUS_END
    )

    libs.cfg.total_ok_processed += 1


# -----------------------------------------------------------------------------
# Prepare the document data for the next step.
# -----------------------------------------------------------------------------
def prepare_document_4_next_step(next_file_type: str, next_step: str) -> None:
    """Prepare the document data for the next step.

    Args:
        next_file_type (str): File type of next document
        next_step (str): Next processing step
    """
    libs.cfg.document_child_directory_name = libs.cfg.document_directory_name
    libs.cfg.document_child_directory_type = libs.cfg.document_directory_type
    libs.cfg.document_child_error_code = None
    libs.cfg.document_child_file_type = next_file_type
    libs.cfg.document_child_id_base = libs.cfg.document_id_base
    libs.cfg.document_child_id_parent = libs.cfg.document_id
    libs.cfg.document_child_language_id = libs.cfg.document_language_id
    libs.cfg.document_child_next_step = next_step
    libs.cfg.document_child_status = db.cfg.DOCUMENT_STATUS_START


# -----------------------------------------------------------------------------
# Prepare the source and target file names.
# -----------------------------------------------------------------------------
def prepare_file_names(file_extension: str = db.cfg.DOCUMENT_FILE_TYPE_PDF) -> Tuple[str, str]:
    """Prepare the source and target file names.

    Args:
        file_extension (str): File extension, default value 'pdf'.

    Returns:
        Tuple(str,str): Source file name and target file name.
    """
    source_file = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    target_file = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_stem_name + "." + file_extension,
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
    if libs.cfg.is_verbose:
        final_msg: str = (
            libs.cfg.LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg + "."
        )

        print(final_msg)

        libs.cfg.logger.debug(final_msg)


# -----------------------------------------------------------------------------
# Create a progress message: connected to database.
# -----------------------------------------------------------------------------
def progress_msg_connected() -> None:
    """Create a progress message: connected to database."""
    if libs.cfg.is_verbose:
        print("")
        progress_msg(
            f"User '{db.cfg.db_current_user}' is now connected "
            f"to database '{db.cfg.db_current_database}'"
        )


# -----------------------------------------------------------------------------
# Create a progress message: disconnected from database.
# -----------------------------------------------------------------------------
def progress_msg_disconnected() -> None:
    """Create a progress message: disconnected from database."""
    if libs.cfg.is_verbose:
        if db.cfg.db_current_database is None and db.cfg.db_current_user is None:
            print("")
            libs.utils.progress_msg("Database is now disconnected")
            return

        database = (
            libs.cfg.INFORMATION_NOT_YET_AVAILABLE
            if db.cfg.db_current_database is None
            else db.cfg.db_current_database
        )
        user = (
            libs.cfg.INFORMATION_NOT_YET_AVAILABLE
            if db.cfg.db_current_user is None
            else db.cfg.db_current_user
        )

        print("")
        libs.utils.progress_msg(f"User '{user}' is now disconnected from database '{database}'")

        db.cfg.db_current_database = None
        db.cfg.db_current_user = None


# -----------------------------------------------------------------------------
# Create a progress message with empty line before.
# -----------------------------------------------------------------------------
def progress_msg_empty_before(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    if libs.cfg.is_verbose:
        print("")
        progress_msg(msg)


# -----------------------------------------------------------------------------
# Reset the language related statistic counters.
# -----------------------------------------------------------------------------
def reset_statistics_language() -> None:
    """Reset the language related statistic counters."""
    libs.cfg.language_erroneous = 0
    libs.cfg.language_ok_processed = 0
    libs.cfg.language_ok_processed_pandoc = 0
    libs.cfg.language_ok_processed_pdf2image = 0
    libs.cfg.language_ok_processed_pdflib = 0
    libs.cfg.language_ok_processed_tesseract = 0
    libs.cfg.language_to_be_processed = 0


# -----------------------------------------------------------------------------
# Reset the total statistic counters.
# -----------------------------------------------------------------------------
def reset_statistics_total() -> None:
    """Reset the total statistic counters."""
    libs.cfg.total_erroneous = 0
    libs.cfg.total_generated = 0
    libs.cfg.total_ok_processed = 0
    libs.cfg.total_ok_processed_pandoc = 0
    libs.cfg.total_ok_processed_pdf2image = 0
    libs.cfg.total_ok_processed_pdflib = 0
    libs.cfg.total_ok_processed_tesseract = 0
    libs.cfg.total_status_error = 0
    libs.cfg.total_status_ready = 0
    libs.cfg.total_to_be_processed = 0


# -----------------------------------------------------------------------------
# Prepare the selection of the documents to be processed.
# -----------------------------------------------------------------------------
def select_document_prepare() -> Table:
    """Prepare the selection of the documents to be processed.

    Returns:
        Table: Database table document,
    """
    # Check the inbox file directories.
    libs.utils.check_directories()

    return Table(
        db.cfg.DBT_DOCUMENT,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )


# -----------------------------------------------------------------------------
# Show the language related statistics of the run.
# -----------------------------------------------------------------------------
def show_statistics_language() -> None:
    """Show the language related statistics of the run."""
    libs.utils.progress_msg("===============================> Summary Language")
    libs.utils.progress_msg(
        f"Number documents to be processed:          {libs.cfg.language_to_be_processed:6d}"
    )

    if libs.cfg.language_to_be_processed > 0:
        libs.utils.progress_msg(
            f"Number documents accepted - "
            f"Pandoc:        {libs.cfg.language_ok_processed_pandoc:6d}"
        )
        libs.utils.progress_msg(
            f"Number documents accepted - "
            f"pdf2image:     {libs.cfg.language_ok_processed_pdf2image:6d}"
        )
        libs.utils.progress_msg(
            f"Number documents accepted - "
            f"PDFlib TET:    {libs.cfg.language_ok_processed_pdflib:6d}"
        )
        libs.utils.progress_msg(
            f"Number documents accepted - "
            f"Tesseract OCR: {libs.cfg.language_ok_processed_tesseract:6d}"
        )
        libs.utils.progress_msg(
            f"Number documents accepted - " f"Total:         {libs.cfg.language_ok_processed:6d}"
        )
        libs.utils.progress_msg(
            f"Number documents rejected:                 {libs.cfg.language_erroneous:6d}"
        )


# -----------------------------------------------------------------------------
# Show the total statistics of the run.
# -----------------------------------------------------------------------------
def show_statistics_total() -> None:
    """Show the total statistics of the run."""
    libs.utils.progress_msg("==================================> Summary Total")
    libs.utils.progress_msg(
        f"Number documents to be processed:          {libs.cfg.total_to_be_processed:6d}"
    )

    if libs.cfg.total_to_be_processed > 0:
        if libs.cfg.total_status_ready > 0 or libs.cfg.total_status_error > 0:
            libs.utils.progress_msg(
                f"Number with document status ready:         {libs.cfg.total_status_ready:6d}"
            )
            libs.utils.progress_msg(
                f"Number with document status error:         {libs.cfg.total_status_error:6d}"
            )

        if libs.cfg.run_action == libs.cfg.RUN_ACTION_PROCESS_INBOX:
            libs.utils.progress_msg(
                f"Number documents accepted - "
                f"Pandoc:        {libs.cfg.total_ok_processed_pandoc:6d}"
            )
            libs.utils.progress_msg(
                f"Number documents accepted - "
                f"pdf2image:     {libs.cfg.total_ok_processed_pdf2image:6d}"
            )
            libs.utils.progress_msg(
                f"Number documents accepted - "
                f"PDFlib TET:    {libs.cfg.total_ok_processed_pdflib:6d}"
            )
            libs.utils.progress_msg(
                f"Number documents accepted - "
                f"Tesseract OCR: {libs.cfg.total_ok_processed_tesseract:6d}"
            )
            libs.utils.progress_msg(
                "Number documents accepted - " + f"Total:         {libs.cfg.total_ok_processed:6d}"
            )
        elif libs.cfg.run_action == libs.cfg.RUN_ACTION_TEXT_FROM_PDF:
            libs.utils.progress_msg(
                f"Number documents extracted:                {libs.cfg.total_ok_processed:6d}"
            )
        else:
            libs.utils.progress_msg(
                f"Number documents converted:                {libs.cfg.total_ok_processed:6d}"
            )

        if libs.cfg.total_generated > 0:
            libs.utils.progress_msg(
                f"Number documents generated:                {libs.cfg.total_generated:6d}"
            )

        if libs.cfg.run_action == libs.cfg.RUN_ACTION_PROCESS_INBOX:
            libs.utils.progress_msg(
                f"Number documents rejected:                 {libs.cfg.total_erroneous:6d}"
            )
        else:
            libs.utils.progress_msg(
                f"Number documents erroneous:                {libs.cfg.total_erroneous:6d}"
            )


# -----------------------------------------------------------------------------
# Start document processing.
# -----------------------------------------------------------------------------
def start_document_processing(document: Row) -> None:
    """Start document processing.

    Args:
        document (Row):       Database row document.
    """
    libs.cfg.total_to_be_processed += 1

    libs.cfg.document_child_child_no = document.child_no
    libs.cfg.document_directory_name = document.directory_name
    libs.cfg.document_directory_type = document.directory_type
    libs.cfg.document_file_name = document.file_name
    libs.cfg.document_file_type = document.file_type
    libs.cfg.document_id = document.id
    libs.cfg.document_id_base = document.document_id_base
    libs.cfg.document_id_parent = document.document_id_parent
    libs.cfg.document_language_id = document.language_id
    libs.cfg.document_status = document.status
    libs.cfg.document_stem_name = document.stem_name

    db.orm.dml.update_dbt_id(
        db.cfg.DBT_DOCUMENT,
        libs.cfg.document_id,
        {
            db.cfg.DBC_STATUS: db.cfg.DOCUMENT_STATUS_START,
        },
    )

    if libs.cfg.document_status == db.cfg.DOCUMENT_STATUS_ERROR:
        # not testable
        libs.cfg.total_status_error += 1
    else:
        libs.cfg.total_status_ready += 1


# -----------------------------------------------------------------------------
# Convert a string into a file path.
# -----------------------------------------------------------------------------
def str_2_path(param: str) -> pathlib.Path:
    """Convert a string into a file path.

    Args:
        param (str): text parameter.

    Returns:
        pathlib.Path: File path.
    """
    return pathlib.Path(os.path.join(os.getcwd(), *param.split("/" if "/" in param else "\\")))


# -----------------------------------------------------------------------------
# Terminate the application immediately.
# -----------------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message.
    """
    print("")
    print(libs.cfg.LOGGER_FATAL_HEAD)
    print(libs.cfg.LOGGER_FATAL_HEAD, error_msg, libs.cfg.LOGGER_FATAL_TAIL, sep="")
    print(libs.cfg.LOGGER_FATAL_HEAD)
    libs.cfg.logger.critical(
        "%s%s%s", libs.cfg.LOGGER_FATAL_HEAD, error_msg, libs.cfg.LOGGER_FATAL_TAIL
    )

    traceback.print_exc(chain=True)

    db.driver.disconnect_db()

    sys.exit(1)
