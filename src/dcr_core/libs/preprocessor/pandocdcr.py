"""Module libs.preprocessor.pandocdcr: Convert non-pdf documents to pdf
files."""
import os
import time

import libs.cfg
import libs.db.cfg
import libs.db.orm.dml
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

    libs.utils.reset_statistics_total()

    with libs.db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, libs.db.cfg.DOCUMENT_STEP_PANDOC)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            convert_non_pdf_2_pdf_file()

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert a non-pdf document to a pdf file (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf_file() -> None:
    """Convert a non-pdf document to a pdf file."""
    source_file_name, target_file_name = libs.utils.prepare_file_names()

    if os.path.exists(target_file_name):
        libs.utils.report_document_error(
            error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error=libs.db.cfg.ERROR_31_903.replace("{file_name}", target_file_name),
        )
        return

    # Convert the document
    # not testable
    # try:
    # output = pypandoc.convert_file(
    pypandoc.convert_file(
        source_file_name,
        libs.db.cfg.DOCUMENT_FILE_TYPE_PDF,
        extra_args=(
            [
                f"--pdf-engine={libs.cfg.PANDOC_PDF_ENGINE_XELATEX}",
                "-V",
                f"lang:{libs.cfg.languages_pandoc[libs.cfg.document_language_id]}",
            ]
        ),
        outputfile=target_file_name,
    )

    # not testable
    # if output != "":
    #     libs.utils.report_document_error(
    #         error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PANDOC,
    #         error=libs.db.cfg.ERROR_31_901.replace("{source_file}", source_file_name)
    #         .replace("{target_file}", target_file_name)
    #         .replace("{output}", output),
    #     )
    # else:
    libs.utils.prepare_document_4_next_step(
        next_file_type=libs.db.cfg.DOCUMENT_FILE_TYPE_PDF,
        next_step=libs.db.cfg.DOCUMENT_STEP_PDFLIB,
    )

    libs.cfg.document_child_file_name = (
        libs.cfg.document_stem_name + "." + libs.db.cfg.DOCUMENT_FILE_TYPE_PDF
    )
    libs.cfg.document_child_stem_name = libs.cfg.document_stem_name

    libs.utils.initialise_document_child()

    libs.utils.delete_auxiliary_file(source_file_name)

    # Document successfully converted to pdf format
    libs.utils.finalize_file_processing()

    libs.db.orm.dml.insert_journal_statistics(libs.cfg.document_id)
    # not testable
    # except RuntimeError as err:
    #     libs.utils.report_document_error(
    #         error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE,
    #         error=libs.db.cfg.ERROR_31_902.replace("{file_name}", source_file_name).replace(
    #             "{error_msg}", str(str(err).encode("utf-8"))
    #         ),
    #     )
