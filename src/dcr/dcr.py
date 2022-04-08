"""Module dcr: Entry Point Functionality.

This is the entry point to the application DCR.
"""
import configparser
import locale
import logging
import logging.config
import os
import sys
import time
from typing import List

import db.cfg
import db.driver
import db.orm.connection
import db.orm.dml
import libs.cfg
import libs.utils
import preprocessor.inbox
import preprocessor.pandocdcr
import preprocessor.parser
import preprocessor.pdf2imagedcr
import preprocessor.pdflibdcr
import preprocessor.tesseractdcr
import sqlalchemy
import yaml
from sqlalchemy import Table
from sqlalchemy import select


# -----------------------------------------------------------------------------
# Check that the database version is up to date.
# -----------------------------------------------------------------------------
def check_db_up_to_date() -> None:
    """Check that the database version is up-to-date."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if db.cfg.db_orm_engine is None:
        libs.utils.terminate_fatal(
            "The database does not yet exist.",
        )

    if not sqlalchemy.inspect(db.cfg.db_orm_engine).has_table(db.cfg.DBT_VERSION):
        libs.utils.terminate_fatal(
            "The database table 'version' does not yet exist.",
        )

    current_version = db.orm.dml.select_version_version_unique()

    if libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION] != current_version:
        libs.utils.terminate_fatal(
            f"Current database version is '{current_version}' - but expected version is '"
            f"{str(libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION])}''"
        )

    libs.utils.progress_msg(f"The current version of database is '{current_version}'")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


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
        n_2_p - Convert non-pdf documents to pdf files.
        ocr   - Convert image documents to pdf files.
        p_2_i - Convert pdf documents to image files.
        p_i   - Process the inbox directory.
        s_f_p - Store the document structure from the parser result.
        tet   - Extract text and metadata from pdf documents.

    With the option all, the following process steps are executed
    in this order:

        1. p_i
        2. p_2_i
        3. n_2_p
        4. ocr
        5. tet
        6. s_f_p

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
        libs.cfg.RUN_ACTION_IMAGE_2_PDF: False,
        libs.cfg.RUN_ACTION_NON_PDF_2_PDF: False,
        libs.cfg.RUN_ACTION_PDF_2_IMAGE: False,
        libs.cfg.RUN_ACTION_PROCESS_INBOX: False,
        libs.cfg.RUN_ACTION_STORE_FROM_PARSER: False,
        libs.cfg.RUN_ACTION_TEXT_FROM_PDF: False,
        libs.cfg.RUN_ACTION_UPGRADE_DB: False,
    }

    for i in range(1, num):
        arg = argv[i].lower()
        if arg == libs.cfg.RUN_ACTION_ALL_COMPLETE:
            args[libs.cfg.RUN_ACTION_IMAGE_2_PDF] = True
            args[libs.cfg.RUN_ACTION_NON_PDF_2_PDF] = True
            args[libs.cfg.RUN_ACTION_PDF_2_IMAGE] = True
            args[libs.cfg.RUN_ACTION_PROCESS_INBOX] = True
            args[libs.cfg.RUN_ACTION_STORE_FROM_PARSER] = True
            args[libs.cfg.RUN_ACTION_TEXT_FROM_PDF] = True
        elif arg in (
            libs.cfg.RUN_ACTION_CREATE_DB,
            libs.cfg.RUN_ACTION_IMAGE_2_PDF,
            libs.cfg.RUN_ACTION_NON_PDF_2_PDF,
            libs.cfg.RUN_ACTION_PDF_2_IMAGE,
            libs.cfg.RUN_ACTION_PROCESS_INBOX,
            libs.cfg.RUN_ACTION_STORE_FROM_PARSER,
            libs.cfg.RUN_ACTION_TEXT_FROM_PDF,
            libs.cfg.RUN_ACTION_UPGRADE_DB,
        ):
            args[arg] = True
        else:
            libs.utils.terminate_fatal(f"Unknown command line argument='{argv[i]}'")

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
            f"The environment variable '{libs.cfg.DCR_ENVIRONMENT_TYPE}' is missing"
        )

    if libs.cfg.environment_type not in [
        libs.cfg.ENVIRONMENT_TYPE_DEV,
        libs.cfg.ENVIRONMENT_TYPE_PROD,
        libs.cfg.ENVIRONMENT_TYPE_TEST,
    ]:
        libs.utils.terminate_fatal(
            f"The environment variable '{libs.cfg.DCR_ENVIRONMENT_TYPE}' "
            f"has the invalid content '{libs.cfg.environment_type}'"
        )

    libs.utils.progress_msg("The run is performed in the environment '{libs.cfg.environment_type}'")


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
# Load the data from the database table 'language'.
# -----------------------------------------------------------------------------
def load_data_from_dbt_language() -> None:
    """Load the data from the database table 'language'."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = Table(
        db.cfg.DBT_LANGUAGE,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    libs.cfg.languages_pandoc = {}
    libs.cfg.languages_spacy = {}
    libs.cfg.languages_tesseract = {}

    with db.cfg.db_orm_engine.connect() as conn:
        rows = conn.execute(
            select(dbt.c.id, dbt.c.code_pandoc, dbt.c.code_spacy, dbt.c.code_tesseract).where(
                dbt.c.active,
            )
        )

        for row in rows:
            libs.cfg.languages_pandoc[row.id] = row.code_pandoc
            libs.cfg.languages_spacy[row.id] = row.code_spacy
            libs.cfg.languages_tesseract[row.id] = row.code_tesseract

        conn.close()

    libs.utils.progress_msg(f"Available languages for Pandoc        '{libs.cfg.languages_pandoc}'")
    libs.utils.progress_msg(f"Available languages for SpaCy         '{libs.cfg.languages_spacy}'")
    libs.utils.progress_msg(
        f"Available languages for Tesseract OCR '{libs.cfg.languages_tesseract}'"
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


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
        db.driver.create_database()
        libs.utils.progress_msg("End  : Create the database ...")
    elif args[libs.cfg.RUN_ACTION_UPGRADE_DB]:
        # Upgrade the database.
        libs.utils.progress_msg_empty_before("Start: Upgrade the database ...")
        db.driver.upgrade_database()
        libs.utils.progress_msg("End  : Upgrade the database ...")
    else:
        # Process the documents.
        process_documents(args)

    print("End   dcr.py")

    libs.cfg.logger.info("End   dcr.py")
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert image documents to pdf files.
# -----------------------------------------------------------------------------
def process_convert_image_2_pdf() -> None:
    """Convert image documents to pdf files."""
    libs.cfg.run_action = libs.cfg.RUN_ACTION_IMAGE_2_PDF

    libs.utils.progress_msg_empty_before(
        "Start: Convert image documents to pdf files ... Tesseract OCR"
    )
    libs.cfg.run_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_RUN,
        {
            db.cfg.DBC_ACTION: libs.cfg.run_action,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_START,
        },
    )
    preprocessor.tesseractdcr.convert_image_2_pdf()
    db.orm.dml.update_dbt_id(
        db.cfg.DBT_RUN,
        libs.cfg.run_id,
        {
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_END,
            db.cfg.DBC_TOTAL_TO_BE_PROCESSED: libs.cfg.total_to_be_processed,
            db.cfg.DBC_TOTAL_OK_PROCESSED: libs.cfg.total_ok_processed,
            db.cfg.DBC_TOTAL_ERRONEOUS: libs.cfg.total_erroneous,
        },
    )
    libs.utils.progress_msg("End  : Convert image documents to pdf files ...")

    libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_PYPDF4

    libs.utils.progress_msg_empty_before("Start: Reunite the related pdf files ... PyPDF4")
    libs.cfg.run_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_RUN,
        {
            db.cfg.DBC_ACTION: libs.cfg.run_action,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_START,
        },
    )
    preprocessor.tesseractdcr.reunite_pdfs()
    db.orm.dml.update_dbt_id(
        db.cfg.DBT_RUN,
        libs.cfg.run_id,
        {
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_END,
            db.cfg.DBC_TOTAL_TO_BE_PROCESSED: libs.cfg.total_to_be_processed,
            db.cfg.DBC_TOTAL_OK_PROCESSED: libs.cfg.total_ok_processed,
            db.cfg.DBC_TOTAL_ERRONEOUS: libs.cfg.total_erroneous,
        },
    )
    libs.utils.progress_msg("End  : Reunite the related pdf files ...")


