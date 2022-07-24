# pylint: disable=unused-argument
"""Testing Module pp.tesseract."""

import cfg.cls_setup
import cfg.glob
import db.cls_run
import launcher
import pytest

import dcr_core.cls_setup
import dcr_core.core_glob

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
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )

    # -------------------------------------------------------------------------
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
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_TESSERACT_TIMEOUT, "1"),
        ],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_normal_timeout 1/2 <=========")

    stem_name = "pdf_scanned_ok"
    file_ext = "pdf"

    document_id, _ = pytest.helpers.help_run_action_process_inbox_normal(
        stem_name,
        file_ext,
    )

    # -------------------------------------------------------------------------
    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_image_2_pdf_normal_timeout 2/2 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                stem_name + "_" + str(document_id) + "." + file_ext,
                stem_name + "_" + str(document_id) + "_1." + dcr_core.core_glob.setup.pdf2image_type,
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
