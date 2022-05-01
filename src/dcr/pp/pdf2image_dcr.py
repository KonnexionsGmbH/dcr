"""Module pp.pdf2image_dcr: Convert scanned image pdf documents to image
files."""
import os
import time

import cfg.glob
import comm.utils
import db.dml
import pdf2image


# -----------------------------------------------------------------------------
# Convert scanned image pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image() -> None:
    """Convert scanned image pdf documents to image files.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    if cfg.glob.setup.pdf2image_type == cfg.glob.setup.PDF2IMAGE_TYPE_PNG:
        cfg.glob.document_child_file_type = cfg.glob.DOCUMENT_FILE_TYPE_PNG
    else:
        cfg.glob.document_child_file_type = cfg.glob.DOCUMENT_FILE_TYPE_JPG

    comm.utils.reset_statistics_total()

    dbt = db.dml.dml_prepare(cfg.glob.DBT_DOCUMENT)

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = db.dml.select_document(conn, dbt, cfg.glob.DOCUMENT_STEP_PDF2IMAGE)

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            comm.utils.start_document_processing(
                document=row,
            )

            convert_pdf_2_image_file()

        conn.close()

    comm.utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert a scanned image pdf document to an image file (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image_file() -> None:
    """Convert a scanned image pdf document to an image file."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    file_name_parent = os.path.join(
        cfg.glob.document_directory_name,
        cfg.glob.document_file_name,
    )

    images = pdf2image.convert_from_path(file_name_parent)

    comm.utils.prepare_document_4_next_step(
        next_file_type=cfg.glob.setup.pdf2image_type,
        next_step=cfg.glob.DOCUMENT_STEP_TESSERACT,
    )

    cfg.glob.document_child_child_no = 0

    # Store the image pages
    for img in images:
        cfg.glob.document_child_child_no += 1

        cfg.glob.document_child_stem_name = cfg.glob.document_stem_name + "_" + str(cfg.glob.document_child_child_no)

        cfg.glob.document_child_file_name = cfg.glob.document_child_stem_name + "." + cfg.glob.document_child_file_type

        file_name_child = os.path.join(
            cfg.glob.document_child_directory_name,
            cfg.glob.document_child_file_name,
        )

        if os.path.exists(file_name_child):
            db.dml.update_document_error(
                document_id=cfg.glob.document_id,
                error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
                error_msg=cfg.glob.ERROR_21_903.replace("{file_name}", file_name_child),
            )
        else:
            img.save(
                file_name_child,
                cfg.glob.setup.pdf2image_type,
            )

            db.dml.insert_document_child()

            cfg.glob.total_generated += 1

    comm.utils.delete_auxiliary_file(file_name_parent)

    cfg.glob.total_ok_processed += 1

    # Document successfully converted to image format
    duration_ns = db.dml.update_document_statistics(
        document_id=cfg.glob.document_id, status=cfg.glob.DOCUMENT_STATUS_END
    )

    if cfg.glob.setup.is_verbose:
        comm.utils.progress_msg(
            f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {cfg.glob.document_id:6d} "
            f"[{db.dml.select_document_file_name_id(cfg.glob.document_id)}]"
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
