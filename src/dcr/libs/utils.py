"""### Module: **Helper functions**."""
import logging
import sys

from libs.globals import LOGGER_FATAL_HEAD
from libs.globals import LOGGER_FATAL_TAIL


# -----------------------------------------------------------------------------
# Terminate the application immediately..
# -----------------------------------------------------------------------------
def terminate_fatal(logger: logging.Logger, error_msg: str) -> None:
    """
    Terminate the application immediately.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    - **error_msg (str)**: Error message.
    """
    print("")
    print(LOGGER_FATAL_HEAD)
    print(LOGGER_FATAL_HEAD, error_msg, LOGGER_FATAL_TAIL, sep="")
    print(LOGGER_FATAL_HEAD)
    logger.critical(LOGGER_FATAL_HEAD + error_msg + LOGGER_FATAL_TAIL)
    sys.exit(1)
