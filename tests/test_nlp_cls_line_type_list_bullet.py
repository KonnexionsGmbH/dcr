# pylint: disable=unused-argument
"""Testing Module dcr_core.nlp.cls_line_type_list_bullet."""

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_run
import nlp.cls_text_parser
import pytest

import dcr
import dcr_core.cfg.glob
import dcr_core.nlp.cls_line_type_list_bullet
import dcr_core.utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test LineType Bulleted List - maximum version.
# -----------------------------------------------------------------------------
def test_line_type_list_bullet_maximum(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Bulleted List - maximum version."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_list_bullet", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES, "2"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_RULE_FILE, "data/lt_export_rule_list_bullet_test.json"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX, "5"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_BULLET, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_list_bullet.line.json", no_lines_footer=1, no_lines_header=1, no_lists_bullet_in_document=8)

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.check_json_line("docx_list_bullet.line_token.json", no_lines_footer=1, no_lines_header=1, no_lists_bullet_in_document=8)

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_maximum_version_2 <=========")

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
                "docx_list_bullet.pdf",
                1,
                4,
                1,
                1,
                0,
                8,
                0,
                0,
                4,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_maximum_version_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_list_bullet.line.json",
                "docx_list_bullet.line.xml",
                "docx_list_bullet.line_list_bullet.json",
                "docx_list_bullet.line_token.json",
                "docx_list_bullet.page.json",
                "docx_list_bullet.page.xml",
                "docx_list_bullet.pdf",
                "docx_list_bullet.word.json",
                "docx_list_bullet.word.xml",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Bulleted List - minimum version - 1.
# -----------------------------------------------------------------------------
def test_line_type_list_bullet_minimum_1(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Bulleted List - minimum version - 1."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_list_bullet", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES, "2"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_RULE_FILE, "data/lt_export_rule_list_bullet_test.json"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX, "5"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_BULLET, "false"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_list_bullet.line.json", no_lines_footer=1, no_lines_header=1, no_lists_bullet_in_document=8)

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_1_2 <=========")

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
                "docx_list_bullet.pdf",
                1,
                4,
                1,
                1,
                0,
                8,
                0,
                0,
                4,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_1_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_list_bullet.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Bulleted List - minimum version - 2.
# -----------------------------------------------------------------------------
def test_line_type_list_bullet_minimum_2(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Bulleted List - minimum version - 2."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_list_bullet", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES, "99"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_RULE_FILE, "data/lt_export_rule_list_bullet_test.json"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX, "5"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_BULLET, "false"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_list_bullet.line.json", no_lines_footer=1, no_lines_header=1)

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_1_2 <=========")

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
                "docx_list_bullet.pdf",
                1,
                4,
                1,
                1,
                0,
                0,
                0,
                0,
                4,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_1_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_list_bullet.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_list_bullet - coverage - exists.
# -----------------------------------------------------------------------------
def test_line_type_list_bullet_missing_dependencies_coverage_exists(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_list_bullet - coverage - exists."""
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
    instance = dcr_core.nlp.cls_line_type_list_bullet.LineTypeListBullet(
        action_file_name=cfg.glob.action_curr.action_file_name,
        is_verbose_lt=cfg.glob.setup.is_verbose_lt_list_bullet,
    )

    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_list_bullet - TextParser.
# -----------------------------------------------------------------------------
def test_line_type_list_bullet_missing_dependencies_text_parser(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_list_bullet - TextParser."""
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
        dcr_core.nlp.cls_line_type_list_bullet.LineTypeListBullet(
            action_file_name=cfg.glob.action_curr.action_file_name,
            is_verbose_lt=cfg.glob.setup.is_verbose_lt_list_bullet,
        )

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
