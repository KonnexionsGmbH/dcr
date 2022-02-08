"""Entry point functionality.

This is the entry point to the application DCR.

Returns:
    [type]: None.
"""

import configparser
import locale
import logging
import logging.config
import sys
from typing import List

import yaml
from libs import cfg
from libs import db
from libs import inbox
from libs import utils
from libs.db import create_db_tables
from libs.db import create_db_triggers


# -----------------------------------------------------------------------------
# Load the command line arguments into memory.
# -----------------------------------------------------------------------------
def get_args(logger: logging.Logger, argv: List[str]) -> dict[str, bool]:
    """Load the command line arguments into memory.

    The command line arguments define the process steps to be executed.
    The valid arguments are:

        all   - Run the complete processing of all new documents.
        db_c  - Create the database.
        p_i   - Process input folder.

    With the option all, the following process steps are executed
    in this order:

        1. p_i

    Args:
        logger (logging.Logger): Current logger.
        argv (List[str]): Command line arguments.

    Returns:
        dict[str, bool]: The processing steps based on CLI arguments.
    """
    logger.debug(cfg.LOGGER_START)

    num = len(argv)

    if num == 0:
        utils.terminate_fatal(logger, "No command line arguments found")

    if num == 1:
        utils.terminate_fatal(
            logger, "The specific command line arguments are missing"
        )

    args = {
        cfg.RUN_ACTION_CREATE_DB: False,
        cfg.RUN_ACTION_PROCESS_INBOX: False,
    }

    for i in range(1, num):
        arg = argv[i].lower()
        if arg == cfg.RUN_ACTION_ALL_COMPLETE:
            args[cfg.RUN_ACTION_PROCESS_INBOX] = True
        elif arg in (
            cfg.RUN_ACTION_CREATE_DB,
            cfg.RUN_ACTION_PROCESS_INBOX,
        ):
            args[arg] = True
        else:
            utils.terminate_fatal(
                logger, "Unknown command line argument='" + argv[i] + "'"
            )

    utils.progress_msg(
        logger, "The command line arguments are validated and loaded"
    )

    logger.debug(cfg.LOGGER_END)

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
    logger.debug(cfg.LOGGER_START)

    config_parser = configparser.ConfigParser()
    config_parser.read(cfg.DCR_CFG_FILE)

    for section in config_parser.sections():
        if section == cfg.DCR_CFG_SECTION:
            for (key, value) in config_parser.items(section):
                cfg.config[key] = value

    cfg.config[cfg.DCR_CFG_DATABASE] = (
        cfg.config[cfg.DCR_CFG_DATABASE_URL]
        + cfg.config[cfg.DCR_CFG_DATABASE_FILE]
    )

    utils.progress_msg(
        logger, "The configuration parameters are checked and loaded"
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def initialise_logger() -> logging.Logger:
    """Initialise the root logging functionality.

    Returns:
        logging.Logger: Root logger.
    """
    with open(
        cfg.LOGGER_CFG_FILE, "r", encoding=cfg.FILE_ENCODING_DEFAULT
    ) as file:
        log_config = yaml.safe_load(file.read())

    logging.config.dictConfig(log_config)
    logger = logging.getLogger("dcr.py")
    logger.setLevel(logging.DEBUG)

    utils.progress_msg(logger, "The logger is configured and ready")

    return logger


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def main(argv: List[str]) -> None:
    """Entry point.

    The processes to be carried out are selected via command line arguments.

    Args:
        argv (List[str]): Command line arguments.
    """
    # Initialise the logging functionality.
    logger = initialise_logger()

    logger.debug(cfg.LOGGER_START)

    print("Start dcr.py")

    locale.setlocale(locale.LC_ALL, cfg.LOCALE)

    # Load the command line arguments into the memory.
    args = get_args(logger, argv)

    # Load the configuration parameters into the memory.
    get_config(logger)

    if args[cfg.RUN_ACTION_CREATE_DB]:
        # Create the database tables.
        utils.progress_msg(logger, "Start: Create the database tables ...")
        create_db_tables(logger)
        # Create the database triggers.
        utils.progress_msg(logger, "Start: Create the database triggers ...")
        create_db_triggers(logger)
        db.create_dbt_version_row(logger)
    else:
        # Process the documents.
        utils.progress_msg(logger, "Start: Process the documents ...")
        process_documents(logger, args)

    print("End   dcr.py")

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the documents.
# -----------------------------------------------------------------------------
def process_documents(logger: logging.Logger, args: dict[str, bool]) -> None:
    """Process the documents.

    Args:
        logger (logging.Logger): Current logger.
        args (dict[str, bool]): The processing steps based on CLI arguments.
    """
    # Connect to the database.
    db.connect_db(logger)

    # Check the version of the database.
    db.check_db_up_to_date(logger)

    # Creation of the run entry in the database.
    db.create_dbt_run_row(logger)

    # Process the documents in the inbox file directory.
    if args[cfg.RUN_ACTION_PROCESS_INBOX]:
        inbox.process_inbox_new(logger)

    # Finalise the run entry in the database.
    terminate_run_entry(logger)

    # Disconnect from the database.
    db.disconnect_db(logger)


# -----------------------------------------------------------------------------
# Terminate the current entry in the database table run.
# -----------------------------------------------------------------------------
def terminate_run_entry(logger: logging.Logger) -> None:
    """Terminate the current entry in the database table run.

    Returns:
        logging.Logger: Root logger.
    """
    logger.debug(cfg.LOGGER_START)

    db.update_dbt_id(
        logger,
        cfg.DBT_RUN,
        cfg.run_id,
        {
            cfg.DBC_STATUS: cfg.STATUS_END,
            cfg.DBC_TOTAL_ACCEPTED: cfg.total_accepted,
            cfg.DBC_TOTAL_NEW: cfg.total_new,
            cfg.DBC_TOTAL_REJECTED: cfg.total_rejected,
        },
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)
