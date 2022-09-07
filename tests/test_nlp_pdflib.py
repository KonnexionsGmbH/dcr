# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

# pylint: disable=unused-argument
"""Testing Module nlp.pdflib."""
import os

import dcr_core.cls_setup
import dcr_core.core_glob
import dcr_core.core_utils
import pytest

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_run
import dcr.launcher

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - normal - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_normal_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - normal - duplicate."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.info("=========> test_run_action_extract_text_from_pdf_normal_duplicate <=========")

    stem_name_1 = "pdf_text_ok_protected"
    file_ext_1 = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name_1, file_ext_1),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    stem_name_2 = "pdf_text_ok_protected_1.line"
    file_ext_2 = "xml"

    pytest.helpers.help_run_action_all_complete_duplicate_file(file_ext_1, file_ext_2, stem_name_1, stem_name_2)

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - normal - keep.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_normal_keep(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - normal - keep."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok_protected", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
        ],
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.info("=========> test_run_action_extract_text_from_pdf_normal_keep <=========")

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
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - normal - keep - only page.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_normal_keep_only_page(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - normal - keep - only page."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok_protected", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
        ],
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.info("=========> test_run_action_extract_text_from_pdf_normal_keep_only_page <=========")

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
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - line.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_rej_file_open_line(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - line."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
        ],
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TESSERACT])

    os.remove(
        dcr_core.core_utils.get_full_name_from_components(
            dcr_core.core_glob.setup.directory_inbox_accepted,
            "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_0.pdf",
        )
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.info("=========> test_run_action_extract_text_from_pdf_rej_file_open_line <=========")

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
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - page.
# -----------------------------------------------------------------------------
def test_run_action_extract_text_from_pdf_rej_file_open_page(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TEXT_FROM_PDF - rej_file_open - page."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TESSERACT])

    os.remove(
        dcr_core.core_utils.get_full_name_from_components(
            dcr_core.core_glob.setup.directory_inbox_accepted,
            "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_1_0.pdf",
        )
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.info("=========> test_run_action_extract_text_from_pdf_rej_file_open_page <=========")

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
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
