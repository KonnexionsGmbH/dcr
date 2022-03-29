# pylint: disable=unused-argument
"""Testing Module libs.preprocessor.pdflibdcr."""
import libs.cfg
import libs.db
import libs.db.cfg
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - normal.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_normal(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - normal."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_text_ok_protected", "pdf"),
        ],
        libs.cfg.directory_inbox,
    )

    # -------------------------------------------------------------------------
    value_original_delete_auxiliary_files = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES, "false"
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION,
        libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES,
        value_original_delete_auxiliary_files,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_extract_text_from_pdf_normal <=========")

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_accepted,
        [],
        [
            "pdf_text_ok_protected_1.pdf",
            "pdf_text_ok_protected_1.xml",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
