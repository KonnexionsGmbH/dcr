"""Module libs.pandoc: Convert non-pdf documents to pdf files."""
import inspect
import os

import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.utils
import pypandoc


# -----------------------------------------------------------------------------
# Convert non-pdf documents to pdf files (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf() -> None:
    """Convert non-pdf documents to pdf files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = libs.utils.select_document_prepare()

    libs.utils.reset_statistics()

    with libs.db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, libs.db.cfg.DOCUMENT_NEXT_STEP_PANDOC)

        for row in rows:
            libs.utils.start_document_processing(row, libs.db.cfg.JOURNAL_ACTION_31_001)
            convert_non_pdf_2_pdf_file()

        conn.close()

    libs.utils.show_statistics()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert non-pdf documents to pdf files (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf_file() -> None:
    """Convert scanned image pdf documents to image files."""
    source_file, target_file = libs.utils.prepare_file_names()

    if os.path.exists(target_file):
        libs.utils.duplicate_file_error(target_file)
        return

    # Convert the document
    output = pypandoc.convert_file(
        source_file, libs.db.cfg.DOCUMENT_FILE_TYPE_PDF, outputfile=target_file
    )

    # not testable
    if output != "":
        libs.cfg.total_erroneous += 1

        libs.db.orm.update_document_status(
            {
                libs.db.cfg.DBC_ERROR_CODE: libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PANDOC,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
            },
            libs.db.orm.insert_journal(
                __name__,
                inspect.stack()[0][3],
                libs.cfg.document_id,
                libs.db.cfg.JOURNAL_ACTION_31_901.replace("{source_file}", source_file)
                .replace("{target_file}", target_file)
                .replace("{output}", output),
            ),
        )
    else:
        libs.utils.prepare_document_4_pdflib()

        libs.cfg.document_child_file_name = (
            libs.cfg.document_stem_name + "." + libs.db.cfg.DOCUMENT_FILE_TYPE_PDF
        )
        libs.cfg.document_child_stem_name = libs.cfg.document_stem_name

        journal_action: str = libs.db.cfg.JOURNAL_ACTION_31_003.replace(
            "{file_name}", libs.cfg.document_child_file_name
        )

        libs.utils.initialise_document_child(journal_action)

        # Document successfully converted to pdf format
        journal_action = libs.db.cfg.JOURNAL_ACTION_31_002.replace(
            "{source_file}", source_file
        ).replace("{target_file}", target_file)

        libs.utils.finalize_file_conversion(journal_action)
