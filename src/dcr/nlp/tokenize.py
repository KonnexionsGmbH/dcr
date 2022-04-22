"""Module nlp.tokenizer: Store the document tokens page by page in the
database."""
import time
from typing import Dict
from typing import List

import db.cfg
import db.orm.dml
import libs.cfg
import libs.utils
import spacy
from spacy import Language
from sqlalchemy import Table


# -----------------------------------------------------------------------------
# Create document tokens (step: tkn).
# -----------------------------------------------------------------------------
def tokenize() -> None:
    """Create document tokens (step: tkn).

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt_content_tetml_page: Table = db.orm.dml.dml_prepare(db.cfg.DBT_CONTENT_TETML_PAGE)
    dbt_document = db.orm.dml.dml_prepare(db.cfg.DBT_DOCUMENT)

    nlp: Language
    spacy_model_current: str | None = None

    libs.utils.reset_statistics_total()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.orm.dml.select_document(conn, dbt_document, db.cfg.DOCUMENT_STEP_TOKENIZE)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            spacy_model = libs.cfg.languages_spacy[libs.cfg.document_language_id]

            if spacy_model != spacy_model_current:
                nlp = spacy.load(spacy_model)
                spacy_model_current = spacy_model

            tokenize_document(nlp, dbt_content_tetml_page)

            # Document successfully converted to pdf format
            duration_ns = libs.utils.finalize_file_processing()

            if libs.cfg.is_verbose:
                libs.utils.progress_msg(
                    f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                    f"Document: {libs.cfg.document_id:6d} "
                    f"[base: {db.orm.dml.select_document_file_name_id(libs.cfg.document_id_base)}]"
                )

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the tokens of a document page by page (step: tkn).
# -----------------------------------------------------------------------------
def tokenize_document(nlp: Language, dbt_content: Table) -> None:
    """Create the tokens of a document page by page.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.orm.dml.select_content_tetml_page(conn, dbt_content, libs.cfg.document_id_base)

        for row in rows:
            tokens_json: List[Dict[str, bool | str]] = []

            page_no = row[0]
            for token in nlp(row[1]):
                tokens_json.append(
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

            db.orm.dml.insert_dbt_row(
                db.cfg.DBT_CONTENT_TOKEN,
                {
                    db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id_base,
                    db.cfg.DBC_PAGE_NO: page_no,
                    db.cfg.DBC_TOKEN: tokens_json,
                },
            )

        conn.close()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
