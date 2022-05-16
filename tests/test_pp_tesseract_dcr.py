# pylint: disable=unused-argument
"""Testing Module pp.tesseract_dcr."""
import typing

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
# Test RUN_ACTION_IMAGE_2_PDF - normal.
# -----------------------------------------------------------------------------
def test_run_action_image_2_pdf_normal(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_IMAGE_2_PDF - normal."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_scanned_ok", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_normal <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    files_expected: typing.List = [
        "pdf_scanned_ok_1.pdf",
        "pdf_scanned_ok_1_1.pdf",
    ]

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        files_expected,
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_IMAGE_2_PDF - normal - keep.
# -----------------------------------------------------------------------------
def test_run_action_image_2_pdf_normal_keep(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_IMAGE_2_PDF - normal - keep."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_scanned_01_ok_16_c", "bmp"),
            ("pdf_scanned_01_ok_24", "bmp"),
            ("pdf_scanned_01_ok_256_c", "bmp"),
            ("pdf_scanned_01_ok_m", "bmp"),
            ("pdf_scanned_02_ok", "gif"),
            # TBD next Tesseract OCR version
            # ("pdf_scanned_03_ok", "jp2"),
            ("pdf_scanned_04_ok", "jpeg"),
            ("pdf_scanned_05_ok", "png"),
            ("pdf_scanned_06_ok", "pnm"),
            ("pdf_scanned_07_ok", "tiff"),
            ("pdf_scanned_08_ok", "webp"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.glob.setup._DCR_CFG_TESSERACT_TIMEOUT, "30"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_normal <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    files_expected: typing.List = [
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
        # TBD next Tesseract OCR version
        # "pdf_scanned_03_ok_11.jp2",
        # "pdf_scanned_03_ok_11.pdf",
        "pdf_scanned_04_ok_11.jpeg",
        "pdf_scanned_04_ok_11.pdf",
        "pdf_scanned_05_ok_13.png",
        "pdf_scanned_05_ok_13.pdf",
        "pdf_scanned_06_ok_15.pnm",
        "pdf_scanned_06_ok_15.pdf",
        "pdf_scanned_07_ok_17.tiff",
        "pdf_scanned_07_ok_17.pdf",
        "pdf_scanned_08_ok_19.webp",
        "pdf_scanned_08_ok_19.pdf",
    ]

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        files_expected,
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_IMAGE_2_PDF - normal - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_image_2_pdf_normal_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_IMAGE_2_PDF - normal - duplicate."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_normal_duplicate <=========")

    stem_name_1: str = "tiff_pdf_text_ok"
    file_ext_1: str = "tiff"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext_1)], cfg.glob.setup.directory_inbox)

    stem_name_2: str = "tiff_pdf_text_ok_1"
    file_ext_2: str = "pdf"

    pytest.helpers.help_run_action_all_complete_duplicate_file(file_ext_1, file_ext_2, stem_name_1, stem_name_2)

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_IMAGE_2_PDF - normal - timeout.
# -----------------------------------------------------------------------------
def test_run_action_image_2_pdf_normal_timeout(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_IMAGE_2_PDF - normal - timeout."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_normal_timeout 1/2 <=========")

    stem_name: str = "pdf_scanned_ok"
    file_ext: str = "pdf"

    document_id, _file_tesseract_1 = pytest.helpers.help_run_action_process_inbox_normal(
        stem_name,
        file_ext,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.glob.setup._DCR_CFG_TESSERACT_TIMEOUT, "1"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_normal_timeout 2/2 <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            stem_name + "_" + str(document_id) + "." + file_ext,
            stem_name + "_" + str(document_id) + "_1." + cfg.glob.setup.pdf2image_type,
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
# Test RUN_ACTION_IMAGE_2_PDF - reunite.
# -----------------------------------------------------------------------------
def test_run_action_image_2_pdf_reunite(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_IMAGE_2_PDF - reunite."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("translating_sql_into_relational_algebra_p01_02", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.glob.setup._DCR_CFG_TESSERACT_TIMEOUT, "30"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_reunite <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    files_expected: typing.List = [
        "translating_sql_into_relational_algebra_p01_02_1.pdf",
        "translating_sql_into_relational_algebra_p01_02_1_0.pdf",
    ]

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        files_expected,
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_IMAGE_2_PDF - reunite - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_image_2_pdf_reunite_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_IMAGE_2_PDF - reunite - duplicate."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_normal_duplicate <=========")

    stem_name_1: str = "translating_sql_into_relational_algebra_p01_02"
    file_ext_1: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext_1)], cfg.glob.setup.directory_inbox)

    stem_name_2: str = "translating_sql_into_relational_algebra_p01_02_1_0"
    file_ext_2: str = "pdf"

    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.glob.setup._DCR_CFG_TESSERACT_TIMEOUT, "30"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "false"),
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "false"),
        ],
    )

    pytest.helpers.help_run_action_all_complete_duplicate_file(file_ext_1, file_ext_2, stem_name_1, stem_name_2)

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
