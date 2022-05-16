"""Module nlp.tokenizer: Store the document tokens page by page in the
database."""

import json
import time
from typing import Dict

import cfg.glob
import db.cls_action
import db.cls_base
import db.cls_run
import db.dml
import spacy
import spacy.tokens
import utils


# pylint: disable=R0912
# pylint: disable=R0915
# -----------------------------------------------------------------------------
# Extract the text from the page lines.
# -----------------------------------------------------------------------------
def get_text_from_line_2_page() -> str:
    """Extract the text from the page data.

    Returns:
        str: Reconstructed text.
    """
    line_0_lines = []

    for cfg.glob.parse_result_line_0_line in cfg.glob.parse_result_line_2_page[cfg.glob.JSON_NAME_LINES]:
        if cfg.glob.parse_result_line_0_line[cfg.glob.JSON_NAME_LINE_TYPE] == cfg.glob.DOCUMENT_LINE_TYPE_BODY:
            line_0_lines.append(cfg.glob.parse_result_line_0_line[cfg.glob.JSON_NAME_LINE_TEXT])

    return "\n".join(line_0_lines)


# -----------------------------------------------------------------------------
# Determine the requested token attributes.
# -----------------------------------------------------------------------------
def get_token_attributes(token: spacy.tokens.Token) -> Dict[str, bool | float | int | str]:  # noqa: C901
    """Determine the requested token attributes.

    Args:
        token (spacy.tokens.Token): spaCy token.

    Returns:
        Dict[str, bool | float | int | str]: Requested token attributes.
    """
    token_attr = {}

    if cfg.glob.setup.is_spacy_tkn_attr_cluster:
        if token.cluster != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_CLUSTER] = token.cluster

    if cfg.glob.setup.is_spacy_tkn_attr_dep_:
        if token.dep_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_DEP_] = token.dep_

    if cfg.glob.setup.is_spacy_tkn_attr_doc:
        if token.doc is not None:
            token_attr[cfg.glob.JSON_NAME_TOKEN_DOC] = token.doc.text

    if cfg.glob.setup.is_spacy_tkn_attr_ent_iob_:
        if token.ent_iob_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_ENT_IOB_] = token.ent_iob_

    if cfg.glob.setup.is_spacy_tkn_attr_ent_kb_id_:
        # not testable
        if token.ent_kb_id_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_ENT_KB_ID_] = token.ent_kb_id_

    if cfg.glob.setup.is_spacy_tkn_attr_ent_type_:
        if token.ent_type_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_ENT_TYPE_] = token.ent_type_

    if cfg.glob.setup.is_spacy_tkn_attr_head:
        if token.head is not None:
            token_attr[cfg.glob.JSON_NAME_TOKEN_HEAD] = token.head.i

    if cfg.glob.setup.is_spacy_tkn_attr_i:
        token_attr[cfg.glob.JSON_NAME_TOKEN_I] = token.i

    if cfg.glob.setup.is_spacy_tkn_attr_idx:
        if token.idx != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_IDX] = token.idx

    if cfg.glob.setup.is_spacy_tkn_attr_is_alpha:
        if token.is_alpha:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_ALPHA] = token.is_alpha

    if cfg.glob.setup.is_spacy_tkn_attr_is_ascii:
        if token.is_ascii:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_ASCII] = token.is_ascii

    if cfg.glob.setup.is_spacy_tkn_attr_is_bracket:
        if token.is_bracket:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_BRACKET] = token.is_bracket

    if cfg.glob.setup.is_spacy_tkn_attr_is_currency:
        if token.is_currency:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_CURRENCY] = token.is_currency

    if cfg.glob.setup.is_spacy_tkn_attr_is_digit:
        if token.is_digit:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_DIGIT] = token.is_digit

    if cfg.glob.setup.is_spacy_tkn_attr_is_left_punct:
        if token.is_left_punct:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_LEFT_PUNCT] = token.is_left_punct

    if cfg.glob.setup.is_spacy_tkn_attr_is_lower:
        if token.is_lower:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_LOWER] = token.is_lower

    if cfg.glob.setup.is_spacy_tkn_attr_is_oov:
        if token.is_oov:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_OOV] = token.is_oov

    if cfg.glob.setup.is_spacy_tkn_attr_is_punct:
        if token.is_punct:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_PUNCT] = token.is_punct

    if cfg.glob.setup.is_spacy_tkn_attr_is_quote:
        if token.is_quote:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_QUOTE] = token.is_quote

    if cfg.glob.setup.is_spacy_tkn_attr_is_right_punct:
        if token.is_right_punct:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_RIGHT_PUNCT] = token.is_right_punct

    if cfg.glob.setup.is_spacy_tkn_attr_is_sent_end:
        if token.is_sent_end:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_SENT_END] = token.is_sent_end

    if cfg.glob.setup.is_spacy_tkn_attr_is_sent_start:
        if token.is_sent_start:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_SENT_START] = token.is_sent_start

    if cfg.glob.setup.is_spacy_tkn_attr_is_space:
        if token.is_space:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_SPACE] = token.is_space

    if cfg.glob.setup.is_spacy_tkn_attr_is_stop:
        if token.is_stop:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_STOP] = token.is_stop

    if cfg.glob.setup.is_spacy_tkn_attr_is_title:
        if token.is_title:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_TITLE] = token.is_title

    if cfg.glob.setup.is_spacy_tkn_attr_is_upper:
        if token.is_upper:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_UPPER] = token.is_upper

    if cfg.glob.setup.is_spacy_tkn_attr_lang_:
        if token.lang_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_LANG_] = token.lang_

    if cfg.glob.setup.is_spacy_tkn_attr_left_edge:
        if token.left_edge.text is not None:
            token_attr[cfg.glob.JSON_NAME_TOKEN_LEFT_EDGE] = token.left_edge.i

    if cfg.glob.setup.is_spacy_tkn_attr_lemma_:
        if token.lemma_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_LEMMA_] = token.lemma_

    if cfg.glob.setup.is_spacy_tkn_attr_lex:
        if token.lex is not None:
            token_attr[cfg.glob.JSON_NAME_TOKEN_LEX] = token.lex.text

    if cfg.glob.setup.is_spacy_tkn_attr_lex_id:
        if token.lex_id != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_LEX_ID] = token.lex_id

    if cfg.glob.setup.is_spacy_tkn_attr_like_email:
        if token.like_email:
            token_attr[cfg.glob.JSON_NAME_TOKEN_LIKE_EMAIL] = token.like_email

    if cfg.glob.setup.is_spacy_tkn_attr_like_num:
        if token.like_num:
            token_attr[cfg.glob.JSON_NAME_TOKEN_LIKE_NUM] = token.like_num

    if cfg.glob.setup.is_spacy_tkn_attr_like_url:
        if token.like_url:
            token_attr[cfg.glob.JSON_NAME_TOKEN_LIKE_URL] = token.like_url

    if cfg.glob.setup.is_spacy_tkn_attr_lower_:
        if token.lower_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_LOWER_] = token.lower_

    if cfg.glob.setup.is_spacy_tkn_attr_morph:
        if token.morph is not None:
            token_attr[cfg.glob.JSON_NAME_TOKEN_MORPH] = token.morph.__str__()

    if cfg.glob.setup.is_spacy_tkn_attr_norm_:
        if token.norm_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_NORM_] = token.norm_

    if cfg.glob.setup.is_spacy_tkn_attr_orth_:
        if token.orth_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_ORTH_] = token.orth_

    if cfg.glob.setup.is_spacy_tkn_attr_pos_:
        if token.pos_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_POS_] = token.pos_

    if cfg.glob.setup.is_spacy_tkn_attr_prefix_:
        if token.prefix_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_PREFIX_] = token.prefix_

    if cfg.glob.setup.is_spacy_tkn_attr_prob:
        if token.prob != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_PROB] = token.prob

    if cfg.glob.setup.is_spacy_tkn_attr_rank:
        if token.rank != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_RANK] = token.rank

    if cfg.glob.setup.is_spacy_tkn_attr_right_edge:
        if token.right_edge is not None:
            token_attr[cfg.glob.JSON_NAME_TOKEN_RIGHT_EDGE] = token.right_edge.i

    if cfg.glob.setup.is_spacy_tkn_attr_sent:
        if token.sent is not None:
            token_attr[cfg.glob.JSON_NAME_TOKEN_SENT] = token.sent.text

    if cfg.glob.setup.is_spacy_tkn_attr_sentiment:
        if token.sentiment != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_SENTIMENT] = token.sentiment

    if cfg.glob.setup.is_spacy_tkn_attr_shape_:
        if token.shape_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_SHAPE_] = token.shape_

    if cfg.glob.setup.is_spacy_tkn_attr_suffix_:
        if token.suffix_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_SUFFIX_] = token.suffix_

    if cfg.glob.setup.is_spacy_tkn_attr_tag_:
        if token.tag_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_TAG_] = token.tag_

    if cfg.glob.setup.is_spacy_tkn_attr_tensor:
        try:
            token_attr[cfg.glob.JSON_NAME_TOKEN_TENSOR] = token.tensor.__str__()
        except IndexError:
            pass

    if cfg.glob.setup.is_spacy_tkn_attr_text:
        if token.text != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_TEXT] = token.text

    if cfg.glob.setup.is_spacy_tkn_attr_text_with_ws:
        if token.text_with_ws != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_TEXT_WITH_WS] = token.text_with_ws

    if cfg.glob.setup.is_spacy_tkn_attr_vocab:
        if token.vocab is not None:
            token_attr[cfg.glob.JSON_NAME_TOKEN_RANK] = token.vocab.__str__()

    if cfg.glob.setup.is_spacy_tkn_attr_whitespace_:
        if token.whitespace_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_WHITESPACE_] = token.whitespace_

    return token_attr


