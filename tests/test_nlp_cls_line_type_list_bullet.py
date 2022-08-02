# pylint: disable=unused-argument
"""Testing Module dcr_core.cls_line_type_list_bullet."""

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_run
import launcher
import pytest

import dcr_core.cls_line_type_list_bullet
import dcr_core.cls_text_parser
import dcr_core.core_glob
import dcr_core.core_utils

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
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_BULLET, "true"),
        ],
    )

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line(
        "docx_list_bullet.line.json", no_lines_footer=1, no_lines_header=1, no_lists_bullet_in_document=8
    )

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.check_json_line(
        "docx_list_bullet.line_token.json", no_lines_footer=1, no_lines_header=1, no_lists_bullet_in_document=8
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_maximum_version_2 <=========")

    pytest.helpers.check_dbt_document(
        (
            1,
            (
                1,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
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
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "false"),
        ],
    )

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line(
        "docx_list_bullet.line.json", no_lines_footer=1, no_lines_header=1, no_lists_bullet_in_document=8
    )

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_1_2 <=========")

    pytest.helpers.check_dbt_document(
        (
            1,
            (
                1,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
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
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES, "99"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
        ],
    )

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_list_bullet.line.json", no_lines_footer=1, no_lines_header=1)

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_1_2 <=========")

    pytest.helpers.check_dbt_document(
        (
            1,
            (
                1,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
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
    cfg.glob.document = db.cls_document.Document(
        action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup = cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    dcr_core.core_glob.text_parser = dcr_core.cls_text_parser.TextParser()

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_line_type_list_bullet.LineTypeListBullet(
        file_name_curr=cfg.glob.action_curr.action_file_name,
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
    cfg.glob.document = db.cls_document.Document(
        action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup = cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_text_parser=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr_core.cls_line_type_list_bullet.LineTypeListBullet(
            file_name_curr=cfg.glob.action_curr.action_file_name,
        )

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
