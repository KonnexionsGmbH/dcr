# pylint: disable=unused-argument
"""Testing Module nlp.tokenize."""

import libs.cfg
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TOKENIZE - normal.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "tetml_line, tetml_page", [("false", "true"), ("true", "false"), ("true", "true")]
)
def test_run_action_tokenize_normal(
    tetml_line: str, tetml_page: str, fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox
):
    """Test RUN_ACTION_TOKENIZE - normal."""
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
            (libs.cfg.config._DCR_CFG_TETML_LINE, tetml_line),
            (libs.cfg.config._DCR_CFG_TETML_PAGE, tetml_page),
        ],
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_STORE_FROM_PARSER])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TOKENIZE])

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_tokenize_normal <=========")

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
