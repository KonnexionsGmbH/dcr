# pylint: disable=unused-argument
"""Testing Module libs.tesseract."""
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
# Test RUN_ACTION_IMAGE_2_PDF - normal.
# -----------------------------------------------------------------------------
def test_run_action_image_2_pdf_normal(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_IMAGE_2_PDF - normal."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_from_pytest_2_dir(
        [
            ("pdf_scanned_01_ok", "bmp"),
            ("pdf_scanned_02_ok", "gif"),
            ("pdf_scanned_03_ok", "jp2"),
            ("pdf_scanned_04_ok", "jpeg"),
            ("pdf_scanned_05_ok", "png"),
            ("pdf_scanned_06_ok", "pnm"),
            ("pdf_scanned_07_ok", "tiff"),
            ("pdf_scanned_08_ok", "webp"),
        ],
        libs.cfg.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_IMAGE_2_PDF])

    # -------------------------------------------------------------------------
    # TBD
    # no_files_expected = (0, 16, 0)
    no_files_expected = (0, 14, 0)

    files_to_be_checked = [
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_01_ok", "1"],
            "bmp",
        ),
        # TBD
        # (
        #     libs.cfg.directory_inbox_accepted,
        #     ["pdf_scanned_01_ok", "1"],
        #     "pdf",
        # ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_02_ok", "3"],
            "gif",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_02_ok", "3"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_03_ok", "5"],
            "jp2",
        ),
        # TBD
        # (
        #     libs.cfg.directory_inbox_accepted,
        #     ["pdf_scanned_03_ok", "5"],
        #     "pdf",
        # ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_04_ok", "7"],
            "jpeg",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_04_ok", "7"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_05_ok", "9"],
            "png",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_05_ok", "9"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_06_ok", "11"],
            "pnm",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_06_ok", "11"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_07_ok", "13"],
            "tiff",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_07_ok", "13"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_08_ok", "15"],
            "webp",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["pdf_scanned_08_ok", "15"],
            "pdf",
        ),
    ]

    pytest.helpers.verify_content_inboxes(
        files_to_be_checked,
        no_files_expected,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_IMAGE_2_PDF - normal - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_image_2_pdf_normal_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_IMAGE_2_PDF - normal - duplicate."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name_1: str = "tiff_pdf_text_ok_1"
    file_ext_1: str = "tiff"

    pytest.helpers.copy_files_from_pytest_2_dir(
        [(stem_name_1, file_ext_1)], libs.cfg.directory_inbox
    )

    stem_name_2: str = "tiff_pdf_text_ok_1_1"
    file_ext_2: str = "pdf"

    pytest.helpers.help_run_action_all_complete_duplicate_file(
        file_ext_1, file_ext_2, stem_name_1, stem_name_2
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_IMAGE_2_PDF - normal - timeout.
# -----------------------------------------------------------------------------
def test_run_action_image_2_pdf_normal_timeout(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_IMAGE_2_PDF - normal - timeout."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name: str = "pdf_scanned_ok"
    file_ext: str = "pdf"

    document_id, file_tesseract_1 = pytest.helpers.help_run_action_process_inbox_normal(
        file_ext, stem_name
    )

    # -------------------------------------------------------------------------
    value_original = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_TESSERACT_TIMEOUT, "1"
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_IMAGE_2_PDF])

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_TESSERACT_TIMEOUT, value_original
    )

    # -------------------------------------------------------------------------
    no_files_expected = (0, 2, 0)

    file_tesseract_2 = (
        libs.cfg.directory_inbox_accepted,
        [stem_name, str(document_id), "1"],
        libs.cfg.pdf2image_type,
    )

    files_to_be_checked = [
        file_tesseract_1,
        file_tesseract_2,
    ]

    pytest.helpers.verify_content_inboxes(
        files_to_be_checked,
        no_files_expected,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
