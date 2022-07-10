"""Module pp.pandoc_dcr: Convert non-pdf documents to pdf documents."""
import os
import time

import cfg.glob
import db.cls_action
import db.cls_document
import db.cls_language
import db.cls_run
import pypandoc
import utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_31_902 = (
    "31.902 Issue (n_2_p): The file '{full_name}' cannot be converted to an "
    + "'pdf' document - "
    + "error type: '{error_type}' - error: '{error_msg}'."
)
ERROR_31_903 = "31.903 Issue (n_2_p): The target file '{full_name}' already exists."

PANDOC_PDF_ENGINE_LULATEX = "lulatex"
PANDOC_PDF_ENGINE_XELATEX = "xelatex"


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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name_curr = cfg.glob.action_curr.get_full_name()

    file_name_next = cfg.glob.action_curr.get_stem_name() + "." + db.cls_document.Document.DOCUMENT_FILE_TYPE_PDF
    full_name_next = utils.get_full_name(
        cfg.glob.action_curr.action_directory_name,
        file_name_next,
    )

    if os.path.exists(full_name_next):
        cfg.glob.action_curr.finalise_error(
            error_code=db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=ERROR_31_903.replace("{full_name}", full_name_next),
        )

        return

    # Convert the document
    extra_args = [
        f"--pdf-engine={PANDOC_PDF_ENGINE_XELATEX}",
        "-V",
        f"lang:{db.cls_language.Language.LANGUAGES_PANDOC[cfg.glob.document.document_id_language]}",
    ]

    try:
        pypandoc.convert_file(
            full_name_curr,
            db.cls_document.Document.DOCUMENT_FILE_TYPE_PDF,
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
            id_document=cfg.glob.action_curr.action_id_document,
            id_parent=cfg.glob.action_curr.action_id,
            no_pdf_pages=utils.get_pdf_pages_no(full_name_next),
        )

        utils.delete_auxiliary_file(full_name_curr)

        cfg.glob.action_curr.finalise()

        cfg.glob.run.run_total_processed_ok += 1
    except RuntimeError as err:
        cfg.glob.action_curr.finalise_error(
            error_code=db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE,
            error_msg=ERROR_31_902.replace("{full_name}", full_name_curr).replace("{error_type}", str(type(err))).replace("{error_msg}", str(err)),
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
