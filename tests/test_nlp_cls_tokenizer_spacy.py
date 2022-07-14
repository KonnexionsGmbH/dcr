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
        instance.process_document(
            document_file_name="",
            document_id=0,
            document_no_lines_footer=0,
            document_no_lines_header=0,
            document_no_lines_toc=0,
            file_encoding="",
            full_name="",
            is_json_sort_keys=False,
            is_spacy_ignore_bracket=False,
            is_spacy_ignore_left_punct=False,
            is_spacy_ignore_line_type_footer=False,
            is_spacy_ignore_line_type_header=False,
            is_spacy_ignore_line_type_heading=False,
            is_spacy_ignore_line_type_list_bullet=False,
            is_spacy_ignore_line_type_list_number=False,
            is_spacy_ignore_line_type_table=False,
            is_spacy_ignore_line_type_toc=False,
            is_spacy_ignore_punct=False,
            is_spacy_ignore_quote=False,
            is_spacy_ignore_right_punct=False,
            is_spacy_ignore_space=False,
            is_spacy_ignore_stop=False,
            is_spacy_tkn_attr_cluster=False,
            is_spacy_tkn_attr_dep_=False,
            is_spacy_tkn_attr_doc=False,
            is_spacy_tkn_attr_ent_iob_=False,
            is_spacy_tkn_attr_ent_kb_id_=False,
            is_spacy_tkn_attr_ent_type_=False,
            is_spacy_tkn_attr_head=False,
            is_spacy_tkn_attr_i=False,
            is_spacy_tkn_attr_idx=False,
            is_spacy_tkn_attr_is_alpha=False,
            is_spacy_tkn_attr_is_ascii=False,
            is_spacy_tkn_attr_is_bracket=False,
            is_spacy_tkn_attr_is_currency=False,
            is_spacy_tkn_attr_is_digit=False,
            is_spacy_tkn_attr_is_left_punct=False,
            is_spacy_tkn_attr_is_lower=False,
            is_spacy_tkn_attr_is_oov=False,
            is_spacy_tkn_attr_is_punct=False,
            is_spacy_tkn_attr_is_quote=False,
            is_spacy_tkn_attr_is_right_punct=False,
            is_spacy_tkn_attr_is_sent_end=False,
            is_spacy_tkn_attr_is_sent_start=False,
            is_spacy_tkn_attr_is_space=False,
            is_spacy_tkn_attr_is_stop=False,
            is_spacy_tkn_attr_is_title=False,
            is_spacy_tkn_attr_is_upper=False,
            is_spacy_tkn_attr_lang_=False,
            is_spacy_tkn_attr_left_edge=False,
            is_spacy_tkn_attr_lemma_=False,
            is_spacy_tkn_attr_lex=False,
            is_spacy_tkn_attr_lex_id=False,
            is_spacy_tkn_attr_like_email=False,
            is_spacy_tkn_attr_like_num=False,
            is_spacy_tkn_attr_like_url=False,
            is_spacy_tkn_attr_lower_=False,
            is_spacy_tkn_attr_morph=False,
            is_spacy_tkn_attr_norm_=False,
            is_spacy_tkn_attr_orth_=False,
            is_spacy_tkn_attr_pos_=False,
            is_spacy_tkn_attr_prefix_=False,
            is_spacy_tkn_attr_prob=False,
            is_spacy_tkn_attr_rank=False,
            is_spacy_tkn_attr_right_edge=False,
            is_spacy_tkn_attr_sent=False,
            is_spacy_tkn_attr_sentiment=False,
            is_spacy_tkn_attr_shape_=False,
            is_spacy_tkn_attr_suffix_=False,
            is_spacy_tkn_attr_tag_=False,
            is_spacy_tkn_attr_tensor=False,
            is_spacy_tkn_attr_text=False,
            is_spacy_tkn_attr_text_with_ws=False,
            is_spacy_tkn_attr_vocab=False,
            is_spacy_tkn_attr_whitespace_=False,
            is_tokenize_2_jsonfile=False,
            json_indent="",
            pipeline_name="en_core_web_trf",
        )

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing: process_document()"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing: process_document()"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
