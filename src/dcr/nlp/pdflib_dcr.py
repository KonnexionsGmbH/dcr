"""Module nlp.pdflib_dcr: Extract text from pdf documents."""
import os
import time

import cfg.glob
import db.cls_action
import db.cls_document
import db.cls_run
import db.dml
import PDFlib.TET
import utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
LINE_TET_DOCUMENT_OPT_LIST: str = "engines={noannotation noimage text notextcolor novector}"
LINE_TET_PAGE_OPT_LIST: str = "granularity=line"
LINE_XML_VARIATION: str = "line."

PAGE_TET_DOCUMENT_OPT_LIST: str = "engines={noannotation noimage text notextcolor novector} " + "lineseparator=U+0020"
PAGE_TET_PAGE_OPT_LIST: str = "granularity=page"
PAGE_XML_VARIATION: str = "page."

WORD_TET_DOCUMENT_OPT_LIST: str = "engines={noannotation noimage text notextcolor novector}"
WORD_TET_PAGE_OPT_LIST: str = "granularity=word tetml={elements={line}}"
WORD_XML_VARIATION: str = "word."


# -----------------------------------------------------------------------------
# Extract text from pdf documents (step: tet).
# -----------------------------------------------------------------------------
def extract_text_from_pdf() -> None:
    """Extract text from pdf documents.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    with cfg.glob.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(
            conn=conn, action_code=db.cls_run.Run.ACTION_CODE_PDFLIB
        )

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_row(row)

            if cfg.glob.action_curr.action_status == cfg.glob.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                cfg.glob.run.total_status_ready += 1

            cfg.glob.document = db.cls_document.Document.from_id(id_document=cfg.glob.action_curr.action_id_document)

            is_no_error = extract_text_from_pdf_file(
                document_opt_list=LINE_TET_DOCUMENT_OPT_LIST,
                page_opt_list=LINE_TET_PAGE_OPT_LIST,
                xml_variation=LINE_XML_VARIATION,
            )

            if cfg.glob.setup.is_tetml_page:
                if is_no_error:
                    is_no_error = extract_text_from_pdf_file(
                        document_opt_list=PAGE_TET_DOCUMENT_OPT_LIST,
                        page_opt_list=PAGE_TET_PAGE_OPT_LIST,
                        xml_variation=PAGE_XML_VARIATION,
                    )

            if cfg.glob.setup.is_tetml_word:
                if is_no_error:
                    is_no_error = extract_text_from_pdf_file(
                        document_opt_list=WORD_TET_DOCUMENT_OPT_LIST,
                        page_opt_list=WORD_TET_PAGE_OPT_LIST,
                        xml_variation=WORD_XML_VARIATION,
                    )

            if is_no_error:
                utils.delete_auxiliary_file(cfg.glob.action_curr.get_full_name())

                cfg.glob.action_curr.finalise()

                cfg.glob.run.run_total_processed_ok += 1

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text from a pdf document (step: tet).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def extract_text_from_pdf_file(document_opt_list: str, page_opt_list: str, xml_variation: str) -> bool:
    """Extract text from a pdf document (step: tet) - method line."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name_curr = cfg.glob.action_curr.get_full_name()

    file_name_next = cfg.glob.action_curr.get_stem_name() + "." + xml_variation + cfg.glob.DOCUMENT_FILE_TYPE_XML
    full_name_next = utils.get_full_name(
        cfg.glob.action_curr.action_directory_name,
        file_name_next,
    )

    if os.path.exists(full_name_next):
        cfg.glob.action_curr.finalise_error(
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=cfg.glob.ERROR_51_904.replace("{full_name}", full_name_next),
        )

        return False

    tet = PDFlib.TET.TET()

    doc_opt_list = f"tetml={{filename={{{full_name_next}}}}} {document_opt_list}"

    file_curr = tet.open_document(full_name_curr, doc_opt_list)
    if file_curr == -1:
        cfg.glob.action_curr.finalise_error(
            error_code=cfg.glob.DOCUMENT_ERROR_CODE_REJ_FILE_OPEN,
            error_msg=cfg.glob.ERROR_51_901.replace("{full_name}", full_name_curr)
            .replace("{error_no}", str(tet.get_errnum()))
            .replace("{api_name}", tet.get_apiname() + "()")
            .replace("{error}", tet.get_errmsg()),
        )

        return False

    # get number of pages in the document */
    no_pages = tet.pcos_get_number(file_curr, "length:pages")

    # loop over pages in the document */
    for page_no in range(1, int(no_pages) + 1):
        tet.process_page(file_curr, page_no, page_opt_list)

    # This could be combined with the last page-related call
    tet.process_page(file_curr, 0, "tetml={trailer}")

    tet.close_document(file_curr)

    if xml_variation == LINE_XML_VARIATION:
        action_code = db.cls_run.Run.ACTION_CODE_PARSER_LINE
    elif xml_variation == PAGE_XML_VARIATION:
        action_code = db.cls_run.Run.ACTION_CODE_PARSER_PAGE
    else:
        action_code = db.cls_run.Run.ACTION_CODE_PARSER_WORD

    db.cls_action.Action(
        action_code=action_code,
        id_run_last=cfg.glob.run.run_id,
        directory_name=cfg.glob.action_curr.action_directory_name,
        directory_type=cfg.glob.action_curr.action_directory_type,
        file_name=file_name_next,
        file_size_bytes=os.path.getsize(full_name_next),
        id_document=cfg.glob.action_curr.action_id_document,
        id_parent=cfg.glob.action_curr.action_id,
        no_pdf_pages=utils.get_pdf_pages_no(full_name_next),
        status=cfg.glob.DOCUMENT_STATUS_START,
    )

    tet.delete()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    return True
