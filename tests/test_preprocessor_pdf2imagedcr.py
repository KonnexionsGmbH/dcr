# pylint: disable=unused-argument
"""Testing Module preprocessor.pdf2imagedcr."""
import libs.cfg
import libs.db
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PDF_2_IMAGE - normal - jpeg - keep.
# -----------------------------------------------------------------------------
def test_run_action_pdf_2_image_normal_jpeg_keep(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PDF_2_IMAGE - normal - jpeg - keep."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_pdf_2_image_normal_jpeg 1/2 <=========")

    stem_name: str = "pdf_scanned_ok"
    file_ext: str = "pdf"

    document_id, _file_p_i = pytest.helpers.help_run_action_process_inbox_normal(
        stem_name,
        file_ext,
    )

    # -------------------------------------------------------------------------
    value_original_delete_auxiliary_files = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES, "false"
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION,
        libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES,
        value_original_delete_auxiliary_files,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_pdf_2_image_normal_jpeg 2/2 <=========")

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
    fxtr_rmdir_opt(libs.cfg.directory_inbox_accepted)

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    assert expt.type == SystemExit, "inbox_accepted directory missing"
    assert expt.value.code == 1, "inbox_accepted, directory missing"

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PDF_2_IMAGE - normal - jpeg - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_pdf_2_image_normal_jpeg_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PDF_2_IMAGE - normal - jpeg - duplicate."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    value_original_delete_auxiliary_files = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES, "false"
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_pdf_2_image_normal_jpeg_duplicate <=========")

    stem_name_1: str = "pdf_scanned_ok"
    file_ext_1: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext_1)], libs.cfg.directory_inbox)

    stem_name_2: str = "pdf_scanned_ok_1_1"
    file_ext_2: str = "jpeg"

    pytest.helpers.help_run_action_all_complete_duplicate_file(
        file_ext_1, file_ext_2, stem_name_1, stem_name_2
    )

    # -------------------------------------------------------------------------
    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION,
        libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES,
        value_original_delete_auxiliary_files,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PDF_2_IMAGE - normal - png.
# -----------------------------------------------------------------------------
def test_run_action_pdf_2_image_normal_png(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PDF_2_IMAGE - normal - jpeg - duplicate."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_pdf_2_image_normal_png 1/2 <=========")

    stem_name: str = "pdf_scanned_ok"
    file_ext: str = "pdf"

    document_id, _file_pdf2image_1 = pytest.helpers.help_run_action_process_inbox_normal(
        stem_name,
        file_ext,
    )

    # -------------------------------------------------------------------------
    value_original_delete_auxiliary_files = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES, "false"
    )

    value_original_pdf2image_type = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION,
        libs.cfg.DCR_CFG_PDF2IMAGE_TYPE,
        libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_PNG,
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION,
        libs.cfg.DCR_CFG_DELETE_AUXILIARY_FILES,
        value_original_delete_auxiliary_files,
    )

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_PDF2IMAGE_TYPE, value_original_pdf2image_type
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_pdf_2_image_normal_png 2/2 <=========")

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
            stem_name + "_" + str(document_id) + "_1." + libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_PNG,
        ],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
