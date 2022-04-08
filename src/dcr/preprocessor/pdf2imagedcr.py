"""Module preprocessor.pdf2imagedcr: Convert scanned image pdf documents to
image files."""
import os
import time

import db.cfg
import db.orm.dml
import libs.cfg
import libs.utils
import pdf2image

# not testable
# from pdf2image.exceptions import PDFPopplerTimeoutError


# -----------------------------------------------------------------------------
# Convert scanned image pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image() -> None:
    """Convert scanned image pdf documents to image files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.config[libs.cfg.DCR_CFG_PDF2IMAGE_TYPE] == libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_PNG:
        libs.cfg.document_child_file_type = db.cfg.DOCUMENT_FILE_TYPE_PNG
    else:
        libs.cfg.document_child_file_type = db.cfg.DOCUMENT_FILE_TYPE_JPG

    libs.utils.reset_statistics_total()

    dbt = libs.utils.select_document_prepare()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, db.cfg.DOCUMENT_STEP_PDF2IMAGE)

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
    file_name_parent = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    # not testable
    # number_errors = 0
    #
    # try:
    # Convert the 'pdf' document
    images = pdf2image.convert_from_path(file_name_parent)

    libs.utils.prepare_document_4_next_step(
        next_file_type=libs.cfg.pdf2image_type,
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
            libs.utils.report_document_error(
                error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
                error=db.cfg.ERROR_21_903.replace("{file_name}", file_name_child),
            )
        else:
            img.save(
                file_name_child,
                libs.cfg.pdf2image_type,
            )

            libs.utils.initialise_document_child()

            libs.cfg.total_generated += 1

            # Document successfully converted to image format
            libs.utils.finalize_file_processing()
            libs.cfg.total_ok_processed -= 1

    libs.cfg.total_ok_processed += 1

    db.orm.dml.insert_journal_statistics(libs.cfg.document_id)
    # not testable
    # except PDFPopplerTimeoutError as err:
    #     number_errors += 1
    #     libs.utils.report_document_error(
    #         error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE,
    #         error=db.cfg.ERROR_21_901.replace(
    #             "{file_name}", libs.cfg.document_file_name
    #         ).replace("{error_msg}", str(err)),
    #     )
