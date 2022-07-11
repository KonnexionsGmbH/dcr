"""Module utils: Helper functions."""
import datetime
import sys
import traceback

import dcr_core.cfg.glob


# -----------------------------------------------------------------------------
# Check the existence of objects.
# -----------------------------------------------------------------------------
def check_exists_object(  # noqa: C901
    is_line_type_table: bool = False,
    is_text_parser: bool = False,
) -> None:
    """Check the existence of objects.

    Args:
        is_line_type_table (bool, optional):
                Check an object of class LineTypeTable. Defaults to False.
        is_text_parser (bool, optional):
                Check an object of class TextParser. Defaults to False.
    """
    if is_line_type_table:
        try:
            dcr_core.cfg.glob.line_type_table.exists()  # type: ignore
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'LineTypeTable' does not yet exist.",
            )

    if is_text_parser:
        try:
            dcr_core.cfg.glob.text_parser.exists()
        except AttributeError:
            terminate_fatal(
                "The required instance of the class 'TextParser' does not yet exist.",
            )


# -----------------------------------------------------------------------------
# Create a progress message.
# -----------------------------------------------------------------------------
def progress_msg(is_verbose: bool, msg: str) -> None:
    """Create a progress message.

    Args:
        is_verbose (bool):
                If true, processing results are reported.
        msg (str):
                Progress message.
    """
    if is_verbose:
        progress_msg_core(msg)


# -----------------------------------------------------------------------------
# Create a progress message.
# -----------------------------------------------------------------------------
def progress_msg_core(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str):
                Progress message.
    """
    final_msg = dcr_core.cfg.glob.LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg + "."

    print(final_msg)


# -----------------------------------------------------------------------------
# Terminate the application immediately.
# -----------------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message.
    """
    print("")
    print(dcr_core.cfg.glob.LOGGER_FATAL_HEAD)
    print(dcr_core.cfg.glob.LOGGER_FATAL_HEAD, error_msg, dcr_core.cfg.glob.LOGGER_FATAL_TAIL, sep="")
    print(dcr_core.cfg.glob.LOGGER_FATAL_HEAD)

    traceback.print_exc(chain=True)

    sys.exit(1)
