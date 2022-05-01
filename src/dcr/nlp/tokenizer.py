"""Module nlp.tokenizer: Store the document tokens page by page in the
database."""

import time
import typing

import cfg.glob
import comm.utils
import db.dml
import spacy
import sqlalchemy


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
        text_lines.append(page_line[cfg.glob.JSON_NAME_LINE_TEXT])

    return "\n".join(text_lines)


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

    comm.utils.reset_statistics_total()

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = db.dml.select_document(conn, dbt_document, cfg.glob.DOCUMENT_STEP_TOKENIZE)

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            comm.utils.start_document_processing(
                document=row,
            )

            spacy_model = cfg.glob.languages_spacy[cfg.glob.document_language_id]

            if spacy_model != spacy_model_current:
                nlp = spacy.load(spacy_model)
                spacy_model_current = spacy_model

            tokenize_document(nlp, dbt_content_tetml)

            # Document successfully converted to pdf format
            duration_ns = comm.utils.finalize_file_processing()

            if cfg.glob.setup.is_verbose:
                comm.utils.progress_msg(
                    f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                    f"Document: {cfg.glob.document_id:6d} "
                    f"[base: {db.dml.select_document_file_name_id(cfg.glob.document_id_base)}]"
                )

        conn.close()

    comm.utils.show_statistics_total()

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

            page_no = row[0]
            text = get_text_from_page_lines(row[1]) if cfg.glob.setup.is_tetml_line else row[1]

            for token in nlp(text):
                page_tokens.append(
                    {
                        cfg.glob.JSON_NAME_TOKEN_TEXT: token.text,
                        cfg.glob.JSON_NAME_TOKEN_INDEX: token.i,
                        cfg.glob.JSON_NAME_TOKEN_LEMMA: token.lemma_,
                        cfg.glob.JSON_NAME_TOKEN_POS: token.pos_,
                        cfg.glob.JSON_NAME_TOKEN_TAG: token.tag_,
                        cfg.glob.JSON_NAME_TOKEN_DEP: token.dep_,
                        cfg.glob.JSON_NAME_TOKEN_SHAPE: token.shape_,
                        cfg.glob.JSON_NAME_TOKEN_IS_ALPHA: token.is_alpha,
                        cfg.glob.JSON_NAME_TOKEN_IS_STOP: token.is_stop,
                    }
                )

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
