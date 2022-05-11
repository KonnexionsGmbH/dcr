"""Module nlp.pdflib_dcr: Extract text from pdf documents."""
import os
import time

import cfg.glob
import db.dml
import PDFlib.TET
import utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
LINE_TET_DOCUMENT_OPT_LIST: str = "engines={noannotation noimage text notextcolor novector}"
LINE_TET_PAGE_OPT_LIST: str = "granularity=line"

PAGE_TET_DOCUMENT_OPT_LIST: str = "engines={noannotation noimage text notextcolor novector} " + "lineseparator=U+0020"
PAGE_TET_PAGE_OPT_LIST: str = "granularity=page"

WORD_TET_DOCUMENT_OPT_LIST: str = "engines={noannotation noimage text notextcolor novector}"
WORD_TET_PAGE_OPT_LIST: str = "granularity=word tetml={elements={line}}"


# -----------------------------------------------------------------------------
# Create the child document entry.
# -----------------------------------------------------------------------------
def create_child_document() -> None:
    """Create the child document entry."""
    cfg.glob.document_child_id = db.dml.insert_dbt_row(
        cfg.glob.DBT_DOCUMENT,
        {
            cfg.glob.DBC_CURRENT_STEP: cfg.glob.document_current_step,
            cfg.glob.DBC_DOCUMENT_ID_BASE: cfg.glob.base.base_id_base,
            cfg.glob.DBC_DOCUMENT_ID_PARENT: cfg.glob.base.base_id,
            cfg.glob.DBC_DURATION_NS: 0,
            cfg.glob.DBC_ERROR_NO: 0,
            cfg.glob.DBC_NEXT_STEP: db.cls_run.Run.ACTION_CODE_TOKENIZE,
            cfg.glob.DBC_ID_LANGUAGE: cfg.glob.base.base_id_language,
            cfg.glob.DBC_ID_RUN: cfg.glob.run.run_id_run,
            cfg.glob.DBC_STATUS: cfg.glob.DOCUMENT_STATUS_START,
        },
    )


