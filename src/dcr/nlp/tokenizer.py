"""Module nlp.cls_tokenizer: Store the document tokens page by page in the
database."""

import time

import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_language
import db.cls_run
import db.cls_token
import utils

import dcr_core.cfg.glob
import dcr_core.nlp.cls_nlp_core
import dcr_core.nlp.cls_text_parser
import dcr_core.nlp.cls_tokenizer_spacy
import dcr_core.utils

# -----------------------------------------------------------------------------
# Global constants.
# -----------------------------------------------------------------------------
ERROR_71_901 = "71.901 Issue (tkn): Tokenizing the file '{full_name_curr}' failed - " + "error type: '{error_type}' - error: '{error}'."


# -----------------------------------------------------------------------------
# Save the tokens sentence by sentence in the database.
# -----------------------------------------------------------------------------
def store_tokens_in_database() -> None:
    """Save the tokens sentence by sentence in the database."""
    if not cfg.glob.setup.is_tokenize_2_database:
        return

    for page in dcr_core.cfg.glob.tokenizer_spacy.token_pages:
        page_no = page[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]
        paras = page[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARAS]
        for para in paras:
            para_no = para[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]
            sents = para[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_SENTS]
            for sent in sents:
                if dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO in sent:
                    column_no = sent[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO]
                    row_no = sent[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO]
                else:
                    column_no = 0
                    row_no = 0

                if dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN in sent:
                    column_span = sent[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN]
                else:
                    column_span = 0

                db.cls_token.Token(
                    id_document=cfg.glob.document.document_id,
                    column_no=column_no,
                    column_span=column_span,
                    coord_llx=sent[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX],
                    coord_urx=sent[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX],
                    line_type=sent[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE],
                    no_tokens_in_sent=sent[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT],
                    page_no=page_no,
                    para_no=para_no,
                    row_no=row_no,
                    sent_no=sent[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_SENT_NO],
                    text=sent[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT],
                    tokens=sent[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKENS],  # type: ignore
                )


