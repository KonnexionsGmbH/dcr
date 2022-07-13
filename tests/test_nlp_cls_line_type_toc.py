# pylint: disable=unused-argument
"""Testing Module nlp.cls_line_type_toc."""
import os.path

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
import dcr_core.nlp.cls_line_type_toc
import dcr_core.utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=duplicate-code
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test LineType TOC - base version.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("lt_toc_last_page", ["0", "5"])
def test_line_type_toc_base(lt_toc_last_page: str, fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType TOC - base version."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_toc_line_bullet_list", "pdf"),
            ("pdf_toc_table_bullet_list", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_TOC_LAST_PAGE, lt_toc_last_page),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TOC, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, "false"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    if lt_toc_last_page == "0":
        target_toc_exp_line = 0
        target_toc_exp_table = 0
    else:
        target_toc_exp_line = 7
        target_toc_exp_table = 15

    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "pdf_toc_line_bullet_list_1.line.json")),
        target_footer=[(1, [2, 3]), (2, [8, 9]), (3, [12, 13]), (4, [10, 11]), (5, [6, 7]), (6, [6, 7]), (7, [6, 7])],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1]), (4, [0, 1]), (5, [0, 1]), (6, [0, 1]), (7, [0, 1])],
        target_toc=target_toc_exp_line,
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "pdf_toc_table_bullet_list_2.line.json")),
        target_footer=[(1, [11, 12]), (2, [8, 9]), (3, [10, 11]), (4, [10, 11]), (5, [6, 7]), (6, [6, 7]), (7, [6, 7])],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1]), (4, [0, 1]), (5, [0, 1]), (6, [0, 1]), (7, [0, 1])],
        target_toc=target_toc_exp_table,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType TOC - maximum version.
