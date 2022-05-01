"""Module pp.tesseract_dcr: Convert image documents to pdf files."""
import os
import time

import cfg.glob
import db.dml
import libs.utils
import PyPDF2
import pytesseract
import sqlalchemy


# -----------------------------------------------------------------------------
# Convert image documents to pdf files (step: ocr).
# -----------------------------------------------------------------------------
def convert_image_2_pdf() -> None:
    """Convert image documents to pdf files.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    dbt = db.dml.dml_prepare(cfg.glob.DBT_DOCUMENT)

    libs.utils.reset_statistics_total()

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = db.dml.select_document(conn, dbt, cfg.glob.DOCUMENT_STEP_TESSERACT)

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            convert_image_2_pdf_file()

        conn.close()

    libs.utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert image documents to pdf files (step: ocr).
# -----------------------------------------------------------------------------
def convert_image_2_pdf_file() -> None:
    """Convert scanned image pdf documents to image files."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    source_file_name, target_file_name = libs.utils.prepare_file_names(cfg.glob.DOCUMENT_FILE_TYPE_PDF)

    if os.path.exists(target_file_name):
        db.dml.update_document_error(
            document_id=cfg.glob.document_id,
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=cfg.glob.ERROR_41_903.replace("{file_name}", target_file_name),
        )
        return

    # Convert the document
    try:
        pdf = pytesseract.image_to_pdf_or_hocr(
            extension="pdf",
            image=source_file_name,
            lang=cfg.glob.languages_tesseract[cfg.glob.document_language_id],
            timeout=cfg.glob.setup.tesseract_timeout,
        )

        with open(target_file_name, "w+b") as target_file:
            # pdf type is bytes by default
            target_file.write(pdf)

        libs.utils.prepare_document_4_next_step(
            next_file_type=cfg.glob.DOCUMENT_FILE_TYPE_PDF,
            next_step=cfg.glob.DOCUMENT_STEP_PDFLIB,
        )

        cfg.glob.document_child_file_name = cfg.glob.document_stem_name + "." + cfg.glob.DOCUMENT_FILE_TYPE_PDF

        cfg.glob.document_child_stem_name = cfg.glob.document_stem_name

        db.dml.insert_document_child()

        if cfg.glob.document_id_base != cfg.glob.document_id_parent:
            libs.utils.delete_auxiliary_file(source_file_name)

        # Document successfully converted to pdf format
        duration_ns = libs.utils.finalize_file_processing()

        if cfg.glob.setup.is_verbose:
            libs.utils.progress_msg(
                f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                f"Document: {cfg.glob.document_id:6d} "
                f"[{db.dml.select_document_file_name_id(cfg.glob.document_id)}]"
            )
    except RuntimeError as err:
        db.dml.update_document_error(
            document_id=cfg.glob.document_id,
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_TESSERACT,
            error_msg=cfg.glob.ERROR_41_901.replace("{source_file}", source_file_name)
            .replace("{target_file}", target_file_name)
            .replace("{type_error}", str(type(err)))
            .replace("{error}", str(err)),
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Reunite all related pdf documents.
# -----------------------------------------------------------------------------
def reunite_pdfs() -> None:
    """Reunite all related pdf documents.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    dbt = db.dml.dml_prepare(cfg.glob.DBT_DOCUMENT)

    libs.utils.reset_statistics_total()

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = conn.execute(
            sqlalchemy.select(dbt).where(
                dbt.c.id.in_(
                    sqlalchemy.select(dbt.c.document_id_base)
                    .where(dbt.c.status == cfg.glob.DOCUMENT_STATUS_START)
                    .where(dbt.c.next_step == cfg.glob.DOCUMENT_STEP_PDFLIB)
                    .group_by(dbt.c.document_id_base)
                    .having(sqlalchemy.func.count(dbt.c.document_id_base) > 1)
                    .scalar_subquery()
                )
            )
        )

        for row in rows:
            libs.utils.start_document_processing(
                document=row,
            )

            reunite_pdfs_file()

        conn.close()

    libs.utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Reunite the related pdf documents of a specific base document.
# -----------------------------------------------------------------------------
def reunite_pdfs_file() -> None:
    """Reunite the related pdf documents of a specific base document."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    cfg.glob.document_child_stem_name = cfg.glob.document_stem_name + "_" + str(cfg.glob.document_id_base) + "_0"
    cfg.glob.document_child_file_name = cfg.glob.document_child_stem_name + "." + cfg.glob.DOCUMENT_FILE_TYPE_PDF

    target_file_path = os.path.join(
        cfg.glob.setup.directory_inbox_accepted,
        cfg.glob.document_child_file_name,
    )

    if os.path.exists(target_file_path):
        db.dml.update_document_error(
            document_id=cfg.glob.document_id,
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=cfg.glob.ERROR_41_904.replace("{file_name}", str(target_file_path)),
        )
        return

    pdf_writer = PyPDF2.PdfFileWriter()

    cfg.glob.documents_to_be_reunited = []

    dbt = db.dml.dml_prepare(cfg.glob.DBT_DOCUMENT)

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = conn.execute(
            sqlalchemy.select(dbt)
            .where(dbt.c.status == cfg.glob.DOCUMENT_STATUS_START)
            .where(dbt.c.next_step == cfg.glob.DOCUMENT_STEP_PDFLIB)
            .where(dbt.c.document_id_base == cfg.glob.document_id_base)
            .order_by(dbt.c.id)
        )

        cfg.glob.document_child_id_parent = 0

        for row in rows:
            start_time_document = time.perf_counter_ns()

            cfg.glob.document_child_id_parent = row.id

            source_file_path = os.path.join(row.directory_name, row.file_name)

            pdf_reader = PyPDF2.PdfFileReader(source_file_path)
            for page in range(pdf_reader.getNumPages()):
                # Add each page to the writer object
                pdf_writer.addPage(pdf_reader.getPage(page))

            libs.utils.delete_auxiliary_file(str(source_file_path))

            duration_ns = time.perf_counter_ns() - start_time_document

            db.dml.update_dbt_id(
                cfg.glob.DBT_DOCUMENT,
                row.id,
                {
                    cfg.glob.DBC_DURATION_NS: duration_ns,
                    cfg.glob.DBC_NEXT_STEP: cfg.glob.DOCUMENT_STEP_PYPDF2,
                    cfg.glob.DBC_STATUS: cfg.glob.DOCUMENT_STATUS_END,
                },
            )

            cfg.glob.document_child_id_parent = row.id

        conn.close()

    # Write out the merged PDF
    with open(target_file_path, "wb") as out:
        pdf_writer.write(out)

    libs.utils.prepare_document_4_next_step(
        next_file_type=cfg.glob.DOCUMENT_FILE_TYPE_PDF,
        next_step=cfg.glob.DOCUMENT_STEP_PDFLIB,
    )

    cfg.glob.document_child_directory_name = cfg.glob.setup.directory_inbox_accepted
    cfg.glob.document_child_directory_type = cfg.glob.DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED

    db.dml.insert_document_child()

    # Child document successfully reunited to one pdf document
    duration_ns = libs.utils.finalize_file_processing()

    if cfg.glob.setup.is_verbose:
        libs.utils.progress_msg(
            f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {cfg.glob.document_id:6d} "
            f"[{db.dml.select_document_file_name_id(cfg.glob.document_id)}]"
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
