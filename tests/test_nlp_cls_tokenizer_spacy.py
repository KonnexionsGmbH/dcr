# pylint: disable=unused-argument
"""Testing Module nlp.cls_tokenizer_spacy."""

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_run
import pytest

import dcr_core.nlp.cls_text_parser
import dcr_core.nlp.cls_tokenizer_spacy

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test TokenizeSpacy.
# -----------------------------------------------------------------------------
def test_cls_tokenizer_spacy(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test TokenizeSpacy."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    instance = dcr_core.nlp.cls_tokenizer_spacy.TokenizerSpacy()
    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - tokenizer_spacy - Document.
# -----------------------------------------------------------------------------
def test_missing_dependencies_tokenizer_spacy_document(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - tokenizer_spacy - Document."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    cfg.glob.db_document = db.cls_document.Document(action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_document=True)

    # -------------------------------------------------------------------------
    instance = dcr_core.nlp.cls_tokenizer_spacy.TokenizerSpacy()

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        instance._finish_document()

    assert expt.type == SystemExit, "Instance of class 'Document' is missing: _finish_document()"
    assert expt.value.code == 1, "Instance of class 'Document' is missing: _finish_document()"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        instance._finish_sent()

    assert expt.type == SystemExit, "Instance of class 'Document' is missing: _finish_sent()"
    assert expt.value.code == 1, "Instance of class 'Document' is missing: _finish_sent()"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - tokenizer_spacy - Setup.
# -----------------------------------------------------------------------------
def test_missing_dependencies_tokenizer_spacy_setup(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - tokenizer_spacy - Setup."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    instance = dcr_core.nlp.cls_tokenizer_spacy.TokenizerSpacy()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_setup=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr_core.nlp.cls_tokenizer_spacy.TokenizerSpacy()

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing: __init__()"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing: __init__()"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        instance.process_document(full_name="", pipeline_name="en_core_web_trf")

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing: process_document()"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing: process_document()"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - tokenizer_spacy - TextParser.
# -----------------------------------------------------------------------------
def test_missing_dependencies_tokenizer_spacy_text_parser(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - tokenizer_spacy - TextParser."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    cfg.glob.db_document = db.cls_document.Document(action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_text_parser=True)

    # -------------------------------------------------------------------------
    instance = dcr_core.nlp.cls_tokenizer_spacy.TokenizerSpacy()

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
        instance.process_document(full_name="", pipeline_name="en_core_web_trf")

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing: process_document()"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing: process_document()"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
