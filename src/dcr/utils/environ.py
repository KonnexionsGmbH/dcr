"""
### **Auxiliary routines for the environment data**.

Support of command line arguments, configuration parameters and
logging functionality.
"""

import configparser
import logging
import logging.config
import sys
from datetime import datetime

import yaml
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
    **Load the command line arguments into memory**.

    The command line arguments define the process steps to be executed.
    The available options are:

        m_d_e - Run the development ecosystem.
        m_d_i - Run the installation of the necessary 3rd party packages
                for development.
        m_p   - Run the installation of the necessary 3rd party packages
                for development and compile all packages and modules.
        new   - Run the complete processing of all new documents.
        p_i   - Process input folder.
        p_i_o - Process input folder OCR.

    With the option `new`, the following process steps are executed
    in the specified order:

        1. p_i
        2. p_i_o

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


# -----------------------------------------------------------------------------
# Load the configuration parameters into memory.
# -----------------------------------------------------------------------------


def get_config(logger: logging.Logger) -> dict[str, str]:
    """
    **Load the configuration parameters into memory**.

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
    **Initialise the root logging functionality**.

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
