"""Module dcr: Entry Point Functionality.

This is the entry point to the application DCR.
"""
import locale
import logging
import logging.config
import sys
import time
import typing

import cfg.glob
import cfg.setup
import db.dml
import db.driver
import nlp.tokenizer
import pp.inbox
import pp.pandoc_dcr
import pp.parser
import pp.pdf2image_dcr
import pp.pdflib_dcr
import pp.tesseract_dcr
import sqlalchemy
import utils
import yaml


# -----------------------------------------------------------------------------
# Check that the database version is up to date.
# -----------------------------------------------------------------------------
def check_db_up_to_date() -> None:
    """Check that the database version is up-to-date."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    if cfg.glob.db_orm_engine is None:
        utils.terminate_fatal(
            "The database does not yet exist.",
        )

    if not sqlalchemy.inspect(cfg.glob.db_orm_engine).has_table(cfg.glob.DBT_VERSION):
        utils.terminate_fatal(
            "The database table 'version' does not yet exist.",
        )

    current_version = db.dml.select_version_version_unique()

    if cfg.glob.setup.dcr_version != current_version:
        utils.terminate_fatal(
            f"Current database version is '{current_version}' - but expected version is '"
            f"{cfg.glob.setup.dcr_version}''"
        )

    utils.progress_msg(f"The current version of database is '{current_version}'")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Load the command line arguments into memory.
# -----------------------------------------------------------------------------
def get_args(argv: typing.List[str]) -> dict[str, bool]:
    """Load the command line arguments.

    The command line arguments define the process steps to be executed.
    The valid arguments are:

        all   - Run the complete core processing of all new documents.
        db_c  - Create the database.
        db_u  - Upgrade the database.
        m_d   - Run the installation of the necessary 3rd party packages
                for development and run the development ecosystem.
        m_p   - Run the installation of the necessary 3rd party packages
                for production and compile all packages and modules.
        n_2_p - Convert non-pdf documents to pdf files:             Pandoc
        ocr   - Convert image documents to pdf files:               Tesseract OCR / Tex Live.
        p_2_i - Convert pdf documents to image files:               pdf2image / Poppler.
        p_i   - Process the inbox directory.
        s_f_p - Store the document structure from the parser result.
        tet   - Extract text and metadata from pdf documents:       PDFlib TET.
        tkn   - Create document tokens:                             SpaCy.

    With the option all, the following process steps are executed
    in this order:

        1. p_i
        2. p_2_i
        3. n_2_p
        4. ocr
        5. tet
        6. s_f_p
        7. tkn

    Args:
        argv (List[str]): Command line arguments.

    Returns:
        dict[str, bool]: The processing steps based on CLI arguments.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    num = len(argv)

    if num == 0:
        utils.terminate_fatal("No command line arguments found")

    if num == 1:
        utils.terminate_fatal("The specific command line arguments are missing")

    args = {
        cfg.glob.RUN_ACTION_CREATE_DB: False,
        cfg.glob.RUN_ACTION_IMAGE_2_PDF: False,
        cfg.glob.RUN_ACTION_NON_PDF_2_PDF: False,
        cfg.glob.RUN_ACTION_PDF_2_IMAGE: False,
        cfg.glob.RUN_ACTION_PROCESS_INBOX: False,
        cfg.glob.RUN_ACTION_STORE_FROM_PARSER: False,
        cfg.glob.RUN_ACTION_TEXT_FROM_PDF: False,
        cfg.glob.RUN_ACTION_TOKENIZE: False,
        cfg.glob.RUN_ACTION_UPGRADE_DB: False,
    }

    for i in range(1, num):
        arg = argv[i].lower()
        if arg == cfg.glob.RUN_ACTION_ALL_COMPLETE:
            args[cfg.glob.RUN_ACTION_IMAGE_2_PDF] = True
            args[cfg.glob.RUN_ACTION_NON_PDF_2_PDF] = True
            args[cfg.glob.RUN_ACTION_PDF_2_IMAGE] = True
            args[cfg.glob.RUN_ACTION_PROCESS_INBOX] = True
            args[cfg.glob.RUN_ACTION_STORE_FROM_PARSER] = True
            args[cfg.glob.RUN_ACTION_TEXT_FROM_PDF] = True
            args[cfg.glob.RUN_ACTION_TOKENIZE] = True
        elif arg in (
            cfg.glob.RUN_ACTION_CREATE_DB,
            cfg.glob.RUN_ACTION_IMAGE_2_PDF,
            cfg.glob.RUN_ACTION_NON_PDF_2_PDF,
            cfg.glob.RUN_ACTION_PDF_2_IMAGE,
            cfg.glob.RUN_ACTION_PROCESS_INBOX,
            cfg.glob.RUN_ACTION_STORE_FROM_PARSER,
            cfg.glob.RUN_ACTION_TEXT_FROM_PDF,
            cfg.glob.RUN_ACTION_TOKENIZE,
            cfg.glob.RUN_ACTION_UPGRADE_DB,
        ):
            args[arg] = True
        else:
            utils.terminate_fatal(f"Unknown command line argument='{argv[i]}'")

    utils.progress_msg("The command line arguments are validated and loaded")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    return args


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def initialise_logger() -> None:
    """Initialise the root logging functionality."""
    with open(cfg.glob.LOGGER_CFG_FILE, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file:
        log_config = yaml.safe_load(file.read())

    logging.config.dictConfig(log_config)
    cfg.glob.logger = logging.getLogger("dcr.py")
    cfg.glob.logger.setLevel(logging.DEBUG)

    utils.progress_msg_core("The logger is configured and ready")


# -----------------------------------------------------------------------------
# Load the data from the database table 'language'.
# -----------------------------------------------------------------------------
def load_data_from_dbt_language() -> None:
    """Load the data from the database table 'language'."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    dbt = sqlalchemy.Table(
        cfg.glob.DBT_LANGUAGE,
        cfg.glob.db_orm_metadata,
        autoload_with=cfg.glob.db_orm_engine,
    )

    cfg.glob.languages_pandoc = {}
    cfg.glob.languages_spacy = {}
    cfg.glob.languages_tesseract = {}

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = conn.execute(
            sqlalchemy.select(dbt.c.id, dbt.c.code_pandoc, dbt.c.code_spacy, dbt.c.code_tesseract).where(
                dbt.c.active,
            )
        )

        for row in rows:
            cfg.glob.languages_pandoc[row.id] = row.code_pandoc
            cfg.glob.languages_spacy[row.id] = row.code_spacy
            cfg.glob.languages_tesseract[row.id] = row.code_tesseract

        conn.close()

    utils.progress_msg(f"Available languages for Pandoc        '{cfg.glob.languages_pandoc}'")
    utils.progress_msg(f"Available languages for SpaCy         '{cfg.glob.languages_spacy}'")
    utils.progress_msg(f"Available languages for Tesseract OCR '{cfg.glob.languages_tesseract}'")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def main(argv: typing.List[str]) -> None:
    """Entry point.

    The processes to be carried out are selected via command line arguments.

    Args:
        argv (List[str]): Command line arguments.
    """
    # Initialise the logging functionality.
    initialise_logger()

    cfg.glob.logger.debug(cfg.glob.LOGGER_START)
    cfg.glob.logger.info("Start dcr.py")

    print("Start dcr.py")

    locale.setlocale(locale.LC_ALL, cfg.glob.LOCALE)

    # Load the configuration parameters.
    cfg.glob.setup = cfg.setup.Setup()

    # Load the command line arguments.
    args = get_args(argv)

    if args[cfg.glob.RUN_ACTION_CREATE_DB]:
        # Create the database.
        utils.progress_msg_empty_before("Start: Create the database ...")
        db.driver.create_database()
        utils.progress_msg("End  : Create the database ...")
    elif args[cfg.glob.RUN_ACTION_UPGRADE_DB]:
        # Upgrade the database.
        utils.progress_msg_empty_before("Start: Upgrade the database ...")
        db.driver.upgrade_database()
        utils.progress_msg("End  : Upgrade the database ...")
    else:
        # Process the documents.
        process_documents(args)

    print("End   dcr.py")

    cfg.glob.logger.info("End   dcr.py")
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert image documents to pdf files.
# -----------------------------------------------------------------------------
def process_convert_image_2_pdf() -> None:
    """Convert image documents to pdf files."""
    cfg.glob.run_action = cfg.glob.RUN_ACTION_IMAGE_2_PDF

    utils.progress_msg_empty_before("Start: Convert image documents to pdf files ... Tesseract OCR")
    cfg.glob.run_id = db.dml.insert_dbt_row(
        cfg.glob.DBT_RUN,
        {
            cfg.glob.DBC_ACTION: cfg.glob.run_action,
            cfg.glob.DBC_RUN_ID: cfg.glob.run_run_id,
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_START,
        },
    )
    pp.tesseract_dcr.convert_image_2_pdf()
    db.dml.update_dbt_id(
        cfg.glob.DBT_RUN,
        cfg.glob.run_id,
        {
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_END,
            cfg.glob.DBC_TOTAL_TO_BE_PROCESSED: cfg.glob.total_to_be_processed,
            cfg.glob.DBC_TOTAL_OK_PROCESSED: cfg.glob.total_ok_processed,
            cfg.glob.DBC_TOTAL_ERRONEOUS: cfg.glob.total_erroneous,
        },
    )
    utils.progress_msg("End  : Convert image documents to pdf files ...")

    cfg.glob.document_current_step = cfg.glob.DOCUMENT_STEP_PYPDF2

    utils.progress_msg_empty_before("Start: Reunite the related pdf files ... PyPDF2")
    cfg.glob.run_id = db.dml.insert_dbt_row(
        cfg.glob.DBT_RUN,
        {
            cfg.glob.DBC_ACTION: cfg.glob.run_action,
            cfg.glob.DBC_RUN_ID: cfg.glob.run_run_id,
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_START,
        },
    )
    pp.tesseract_dcr.reunite_pdfs()
    db.dml.update_dbt_id(
        cfg.glob.DBT_RUN,
        cfg.glob.run_id,
        {
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_END,
            cfg.glob.DBC_TOTAL_TO_BE_PROCESSED: cfg.glob.total_to_be_processed,
            cfg.glob.DBC_TOTAL_OK_PROCESSED: cfg.glob.total_ok_processed,
            cfg.glob.DBC_TOTAL_ERRONEOUS: cfg.glob.total_erroneous,
        },
    )
    utils.progress_msg("End  : Reunite the related pdf files ...")


# -----------------------------------------------------------------------------
# Convert non-pdf documents to pdf files.
# -----------------------------------------------------------------------------
def process_convert_non_pdf_2_pdf() -> None:
    """Convert non-pdf documents to pdf files."""
    cfg.glob.run_action = cfg.glob.RUN_ACTION_NON_PDF_2_PDF
    utils.progress_msg_empty_before("Start: Convert non-pdf documents to pdf files ... Pandoc [TeX Live]")
    cfg.glob.run_id = db.dml.insert_dbt_row(
        cfg.glob.DBT_RUN,
        {
            cfg.glob.DBC_ACTION: cfg.glob.run_action,
            cfg.glob.DBC_RUN_ID: cfg.glob.run_run_id,
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_START,
        },
    )
    pp.pandoc_dcr.convert_non_pdf_2_pdf()
    db.dml.update_dbt_id(
        cfg.glob.DBT_RUN,
        cfg.glob.run_id,
        {
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_END,
            cfg.glob.DBC_TOTAL_TO_BE_PROCESSED: cfg.glob.total_to_be_processed,
            cfg.glob.DBC_TOTAL_OK_PROCESSED: cfg.glob.total_ok_processed,
            cfg.glob.DBC_TOTAL_ERRONEOUS: cfg.glob.total_erroneous,
        },
    )
    utils.progress_msg("End  : Convert non-pdf documents to pdf files ...")


# -----------------------------------------------------------------------------
# Convert pdf documents to image files.
# -----------------------------------------------------------------------------
def process_convert_pdf_2_image() -> None:
    """Convert pdf documents to image files."""
    cfg.glob.run_action = cfg.glob.RUN_ACTION_PDF_2_IMAGE
    utils.progress_msg_empty_before("Start: Convert pdf documents to image files ... pdf2image [Poppler]")
    cfg.glob.run_id = db.dml.insert_dbt_row(
        cfg.glob.DBT_RUN,
        {
            cfg.glob.DBC_ACTION: cfg.glob.run_action,
            cfg.glob.DBC_RUN_ID: cfg.glob.run_run_id,
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_START,
        },
    )
    pp.pdf2image_dcr.convert_pdf_2_image()
    db.dml.update_dbt_id(
        cfg.glob.DBT_RUN,
        cfg.glob.run_id,
        {
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_END,
            cfg.glob.DBC_TOTAL_TO_BE_PROCESSED: cfg.glob.total_to_be_processed,
            cfg.glob.DBC_TOTAL_OK_PROCESSED: cfg.glob.total_ok_processed,
            cfg.glob.DBC_TOTAL_ERRONEOUS: cfg.glob.total_erroneous,
        },
    )
    utils.progress_msg("End  : Convert pdf documents to image files ...")


# -----------------------------------------------------------------------------
# Process the documents.
# -----------------------------------------------------------------------------
def process_documents(args: dict[str, bool]) -> None:
    """Process the documents.

    Args:
        args (dict[str, bool]): The processing steps based on CLI arguments.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # Connect to the database.
    db.driver.connect_db()

    # Check the version of the database.
    check_db_up_to_date()

    cfg.glob.run_run_id = db.dml.select_run_run_id_last() + 1

    # Load the data from the database table 'language'.
    load_data_from_dbt_language()

    # Process the documents in the inbox file directory.
    if args[cfg.glob.RUN_ACTION_PROCESS_INBOX]:
        start_time_process = time.perf_counter_ns()
        cfg.glob.document_current_step = cfg.glob.DOCUMENT_STEP_INBOX
        process_inbox_directory()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Convert the scanned image pdf documents to image files.
    if args[cfg.glob.RUN_ACTION_PDF_2_IMAGE]:
        start_time_process = time.perf_counter_ns()
        cfg.glob.document_current_step = cfg.glob.DOCUMENT_STEP_PDF2IMAGE
        process_convert_pdf_2_image()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Convert the image documents to pdf files.
    if args[cfg.glob.RUN_ACTION_IMAGE_2_PDF]:
        start_time_process = time.perf_counter_ns()
        cfg.glob.document_current_step = cfg.glob.DOCUMENT_STEP_TESSERACT
        process_convert_image_2_pdf()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Convert the non-pdf documents to pdf files.
    if args[cfg.glob.RUN_ACTION_NON_PDF_2_PDF]:
        start_time_process = time.perf_counter_ns()
        cfg.glob.document_current_step = cfg.glob.DOCUMENT_STEP_PANDOC
        process_convert_non_pdf_2_pdf()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Extract text and metadata from pdf documents.
    if args[cfg.glob.RUN_ACTION_TEXT_FROM_PDF]:
        start_time_process = time.perf_counter_ns()
        cfg.glob.document_current_step = cfg.glob.DOCUMENT_STEP_PDFLIB
        process_extract_text_from_pdf()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Store the document structure from the parser result.
    if args[cfg.glob.RUN_ACTION_STORE_FROM_PARSER]:
        start_time_process = time.perf_counter_ns()
        process_store_from_parser()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Create document token.
    if args[cfg.glob.RUN_ACTION_TOKENIZE]:
        start_time_process = time.perf_counter_ns()
        cfg.glob.document_current_step = cfg.glob.DOCUMENT_STEP_TOKENIZE
        process_tokenize()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Disconnect from the database.
    db.driver.disconnect_db()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text and metadata from pdf documents.
# -----------------------------------------------------------------------------
def process_extract_text_from_pdf() -> None:
    """Extract text and metadata from pdf documents."""
    cfg.glob.run_action = cfg.glob.RUN_ACTION_TEXT_FROM_PDF
    utils.progress_msg_empty_before("Start: Extract text and metadata from pdf documents ... PDFlib TET")
    cfg.glob.run_id = db.dml.insert_dbt_row(
        cfg.glob.DBT_RUN,
        {
            cfg.glob.DBC_ACTION: cfg.glob.run_action,
            cfg.glob.DBC_RUN_ID: cfg.glob.run_run_id,
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_START,
        },
    )
    pp.pdflib_dcr.extract_text_from_pdf()
    db.dml.update_dbt_id(
        cfg.glob.DBT_RUN,
        cfg.glob.run_id,
        {
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_END,
            cfg.glob.DBC_TOTAL_TO_BE_PROCESSED: cfg.glob.total_to_be_processed,
            cfg.glob.DBC_TOTAL_OK_PROCESSED: cfg.glob.total_ok_processed,
            cfg.glob.DBC_TOTAL_ERRONEOUS: cfg.glob.total_erroneous,
        },
    )
    utils.progress_msg("End  : Extract text and metadata from pdf documents ...")


# -----------------------------------------------------------------------------
# Process the inbox directory.
# -----------------------------------------------------------------------------
def process_inbox_directory() -> None:
    """Process the inbox directory."""
    cfg.glob.run_action = cfg.glob.RUN_ACTION_PROCESS_INBOX

    utils.progress_msg_empty_before("Start: Process the inbox directory ... PyMuPDF [fitz]")

    cfg.glob.run_id = db.dml.insert_dbt_row(
        cfg.glob.DBT_RUN,
        {
            cfg.glob.DBC_ACTION: cfg.glob.run_action,
            cfg.glob.DBC_RUN_ID: cfg.glob.run_run_id,
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_START,
        },
    )

    pp.inbox.process_inbox()

    db.dml.update_dbt_id(
        cfg.glob.DBT_RUN,
        cfg.glob.run_id,
        {
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_END,
            cfg.glob.DBC_TOTAL_TO_BE_PROCESSED: cfg.glob.total_to_be_processed,
            cfg.glob.DBC_TOTAL_OK_PROCESSED: cfg.glob.total_ok_processed,
            cfg.glob.DBC_TOTAL_ERRONEOUS: cfg.glob.total_erroneous,
        },
    )

    utils.progress_msg("End  : Process the inbox directory ...")


# -----------------------------------------------------------------------------
# Store the document structure from the parser result.
# -----------------------------------------------------------------------------
def process_store_from_parser() -> None:
    """Store the document structure from the parser result."""
    cfg.glob.run_action = cfg.glob.RUN_ACTION_STORE_FROM_PARSER

    utils.progress_msg_empty_before("Start: Store document structure ... defusedxml [xml.etree.ElementTree]")

    cfg.glob.run_id = db.dml.insert_dbt_row(
        cfg.glob.DBT_RUN,
        {
            cfg.glob.DBC_ACTION: cfg.glob.run_action,
            cfg.glob.DBC_RUN_ID: cfg.glob.run_run_id,
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_START,
        },
    )

    pp.parser.parse_tetml()

    db.dml.update_dbt_id(
        cfg.glob.DBT_RUN,
        cfg.glob.run_id,
        {
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_END,
            cfg.glob.DBC_TOTAL_TO_BE_PROCESSED: cfg.glob.total_to_be_processed,
            cfg.glob.DBC_TOTAL_OK_PROCESSED: cfg.glob.total_ok_processed,
            cfg.glob.DBC_TOTAL_ERRONEOUS: cfg.glob.total_erroneous,
        },
    )

    utils.progress_msg("End  : Store document structure ...")


# -----------------------------------------------------------------------------
# Create document tokens.
# -----------------------------------------------------------------------------
def process_tokenize() -> None:
    """Create document tokens."""
    cfg.glob.run_action = cfg.glob.RUN_ACTION_TOKENIZE

    utils.progress_msg_empty_before("Start: Create document tokens ... SpaCy")

    cfg.glob.run_id = db.dml.insert_dbt_row(
        cfg.glob.DBT_RUN,
        {
            cfg.glob.DBC_ACTION: cfg.glob.run_action,
            cfg.glob.DBC_RUN_ID: cfg.glob.run_run_id,
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_START,
        },
    )

    nlp.tokenizer.tokenize()

    db.dml.update_dbt_id(
        cfg.glob.DBT_RUN,
        cfg.glob.run_id,
        {
            cfg.glob.DBC_STATUS: cfg.glob.RUN_STATUS_END,
            cfg.glob.DBC_TOTAL_TO_BE_PROCESSED: cfg.glob.total_to_be_processed,
            cfg.glob.DBC_TOTAL_OK_PROCESSED: cfg.glob.total_ok_processed,
            cfg.glob.DBC_TOTAL_ERRONEOUS: cfg.glob.total_erroneous,
        },
    )

    utils.progress_msg("End  : Create document tokens ...")


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # not testable
    main(sys.argv)