# -----------------------------------------------------------------------------
# Create document tokens (step: tkn).
# -----------------------------------------------------------------------------
def tokenize() -> None:
    """Create document tokens (step: tkn).

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    dcr_core.cfg.glob.tokenizer_spacy = dcr_core.nlp.cls_tokenizer_spacy.TokenizerSpacy()

    with cfg.glob.db_core.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(conn=conn, action_code=db.cls_run.Run.ACTION_CODE_TOKENIZE)

        for row in rows:
            # ------------------------------------------------------------------
            # Processing a single document
            # ------------------------------------------------------------------
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_row(row)

            if cfg.glob.action_curr.action_status == db.cls_document.Document.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                cfg.glob.run.total_status_ready += 1

            tokenize_file()

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the tokens of a document page by page (step: tkn).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def tokenize_file() -> None:
    """Create the tokens of a document page by page.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    cfg.glob.document = db.cls_document.Document.from_id(id_document=cfg.glob.action_curr.action_id_document)

    pipeline_name = db.cls_language.Language.LANGUAGES_SPACY[cfg.glob.document.document_id_language]

    full_name_curr = cfg.glob.action_curr.get_full_name()

    if cfg.glob.setup.is_tokenize_2_jsonfile:
        file_name_next = cfg.glob.action_curr.get_stem_name() + "_token." + dcr_core.cfg.glob.FILE_TYPE_JSON
        full_name_next = dcr_core.utils.get_full_name(
            cfg.glob.action_curr.action_directory_name,
            file_name_next,
        )
    else:
        full_name_next = ""

    try:
        dcr_core.cfg.glob.text_parser = dcr_core.nlp.cls_text_parser.TextParser.from_files(
            file_encoding=cfg.glob.FILE_ENCODING_DEFAULT, full_name_line=full_name_curr
        )

        dcr_core.cfg.glob.tokenizer_spacy.process_document(
            document_file_name=cfg.glob.document.document_file_name,
            document_id=cfg.glob.document.document_id,
            document_no_lines_footer=cfg.glob.document.document_no_lines_footer,
            document_no_lines_header=cfg.glob.document.document_no_lines_header,
            document_no_lines_toc=cfg.glob.document.document_no_lines_toc,
            file_encoding=cfg.glob.FILE_ENCODING_DEFAULT,
            full_name=full_name_next,
            is_json_sort_keys=cfg.glob.setup.is_json_sort_keys,
            is_spacy_ignore_bracket=cfg.glob.setup.is_spacy_ignore_bracket,
            is_spacy_ignore_left_punct=cfg.glob.setup.is_spacy_ignore_left_punct,
            is_spacy_ignore_line_type_footer=cfg.glob.setup.is_spacy_ignore_line_type_footer,
            is_spacy_ignore_line_type_header=cfg.glob.setup.is_spacy_ignore_line_type_header,
            is_spacy_ignore_line_type_heading=cfg.glob.setup.is_spacy_ignore_line_type_heading,
            is_spacy_ignore_line_type_list_bullet=cfg.glob.setup.is_spacy_ignore_line_type_list_bullet,
            is_spacy_ignore_line_type_list_number=cfg.glob.setup.is_spacy_ignore_line_type_list_number,
            is_spacy_ignore_line_type_table=cfg.glob.setup.is_spacy_ignore_line_type_table,
            is_spacy_ignore_line_type_toc=cfg.glob.setup.is_spacy_ignore_line_type_toc,
            is_spacy_ignore_punct=cfg.glob.setup.is_spacy_ignore_punct,
            is_spacy_ignore_quote=cfg.glob.setup.is_spacy_ignore_quote,
            is_spacy_ignore_right_punct=cfg.glob.setup.is_spacy_ignore_right_punct,
            is_spacy_ignore_space=cfg.glob.setup.is_spacy_ignore_space,
            is_spacy_ignore_stop=cfg.glob.setup.is_spacy_ignore_stop,
            is_spacy_tkn_attr_cluster=cfg.glob.setup.is_spacy_tkn_attr_cluster,
            is_spacy_tkn_attr_dep_=cfg.glob.setup.is_spacy_tkn_attr_dep_,
            is_spacy_tkn_attr_doc=cfg.glob.setup.is_spacy_tkn_attr_doc,
            is_spacy_tkn_attr_ent_iob_=cfg.glob.setup.is_spacy_tkn_attr_ent_iob_,
            is_spacy_tkn_attr_ent_kb_id_=cfg.glob.setup.is_spacy_tkn_attr_ent_kb_id_,
            is_spacy_tkn_attr_ent_type_=cfg.glob.setup.is_spacy_tkn_attr_ent_type_,
            is_spacy_tkn_attr_head=cfg.glob.setup.is_spacy_tkn_attr_head,
            is_spacy_tkn_attr_i=cfg.glob.setup.is_spacy_tkn_attr_i,
            is_spacy_tkn_attr_idx=cfg.glob.setup.is_spacy_tkn_attr_idx,
            is_spacy_tkn_attr_is_alpha=cfg.glob.setup.is_spacy_tkn_attr_is_alpha,
            is_spacy_tkn_attr_is_ascii=cfg.glob.setup.is_spacy_tkn_attr_is_ascii,
            is_spacy_tkn_attr_is_bracket=cfg.glob.setup.is_spacy_tkn_attr_is_bracket,
            is_spacy_tkn_attr_is_currency=cfg.glob.setup.is_spacy_tkn_attr_is_currency,
            is_spacy_tkn_attr_is_digit=cfg.glob.setup.is_spacy_tkn_attr_is_digit,
            is_spacy_tkn_attr_is_left_punct=cfg.glob.setup.is_spacy_tkn_attr_is_left_punct,
            is_spacy_tkn_attr_is_lower=cfg.glob.setup.is_spacy_tkn_attr_is_lower,
            is_spacy_tkn_attr_is_oov=cfg.glob.setup.is_spacy_tkn_attr_is_oov,
            is_spacy_tkn_attr_is_punct=cfg.glob.setup.is_spacy_tkn_attr_is_punct,
            is_spacy_tkn_attr_is_quote=cfg.glob.setup.is_spacy_tkn_attr_is_quote,
            is_spacy_tkn_attr_is_right_punct=cfg.glob.setup.is_spacy_tkn_attr_is_right_punct,
            is_spacy_tkn_attr_is_sent_end=cfg.glob.setup.is_spacy_tkn_attr_is_sent_end,
            is_spacy_tkn_attr_is_sent_start=cfg.glob.setup.is_spacy_tkn_attr_is_sent_start,
            is_spacy_tkn_attr_is_space=cfg.glob.setup.is_spacy_tkn_attr_is_space,
            is_spacy_tkn_attr_is_stop=cfg.glob.setup.is_spacy_tkn_attr_is_stop,
            is_spacy_tkn_attr_is_title=cfg.glob.setup.is_spacy_tkn_attr_is_title,
            is_spacy_tkn_attr_is_upper=cfg.glob.setup.is_spacy_tkn_attr_is_upper,
            is_spacy_tkn_attr_lang_=cfg.glob.setup.is_spacy_tkn_attr_lang_,
            is_spacy_tkn_attr_left_edge=cfg.glob.setup.is_spacy_tkn_attr_left_edge,
            is_spacy_tkn_attr_lemma_=cfg.glob.setup.is_spacy_tkn_attr_lemma_,
            is_spacy_tkn_attr_lex=cfg.glob.setup.is_spacy_tkn_attr_lex,
            is_spacy_tkn_attr_lex_id=cfg.glob.setup.is_spacy_tkn_attr_lex_id,
            is_spacy_tkn_attr_like_email=cfg.glob.setup.is_spacy_tkn_attr_like_email,
            is_spacy_tkn_attr_like_num=cfg.glob.setup.is_spacy_tkn_attr_like_num,
            is_spacy_tkn_attr_like_url=cfg.glob.setup.is_spacy_tkn_attr_like_url,
            is_spacy_tkn_attr_lower_=cfg.glob.setup.is_spacy_tkn_attr_lower_,
            is_spacy_tkn_attr_morph=cfg.glob.setup.is_spacy_tkn_attr_morph,
            is_spacy_tkn_attr_norm_=cfg.glob.setup.is_spacy_tkn_attr_norm_,
            is_spacy_tkn_attr_orth_=cfg.glob.setup.is_spacy_tkn_attr_orth_,
            is_spacy_tkn_attr_pos_=cfg.glob.setup.is_spacy_tkn_attr_pos_,
            is_spacy_tkn_attr_prefix_=cfg.glob.setup.is_spacy_tkn_attr_prefix_,
            is_spacy_tkn_attr_prob=cfg.glob.setup.is_spacy_tkn_attr_prob,
            is_spacy_tkn_attr_rank=cfg.glob.setup.is_spacy_tkn_attr_rank,
            is_spacy_tkn_attr_right_edge=cfg.glob.setup.is_spacy_tkn_attr_right_edge,
            is_spacy_tkn_attr_sent=cfg.glob.setup.is_spacy_tkn_attr_sent,
            is_spacy_tkn_attr_sentiment=cfg.glob.setup.is_spacy_tkn_attr_sentiment,
            is_spacy_tkn_attr_shape_=cfg.glob.setup.is_spacy_tkn_attr_shape_,
            is_spacy_tkn_attr_suffix_=cfg.glob.setup.is_spacy_tkn_attr_suffix_,
            is_spacy_tkn_attr_tag_=cfg.glob.setup.is_spacy_tkn_attr_tag_,
            is_spacy_tkn_attr_tensor=cfg.glob.setup.is_spacy_tkn_attr_tensor,
            is_spacy_tkn_attr_text=cfg.glob.setup.is_spacy_tkn_attr_text,
            is_spacy_tkn_attr_text_with_ws=cfg.glob.setup.is_spacy_tkn_attr_text_with_ws,
            is_spacy_tkn_attr_vocab=cfg.glob.setup.is_spacy_tkn_attr_vocab,
            is_spacy_tkn_attr_whitespace_=cfg.glob.setup.is_spacy_tkn_attr_whitespace_,
            is_tokenize_2_jsonfile=cfg.glob.setup.is_tokenize_2_jsonfile,
            json_indent=cfg.glob.setup.json_indent,
            pipeline_name=pipeline_name,
        )

        if dcr_core.cfg.glob.tokenizer_spacy.processing_ok():
            store_tokens_in_database()
            utils.delete_auxiliary_file(full_name_curr)
            cfg.glob.action_curr.finalise()
            cfg.glob.run.run_total_processed_ok += 1

    except FileNotFoundError as err:
        cfg.glob.action_curr.finalise_error(
            error_code=db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_TOKENIZE,
            error_msg=ERROR_71_901.replace("{full_name_curr}", full_name_curr).replace("{error_type}", str(type(err))).replace("{error}", str(err)),
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
