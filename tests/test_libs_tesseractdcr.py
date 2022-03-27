# pylint: disable=unused-argument
"""Testing Module libs.tesseractdcr."""
import platform
from typing import List

import libs.cfg
import libs.db
import libs.db.cfg
import libs.parser
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
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_scanned_01_ok_16_c", "bmp"),
            ("pdf_scanned_01_ok_24", "bmp"),
            ("pdf_scanned_01_ok_256_c", "bmp"),
            ("pdf_scanned_01_ok_m", "bmp"),
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
    libs.cfg.logger.info("=========> test_run_action_image_2_pdf_normal <=========")

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox,
        [],
        [],
    )

    files_expected: List = [
        "pdf_scanned_01_ok_16_c_1.bmp",
        "pdf_scanned_01_ok_16_c_1.pdf",
        "pdf_scanned_01_ok_24_3.bmp",
        "pdf_scanned_01_ok_24_3.pdf",
        "pdf_scanned_01_ok_256_c_5.bmp",
        "pdf_scanned_01_ok_256_c_5.pdf",
        "pdf_scanned_01_ok_m_7.bmp",
        "pdf_scanned_01_ok_m_7.pdf",
        "pdf_scanned_02_ok_9.gif",
        "pdf_scanned_02_ok_9.pdf",
        "pdf_scanned_03_ok_11.jp2",
        # TBD
        # "pdf_scanned_03_ok_11.pdf",
        "pdf_scanned_04_ok_13.jpeg",
        "pdf_scanned_04_ok_13.pdf",
        "pdf_scanned_05_ok_15.png",
        "pdf_scanned_05_ok_15.pdf",
        "pdf_scanned_06_ok_17.pnm",
        "pdf_scanned_06_ok_17.pdf",
        "pdf_scanned_07_ok_19.tiff",
        "pdf_scanned_07_ok_19.pdf",
        "pdf_scanned_08_ok_21.webp",
        "pdf_scanned_08_ok_21.pdf",
    ]

    # TBD
    if platform.system() != "Windows":
        files_expected.append(
            "pdf_scanned_03_ok_11.pdf",
        )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_accepted,
        [],
        files_expected,
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_rejected,
        [],
        [],
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
    libs.cfg.logger.info("=========> test_run_action_image_2_pdf_normal_duplicate <=========")

    stem_name_1: str = "tiff_pdf_text_ok_1"
    file_ext_1: str = "tiff"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext_1)], libs.cfg.directory_inbox)

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
    libs.cfg.logger.info("=========> test_run_action_image_2_pdf_normal_timeout 1/2 <=========")

    stem_name: str = "pdf_scanned_ok"
    file_ext: str = "pdf"

    document_id, _file_tesseract_1 = pytest.helpers.help_run_action_process_inbox_normal(
        stem_name,
        file_ext,
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
    libs.cfg.logger.info("=========> test_run_action_image_2_pdf_normal_timeout 2/2 <=========")

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_accepted,
        [],
        [
            stem_name + "_" + str(document_id) + "." + file_ext,
            stem_name + "_" + str(document_id) + "_1." + libs.cfg.pdf2image_type,
        ],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
