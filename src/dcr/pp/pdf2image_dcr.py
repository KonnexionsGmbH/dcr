"""Module pp.pdf2image_dcr: Convert scanned image pdf documents to image
files."""
import os
import time

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_document
import db.cls_run
import pdf2image
import utils
from pdf2image.exceptions import PDFPageCountError

# -----------------------------------------------------------------------------
# Class variables.
# -----------------------------------------------------------------------------
ERROR_21_901: str = (
    "21.901 Issue (p_2_i): Processing file '{full_name_curr}' with pdf2image failed - "
    + "error type: '{error_type}' - error: '{error}'."
)
ERROR_21_903: str = "21.903 Issue (p_2_i): The target file '{full_name}' already exists."


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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name_curr = utils.get_full_name(
        cfg.glob.action_curr.action_directory_name,
        cfg.glob.action_curr.action_file_name,
    )

    try:
        images = pdf2image.convert_from_path(full_name_curr)

        cfg.glob.action_curr.action_no_children = 0

        is_no_error: bool = True

        # Store the image pages
        for img in images:
            cfg.glob.action_curr.action_no_children += 1

            stem_name_next = cfg.glob.action_curr.get_stem_name() + "_" + str(cfg.glob.action_curr.action_no_children)

            file_name_next = (
                stem_name_next
                + "."
                + (
                    db.cls_document.Document.DOCUMENT_FILE_TYPE_PNG
                    if cfg.glob.setup.pdf2image_type == cfg.cls_setup.Setup.PDF2IMAGE_TYPE_PNG
                    else db.cls_document.Document.DOCUMENT_FILE_TYPE_JPEG
                )
            )

            full_name_next = utils.get_full_name(
                cfg.glob.action_curr.action_directory_name,
                file_name_next,
            )

            if os.path.exists(full_name_next):
                cfg.glob.action_curr.finalise_error(
                    error_code=db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
                    error_msg=ERROR_21_903.replace("{full_name}", full_name_next),
                )

                is_no_error = False
            else:
                img.save(
                    full_name_next,
                    cfg.glob.setup.pdf2image_type,
                )

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

                cfg.glob.run.total_generated += 1

        if is_no_error:
            utils.delete_auxiliary_file(full_name_curr)

            cfg.glob.action_curr.finalise()

            cfg.glob.run.run_total_processed_ok += 1
    except PDFPageCountError as err:
        cfg.glob.action_curr.finalise_error(
            error_code=db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE,
            error_msg=ERROR_21_901.replace("{full_name_curr}", full_name_curr)
            .replace("{error_type}", str(type(err)))
            .replace("{error}", str(err)),
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
