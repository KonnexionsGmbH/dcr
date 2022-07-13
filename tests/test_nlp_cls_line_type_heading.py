# pylint: disable=unused-argument
"""Testing Module nlp.cls_line_type_heading."""

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_run
import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy
import pytest

import dcr
import dcr_core.cfg.glob
import dcr_core.nlp.cls_line_type_heading
import dcr_core.utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test LineType Heading - maximum version.
# -----------------------------------------------------------------------------
def test_cls_line_type_heading_maximum(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Heading - maximum version."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_heading", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_REGEXP, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_MAX_LEVEL, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_MIN_PAGES, "2"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_RULE_FILE, "data/lt_export_rule_heading_test.json"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_TOLERANCE_LLX, "5"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADING, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_heading.line.json", no_lines_footer=1, no_lists_number_in_document=7, no_tables_in_document=1)

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.check_json_line("docx_heading.line_token.json", no_lines_footer=1, no_lists_number_in_document=7, no_tables_in_document=1)

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_heading_maximum_2 <=========")

    pytest.helpers.check_dbt_document(
        (
            1,
            (
                1,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "docx_heading.pdf",
                1,
                4,
                1,
                0,
                0,
                0,
                7,
                1,
                5,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_heading_maximum_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_heading.line.json",
                "docx_heading.line.xml",
                "docx_heading.line_heading.json",
                "docx_heading.line_token.json",
                "docx_heading.page.json",
                "docx_heading.page.xml",
                "docx_heading.pdf",
                "docx_heading.word.json",
                "docx_heading.word.xml",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Heading - minimum version - 1.
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test_cls_line_type_heading_minimum_1(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Heading - minimum version_1."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_heading", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_REGEXP, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_MAX_LEVEL, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_MIN_PAGES, "2"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_RULE_FILE, "data/lt_export_rule_heading_test.json"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_TOLERANCE_LLX, "5"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADING, "false"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_heading.line.json", no_lines_footer=1, no_lists_number_in_document=7, no_tables_in_document=1)

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_heading_minimum_1_2 <=========")

    pytest.helpers.check_dbt_document(
        (
            1,
            (
                1,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "docx_heading.pdf",
                1,
                4,
                1,
                0,
                0,
                0,
                7,
                1,
                5,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_heading_minimum_1_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_heading.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_heading - coverage - exists.
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_heading_coverage_exists(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_heading - coverage - exists."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    cfg.glob.run = db.cls_run.Run(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    cfg.glob.action_curr = db.cls_action.Action(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    cfg.glob.document = db.cls_document.Document(action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711)

    # -------------------------------------------------------------------------
    cfg.glob.setup = cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    dcr_core.cfg.glob.text_parser = nlp.cls_text_parser.TextParser()

    # -------------------------------------------------------------------------
    instance = dcr_core.nlp.cls_line_type_heading.LineTypeHeading(
        action_file_name="",
        is_verbose_lt=cfg.glob.setup.is_verbose_lt_heading,
    )

    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_heading - TextParser.
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_heading_text_parser(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_heading - TextParser."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    cfg.glob.run = db.cls_run.Run(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    cfg.glob.action_curr = db.cls_action.Action(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    cfg.glob.document = db.cls_document.Document(action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711)

    # -------------------------------------------------------------------------
    cfg.glob.setup = cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_text_parser=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr_core.nlp.cls_line_type_heading.LineTypeHeading(
            action_file_name="",
            is_verbose_lt=cfg.glob.setup.is_verbose_lt_heading,
        )

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
