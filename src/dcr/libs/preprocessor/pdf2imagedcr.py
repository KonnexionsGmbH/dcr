"""Module libs.preprocessor.pdf2imagedcr: Convert scanned image pdf documents
to image files."""
import inspect
import os
import time

import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.preprocessor.inbox
import libs.utils
import pdf2image
from pdf2image.exceptions import PDFPopplerTimeoutError


# -----------------------------------------------------------------------------
# Convert scanned image pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image() -> None:
    """Convert scanned image pdf documents to image files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.config[libs.cfg.DCR_CFG_PDF2IMAGE_TYPE] == libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_PNG:
        libs.cfg.document_child_file_type = libs.db.cfg.DOCUMENT_FILE_TYPE_PNG
    else:
        libs.cfg.document_child_file_type = libs.db.cfg.DOCUMENT_FILE_TYPE_JPG

    libs.utils.reset_statistics_total()

    dbt = libs.utils.select_document_prepare()

    with libs.db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, libs.db.cfg.DOCUMENT_NEXT_STEP_PDF2IMAGE)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                module_name=__name__,
                function_name=inspect.stack()[0][3],
                document=row,
                journal_action=libs.db.cfg.JOURNAL_ACTION_21_001,
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

    number_errors = 0

    try:
        # Convert the 'pdf' document
        images = pdf2image.convert_from_path(file_name_parent)

        libs.utils.prepare_document_4_next_step(
            next_file_type=libs.cfg.pdf2image_type,
            next_step=libs.db.cfg.DOCUMENT_NEXT_STEP_TESSERACT,
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
                    module_name=__name__,
                    function_name=inspect.stack()[0][3],
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
                    journal_action=libs.db.cfg.JOURNAL_ACTION_21_903.replace(
                        "{file_name}", file_name_child
                    ),
                )
            else:
                img.save(
                    file_name_child,
                    libs.cfg.pdf2image_type,
                )

                journal_action: str = libs.db.cfg.JOURNAL_ACTION_21_004.replace(
                    "{file_name}", libs.cfg.document_child_file_name
                )

                libs.utils.initialise_document_child(journal_action)

                libs.cfg.total_generated += 1

                # Document successfully converted to image format
                libs.utils.finalize_file_processing(
                    module_name=__name__,
                    function_name=inspect.stack()[0][3],
                    journal_action=libs.db.cfg.JOURNAL_ACTION_21_002.replace(
                        "{file_name}", libs.cfg.document_file_name
                    ).replace("{child_no}", str(libs.cfg.document_child_child_no)),
                )
                libs.cfg.total_ok_processed -= 1

        libs.cfg.total_ok_processed += 1

    # not testable
    except PDFPopplerTimeoutError as err:
        number_errors += 1
        libs.utils.report_document_error(
            module_name=__name__,
            function_name=inspect.stack()[0][3],
            error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE,
            journal_action=libs.db.cfg.JOURNAL_ACTION_21_901.replace(
                "{file_name}", libs.cfg.document_file_name
            ).replace("{error_msg}", str(err)),
        )

    # _pylint: disable=expression-not-assigned
    if number_errors == 0:
        journal_action: str = libs.db.cfg.JOURNAL_ACTION_21_003
    else:
        journal_action: str = libs.db.cfg.JOURNAL_ACTION_21_005

    libs.db.orm.insert_journal(
        __name__,
        inspect.stack()[0][3],
        libs.cfg.document_id,
        journal_action.replace(
            "{file_name}",
            libs.cfg.document_file_name,
        ),
    )
