"""Helper functions."""
import datetime
import logging
import sys

from libs import cfg


# -----------------------------------------------------------------------------
# Terminate the application immediately..
# -----------------------------------------------------------------------------
def progress_msg(logger: logging.Logger, msg: str) -> None:
    """Create a progress message.

    Args:
        logger (logging.Logger): Current logger.
        msg (str): Progress message.
    """
    final_msg: str = (
        cfg.LOGGER_PROGRESS_UPDATE
        + str(datetime.datetime.now())
        + " : "
        + msg
        + "."
    )

    print(final_msg)
    logger.info(final_msg)


# -----------------------------------------------------------------------------
# Terminate the application immediately..
# -----------------------------------------------------------------------------
def terminate_fatal(logger: logging.Logger, error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        logger (logging.Logger): Current logger.
        error_msg (str): Error message.
    """
    print("")
    print(cfg.LOGGER_FATAL_HEAD)
    print(cfg.LOGGER_FATAL_HEAD, error_msg, cfg.LOGGER_FATAL_TAIL, sep="")
    print(cfg.LOGGER_FATAL_HEAD)
    logger.critical(cfg.LOGGER_FATAL_HEAD + error_msg + cfg.LOGGER_FATAL_TAIL)
    sys.exit(1)
