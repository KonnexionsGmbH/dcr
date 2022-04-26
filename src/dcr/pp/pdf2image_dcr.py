"""Module pp.pdf2image_dcr: Convert scanned image pdf documents to image
files."""
import os
import time

import db.cfg
import db.orm.dml
import libs.cfg
import libs.utils
import pdf2image


# -----------------------------------------------------------------------------
# Convert scanned image pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image() -> None:
    """Convert scanned image pdf documents to image files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.config.pdf2image_type == libs.cfg.config.PDF2IMAGE_TYPE_PNG:
        libs.cfg.document_child_file_type = db.cfg.DOCUMENT_FILE_TYPE_PNG
    else:
        libs.cfg.document_child_file_type = db.cfg.DOCUMENT_FILE_TYPE_JPG

    libs.utils.reset_statistics_total()

    dbt = db.orm.dml.dml_prepare(db.cfg.DBT_DOCUMENT)

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.orm.dml.select_document(conn, dbt, db.cfg.DOCUMENT_STEP_PDF2IMAGE)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            convert_pdf_2_image_file()

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert a scanned image pdf document to an image file (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image_file() -> None:
    """Convert a scanned image pdf document to an image file."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    file_name_parent = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    images = pdf2image.convert_from_path(file_name_parent)

    libs.utils.prepare_document_4_next_step(
        next_file_type=libs.cfg.config.pdf2image_type,
        next_step=db.cfg.DOCUMENT_STEP_TESSERACT,
    )

    libs.cfg.document_child_child_no = 0

    # Store the image pages
    for img in images:
        libs.cfg.document_child_child_no += 1

        libs.cfg.document_child_stem_name = (
            libs.cfg.document_stem_name + "_" + str(libs.cfg.document_child_child_no)
        )

        libs.cfg.document_child_file_name = (
            libs.cfg.document_child_stem_name + "." + libs.cfg.document_child_file_type
        )

        file_name_child = os.path.join(
            libs.cfg.document_child_directory_name,
            libs.cfg.document_child_file_name,
        )

        if os.path.exists(file_name_child):
            db.orm.dml.update_document_error(
                document_id=libs.cfg.document_id,
                error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
                error_msg=db.cfg.ERROR_21_903.replace("{file_name}", file_name_child),
            )
        else:
            img.save(
                file_name_child,
                libs.cfg.config.pdf2image_type,
            )

            db.orm.dml.insert_document_child()

            libs.cfg.total_generated += 1

    libs.utils.delete_auxiliary_file(file_name_parent)

    libs.cfg.total_ok_processed += 1

    # Document successfully converted to image format
    duration_ns = db.orm.dml.update_document_statistics(
        document_id=libs.cfg.document_id, status=db.cfg.DOCUMENT_STATUS_END
    )

    if libs.cfg.config.is_verbose:
        libs.utils.progress_msg(
            f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {libs.cfg.document_id:6d} "
            f"[{db.orm.dml.select_document_file_name_id(libs.cfg.document_id)}]"
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
