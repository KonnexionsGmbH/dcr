"""Module pp.pandoc_dcr: Convert non-pdf documents to pdf files."""
import os
import time

import cfg.glob
import db.dml
import pypandoc
import utils

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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    dbt = db.dml.dml_prepare(cfg.glob.DBT_DOCUMENT)

    utils.reset_statistics_total()

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = db.dml.select_document(conn, dbt, db.cls_run.Run.ACTION_CODE_PANDOC)

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            utils.start_document_processing(
                document=row,
            )

            convert_non_pdf_2_pdf_file()

            # Document successfully converted to pdf format
            duration_ns = utils.finalize_file_processing()

            if cfg.glob.setup.is_verbose:
                utils.progress_msg(
                    f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                    f"Document: {cfg.glob.base.base_id:6d} "
                    f"[{db.dml.select_document_file_name_id(cfg.glob.base.base_id)}]"
                )

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert a non-pdf document to a pdf file (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf_file() -> None:
    """Convert a non-pdf document to a pdf file."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    source_file_name, target_file_name = utils.prepare_file_names(cfg.glob.DOCUMENT_FILE_TYPE_PDF)

    if os.path.exists(target_file_name):
        db.dml.update_document_error(
            document_id=cfg.glob.base.base_id,
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=cfg.glob.ERROR_31_903.replace("{file_name}", target_file_name),
        )
        return

    # Convert the document
    extra_args = [
        f"--pdf-engine={PANDOC_PDF_ENGINE_XELATEX}",
        "-V",
        f"lang:{cfg.glob.languages_pandoc[cfg.glob.base.base_id_language]}",
    ]

    try:
        pypandoc.convert_file(
            source_file_name,
            cfg.glob.DOCUMENT_FILE_TYPE_PDF,
            extra_args=extra_args,
            outputfile=target_file_name,
        )

        utils.prepare_document_4_next_step(
            next_file_type=cfg.glob.DOCUMENT_FILE_TYPE_PDF,
            next_step=db.cls_run.Run.ACTION_CODE_PDFLIB,
        )

        cfg.glob.document_child_file_name = cfg.glob.document_stem_name + "." + cfg.glob.DOCUMENT_FILE_TYPE_PDF
        cfg.glob.document_child_stem_name = cfg.glob.document_stem_name

        db.dml.insert_document_child()

        utils.delete_auxiliary_file(source_file_name)
    except RuntimeError as err:
        db.dml.update_document_error(
            document_id=cfg.glob.base.base_id,
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE,
            error_msg=cfg.glob.ERROR_31_902.replace("{file_name}", source_file_name).replace(
                "{error_msg}", str(str(err).encode("utf-8"))
            ),
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
