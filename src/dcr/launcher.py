# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module dcr: Entry Point Functionality.

This is the entry point to the application DCR.
"""
import locale
import logging
import logging.config
import sys
import time

import dcr_core.cls_nlp_core
import dcr_core.cls_setup
import dcr_core.core_glob
import dcr_core.core_utils
import sqlalchemy
import yaml

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_db_core
import dcr.db.cls_language
import dcr.db.cls_run
import dcr.db.cls_version
import dcr.nlp.parser
import dcr.nlp.pdflib
import dcr.nlp.tokenizer
import dcr.pp.inbox
import dcr.pp.pandoc
import dcr.pp.pdf2image
import dcr.pp.tesseract
import dcr.utils

# -----------------------------------------------------------------------------
# Class variables.
# -----------------------------------------------------------------------------
DCR_ARGV_0 = "src/dcr/launcher.py"

LOCALE = "en_US.UTF-8"

LOGGER_CFG_FILE = "logging_cfg.yaml"


# -----------------------------------------------------------------------------
# Check that the database version is up to date.
# -----------------------------------------------------------------------------
def check_db_up_to_date() -> None:
    """Check that the database version is up-to-date."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    if dcr.cfg.glob.db_core.db_orm_engine is None:
        dcr_core.core_utils.terminate_fatal(
            "The database does not yet exist.",
        )

    if not sqlalchemy.inspect(dcr.cfg.glob.db_core.db_orm_engine).has_table(dcr.db.cls_db_core.DBCore.DBT_VERSION):
        dcr_core.core_utils.terminate_fatal(
            "The database table 'version' does not yet exist.",
        )

    current_version = dcr.db.cls_version.Version.select_version_version_unique()

    if dcr_core.cls_setup.Setup.DCR_VERSION != current_version:
        dcr_core.core_utils.terminate_fatal(
            f"Current database version is '{current_version}' - but expected version is '" f"{dcr_core.cls_setup.Setup.DCR_VERSION}''"
        )

    dcr.utils.progress_msg(f"The current version of database is '{current_version}'")

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


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
        e_lt  - Export the line type rules.
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
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    num = len(argv)

    if num == 0:
        dcr_core.core_utils.terminate_fatal("No command line arguments found")

    if num == 1:
        dcr_core.core_utils.terminate_fatal("The specific command line arguments are missing")

    args = {
        dcr.db.cls_run.Run.ACTION_CODE_CREATE_DB: False,
        dcr.db.cls_run.Run.ACTION_CODE_EXPORT_LT_RULES: False,
        dcr.db.cls_run.Run.ACTION_CODE_INBOX: False,
        dcr.db.cls_run.Run.ACTION_CODE_PANDOC: False,
        dcr.db.cls_run.Run.ACTION_CODE_PARSER: False,
        dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE: False,
        dcr.db.cls_run.Run.ACTION_CODE_PDFLIB: False,
        dcr.db.cls_run.Run.ACTION_CODE_TESSERACT: False,
        dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE: False,
        dcr.db.cls_run.Run.ACTION_CODE_UPGRADE_DB: False,
    }

    for i in range(1, num):
        arg = argv[i].lower()
        if arg == dcr.db.cls_run.Run.ACTION_CODE_ALL_COMPLETE:
            args[dcr.db.cls_run.Run.ACTION_CODE_INBOX] = True
            args[dcr.db.cls_run.Run.ACTION_CODE_PANDOC] = True
            args[dcr.db.cls_run.Run.ACTION_CODE_PARSER] = True
            args[dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE] = True
            args[dcr.db.cls_run.Run.ACTION_CODE_PDFLIB] = True
            args[dcr.db.cls_run.Run.ACTION_CODE_TESSERACT] = True
            args[dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE] = True
        elif arg in (
            dcr.db.cls_run.Run.ACTION_CODE_CREATE_DB,
            dcr.db.cls_run.Run.ACTION_CODE_EXPORT_LT_RULES,
            dcr.db.cls_run.Run.ACTION_CODE_INBOX,
            dcr.db.cls_run.Run.ACTION_CODE_PANDOC,
            dcr.db.cls_run.Run.ACTION_CODE_PARSER,
            dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE,
            dcr.db.cls_run.Run.ACTION_CODE_PDFLIB,
            dcr.db.cls_run.Run.ACTION_CODE_TESSERACT,
            dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE,
            dcr.db.cls_run.Run.ACTION_CODE_UPGRADE_DB,
        ):
            args[arg] = True
        else:
            dcr_core.core_utils.terminate_fatal(f"Unknown command line argument='{argv[i]}'")

    dcr.utils.progress_msg("The command line arguments are validated and loaded")

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    return args


