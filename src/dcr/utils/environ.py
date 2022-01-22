"""
### Module: **Auxiliary routines for the environment data**.

Support of command line arguments, configuration parameters and
logging functionality.
"""

import configparser
import logging
import logging.config
import sys
from datetime import datetime

import yaml
from utils.constant import ACTION_DB_CREATE_OR_UPDATE
from utils.constant import ACTION_NEW_COMPLETE
from utils.constant import ACTION_PROCESS_INBOX
from utils.constant import ACTION_PROCESS_INBOX_OCR
from utils.constant import DCR_CFG_FILE
from utils.constant import DCR_CFG_SECTION
from utils.constant import FILE_ENCODING_DEFAULT
from utils.constant import LOGGER_CFG_FILE
from utils.constant import LOGGER_END
from utils.constant import LOGGER_PROGRESS_UPDATE
from utils.constant import LOGGER_START


# -----------------------------------------------------------------------------
# Load the command line arguments into memory.
# -----------------------------------------------------------------------------


def get_args(logger: logging.Logger) -> dict[str, bool]:
    """
    #### Function: **Load the command line arguments into memory**.

    The command line arguments define the process steps to be executed.
    The valid arguments are:

        d_c_u - Create or upgrade the database.
        new   - Run the complete processing of all new documents.
        p_i   - Process input folder.
        p_i_o - Process input folder OCR.

    With the option `new`, the following process steps are executed
    in this order:

        1. d_c_u
        2. p_i
        3. p_i_o

    **Args**:
    - **logger (logging.Logger)**: Current logger.

    **Returns**:
    - **dict[str, bool]**: The command line arguments found.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    num = len(sys.argv)

    if num == 1:
        logger.critical("fatal error: command line arguments missing")
        sys.exit(1)

    args = {
        ACTION_DB_CREATE_OR_UPDATE: False,
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: False,
    }

    for i in range(1, num):
        arg = sys.argv[i].lower()
        if arg == ACTION_NEW_COMPLETE:
            for key in args:
                args[key] = True
        elif arg in (
            ACTION_DB_CREATE_OR_UPDATE,
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


# -----------------------------------------------------------------------------
# Load the configuration parameters into memory.
# -----------------------------------------------------------------------------


def get_config(logger: logging.Logger) -> dict[str, str]:
    """
    #### Function: **Load the configuration parameters into memory**.

    Loads the configuration parameters from the `setup.cfg` file under
    the `dcr` section into memory.

    **Args**:
    - **logger (logging.Logger)**: Current logger.

    **Returns**:
    - **dict[str, str]**: Configuration parameters.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    config_parser = configparser.ConfigParser()
    config_parser.read(DCR_CFG_FILE)

    config: dict[str, str] = {}

    for section in config_parser.sections():
        if section == DCR_CFG_SECTION:
            for (key, value) in config_parser.items(section):
                config[key] = value

    print(
        LOGGER_PROGRESS_UPDATE
        + str(datetime.now())
        + " : The configuration parameters are checked and loaded."
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)

    return config


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------


def initialise_logger() -> logging.Logger:
    """
    #### Function: **Initialise the root logging functionality**.

    **Returns**:
    - **logging.Logger**: Root logger.
    """
    with open(LOGGER_CFG_FILE, "r", encoding=FILE_ENCODING_DEFAULT) as file:
        log_config = yaml.safe_load(file.read())

    logging.config.dictConfig(log_config)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    print(
        LOGGER_PROGRESS_UPDATE
        + str(datetime.now())
        + " : The logger is configured and ready."
    )

    return logger
