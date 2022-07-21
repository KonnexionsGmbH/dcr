# pylint: disable=unused-argument
"""Testing Module nlp.cls_line_type_headers_footers."""
import os.path

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_run
import pytest

import dcr
import dcr_core.cfg.cls_setup
import dcr_core.cfg.glob
import dcr_core.nlp.cls_line_type_headers_footers
import dcr_core.nlp.cls_line_type_toc
import dcr_core.nlp.cls_nlp_core
import dcr_core.nlp.cls_text_parser
import dcr_core.nlp.cls_tokenizer_spacy
import dcr_core.utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=duplicate-code
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test LineType Header & Footers - basic test.
# -----------------------------------------------------------------------------
def test_cls_line_type_headers_footers_basic(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Header & Footers - basic test."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("p_1_h_0_f_0", "pdf"),
            ("p_2_h_0_f_0", "pdf"),
            ("p_2_h_0_f_2", "pdf"),
            ("p_2_h_1_f_0", "pdf"),
            ("p_2_h_1_f_1", "pdf"),
            ("p_2_h_2_f_0", "pdf"),
            ("p_2_h_2_f_2", "pdf"),
            ("p_3_h_0_f_4", "pdf"),
            ("p_3_h_2_f_2", "pdf"),
            ("p_3_h_3_f_3", "pdf"),
            ("p_3_h_4_f_0", "pdf"),
            ("p_3_h_4_f_4", "pdf"),
            ("p_4_h_4_f_4_different_first", "pdf"),
            ("p_4_h_4_f_4_different_last", "pdf"),
            ("p_4_h_4_f_4_empty_first", "pdf"),
            ("p_4_h_4_f_4_empty_last", "pdf"),
            ("p_5_h_0_f_0", "pdf"),
            ("p_5_h_0_f_2", "pdf"),
            ("p_5_h_2_f_0", "pdf"),
            ("p_5_h_2_f_2", "pdf"),
            ("p_5_h_4_f_4_different_both", "pdf"),
            ("p_5_h_4_f_4_empty_both", "pdf"),
            ("p_5_h_4_f_4_empty_center", "pdf"),
        ],
        target_path=dcr_core.cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    # -------------------------------------------------------------------------
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_1_h_0_f_0_1.line.json")),
        target_footer=[],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_2_h_0_f_0_2.line.json")),
        target_footer=[],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_2_h_0_f_2_3.line.json")),
        target_footer=[(1, [0, 1]), (2, [0, 1])],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_2_h_1_f_0_4.line.json")),
        target_footer=[],
        target_header=[(1, [0]), (2, [0])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_2_h_1_f_1_5.line.json")),
        target_footer=[(1, [4]), (2, [4])],
        target_header=[(1, [0]), (2, [0])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_2_h_2_f_0_6.line.json")),
        target_footer=[(1, [0, 1]), (2, [0, 1])],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_2_h_2_f_2_7.line.json")),
        target_footer=[(1, [1, 2, 3]), (2, [1, 2, 3])],
        target_header=[(1, [0]), (2, [0])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_3_h_0_f_4_8.line.json")),
        target_footer=[(1, [4, 5, 6]), (2, [4, 5, 6]), (3, [4, 5, 6])],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_3_h_2_f_2_9.line.json")),
        target_footer=[(1, [5, 6]), (2, [5, 6]), (3, [5, 6])],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_3_h_3_f_3_10.line.json")),
        target_footer=[(1, [6, 7, 8]), (2, [6, 7, 8]), (3, [6, 7, 8])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_3_h_4_f_0_11.line.json")),
        target_footer=[],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_3_h_4_f_4_12.line.json")),
        target_footer=[(1, [8, 9, 10]), (2, [8, 9, 10]), (3, [8, 9, 10])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_different_first_13.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_different_last_14.line.json")),
        target_footer=[(1, [8, 9, 10]), (2, [8, 9, 10]), (3, [8, 9, 10])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_empty_first_15.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_empty_last_16.line.json")),
        target_footer=[(1, [8, 9, 10]), (2, [8, 9, 10]), (3, [8, 9, 10])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_5_h_0_f_0_17.line.json")),
        target_footer=[],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_5_h_0_f_2_18.line.json")),
        target_footer=[(1, [5, 6]), (2, [5, 6]), (3, [5, 6]), (4, [3, 4]), (5, [5, 6])],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_5_h_2_f_0_19.line.json")),
        target_footer=[],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1]), (4, [0, 1]), (5, [0, 1])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_5_h_2_f_2_20.line.json")),
        target_footer=[(1, [5, 6]), (2, [5, 6]), (3, [5, 6]), (4, [5, 6]), (5, [5, 6])],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1]), (4, [0, 1]), (5, [0, 1])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_5_h_4_f_4_different_both_21.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_5_h_4_f_4_empty_both_22.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "p_5_h_4_f_4_empty_center_23.line.json")),
        target_footer=[],
        target_header=[],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Header & Footers - maximum version.
# -----------------------------------------------------------------------------
def test_cls_line_type_headers_footers_maximum_version(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Header & Footers - maximum version."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("p_5_h_0_f_0", "pdf"),
            ("p_5_h_0_f_2", "pdf"),
            ("p_5_h_2_f_0", "pdf"),
            ("p_5_h_2_f_2", "pdf"),
        ],
        target_path=dcr_core.cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("p_5_h_0_f_0.line.json", no_lines_footer=0, no_lines_header=0)
    pytest.helpers.check_json_line("p_5_h_0_f_2.line.json", no_lines_footer=2, no_lines_header=0)
    pytest.helpers.check_json_line("p_5_h_2_f_0.line.json", no_lines_footer=0, no_lines_header=2)
    pytest.helpers.check_json_line("p_5_h_2_f_2.line.json", no_lines_footer=2, no_lines_header=2)

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.check_json_line("p_5_h_0_f_0.line_token.json", no_lines_footer=0, no_lines_header=0)
    pytest.helpers.check_json_line("p_5_h_0_f_2.line_token.json", no_lines_footer=2, no_lines_header=0)
    pytest.helpers.check_json_line("p_5_h_2_f_0.line_token.json", no_lines_footer=0, no_lines_header=2)
    pytest.helpers.check_json_line("p_5_h_2_f_2.line_token.json", no_lines_footer=2, no_lines_header=2)

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
                "p_5_h_0_f_0.pdf",
                1,
                4,
                0,
                0,
                0,
                0,
                0,
                0,
                5,
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
                "p_5_h_0_f_2.pdf",
                1,
                4,
                2,
                0,
                0,
                0,
                0,
                0,
                5,
                "end",
            ),
        )
    )

    pytest.helpers.check_dbt_document(
        (
            3,
            (
                3,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "p_5_h_2_f_0.pdf",
                1,
                4,
                0,
                2,
                0,
                0,
                0,
                0,
                5,
                "end",
            ),
        )
    )

    pytest.helpers.check_dbt_document(
        (
            4,
            (
                4,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "p_5_h_2_f_2.pdf",
                1,
                4,
                2,
                2,
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
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_maximum_version_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "p_5_h_0_f_0.line.json",
                "p_5_h_0_f_0.line.xml",
                "p_5_h_0_f_0.line_token.json",
                "p_5_h_0_f_0.page.json",
                "p_5_h_0_f_0.page.xml",
                "p_5_h_0_f_0.pdf",
                "p_5_h_0_f_0.word.json",
                "p_5_h_0_f_0.word.xml",
                "p_5_h_0_f_2.line.json",
                "p_5_h_0_f_2.line.xml",
                "p_5_h_0_f_2.line_token.json",
                "p_5_h_0_f_2.page.json",
                "p_5_h_0_f_2.page.xml",
                "p_5_h_0_f_2.pdf",
                "p_5_h_0_f_2.word.json",
                "p_5_h_0_f_2.word.xml",
                "p_5_h_2_f_0.line.json",
                "p_5_h_2_f_0.line.xml",
                "p_5_h_2_f_0.line_token.json",
                "p_5_h_2_f_0.page.json",
                "p_5_h_2_f_0.page.xml",
                "p_5_h_2_f_0.pdf",
                "p_5_h_2_f_0.word.json",
                "p_5_h_2_f_0.word.xml",
                "p_5_h_2_f_2.line.json",
                "p_5_h_2_f_2.line.xml",
                "p_5_h_2_f_2.line_token.json",
                "p_5_h_2_f_2.page.json",
                "p_5_h_2_f_2.page.xml",
                "p_5_h_2_f_2.pdf",
                "p_5_h_2_f_2.word.json",
                "p_5_h_2_f_2.word.xml",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Header & Footers - maximum version - by hand.
# -----------------------------------------------------------------------------
def test_cls_line_type_headers_footers_maximum_version_by_hand(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Header & Footers - maximum version - by hand."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("p_5_h_X_f_X", "pdf"),
        ],
        target_path=dcr_core.cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("p_5_h_X_f_X.line.json", no_lines_footer=1, no_lines_header=0)

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.check_json_line("p_5_h_X_f_X.line_token.json", no_lines_footer=1, no_lines_header=0)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_maximum_version_by_hand_2 <=========")

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
                "p_5_h_X_f_X.pdf",
                1,
                4,
                1,
                0,
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
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_maximum_version_by_hand_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "p_5_h_X_f_X.line.json",
                "p_5_h_X_f_X.line.xml",
                "p_5_h_X_f_X.line_token.json",
                "p_5_h_X_f_X.page.json",
                "p_5_h_X_f_X.page.xml",
                "p_5_h_X_f_X.pdf",
                "p_5_h_X_f_X.word.json",
                "p_5_h_X_f_X.word.xml",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Header & Footers - minimum version - distance.
# -----------------------------------------------------------------------------
def test_cls_line_type_headers_footers_minimum_version_distance(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Header & Footers - minimum version - distance."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("p_5_h_0_f_0", "pdf"),
            ("p_5_h_0_f_2", "pdf"),
            ("p_5_h_2_f_0", "pdf"),
            ("p_5_h_2_f_2", "pdf"),
        ],
        target_path=dcr_core.cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, "0"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "0"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("p_5_h_0_f_0.line.json", no_lines_footer=0, no_lines_header=0)
    pytest.helpers.check_json_line("p_5_h_0_f_2.line.json", no_lines_footer=2, no_lines_header=0)
    pytest.helpers.check_json_line("p_5_h_2_f_0.line.json", no_lines_footer=0, no_lines_header=2)
    pytest.helpers.check_json_line("p_5_h_2_f_2.line.json", no_lines_footer=1, no_lines_header=2)

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_distance_2 <=========")

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
                "p_5_h_0_f_0.pdf",
                1,
                4,
                0,
                0,
                0,
                0,
                0,
                0,
                5,
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
                "p_5_h_0_f_2.pdf",
                1,
                4,
                2,
                0,
                0,
                0,
                0,
                0,
                5,
                "end",
            ),
        )
    )

    pytest.helpers.check_dbt_document(
        (
            3,
            (
                3,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "p_5_h_2_f_0.pdf",
                1,
                4,
                0,
                2,
                0,
                0,
                0,
                0,
                5,
                "end",
            ),
        )
    )

    pytest.helpers.check_dbt_document(
        (
            4,
            (
                4,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "p_5_h_2_f_2.pdf",
                1,
                4,
                1,
                2,
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
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_maximum_version_distance_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "p_5_h_0_f_0.pdf",
                "p_5_h_0_f_2.pdf",
                "p_5_h_2_f_0.pdf",
                "p_5_h_2_f_2.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Header & Footers - minimum version - lines.
# -----------------------------------------------------------------------------
def test_cls_line_type_headers_footers_minimum_version_lines(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Header & Footers - minimum version - lines."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("p_5_h_0_f_0", "pdf"),
            ("p_5_h_0_f_2", "pdf"),
            ("p_5_h_2_f_0", "pdf"),
            ("p_5_h_2_f_2", "pdf"),
        ],
        target_path=dcr_core.cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "0"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "0"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.check_json_line("p_5_h_0_f_0.line.json", no_lines_footer=0, no_lines_header=0)
    pytest.helpers.check_json_line("p_5_h_0_f_2.line.json", no_lines_footer=0, no_lines_header=0)
    pytest.helpers.check_json_line("p_5_h_2_f_0.line.json", no_lines_footer=0, no_lines_header=0)
    pytest.helpers.check_json_line("p_5_h_2_f_2.line.json", no_lines_footer=0, no_lines_header=0)

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_minimum_version_distance_2 <=========")

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
                "p_5_h_0_f_0.pdf",
                1,
                4,
                0,
                0,
                0,
                0,
                0,
                0,
                5,
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
                "p_5_h_0_f_2.pdf",
                1,
                4,
                0,
                0,
                0,
                0,
                0,
                0,
                5,
                "end",
            ),
        )
    )

    pytest.helpers.check_dbt_document(
        (
            3,
            (
                3,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "p_5_h_2_f_0.pdf",
                1,
                4,
                0,
                0,
                0,
                0,
                0,
                0,
                5,
                "end",
            ),
        )
    )

    pytest.helpers.check_dbt_document(
        (
            4,
            (
                4,
                "tkn",
                "tokenize      (nlp)",
                dcr_core.utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "p_5_h_2_f_2.pdf",
                1,
                4,
                0,
                0,
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
    cfg.glob.logger.info("=========> test_cls_line_type_headers_footers_maximum_version_distance_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "p_5_h_0_f_0.pdf",
                "p_5_h_0_f_2.pdf",
                "p_5_h_2_f_0.pdf",
                "p_5_h_2_f_2.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_headers_footers - coverage - exists.
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_headers_footers_coverage_exists(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_headers_footers - coverage - exists."""
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
    dcr_core.cfg.glob.text_parser = dcr_core.nlp.cls_text_parser.TextParser()

    dcr_core.cfg.glob.text_parser.exists()

    # -------------------------------------------------------------------------
    instance = dcr_core.nlp.cls_line_type_headers_footers.LineTypeHeaderFooters(
        file_name_curr=cfg.glob.action_curr.action_file_name,
    )

    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
