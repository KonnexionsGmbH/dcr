"""Entry Point Functionality.

This is the entry point to the application DCR.

Returns:
    [type]: None.
"""

import configparser
import locale
import logging
import logging.config
import os
import sys
from typing import List

import libs.cfg
import libs.db.cfg
import libs.db.driver
import libs.db.orm
import libs.inbox
import libs.utils
import yaml


# -----------------------------------------------------------------------------
# Load the command line arguments into memory.
# -----------------------------------------------------------------------------
def get_args(argv: List[str]) -> dict[str, bool]:
    """Load the command line arguments.

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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    num = len(argv)

    if num == 0:
        libs.utils.terminate_fatal("No command line arguments found")

    if num == 1:
        libs.utils.terminate_fatal("The specific command line arguments are missing")

    args = {
        libs.cfg.RUN_ACTION_CREATE_DB: False,
        libs.cfg.RUN_ACTION_PDF_2_IMAGE: False,
        libs.cfg.RUN_ACTION_PROCESS_INBOX: False,
        libs.cfg.RUN_ACTION_UPGRADE_DB: False,
    }

    for i in range(1, num):
        arg = argv[i].lower()
        if arg == libs.cfg.RUN_ACTION_ALL_COMPLETE:
            args[libs.cfg.RUN_ACTION_PDF_2_IMAGE] = True
            args[libs.cfg.RUN_ACTION_PROCESS_INBOX] = True
        elif arg in (
            libs.cfg.RUN_ACTION_CREATE_DB,
            libs.cfg.RUN_ACTION_PDF_2_IMAGE,
            libs.cfg.RUN_ACTION_PROCESS_INBOX,
            libs.cfg.RUN_ACTION_UPGRADE_DB,
        ):
            args[arg] = True
        else:
            libs.utils.terminate_fatal("Unknown command line argument='" + argv[i] + "'")

    libs.utils.progress_msg("The command line arguments are validated and loaded")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    return args


# -----------------------------------------------------------------------------
# Load the configuration parameters.
# -----------------------------------------------------------------------------
def get_config() -> None:
    """Load the configuration parameters.

    Loads the configuration parameters from the `setup.cfg` file under
    the `DCR` sections.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    config_parser = configparser.ConfigParser()
    config_parser.read(libs.cfg.DCR_CFG_FILE)

    libs.cfg.config.clear()

    for section in config_parser.sections():
        if section == libs.cfg.DCR_CFG_SECTION:
            for (key, value) in config_parser.items(section):
                libs.cfg.config[key] = value

    for section in config_parser.sections():
        if section == libs.cfg.DCR_CFG_SECTION + "_" + libs.cfg.environment_type:
            for (key, value) in config_parser.items(section):
                libs.cfg.config[key] = value

    validate_config()

    libs.utils.progress_msg("The configuration parameters are checked and loaded")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Load environment variables.
