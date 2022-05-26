"""Module nlp.tokenizer: Store the document tokens page by page in the
database."""

import json
import time
from typing import Dict

import cfg.glob
import db.cls_action
import db.cls_document
import db.cls_run
import db.dml
import nlp.cls_text_parser
import spacy
import spacy.tokens
import utils

# -----------------------------------------------------------------------------
# Global constants.
# -----------------------------------------------------------------------------
JSON_NAME_NO_TOKENS_IN_PAGE: str = "noTokensInPage"

JSON_NAME_TOKEN_CLUSTER: str = "tknCluster"
JSON_NAME_TOKEN_DEP_: str = "tknDep_"
JSON_NAME_TOKEN_DOC: str = "tknDoc"
JSON_NAME_TOKEN_ENT_IOB_: str = "tknEntIob_"
JSON_NAME_TOKEN_ENT_KB_ID_: str = "tknEntKbId_"
JSON_NAME_TOKEN_ENT_TYPE_: str = "tknEntType_"
JSON_NAME_TOKEN_HEAD: str = "tknHead"
JSON_NAME_TOKEN_I: str = "tknI"
JSON_NAME_TOKEN_IDX: str = "tknIdx"
JSON_NAME_TOKEN_IS_ALPHA: str = "tknIsAlpha"
JSON_NAME_TOKEN_IS_ASCII: str = "tknIsAscii"
JSON_NAME_TOKEN_IS_BRACKET: str = "tknIsBracket"
JSON_NAME_TOKEN_IS_CURRENCY: str = "tknIsCurrency"
JSON_NAME_TOKEN_IS_DIGIT: str = "tknIsDigit"
JSON_NAME_TOKEN_IS_LEFT_PUNCT: str = "tknIsLeftPunct"
JSON_NAME_TOKEN_IS_LOWER: str = "tknIsLower"
JSON_NAME_TOKEN_IS_OOV: str = "tknIsOov"
JSON_NAME_TOKEN_IS_PUNCT: str = "tknIsPunct"
JSON_NAME_TOKEN_IS_QUOTE: str = "tknIsQuote"
JSON_NAME_TOKEN_IS_RIGHT_PUNCT: str = "tknIsRightPunct"
JSON_NAME_TOKEN_IS_SENT_END: str = "tknIsSentEnd"
JSON_NAME_TOKEN_IS_SENT_START: str = "tknIsSentStart"
JSON_NAME_TOKEN_IS_SPACE: str = "tknIsSpace"
JSON_NAME_TOKEN_IS_STOP: str = "tknIsStop"
JSON_NAME_TOKEN_IS_TITLE: str = "tknIsTitle"
JSON_NAME_TOKEN_IS_UPPER: str = "tknIsUpper"
JSON_NAME_TOKEN_LANG_: str = "tknLang_"
JSON_NAME_TOKEN_LEFT_EDGE: str = "tknLeftEdge"
JSON_NAME_TOKEN_LEMMA_: str = "tknLemma_"
JSON_NAME_TOKEN_LEX: str = "tknLex"
JSON_NAME_TOKEN_LEX_ID: str = "tknLexId"
JSON_NAME_TOKEN_LIKE_EMAIL: str = "tknLikeEmail"
JSON_NAME_TOKEN_LIKE_NUM: str = "tknLikeNum"
JSON_NAME_TOKEN_LIKE_URL: str = "tknLikeUrl"
JSON_NAME_TOKEN_LOWER_: str = "tknLower_"
JSON_NAME_TOKEN_MORPH: str = "tknMorph"
JSON_NAME_TOKEN_NORM_: str = "tknNorm_"
JSON_NAME_TOKEN_ORTH_: str = "tknOrth_"
JSON_NAME_TOKEN_POS_: str = "tknPos_"
JSON_NAME_TOKEN_PREFIX_: str = "tknPrefix_"
JSON_NAME_TOKEN_PROB: str = "tknProb"
JSON_NAME_TOKEN_RANK: str = "tknRank"
JSON_NAME_TOKEN_RIGHT_EDGE: str = "tknRightEdge"
JSON_NAME_TOKEN_SENT: str = "tknSent"
JSON_NAME_TOKEN_SENTIMENT: str = "tknSentiment"
JSON_NAME_TOKEN_SHAPE_: str = "tknShape_"
JSON_NAME_TOKEN_SUFFIX_: str = "tknSuffix_"
JSON_NAME_TOKEN_TAG_: str = "tknTag_"
JSON_NAME_TOKEN_TENSOR: str = "tknTensor"
JSON_NAME_TOKEN_TEXT: str = "tknText"
JSON_NAME_TOKEN_TEXT_WITH_WS: str = "tknTextWithWs"
JSON_NAME_TOKEN_WHITESPACE_: str = "tknWhitespace_"

