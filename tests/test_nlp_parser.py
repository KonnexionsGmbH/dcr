# pylint: disable=unused-argument
"""Testing Module nlp.parser."""
import os

import cfg.cls_setup
import cfg.glob
import db.cls_run
import jellyfish
import pytest
import roman

import dcr
import dcr_core.utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Levenshtein - arabic.
# -----------------------------------------------------------------------------
def test_levenshtein_arabic():
    """Test Levenshtein - arabic."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    upper_limit = 1200

    for prev in range(upper_limit):
        text_curr = f"Page {prev+1} of {str(upper_limit)}"
        text_prev = f"Page {prev} of {str(upper_limit)}"

        distance = jellyfish.levenshtein_distance(
            text_prev,
            text_curr,
        )

        match distance:
            case 1:
                assert True
            case 2:
                assert (prev + 1) % 10 == 0, "prev=" + text_prev + " - curr=" + text_curr
            case 3:
                assert (prev + 1) % 100 == 0, "prev=" + text_prev + " - curr=" + text_curr
            case 4:
                assert (prev + 1) % 1000 == 0, "prev=" + text_prev + " - curr=" + text_curr
            case _:
                assert False, "distance=" + str(distance) + " prev=" + text_prev + " - curr=" + text_curr

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Levenshtein - roman.
# -----------------------------------------------------------------------------
def test_levenshtein_roman():
    """Test Levenshtein - roman."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    upper_limit = 1200
    upper_limit_roman = roman.toRoman(upper_limit)

    for prev in range(upper_limit):
        text_curr = f"Page {roman.toRoman(prev + 1)} of {upper_limit_roman}"
        text_prev = f"Page {roman.toRoman(prev)} of {upper_limit_roman}"

        distance = jellyfish.levenshtein_distance(
            text_prev,
            text_curr,
        )

        match distance:
            case 1 | 2 | 3 | 4 | 5 | 6 | 7:
                assert True
            case _:
                assert False, "distance=" + str(distance) + " prev=" + text_prev + " - curr=" + text_curr

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_STORE_FROM_PARSER - coverage.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("verbose_parser", ["all", "none", "text"])
def test_run_action_store_parse_result_in_json_coverage(verbose_parser: str, fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_STORE_FROM_PARSER - coverage."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_mini", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "0"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "0"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TOC, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, verbose_parser),
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
    cfg.glob.logger.info("=========> test_run_action_store_parse_result_in_json_coverage <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "pdf_mini_1.line.json",
                "pdf_mini_1.word.json",
                "pdf_mini_1.pdf",
            ],
        ),
    )
    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_STORE_FROM_PARSER - coverage - page.
