"""
Auxiliary routines for the environment data..

Support of command line arguments, configuration parameters and
logging functionality.
"""

import configparser
import logging
import logging.config
import sys
from datetime import datetime

import yaml


# ----------------------------------------------------------------------------------
# Load the command line arguments into memory.
# ----------------------------------------------------------------------------------


def get_args(logger):
    """Load the command line arguments into memory.

    Args:
        logger (Logger): Default logger.

    Returns:
        dict: Edited command line arguments.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Start")

    num = len(sys.argv)

    if num == 1:
        logger.critical("fatal error: command line arguments missing")
        sys.exit(1)

    args = {"p_i": False, "p_i_o": False}

    for i in range(1, num):
        arg = sys.argv[i].lower()
        if arg == "new":
            for key in args:
                args[key] = True
        elif arg in ("p_i", "p_i_o"):
            args[arg] = True
        else:
            logger.critical(
                "fatal error: unknown command line argument='"
                + sys.argv[i]
                + "'"
            )
            sys.exit(1)

    print(
        "Progress update + datetime.now() + "
        + str(datetime.now())
        + " : The command line arguments are validated and loaded."
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("End")

    return args


# ----------------------------------------------------------------------------------
# Load the configuration parameters into memory.
# ----------------------------------------------------------------------------------


def get_config(logger):
    """Load the configuration parameters into memory.

    Args:
        logger (Logger): Default logger.

    Returns:
        dict: Configuration parameters.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Start")

    config_parser = configparser.ConfigParser()
    config_parser.read("resources/dcr.properties")

    config = {
        "database.url": config_parser["DEFAULT"]["database.url"],
        "dcr.version": config_parser["DEFAULT"]["dcr.version"],
        "directory.inbox": config_parser["DEFAULT"]["directory.inbox"],
        "directory.inbox.accepted": config_parser["DEFAULT"][
            "directory.inbox.accepted"
        ],
        "directory.inbox.ocr": config_parser["DEFAULT"]["directory.inbox.ocr"],
        "directory.inbox.ocr.accepted": config_parser["DEFAULT"][
            "directory.inbox.ocr.accepted"
        ],
        "directory.inbox.ocr.rejected": config_parser["DEFAULT"][
            "directory.inbox.ocr.rejected"
        ],
        "directory.inbox.rejected": config_parser["DEFAULT"][
            "directory.inbox.rejected"
        ],
    }

    print(
        "Progress update + datetime.now() + "
        + str(datetime.now())
        + " : The configuration parameters are checked and loaded."
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("End")

    return config


# ----------------------------------------------------------------------------------
# Initialising the logging functionality.
# ----------------------------------------------------------------------------------


def initialise_logger():
    """
    Initialise the logging functionality.

    Returns:
        Logger: Default logger.
    """
    with open("logging_cfg.yaml", "r", encoding="utf-8") as file:
        log_config = yaml.safe_load(file.read())

    logging.config.dictConfig(log_config)
    logger = logging.getLogger("dcr.py")
    logger.setLevel(logging.DEBUG)

    print(
        "Progress update + datetime.now() + "
        + str(datetime.now())
        + " : The logger is configured and ready."
    )

    return logger
