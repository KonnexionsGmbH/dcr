"""Module pp.pandoc_dcr: Convert non-pdf documents to pdf documents."""
import os
import time

import cfg.glob
import db.cls_action
import db.cls_document
import db.cls_language
import db.cls_run
import utils

import dcr_core.core_glob
import dcr_core.core_utils
import dcr_core.processing

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_31_903 = "31.903 Issue (n_2_p): The target file '{full_name}' already exists."


# -----------------------------------------------------------------------------
# Convert non-pdf documents to pdf documents (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf() -> None:
    """Convert non-pdf documents to pdf documents.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    with cfg.glob.db_core.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(conn=conn, action_code=db.cls_run.Run.ACTION_CODE_PANDOC)

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_row(row)

            if cfg.glob.action_curr.action_status == db.cls_document.Document.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                cfg.glob.run.total_status_ready += 1

            cfg.glob.document = db.cls_document.Document.from_id(id_document=cfg.glob.action_curr.action_id_document)

            convert_non_pdf_2_pdf_file()

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert a non-pdf document to a pdf document (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf_file() -> None:
    """Convert a non-pdf document to a pdf document."""
    full_name_curr = cfg.glob.action_curr.get_full_name()

    file_name_next = cfg.glob.action_curr.get_stem_name() + "." + dcr_core.core_glob.FILE_TYPE_PDF
    full_name_next = dcr_core.core_utils.get_full_name(
        cfg.glob.action_curr.action_directory_name,
        file_name_next,
    )

    if os.path.exists(full_name_next):
        cfg.glob.action_curr.finalise_error(
            error_code=db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=ERROR_31_903.replace("{full_name}", full_name_next),
        )

        return

    (error_code, error_msg) = dcr_core.processing.pandoc_process(
        full_name_in=full_name_curr,
        full_name_out=full_name_next,
        language_pandoc=db.cls_language.Language.LANGUAGES_PANDOC[cfg.glob.document.document_id_language],
    )
    if (error_code, error_msg) != dcr_core.core_glob.RETURN_OK:
        cfg.glob.action_curr.finalise_error(error_code, error_msg)
        return

    cfg.glob.action_next = db.cls_action.Action(
        action_code=db.cls_run.Run.ACTION_CODE_PDFLIB,
        id_run_last=cfg.glob.run.run_id,
        directory_name=cfg.glob.action_curr.action_directory_name,
        directory_type=cfg.glob.action_curr.action_directory_type,
        file_name=file_name_next,
        file_size_bytes=os.path.getsize(full_name_next),
        id_document=cfg.glob.action_curr.action_id_document,
        id_parent=cfg.glob.action_curr.action_id,
        no_pdf_pages=utils.get_pdf_pages_no(full_name_next),
    )

    utils.delete_auxiliary_file(full_name_curr)

    cfg.glob.action_curr.finalise()

    cfg.glob.run.run_total_processed_ok += 1
