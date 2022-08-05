# pylint: disable=unused-argument
"""Testing Module dcr_core.cls_line_type_list_number."""

import pytest

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_action
import dcr.db.cls_db_core
import dcr.db.cls_document
import dcr.db.cls_run
import dcr.launcher
import dcr_core.cls_line_type_list_number
import dcr_core.cls_text_parser
import dcr_core.core_glob
import dcr_core.core_utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test LineType Numbered List - maximum version.
# -----------------------------------------------------------------------------
def test_line_type_list_number_maximum(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Numbered List - maximum version."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_list_number", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_NUMBER, "true"),
        ],
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_list_number.line.json", no_lines_footer=1, no_lines_header=1, no_lists_number_in_document=11)

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.check_json_line("docx_list_number.line_token.json", no_lines_footer=1, no_lines_header=1, no_lists_number_in_document=11)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_maximum_version_2 <=========")

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
                "docx_list_number.pdf",
                1,
                4,
                1,
                1,
                0,
                0,
                11,
                0,
                5,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_maximum_version_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_list_number.line.json",
                "docx_list_number.line.xml",
                "docx_list_number.line_list_number.json",
                "docx_list_number.line_token.json",
                "docx_list_number.page.json",
                "docx_list_number.page.xml",
                "docx_list_number.pdf",
                "docx_list_number.word.json",
                "docx_list_number.word.xml",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Numbered List - minimum version - 1.
# -----------------------------------------------------------------------------
def test_line_type_list_number_minimum_1(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Numbered List - minimum version - 1."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_list_number", "pdf"),
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
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, "false"),
        ],
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_list_number.line.json", no_lines_footer=1, no_lines_header=1, no_lists_number_in_document=11)

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_1_2 <=========")

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
                "docx_list_number.pdf",
                1,
                4,
                1,
                1,
                0,
                0,
                11,
                0,
                5,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_1_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_list_number.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Numbered List - minimum version - 2.
# -----------------------------------------------------------------------------
def test_line_type_list_number_minimum_2(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Numbered List - minimum version - 2."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_list_number", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_LT_LIST_NUMBER_MIN_ENTRIES, "99"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
        ],
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("docx_list_number.line.json", no_lines_footer=1, no_lines_header=1)

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_1_2 <=========")

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
                "docx_list_number.pdf",
                1,
                4,
                1,
                1,
                0,
                0,
                0,
                0,
                5,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_1_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_list_number.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_list_number - coverage - exists.
# -----------------------------------------------------------------------------
def test_line_type_list_number_missing_dependencies_coverage_exists(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_list_number - coverage - exists."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.run = dcr.db.cls_run.Run(
        _row_id=1,
        action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action(
        _row_id=1,
        action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.document = dcr.db.cls_document.Document(
        action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    dcr_core.core_glob.text_parser = dcr_core.cls_text_parser.TextParser()

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_line_type_list_number.LineTypeListNumber(
        file_name_curr=dcr.cfg.glob.action_curr.action_file_name,
    )

    instance.exists()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_list_number - TextParser.
# -----------------------------------------------------------------------------
def test_line_type_list_number_missing_dependencies_text_parser(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_list_number - TextParser."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.run = dcr.db.cls_run.Run(
        _row_id=1,
        action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action(
        _row_id=1,
        action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.document = dcr.db.cls_document.Document(
        action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_text_parser=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr_core.cls_line_type_list_number.LineTypeListNumber(
            file_name_curr=dcr.cfg.glob.action_curr.action_file_name,
        )

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing"

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)
