# pylint: disable=unused-argument
"""Testing Module libs.pandoc."""
import libs.cfg
import libs.db
import libs.db.cfg
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_NON_PDF_2_PDF - normal.
# -----------------------------------------------------------------------------
def test_run_action_non_pdf_2_pdf_normal(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_NON_PDF_2_PDF - normal."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name: str = "docx_ok"
    file_ext: str = "docx"

    document_id, file_p_i = pytest.helpers.help_run_action_process_inbox_normal(file_ext, stem_name)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_NON_PDF_2_PDF])

    # -------------------------------------------------------------------------
    no_files_expected = (0, 2, 0)

    file_n_2_p = (
        libs.cfg.directory_inbox_accepted,
        [stem_name, str(document_id)],
        libs.db.cfg.DOCUMENT_FILE_TYPE_PDF,
    )

    files_to_be_checked = [
        file_p_i,
        file_n_2_p,
    ]

    pytest.helpers.verify_content_inboxes(
        files_to_be_checked,
        no_files_expected,
    )

    # -------------------------------------------------------------------------
    fxtr_rmdir_opt(libs.cfg.directory_inbox_accepted)

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_NON_PDF_2_PDF])

    assert expt.type == SystemExit, "inbox_accepted directory missing"
    assert expt.value.code == 1, "inbox_accepted, directory missing"

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
