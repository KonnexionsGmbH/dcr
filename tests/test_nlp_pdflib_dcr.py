# pylint: disable=unused-argument
"""Testing Module nlp.pdflib_dcr."""
import os

import cfg.glob
import db.cls_run
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - normal - keep.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_normal_keep(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - normal - keep."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_text_ok_protected", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_extract_text_from_pdf_normal_keep <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            "pdf_text_ok_protected_1.pdf",
            "pdf_text_ok_protected_1.line.xml",
            "pdf_text_ok_protected_1.word.xml",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - normal - keep - only page.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_normal_keep_only_page(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - normal - keep - only page."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_text_ok_protected", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_extract_text_from_pdf_normal_keep_only_page <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            "pdf_text_ok_protected_1.pdf",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - line.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_rej_file_open_line(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - line."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "false"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    os.remove(
        os.path.join(
            cfg.glob.setup.directory_inbox_accepted,
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.pdf",
        )
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_extract_text_from_pdf_rej_file_open_line <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1.pdf",
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.jpeg",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - page.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_rej_file_open_page(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - page."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    os.remove(
        os.path.join(
            cfg.glob.setup.directory_inbox_accepted,
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.pdf",
        )
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_extract_text_from_pdf_rej_file_open_page <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1.pdf",
            "case_03_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.jpeg",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
