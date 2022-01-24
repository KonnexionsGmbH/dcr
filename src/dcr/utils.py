"""### Module: **Help functions**."""
import logging
import sys

# -----------------------------------------------------------------------------
# Terminate the application immediately..
# -----------------------------------------------------------------------------
from globals import LOGGER_FATAL_HEAD
from globals import LOGGER_FATAL_TAIL


def terminate_fatal(logger: logging.Logger, error_msg: str) -> None:
    """
    Terminate the application immediately.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    - **error_msg (str)**: Error message.
    """
    print("")
    print(LOGGER_FATAL_HEAD)
    print(LOGGER_FATAL_HEAD + error_msg + LOGGER_FATAL_TAIL)
    print(LOGGER_FATAL_HEAD)
    logger.error(LOGGER_FATAL_HEAD + error_msg + LOGGER_FATAL_TAIL)
    sys.exit(1)
