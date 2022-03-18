"""Module libs.pdflibdcr: Extract text and metadata from pdf documents."""
import inspect

import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.utils
from PDFlib.TET import TET
from tetlib_py import TETException

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
# document-specific option list
BASE_DOC_OPT_LIST = "engines={notextcolor}"

# global option list */
GLOBAL_OPT_LIST = ""

# page-specific option list */
PAGE_OPT_LIST = "granularity=word tetml={elements={line}}"


# -----------------------------------------------------------------------------
# Extract text and metadata from pdf documents (step: tet).
# -----------------------------------------------------------------------------
def extract_text_from_pdf() -> None:
    """Extract text and metadata  from pdf documents.

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
# Extract text and metadata  from a pdf document (step: tet).
# -----------------------------------------------------------------------------
def extract_text_from_pdf_file() -> None:
    """Extract text and metadata  from a pdf document."""
    source_file_name, target_file_name = libs.utils.prepare_file_names(
        libs.db.cfg.DOCUMENT_FILE_TYPE_XML
    )

    tet = None

    try:
        tet = TET()

        tet.set_option(GLOBAL_OPT_LIST)

        doc_opt_list = f"tetml={{filename={{{target_file_name}}}}} {BASE_DOC_OPT_LIST}"

        print("wwe doc_opt_list=",doc_opt_list)

        source_file = tet.open_document(source_file_name, doc_opt_list)

        # not testable
        if source_file == -1:
            libs.cfg.total_erroneous += 1

            libs.db.orm.update_document_status(
                {
                    libs.db.cfg.DBC_ERROR_CODE: libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PDFLIB,
                    libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
                },
                libs.db.orm.insert_journal(
                    __name__,
                    inspect.stack()[0][3],
                    libs.cfg.document_id,
                    libs.db.cfg.JOURNAL_ACTION_51_901.replace("{file_name}", source_file_name)
                    .replace("{error_no}", str(tet.get_errnum()))
                    .replace("{api_name}", tet.get_apiname() + "()")
                    .replace("{error}", tet.get_errmsg()),
                ),
            )
            return

        # get number of pages in the document */
        no_pages = tet.pcos_get_number(source_file, "length:pages")

        # loop over pages in the document */
        for page_no in range(1, int(no_pages) + 1):
            tet.process_page(source_file, page_no, PAGE_OPT_LIST)

        # This could be combined with the last page-related call
        tet.process_page(source_file, 0, "tetml={trailer}")

        tet.close_document(source_file)

        prepare_document_4_parser()

        libs.cfg.document_child_file_name = (
            libs.cfg.document_stem_name + "." + libs.db.cfg.DOCUMENT_FILE_TYPE_XML
        )
        libs.cfg.document_child_stem_name = libs.cfg.document_stem_name

        journal_action: str = libs.db.cfg.JOURNAL_ACTION_51_003.replace(
            "{file_name}", libs.cfg.document_child_file_name
        )

        libs.utils.initialise_document_child(journal_action)

        # Text and metadata from Document successfully extracted to xml format
        journal_action = libs.db.cfg.JOURNAL_ACTION_51_002.replace(
            "{source_file}", source_file_name
        ).replace("{target_file}", target_file_name)

        libs.utils.finalize_file_conversion(journal_action)
    except TETException:
        # not testable
        libs.cfg.total_erroneous += 1

        libs.db.orm.update_document_status(
            {
                libs.db.cfg.DBC_ERROR_CODE: libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PDFLIB,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
            },
            libs.db.orm.insert_journal(
                __name__,
                inspect.stack()[0][3],
                libs.cfg.document_id,
                libs.db.cfg.JOURNAL_ACTION_51_903.replace("{file_name}", source_file_name)
                .replace("{target_file}", target_file_name)
                .replace("{error_no}", str(tet.get_errnum()))
                .replace("{api_name}", tet.get_apiname() + "()")
                .replace("{error}", tet.get_errmsg()),
            ),
        )
    finally:
        if tet:
            tet.delete()


# -----------------------------------------------------------------------------
# Prepare the text document data - next step Parser.
# -----------------------------------------------------------------------------
def prepare_document_4_parser() -> None:
    """Prepare the text document data - next step Parser."""
    libs.utils.prepare_document_4_parser_tesseract()

    libs.cfg.document_child_next_step = libs.db.cfg.DOCUMENT_NEXT_STEP_PARSER
    libs.cfg.document_child_status = libs.db.cfg.DOCUMENT_STATUS_START
