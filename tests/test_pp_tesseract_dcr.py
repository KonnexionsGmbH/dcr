# pylint: disable=unused-argument
"""Testing Module pp.tesseract_dcr."""
import os

import cfg.cls_setup
import cfg.glob
import db.cls_run
import pytest

import dcr
import dcr_core.cfg.cls_setup

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_IMAGE_2_PDF - normal - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_image_2_pdf_normal_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_IMAGE_2_PDF - normal - duplicate."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_normal_duplicate <=========")

    stem_name_1 = "tiff_pdf_text_ok"
    file_ext_1 = "tiff"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name_1, file_ext_1),
        ],
        target_path=dcr_core.cfg.glob.setup.directory_inbox,
    )

    stem_name_2 = "tiff_pdf_text_ok_1"
    file_ext_2 = "pdf"

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

    stem_name = "pdf_scanned_ok"
    file_ext = "pdf"

    document_id, _ = pytest.helpers.help_run_action_process_inbox_normal(
        stem_name,
        file_ext,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )
    values_original_core = pytest.helpers.backup_config_params(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TESSERACT_TIMEOUT, "1"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    pytest.helpers.restore_config_params(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_core,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_normal_timeout 2/2 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                stem_name + "_" + str(document_id) + "." + file_ext,
                stem_name + "_" + str(document_id) + "_1." + dcr_core.cfg.glob.setup.pdf2image_type,
            ],
        ),
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

    stem_name_1 = "translating_sql_into_relational_algebra_p01_02"
    file_ext_1 = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name_1, file_ext_1),
        ],
        target_path=dcr_core.cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
        ],
    )
    values_original_core = pytest.helpers.backup_config_params(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TESSERACT_TIMEOUT, "30"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
        ],
    )

    # -------------------------------------------------------------------------
    stem_name_2 = "translating_sql_into_relational_algebra_p01_02_1_0"
    file_ext_2 = "pdf"

    pytest.helpers.help_run_action_all_complete_duplicate_file(file_ext_1, file_ext_2, stem_name_1, stem_name_2, is_ocr=True)

    # -------------------------------------------------------------------------
    os.remove(os.path.join(dcr_core.cfg.glob.setup.directory_inbox_accepted, "translating_sql_into_relational_algebra_p01_02_1_0.pdf"))

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    # -------------------------------------------------------------------------
    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    pytest.helpers.restore_config_params(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_core,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
