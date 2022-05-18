"""Module utils: Helper functions."""
import datetime
import hashlib
import os
import pathlib
import sys
import traceback

import cfg.glob
import db.cls_run
import db.dml
import db.driver
import PyPDF2
import PyPDF2.utils
import utils


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

    with open(file, "rb") as file_handle:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file_handle.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


# -----------------------------------------------------------------------------
# Delete the given auxiliary file.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def delete_auxiliary_file(file_name: pathlib.Path | str) -> None:
    """Delete the given auxiliary file.

    Args:
        file_name (pathlib.Path | str): File name.
    """
    if not cfg.glob.setup.is_delete_auxiliary_files:
        return

    file_name = get_os_independent_name(file_name)

    # Don't remove the base document !!!
    if file_name == get_full_name(cfg.glob.action_curr.action_directory_name, cfg.glob.base.get_file_name_next()):
        return

    if os.path.isfile(file_name):
        os.remove(file_name)
        utils.progress_msg(f"Auxiliary file '{file_name}' deleted")


# -----------------------------------------------------------------------------
# Get the file type from a file name.
# -----------------------------------------------------------------------------
def get_file_type(file_name: pathlib.Path | str | None) -> str:
    """Get the file type from a file name.

    Args:
        file_name (pathlib.Path | str | None): File name or file path.

    Returns:
        str: File type.
    """
    if file_name is None:
        return ""

    if isinstance(file_name, str):
        file_name = pathlib.Path(file_name)

    return file_name.suffix[1:].lower()


# -----------------------------------------------------------------------------
# Get the full name from a directory name or path and a file name or path.
# -----------------------------------------------------------------------------
def get_full_name(directory_name: pathlib.Path | str | None, file_name: pathlib.Path | str | None) -> str:
    """Get the full name from a directory name or path and a file name or path.

    Args:
        directory_name (pathlib.Path | str | None): Directory name or directory path.
        file_name (pathlib.Path | str | None): File name or file path.

    Returns:
        str: Full file name.
    """
    if directory_name is None and file_name is None:
        return ""

    if isinstance(directory_name, pathlib.Path):
        directory_name = str(directory_name)

    if isinstance(file_name, pathlib.Path):
        file_name = str(file_name)

    print(f"wwe os.path.join(directory_name, file_name)={str(os.path.join(directory_name, file_name))}")

    return str(os.path.join(directory_name, file_name))


# -----------------------------------------------------------------------------
# Get the platform-independent name.
# -----------------------------------------------------------------------------
def get_os_independent_name(name: pathlib.Path | str | None) -> str:
    """Get the platform-independent name..

    Args:
        name (pathlib.Path | str | None): File name or file path.

    Returns:
        str: Platform-independent name.
    """
    if name is None:
        return ""

    if isinstance(name, str):
        return name.replace(("\\" if os.sep == "/" else "/"), os.sep)

    return str(name)


# -----------------------------------------------------------------------------
# Get the path name from a directory name or a file name.
# -----------------------------------------------------------------------------
def get_path_name(name: pathlib.Path | str | None) -> pathlib.Path | None:
    """Get the full name from a directory name or path and a file name or path.

    Args:
        name (pathlib.Path | str | None): Directory name or file name.

    Returns:
        str: Full file name.
    """
    if name is None:
        return None

    return pathlib.Path(name)


# -----------------------------------------------------------------------------
# Determine the number of pages in a pdf document.
# -----------------------------------------------------------------------------
def get_pdf_pages_no(
    file_name: pathlib.Path | str,
) -> int:
    """Determine the number of pages in a pdf document.

    Args:
        file_name (pathlib.Path | str): File name.

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
        str: Stem name.
    """
    if file_name is None:
        return ""

    if isinstance(file_name, str):
        file_name = pathlib.Path(file_name)

    return file_name.stem


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
            if cfg.glob.run.run_action_code == db.cls_run.Run.ACTION_CODE_PYPDF2:
                utils.progress_msg(f"Number generated pdf documents:            {cfg.glob.run.total_generated:6d}")
            else:
                utils.progress_msg(f"Number pdf documents generated:            {cfg.glob.run.total_generated:6d}")

        # noinspection PyUnresolvedReferences
        if cfg.glob.run.run_action_code == db.cls_run.Run.ACTION_CODE_INBOX:
            utils.progress_msg(f"Number documents rejected:                 {cfg.glob.run.run_total_erroneous:6d}")
        else:
            utils.progress_msg(f"Number documents erroneous:                {cfg.glob.run.run_total_erroneous:6d}")


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