# -----------------------------------------------------------------------------
# Convert non-pdf documents to pdf files.
# -----------------------------------------------------------------------------
def process_convert_non_pdf_2_pdf() -> None:
    """Convert non-pdf documents to pdf files."""
    libs.cfg.run_action = libs.cfg.RUN_ACTION_NON_PDF_2_PDF
    libs.utils.progress_msg_empty_before(
        "Start: Convert non-pdf documents to pdf files ... Pandoc [TeX Live]"
    )
    libs.cfg.run_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_RUN,
        {
            db.cfg.DBC_ACTION: libs.cfg.run_action,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_START,
        },
    )
    preprocessor.pandocdcr.convert_non_pdf_2_pdf()
    db.orm.dml.update_dbt_id(
        db.cfg.DBT_RUN,
        libs.cfg.run_id,
        {
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_END,
            db.cfg.DBC_TOTAL_TO_BE_PROCESSED: libs.cfg.total_to_be_processed,
            db.cfg.DBC_TOTAL_OK_PROCESSED: libs.cfg.total_ok_processed,
            db.cfg.DBC_TOTAL_ERRONEOUS: libs.cfg.total_erroneous,
        },
    )
    libs.utils.progress_msg("End  : Convert non-pdf documents to pdf files ...")


# -----------------------------------------------------------------------------
# Convert pdf documents to image files.
# -----------------------------------------------------------------------------
def process_convert_pdf_2_image() -> None:
    """Convert pdf documents to image files."""
    libs.cfg.run_action = libs.cfg.RUN_ACTION_PDF_2_IMAGE
    libs.utils.progress_msg_empty_before(
        "Start: Convert pdf documents to image files ... pdf2image [Poppler]"
    )
    libs.cfg.run_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_RUN,
        {
            db.cfg.DBC_ACTION: libs.cfg.run_action,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_START,
        },
    )
    preprocessor.pdf2imagedcr.convert_pdf_2_image()
    db.orm.dml.update_dbt_id(
        db.cfg.DBT_RUN,
        libs.cfg.run_id,
        {
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_END,
            db.cfg.DBC_TOTAL_TO_BE_PROCESSED: libs.cfg.total_to_be_processed,
            db.cfg.DBC_TOTAL_OK_PROCESSED: libs.cfg.total_ok_processed,
            db.cfg.DBC_TOTAL_ERRONEOUS: libs.cfg.total_erroneous,
        },
    )
    libs.utils.progress_msg("End  : Convert pdf documents to image files ...")


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
    db.orm.connection.connect_db()

    # Check the version of the database.
    check_db_up_to_date()

    libs.cfg.run_run_id = db.orm.dml.select_run_run_id_last() + 1

    # Load the data from the database table 'language'.
    load_data_from_dbt_language()

    # Process the documents in the inbox file directory.
    if args[libs.cfg.RUN_ACTION_PROCESS_INBOX]:
        start_time_process = time.perf_counter_ns()
        libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_INBOX
        process_inbox_directory()
        libs.utils.progress_msg(
            f"Time : {round((time.perf_counter_ns() - start_time_process)/1000000000,2) :10.2f} s"
        )

    # Convert the scanned image pdf documents to image files.
    if args[libs.cfg.RUN_ACTION_PDF_2_IMAGE]:
        start_time_process = time.perf_counter_ns()
        libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_PDF2IMAGE
        process_convert_pdf_2_image()
        libs.utils.progress_msg(
            f"Time : {round((time.perf_counter_ns() - start_time_process)/1000000000,2) :10.2f} s"
        )

    # Convert the image documents to pdf files.
    if args[libs.cfg.RUN_ACTION_IMAGE_2_PDF]:
        start_time_process = time.perf_counter_ns()
        libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_TESSERACT
        process_convert_image_2_pdf()
        libs.utils.progress_msg(
            f"Time : {round((time.perf_counter_ns() - start_time_process)/1000000000,2) :10.2f} s"
        )

    # Convert the non-pdf documents to pdf files.
    if args[libs.cfg.RUN_ACTION_NON_PDF_2_PDF]:
        start_time_process = time.perf_counter_ns()
        libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_PANDOC
        process_convert_non_pdf_2_pdf()
        libs.utils.progress_msg(
            f"Time : {round((time.perf_counter_ns() - start_time_process)/1000000000,2) :10.2f} s"
        )

    # Extract text and metadata from pdf documents.
    if args[libs.cfg.RUN_ACTION_TEXT_FROM_PDF]:
        start_time_process = time.perf_counter_ns()
        libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_PDFLIB
        process_extract_text_from_pdf()
        libs.utils.progress_msg(
            f"Time : {round((time.perf_counter_ns() - start_time_process)/1000000000,2) :10.2f} s"
        )

    # Store the document structure from the parser result.
    if args[libs.cfg.RUN_ACTION_STORE_FROM_PARSER]:
        start_time_process = time.perf_counter_ns()
        libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_PARSER
        process_store_from_parser()
        libs.utils.progress_msg(
            f"Time : {round((time.perf_counter_ns() - start_time_process)/1000000000,2) :10.2f} s"
        )

    # Disconnect from the database.
    db.orm.connection.disconnect_db()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text and metadata from pdf documents.
