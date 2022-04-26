"""Module pp.pandoc_dcr: Convert non-pdf documents to pdf files."""
import os
import time

import db.cfg
import db.orm.dml
import libs.cfg
import libs.utils
import pypandoc

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
PANDOC_PDF_ENGINE_LULATEX: str = "lulatex"
PANDOC_PDF_ENGINE_XELATEX: str = "xelatex"


# -----------------------------------------------------------------------------
# Convert non-pdf documents to pdf files (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf() -> None:
    """Convert non-pdf documents to pdf files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = db.orm.dml.dml_prepare(db.cfg.DBT_DOCUMENT)

    libs.utils.reset_statistics_total()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.orm.dml.select_document(conn, dbt, db.cfg.DOCUMENT_STEP_PANDOC)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            convert_non_pdf_2_pdf_file()

            # Document successfully converted to pdf format
            duration_ns = libs.utils.finalize_file_processing()

            if libs.cfg.config.is_verbose:
                libs.utils.progress_msg(
                    f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                    f"Document: {libs.cfg.document_id:6d} "
                    f"[{db.orm.dml.select_document_file_name_id(libs.cfg.document_id)}]"
                )

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert a non-pdf document to a pdf file (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf_file() -> None:
    """Convert a non-pdf document to a pdf file."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    source_file_name, target_file_name = libs.utils.prepare_file_names()

    if os.path.exists(target_file_name):
        db.orm.dml.update_document_error(
            document_id=libs.cfg.document_id,
            error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=db.cfg.ERROR_31_903.replace("{file_name}", target_file_name),
        )
        return

    # Convert the document
    extra_args = [
        f"--pdf-engine={PANDOC_PDF_ENGINE_XELATEX}",
        "-V",
        f"lang:{libs.cfg.languages_pandoc[libs.cfg.document_language_id]}",
    ]

    pypandoc.convert_file(
        source_file_name,
        db.cfg.DOCUMENT_FILE_TYPE_PDF,
        extra_args=extra_args,
        outputfile=target_file_name,
    )

    libs.utils.prepare_document_4_next_step(
        next_file_type=db.cfg.DOCUMENT_FILE_TYPE_PDF,
        next_step=db.cfg.DOCUMENT_STEP_PDFLIB,
    )

    libs.cfg.document_child_file_name = (
        libs.cfg.document_stem_name + "." + db.cfg.DOCUMENT_FILE_TYPE_PDF
    )
    libs.cfg.document_child_stem_name = libs.cfg.document_stem_name

    db.orm.dml.insert_document_child()

    libs.utils.delete_auxiliary_file(source_file_name)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
