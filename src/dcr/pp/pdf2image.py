"""Module pp.pdf2image: Convert scanned image pdf documents to image files."""
import os
import time

import dcr_core.cls_setup
import dcr_core.core_glob
import dcr_core.core_utils
import dcr_core.processing

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_action
import dcr.db.cls_document
import dcr.db.cls_run
import dcr.utils


# -----------------------------------------------------------------------------
# Convert scanned image pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image() -> None:
    """Convert scanned image pdf documents to image files.

    TBD
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    with dcr.cfg.glob.db_core.db_orm_engine.begin() as conn:
        rows = dcr.db.cls_action.Action.select_action_by_action_code(conn=conn, action_code=dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE)

        for row in rows:
            dcr.cfg.glob.start_time_document = time.perf_counter_ns()

            dcr.cfg.glob.run.run_total_processed_to_be += 1

            dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_row(row)

            if dcr.cfg.glob.action_curr.action_status == dcr.db.cls_document.Document.DOCUMENT_STATUS_ERROR:
                dcr.cfg.glob.run.total_status_error += 1
            else:
                dcr.cfg.glob.run.total_status_ready += 1

            dcr.cfg.glob.document = dcr.db.cls_document.Document.from_id(id_document=dcr.cfg.glob.action_curr.action_id_document)

            convert_pdf_2_image_file()

        conn.close()

    dcr.utils.show_statistics_total()

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert a scanned image pdf document to an image file (step: p_2_i).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def convert_pdf_2_image_file() -> None:
    """Convert a scanned image pdf document to an image file."""
    full_name_curr = dcr_core.core_utils.get_full_name(
        dcr.cfg.glob.action_curr.action_directory_name,
        dcr.cfg.glob.action_curr.action_file_name,
    )

    file_name_next = (
        dcr.cfg.glob.action_curr.get_stem_name()
        + "_[0-9]*."
        + (
            dcr_core.core_glob.FILE_TYPE_PNG
            if dcr_core.core_glob.setup.pdf2image_type == dcr_core.cls_setup.Setup.PDF2IMAGE_TYPE_PNG
            else dcr_core.core_glob.FILE_TYPE_JPEG
        )
    )

    (error_code, error_msg, children) = dcr_core.processing.pdf2image_process(
        full_name_in=full_name_curr,
    )
    if error_code != dcr_core.core_glob.RETURN_OK[0]:
        dcr.cfg.glob.action_curr.finalise_error(error_code, error_msg)
        return

    file_size_bytes = 0

    for (_, full_name_next) in children:
        file_size_bytes += os.path.getsize(full_name_next)

    dcr.cfg.glob.action_curr.action_no_children = len(children)

    dcr.cfg.glob.action_next = dcr.db.cls_action.Action(
        action_code=dcr.db.cls_run.Run.ACTION_CODE_TESSERACT,
        id_run_last=dcr.cfg.glob.run.run_id,
        directory_name=dcr.cfg.glob.action_curr.action_directory_name,
        directory_type=dcr.cfg.glob.action_curr.action_directory_type,
        file_name=file_name_next,
        file_size_bytes=file_size_bytes,
        id_document=dcr.cfg.glob.action_curr.action_id_document,
        id_parent=dcr.cfg.glob.action_curr.action_id,
        no_children=dcr.cfg.glob.action_curr.action_no_children,
        no_pdf_pages=dcr.cfg.glob.action_curr.action_no_children,
    )

    dcr.cfg.glob.run.total_generated += len(children)

    dcr.utils.delete_auxiliary_file(full_name_curr)

    dcr.cfg.glob.action_curr.finalise()

    dcr.cfg.glob.run.run_total_processed_ok += 1