# -----------------------------------------------------------------------------
def process_extract_text_from_pdf() -> None:
    """Extract text and metadata from pdf documents."""
    libs.cfg.run_action = libs.cfg.RUN_ACTION_TEXT_FROM_PDF
    libs.utils.progress_msg_empty_before(
        "Start: Extract text and metadata from pdf documents ... PDFlib TET"
    )
    libs.cfg.run_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_RUN,
        {
            db.cfg.DBC_ACTION: libs.cfg.run_action,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_START,
        },
    )
    preprocessor.pdflibdcr.extract_text_from_pdf()
    db.orm.dml.update_dbt_id(
        db.cfg.DBT_RUN,
        libs.cfg.run_id,
        {
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_END,
            db.cfg.DBC_TOTAL_TO_BE_PROCESSED: libs.cfg.total_to_be_processed,
            db.cfg.DBC_TOTAL_OK_PROCESSED: libs.cfg.total_ok_processed,
            db.cfg.DBC_TOTAL_ERRONEOUS: libs.cfg.total_erroneous,
        },
    )
    libs.utils.progress_msg("End  : Extract text and metadata from pdf documents ...")


# -----------------------------------------------------------------------------
# Process the inbox directory.
# -----------------------------------------------------------------------------
def process_inbox_directory() -> None:
    """Process the inbox directory."""
    libs.cfg.run_action = libs.cfg.RUN_ACTION_PROCESS_INBOX

    libs.utils.progress_msg_empty_before("Start: Process the inbox directory ... PyMuPDF [fitz]")

    libs.cfg.run_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_RUN,
        {
            db.cfg.DBC_ACTION: libs.cfg.run_action,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_START,
        },
    )

    preprocessor.inbox.process_inbox()

    db.orm.dml.update_dbt_id(
        db.cfg.DBT_RUN,
        libs.cfg.run_id,
        {
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_END,
            db.cfg.DBC_TOTAL_TO_BE_PROCESSED: libs.cfg.total_to_be_processed,
            db.cfg.DBC_TOTAL_OK_PROCESSED: libs.cfg.total_ok_processed,
            db.cfg.DBC_TOTAL_ERRONEOUS: libs.cfg.total_erroneous,
        },
    )

    libs.utils.progress_msg("End  : Process the inbox directory ...")