# -----------------------------------------------------------------------------
# Initialising the logging functionality.
# -----------------------------------------------------------------------------
def initialise_logger() -> None:
    """Initialise the root logging functionality."""
    with open(LOGGER_CFG_FILE, "r", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as file_handle:
        log_config = yaml.safe_load(file_handle.read())

    logging.config.dictConfig(log_config)
    dcr.cfg.glob.logger = logging.getLogger("launcher.py")
    dcr.cfg.glob.logger.setLevel(logging.DEBUG)

    dcr.utils.progress_msg_core("The logger is configured and ready")


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

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)
    dcr.cfg.glob.logger.info("Start launcher.py")

    print("Start launcher.py")

    locale.setlocale(locale.LC_ALL, LOCALE)

    # Load the configuration parameters.
    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # Load the command line arguments.
    args = get_args(argv)

    if args[dcr.db.cls_run.Run.ACTION_CODE_CREATE_DB]:
        # Create the database.
        dcr.utils.progress_msg_empty_before("Start: Create the database ...")
        dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore(is_admin=True)
        dcr.cfg.glob.db_core.create_database()
        dcr.utils.progress_msg("End  : Create the database ...")
    elif args[dcr.db.cls_run.Run.ACTION_CODE_UPGRADE_DB]:
        # Upgrade the database.
        dcr.utils.progress_msg_empty_before("Start: Upgrade the database ...")
        dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()
        dcr.cfg.glob.db_core.upgrade_database()
        dcr.utils.progress_msg("End  : Upgrade the database ...")
    else:
        # Process the documents.
        process_documents(args)

    print("End   launcher.py")

    dcr.cfg.glob.logger.info("End   launcher.py")
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert image files to pdf documents.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_convert_image_2_pdf() -> None:
    """Convert image files to pdf documents."""
    dcr.utils.progress_msg_empty_before("Start: Convert image files to pdf documents ... Tesseract OCR")

    dcr.cfg.glob.run = dcr.db.cls_run.Run(action_code=dcr.db.cls_run.Run.ACTION_CODE_TESSERACT)

    dcr.pp.tesseract.convert_image_2_pdf()

    dcr.cfg.glob.run.finalise()

    dcr.utils.progress_msg("End  : Convert image files to pdf documents ...")


# -----------------------------------------------------------------------------
# Convert non-pdf documents to pdf documents.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_convert_non_pdf_2_pdf() -> None:
    """Convert non-pdf documents to pdf documents."""
    dcr.utils.progress_msg_empty_before("Start: Convert non-pdf documents to pdf documents ... Pandoc [TeX Live]")

    dcr.cfg.glob.run = dcr.db.cls_run.Run(action_code=dcr.db.cls_run.Run.ACTION_CODE_PANDOC)

    dcr.pp.pandoc.convert_non_pdf_2_pdf()

    dcr.cfg.glob.run.finalise()

    dcr.utils.progress_msg("End  : Convert non-pdf documents to pdf documents ...")


# -----------------------------------------------------------------------------
# Convert pdf documents to image files.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_convert_pdf_2_image() -> None:
    """Convert pdf documents to image files."""
    dcr.utils.progress_msg_empty_before("Start: Convert pdf documents to image files ... pdf2image [Poppler]")

    dcr.cfg.glob.run = dcr.db.cls_run.Run(action_code=dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE)

    dcr.pp.pdf2image.convert_pdf_2_image()

    dcr.cfg.glob.run.finalise()

    dcr.utils.progress_msg("End  : Convert pdf documents to image files ...")


