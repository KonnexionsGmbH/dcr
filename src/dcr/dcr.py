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


# -----------------------------------------------------------------------------
# Load the command line arguments into memory.
# -----------------------------------------------------------------------------
def get_args(argv: List[str]) -> dict[str, bool]:
    """Load the command line arguments into memory.

    The command line arguments define the process steps to be executed.
    The valid arguments are:

        all   - Run the complete processing of all new documents.
        db_c  - Create the database.
        db_u  - Upgrade the database.
        p_i   - Process the inbox directory.
        p_2_i - Convert pdf documents to image files.

    With the option all, the following process steps are executed
    in this order:

        1. p_i
        2. p_2_i

    Args:
        argv (List[str]): Command line arguments.

    Returns:
        dict[str, bool]: The processing steps based on CLI arguments.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    num = len(argv)

    if num == 0:
        utils.terminate_fatal("No command line arguments found")

    if num == 1:
        utils.terminate_fatal(
            "The specific command line arguments are missing"
        )

    args = {
        cfg.RUN_ACTION_CREATE_DB: False,
        cfg.RUN_ACTION_PDF_2_IMAGE: False,
        cfg.RUN_ACTION_PROCESS_INBOX: False,
        cfg.RUN_ACTION_UPGRADE_DB: False,
    }

    for i in range(1, num):
        arg = argv[i].lower()
        if arg == cfg.RUN_ACTION_ALL_COMPLETE:
            args[cfg.RUN_ACTION_PDF_2_IMAGE] = True
            args[cfg.RUN_ACTION_PROCESS_INBOX] = True
        elif arg in (
            cfg.RUN_ACTION_CREATE_DB,
            cfg.RUN_ACTION_PDF_2_IMAGE,
            cfg.RUN_ACTION_PROCESS_INBOX,
            cfg.RUN_ACTION_UPGRADE_DB,
        ):
            args[arg] = True
        else:
            utils.terminate_fatal(
                "Unknown command line argument='" + argv[i] + "'"
            )

    utils.progress_msg("The command line arguments are validated and loaded")

    cfg.logger.debug(cfg.LOGGER_END)

    return args


# -----------------------------------------------------------------------------
# Load the configuration parameters into memory.
# -----------------------------------------------------------------------------
def get_config() -> None:
    """Load the configuration parameters into memory.

    Loads the configuration parameters from the `setup.cfg` file under
    the `DCR` section into memory.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    config_parser = configparser.ConfigParser()
    config_parser.read(cfg.DCR_CFG_FILE)

    for section in config_parser.sections():
        if section == cfg.DCR_CFG_SECTION:
            for (key, value) in config_parser.items(section):
                cfg.config[key] = value

    utils.progress_msg("The configuration parameters are checked and loaded")

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def initialise_logger() -> None:
    """Initialise the root logging functionality."""
    with open(
        cfg.LOGGER_CFG_FILE, "r", encoding=cfg.FILE_ENCODING_DEFAULT
    ) as file:
        log_config = yaml.safe_load(file.read())

    logging.config.dictConfig(log_config)
    cfg.logger = logging.getLogger("dcr.py")
    cfg.logger.setLevel(logging.DEBUG)

    utils.progress_msg("The logger is configured and ready")


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
    initialise_logger()

    cfg.logger.debug(cfg.LOGGER_START)
    cfg.logger.info("Start dcr.py")

    print("Start dcr.py")

    locale.setlocale(locale.LC_ALL, cfg.LOCALE)

    # Load the command line arguments into the memory.
    args = get_args(argv)

    # Load the configuration parameters into the memory.
    get_config()

    if args[cfg.RUN_ACTION_CREATE_DB]:
        # Create the database.
        print("")
        utils.progress_msg("Start: Create the database ...")
        db.create_database()
        utils.progress_msg("End  : Create the database ...")
    elif args[cfg.RUN_ACTION_UPGRADE_DB]:
        # Upgrade the database.
        print("")
        utils.progress_msg("Start: Upgrade the database ...")
        db.upgrade_database()
        utils.progress_msg("End  : Upgrade the database ...")
    else:
        # Process the documents.
        process_documents(args)

    # Disconnect from the database.
    db.disconnect_db()

    print("End   dcr.py")

    cfg.logger.info("End   dcr.py")
    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the documents.
# -----------------------------------------------------------------------------
def process_documents(args: dict[str, bool]) -> None:
    """Process the documents.

    Args:
        args (dict[str, bool]): The processing steps based on CLI arguments.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    # Connect to the database.
    db.connect_db()

    # Check the version of the database.
    db.check_db_up_to_date()

    cfg.run_run_id = db.select_run_run_id_last() + 1

    # Process the documents in the inbox file directory.
    if args[cfg.RUN_ACTION_PROCESS_INBOX]:
        cfg.run_action = cfg.RUN_ACTION_PROCESS_INBOX
        print("")
        utils.progress_msg("Start: Process the inbox directory ...")
        db.insert_dbt_run_row()
        inbox.process_inbox_files()
        db.update_dbt_id(
            db.DBT_RUN,
            cfg.run_id,
            {
                db.DBC_STATUS: cfg.STATUS_END,
                db.DBC_TOTAL_TO_BE_PROCESSED: cfg.total_to_be_processed,
                db.DBC_TOTAL_OK_PROCESSED: cfg.total_ok_processed,
                db.DBC_TOTAL_ERRONEOUS: cfg.total_erroneous,
            },
        )
        utils.progress_msg("End  : Process the inbox directory ...")

    # Convert the scanned image pdf documents to image files.
    if args[cfg.RUN_ACTION_PDF_2_IMAGE]:
        cfg.run_action = cfg.RUN_ACTION_PDF_2_IMAGE
        print("")
        utils.progress_msg("Start: Convert pdf documentss to image files ...")
        db.insert_dbt_run_row()
        inbox.convert_pdf_2_image()
        db.update_dbt_id(
            db.DBT_RUN,
            cfg.run_id,
            {
                db.DBC_STATUS: cfg.STATUS_END,
                db.DBC_TOTAL_TO_BE_PROCESSED: cfg.total_to_be_processed,
                db.DBC_TOTAL_OK_PROCESSED: cfg.total_ok_processed,
                db.DBC_TOTAL_ERRONEOUS: cfg.total_erroneous,
            },
        )
        utils.progress_msg("End  : Convert pdf documentss to image files ...")

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)
