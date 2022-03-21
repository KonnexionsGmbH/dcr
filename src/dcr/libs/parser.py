"""Module libs.parser: Store the document structure from the parser result."""
import os

import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.utils


# -----------------------------------------------------------------------------
# Parse a document (step: s_f_p).
# -----------------------------------------------------------------------------
def parse_document() -> None:
    """Parse a document.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    file_name = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    # Text and metadata from Document successfully extracted to xml format
    journal_action = libs.db.cfg.JOURNAL_ACTION_61_002.replace("{file_name}", file_name)

    libs.utils.finalize_file_processing(journal_action)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Parse the TETML files (step: s_f_p).
# -----------------------------------------------------------------------------
def parse_tetml_filrs() -> None:
    """Parse the TETML files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = libs.utils.select_document_prepare()

    libs.utils.reset_statistics()

    with libs.db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, libs.db.cfg.DOCUMENT_NEXT_STEP_PARSER)

        for row in rows:
            libs.utils.start_document_processing(row, libs.db.cfg.JOURNAL_ACTION_61_001)
            parse_document()

        conn.close()

    libs.utils.show_statistics()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
