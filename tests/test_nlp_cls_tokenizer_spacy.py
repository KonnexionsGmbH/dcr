# pylint: disable=unused-argument
"""Testing Module nlp.cls_tokenizer_spacy."""

import pytest

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_action
import dcr.db.cls_db_core
import dcr.db.cls_document
import dcr.db.cls_run
import dcr_core.cls_text_parser
import dcr_core.cls_tokenizer_spacy

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test TokenizeSpacy.
# -----------------------------------------------------------------------------
def test_cls_tokenizer_spacy(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test TokenizeSpacy."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_tokenizer_spacy.TokenizerSpacy()
    instance.exists()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - tokenizer_spacy - TextParser.
# -----------------------------------------------------------------------------
def test_missing_dependencies_tokenizer_spacy_text_parser(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - tokenizer_spacy - TextParser."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_document = dcr.db.cls_document.Document(
        action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_text_parser=True)

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_tokenizer_spacy.TokenizerSpacy()

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        instance._init_para()

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing: _init_para()"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing: _init_para()"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        instance._process_page()

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing: _process_page()"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing: _process_page()"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        instance._process_para()

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing: _process_para()"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing: _process_para()"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        instance.process_document(
            document_id=0,
            file_name_next="",
            file_name_orig="",
            no_lines_footer=0,
            no_lines_header=0,
            no_lines_toc=0,
            pipeline_name="en_core_web_trf",
        )

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing: process_document()"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing: process_document()"

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)