# -----------------------------------------------------------------------------
# Store the document structure from the parser result.
# -----------------------------------------------------------------------------
def process_store_from_parser() -> None:
    """Store the document structure from the parser result."""
    libs.cfg.run_action = libs.cfg.RUN_ACTION_STORE_FROM_PARSER

    libs.utils.progress_msg_empty_before(
        "Start: Store document structure ... defusedxml [xml.etree.ElementTree]"
    )

    libs.cfg.run_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_RUN,
        {
            db.cfg.DBC_ACTION: libs.cfg.run_action,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_START,
        },
    )

    preprocessor.parser.parse_tetml()

    db.orm.dml.update_dbt_id(
        db.cfg.DBT_RUN,
        libs.cfg.run_id,
        {
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_END,
            db.cfg.DBC_TOTAL_TO_BE_PROCESSED: libs.cfg.total_to_be_processed,
            db.cfg.DBC_TOTAL_OK_PROCESSED: libs.cfg.total_ok_processed,
            db.cfg.DBC_TOTAL_ERRONEOUS: libs.cfg.total_erroneous,
        },
    )

    libs.utils.progress_msg("End  : Store document structure ...")


# -----------------------------------------------------------------------------
# validate the configuration parameters.
# -----------------------------------------------------------------------------
def validate_config() -> None:
    """Validate the configuration parameters."""
    # -------------------------------------------------------------------------
    validate_config_delete_auxiliary_files()
    validate_config_directory_inbox()
    validate_config_directory_inbox_accepted()
    validate_config_directory_inbox_rejected()
    validate_config_ignore_duplicates()
    validate_config_pdf2image_type()
    validate_config_simulate_parser()
    validate_config_tesseract_timeout()
    validate_config_verbose()
    validate_config_verbose_parser()


