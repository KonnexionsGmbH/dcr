"""Module pp.pdflibdcr: Extract text and metadata from pdf documents."""
import time

import db.cfg
import db.orm.dml
import libs.cfg
import libs.utils
from PDFlib.TET import TET

# not testable
# from tetlib_py import TETException


# -----------------------------------------------------------------------------
# Extract text and metadata from pdf documents (step: tet).
# -----------------------------------------------------------------------------
def extract_text_from_pdf() -> None:
    """Extract text and metadata from pdf documents.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = libs.utils.select_document_prepare()

    libs.utils.reset_statistics_total()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.orm.dml.select_document(conn, dbt, db.cfg.DOCUMENT_STEP_PDFLIB)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            extract_text_from_pdf_file()

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text and metadata  from a pdf document (step: tet).
# -----------------------------------------------------------------------------
def extract_text_from_pdf_file() -> None:
    """Extract text and metadata from a pdf document."""
    source_file_name, target_file_name = libs.utils.prepare_file_names(
        db.cfg.DOCUMENT_FILE_TYPE_XML
    )

    print(f"wwe document_directory_name={libs.cfg.document_directory_name}")
    print(f"wwe source_file_name       ={source_file_name}")
    print(f"wwe target_file_name       ={target_file_name}")

    # not testable
    # tet = None

    # not testable
    # try:
    tet = TET()

    tet.set_option(libs.cfg.TET_GLOBAL_OPT_LIST)

    doc_opt_list = f"tetml={{filename={{{target_file_name}}}}} {libs.cfg.TET_BASE_DOC_OPT_LIST}"

    source_file = tet.open_document(source_file_name, doc_opt_list)

    # not testable
    # if source_file == -1:
    #     libs.utils.report_document_error(
    #         document_id = libs.cfg.document_id,
    #         error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_PDFLIB,
    #         error_msg=db.cfg.ERROR_51_901.replace("{file_name}", source_file_name)
    #         .replace("{error_no}", str(tet.get_errnum()))
    #         .replace("{api_name}", tet.get_apiname() + "()")
    #         .replace("{error}", tet.get_errmsg()),
    #     )
    #     return

    # get number of pages in the document */
    no_pages = tet.pcos_get_number(source_file, "length:pages")

    # loop over pages in the document */
    for page_no in range(1, int(no_pages) + 1):
        tet.process_page(source_file, page_no, libs.cfg.TET_PAGE_OPT_LIST)

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

    # Text and metadata from Document successfully extracted to xml format
    libs.utils.finalize_file_processing()
    # not testable
    # except TETException:
    #     libs.utils.report_document_error(
    #         document_id = libs.cfg.document_id,
    #         error_code=db.cfg.DOCUMENT_ERROR_CODE_REJ_PDFLIB,
    #         error_msg=db.cfg.ERROR_51_903.replace("{file_name}", source_file_name)
    #         .replace("{target_file}", target_file_name)
    #         .replace("{error_no}", str(tet.get_errnum()))
    #         .replace("{api_name}", tet.get_apiname() + "()")
    #         .replace("{error}", tet.get_errmsg()),
    #     )
    # not testable
    # finally:
    if tet:
        tet.delete()