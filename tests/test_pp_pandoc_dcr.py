# pylint: disable=unused-argument
"""Testing Module pp.pandoc_dcr."""
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
# Test RUN_ACTION_NON_PDF_2_PDF - coverage.
# -----------------------------------------------------------------------------
def test_run_action_non_pdf_2_pdf_coverage(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_NON_PDF_2_PDF - coverage."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("p_2_header_0_footer_2_text_0", "docx"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PANDOC])

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_NON_PDF_2_PDF - normal - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_non_pdf_2_pdf_normal_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_NON_PDF_2_PDF - normal - duplicate."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_non_pdf_2_pdf_normal_duplicate <=========")

    stem_name_1: str = "docx_ok"
    file_ext_1: str = "docx"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext_1)], cfg.glob.setup.directory_inbox)

    stem_name_2: str = "docx_ok_1"
    file_ext_2: str = "pdf"

    pytest.helpers.help_run_action_all_complete_duplicate_file(file_ext_1, file_ext_2, stem_name_1, stem_name_2)

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_NON_PDF_2_PDF - normal -keep.
# -----------------------------------------------------------------------------
def test_run_action_non_pdf_2_pdf_normal_keep(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_NON_PDF_2_PDF - normal - keep."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

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
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PANDOC])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_non_pdf_2_pdf_normal <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
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
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_NON_PDF_2_PDF - special.
# -----------------------------------------------------------------------------
def test_run_action_non_pdf_2_pdf_special(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_NON_PDF_2_PDF - special."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    fxtr_rmdir_opt(cfg.glob.setup.directory_inbox_accepted)

    with pytest.raises(SystemExit) as expt:
        dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PANDOC])

    assert expt.type == SystemExit, "inbox_accepted directory missing"
    assert expt.value.code == 1, "inbox_accepted, directory missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
