"""Module pp.pdf2image: Convert scanned image pdf documents to image files."""
import os
import time

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_document
import db.cls_run
import utils

import dcr_core.cfg.glob
import dcr_core.pp.pdf2image
import dcr_core.utils


# -----------------------------------------------------------------------------
# Convert scanned image pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image() -> None:
    """Convert scanned image pdf documents to image files.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    with cfg.glob.db_core.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(conn=conn, action_code=db.cls_run.Run.ACTION_CODE_PDF2IMAGE)

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_row(row)

            if cfg.glob.action_curr.action_status == db.cls_document.Document.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                cfg.glob.run.total_status_ready += 1

            cfg.glob.document = db.cls_document.Document.from_id(id_document=cfg.glob.action_curr.action_id_document)

            convert_pdf_2_image_file()

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert a scanned image pdf document to an image file (step: p_2_i).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def convert_pdf_2_image_file() -> None:
    """Convert a scanned image pdf document to an image file."""
    full_name_curr = dcr_core.utils.get_full_name(
        cfg.glob.action_curr.action_directory_name,
        cfg.glob.action_curr.action_file_name,
    )

    (error_code, error_msg, children) = dcr_core.pp.pdf2image.process(
        full_name_in=full_name_curr,
    )
    if error_code != dcr_core.cfg.glob.RETURN_OK[0]:
        cfg.glob.action_curr.finalise_error(error_code, error_msg)
        return

    for no_children, (file_name_next, full_name_next) in enumerate(children):
        cfg.glob.action_curr.action_no_children = no_children + 1

        cfg.glob.action_next = db.cls_action.Action(
            action_code=db.cls_run.Run.ACTION_CODE_TESSERACT,
            id_run_last=cfg.glob.run.run_id,
            directory_name=cfg.glob.action_curr.action_directory_name,
            directory_type=cfg.glob.action_curr.action_directory_type,
            file_name=file_name_next,
            file_size_bytes=os.path.getsize(full_name_next),
            id_document=cfg.glob.action_curr.action_id_document,
            id_parent=cfg.glob.action_curr.action_id,
            no_pdf_pages=utils.get_pdf_pages_no(full_name_next),
        )

    cfg.glob.run.total_generated += len(children)

    utils.delete_auxiliary_file(full_name_curr)

    cfg.glob.action_curr.finalise()

    cfg.glob.run.run_total_processed_ok += 1
