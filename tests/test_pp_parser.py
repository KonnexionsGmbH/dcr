# pylint: disable=unused-argument
"""Testing Module pp.parser."""
import typing

import jellyfish
import libs.cfg
import pytest
import roman

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Levenshtein - arabic.
# -----------------------------------------------------------------------------
def test_levenshtein_arabic():
    """Test Levenshtein - arabic."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    upper_limit: int = 1200

    for prev in range(upper_limit):
        text_curr = f"Page {prev+1} of {str(upper_limit)}"
        text_prev = f"Page {prev} of {str(upper_limit)}"

        distance: int = jellyfish.levenshtein_distance(
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
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Levenshtein - roman.
# -----------------------------------------------------------------------------
def test_levenshtein_roman():
    """Test Levenshtein - roman."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    upper_limit: int = 1200
    upper_limit_roman: str = roman.toRoman(upper_limit)

    for prev in range(upper_limit):
        text_curr = f"Page {roman.toRoman(prev + 1)} of {upper_limit_roman}"
        text_prev = f"Page {roman.toRoman(prev)} of {upper_limit_roman}"

        distance: int = jellyfish.levenshtein_distance(
            text_prev,
            text_curr,
        )

        match distance:
            case 1 | 2 | 3 | 4 | 5 | 6 | 7:
                assert True
            case _:
                assert False, "distance=" + str(distance) + " prev=" + text_prev + " - curr=" + text_curr

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_STORE_FROM_PARSER - coverage.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("verbose_parser", ["all", "none", "text"])
def test_run_action_store_from_parser_coverage(verbose_parser: str, fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_STORE_FROM_PARSER - coverage."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_mini", "pdf"),
        ],
        libs.cfg.config.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (libs.cfg.config._DCR_CFG_VERBOSE_PARSER, verbose_parser),
            (libs.cfg.config._DCR_CFG_TETML_LINE, "true"),
            (libs.cfg.config._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_STORE_FROM_PARSER])

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_store_from_parser_coverage <=========")

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox_accepted,
        [],
        [
            "pdf_mini_1.pdf",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_STORE_FROM_PARSER - normal.
# -----------------------------------------------------------------------------
def test_run_action_store_from_parser_normal(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_STORE_FROM_PARSER - normal."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_mini", "pdf"),
            ("pdf_scanned_ok", "pdf"),
            ("translating_sql_into_relational_algebra_p01_02", "pdf"),
        ],
        libs.cfg.config.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (libs.cfg.config._DCR_CFG_TESSERACT_TIMEOUT, "30"),
            (libs.cfg.config._DCR_CFG_TETML_LINE, "true"),
            (libs.cfg.config._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_IMAGE_2_PDF])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_NON_PDF_2_PDF])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_STORE_FROM_PARSER])

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_store_from_parser_normal <=========")

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox,
        [],
        [],
    )

    files_expected: typing.List = [
        "pdf_mini_1.pdf",
        "pdf_scanned_ok_3.pdf",
        "translating_sql_into_relational_algebra_p01_02_5.pdf",
    ]

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox_accepted,
        [],
        files_expected,
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_STORE_FROM_PARSER - normal - keep.
# -----------------------------------------------------------------------------
def test_run_action_store_from_parser_normal_keep(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_STORE_FROM_PARSER - normal - keep."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_mini", "pdf"),
            ("pdf_scanned_ok", "pdf"),
            ("translating_sql_into_relational_algebra_p01_02", "pdf"),
        ],
        libs.cfg.config.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (libs.cfg.config._DCR_CFG_TESSERACT_TIMEOUT, "30"),
            (libs.cfg.config._DCR_CFG_TETML_LINE, "true"),
            (libs.cfg.config._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_IMAGE_2_PDF])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_NON_PDF_2_PDF])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_STORE_FROM_PARSER])

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_store_from_parser_normal_keep <=========")

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox,
        [],
        [],
    )

    files_expected: typing.List = [
        "pdf_mini_1.pdf",
        "pdf_mini_1.line.xml",
        "pdf_mini_1.word.xml",
        "pdf_scanned_ok_3.pdf",
        "pdf_scanned_ok_3_1.jpeg",
        "pdf_scanned_ok_3_1.pdf",
        "pdf_scanned_ok_3_1.line.xml",
        "pdf_scanned_ok_3_1.word.xml",
        "translating_sql_into_relational_algebra_p01_02_5.pdf",
        "translating_sql_into_relational_algebra_p01_02_5_0.pdf",
        "translating_sql_into_relational_algebra_p01_02_5_0.line.xml",
        "translating_sql_into_relational_algebra_p01_02_5_0.word.xml",
        "translating_sql_into_relational_algebra_p01_02_5_1.jpeg",
        "translating_sql_into_relational_algebra_p01_02_5_1.pdf",
        "translating_sql_into_relational_algebra_p01_02_5_2.jpeg",
        "translating_sql_into_relational_algebra_p01_02_5_2.pdf",
    ]

    # TBD
    # if platform.system() != "Windows":
    #     files_expected.append(
    #         "pdf_scanned_03_ok_11.pdf",
    #     )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox_accepted,
        [],
        files_expected,
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
