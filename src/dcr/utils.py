"""Module utils: Helper functions."""
import datetime
import hashlib
import os
import pathlib

import PyPDF2
import PyPDF2.errors

import dcr.cfg.glob
import dcr.db.cls_document
import dcr.db.cls_run
import dcr_core.core_glob
import dcr_core.core_utils


# -----------------------------------------------------------------------------
# Check the existence of objects.
# -----------------------------------------------------------------------------
def check_exists_object(  # noqa: C901
    is_action_curr: bool = False,
    is_action_next: bool = False,
    is_db_core: bool = False,
    is_document: bool = False,
    is_run: bool = False,
) -> None:
    """Check the existence of objects.

    Args:
        is_action_curr (bool, optional):
                Check an object of class Action. Defaults to False.
        is_action_next (bool, optional):
                Check an object of class Action . Defaults to False.
        is_db_core (bool, optional):
                Check an object of class DBCore. Defaults to False.
        is_document (bool, optional):
                Check an object of class Document. Defaults to False.
        is_run (bool, optional):
                Check an object of class Run. Defaults to False.
    """
    if is_action_curr:
        try:
            dcr.cfg.glob.action_curr.exists()  # type: ignore
        except AttributeError:
            dcr_core.core_utils.terminate_fatal(
                "The required instance of the class 'Action (action_curr)' does not yet exist.",
            )

    if is_action_next:
        try:
            dcr.cfg.glob.action_next.exists()  # type: ignore
        except AttributeError:
            dcr_core.core_utils.terminate_fatal(
                "The required instance of the class 'Action (action_next)' does not yet exist.",
            )

    if is_db_core:
        try:
            dcr.cfg.glob.db_core.exists()  # type: ignore
        except AttributeError:
            dcr_core.core_utils.terminate_fatal(
                "The required instance of the class 'DBCore' does not yet exist.",
            )

    if is_document:
        try:
            dcr.cfg.glob.document.exists()  # type: ignore
        except AttributeError:
            dcr_core.core_utils.terminate_fatal(
                "The required instance of the class 'Document' does not yet exist.",
            )

    if is_run:
        try:
            dcr.cfg.glob.run.exists()  # type: ignore
        except AttributeError:
            dcr_core.core_utils.terminate_fatal(
                "The required instance of the class 'Run' does not yet exist.",
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
    with open(file, "rb") as file_handle:
        content = file_handle.read()
        return hashlib.sha256(content).hexdigest()


# -----------------------------------------------------------------------------
# Delete the given auxiliary file.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def delete_auxiliary_file(full_name: pathlib.Path | str) -> None:
    """Delete the given auxiliary file.

    Args:
        full_name (pathlib.Path | str): File name.
    """
    if not dcr_core.core_glob.setup.is_delete_auxiliary_files:
        return

    full_name = dcr_core.core_utils.get_os_independent_name(full_name)

    # Don't remove the base document !!!
    if full_name == dcr_core.core_utils.get_full_name(
        dcr.cfg.glob.action_curr.action_directory_name, dcr.cfg.glob.document.get_file_name_next()
    ):
        return

    if os.path.isfile(full_name):
        os.remove(full_name)
        progress_msg(f"Auxiliary file '{full_name}' deleted")


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
# Get the path name from a directory name or a file name.
# -----------------------------------------------------------------------------
def get_path_name(name: pathlib.Path | str | None) -> pathlib.Path | str:
    """Get the full name from a directory name or path and a file name or path.

    Args:
        name (pathlib.Path | str | None): Directory name or file name.

    Returns:
        str: Full file name.
    """
    if name is None:
        return ""

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
    if get_file_type(file_name) != dcr_core.core_glob.FILE_TYPE_PDF:
        return -1

    try:
        return len(PyPDF2.PdfReader(file_name).pages)
    except PyPDF2.errors.PdfReadError:
        return -1


# -----------------------------------------------------------------------------
# Create a progress message.
# -----------------------------------------------------------------------------
def progress_msg(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    try:
        dcr_core.core_glob.setup.exists()

        if dcr_core.core_glob.setup.is_verbose:
            progress_msg_core(msg)
    except AttributeError:
        progress_msg_core(msg)


# -----------------------------------------------------------------------------
# Create a progress message: connected to database.
# -----------------------------------------------------------------------------
def progress_msg_connected(database: str | None, user: str | None) -> None:
    """Create a progress message: connected to database."""
    try:
        dcr_core.core_glob.setup.exists()

        if dcr_core.core_glob.setup.is_verbose:
            print("")
            progress_msg(f"User '{user}' is now connected " f"to database '{database}'")
    except AttributeError:
        print("")
        progress_msg(f"User '{user}' is now connected " f"to database '{database}'")


# -----------------------------------------------------------------------------
# Create a progress message.
# -----------------------------------------------------------------------------
def progress_msg_core(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    final_msg = dcr_core.core_glob.LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg + "."

    print(final_msg)

    dcr.cfg.glob.logger.debug(final_msg)


# -----------------------------------------------------------------------------
# Create a progress message: disconnected from database.
# -----------------------------------------------------------------------------
def progress_msg_disconnected() -> None:
    """Create a progress message: disconnected from database."""
    try:
        dcr_core.core_glob.setup.exists()

        if dcr_core.core_glob.setup.is_verbose:
            if dcr.cfg.glob.db_core.db_current_database == "" and dcr.cfg.glob.db_core.db_current_user == "":
                print("")
                progress_msg("Database is now disconnected")
                return

            database = (
                dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE
                if dcr.cfg.glob.db_core.db_current_database == ""
                else dcr.cfg.glob.db_core.db_current_database
            )

            user = (
                dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE
                if dcr.cfg.glob.db_core.db_current_user == ""
                else dcr.cfg.glob.db_core.db_current_user
            )

            print("")
            progress_msg(f"User '{user}' is now disconnected from database '{database}'")

            dcr.cfg.glob.db_core.db_current_database = ""
            dcr.cfg.glob.db_core.db_current_user = ""
    except AttributeError:
        pass


# -----------------------------------------------------------------------------
# Create a progress message with empty line before.
# -----------------------------------------------------------------------------
def progress_msg_empty_before(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    try:
        dcr_core.core_glob.setup.exists()
        if dcr_core.core_glob.setup.is_verbose:
            print("")
            progress_msg(msg)
    except AttributeError:
        print("")
        progress_msg(msg)


# -----------------------------------------------------------------------------
# Reset the total statistic counters.
# -----------------------------------------------------------------------------
def reset_statistics_total() -> None:
    """Reset the total statistic counters."""
    dcr.cfg.glob.run.run_total_erroneous = 0
    dcr.cfg.glob.run.run_total_processed_ok = 0
    dcr.cfg.glob.run.run_total_processed_to_be = 0

    dcr.cfg.glob.run.total_generated = 0
    dcr.cfg.glob.run.total_processed_pandoc = 0
    dcr.cfg.glob.run.total_processed_pdf2image = 0
    dcr.cfg.glob.run.total_processed_pdflib = 0
    dcr.cfg.glob.run.total_processed_tesseract = 0
    dcr.cfg.glob.run.total_status_error = 0
    dcr.cfg.glob.run.total_status_ready = 0


# -----------------------------------------------------------------------------
# Show the language related statistics of the run.
# -----------------------------------------------------------------------------
def show_statistics_language() -> None:
    """Show the language related statistics of the run."""
    progress_msg("===============================> Summary Language")
    progress_msg(f"Number documents to be processed:          {dcr.cfg.glob.language.total_processed_to_be:6d}")

    if dcr.cfg.glob.language.total_processed_to_be > 0:
        progress_msg(f"Number documents accepted - " f"Pandoc:        {dcr.cfg.glob.language.total_processed_pandoc:6d}")
        progress_msg(f"Number documents accepted - " f"pdf2image:     {dcr.cfg.glob.language.total_processed_pdf2image:6d}")
        progress_msg(f"Number documents accepted - " f"PDFlib TET:    {dcr.cfg.glob.language.total_processed_pdflib:6d}")
        progress_msg(f"Number documents accepted - " f"Tesseract OCR: {dcr.cfg.glob.language.total_processed_tesseract:6d}")
        progress_msg(f"Number documents accepted - " f"Total:         {dcr.cfg.glob.language.total_processed:6d}")
        progress_msg(f"Number documents rejected:                 {dcr.cfg.glob.language.total_erroneous:6d}")


# -----------------------------------------------------------------------------
# Show the total statistics of the run.
# -----------------------------------------------------------------------------
def show_statistics_total() -> None:
    """Show the total statistics of the run."""
    progress_msg("==================================> Summary Total")
    progress_msg(f"Number documents to be processed:          {dcr.cfg.glob.run.run_total_processed_to_be:6d}")

    if dcr.cfg.glob.run.run_total_processed_to_be > 0:
        if dcr.cfg.glob.run.total_status_ready > 0 or dcr.cfg.glob.run.total_status_error > 0:
            progress_msg(f"Number with document status ready:         {dcr.cfg.glob.run.total_status_ready:6d}")
            progress_msg(f"Number with document status error:         {dcr.cfg.glob.run.total_status_error:6d}")

        # noinspection PyUnresolvedReferences
        if dcr.cfg.glob.run.run_action_code == dcr.db.cls_run.Run.ACTION_CODE_INBOX:
            progress_msg(f"Number documents accepted - " f"Pandoc:        {dcr.cfg.glob.run.total_processed_pandoc:6d}")
            progress_msg(f"Number documents accepted - " f"pdf2image:     {dcr.cfg.glob.run.total_processed_pdf2image:6d}")
            progress_msg(f"Number documents accepted - " f"PDFlib TET:    {dcr.cfg.glob.run.total_processed_pdflib:6d}")
            progress_msg(f"Number documents accepted - " f"Tesseract OCR: {dcr.cfg.glob.run.total_processed_tesseract:6d}")
            progress_msg(f"Number documents accepted - " f"Total:         {dcr.cfg.glob.run.run_total_processed_ok:6d}")
        elif dcr.cfg.glob.run.run_action_code == dcr.db.cls_run.Run.ACTION_CODE_PDFLIB:
            progress_msg(f"Number documents extracted:                {dcr.cfg.glob.run.run_total_processed_ok:6d}")
        else:
            progress_msg(f"Number documents converted:                {dcr.cfg.glob.run.run_total_processed_ok:6d}")

        if dcr.cfg.glob.run.total_generated > 0:
            if dcr.cfg.glob.run.run_action_code == dcr.db.cls_run.Run.ACTION_CODE_PYPDF2:
                progress_msg(f"Number generated pdf documents:            {dcr.cfg.glob.run.total_generated:6d}")
            else:
                progress_msg(f"Number pdf documents generated:            {dcr.cfg.glob.run.total_generated:6d}")

        # noinspection PyUnresolvedReferences
        if dcr.cfg.glob.run.run_action_code == dcr.db.cls_run.Run.ACTION_CODE_INBOX:
            progress_msg(f"Number documents rejected:                 {dcr.cfg.glob.run.run_total_erroneous:6d}")
        else:
            progress_msg(f"Number documents erroneous:                {dcr.cfg.glob.run.run_total_erroneous:6d}")