# -----------------------------------------------------------------------------
def test_run_action_store_parse_result_in_json_coverage_page(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_STORE_FROM_PARSER - coverage."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_mini", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "0"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "0"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TOC, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, "text"),
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
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_STORE_FROM_PARSER - coverage - LineType.
# -----------------------------------------------------------------------------
def test_run_action_store_parse_result_in_json_coverage_line_type(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_STORE_FROM_PARSER - coverage - LineType."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("p_2_h_0_f_2", "pdf"),
            ("p_2_h_2_f_0", "pdf"),
            ("p_2_h_2_f_2", "pdf"),
            ("p_3_h_0_f_4", "pdf"),
            ("p_3_h_4_f_4", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TOC, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
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
    cfg.glob.logger.info("=========> test_run_action_store_parse_result_in_json_coverage <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "p_2_h_0_f_2_1.line.json",
                "p_2_h_0_f_2_1.line.xml",
                "p_2_h_0_f_2_1.pdf",
                "p_2_h_2_f_0_2.line.json",
                "p_2_h_2_f_0_2.line.xml",
                "p_2_h_2_f_0_2.pdf",
                "p_2_h_2_f_2_3.line.json",
                "p_2_h_2_f_2_3.line.xml",
                "p_2_h_2_f_2_3.pdf",
                "p_3_h_0_f_4_4.line.json",
                "p_3_h_0_f_4_4.line.xml",
                "p_3_h_0_f_4_4.pdf",
                "p_3_h_4_f_4_5.line.json",
                "p_3_h_4_f_4_5.line.xml",
                "p_3_h_4_f_4_5.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_STORE_FROM_PARSER - missing input file.
# -----------------------------------------------------------------------------
def test_run_action_store_parse_result_in_json_missing_input_file(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_STORE_FROM_PARSER - missing input file."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_store_parse_result_in_json_missing_input_file <=========")

    stem_name_1 = "case_3_pdf_text_route_inbox_pdflib"
    file_ext_1 = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name_1, file_ext_1),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    os.remove(dcr_core.utils.get_full_name(cfg.glob.setup.directory_inbox_accepted, stem_name_1 + "_1.line.xml"))

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_STORE_FROM_PARSER - normal.
# -----------------------------------------------------------------------------
def test_run_action_store_parse_result_in_json_normal(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_STORE_FROM_PARSER - normal."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_mini", "pdf"),
            ("pdf_scanned_ok", "pdf"),
            ("translating_sql_into_relational_algebra_p01_02", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TOC, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TESSERACT_TIMEOUT, "30"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PANDOC])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_store_parse_result_in_json_normal <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "pdf_mini_1.line.json",
                "pdf_mini_1.pdf",
                "pdf_mini_1.word.json",
                "pdf_scanned_ok_2_1.line.json",
                "pdf_scanned_ok_2.pdf",
                "pdf_scanned_ok_2_1.word.json",
                "translating_sql_into_relational_algebra_p01_02_3_0.line.json",
                "translating_sql_into_relational_algebra_p01_02_3.pdf",
                "translating_sql_into_relational_algebra_p01_02_3_0.word.json",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_STORE_FROM_PARSER - normal - keep.
# -----------------------------------------------------------------------------
def test_run_action_store_parse_result_in_json_normal_keep(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_STORE_FROM_PARSER - normal - keep."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_mini", "pdf"),
            ("pdf_scanned_ok", "pdf"),
            ("translating_sql_into_relational_algebra_p01_02", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TOC, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TESSERACT_TIMEOUT, "30"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PANDOC])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_store_parse_result_in_json_normal_keep <=========")

    # TBD
    # if platform.system() != "Windows":
    #     files_expected.append(
    #         "pdf_scanned_03_ok_11.pdf",
    #     )
    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "pdf_mini_1.line.json",
                "pdf_mini_1.line.xml",
                "pdf_mini_1.pdf",
                "pdf_mini_1.word.json",
                "pdf_mini_1.word.xml",
                "pdf_scanned_ok_2.pdf",
                "pdf_scanned_ok_2_1.jpeg",
                "pdf_scanned_ok_2_1.line.json",
                "pdf_scanned_ok_2_1.line.xml",
                "pdf_scanned_ok_2_1.pdf",
                "pdf_scanned_ok_2_1.word.json",
                "pdf_scanned_ok_2_1.word.xml",
                "translating_sql_into_relational_algebra_p01_02_3.pdf",
                "translating_sql_into_relational_algebra_p01_02_3_0.line.json",
                "translating_sql_into_relational_algebra_p01_02_3_0.line.xml",
                "translating_sql_into_relational_algebra_p01_02_3_0.pdf",
                "translating_sql_into_relational_algebra_p01_02_3_0.word.json",
                "translating_sql_into_relational_algebra_p01_02_3_0.word.xml",
                "translating_sql_into_relational_algebra_p01_02_3_1.jpeg",
                "translating_sql_into_relational_algebra_p01_02_3_1.pdf",
                "translating_sql_into_relational_algebra_p01_02_3_2.jpeg",
                "translating_sql_into_relational_algebra_p01_02_3_2.pdf",
            ],
        ),
    )
    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
