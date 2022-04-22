# pylint: disable=unused-argument
"""Testing Module nlp.tokenize."""

import libs.cfg
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TOKENIZE - normal.
# -----------------------------------------------------------------------------
def test_run_action_tokenize_normal(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - normal."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_mini", "pdf"),
        ],
        libs.cfg.directory_inbox,
    )

    # -------------------------------------------------------------------------
    value_original_delete_auxiliary_files = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES, "true"
    )
    value_original_tesseract_timeout = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_TESSERACT_TIMEOUT, "30"
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_STORE_FROM_PARSER])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TOKENIZE])

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION,
        libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES,
        value_original_delete_auxiliary_files,
    )
    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION,
        libs.cfg.DCR_CFG_TESSERACT_TIMEOUT,
        value_original_tesseract_timeout,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_tokenize_normal <=========")

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_accepted,
        [],
        [
            "pdf_mini_1.pdf",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