JSON_NAME_TOKENS: str = "tokens"


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

    for cfg.glob.text_parser.parse_result_line_0_line in cfg.glob.text_parser.parse_result_line_2_page[
        cfg.glob.text_parser.JSON_NAME_LINES
    ]:
        if (
            cfg.glob.text_parser.parse_result_line_0_line[cfg.glob.text_parser.JSON_NAME_LINE_TYPE]
            == cfg.glob.DOCUMENT_LINE_TYPE_BODY
        ):
            line_0_lines.append(cfg.glob.text_parser.parse_result_line_0_line[cfg.glob.text_parser.JSON_NAME_LINE_TEXT])

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
            token_attr[JSON_NAME_TOKEN_CLUSTER] = token.cluster

    if cfg.glob.setup.is_spacy_tkn_attr_dep_:
        if token.dep_ != "":
            token_attr[JSON_NAME_TOKEN_DEP_] = token.dep_

    if cfg.glob.setup.is_spacy_tkn_attr_doc:
        if token.doc is not None:
            token_attr[JSON_NAME_TOKEN_DOC] = token.doc.text

    if cfg.glob.setup.is_spacy_tkn_attr_ent_iob_:
        if token.ent_iob_ != "":
            token_attr[JSON_NAME_TOKEN_ENT_IOB_] = token.ent_iob_

    if cfg.glob.setup.is_spacy_tkn_attr_ent_kb_id_:
        # not testable
        if token.ent_kb_id_ != "":
            token_attr[JSON_NAME_TOKEN_ENT_KB_ID_] = token.ent_kb_id_

    if cfg.glob.setup.is_spacy_tkn_attr_ent_type_:
        if token.ent_type_ != "":
            token_attr[JSON_NAME_TOKEN_ENT_TYPE_] = token.ent_type_

    if cfg.glob.setup.is_spacy_tkn_attr_head:
        if token.head is not None:
            token_attr[JSON_NAME_TOKEN_HEAD] = token.head.i

    if cfg.glob.setup.is_spacy_tkn_attr_i:
        token_attr[JSON_NAME_TOKEN_I] = token.i

    if cfg.glob.setup.is_spacy_tkn_attr_idx:
        if token.idx != "":
            token_attr[JSON_NAME_TOKEN_IDX] = token.idx

    if cfg.glob.setup.is_spacy_tkn_attr_is_alpha:
        if token.is_alpha:
            token_attr[JSON_NAME_TOKEN_IS_ALPHA] = token.is_alpha

    if cfg.glob.setup.is_spacy_tkn_attr_is_ascii:
        if token.is_ascii:
            token_attr[JSON_NAME_TOKEN_IS_ASCII] = token.is_ascii

    if cfg.glob.setup.is_spacy_tkn_attr_is_bracket:
        if token.is_bracket:
            token_attr[JSON_NAME_TOKEN_IS_BRACKET] = token.is_bracket

    if cfg.glob.setup.is_spacy_tkn_attr_is_currency:
        if token.is_currency:
            token_attr[JSON_NAME_TOKEN_IS_CURRENCY] = token.is_currency

    if cfg.glob.setup.is_spacy_tkn_attr_is_digit:
        if token.is_digit:
            token_attr[JSON_NAME_TOKEN_IS_DIGIT] = token.is_digit

    if cfg.glob.setup.is_spacy_tkn_attr_is_left_punct:
        if token.is_left_punct:
            token_attr[JSON_NAME_TOKEN_IS_LEFT_PUNCT] = token.is_left_punct

    if cfg.glob.setup.is_spacy_tkn_attr_is_lower:
        if token.is_lower:
            token_attr[JSON_NAME_TOKEN_IS_LOWER] = token.is_lower

    if cfg.glob.setup.is_spacy_tkn_attr_is_oov:
        if token.is_oov:
            token_attr[JSON_NAME_TOKEN_IS_OOV] = token.is_oov

    if cfg.glob.setup.is_spacy_tkn_attr_is_punct:
        if token.is_punct:
            token_attr[JSON_NAME_TOKEN_IS_PUNCT] = token.is_punct

    if cfg.glob.setup.is_spacy_tkn_attr_is_quote:
        if token.is_quote:
            token_attr[JSON_NAME_TOKEN_IS_QUOTE] = token.is_quote

    if cfg.glob.setup.is_spacy_tkn_attr_is_right_punct:
        if token.is_right_punct:
            token_attr[JSON_NAME_TOKEN_IS_RIGHT_PUNCT] = token.is_right_punct

    if cfg.glob.setup.is_spacy_tkn_attr_is_sent_end:
        if token.is_sent_end:
            token_attr[JSON_NAME_TOKEN_IS_SENT_END] = token.is_sent_end

    if cfg.glob.setup.is_spacy_tkn_attr_is_sent_start:
        if token.is_sent_start:
            token_attr[JSON_NAME_TOKEN_IS_SENT_START] = token.is_sent_start

    if cfg.glob.setup.is_spacy_tkn_attr_is_space:
        if token.is_space:
            token_attr[JSON_NAME_TOKEN_IS_SPACE] = token.is_space

    if cfg.glob.setup.is_spacy_tkn_attr_is_stop:
        if token.is_stop:
            token_attr[JSON_NAME_TOKEN_IS_STOP] = token.is_stop

    if cfg.glob.setup.is_spacy_tkn_attr_is_title:
        if token.is_title:
            token_attr[JSON_NAME_TOKEN_IS_TITLE] = token.is_title

    if cfg.glob.setup.is_spacy_tkn_attr_is_upper:
        if token.is_upper:
            token_attr[JSON_NAME_TOKEN_IS_UPPER] = token.is_upper

    if cfg.glob.setup.is_spacy_tkn_attr_lang_:
        if token.lang_ != "":
            token_attr[JSON_NAME_TOKEN_LANG_] = token.lang_

    if cfg.glob.setup.is_spacy_tkn_attr_left_edge:
        if token.left_edge.text is not None:
            token_attr[JSON_NAME_TOKEN_LEFT_EDGE] = token.left_edge.i

    if cfg.glob.setup.is_spacy_tkn_attr_lemma_:
        if token.lemma_ != "":
            token_attr[JSON_NAME_TOKEN_LEMMA_] = token.lemma_

    if cfg.glob.setup.is_spacy_tkn_attr_lex:
        if token.lex is not None:
            token_attr[JSON_NAME_TOKEN_LEX] = token.lex.text

    if cfg.glob.setup.is_spacy_tkn_attr_lex_id:
        if token.lex_id != "":
            token_attr[JSON_NAME_TOKEN_LEX_ID] = token.lex_id

    if cfg.glob.setup.is_spacy_tkn_attr_like_email:
        if token.like_email:
            token_attr[JSON_NAME_TOKEN_LIKE_EMAIL] = token.like_email

    if cfg.glob.setup.is_spacy_tkn_attr_like_num:
        if token.like_num:
            token_attr[JSON_NAME_TOKEN_LIKE_NUM] = token.like_num

    if cfg.glob.setup.is_spacy_tkn_attr_like_url:
        if token.like_url:
            token_attr[JSON_NAME_TOKEN_LIKE_URL] = token.like_url

    if cfg.glob.setup.is_spacy_tkn_attr_lower_:
        if token.lower_ != "":
            token_attr[JSON_NAME_TOKEN_LOWER_] = token.lower_

    if cfg.glob.setup.is_spacy_tkn_attr_morph:
        if token.morph is not None:
            token_attr[JSON_NAME_TOKEN_MORPH] = token.morph.__str__()

    if cfg.glob.setup.is_spacy_tkn_attr_norm_:
        if token.norm_ != "":
            token_attr[JSON_NAME_TOKEN_NORM_] = token.norm_

    if cfg.glob.setup.is_spacy_tkn_attr_orth_:
        if token.orth_ != "":
            token_attr[JSON_NAME_TOKEN_ORTH_] = token.orth_

    if cfg.glob.setup.is_spacy_tkn_attr_pos_:
        if token.pos_ != "":
            token_attr[JSON_NAME_TOKEN_POS_] = token.pos_

    if cfg.glob.setup.is_spacy_tkn_attr_prefix_:
        if token.prefix_ != "":
            token_attr[JSON_NAME_TOKEN_PREFIX_] = token.prefix_

    if cfg.glob.setup.is_spacy_tkn_attr_prob:
        if token.prob != "":
            token_attr[JSON_NAME_TOKEN_PROB] = token.prob

    if cfg.glob.setup.is_spacy_tkn_attr_rank:
        if token.rank != "":
            token_attr[JSON_NAME_TOKEN_RANK] = token.rank

    if cfg.glob.setup.is_spacy_tkn_attr_right_edge:
        if token.right_edge is not None:
            token_attr[JSON_NAME_TOKEN_RIGHT_EDGE] = token.right_edge.i

    if cfg.glob.setup.is_spacy_tkn_attr_sent:
        if token.sent is not None:
            token_attr[JSON_NAME_TOKEN_SENT] = token.sent.text

    if cfg.glob.setup.is_spacy_tkn_attr_sentiment:
        if token.sentiment != "":
            token_attr[JSON_NAME_TOKEN_SENTIMENT] = token.sentiment

    if cfg.glob.setup.is_spacy_tkn_attr_shape_:
        if token.shape_ != "":
            token_attr[JSON_NAME_TOKEN_SHAPE_] = token.shape_

    if cfg.glob.setup.is_spacy_tkn_attr_suffix_:
        if token.suffix_ != "":
            token_attr[JSON_NAME_TOKEN_SUFFIX_] = token.suffix_

    if cfg.glob.setup.is_spacy_tkn_attr_tag_:
        if token.tag_ != "":
            token_attr[JSON_NAME_TOKEN_TAG_] = token.tag_

    if cfg.glob.setup.is_spacy_tkn_attr_tensor:
        try:
            token_attr[JSON_NAME_TOKEN_TENSOR] = token.tensor.__str__()
        except IndexError:
            pass

    if cfg.glob.setup.is_spacy_tkn_attr_text:
        if token.text != "":
            token_attr[JSON_NAME_TOKEN_TEXT] = token.text

    if cfg.glob.setup.is_spacy_tkn_attr_text_with_ws:
        if token.text_with_ws != "":
            token_attr[JSON_NAME_TOKEN_TEXT_WITH_WS] = token.text_with_ws

    if cfg.glob.setup.is_spacy_tkn_attr_vocab:
        if token.vocab is not None:
            token_attr[JSON_NAME_TOKEN_RANK] = token.vocab.__str__()

    if cfg.glob.setup.is_spacy_tkn_attr_whitespace_:
        if token.whitespace_ != "":
            token_attr[JSON_NAME_TOKEN_WHITESPACE_] = token.whitespace_

    return token_attr