# -----------------------------------------------------------------------------
def get_environment() -> None:
    """Load environment variables."""
    try:
        libs.cfg.environment_type = os.environ[libs.cfg.DCR_ENVIRONMENT_TYPE]
    except KeyError:
        libs.utils.terminate_fatal(
            "The environment variable '" + libs.cfg.DCR_ENVIRONMENT_TYPE + "' is missing"
        )

    if libs.cfg.environment_type not in [
        libs.cfg.ENVIRONMENT_TYPE_DEV,
        libs.cfg.ENVIRONMENT_TYPE_PROD,
        libs.cfg.ENVIRONMENT_TYPE_TEST,
    ]:
        libs.utils.terminate_fatal(
            "The environment variable '"
            + libs.cfg.DCR_ENVIRONMENT_TYPE
            + "' has the invalid content '"
            + libs.cfg.environment_type
            + "'"
        )

    libs.utils.progress_msg(
        "The run is performed in the environment '" + libs.cfg.environment_type + "'"
    )


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def initialise_logger() -> None:
    """Initialise the root logging functionality."""
    with open(libs.cfg.LOGGER_CFG_FILE, "r", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as file:
        log_config = yaml.safe_load(file.read())

    logging.config.dictConfig(log_config)
    libs.cfg.logger = logging.getLogger("dcr.py")
    libs.cfg.logger.setLevel(logging.DEBUG)

    libs.utils.progress_msg("The logger is configured and ready")


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

    libs.cfg.logger.debug(libs.cfg.LOGGER_START)
    libs.cfg.logger.info("Start dcr.py")

    print("Start dcr.py")

    locale.setlocale(locale.LC_ALL, libs.cfg.LOCALE)

    # Load the environment variables.
    get_environment()

    # Load the command line arguments.
    args = get_args(argv)

    # Load the configuration parameters.
    get_config()

    if args[libs.cfg.RUN_ACTION_CREATE_DB]:
        # Create the database.
        libs.utils.progress_msg_empty_before("Start: Create the database ...")
        libs.db.driver.create_database()
        libs.utils.progress_msg("End  : Create the database ...")
    elif args[libs.cfg.RUN_ACTION_UPGRADE_DB]:
        # Upgrade the database.
        libs.utils.progress_msg_empty_before("Start: Upgrade the database ...")
        libs.db.driver.upgrade_database()
        libs.utils.progress_msg("End  : Upgrade the database ...")
    else:
        # Process the documents.
        process_documents(args)

    print("End   dcr.py")

    libs.cfg.logger.info("End   dcr.py")
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Process the documents.
# -----------------------------------------------------------------------------
def process_documents(args: dict[str, bool]) -> None:
    """Process the documents.

    Args:
        args (dict[str, bool]): The processing steps based on CLI arguments.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # Connect to the database.
    libs.db.orm.connect_db()

    # Check the version of the database.
    libs.db.orm.check_db_up_to_date()

    libs.cfg.run_run_id = libs.db.orm.select_run_run_id_last() + 1

    # Process the documents in the inbox file directory.
    if args[libs.cfg.RUN_ACTION_PROCESS_INBOX]:
        libs.cfg.run_action = libs.cfg.RUN_ACTION_PROCESS_INBOX
        libs.utils.progress_msg_empty_before("Start: Process the inbox directory ...")
        libs.cfg.run_id = libs.db.orm.insert_dbt_row(
            libs.db.cfg.DBT_RUN,
            {
                libs.db.cfg.DBC_ACTION: libs.cfg.run_action,
                libs.db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.RUN_STATUS_START,
            },
        )
        libs.inbox.process_inbox()
        libs.db.orm.update_dbt_id(
            libs.db.cfg.DBT_RUN,
            libs.cfg.run_id,
            {
                libs.db.cfg.DBC_STATUS: libs.db.cfg.RUN_STATUS_END,
                libs.db.cfg.DBC_TOTAL_TO_BE_PROCESSED: libs.cfg.total_to_be_processed,
                libs.db.cfg.DBC_TOTAL_OK_PROCESSED: libs.cfg.total_ok_processed,
                libs.db.cfg.DBC_TOTAL_ERRONEOUS: libs.cfg.total_erroneous,
            },
        )
        libs.utils.progress_msg("End  : Process the inbox directory ...")

    # Convert the scanned image pdf documents to image files.
    if args[libs.cfg.RUN_ACTION_PDF_2_IMAGE]:
        libs.cfg.run_action = libs.cfg.RUN_ACTION_PDF_2_IMAGE
        libs.utils.progress_msg_empty_before("Start: Convert pdf documents to image files ...")
        libs.cfg.run_id = libs.db.orm.insert_dbt_row(
            libs.db.cfg.DBT_RUN,
            {
                libs.db.cfg.DBC_ACTION: libs.cfg.run_action,
                libs.db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.RUN_STATUS_START,
            },
        )
        libs.inbox.convert_pdf_2_image()
        libs.db.orm.update_dbt_id(
            libs.db.cfg.DBT_RUN,
            libs.cfg.run_id,
            {
                libs.db.cfg.DBC_STATUS: libs.db.cfg.RUN_STATUS_END,
                libs.db.cfg.DBC_TOTAL_TO_BE_PROCESSED: libs.cfg.total_to_be_processed,
                libs.db.cfg.DBC_TOTAL_OK_PROCESSED: libs.cfg.total_ok_processed,
                libs.db.cfg.DBC_TOTAL_ERRONEOUS: libs.cfg.total_erroneous,
            },
        )
        libs.utils.progress_msg("End  : Convert pdf documents to image files ...")

    # Disconnect from the database.
    libs.db.orm.disconnect_db()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# validate the configuration parameters.
# -----------------------------------------------------------------------------
def validate_config() -> None:
    """Validate the configuration parameters."""
    # -------------------------------------------------------------------------
    # Parameter: ignore_duplicates
    #
    if libs.cfg.DCR_CFG_IGNORE_DUPLICATES in libs.cfg.config:
        if libs.cfg.config[libs.cfg.DCR_CFG_IGNORE_DUPLICATES].lower() == "true":
            libs.cfg.is_ignore_duplicates = True

    # -------------------------------------------------------------------------
    # Parameter: pdf2image_type
    #
    if libs.cfg.DCR_CFG_PDF2IMAGE_TYPE not in libs.cfg.config:
        libs.cfg.pdf2image_type = libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_JPEG
    else:
        libs.cfg.pdf2image_type = libs.cfg.config[libs.cfg.DCR_CFG_PDF2IMAGE_TYPE]
        if libs.cfg.pdf2image_type not in [
            libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_JPEG,
            libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_PNG,
        ]:
            libs.utils.terminate_fatal(
                "Invalid configuration parameter value for parameter "
                + "'pdf2image_type': '"
                + libs.cfg.pdf2image_type
                + "'"
            )

    # -------------------------------------------------------------------------
    # Parameter: verbose
    #
    if libs.cfg.DCR_CFG_VERBOSE in libs.cfg.config:
        if libs.cfg.config[libs.cfg.DCR_CFG_VERBOSE].lower() == "false":
            libs.cfg.is_verbose = False
        else:
            libs.cfg.is_verbose = True


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)
