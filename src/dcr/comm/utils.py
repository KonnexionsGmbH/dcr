"""Module comm.utils: Helper functions."""
import datetime
import hashlib
import os
import pathlib
import sys
import traceback
import typing

import cfg.glob
import comm.utils
import db.dml
import db.driver
import sqlalchemy.engine


# -----------------------------------------------------------------------------
# Check the inbox file directories.
# -----------------------------------------------------------------------------
def check_directories() -> None:
    """Check the inbox file directories.

    The file directory inbox_accepted must exist.
    """
    if not os.path.isdir(cfg.glob.setup.directory_inbox_accepted):
        comm.utils.terminate_fatal(
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
    if file_name == db.dml.select_document_base_file_name():
        return

    if os.path.isfile(file_name):
        os.remove(file_name)
        comm.utils.progress_msg(f"Auxiliary file '{file_name}' deleted")


# -----------------------------------------------------------------------------
# Finalise the file processing.
# -----------------------------------------------------------------------------
def finalize_file_processing() -> int:
    """Finalise the file processing."""
    duration_ns = db.dml.update_document_statistics(
        document_id=cfg.glob.document_id, status=cfg.glob.DOCUMENT_STATUS_END
    )

    cfg.glob.total_ok_processed += 1

    return duration_ns


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
    cfg.glob.document_child_id_base = cfg.glob.document_id_base
    cfg.glob.document_child_id_parent = cfg.glob.document_id
    cfg.glob.document_child_language_id = cfg.glob.document_language_id
    cfg.glob.document_child_next_step = next_step
    cfg.glob.document_child_status = cfg.glob.DOCUMENT_STATUS_START


# -----------------------------------------------------------------------------
# Prepare the source and target file names.
# -----------------------------------------------------------------------------
def prepare_file_names(
    file_extension: str,
) -> typing.Tuple[str, str]:
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
            comm.utils.progress_msg("Database is now disconnected")
            return

        database = (
            cfg.glob.INFORMATION_NOT_YET_AVAILABLE
            if cfg.glob.db_current_database is None
            else cfg.glob.db_current_database
        )
        user = cfg.glob.INFORMATION_NOT_YET_AVAILABLE if cfg.glob.db_current_user is None else cfg.glob.db_current_user

        print("")
        comm.utils.progress_msg(f"User '{user}' is now disconnected from database '{database}'")

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
# Reset the language related statistic counters.
# -----------------------------------------------------------------------------
def reset_statistics_language() -> None:
    """Reset the language related statistic counters."""
    cfg.glob.language_erroneous = 0
    cfg.glob.language_ok_processed = 0
    cfg.glob.language_ok_processed_pandoc = 0
    cfg.glob.language_ok_processed_pdf2image = 0
    cfg.glob.language_ok_processed_pdflib = 0
    cfg.glob.language_ok_processed_tesseract = 0
    cfg.glob.language_to_be_processed = 0


# -----------------------------------------------------------------------------
# Reset the total statistic counters.
# -----------------------------------------------------------------------------
def reset_statistics_total() -> None:
    """Reset the total statistic counters."""
    cfg.glob.total_erroneous = 0
    cfg.glob.total_generated = 0
    cfg.glob.total_ok_processed = 0
    cfg.glob.total_ok_processed_pandoc = 0
    cfg.glob.total_ok_processed_pdf2image = 0
    cfg.glob.total_ok_processed_pdflib = 0
    cfg.glob.total_ok_processed_tesseract = 0
    cfg.glob.total_status_error = 0
    cfg.glob.total_status_ready = 0
    cfg.glob.total_to_be_processed = 0


# -----------------------------------------------------------------------------
# Show the language related statistics of the run.
# -----------------------------------------------------------------------------
def show_statistics_language() -> None:
    """Show the language related statistics of the run."""
    comm.utils.progress_msg("===============================> Summary Language")
    comm.utils.progress_msg(f"Number documents to be processed:          {cfg.glob.language_to_be_processed:6d}")

    if cfg.glob.language_to_be_processed > 0:
        comm.utils.progress_msg(
            f"Number documents accepted - " f"Pandoc:        {cfg.glob.language_ok_processed_pandoc:6d}"
        )
        comm.utils.progress_msg(
            f"Number documents accepted - " f"pdf2image:     {cfg.glob.language_ok_processed_pdf2image:6d}"
        )
        comm.utils.progress_msg(
            f"Number documents accepted - " f"PDFlib TET:    {cfg.glob.language_ok_processed_pdflib:6d}"
        )
        comm.utils.progress_msg(
            f"Number documents accepted - " f"Tesseract OCR: {cfg.glob.language_ok_processed_tesseract:6d}"
        )
        comm.utils.progress_msg(f"Number documents accepted - " f"Total:         {cfg.glob.language_ok_processed:6d}")
        comm.utils.progress_msg(f"Number documents rejected:                 {cfg.glob.language_erroneous:6d}")


# -----------------------------------------------------------------------------
# Show the total statistics of the run.
# -----------------------------------------------------------------------------
def show_statistics_total() -> None:
    """Show the total statistics of the run."""
    comm.utils.progress_msg("==================================> Summary Total")
    comm.utils.progress_msg(f"Number documents to be processed:          {cfg.glob.total_to_be_processed:6d}")

    if cfg.glob.total_to_be_processed > 0:
        if cfg.glob.total_status_ready > 0 or cfg.glob.total_status_error > 0:
            comm.utils.progress_msg(f"Number with document status ready:         {cfg.glob.total_status_ready:6d}")
            comm.utils.progress_msg(f"Number with document status error:         {cfg.glob.total_status_error:6d}")

        if cfg.glob.run_action == cfg.glob.RUN_ACTION_PROCESS_INBOX:
            comm.utils.progress_msg(
                f"Number documents accepted - " f"Pandoc:        {cfg.glob.total_ok_processed_pandoc:6d}"
            )
            comm.utils.progress_msg(
                f"Number documents accepted - " f"pdf2image:     {cfg.glob.total_ok_processed_pdf2image:6d}"
            )
            comm.utils.progress_msg(
                f"Number documents accepted - " f"PDFlib TET:    {cfg.glob.total_ok_processed_pdflib:6d}"
            )
            comm.utils.progress_msg(
                f"Number documents accepted - " f"Tesseract OCR: {cfg.glob.total_ok_processed_tesseract:6d}"
            )
            comm.utils.progress_msg("Number documents accepted - " + f"Total:         {cfg.glob.total_ok_processed:6d}")
        elif cfg.glob.run_action == cfg.glob.RUN_ACTION_TEXT_FROM_PDF:
            comm.utils.progress_msg(f"Number documents extracted:                {cfg.glob.total_ok_processed:6d}")
        else:
            comm.utils.progress_msg(f"Number documents converted:                {cfg.glob.total_ok_processed:6d}")

        if cfg.glob.total_generated > 0:
            comm.utils.progress_msg(f"Number documents generated:                {cfg.glob.total_generated:6d}")

        if cfg.glob.run_action == cfg.glob.RUN_ACTION_PROCESS_INBOX:
            comm.utils.progress_msg(f"Number documents rejected:                 {cfg.glob.total_erroneous:6d}")
        else:
            comm.utils.progress_msg(f"Number documents erroneous:                {cfg.glob.total_erroneous:6d}")


# -----------------------------------------------------------------------------
# Start document processing.
# -----------------------------------------------------------------------------
def start_document_processing(document: sqlalchemy.engine.Row) -> None:
    """Start document processing.

    Args:
        document (Row):       Database row document.
    """
    cfg.glob.total_to_be_processed += 1

    cfg.glob.document_child_child_no = document.child_no
    cfg.glob.document_directory_name = document.directory_name
    cfg.glob.document_directory_type = document.directory_type
    cfg.glob.document_file_name = document.file_name
    cfg.glob.document_file_type = document.file_type
    cfg.glob.document_id = document.id
    cfg.glob.document_id_base = document.document_id_base
    cfg.glob.document_id_parent = document.document_id_parent
    cfg.glob.document_language_id = document.language_id
    cfg.glob.document_status = document.status
    cfg.glob.document_stem_name = document.stem_name

    db.dml.update_dbt_id(
        cfg.glob.DBT_DOCUMENT,
        cfg.glob.document_id,
        {
            cfg.glob.DBC_STATUS: cfg.glob.DOCUMENT_STATUS_START,
        },
    )

    if cfg.glob.document_status == cfg.glob.DOCUMENT_STATUS_ERROR:
        # not testable
        cfg.glob.total_status_error += 1
    else:
        cfg.glob.total_status_ready += 1


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
