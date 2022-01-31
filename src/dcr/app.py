"""Entry point functionality.

This is the entry point to the application DCR.

Returns:
    [type]: None.
"""

import configparser
import datetime
import locale
import logging
import logging.config
import sys
from typing import List

import yaml
from libs import inbox
from libs.database import check_db_up_to_date
from libs.database import create_or_upgrade_database
from libs.globals import ACTION_ALL_COMPLETE
from libs.globals import ACTION_DB_CREATE_OR_UPGRADE
from libs.globals import ACTION_PROCESS_INBOX
from libs.globals import ACTION_PROCESS_INBOX_OCR
from libs.globals import CONFIG
from libs.globals import DCR_CFG_DATABASE
from libs.globals import DCR_CFG_DATABASE_FILE
from libs.globals import DCR_CFG_DATABASE_URL
from libs.globals import DCR_CFG_FILE
from libs.globals import DCR_CFG_SECTION
from libs.globals import FILE_ENCODING_DEFAULT
from libs.globals import LOCALE
from libs.globals import LOGGER_CFG_FILE
from libs.globals import LOGGER_END
from libs.globals import LOGGER_PROGRESS_UPDATE
from libs.globals import LOGGER_START
from libs.utils import terminate_fatal


# -----------------------------------------------------------------------------
# Load the command line arguments into memory.
# -----------------------------------------------------------------------------
def get_args(logger: logging.Logger, argv: List[str]) -> dict[str, bool]:
    """Load the command line arguments into memory.

    The command line arguments define the process steps to be executed.
    The valid arguments are:

        all   - Run the complete processing of all new documents.
        d_c_u - Create or upgrade the database.
        p_i   - Process input folder.

    With the option all, the following process steps are executed
    in this order:

        1. d_c_u
        2. p_i

    Args:
        logger (logging.Logger): Current logger.
        argv (List[str]): Command line arguments.

    Returns:
        dict[str, bool]: The command line arguments found.
    """
    logger.debug(LOGGER_START)

    num = len(argv)

    if num == 0:
        terminate_fatal(logger, "No command line arguments found")

    if num == 1:
        terminate_fatal(
            logger, "The specific command line arguments are missing"
        )

    args = {
        ACTION_DB_CREATE_OR_UPGRADE: False,
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: False,
    }

    for i in range(1, num):
        arg = argv[i].lower()
        if arg == ACTION_ALL_COMPLETE:
            for key in args:
                args[key] = True
        elif arg in (
            ACTION_DB_CREATE_OR_UPGRADE,
            ACTION_PROCESS_INBOX,
            ACTION_PROCESS_INBOX_OCR,
        ):
            args[arg] = True
        else:
            terminate_fatal(
                logger, "Unknown command line argument='" + argv[i] + "'"
            )

    print(
        LOGGER_PROGRESS_UPDATE,
        str(datetime.datetime.now()),
        " : The command line arguments are validated and loaded.",
        sep="",
    )

    logger.debug(LOGGER_END)

    return args


# -----------------------------------------------------------------------------
# Load the configuration parameters into memory.
# -----------------------------------------------------------------------------
def get_config(logger: logging.Logger) -> None:
    """Load the configuration parameters into memory.

    Loads the configuration parameters from the `setup.cfg` file under
    the `DCR` section into memory.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(LOGGER_START)

    config_parser = configparser.ConfigParser()
    config_parser.read(DCR_CFG_FILE)

    for section in config_parser.sections():
        if section == DCR_CFG_SECTION:
            for (key, value) in config_parser.items(section):
                CONFIG[key] = value

    CONFIG[DCR_CFG_DATABASE] = (
        CONFIG[DCR_CFG_DATABASE_URL] + CONFIG[DCR_CFG_DATABASE_FILE]
    )

    print(
        LOGGER_PROGRESS_UPDATE,
        str(datetime.datetime.now()),
        " : The configuration parameters are checked and loaded.",
        sep="",
    )

    logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def initialise_logger() -> logging.Logger:
    """Initialise the root logging functionality.

    Returns:
        logging.Logger: Root loggger.
    """
    with open(LOGGER_CFG_FILE, "r", encoding=FILE_ENCODING_DEFAULT) as file:
        log_config = yaml.safe_load(file.read())

    logging.config.dictConfig(log_config)
    logger = logging.getLogger("dcr.py")
    logger.setLevel(logging.DEBUG)

    print(
        LOGGER_PROGRESS_UPDATE,
        str(datetime.datetime.now()),
        " : The logger is configured and ready.",
        sep="",
    )
    print("")

    return logger


# -----------------------------------------------------------------------------
# Entry point.
# -----------------------------------------------------------------------------
def main(argv: List[str]) -> None:
    """Entry point.

    The processes to be carried out are selected via command line arguments.

    Args:
        argv (List[str]): Command line arguments.
    """
    # Initialise the logging functionality.
    logger = initialise_logger()

    logger.debug(LOGGER_START)

    print("Start app.py")

    locale.setlocale(locale.LC_ALL, LOCALE)

    # Load the command line arguments into the memory (pdf ...`)
    args = get_args(logger, argv)

    # Load the configuration parameters into the memory (CONFIG params
    # `file.configuration.name ...`)
    get_config(logger)

    if args[ACTION_DB_CREATE_OR_UPGRADE]:
        # Create or upgrade the database.
        create_or_upgrade_database(logger)

    # Setting up the database.
    check_db_up_to_date(logger)

    if args[ACTION_PROCESS_INBOX]:
        # Processing the inbox directory.
        inbox.process_inbox(logger)

    print("End   app.py")

    logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)
