"""Module pp.pdflib_dcr: Extract text from pdf documents."""
import os
import time

import db.cfg
import db.orm.dml
import libs.cfg
import libs.utils
from PDFlib.TET import TET

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
PAGE_TET_DOCUMENT_OPT_LIST: str = (
    "engines={noannotation noimage text notextcolor novector} " + "lineseparator=U+0020"
)
PAGE_TET_PAGE_OPT_LIST: str = "granularity=page"

WORD_TET_DOCUMENT_OPT_LIST: str = "engines={noannotation noimage text notextcolor novector}"
WORD_TET_PAGE_OPT_LIST: str = "granularity=word tetml={elements={line}}"


# -----------------------------------------------------------------------------
# Extract text from pdf documents (step: tet).
# -----------------------------------------------------------------------------
def extract_text_from_pdf() -> None:
    """Extract text from pdf documents.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = db.orm.dml.dml_prepare(db.cfg.DBT_DOCUMENT)

    libs.utils.reset_statistics_total()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.orm.dml.select_document(conn, dbt, db.cfg.DOCUMENT_STEP_PDFLIB)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            extract_text_from_pdf_file_page()

            extract_text_from_pdf_file_word()

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text from a pdf document (step: tet) - method page.
# -----------------------------------------------------------------------------
def extract_text_from_pdf_file_page() -> None:
    """Extract text from a pdf document (step: tet) - method page."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    file_name = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    tet = TET()

    source_file = tet.open_document(file_name, PAGE_TET_DOCUMENT_OPT_LIST)

    if source_file == -1:
        db.orm.dml.update_document_error(
            document_id=libs.cfg.document_id,
            error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_OPEN,
            error_msg=db.cfg.ERROR_51_901.replace("{file_name}", file_name)
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

        db.orm.dml.insert_dbt_row(
            db.cfg.DBT_CONTENT_TETML_PAGE,
            {
                db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id_base,
                db.cfg.DBC_PAGE_NO: page_no,
                db.cfg.DBC_PAGE_TEXT: tet.get_text(page_handle),
            },
        )

        tet.close_page(page_handle)

    tet.close_document(source_file)

    libs.cfg.document_child_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_DOCUMENT,
        {
            db.cfg.DBC_CURRENT_STEP: libs.cfg.document_current_step,
            db.cfg.DBC_DOCUMENT_ID_BASE: libs.cfg.document_id_base,
            db.cfg.DBC_DOCUMENT_ID_PARENT: libs.cfg.document_id,
            db.cfg.DBC_DURATION_NS: 0,
            db.cfg.DBC_ERROR_NO: 0,
            db.cfg.DBC_NEXT_STEP: db.cfg.DOCUMENT_STEP_TOKENIZE,
            db.cfg.DBC_LANGUAGE_ID: libs.cfg.document_language_id,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: db.cfg.DOCUMENT_STATUS_START,
        },
    )

    tet.delete()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text from a pdf document (step: tet) - method word.
# -----------------------------------------------------------------------------
def extract_text_from_pdf_file_word() -> None:
    """Extract text from a pdf document (step: tet) - method word."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    source_file_name, target_file_name = libs.utils.prepare_file_names(
        db.cfg.DOCUMENT_FILE_TYPE_XML
    )

    tet = TET()

    doc_opt_list = f"tetml={{filename={{{target_file_name}}}}} {WORD_TET_DOCUMENT_OPT_LIST}"

    source_file = tet.open_document(source_file_name, doc_opt_list)

    if source_file == -1:
        db.orm.dml.update_document_error(
            document_id=libs.cfg.document_id,
            error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_OPEN,
            error_msg=db.cfg.ERROR_51_901.replace("{file_name}", source_file_name)
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

    libs.utils.prepare_document_4_next_step(
        next_file_type=db.cfg.DOCUMENT_FILE_TYPE_XML,
        next_step=db.cfg.DOCUMENT_STEP_PARSER,
    )

    libs.cfg.document_child_file_name = (
        libs.cfg.document_stem_name + "." + db.cfg.DOCUMENT_FILE_TYPE_XML
    )
    libs.cfg.document_child_stem_name = libs.cfg.document_stem_name

    db.orm.dml.insert_document_child()

    libs.utils.delete_auxiliary_file(source_file_name)

    tet.delete()

    # Text from Document successfully extracted to database
    libs.utils.finalize_file_processing()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
