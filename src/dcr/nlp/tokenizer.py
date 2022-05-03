"""Module nlp.tokenizer: Store the document tokens page by page in the
database."""

import time
import typing

import cfg.glob
import db.dml
import spacy
import spacy.tokens
import sqlalchemy
import utils


# pylint: disable=R0912
# pylint: disable=R0915
# -----------------------------------------------------------------------------
# Extract the text from the page lines.
# -----------------------------------------------------------------------------
def get_text_from_page_lines(page_data: typing.Dict[str, str | typing.List[typing.Dict[str, int | str]]]) -> str:
    """Extract the text from the page data.

    Args:
        page_data (Dict[str, str | List[Dict[str, int | str]]]): Page data.

    Returns:
        str: Reconstructed text.
    """
    text_lines = []

    for page_line in page_data[cfg.glob.JSON_NAME_PAGE_LINES]:
        if page_line[cfg.glob.JSON_NAME_LINE_TYPE] == cfg.glob.DOCUMENT_LINE_TYPE_BODY:
            text_lines.append(page_line[cfg.glob.JSON_NAME_LINE_TEXT])

    return "\n".join(text_lines)


# -----------------------------------------------------------------------------
# Determine the requested token attributes.
# -----------------------------------------------------------------------------
def get_token_attributes(token: spacy.tokens.Token) -> typing.Dict[str, bool | int | str]:  # noqa: C901
    """Determine the requested token attributes.

    Args:
        token (spacy.tokens.Token): SpaCy token.

    Returns:
        typing.Dict[str, bool | int | str]: Requested token attributes.
    """
    token_attr = {}

    if cfg.glob.setup.is_spacy_tkn_attr_dep_:
        if token.dep_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_DEP_] = token.dep_

    if cfg.glob.setup.is_spacy_tkn_attr_ent_iob_:
        if token.ent_iob_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_ENT_IOB_] = token.ent_iob_

    if cfg.glob.setup.is_spacy_tkn_attr_ent_kb_id_:
        if token.ent_kb_id_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_ENT_KB_ID_] = token.ent_kb_id_

    if cfg.glob.setup.is_spacy_tkn_attr_ent_type_:
        if token.ent_type_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_ENT_TYPE_] = token.ent_type_

    if cfg.glob.setup.is_spacy_tkn_attr_i:
        token_attr[cfg.glob.JSON_NAME_TOKEN_I] = token.i

    if cfg.glob.setup.is_spacy_tkn_attr_is_alpha:
        if token.is_alpha:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_ALPHA] = token.is_alpha

    if cfg.glob.setup.is_spacy_tkn_attr_is_currency:
        if token.is_currency:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_CURRENCY] = token.is_currency

    if cfg.glob.setup.is_spacy_tkn_attr_is_digit:
        if token.is_digit:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_DIGIT] = token.is_digit

    if cfg.glob.setup.is_spacy_tkn_attr_is_oov:
        if token.is_oov:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_OOV] = token.is_oov

    if cfg.glob.setup.is_spacy_tkn_attr_is_punct:
        if token.is_punct:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_PUNCT] = token.is_punct

    if cfg.glob.setup.is_spacy_tkn_attr_is_sent_end:
        if token.is_sent_end:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_SENT_END] = token.is_sent_end

    if cfg.glob.setup.is_spacy_tkn_attr_is_sent_start:
        if token.is_sent_start:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_SENT_START] = token.is_sent_start

    if cfg.glob.setup.is_spacy_tkn_attr_is_stop:
        if token.is_stop:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_STOP] = token.is_stop

    if cfg.glob.setup.is_spacy_tkn_attr_is_title:
        if token.is_title:
            token_attr[cfg.glob.JSON_NAME_TOKEN_IS_TITLE] = token.is_title

    if cfg.glob.setup.is_spacy_tkn_attr_lang_:
        if token.lang_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_LANG_] = token.lang_

    if cfg.glob.setup.is_spacy_tkn_attr_left_edge:
        if token.left_edge != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_LEFT_EDGE] = token.left_edge

    if cfg.glob.setup.is_spacy_tkn_attr_lemma_:
        if token.lemma_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_LEMMA_] = token.lemma_

    if cfg.glob.setup.is_spacy_tkn_attr_like_email:
        if token.like_email:
            token_attr[cfg.glob.JSON_NAME_TOKEN_LIKE_EMAIL] = token.like_email

    if cfg.glob.setup.is_spacy_tkn_attr_like_num:
        if token.like_num:
            token_attr[cfg.glob.JSON_NAME_TOKEN_LIKE_NUM] = token.like_num

    if cfg.glob.setup.is_spacy_tkn_attr_like_url:
        if token.like_url:
            token_attr[cfg.glob.JSON_NAME_TOKEN_LIKE_URL] = token.like_url

    if cfg.glob.setup.is_spacy_tkn_attr_norm_:
        if token.norm_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_NORM_] = token.norm_

    if cfg.glob.setup.is_spacy_tkn_attr_right_edge:
        if token.right_edge != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_RIGHT_EDGE] = token.right_edge

    if cfg.glob.setup.is_spacy_tkn_attr_shape_:
        if token.shape_ != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_SHAPE_] = token.shape_

    if cfg.glob.setup.is_spacy_tkn_attr_text:
        if token.text != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_TEXT] = token.text

    if cfg.glob.setup.is_spacy_tkn_attr_text_with_ws:
        if token.text_with_ws != "":
            token_attr[cfg.glob.JSON_NAME_TOKEN_TEXT_WITH_WS] = token.text_with_ws

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

    if cfg.glob.setup.is_tetml_line:
        dbt_content_tetml: sqlalchemy.Table = db.dml.dml_prepare(cfg.glob.DBT_CONTENT_TETML_LINE)
    else:
        dbt_content_tetml: sqlalchemy.Table = db.dml.dml_prepare(cfg.glob.DBT_CONTENT_TETML_PAGE)

    dbt_document = db.dml.dml_prepare(cfg.glob.DBT_DOCUMENT)

    nlp: spacy.Language
    spacy_model_current: str | None = None

    utils.reset_statistics_total()

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = db.dml.select_document(conn, dbt_document, cfg.glob.DOCUMENT_STEP_TOKENIZE)

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            utils.start_document_processing(
                document=row,
            )

            spacy_model = cfg.glob.languages_spacy[cfg.glob.document_language_id]

            if spacy_model != spacy_model_current:
                nlp = spacy.load(spacy_model)
                spacy_model_current = spacy_model

            tokenize_document(nlp, dbt_content_tetml)

            # Document successfully converted to pdf format
            duration_ns = utils.finalize_file_processing()

            if cfg.glob.setup.is_verbose:
                utils.progress_msg(
                    f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                    f"Document: {cfg.glob.document_id:6d} "
                    f"[base: {db.dml.select_document_file_name_id(cfg.glob.document_id_base)}]"
                )

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the tokens of a document page by page (step: tkn).
# -----------------------------------------------------------------------------
def tokenize_document(nlp: spacy.Language, dbt_content: sqlalchemy.Table) -> None:
    """Create the tokens of a document page by page.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = db.dml.select_content_tetml(conn, dbt_content, cfg.glob.document_id_base)
        for row in rows:
            # ------------------------------------------------------------------
            # Processing a single page
            # ------------------------------------------------------------------
            page_tokens: typing.List[typing.Dict[str, bool | str]] = []

            page_no = row[1]
            text = get_text_from_page_lines(row[2]) if cfg.glob.setup.is_tetml_line else row[2]

            for token in nlp(text):
                page_tokens.append(get_token_attributes(token))

            db.dml.insert_dbt_row(
                cfg.glob.DBT_CONTENT_TOKEN,
                {
                    cfg.glob.DBC_DOCUMENT_ID: cfg.glob.document_id_base,
                    cfg.glob.DBC_PAGE_NO: page_no,
                    cfg.glob.DBC_PAGE_DATA: page_tokens,
                },
            )

        conn.close()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