# -----------------------------------------------------------------------------
# Process the documents.
# -----------------------------------------------------------------------------
def process_documents(args: dict[str, bool]) -> None:
    """Process the documents.

    Args:
        args (dict[str, bool]): The processing steps based on CLI arguments.
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # Connect to the database.
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # Check the version of the database.
    check_db_up_to_date()

    # Load the data from the database table 'language'.
    dcr.db.cls_language.Language.load_data_from_dbt_language()

    # Export the line type rules.
    if args[dcr.db.cls_run.Run.ACTION_CODE_EXPORT_LT_RULES]:
        start_time_process = time.perf_counter_ns()
        process_export_lt_rules()
        dcr.utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Process the documents in the inbox file directory.
    if args[dcr.db.cls_run.Run.ACTION_CODE_INBOX]:
        start_time_process = time.perf_counter_ns()
        process_inbox_directory()
        dcr.utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Convert the scanned image pdf documents to image files.
    if args[dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE]:
        start_time_process = time.perf_counter_ns()
        process_convert_pdf_2_image()
        dcr.utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Convert the image files to pdf documents.
    if args[dcr.db.cls_run.Run.ACTION_CODE_TESSERACT]:
        start_time_process = time.perf_counter_ns()
        process_convert_image_2_pdf()
        dcr.utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Convert the non-pdf documents to pdf documents.
    if args[dcr.db.cls_run.Run.ACTION_CODE_PANDOC]:
        start_time_process = time.perf_counter_ns()
        process_convert_non_pdf_2_pdf()
        dcr.utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Extract text and metadata from pdf documents.
    if args[dcr.db.cls_run.Run.ACTION_CODE_PDFLIB]:
        start_time_process = time.perf_counter_ns()
        process_extract_text_from_pdf()
        dcr.utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Store the document structure from the parser result.
    if args[dcr.db.cls_run.Run.ACTION_CODE_PARSER]:
        start_time_process = time.perf_counter_ns()
        process_store_parse_result_in_json()
        dcr.utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Create document token.
    if args[dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE]:
        start_time_process = time.perf_counter_ns()
        process_tokenize()
        dcr.utils.progress_msg(f"Time : {round((time.perf_counter_ns() - start_time_process) / 1000000000, 2) :10.2f} s")

    # Disconnect from the database.
    dcr.cfg.glob.db_core.disconnect_db()

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Export the line type rules.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_export_lt_rules() -> None:
    """Export the line type rules."""
    dcr.utils.progress_msg_empty_before("Start: Export the line type rules ...")

    dcr_core.cls_nlp_core.NLPCore.export_rule_file_heading(
        is_verbose=dcr_core.core_glob.setup.is_verbose,
        file_name=dcr_core.core_glob.setup.lt_export_rule_file_heading,
        file_encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT,
        json_indent=dcr_core.core_glob.setup.json_indent,
        is_json_sort_keys=dcr_core.core_glob.setup.is_json_sort_keys,
    )

    dcr_core.cls_nlp_core.NLPCore.export_rule_file_list_bullet(
        is_verbose=dcr_core.core_glob.setup.is_verbose,
        file_name=dcr_core.core_glob.setup.lt_export_rule_file_list_bullet,
        file_encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT,
        json_indent=dcr_core.core_glob.setup.json_indent,
        is_json_sort_keys=dcr_core.core_glob.setup.is_json_sort_keys,
        environment_variant=dcr_core.core_glob.setup.environment_variant,
    )

    dcr_core.cls_nlp_core.NLPCore.export_rule_file_list_number(
        is_verbose=dcr_core.core_glob.setup.is_verbose,
        file_name=dcr_core.core_glob.setup.lt_export_rule_file_list_number,
        file_encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT,
        json_indent=dcr_core.core_glob.setup.json_indent,
        is_json_sort_keys=dcr_core.core_glob.setup.is_json_sort_keys,
        environment_variant=dcr_core.core_glob.setup.environment_variant,
    )

    dcr.utils.progress_msg("End  : Export the line type rules ...")


# -----------------------------------------------------------------------------
# Extract text and metadata from pdf documents.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_extract_text_from_pdf() -> None:
    """Extract text and metadata from pdf documents."""
    dcr.utils.progress_msg_empty_before("Start: Extract text and metadata from pdf documents ... PDFlib TET")

    dcr.cfg.glob.run = dcr.db.cls_run.Run(action_code=dcr.db.cls_run.Run.ACTION_CODE_PDFLIB)

    dcr.nlp.pdflib.extract_text_from_pdf()

    dcr.cfg.glob.run.finalise()

    dcr.utils.progress_msg("End  : Extract text and metadata from pdf documents ...")


# -----------------------------------------------------------------------------
# Process the inbox directory.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_inbox_directory() -> None:
    """Process the inbox directory."""
    dcr.utils.progress_msg_empty_before("Start: Process the inbox directory ... PyMuPDF [fitz]")

    dcr.cfg.glob.run = dcr.db.cls_run.Run(action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX)

    dcr.pp.inbox.process_inbox()

    dcr.cfg.glob.run.finalise()

    dcr.utils.progress_msg("End  : Process the inbox directory ...")


# -----------------------------------------------------------------------------
# Store the document structure from the parser result.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_store_parse_result_in_json() -> None:
    """Store the document structure from the parser result."""
    dcr.utils.progress_msg_empty_before("Start: Store document structure ... defusedxml [xml.etree.ElementTree]")

    dcr.cfg.glob.run = dcr.db.cls_run.Run(action_code=dcr.db.cls_run.Run.ACTION_CODE_PARSER)

    dcr.nlp.parser.parse_tetml()

    dcr.cfg.glob.run.finalise()

    dcr.utils.progress_msg("End  : Store document structure ...")


# -----------------------------------------------------------------------------
# Create document tokens.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def process_tokenize() -> None:
    """Create document tokens."""
    dcr.utils.progress_msg_empty_before("Start: Create document tokens ... spaCy")

    dcr.cfg.glob.run = dcr.db.cls_run.Run(action_code=dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE)

    dcr.nlp.tokenizer.tokenize()

    dcr.cfg.glob.run.finalise()

    dcr.utils.progress_msg("End  : Create document tokens ...")


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # not testable
    main(sys.argv)
