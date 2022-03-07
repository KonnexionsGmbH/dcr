"""Module libs.inbox: Check, distribute and process incoming documents.

New documents are made available in the file directory inbox. These are
then checked and moved to the accepted or rejected file directories
depending on the result of the check. Depending on the file format, the
accepted documents are then converted into the pdf file format either
with the help of Pandoc or with the help of Tesseract OCR.
"""
import inspect
import os

import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.inbox
import libs.utils
import pdf2image
from pdf2image.exceptions import PDFPopplerTimeoutError
from sqlalchemy import Table


# -----------------------------------------------------------------------------
# Convert pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image() -> None:
    """Convert scanned image pdf documents to image files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.total_erroneous = 0
    libs.cfg.total_generated = 0
    libs.cfg.total_ok_processed = 0
    libs.cfg.total_status_error = 0
    libs.cfg.total_status_ready = 0
    libs.cfg.total_to_be_processed = 0

    if libs.cfg.config[libs.cfg.DCR_CFG_PDF2IMAGE_TYPE] == libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_PNG:
        libs.cfg.document_child_file_type = libs.db.cfg.DOCUMENT_FILE_TYPE_PNG
    else:
        libs.cfg.document_child_file_type = libs.db.cfg.DOCUMENT_FILE_TYPE_JPG

    # Check the inbox file directories.
    libs.utils.check_directories()

    dbt = Table(
        libs.db.cfg.DBT_DOCUMENT,
        libs.db.cfg.db_orm_metadata,
        autoload_with=libs.db.cfg.db_orm_engine,
    )

    with libs.db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_documents(conn, dbt, libs.db.cfg.DOCUMENT_NEXT_STEP_PDF2IMAGE)

        for row in rows:
            libs.cfg.total_to_be_processed += 1

            libs.cfg.document_directory_name = row.directory_name
            libs.cfg.document_directory_type = row.directory_type
            libs.cfg.document_file_name = row.file_name
            libs.cfg.document_file_type = row.file_type
            libs.cfg.document_id = row.id
            libs.cfg.document_id_base = row.document_id_base
            libs.cfg.document_id_parent = row.document_id_parent
            libs.cfg.document_status = row.status
            libs.cfg.document_stem_name = row.stem_name

            libs.db.orm.update_document_status(
                {
                    libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_START,
                },
                libs.db.orm.insert_journal(
                    __name__,
                    inspect.stack()[0][3],
                    libs.cfg.document_id,
                    libs.db.cfg.JOURNAL_ACTION_21_001.replace(
                        "{file_name}", libs.cfg.document_file_name
                    ),
                ),
            )

            if libs.cfg.document_status == libs.db.cfg.DOCUMENT_STATUS_START:
                libs.cfg.total_status_ready += 1
            else:
                # not testable
                libs.cfg.total_status_error += 1

            convert_pdf_2_image_file()

        conn.close()

    libs.utils.progress_msg(
        f"Number documents to be processed:  {libs.cfg.total_to_be_processed:6d}"
    )

    if libs.cfg.total_to_be_processed > 0:
        libs.utils.progress_msg(
            f"Number status tesseract_pdf_ready: {libs.cfg.total_status_ready:6d}"
        )
        libs.utils.progress_msg(
            f"Number status tesseract_pdf_error: {libs.cfg.total_status_error:6d}"
        )
        libs.utils.progress_msg(
            f"Number documents converted:        {libs.cfg.total_ok_processed:6d}"
        )
        libs.utils.progress_msg(f"Number documents generated:        {libs.cfg.total_generated:6d}")
        libs.utils.progress_msg(f"Number documents erroneous:        {libs.cfg.total_erroneous:6d}")
        libs.utils.progress_msg(
            "The involved 'pdf' documents in the file directory "
            + "'inbox_accepted' are converted to an image format "
            + "for further processing",
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert pdf documents to image files (step: p_2_i).
# -----------------------------------------------------------------------------
def convert_pdf_2_image_file() -> None:
    """Convert scanned image pdf documents to image files."""
    file_name_parent = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    try:
        # Convert the 'pdf' document
        images = pdf2image.convert_from_path(file_name_parent)

        prepare_document_child_pdf2image()

        # Store the image pages
        for img in images:
            libs.cfg.document_child_child_no = +1

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
                # pylint: disable=expression-not-assigned
                libs.db.orm.update_document_status(
                    {
                        libs.db.cfg.DBC_ERROR_CODE: libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
                        libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
                    },
                    libs.db.orm.insert_journal(
                        __name__,
                        inspect.stack()[0][3],
                        libs.cfg.document_id,
                        libs.db.cfg.JOURNAL_ACTION_01_906.replace("{file_name}", file_name_child),
                    ),
                )

                libs.cfg.total_erroneous += 1
            else:
                img.save(
                    file_name_child,
                    libs.cfg.pdf2image_type,
                )

                journal_action: str = libs.db.cfg.JOURNAL_ACTION_21_003.replace(
                    "{file_name}", libs.cfg.document_child_file_name
                )

                libs.utils.initialise_document_child(journal_action)

                libs.cfg.total_generated += 1

                # Document successfully converted to image format
                libs.cfg.total_ok_processed += 1

                libs.db.orm.update_document_status(
                    {
                        libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_END,
                    },
                    libs.db.orm.insert_journal(
                        __name__,
                        inspect.stack()[0][3],
                        libs.cfg.document_id,
                        libs.db.cfg.JOURNAL_ACTION_21_002.replace(
                            "{file_name}", libs.cfg.document_file_name
                        ).replace("{child_no}", str(libs.cfg.document_child_child_no)),
                    ),
                )
    # not testable
    except PDFPopplerTimeoutError as err:
        libs.cfg.total_erroneous += 1

        libs.db.orm.update_document_status(
            {
                libs.db.cfg.DBC_ERROR_CODE: libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
            },
            libs.db.orm.insert_journal(
                __name__,
                inspect.stack()[0][3],
                libs.cfg.document_id,
                libs.db.cfg.JOURNAL_ACTION_21_901.replace(
                    "{file_name}", libs.cfg.document_file_name
                ).replace("{error_msg}", str(err)),
            ),
        )


# -----------------------------------------------------------------------------
# Prepare the base child document data - pdf2image.
# -----------------------------------------------------------------------------
def prepare_document_child_pdf2image() -> None:
    """Prepare the base child document data - pdf2image."""
    libs.cfg.document_child_child_no = 0
    libs.cfg.document_child_directory_name = libs.cfg.document_directory_name
    libs.cfg.document_child_directory_type = libs.cfg.document_directory_type
    libs.cfg.document_child_error_code = None

    libs.cfg.document_child_file_type = libs.cfg.pdf2image_type

    libs.cfg.document_child_id_base = libs.cfg.document_id_base
    libs.cfg.document_child_id_parent = libs.cfg.document_id

    libs.cfg.document_child_next_step = libs.db.cfg.DOCUMENT_NEXT_STEP_TESSERACT
    libs.cfg.document_child_status = libs.db.cfg.DOCUMENT_STATUS_START