# -----------------------------------------------------------------------------
# Extract text from pdf documents (step: tet).
# -----------------------------------------------------------------------------
def extract_text_from_pdf() -> None:
    """Extract text from pdf documents.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    dbt = db.dml.dml_prepare(cfg.glob.DBT_DOCUMENT)

    utils.reset_statistics_total()

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = db.dml.select_document(conn, dbt, db.cls_run.Run.ACTION_CODE_PDFLIB)

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            utils.start_document_processing(
                document=row,
            )

            if cfg.glob.setup.is_tetml_line:
                extract_text_from_pdf_file_line()

            if cfg.glob.setup.is_tetml_page:
                extract_text_from_pdf_file_page()

            if cfg.glob.setup.is_tetml_word:
                extract_text_from_pdf_file_word()

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text from a pdf document (step: tet) - method line.
# -----------------------------------------------------------------------------
def extract_text_from_pdf_file_line() -> None:
    """Extract text from a pdf document (step: tet) - method line."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    xml_variation = "line."

    source_file_name, target_file_name = utils.prepare_file_names(xml_variation + cfg.glob.DOCUMENT_FILE_TYPE_XML)

    tet = PDFlib.TET.TET()

    doc_opt_list = f"tetml={{filename={{{target_file_name}}}}} {LINE_TET_DOCUMENT_OPT_LIST}"

    source_file = tet.open_document(source_file_name, doc_opt_list)
    if source_file == -1:
        db.dml.update_document_error(
            document_id=cfg.glob.base.base_id,
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_OPEN,
            error_msg=cfg.glob.ERROR_51_901.replace("{file_name}", source_file_name)
            .replace("{error_no}", str(tet.get_errnum()))
            .replace("{api_name}", tet.get_apiname() + "()")
            .replace("{error}", tet.get_errmsg()),
        )
        return

    # get number of pages in the document */
    no_pages = tet.pcos_get_number(source_file, "length:pages")

    # loop over pages in the document */
    for page_no in range(1, int(no_pages) + 1):
        tet.process_page(source_file, page_no, LINE_TET_PAGE_OPT_LIST)

    # This could be combined with the last page-related call
    tet.process_page(source_file, 0, "tetml={trailer}")

    tet.close_document(source_file)

    utils.prepare_document_4_next_step(
        next_file_type=cfg.glob.DOCUMENT_FILE_TYPE_XML,
        next_step=db.cls_run.Run.ACTION_CODE_PARSER_LINE,
    )

    cfg.glob.document_child_file_name = (
        cfg.glob.document_stem_name + "." + xml_variation + cfg.glob.DOCUMENT_FILE_TYPE_XML
    )

    cfg.glob.document_child_stem_name = cfg.glob.document_stem_name

    db.dml.insert_document_child()

    utils.delete_auxiliary_file(source_file_name)

    tet.delete()

    create_child_document()

    # Text from Document successfully extracted to database
    duration_ns = utils.finalize_file_processing()

    if cfg.glob.setup.is_verbose:
        utils.progress_msg(
            f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {cfg.glob.base.base_id:6d} "
            f"[line version: {db.dml.select_document_file_name_id(cfg.glob.base.base_id)}]"
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text from a pdf document (step: tet) - method page.
# -----------------------------------------------------------------------------
def extract_text_from_pdf_file_page() -> None:
    """Extract text from a pdf document (step: tet) - method page."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    file_name = os.path.join(
        cfg.glob.document_directory_name,
        cfg.glob.document_file_name,
    )

    tet = PDFlib.TET.TET()

    source_file = tet.open_document(file_name, PAGE_TET_DOCUMENT_OPT_LIST)
    if source_file == -1:
        db.dml.update_document_error(
            document_id=cfg.glob.base.base_id,
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_OPEN,
            error_msg=cfg.glob.ERROR_51_901.replace("{file_name}", file_name)
            .replace("{error_no}", str(tet.get_errnum()))
            .replace("{api_name}", tet.get_apiname() + "()")
            .replace("{error}", tet.get_errmsg()),
        )
        return

    # get number of pages in the document */
    no_pages = tet.pcos_get_number(source_file, "length:pages")

    # loop over pages in the document */
    for page_no in range(1, int(no_pages) + 1):
        page_handle = tet.open_page(source_file, page_no, PAGE_TET_PAGE_OPT_LIST)

        db.dml.insert_dbt_row(
            cfg.glob.DBT_CONTENT_TETML_PAGE,
            {
                cfg.glob.DBC_DOCUMENT_ID: cfg.glob.base.base_id_base,
                cfg.glob.DBC_PAGE_NO: page_no,
                cfg.glob.DBC_PAGE_DATA: tet.get_text(page_handle),
            },
        )

        tet.close_page(page_handle)

    tet.close_document(source_file)

    tet.delete()

    if not cfg.glob.setup.is_tetml_line:
        create_child_document()

    # Text from Document successfully extracted to database
    duration_ns = utils.finalize_file_processing()

    if cfg.glob.setup.is_verbose:
        utils.progress_msg(
            f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {cfg.glob.base.base_id:6d} "
            f"[page version: {db.dml.select_document_file_name_id(cfg.glob.base.base_id)}]"
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text from a pdf document (step: tet) - method word.
# -----------------------------------------------------------------------------
def extract_text_from_pdf_file_word() -> None:
    """Extract text from a pdf document (step: tet) - method word."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    xml_variation = "word."

    source_file_name, target_file_name = utils.prepare_file_names(xml_variation + cfg.glob.DOCUMENT_FILE_TYPE_XML)

    tet = PDFlib.TET.TET()

    doc_opt_list = f"tetml={{filename={{{target_file_name}}}}} {WORD_TET_DOCUMENT_OPT_LIST}"

    source_file = tet.open_document(source_file_name, doc_opt_list)
    if source_file == -1:
        db.dml.update_document_error(
            document_id=cfg.glob.base.base_id,
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_OPEN,
            error_msg=cfg.glob.ERROR_51_901.replace("{file_name}", source_file_name)
            .replace("{error_no}", str(tet.get_errnum()))
            .replace("{api_name}", tet.get_apiname() + "()")
            .replace("{error}", tet.get_errmsg()),
        )
        return

    # get number of pages in the document */
    no_pages = tet.pcos_get_number(source_file, "length:pages")

    # loop over pages in the document */
    for page_no in range(1, int(no_pages) + 1):
        tet.process_page(source_file, page_no, WORD_TET_PAGE_OPT_LIST)

    # This could be combined with the last page-related call
    tet.process_page(source_file, 0, "tetml={trailer}")

    tet.close_document(source_file)

    utils.prepare_document_4_next_step(
        next_file_type=cfg.glob.DOCUMENT_FILE_TYPE_XML,
        next_step=db.cls_run.Run.ACTION_CODE_PARSER_WORD,
    )

    cfg.glob.document_child_file_name = (
        cfg.glob.document_stem_name + "." + xml_variation + cfg.glob.DOCUMENT_FILE_TYPE_XML
    )
    cfg.glob.document_child_stem_name = cfg.glob.document_stem_name

    db.dml.insert_document_child()

    utils.delete_auxiliary_file(source_file_name)

    tet.delete()

    # Text from Document successfully extracted to database
    duration_ns = utils.finalize_file_processing()

    if cfg.glob.setup.is_verbose:
        utils.progress_msg(
            f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {cfg.glob.base.base_id:6d} "
            f"[word version: {db.dml.select_document_file_name_id(cfg.glob.base.base_id)}]"
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
