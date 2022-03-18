# pylint: disable=unused-argument
"""Testing Module libs.pdflibdcr."""
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
    pytest.helpers.copy_files_from_pytest_2_dir(
        [
            ("pdf_text_ok_protected", "pdf"),
        ],
        libs.cfg.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    # -------------------------------------------------------------------------
    no_files_expected = (0, 2, 0)

    files_to_be_checked = [
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_text_ok_protected", "1"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_text_ok_protected", "1"],
            "xml",
        ),
    ]

    pytest.helpers.verify_content_inboxes(
        files_to_be_checked,
        no_files_expected,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# # -----------------------------------------------------------------------------
# # Test RUN_ACTION_TEXT_FROM_PDF - normal - timeout.
# # -----------------------------------------------------------------------------
# def test_run_action_extract_text_from_pdf_normal_timeout(fxtr_rmdir_opt,
# fxtr_setup_empty_db_and_inbox):
#     """Test RUN_ACTION_TEXT_FROM_PDF - normal - timeout."""
#     libs.cfg.logger.debug(libs.cfg.LOGGER_START)
#
#     # -------------------------------------------------------------------------
#     stem_name: str = "pdf_scanned_ok"
#     file_ext: str = "pdf"
#
#     document_id, file_tesseract_1 = pytest.helpers.help_run_action_process_inbox_normal(
#         file_ext, stem_name
#     )
#
#     # -------------------------------------------------------------------------
#     value_original = pytest.helpers.store_config_param(
#         libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_TESSERACT_TIMEOUT, "1"
#     )
#
#     dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])
#
#     dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])
#
#     dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])
#
#     pytest.helpers.restore_config_param(
#         libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_TESSERACT_TIMEOUT, value_original
#     )
#
#     # -------------------------------------------------------------------------
#     no_files_expected = (0, 2, 0)
#
#     file_tesseract_2 = (
#         libs.cfg.directory_inbox_accepted,
#         [stem_name, str(document_id), "1"],
#         libs.cfg.pdf2image_type,
#     )
#
#     files_to_be_checked = [
#         file_tesseract_1,
#         file_tesseract_2,
#     ]
#
#     pytest.helpers.verify_content_inboxes(
#         files_to_be_checked,
#         no_files_expected,
#     )
#
#     # -------------------------------------------------------------------------
#     libs.cfg.logger.debug(libs.cfg.LOGGER_END)
