# pylint: disable=unused-argument
"""Testing Module libs.pdf2image."""
import libs.cfg
import libs.db
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PDF_2_IMAGE - normal - jpeg.
# -----------------------------------------------------------------------------
def test_run_action_pdf_2_image_normal_jpeg(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PDF_2_IMAGE - normal - jpeg."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name: str = "pdf_scanned_ok"
    file_ext: str = "pdf"

    document_id, file_p_i = pytest.helpers.help_run_action_pdf_2_image_normal(file_ext, stem_name)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    # -------------------------------------------------------------------------
    child_no: int = 1
    no_files_expected = (0, 2, 0)

    file_p_2_i = (
        libs.cfg.directory_inbox_accepted,
        [stem_name, str(document_id), str(child_no)],
        libs.cfg.pdf2image_type,
    )

    files_to_be_checked = [
        file_p_i,
        file_p_2_i,
    ]

    pytest.helpers.verify_content_inboxes(
        files_to_be_checked,
        no_files_expected,
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
    stem_name_1: str = "pdf_scanned_ok"
    file_ext_1: str = "pdf"

    pytest.helpers.copy_files_from_pytest_2_dir(
        [(stem_name_1, file_ext_1)], libs.cfg.directory_inbox
    )

    stem_name_2: str = "pdf_scanned_ok_1_1"
    file_ext_2: str = "jpeg"

    pytest.helpers.help_run_action_pdf_2_image_normal_jpeg_duplicate(
        file_ext_1, file_ext_2, stem_name_1, stem_name_2
    )


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PDF_2_IMAGE - normal - png.
# -----------------------------------------------------------------------------
def test_run_action_pdf_2_image_normal_png(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PDF_2_IMAGE - normal - jpeg - duplicate."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name: str = "pdf_scanned_ok"
    file_ext: str = "pdf"

    document_id, file_p_i = pytest.helpers.help_run_action_pdf_2_image_normal(file_ext, stem_name)

    # -------------------------------------------------------------------------
    value_original = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION,
        libs.cfg.DCR_CFG_PDF2IMAGE_TYPE,
        libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_PNG,
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_IGNORE_DUPLICATES, value_original
    )

    # -------------------------------------------------------------------------
    child_no: int = 1
    no_files_expected = (0, 2, 0)

    file_p_2_i = (
        libs.cfg.directory_inbox_accepted,
        [stem_name, str(document_id), str(child_no)],
        libs.cfg.pdf2image_type,
    )

    files_to_be_checked = [
        file_p_i,
        file_p_2_i,
    ]

    pytest.helpers.verify_content_inboxes(
        files_to_be_checked,
        no_files_expected,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
