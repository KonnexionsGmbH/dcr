# pylint: disable=unused-argument
"""Testing Module pp.pdf2image."""
import os

import cfg.cls_setup
import cfg.glob
import db.cls_run
import pytest

import dcr
import dcr_core.core_glob
import dcr_core.core_utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PDF_2_IMAGE - missing input file.
# -----------------------------------------------------------------------------
def test_run_action_pdf_2_image_missing_input_file(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PDF_2_IMAGE - missing input file."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_pdf_2_image_missing_input_file <=========")

    stem_name_1 = "case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib"
    file_ext_1 = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name_1, file_ext_1),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    os.remove(dcr_core.core_utils.get_full_name(dcr_core.core_glob.setup.directory_inbox_accepted, stem_name_1 + "_1." + file_ext_1))

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PDF_2_IMAGE - normal - png.
# -----------------------------------------------------------------------------
def test_run_action_pdf_2_image_normal_png(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PDF_2_IMAGE - normal - png - duplicate."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_pdf_2_image_normal_png 1/2 <=========")

    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_PDF2IMAGE_TYPE, dcr_core.cls_setup.Setup.PDF2IMAGE_TYPE_PNG),
        ],
    )

    # -------------------------------------------------------------------------
    stem_name = "pdf_scanned_ok"
    file_ext = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name, file_ext),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_pdf_2_image_normal_png 2/2 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                stem_name + "_1.pdf",
                stem_name + "_1_1." + dcr_core.core_glob.setup.PDF2IMAGE_TYPE_PNG,
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