# -----------------------------------------------------------------------------
# validate the configuration parameters - delete_auxiliary_files
# -----------------------------------------------------------------------------
def validate_config_delete_auxiliary_files() -> None:
    """Validate the configuration parameters - delete_auxiliary_files."""
    libs.cfg.is_delete_auxiliary_files = True

    if libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES in libs.cfg.config:
        if libs.cfg.config[libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES].lower() == "false":
            libs.cfg.is_delete_auxiliary_files = False


# -----------------------------------------------------------------------------
# validate the configuration parameters - directory_inbox
# -----------------------------------------------------------------------------
def validate_config_directory_inbox() -> None:
    """Validate the configuration parameters - directory_inbox."""
    if libs.cfg.DCR_CFG_DIRECTORY_INBOX in libs.cfg.config:
        libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX] = libs.utils.str_2_path(
            libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
        )

        libs.cfg.directory_inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    else:
        libs.utils.terminate_fatal(
            f"Missing configuration parameter '{libs.cfg.DCR_CFG_DIRECTORY_INBOX}'"
        )


# -----------------------------------------------------------------------------
# validate the configuration parameters - directory_inbox_accepted
# -----------------------------------------------------------------------------
def validate_config_directory_inbox_accepted() -> None:
    """Validate the configuration parameters - directory_inbox_accepted."""
    if libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED in libs.cfg.config:
        libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED] = libs.utils.str_2_path(
            libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
        )

        libs.cfg.directory_inbox_accepted = libs.cfg.config[
            libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED
        ]
    else:
        libs.utils.terminate_fatal(
            f"Missing configuration parameter '{libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED}'"
        )


