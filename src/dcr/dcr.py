"""Module dcr: Entry Point Functionality.

This is the entry point to the application DCR.
"""
import locale
import logging
import logging.config
import sys
import time
import typing

import db.cfg
import db.driver
import db.orm.connection
import db.orm.dml
import libs.cfg
import libs.utils
import nlp.tokenizer
import pp.inbox
import pp.pandoc_dcr
import pp.parser
import pp.pdf2image_dcr
import pp.pdflib_dcr
import pp.tesseract_dcr
import setup.config
import sqlalchemy
import yaml


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

    if libs.cfg.config.dcr_version != current_version:
        libs.utils.terminate_fatal(
            f"Current database version is '{current_version}' - but expected version is '"
            f"{libs.cfg.config.dcr_version}''"
        )

    libs.utils.progress_msg(f"The current version of database is '{current_version}'")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


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
        libs.cfg.RUN_ACTION_TOKENIZE: False,
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
            args[libs.cfg.RUN_ACTION_TOKENIZE] = True
        elif arg in (
            libs.cfg.RUN_ACTION_CREATE_DB,
            libs.cfg.RUN_ACTION_IMAGE_2_PDF,
            libs.cfg.RUN_ACTION_NON_PDF_2_PDF,
            libs.cfg.RUN_ACTION_PDF_2_IMAGE,
            libs.cfg.RUN_ACTION_PROCESS_INBOX,
            libs.cfg.RUN_ACTION_STORE_FROM_PARSER,
            libs.cfg.RUN_ACTION_TEXT_FROM_PDF,
            libs.cfg.RUN_ACTION_TOKENIZE,
            libs.cfg.RUN_ACTION_UPGRADE_DB,
        ):
            args[arg] = True
        else:
            libs.utils.terminate_fatal(f"Unknown command line argument='{argv[i]}'")

    libs.utils.progress_msg("The command line arguments are validated and loaded")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    return args


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

    libs.utils.progress_msg_core("The logger is configured and ready")


# -----------------------------------------------------------------------------
# Load the data from the database table 'language'.
# -----------------------------------------------------------------------------
def load_data_from_dbt_language() -> None:
    """Load the data from the database table 'language'."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = sqlalchemy.Table(
        db.cfg.DBT_LANGUAGE,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    libs.cfg.languages_pandoc = {}
    libs.cfg.languages_spacy = {}
    libs.cfg.languages_tesseract = {}

    with db.cfg.db_orm_engine.connect() as conn:
        rows = conn.execute(
            sqlalchemy.select(
                dbt.c.id, dbt.c.code_pandoc, dbt.c.code_spacy, dbt.c.code_tesseract
            ).where(
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
def main(argv: typing.List[str]) -> None:
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

    # Load the configuration parameters.
    libs.cfg.config = setup.config.Config()

    # Load the command line arguments.
    args = get_args(argv)

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
    pp.tesseract_dcr.convert_image_2_pdf()
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

    libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_PYPDF2

    libs.utils.progress_msg_empty_before("Start: Reunite the related pdf files ... PyPDF2")
    libs.cfg.run_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_RUN,
        {
            db.cfg.DBC_ACTION: libs.cfg.run_action,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_START,
        },
    )
    pp.tesseract_dcr.reunite_pdfs()
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
    pp.pandoc_dcr.convert_non_pdf_2_pdf()
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
    pp.pdf2image_dcr.convert_pdf_2_image()
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
        process_store_from_parser()
        libs.utils.progress_msg(
            f"Time : {round((time.perf_counter_ns() - start_time_process)/1000000000,2) :10.2f} s"
        )

    # Create document token.
    if args[libs.cfg.RUN_ACTION_TOKENIZE]:
        start_time_process = time.perf_counter_ns()
        libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_TOKENIZE
        process_tokenize()
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
    pp.pdflib_dcr.extract_text_from_pdf()
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

    pp.inbox.process_inbox()

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

    pp.parser.parse_tetml()

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
# Create document tokens.
# -----------------------------------------------------------------------------
def process_tokenize() -> None:
    """Create document tokens."""
    libs.cfg.run_action = libs.cfg.RUN_ACTION_TOKENIZE

    libs.utils.progress_msg_empty_before("Start: Create document tokens ... SpaCy")

    libs.cfg.run_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_RUN,
        {
            db.cfg.DBC_ACTION: libs.cfg.run_action,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: db.cfg.RUN_STATUS_START,
        },
    )

    nlp.tokenizer.tokenize()

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

    libs.utils.progress_msg("End  : Create document tokens ...")


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # not testable
    main(sys.argv)
