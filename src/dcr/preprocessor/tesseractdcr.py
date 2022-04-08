"""Module preprocessor.tesseractdcr: Convert image documents to pdf files."""
import os
import time

import db.cfg
import db.orm.dml
import libs.cfg
import libs.utils
import PyPDF4
import pytesseract
from sqlalchemy import func
from sqlalchemy import select


# -----------------------------------------------------------------------------
# Convert image documents to pdf files (step: ocr).
# -----------------------------------------------------------------------------
def convert_image_2_pdf() -> None:
    """Convert image documents to pdf files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = libs.utils.select_document_prepare()

    libs.utils.reset_statistics_total()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, db.cfg.DOCUMENT_STEP_TESSERACT)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            convert_image_2_pdf_file()

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert image documents to pdf files (step: ocr).
# -----------------------------------------------------------------------------
def convert_image_2_pdf_file() -> None:
    """Convert scanned image pdf documents to image files."""
    source_file_name, target_file_name = libs.utils.prepare_file_names()

    if os.path.exists(target_file_name):
        libs.utils.report_document_error(
            error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error=db.cfg.ERROR_41_903.replace("{file_name}", target_file_name),
        )
        return

    # Convert the document
    try:
        pdf = pytesseract.image_to_pdf_or_hocr(
            extension="pdf",
            image=source_file_name,
            lang=libs.cfg.languages_tesseract[libs.cfg.document_language_id],
            timeout=libs.cfg.tesseract_timeout,
        )

        with open(target_file_name, "w+b") as target_file:
            # pdf type is bytes by default
            target_file.write(pdf)

        libs.utils.prepare_document_4_next_step(
            next_file_type=db.cfg.DOCUMENT_FILE_TYPE_PDF,
            next_step=db.cfg.DOCUMENT_STEP_PDFLIB,
        )

        libs.cfg.document_child_file_name = (
            libs.cfg.document_stem_name + "." + db.cfg.DOCUMENT_FILE_TYPE_PDF
        )

        libs.cfg.document_child_stem_name = libs.cfg.document_stem_name

        libs.utils.initialise_document_child()

        if libs.cfg.document_id_base != libs.cfg.document_id_parent:
            libs.utils.delete_auxiliary_file(source_file_name)

        # Document successfully converted to pdf format
        libs.utils.finalize_file_processing()

        db.orm.dml.insert_journal_statistics(libs.cfg.document_id)
    # not testable
    # except TesseractError as err_t:
    #     libs.utils.report_document_error(
    #         error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_TESSERACT,
    #         error=db.cfg.ERROR_41_902.replace("{source_file}", source_file_name)
    #         .replace("{target_file}", target_file_name)
    #         .replace("{error_status}", str(err_t.status))
    #         .replace("{error}", err_t.message),
    #     )
    except RuntimeError as err:
        libs.utils.report_document_error(
            error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_TESSERACT,
            error=db.cfg.ERROR_41_901.replace("{source_file}", source_file_name)
            .replace("{target_file}", target_file_name)
            .replace("{type_error}", str(type(err)))
            .replace("{error}", str(err)),
        )


# -----------------------------------------------------------------------------
# Reunite all related pdf documents.
# -----------------------------------------------------------------------------
def reunite_pdfs() -> None:
    """Reunite all related pdf documents.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = libs.utils.select_document_prepare()

    libs.utils.reset_statistics_total()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = conn.execute(
            select(dbt).where(
                dbt.c.id
                == (
                    select(dbt.c.document_id_base)
                    .where(dbt.c.status == db.cfg.DOCUMENT_STATUS_START)
                    .where(dbt.c.next_step == db.cfg.DOCUMENT_STEP_PDFLIB)
                    .group_by(dbt.c.document_id_base)
                    .having(func.count(dbt.c.document_id_base) > 1)
                    .scalar_subquery()
                )
            )
        )

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            reunite_pdfs_file()

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Reunite the related pdf documents of a specific base document.
# -----------------------------------------------------------------------------
def reunite_pdfs_file() -> None:
    """Reunite the related pdf documents of a specific base document."""
    libs.cfg.document_child_stem_name = (
        libs.cfg.document_stem_name + "_" + str(libs.cfg.document_id_base) + "_0"
    )
    libs.cfg.document_child_file_name = (
        libs.cfg.document_child_stem_name + "." + db.cfg.DOCUMENT_FILE_TYPE_PDF
    )

    target_file_path = os.path.join(
        libs.cfg.directory_inbox_accepted,
        libs.cfg.document_child_file_name,
    )

    if os.path.exists(target_file_path):
        libs.utils.report_document_error(
            error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error=db.cfg.ERROR_41_904.replace("{file_name}", str(target_file_path)),
        )
        return

    pdf_writer = PyPDF4.PdfFileWriter()

    libs.cfg.documents_to_be_reunited = []

    dbt = libs.utils.select_document_prepare()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = conn.execute(
            select(dbt)
            .where(dbt.c.status == db.cfg.DOCUMENT_STATUS_START)
            .where(dbt.c.next_step == db.cfg.DOCUMENT_STEP_PDFLIB)
            .where(dbt.c.document_id_base == libs.cfg.document_id_base)
            .order_by(dbt.c.id)
        )

        libs.cfg.document_child_id_parent = 0

        for row in rows:
            libs.cfg.document_child_id_parent = row.id

            source_file_path = os.path.join(row.directory_name, row.file_name)

            pdf_reader = PyPDF4.PdfFileReader(source_file_path)
            for page in range(pdf_reader.getNumPages()):
                # Add each page to the writer object
                pdf_writer.addPage(pdf_reader.getPage(page))

            libs.utils.delete_auxiliary_file(str(source_file_path))

            db.orm.dml.update_dbt_id(
                db.cfg.DBT_DOCUMENT,
                row.id,
                {
                    db.cfg.DBC_NEXT_STEP: db.cfg.DOCUMENT_STEP_PYPDF4,
                    db.cfg.DBC_STATUS: db.cfg.DOCUMENT_STATUS_END,
                },
            )

        conn.close()

    # Write out the merged PDF
    with open(target_file_path, "wb") as out:
        pdf_writer.write(out)

    libs.utils.initialise_document_child()

    # Child document successfully reunited to one pdf document
    libs.utils.finalize_file_processing()

    db.orm.dml.insert_journal_statistics(libs.cfg.document_id)
