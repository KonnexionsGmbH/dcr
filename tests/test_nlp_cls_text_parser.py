# pylint: disable=unused-argument
"""Testing Module nlp.cls_text_parser."""

import pytest

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_action
import dcr.db.cls_db_core
import dcr.db.cls_document
import dcr.db.cls_run
import dcr.launcher
import dcr_core.cls_nlp_core
import dcr_core.cls_text_parser
import dcr_core.cls_tokenizer_spacy
import dcr_core.core_glob
import dcr_core.core_utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test TextParser.
# -----------------------------------------------------------------------------
def test_cls_text_parser(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test TextParser."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_mini", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )

    # -------------------------------------------------------------------------
    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PARSER])

    # -------------------------------------------------------------------------
    dcr_core.cls_text_parser.TextParser.from_files(
        file_encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT,
        full_name_line=dcr_core.core_utils.get_full_name(dcr_core.core_glob.setup.directory_inbox_accepted, "pdf_mini_1.line.json"),
        full_name_page=dcr_core.core_utils.get_full_name(dcr_core.core_glob.setup.directory_inbox_accepted, "pdf_mini_1.page.json"),
        full_name_word=dcr_core.core_utils.get_full_name(dcr_core.core_glob.setup.directory_inbox_accepted, "pdf_mini_1.word.json"),
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)
