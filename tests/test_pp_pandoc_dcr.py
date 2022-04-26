# pylint: disable=unused-argument
"""Testing Module pp.pandoc_dcr."""
import libs.cfg
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_NON_PDF_2_PDF - normal - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_non_pdf_2_pdf_normal_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_NON_PDF_2_PDF - normal - duplicate."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_non_pdf_2_pdf_normal_duplicate <=========")

    stem_name_1: str = "docx_ok"
    file_ext_1: str = "docx"

    pytest.helpers.copy_files_4_pytest_2_dir(
        [(stem_name_1, file_ext_1)], libs.cfg.config.directory_inbox
    )

    stem_name_2: str = "docx_ok_1"
    file_ext_2: str = "pdf"

    pytest.helpers.help_run_action_all_complete_duplicate_file(
        file_ext_1, file_ext_2, stem_name_1, stem_name_2
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_NON_PDF_2_PDF - normal -keep.
# -----------------------------------------------------------------------------
def test_run_action_non_pdf_2_pdf_normal_keep(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_NON_PDF_2_PDF - normal - keep."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("csv_ok", "csv"),
            ("docx_ok", "docx"),
            ("epub_ok", "epub"),
            ("html_ok", "html"),
            ("odt_ok", "odt"),
            ("rst_ok", "rst"),
            ("rtf_ok", "rtf"),
        ],
        libs.cfg.config.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_NON_PDF_2_PDF])

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.info("=========> test_run_action_non_pdf_2_pdf_normal <=========")

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox_accepted,
        [],
        [
            "csv_ok_1.csv",
            "csv_ok_1.pdf",
            "docx_ok_3.docx",
            "docx_ok_3.pdf",
            "epub_ok_5.epub",
            "epub_ok_5.pdf",
            "html_ok_7.html",
            "html_ok_7.pdf",
            "odt_ok_9.odt",
            "odt_ok_9.pdf",
            "rst_ok_11.rst",
            "rst_ok_11.pdf",
            "rtf_ok_13.rtf",
            "rtf_ok_13.pdf",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        libs.cfg.config.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_NON_PDF_2_PDF - special.
# -----------------------------------------------------------------------------
def test_run_action_non_pdf_2_pdf_special(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_NON_PDF_2_PDF - special."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    fxtr_rmdir_opt(libs.cfg.config.directory_inbox_accepted)

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_NON_PDF_2_PDF])

    assert expt.type == SystemExit, "inbox_accepted directory missing"
    assert expt.value.code == 1, "inbox_accepted, directory missing"

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
