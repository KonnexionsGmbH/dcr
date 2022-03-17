"""Module libs.pdflibdcr: Extract the text from pdf documents."""

import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.TET
import libs.utils

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
# global option list */
GLOBAL_OPT_LIST = "searchpath={{../data} {../../../resource/cmap}}"

# document-specific option list */
DOC_OPT_LIST = ""

# page-specific option list */
PAGE_OPT_LIST = "granularity=page"

# separator to emit after each chunk of text. This depends on the
# application's needs; for granularity=word a space character may be useful.
SEPARATOR = "\n"


# -----------------------------------------------------------------------------
# Extract the text from pdf documents (step: tet).
# -----------------------------------------------------------------------------
def extract_text_from_pdf() -> None:
    """Extract the text from pdf documents.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = libs.utils.select_document_prepare()

    libs.utils.reset_statistics()

    with libs.db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, libs.db.cfg.DOCUMENT_NEXT_STEP_PDFLIB)

        for row in rows:
            libs.utils.start_document_processing(row, libs.db.cfg.JOURNAL_ACTION_51_001)
            extract_text_from_pdf_file()

        conn.close()

    libs.utils.show_statistics()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract the text from a pdf document (step: tet).
# -----------------------------------------------------------------------------
def extract_text_from_pdf_file() -> None:
    """Extract the text from a pdf document."""
    tet = None

    # page_no = 0

    try:
        tet = libs.TET.TET()
    # except PDFlib.TETException as ex:
    #     if page_no == 0:
    #         print("Error %d in %s(): %s" % (ex.errnum, ex.apiname, ex.errmsg))
    #     else:
    #         print("Error %d in %s() on page %d: %s" % (ex.errnum, ex.apiname, page_no, ex.errmsg))
    finally:
        if tet:
            tet.delete()

    # file = open(os.path.join(
    #     libs.cfg.document_directory_name,
    #     libs.cfg.document_file_name,
    # ), 'w', 2, 'utf-8')
    #
    # # Convert the document
    # output = pypandoc.convert_file(
    #     source_file, libs.db.cfg.DOCUMENT_FILE_TYPE_PDF, outputfile=target_file
    # )
    #
    # # not testable
    # if output != "":
    #     libs.cfg.total_erroneous += 1
    #
    #     libs.db.orm.update_document_status(
    #         {
    #             libs.db.cfg.DBC_ERROR_CODE: libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PANDOC,
    #             libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
    #         },
    #         libs.db.orm.insert_journal(
    #             __name__,
    #             inspect.stack()[0][3],
    #             libs.cfg.document_id,
    #             libs.db.cfg.JOURNAL_ACTION_51_901.replace("{file_name}", source_file)
    #             .replace("{target_file}", target_file)
    #             .replace("{output}", output),
    #         ),
    #     )
    # else:
    #     libs.utils.prepare_document_4_pdflib()
    #
    #     libs.cfg.document_child_file_name = (
    #         libs.cfg.document_stem_name + "." + libs.db.cfg.DOCUMENT_FILE_TYPE_PDF
    #     )
    #     libs.cfg.document_child_stem_name = libs.cfg.document_stem_name
    #
    #     journal_action: str = libs.db.cfg.JOURNAL_ACTION_51_003.replace(
    #         "{file_name}", libs.cfg.document_child_file_name
    #     )
    #
    #     libs.utils.initialise_document_child(journal_action)
    #
    #     # Document successfully converted to pdf format
    #     journal_action = libs.db.cfg.JOURNAL_ACTION_51_002.replace("{file_name}", source_file)
    #
    #     libs.utils.finalize_file_conversion(journal_action)
