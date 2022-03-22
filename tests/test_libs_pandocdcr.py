# pylint: disable=unused-argument
"""Testing Module libs.pandocdcr."""
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
# Test RUN_ACTION_NON_PDF_2_PDF - normal.
# -----------------------------------------------------------------------------
def test_run_action_non_pdf_2_pdf_normal(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_NON_PDF_2_PDF - normal."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_from_pytest_2_dir(
        [
            ("csv_ok", "csv"),
            ("docx_ok", "docx"),
            ("epub_ok", "epub"),
            ("html_ok", "html"),
            ("odt_ok", "odt"),
            ("rst_ok", "rst"),
            ("rtf_ok", "rtf"),
        ],
        libs.cfg.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_NON_PDF_2_PDF])

    # -------------------------------------------------------------------------
    no_files_expected = (0, 14, 0)

    files_to_be_checked = [
        (
            libs.cfg.directory_inbox_accepted,
            ["csv_ok", "1"],
            "csv",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["csv_ok", "1"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["docx_ok", "3"],
            "docx",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["docx_ok", "3"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["epub_ok", "5"],
            "epub",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["epub_ok", "5"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["html_ok", "7"],
            "html",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["html_ok", "7"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["odt_ok", "9"],
            "odt",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["odt_ok", "9"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["rst_ok", "11"],
            "rst",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["rst_ok", "11"],
            "pdf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["rtf_ok", "13"],
            "rtf",
        ),
        (
            libs.cfg.directory_inbox_accepted,
            ["rtf_ok", "13"],
            "pdf",
        ),
    ]

    pytest.helpers.verify_content_inboxes(
        files_to_be_checked,
        no_files_expected,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_NON_PDF_2_PDF - normal - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_non_pdf_2_pdf_normal_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_NON_PDF_2_PDF - normal - duplicate."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name_1: str = "docx_ok"
    file_ext_1: str = "docx"

    pytest.helpers.copy_files_from_pytest_2_dir(
        [(stem_name_1, file_ext_1)], libs.cfg.directory_inbox
    )

    stem_name_2: str = "docx_ok_1"
    file_ext_2: str = "pdf"

    pytest.helpers.help_run_action_all_complete_duplicate_file(
        file_ext_1, file_ext_2, stem_name_1, stem_name_2
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
    fxtr_rmdir_opt(libs.cfg.directory_inbox_accepted)

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_NON_PDF_2_PDF])

    assert expt.type == SystemExit, "inbox_accepted directory missing"
    assert expt.value.code == 1, "inbox_accepted, directory missing"

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