# -----------------------------------------------------------------------------
# Create document tokens (step: tkn).
# -----------------------------------------------------------------------------
def tokenize() -> None:
    """Create document tokens (step: tkn).

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    nlp: spacy.Language
    spacy_model_current: str | None = None

    with cfg.glob.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(
            conn=conn, action_code=db.cls_run.Run.ACTION_CODE_TOKENIZE
        )

        for row in rows:
            # ------------------------------------------------------------------
            # Processing a single document
            # ------------------------------------------------------------------
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_row(row)

            if cfg.glob.action_curr.action_status == cfg.glob.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                cfg.glob.run.total_status_ready += 1

            cfg.glob.base = db.cls_base.Base.from_id(id_base=cfg.glob.action_curr.action_id_base)

            spacy_model = cfg.glob.languages_spacy[cfg.glob.base.base_id_language]

            if spacy_model != spacy_model_current:
                nlp = spacy.load(spacy_model)
                spacy_model_current = spacy_model

            tokenize_file(nlp)

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the tokens of a document page by page (step: tkn).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def tokenize_file(nlp: spacy.Language) -> None:
    """Create the tokens of a document page by page.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name_curr = cfg.glob.action_curr.get_full_name()

    if cfg.glob.setup.is_tokenize_2_jsonfile:
        file_name_next = cfg.glob.action_curr.get_stem_name() + ".token." + cfg.glob.DOCUMENT_FILE_TYPE_JSON
        full_name_next = utils.get_full_name(
            cfg.glob.action_curr.action_directory_name,
            file_name_next,
        )
    else:
        full_name_next = None

    with open(full_name_curr, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
        cfg.glob.parse_result_line_4_document = json.load(file_handle)

        cfg.glob.token_3_pages = []

        for cfg.glob.parse_result_line_2_page in cfg.glob.parse_result_line_4_document[cfg.glob.JSON_NAME_PAGES]:
            # ------------------------------------------------------------------
            # Processing a single page
            # ------------------------------------------------------------------
            page_no = cfg.glob.parse_result_line_2_page[cfg.glob.JSON_NAME_PAGE_NO]

            text = get_text_from_line_2_page()

            cfg.glob.token_1_tokens = []

            for token in nlp(text):
                cfg.glob.token_1_tokens.append(get_token_attributes(token))

            cfg.glob.token_2_page = {
                cfg.glob.JSON_NAME_PAGE_NO: page_no,
                cfg.glob.JSON_NAME_NO_TOKENS_IN_PAGE: len(cfg.glob.token_1_tokens),
                cfg.glob.JSON_NAME_TOKENS: cfg.glob.token_1_tokens,
            }

            if cfg.glob.setup.is_tokenize_2_database:
                db.dml.insert_dbt_row(
                    cfg.glob.DBT_TOKEN,
                    {
                        cfg.glob.DBC_ID_BASE: cfg.glob.base.base_id,
                        cfg.glob.DBC_PAGE_DATA: cfg.glob.token_2_page,
                        cfg.glob.DBC_PAGE_NO: page_no,
                    },
                )

            if cfg.glob.setup.is_tokenize_2_jsonfile:
                cfg.glob.token_3_pages.append(cfg.glob.token_2_page)

    if cfg.glob.setup.is_tokenize_2_jsonfile:
        with open(full_name_next, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(
                {
                    cfg.glob.JSON_NAME_BASE_ID: cfg.glob.base.base_id,
                    cfg.glob.JSON_NAME_BASE_FILE_NAME: cfg.glob.base.base_file_name,
                    cfg.glob.JSON_NAME_NO_PAGES_IN_DOC: cfg.glob.parse_result_line_4_document[
                        cfg.glob.JSON_NAME_NO_PAGES_IN_DOC
                    ],
                    cfg.glob.JSON_NAME_PAGES: cfg.glob.token_3_pages,
                },
                file_handle,
            )

    utils.delete_auxiliary_file(full_name_curr)

    cfg.glob.run.run_total_processed_ok += 1

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
