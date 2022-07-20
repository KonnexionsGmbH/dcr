# pylint: disable=unused-argument
"""Testing Module nlp.cls_text_parser."""

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_run
import pytest

import dcr
import dcr_core.nlp.cls_nlp_core
import dcr_core.nlp.cls_text_parser
import dcr_core.nlp.cls_tokenizer_spacy
import dcr_core.utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test TextParser.
# -----------------------------------------------------------------------------
def test_cls_text_parser(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test TextParser."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_mini", "pdf"),
        ],
        target_path=dcr_core.cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.restore_config_params(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    dcr_core.nlp.cls_text_parser.TextParser.from_files(
        file_encoding=dcr_core.cfg.glob.FILE_ENCODING_DEFAULT,
        full_name_line=dcr_core.utils.get_full_name(dcr_core.cfg.glob.setup.directory_inbox_accepted, "pdf_mini_1.line.json"),
        full_name_page=dcr_core.utils.get_full_name(dcr_core.cfg.glob.setup.directory_inbox_accepted, "pdf_mini_1.page.json"),
        full_name_word=dcr_core.utils.get_full_name(dcr_core.cfg.glob.setup.directory_inbox_accepted, "pdf_mini_1.word.json"),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
