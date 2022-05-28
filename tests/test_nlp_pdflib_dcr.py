# pylint: disable=unused-argument
"""Testing Module nlp.pdflib_dcr."""
import os

import cfg.glob
import db.cls_run
import pytest
import utils

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - normal - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_normal_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - normal - duplicate."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_extract_text_from_pdf_normal_duplicate <=========")

    stem_name_1: str = "pdf_text_ok_protected"
    file_ext_1: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name_1, file_ext_1),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    stem_name_2: str = "pdf_text_ok_protected_1.line"
    file_ext_2: str = "xml"

    pytest.helpers.help_run_action_all_complete_duplicate_file(file_ext_1, file_ext_2, stem_name_1, stem_name_2)

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - normal - keep.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_normal_keep(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - normal - keep."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok_protected", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_extract_text_from_pdf_normal_keep <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "pdf_text_ok_protected_1.pdf",
                "pdf_text_ok_protected_1.line.xml",
                "pdf_text_ok_protected_1.word.xml",
            ],
        ),
        inbox_rejected=(
            [],
            [],
        ),
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
        source_files=[
            ("pdf_text_ok_protected", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_extract_text_from_pdf_normal_keep_only_page <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "pdf_text_ok_protected_1.line.xml",
                "pdf_text_ok_protected_1.page.xml",
                "pdf_text_ok_protected_1.pdf",
            ],
        ),
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
        source_files=[
            ("case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "false"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    os.remove(
        utils.get_full_name(
            cfg.glob.setup.directory_inbox_accepted,
            "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.pdf",
        )
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_extract_text_from_pdf_rej_file_open_line <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1.pdf",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.jpeg",
            ],
        ),
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
        source_files=[
            ("case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    os.remove(
        utils.get_full_name(
            cfg.glob.setup.directory_inbox_accepted,
            "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.pdf",
        )
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_extract_text_from_pdf_rej_file_open_page <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1.pdf",
                "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_1.jpeg",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
