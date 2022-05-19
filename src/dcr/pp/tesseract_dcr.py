"""Module pp.tesseract_dcr: Convert image documents to pdf files."""
import os
import time

import cfg.glob
import db.cls_action
import db.cls_base
import db.cls_run
import db.dml
import PyPDF2
import pytesseract
import utils


# -----------------------------------------------------------------------------
# Convert image documents to pdf files (step: ocr).
# -----------------------------------------------------------------------------
def convert_image_2_pdf() -> None:
    """Convert image documents to pdf files.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    with cfg.glob.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(
            conn=conn, action_code=db.cls_run.Run.ACTION_CODE_TESSERACT
        )

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_row(row)

            if cfg.glob.action_curr.action_status == cfg.glob.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                # not testable
                cfg.glob.run.total_status_ready += 1

            cfg.glob.base = db.cls_base.Base.from_id(id_base=cfg.glob.action_curr.action_id_base)

            convert_image_2_pdf_file()

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert image documents to pdf files (step: ocr).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def convert_image_2_pdf_file() -> None:
    """Convert scanned image pdf documents to image files."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name_curr = cfg.glob.action_curr.get_full_name()

    file_name_next = cfg.glob.action_curr.get_stem_name() + "." + cfg.glob.DOCUMENT_FILE_TYPE_PDF
    full_name_next = utils.get_full_name(
        cfg.glob.action_curr.action_directory_name,
        file_name_next,
    )

    if os.path.exists(full_name_next):
        cfg.glob.action_curr.finalise_error(
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=cfg.glob.ERROR_41_903.replace("{full_name}", full_name_next),
        )
        return

    # Convert the document
    try:
        pdf = pytesseract.image_to_pdf_or_hocr(
            extension="pdf",
            image=full_name_curr,
            lang=cfg.glob.languages_tesseract[cfg.glob.base.base_id_language],
            timeout=cfg.glob.setup.tesseract_timeout,
        )

        with open(full_name_next, "w+b") as file_handle:
            # pdf type is bytes by default
            file_handle.write(pdf)

        cfg.glob.action_next = db.cls_action.Action(
            action_code=db.cls_run.Run.ACTION_CODE_PDFLIB,
            id_run_last=cfg.glob.run.run_id,
            directory_name=cfg.glob.action_curr.action_directory_name,
            directory_type=cfg.glob.action_curr.action_directory_type,
            file_name=file_name_next,
            file_size_bytes=os.path.getsize(full_name_next),
            id_base=cfg.glob.action_curr.action_id_base,
            id_parent=cfg.glob.action_curr.action_id,
            no_pdf_pages=utils.get_pdf_pages_no(full_name_next),
        )

        utils.delete_auxiliary_file(full_name_curr)

        cfg.glob.action_curr.finalise()
    except RuntimeError as err:
        cfg.glob.action_curr.finalise_error(
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_TESSERACT,
            error_msg=cfg.glob.ERROR_41_901.replace("{full_name_curr}", full_name_curr)
            .replace("{full_name_next}", full_name_next)
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

    with cfg.glob.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_id_base_by_action_code_pypdf2(
            conn=conn, action_code=db.cls_run.Run.ACTION_CODE_PDFLIB
        )

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_id(row[0])

            cfg.glob.action_curr.action_action_code = db.cls_run.Run.ACTION_CODE_PYPDF2
            cfg.glob.action_curr.action_file_name = (
                cfg.glob.action_curr.get_stem_name()[0:-2] + "." + cfg.glob.DOCUMENT_FILE_TYPE_PDF
            )
            cfg.glob.action_curr.action_file_size_bytes = -1
            cfg.glob.action_curr.action_id = 0
            cfg.glob.action_curr.action_no_pdf_pages = -1

            if cfg.glob.action_curr.action_status == cfg.glob.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                # not testable
                cfg.glob.run.total_status_ready += 1

            cfg.glob.base = db.cls_base.Base.from_id(id_base=cfg.glob.action_curr.action_id_base)

            reunite_pdfs_file()

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Reunite the related pdf documents of a specific base document.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def reunite_pdfs_file() -> None:
    """Reunite the related pdf documents of a specific base document."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    stem_name_next = cfg.glob.action_curr.get_stem_name() + "_0"
    file_name_next = stem_name_next + "." + cfg.glob.DOCUMENT_FILE_TYPE_PDF

    full_name_next = utils.get_full_name(
        cfg.glob.action_curr.action_directory_name,
        file_name_next,
    )

    if os.path.exists(full_name_next):
        cfg.glob.action_curr.finalise_error(
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=cfg.glob.ERROR_41_904.replace("{full_name}", str(full_name_next)),
        )
        return

    pdf_writer = PyPDF2.PdfFileWriter()

    with cfg.glob.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code_id_base(
            conn=conn, action_code=db.cls_run.Run.ACTION_CODE_PDFLIB, id_base=cfg.glob.action_curr.action_id_base
        )

        for row in rows:
            start_time_document = time.perf_counter_ns()

            cfg.glob.run.total_generated += 1

            cfg.glob.document_child_id_parent = row

            action_part = db.cls_action.Action.from_row(row)

            full_name_curr = action_part.get_full_name()

            pdf_reader = PyPDF2.PdfFileReader(full_name_curr)
            for page in range(pdf_reader.getNumPages()):
                # Add each page to the writer object
                pdf_writer.addPage(pdf_reader.getPage(page))

            utils.delete_auxiliary_file(str(full_name_curr))

            action_part.action_code = db.cls_run.Run.ACTION_CODE_PYPDF2
            action_part.action_duration_ns = time.perf_counter_ns() - start_time_document
            action_part.action_status = cfg.glob.DOCUMENT_STATUS_END

            action_part.persist_2_db()

        conn.close()

    # Write out the merged PDF
    with open(full_name_next, "wb") as file_handle:
        pdf_writer.write(file_handle)

    cfg.glob.action_next = db.cls_action.Action(
        action_code=db.cls_run.Run.ACTION_CODE_PDFLIB,
        id_run_last=cfg.glob.run.run_id,
        directory_name=cfg.glob.action_curr.action_directory_name,
        directory_type=cfg.glob.action_curr.action_directory_type,
        file_name=file_name_next,
        file_size_bytes=os.path.getsize(full_name_next),
        id_base=cfg.glob.action_curr.action_id_base,
        id_parent=cfg.glob.action_curr.action_id,
        no_pdf_pages=utils.get_pdf_pages_no(full_name_next),
    )

    cfg.glob.action_curr.finalise()

    cfg.glob.run.run_total_processed_ok += 1

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
