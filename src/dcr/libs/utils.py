"""### Module: **Helper functions**."""
import datetime
import logging
import sys

from libs.globals import LOGGER_FATAL_HEAD
from libs.globals import LOGGER_FATAL_TAIL
from libs.globals import LOGGER_FIXTURE_HEAD
from libs.globals import LOGGER_FIXTURE_TAIL


# -----------------------------------------------------------------------------
# Print fixture end message.
# -----------------------------------------------------------------------------
def print_fixture_end(fixture_name: str) -> None:
    """Print a fixture end message.

    Args:
        fixture_name (str): Fixture name.
    """
    print("")
    print(LOGGER_FIXTURE_HEAD)
    print(
        LOGGER_FIXTURE_HEAD,
        "End   ",
        fixture_name,
        LOGGER_FIXTURE_TAIL,
        sep="",
    )
    print(LOGGER_FIXTURE_HEAD, str(datetime.datetime.now()))


# -----------------------------------------------------------------------------
# Print fixture start message.
# -----------------------------------------------------------------------------
def print_fixture_start(fixture_name: str) -> None:
    """Print a fixture start message.

    Args:
        fixture_name (str): Fixture name.
    """
    print("")
    print(LOGGER_FIXTURE_HEAD)
    print(
        LOGGER_FIXTURE_HEAD,
        "Start ",
        fixture_name,
        LOGGER_FIXTURE_TAIL,
        sep="",
    )
    print(LOGGER_FIXTURE_HEAD, str(datetime.datetime.now()))


# -----------------------------------------------------------------------------
# Terminate the application immediately..
# -----------------------------------------------------------------------------
def terminate_fatal(logger: logging.Logger, error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        logger (logging.Logger): Current logger.
        error_msg (str): Error message
    """
    print("")
    print(LOGGER_FATAL_HEAD)
    print(LOGGER_FATAL_HEAD, error_msg, LOGGER_FATAL_TAIL, sep="")
    print(LOGGER_FATAL_HEAD)
    logger.critical(LOGGER_FATAL_HEAD + error_msg + LOGGER_FATAL_TAIL)
    sys.exit(1)