# -----------------------------------------------------------------------------
# Create document tokens (step: tkn).
# -----------------------------------------------------------------------------
def tokenize() -> None:
    """Create document tokens (step: tkn).

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    model_data: spacy.Language
    spacy_model_current: str | None = None

    cfg.glob.text_parser = nlp.cls_text_parser.TextParser()

    with cfg.glob.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(conn=conn, action_code=db.cls_run.Run.ACTION_CODE_TOKENIZE)

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

            cfg.glob.document = db.cls_document.Document.from_id(id_document=cfg.glob.action_curr.action_id_document)

            spacy_model = cfg.glob.languages_spacy[cfg.glob.document.document_id_language]

            if spacy_model != spacy_model_current:
                model_data = spacy.load(spacy_model)
                spacy_model_current = spacy_model

            tokenize_file(model_data)

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the tokens of a document page by page (step: tkn).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def tokenize_file(model_data: spacy.Language) -> None:
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

    try:
        cfg.glob.text_parser = nlp.cls_text_parser.TextParser.from_files(full_name_line=full_name_curr)

        cfg.glob.token_3_pages = []

        for cfg.glob.text_parser.parse_result_line_2_page in cfg.glob.text_parser.parse_result_line_4_document[
            cfg.glob.text_parser.JSON_NAME_PAGES
        ]:
            # ------------------------------------------------------------------
            # Processing a single page
            # ------------------------------------------------------------------
            page_no = cfg.glob.text_parser.parse_result_line_2_page[cfg.glob.text_parser.JSON_NAME_PAGE_NO]

            text = get_text_from_line_2_page()

            cfg.glob.token_1_tokens = []

            for token in model_data(text):
                cfg.glob.token_1_tokens.append(get_token_attributes(token))

            cfg.glob.token_2_page = {
                cfg.glob.text_parser.JSON_NAME_PAGE_NO: page_no,
                JSON_NAME_NO_TOKENS_IN_PAGE: len(cfg.glob.token_1_tokens),
                JSON_NAME_TOKENS: cfg.glob.token_1_tokens,
            }

            if cfg.glob.setup.is_tokenize_2_database:
                db.dml.insert_dbt_row(
                    cfg.glob.DBT_TOKEN,
                    {
                        cfg.glob.DBC_ID_DOCUMENT: cfg.glob.document.document_id,
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
                        cfg.glob.text_parser.JSON_NAME_DOCUMENT_ID: cfg.glob.document.document_id,
                        cfg.glob.text_parser.JSON_NAME_DOCUMENT_FILE_NAME: cfg.glob.document.document_file_name,
                        cfg.glob.text_parser.JSON_NAME_NO_PAGES_IN_DOC: cfg.glob.text_parser.parse_result_line_4_document[
                            cfg.glob.text_parser.JSON_NAME_NO_PAGES_IN_DOC
                        ],
                        cfg.glob.text_parser.JSON_NAME_PAGES: cfg.glob.token_3_pages,
                    },
                    file_handle,
                )

        utils.delete_auxiliary_file(full_name_curr)

        cfg.glob.run.run_total_processed_ok += 1
    except FileNotFoundError as err:
        cfg.glob.action_curr.finalise_error(
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_TOKENIZE,
            error_msg=cfg.glob.ERROR_71_901.replace("{full_name_curr}", full_name_curr)
            .replace("{error_type}", str(type(err)))
            .replace("{error}", str(err)),
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
