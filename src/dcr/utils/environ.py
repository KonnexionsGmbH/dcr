"""
Auxiliary routines for the environment data..

Support of command line arguments, configuration parameters and
logging functionality.
"""

import logging
import logging.config
import sys
from datetime import datetime
from typing import Union

import tomli
import yaml
from utils.constant import ACTION_NEW_COMPLETE
from utils.constant import ACTION_PROCESS_INBOX
from utils.constant import ACTION_PROCESS_INBOX_OCR
from utils.constant import DCR_CFG_FILE
from utils.constant import LOGGER_END
from utils.constant import LOGGER_PROGRESS_UPDATE
from utils.constant import LOGGER_START


# ----------------------------------------------------------------------------------
# Load the command line arguments into memory.
# ----------------------------------------------------------------------------------


def get_args(logger: logging.Logger) -> dict[str, bool]:
    """Load the command line arguments into memory.

    Args:
        logger (Logger): Default logger.

    Returns:
        dict: Edited command line arguments.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    num = len(sys.argv)

    if num == 1:
        logger.critical("fatal error: command line arguments missing")
        sys.exit(1)

    args = {
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: False,
    }

    for i in range(1, num):
        arg = sys.argv[i].lower()
        if arg == ACTION_NEW_COMPLETE:
            for key in args:
                args[key] = True
        elif arg in (
            ACTION_PROCESS_INBOX,
            ACTION_PROCESS_INBOX_OCR,
        ):
            args[arg] = True
        else:
            logger.critical(
                "fatal error: unknown command line argument='"
                + sys.argv[i]
                + "'"
            )
            sys.exit(1)

    print(
        LOGGER_PROGRESS_UPDATE
        + str(datetime.now())
        + " : The command line arguments are validated and loaded."
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)

    return args


# ----------------------------------------------------------------------------------
# Load the configuration parameters into memory.
# ----------------------------------------------------------------------------------


def get_config(logger: logging.Logger) -> dict[str, Union[str, str]]:
    """Load the configuration parameters into memory.

    Args:
        logger (logging.Logger): Default logger.

    Returns:
        dict[str, Union[str, PathLike[str]]]: Configuration parameters.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    with open(DCR_CFG_FILE, "rb", encoding="utf-8") as file:
        config: dict[str, str] = tomli.load(file)

    for entry in config:
        print(entry)

    print(
        LOGGER_PROGRESS_UPDATE
        + str(datetime.now())
        + " : The configuration parameters are checked and loaded."
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)

    return config


# ----------------------------------------------------------------------------------
# Initialising the logging functionality.
# ----------------------------------------------------------------------------------


def initialise_logger() -> logging.Logger:
    """
    Initialise the logging functionality.

    Returns:
        Logger: Default logger.
    """
    with open("logging_cfg.yaml", "r", encoding="utf-8") as file:
        log_config = yaml.safe_load(file.read())

    logging.config.dictConfig(log_config)
    logger = logging.getLogger("app.py")
    logger.setLevel(logging.DEBUG)

    print(
        LOGGER_PROGRESS_UPDATE
        + str(datetime.now())
        + " : The logger is configured and ready."
    )

    return logger
