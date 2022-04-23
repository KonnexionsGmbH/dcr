# pylint: disable=unused-argument
"""Testing Module pp.pdflib_dcr."""
import os

import libs.cfg
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - normal - keep.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_normal_keep(
    fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox
):
    """Test RUN_ACTION_TEXT_FROM_PDF - normal - keep."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_text_ok_protected", "pdf"),
        ],
        libs.cfg.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (libs.cfg.DCR_CFG_TETML_LINE, "true"),
            (libs.cfg.DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_extract_text_from_pdf_normal_keep <=========")

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
            "pdf_text_ok_protected_1.line.xml",
            "pdf_text_ok_protected_1.word.xml",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - normal - keep - only page.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_normal_keep_only_page(
    fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox
):
    """Test RUN_ACTION_TEXT_FROM_PDF - normal - keep - only page."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_text_ok_protected", "pdf"),
        ],
        libs.cfg.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info(
        "=========> test_run_action_extract_text_from_pdf_normal_keep_only_page <========="
    )

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
        ],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - line.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_rej_file_open_line(
    fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox
):
    """Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - line."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib", "pdf"),
        ],
        libs.cfg.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (libs.cfg.DCR_CFG_TETML_LINE, "true"),
            (libs.cfg.DCR_CFG_TETML_PAGE, "false"),
        ],
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_IMAGE_2_PDF])

    os.remove(
        os.path.join(
            libs.cfg.directory_inbox_accepted,
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.pdf",
        )
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_extract_text_from_pdf_rej_file_open_line <=========")

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_accepted,
        [],
        [
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1.pdf",
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.jpeg",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - page.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_rej_file_open_page(
    fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox
):
    """Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - page."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib", "pdf"),
        ],
        libs.cfg.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_IMAGE_2_PDF])

    os.remove(
        os.path.join(
            libs.cfg.directory_inbox_accepted,
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.pdf",
        )
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_TEXT_FROM_PDF])

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_extract_text_from_pdf_rej_file_open_page <=========")

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_accepted,
        [],
        [
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1.pdf",
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.jpeg",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