# -----------------------------------------------------------------------------
# validate the configuration parameters - directory_inbox_rejected
# -----------------------------------------------------------------------------
def validate_config_directory_inbox_rejected() -> None:
    """Validate the configuration parameters - directory_inbox_rejected."""
    if libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED in libs.cfg.config:
        libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED] = libs.utils.str_2_path(
            libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]
        )

        libs.cfg.directory_inbox_rejected = libs.cfg.config[
            libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED
        ]
    else:
        libs.utils.terminate_fatal(
            f"Missing configuration parameter '{libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED}'"
        )


# -----------------------------------------------------------------------------
# validate the configuration parameters - ignore_duplicates
# -----------------------------------------------------------------------------
def validate_config_ignore_duplicates() -> None:
    """Validate the configuration parameters - ignore_duplicates."""
    libs.cfg.is_ignore_duplicates = False

    if libs.cfg.DCR_CFG_IGNORE_DUPLICATES in libs.cfg.config:
        if libs.cfg.config[libs.cfg.DCR_CFG_IGNORE_DUPLICATES].lower() == "true":
            libs.cfg.is_ignore_duplicates = True


# -----------------------------------------------------------------------------
# validate the configuration parameters - pdf2image_type
# -----------------------------------------------------------------------------
def validate_config_pdf2image_type() -> None:
    """Validate the configuration parameters - pdf2image_type."""
    libs.cfg.pdf2image_type = libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_JPEG

    if libs.cfg.DCR_CFG_PDF2IMAGE_TYPE in libs.cfg.config:
        libs.cfg.pdf2image_type = libs.cfg.config[libs.cfg.DCR_CFG_PDF2IMAGE_TYPE]
        if libs.cfg.pdf2image_type not in [
            libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_JPEG,
            libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_PNG,
        ]:
            libs.utils.terminate_fatal(
                f"Invalid configuration parameter value for parameter "
                f"'pdf2image_type': '{libs.cfg.pdf2image_type}'"
            )


# -----------------------------------------------------------------------------
# validate the configuration parameters - simulate_parser
# -----------------------------------------------------------------------------
def validate_config_simulate_parser() -> None:
    """Validate the configuration parameters - simulate_parser."""
    libs.cfg.is_simulate_parser = False

    if libs.cfg.DCR_CFG_SIMULATE_PARSER in libs.cfg.config:
        if libs.cfg.config[libs.cfg.DCR_CFG_SIMULATE_PARSER].lower() == "true":
            libs.cfg.is_simulate_parser = True


# -----------------------------------------------------------------------------
# validate the configuration parameters - tesseract_timeout
# -----------------------------------------------------------------------------
def validate_config_tesseract_timeout() -> None:
    """Validate the configuration parameters - tesseract_timeout."""
    libs.cfg.tesseract_timeout = 30

    if libs.cfg.DCR_CFG_TESSERACT_TIMEOUT in libs.cfg.config:
        libs.cfg.tesseract_timeout = int(libs.cfg.config[libs.cfg.DCR_CFG_TESSERACT_TIMEOUT])


# -----------------------------------------------------------------------------
# validate the configuration parameters - verbose
# -----------------------------------------------------------------------------
def validate_config_verbose() -> None:
    """Validate the configuration parameters - verbose."""
    libs.cfg.is_verbose = True

    if libs.cfg.DCR_CFG_VERBOSE in libs.cfg.config:
        if libs.cfg.config[libs.cfg.DCR_CFG_VERBOSE].lower() == "false":
            libs.cfg.is_verbose = False


# -----------------------------------------------------------------------------
# validate the configuration parameters - verbose_parser
# -----------------------------------------------------------------------------
def validate_config_verbose_parser() -> None:
    """Validate the configuration parameters - verbose_parser."""
    libs.cfg.verbose_parser = "none"

    if libs.cfg.DCR_CFG_VERBOSE_PARSER in libs.cfg.config:
        if libs.cfg.config[libs.cfg.DCR_CFG_VERBOSE_PARSER].lower() in ["all", "text"]:
            libs.cfg.verbose_parser = libs.cfg.config[libs.cfg.DCR_CFG_VERBOSE_PARSER].lower()


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # not testable
    main(sys.argv)
