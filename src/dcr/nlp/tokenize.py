"""Module nlp.tokenizer: Store the document tokens page by page in the
database."""
import time

import db.cfg
import db.orm.dml
import libs.cfg
import libs.utils


# -----------------------------------------------------------------------------
# Store the document tokens of one page in the database.
# -----------------------------------------------------------------------------
def insert_content_token(page_no: int) -> None:
    """Store the document tokens of one page in the database."""
    db.orm.dml.insert_dbt_row(
        db.cfg.DBT_CONTENT_TOKEN,
        {
            db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id_base,
            db.cfg.DBC_PAGE_NO: page_no,
            db.cfg.DBC_SENTENCE: libs.cfg.parse_result_sentence,
        },
    )


# -----------------------------------------------------------------------------
# Create document tokens (step: tkn).
# -----------------------------------------------------------------------------
def tokenize() -> None:
    """Create document tokens (step: tkn).

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = libs.utils.select_document_prepare()

    libs.utils.reset_statistics_total()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.orm.dml.select_document(conn, dbt, db.cfg.DOCUMENT_STEP_TOKENIZE)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            tokenize_document()

            # Document successfully converted to pdf format
            libs.utils.finalize_file_processing()

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the tokens of a document page by page (step: tkn).
# -----------------------------------------------------------------------------
def tokenize_document() -> None:
    """Create the tokens of a document page by page.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
