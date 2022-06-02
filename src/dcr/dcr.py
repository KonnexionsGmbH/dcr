"""Module dcr: Entry Point Functionality.

This is the entry point to the application DCR.
"""
import locale
import logging
import logging.config
import sys
import time

import cfg.cls_setup
import cfg.glob
import db.cls_db_core
import db.cls_language
import db.cls_run
import db.cls_version
import nlp.parser
import nlp.pdflib_dcr
import nlp.tokenizer
import pp.inbox
import pp.pandoc_dcr
import pp.pdf2image_dcr
import pp.tesseract_dcr
import sqlalchemy
import utils
import yaml

# -----------------------------------------------------------------------------
# Class variables.
# -----------------------------------------------------------------------------
DCR_ARGV_0: str = "src/dcr/dcr.py"

LOCALE: str = "en_US.UTF-8"

LOGGER_CFG_FILE: str = "logging_cfg.yaml"


# -----------------------------------------------------------------------------
# Check that the database version is up to date.
# -----------------------------------------------------------------------------
def check_db_up_to_date() -> None:
    """Check that the database version is up-to-date."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    if cfg.glob.db_core.db_orm_engine is None:
        utils.terminate_fatal(
            "The database does not yet exist.",
        )

    if not sqlalchemy.inspect(cfg.glob.db_core.db_orm_engine).has_table(db.cls_db_core.DBCore.DBT_VERSION):
        utils.terminate_fatal(
            "The database table 'version' does not yet exist.",
        )

    current_version: str = db.cls_version.Version.select_version_version_unique()

    if cfg.cls_setup.Setup.DCR_VERSION != current_version:
        utils.terminate_fatal(
            f"Current database version is '{current_version}' - but expected version is '"
            f"{cfg.cls_setup.Setup.DCR_VERSION}''"
        )

    utils.progress_msg(f"The current version of database is '{current_version}'")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Load the command line arguments into memory.
# -----------------------------------------------------------------------------
def get_args(argv: list[str]) -> dict[str, bool]:
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
        n_2_p - Convert non-pdf documents to pdf documents:             Pandoc
        ocr   - Convert image files to pdf documents:               Tesseract OCR / Tex Live.
        p_2_i - Convert pdf documents to image files:               pdf2image / Poppler.
        p_i   - Process the inbox directory.
        s_p_j - Store the parser result in a JSON file.
        tet   - Extract text and metadata from pdf documents:       PDFlib TET.
        tkn   - Create document tokens:                             spaCy.

    With the option all, the following process steps are executed
    in this order:

        1. p_i
        2. p_2_i
        3. n_2_p
        4. ocr
        5. tet
        6. s_p_j
        7. tkn

    Args:
        argv (list[str]): Command line arguments.

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
        db.cls_run.Run.ACTION_CODE_CREATE_DB: False,
        db.cls_run.Run.ACTION_CODE_INBOX: False,
        db.cls_run.Run.ACTION_CODE_PANDOC: False,
        db.cls_run.Run.ACTION_CODE_PARSER: False,
        db.cls_run.Run.ACTION_CODE_PDF2IMAGE: False,
        db.cls_run.Run.ACTION_CODE_PDFLIB: False,
        db.cls_run.Run.ACTION_CODE_TESSERACT: False,
        db.cls_run.Run.ACTION_CODE_TOKENIZE: False,
        db.cls_run.Run.ACTION_CODE_UPGRADE_DB: False,
    }

    for i in range(1, num):
        arg = argv[i].lower()
        if arg == db.cls_run.Run.ACTION_CODE_ALL_COMPLETE:
            args[db.cls_run.Run.ACTION_CODE_INBOX] = True
            args[db.cls_run.Run.ACTION_CODE_PANDOC] = True
            args[db.cls_run.Run.ACTION_CODE_PARSER] = True
            args[db.cls_run.Run.ACTION_CODE_PDF2IMAGE] = True
            args[db.cls_run.Run.ACTION_CODE_PDFLIB] = True
            args[db.cls_run.Run.ACTION_CODE_TESSERACT] = True
            args[db.cls_run.Run.ACTION_CODE_TOKENIZE] = True
        elif arg in (
            db.cls_run.Run.ACTION_CODE_CREATE_DB,
            db.cls_run.Run.ACTION_CODE_INBOX,
            db.cls_run.Run.ACTION_CODE_PANDOC,
            db.cls_run.Run.ACTION_CODE_PARSER,
            db.cls_run.Run.ACTION_CODE_PDF2IMAGE,
            db.cls_run.Run.ACTION_CODE_PDFLIB,
            db.cls_run.Run.ACTION_CODE_TESSERACT,
            db.cls_run.Run.ACTION_CODE_TOKENIZE,
            db.cls_run.Run.ACTION_CODE_UPGRADE_DB,
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
    with open(LOGGER_CFG_FILE, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
        log_config = yaml.safe_load(file_handle.read())

    logging.config.dictConfig(log_config)
    cfg.glob.logger = logging.getLogger("dcr.py")
    cfg.glob.logger.setLevel(logging.DEBUG)

    utils.progress_msg_core("The logger is configured and ready")


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def main(argv: list[str]) -> None:
    """Entry point.

    The processes to be carried out are selected via command line arguments.

    Args:
        argv (list[str]): Command line arguments.
    """
    # Initialise the logging functionality.
    initialise_logger()

    cfg.glob.logger.debug(cfg.glob.LOGGER_START)
    cfg.glob.logger.info("Start dcr.py")

    print("Start dcr.py")

    locale.setlocale(locale.LC_ALL, LOCALE)

    # Load the configuration parameters.
    cfg.glob.setup = cfg.cls_setup.Setup()

    # Load the command line arguments.
    args = get_args(argv)

    if args[db.cls_run.Run.ACTION_CODE_CREATE_DB]:
        # Create the database.
        utils.progress_msg_empty_before("Start: Create the database ...")
        cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)
        cfg.glob.db_core.create_database()
        utils.progress_msg("End  : Create the database ...")
    elif args[db.cls_run.Run.ACTION_CODE_UPGRADE_DB]:
        # Upgrade the database.
        utils.progress_msg_empty_before("Start: Upgrade the database ...")
        cfg.glob.db_core = db.cls_db_core.DBCore()
        cfg.glob.db_core.upgrade_database()
        utils.progress_msg("End  : Upgrade the database ...")
    else:
        # Process the documents.
        process_documents(args)

    print("End   dcr.py")

    cfg.glob.logger.info("End   dcr.py")
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert image files to pdf documents.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_convert_image_2_pdf() -> None:
    """Convert image files to pdf documents."""
    utils.progress_msg_empty_before("Start: Convert image files to pdf documents ... Tesseract OCR")

    cfg.glob.run = db.cls_run.Run(action_code=db.cls_run.Run.ACTION_CODE_TESSERACT)

    pp.tesseract_dcr.convert_image_2_pdf()

    cfg.glob.run.finalise()

    utils.progress_msg("End  : Convert image files to pdf documents ...")

    utils.progress_msg_empty_before("Start: Reunite the related pdf documents ... PyPDF2")

    cfg.glob.run = db.cls_run.Run(action_code=db.cls_run.Run.ACTION_CODE_PYPDF2)

    pp.tesseract_dcr.reunite_pdfs()

    cfg.glob.run.finalise()

    utils.progress_msg("End  : Reunite the related pdf documents ...")


# -----------------------------------------------------------------------------
# Convert non-pdf documents to pdf documents.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_convert_non_pdf_2_pdf() -> None:
    """Convert non-pdf documents to pdf documents."""
    utils.progress_msg_empty_before("Start: Convert non-pdf documents to pdf documents ... Pandoc [TeX Live]")

    cfg.glob.run = db.cls_run.Run(action_code=db.cls_run.Run.ACTION_CODE_PANDOC)

    pp.pandoc_dcr.convert_non_pdf_2_pdf()

    cfg.glob.run.finalise()

    utils.progress_msg("End  : Convert non-pdf documents to pdf documents ...")


# -----------------------------------------------------------------------------
# Convert pdf documents to image files.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_convert_pdf_2_image() -> None:
    """Convert pdf documents to image files."""
    utils.progress_msg_empty_before("Start: Convert pdf documents to image files ... pdf2image [Poppler]")

    cfg.glob.run = db.cls_run.Run(action_code=db.cls_run.Run.ACTION_CODE_PDF2IMAGE)

    pp.pdf2image_dcr.convert_pdf_2_image()

    cfg.glob.run.finalise()

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
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # Check the version of the database.
    check_db_up_to_date()

    # Load the data from the database table 'language'.
    db.cls_language.Language.load_data_from_dbt_language()

    # Process the documents in the inbox file directory.
    if args[db.cls_run.Run.ACTION_CODE_INBOX]:
        start_time_process = time.perf_counter_ns()
        process_inbox_directory()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Convert the scanned image pdf documents to image files.
    if args[db.cls_run.Run.ACTION_CODE_PDF2IMAGE]:
        start_time_process = time.perf_counter_ns()
        process_convert_pdf_2_image()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Convert the image files to pdf documents.
    if args[db.cls_run.Run.ACTION_CODE_TESSERACT]:
        start_time_process = time.perf_counter_ns()
        process_convert_image_2_pdf()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Convert the non-pdf documents to pdf documents.
    if args[db.cls_run.Run.ACTION_CODE_PANDOC]:
        start_time_process = time.perf_counter_ns()
        process_convert_non_pdf_2_pdf()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Extract text and metadata from pdf documents.
    if args[db.cls_run.Run.ACTION_CODE_PDFLIB]:
        start_time_process = time.perf_counter_ns()
        process_extract_text_from_pdf()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Store the document structure from the parser result.
    if args[db.cls_run.Run.ACTION_CODE_PARSER]:
        start_time_process = time.perf_counter_ns()
        process_store_parse_result_in_json()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Create document token.
    if args[db.cls_run.Run.ACTION_CODE_TOKENIZE]:
        start_time_process = time.perf_counter_ns()
        process_tokenize()
        utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Disconnect from the database.
    cfg.glob.db_core.disconnect_db()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text and metadata from pdf documents.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_extract_text_from_pdf() -> None:
    """Extract text and metadata from pdf documents."""
    utils.progress_msg_empty_before("Start: Extract text and metadata from pdf documents ... PDFlib TET")

    cfg.glob.run = db.cls_run.Run(action_code=db.cls_run.Run.ACTION_CODE_PDFLIB)

    nlp.pdflib_dcr.extract_text_from_pdf()

    cfg.glob.run.finalise()

    utils.progress_msg("End  : Extract text and metadata from pdf documents ...")


# -----------------------------------------------------------------------------
# Process the inbox directory.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_inbox_directory() -> None:
    """Process the inbox directory."""
    utils.progress_msg_empty_before("Start: Process the inbox directory ... PyMuPDF [fitz]")

    cfg.glob.run = db.cls_run.Run(action_code=db.cls_run.Run.ACTION_CODE_INBOX)

    pp.inbox.process_inbox()

    cfg.glob.run.finalise()

    utils.progress_msg("End  : Process the inbox directory ...")


# -----------------------------------------------------------------------------
# Store the document structure from the parser result.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_store_parse_result_in_json() -> None:
    """Store the document structure from the parser result."""
    utils.progress_msg_empty_before("Start: Store document structure ... defusedxml [xml.etree.ElementTree]")

    cfg.glob.run = db.cls_run.Run(action_code=db.cls_run.Run.ACTION_CODE_PARSER)

    nlp.parser.parse_tetml()

    cfg.glob.run.finalise()

    utils.progress_msg("End  : Store document structure ...")


# -----------------------------------------------------------------------------
# Create document tokens.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_tokenize() -> None:
    """Create document tokens."""
    utils.progress_msg_empty_before("Start: Create document tokens ... spaCy")

    cfg.glob.run = db.cls_run.Run(action_code=db.cls_run.Run.ACTION_CODE_TOKENIZE)

    nlp.tokenizer.tokenize()

    cfg.glob.run.finalise()

    utils.progress_msg("End  : Create document tokens ...")


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # not testable
    main(sys.argv)