# -----------------------------------------------------------------------------
def test_line_type_toc_maximum(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType TOC - maximum version."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_toc_line_bullet_list", "pdf"),
            ("pdf_toc_table_bullet_list", "pdf"),
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
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_TOC_LAST_PAGE, "5"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_TOC_MIN_ENTRIES, "5"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TOC, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line(
        "pdf_toc_line_bullet_list.line.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=7,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
    )
    pytest.helpers.check_json_line(
        "pdf_toc_table_bullet_list.line.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=8,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.check_json_line(
        "pdf_toc_line_bullet_list.line_token.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=7,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
    )
    pytest.helpers.check_json_line(
        "pdf_toc_table_bullet_list.line_token.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=8,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
    )

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_line_type_toc_maximum_2 <=========")

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
                "pdf_toc_line_bullet_list.pdf",
                1,
                4,
                2,
                2,
                7,
                1,
                1,
                0,
                7,
                "end",
            ),
        )
    )

    pytest.helpers.check_dbt_document(
        (
            2,
            (
                2,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "pdf_toc_table_bullet_list.pdf",
                1,
                4,
                2,
                2,
                8,
                1,
                1,
                0,
                7,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_line_type_toc_maximum_3 <=========")

    expected_files = [
        "pdf_toc_line_bullet_list.line.json",
        "pdf_toc_line_bullet_list.line.xml",
        "pdf_toc_line_bullet_list.line_token.json",
        "pdf_toc_line_bullet_list.page.json",
        "pdf_toc_line_bullet_list.page.xml",
        "pdf_toc_line_bullet_list.pdf",
        "pdf_toc_line_bullet_list.word.json",
        "pdf_toc_line_bullet_list.word.xml",
        "pdf_toc_table_bullet_list.line.json",
        "pdf_toc_table_bullet_list.line.xml",
        "pdf_toc_table_bullet_list.line_token.json",
        "pdf_toc_table_bullet_list.page.json",
        "pdf_toc_table_bullet_list.page.xml",
        "pdf_toc_table_bullet_list.pdf",
        "pdf_toc_table_bullet_list.word.json",
        "pdf_toc_table_bullet_list.word.xml",
    ]

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            expected_files,
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType TOC - minimum version - 1.
# -----------------------------------------------------------------------------
def test_line_type_toc_minimum_1(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType TOC - minimum version - 1."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_toc_line_bullet_list", "pdf"),
            ("pdf_toc_table_bullet_list", "pdf"),
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
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_TOC_LAST_PAGE, "0"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_TOC_MIN_ENTRIES, "5"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TOC, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line(
        "pdf_toc_line_bullet_list.line.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=0,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
    )
    pytest.helpers.check_json_line(
        "pdf_toc_table_bullet_list.line.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=0,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
        no_tables_in_document=2,
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.check_json_line(
        "pdf_toc_line_bullet_list.line_token.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=0,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
    )
    pytest.helpers.check_json_line(
        "pdf_toc_table_bullet_list.line_token.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=0,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
        no_tables_in_document=2,
    )

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_line_type_toc_maximum_2 <=========")

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
                "pdf_toc_line_bullet_list.pdf",
                1,
                4,
                2,
                2,
                0,
                1,
                1,
                0,
                7,
                "end",
            ),
        )
    )

    pytest.helpers.check_dbt_document(
        (
            2,
            (
                2,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "pdf_toc_table_bullet_list.pdf",
                1,
                4,
                2,
                2,
                0,
                1,
                1,
                2,
                7,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_line_type_toc_maximum_3 <=========")

    expected_files = [
        "pdf_toc_line_bullet_list.line_token.json",
        "pdf_toc_line_bullet_list.page.json",
        "pdf_toc_line_bullet_list.pdf",
        "pdf_toc_line_bullet_list.word.json",
        "pdf_toc_table_bullet_list.line_token.json",
        "pdf_toc_table_bullet_list.pdf",
        "pdf_toc_table_bullet_list.page.json",
        "pdf_toc_table_bullet_list.word.json",
    ]

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            expected_files,
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType TOC - minimum version - 2.
# -----------------------------------------------------------------------------
def test_line_type_toc_minimum_2(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType TOC - minimum version - 2."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_toc_line_bullet_list", "pdf"),
            ("pdf_toc_table_bullet_list", "pdf"),
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
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_TOC_LAST_PAGE, "5"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_TOC_MIN_ENTRIES, "99"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TOC, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line(
        "pdf_toc_line_bullet_list.line.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=0,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
    )
    pytest.helpers.check_json_line(
        "pdf_toc_table_bullet_list.line.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=0,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
        no_tables_in_document=2,
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.check_json_line(
        "pdf_toc_line_bullet_list.line_token.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=0,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
    )
    pytest.helpers.check_json_line(
        "pdf_toc_table_bullet_list.line_token.json",
        no_lines_footer=2,
        no_lines_header=2,
        no_lines_toc=0,
        no_lists_bullet_in_document=1,
        no_lists_number_in_document=1,
        no_tables_in_document=2,
    )

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_line_type_toc_maximum_2 <=========")

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
                "pdf_toc_line_bullet_list.pdf",
                1,
                4,
                2,
                2,
                0,
                1,
                1,
                0,
                7,
                "end",
            ),
        )
    )

    pytest.helpers.check_dbt_document(
        (
            2,
            (
                2,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "pdf_toc_table_bullet_list.pdf",
                1,
                4,
                2,
                2,
                0,
                1,
                1,
                2,
                7,
                "end",
            ),
        )
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_line_type_toc_maximum_3 <=========")

    expected_files = [
        "pdf_toc_line_bullet_list.line_token.json",
        "pdf_toc_line_bullet_list.page.json",
        "pdf_toc_line_bullet_list.pdf",
        "pdf_toc_line_bullet_list.word.json",
        "pdf_toc_table_bullet_list.line_token.json",
        "pdf_toc_table_bullet_list.pdf",
        "pdf_toc_table_bullet_list.page.json",
        "pdf_toc_table_bullet_list.word.json",
    ]

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            expected_files,
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_toc - coverage - exists.
# -----------------------------------------------------------------------------
def test_line_type_toc_missing_dependencies_coverage_exists(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_toc - coverage - exists."""
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
    dcr_core.cfg.glob.text_parser = nlp.cls_text_parser.TextParser()

    dcr_core.cfg.glob.text_parser.exists()

    # -------------------------------------------------------------------------
    instance = dcr_core.nlp.cls_line_type_toc.LineTypeToc(
        action_file_name=cfg.glob.action_curr.action_file_name,
        is_verbose_lt=cfg.glob.setup.is_verbose_lt_table,
    )

    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
