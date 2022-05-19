# pylint: disable=unused-argument
"""Testing Module pp.pdf2image_dcr."""
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
# Test RUN_ACTION_PDF_2_IMAGE - normal - jpeg - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_pdf_2_image_normal_jpeg_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PDF_2_IMAGE - normal - jpeg - duplicate."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_pdf_2_image_normal_jpeg_duplicate <=========")

    stem_name_1: str = "pdf_scanned_ok"
    file_ext_1: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name_1, file_ext_1),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    stem_name_2: str = "pdf_scanned_ok_1_1"
    file_ext_2: str = "jpeg"

    pytest.helpers.help_run_action_all_complete_duplicate_file(file_ext_1, file_ext_2, stem_name_1, stem_name_2)

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

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

    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.glob.setup._DCR_CFG_PDF2IMAGE_TYPE, cfg.glob.setup.PDF2IMAGE_TYPE_PNG),
        ],
    )

    # -------------------------------------------------------------------------
    stem_name: str = "pdf_scanned_ok"
    file_ext: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name, file_ext),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_pdf_2_image_normal_png 2/2 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
            stem_name + "_1.pdf",
            stem_name + "_1_1." + cfg.glob.setup.PDF2IMAGE_TYPE_PNG,
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
