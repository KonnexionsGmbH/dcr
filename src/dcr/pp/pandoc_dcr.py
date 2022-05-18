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

    with cfg.glob.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(
            conn=conn, action_code=db.cls_run.Run.ACTION_CODE_PANDOC
        )

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_row(row)

            if cfg.glob.action_curr.action_status == cfg.glob.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                cfg.glob.run.total_status_ready += 1

            cfg.glob.base = db.cls_base.Base.from_id(id_base=cfg.glob.action_curr.action_id_base)

            convert_non_pdf_2_pdf_file()

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert a non-pdf document to a pdf file (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf_file() -> None:
    """Convert a non-pdf document to a pdf file."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name_curr = cfg.glob.action_curr.get_full_name()

    file_name_next = cfg.glob.action_curr.get_stem_name() + "." + cfg.glob.DOCUMENT_FILE_TYPE_PDF
    full_name_next = utils.get_full_name(
        cfg.glob.action_curr.action_directory_name,
        file_name_next,
    )

    if os.path.exists(full_name_next):
        cfg.glob.action_curr.finalise_error(
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=cfg.glob.ERROR_31_903.replace("{full_name}", full_name_next),
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
            full_name_curr,
            cfg.glob.DOCUMENT_FILE_TYPE_PDF,
            extra_args=extra_args,
            outputfile=full_name_next,
        )

        cfg.glob.action_next = db.cls_action.Action(
            action_code=db.cls_run.Run.ACTION_CODE_PDFLIB,
            id_run_last=cfg.glob.run.run_id,
            directory_name=cfg.glob.action_curr.action_directory_name,
            directory_type=cfg.glob.action_curr.action_directory_type,
            file_name=file_name_next,
            file_size_bytes=os.path.getsize(full_name_next),
            id_base=cfg.glob.action_curr.action_id_base,
            id_parent=cfg.glob.action_curr.action_id,
            no_pdf_pages=utils.get_pdf_pages_no(full_name_next),
        )

        utils.delete_auxiliary_file(full_name_curr)

        cfg.glob.action_curr.finalise()

        cfg.glob.run.run_total_processed_ok += 1
    except RuntimeError as err:
        cfg.glob.action_curr.finalise_error(
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE,
            error_msg=cfg.glob.ERROR_31_902.replace("{full_name}", full_name_curr).replace(
                "{error_msg}", str(str(err).encode("utf-8"))
            ),
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
