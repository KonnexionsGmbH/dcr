"""Module nlp.tokenizer: Store the document tokens page by page in the
database."""

import time
import typing

import db.cfg
import db.dml
import libs.cfg
import libs.utils
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

    for page_line in page_data[db.cfg.JSON_NAME_PAGE_LINES]:
        text_lines.append(page_line[db.cfg.JSON_NAME_LINE_TEXT])

    return "\n".join(text_lines)


# -----------------------------------------------------------------------------
# Create document tokens (step: tkn).
# -----------------------------------------------------------------------------
def tokenize() -> None:
    """Create document tokens (step: tkn).

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.config.is_tetml_line:
        dbt_content_tetml: sqlalchemy.Table = db.dml.dml_prepare(db.cfg.DBT_CONTENT_TETML_LINE)
    else:
        dbt_content_tetml: sqlalchemy.Table = db.dml.dml_prepare(db.cfg.DBT_CONTENT_TETML_PAGE)

    dbt_document = db.dml.dml_prepare(db.cfg.DBT_DOCUMENT)

    nlp: spacy.Language
    spacy_model_current: str | None = None

    libs.utils.reset_statistics_total()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.dml.select_document(conn, dbt_document, db.cfg.DOCUMENT_STEP_TOKENIZE)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            spacy_model = libs.cfg.languages_spacy[libs.cfg.document_language_id]

            if spacy_model != spacy_model_current:
                nlp = spacy.load(spacy_model)
                spacy_model_current = spacy_model

            tokenize_document(nlp, dbt_content_tetml)

            # Document successfully converted to pdf format
            duration_ns = libs.utils.finalize_file_processing()

            if libs.cfg.config.is_verbose:
                libs.utils.progress_msg(
                    f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                    f"Document: {libs.cfg.document_id:6d} "
                    f"[base: {db.dml.select_document_file_name_id(libs.cfg.document_id_base)}]"
                )

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the tokens of a document page by page (step: tkn).
# -----------------------------------------------------------------------------
def tokenize_document(nlp: spacy.Language, dbt_content: sqlalchemy.Table) -> None:
    """Create the tokens of a document page by page.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.dml.select_content_tetml(conn, dbt_content, libs.cfg.document_id_base)
        for row in rows:
            # ------------------------------------------------------------------
            # Processing a single page
            # ------------------------------------------------------------------
            page_tokens: typing.List[typing.Dict[str, bool | str]] = []

            page_no = row[0]
            text = get_text_from_page_lines(row[1]) if libs.cfg.config.is_tetml_line else row[1]

            for token in nlp(text):
                page_tokens.append(
                    {
                        db.cfg.JSON_NAME_TOKEN_TEXT: token.text,
                        db.cfg.JSON_NAME_TOKEN_INDEX: token.i,
                        db.cfg.JSON_NAME_TOKEN_LEMMA: token.lemma_,
                        db.cfg.JSON_NAME_TOKEN_POS: token.pos_,
                        db.cfg.JSON_NAME_TOKEN_TAG: token.tag_,
                        db.cfg.JSON_NAME_TOKEN_DEP: token.dep_,
                        db.cfg.JSON_NAME_TOKEN_SHAPE: token.shape_,
                        db.cfg.JSON_NAME_TOKEN_IS_ALPHA: token.is_alpha,
                        db.cfg.JSON_NAME_TOKEN_IS_STOP: token.is_stop,
                    }
                )

            db.dml.insert_dbt_row(
                db.cfg.DBT_CONTENT_TOKEN,
                {
                    db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id_base,
                    db.cfg.DBC_PAGE_NO: page_no,
                    db.cfg.DBC_PAGE_DATA: page_tokens,
                },
            )

        conn.close()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
