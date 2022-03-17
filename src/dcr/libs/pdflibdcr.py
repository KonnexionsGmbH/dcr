"""Module libs.pdflibdcr: Extract the text from pdf documents."""
import inspect
import os

import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.utils
import tetlib_py
from PDFlib.TET import TET


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
    source_file_name, target_file_name = libs.utils.prepare_file_names(
        libs.db.cfg.DOCUMENT_FILE_TYPE_TXT
    )

    tet = None

    try:
        tet = TET()

        with open(target_file_name, "w", 2, "utf-8") as target_file:
            source_file = tet.open_document(source_file_name, "")

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
                        libs.db.cfg.JOURNAL_ACTION_51_902.replace("{file_name}", target_file_name)
                        .replace("{err_num}", repr(tet.get_errnum()))
                        .replace("{api_name}", tet.get_apiname() + "()")
                        .replace("{err_msg}", tet.get_errmsg()),
                    ),
                )
                return

            # get number of pages in the document */
            no_pages = tet.pcos_get_number(source_file, "length:pages")

            # loop over pages in the document */
            for page_no in range(1, int(no_pages) + 1):
                page = tet.open_page(source_file, page_no, "granularity=page")

                if page == -1:
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
                            libs.db.cfg.JOURNAL_ACTION_51_903.replace(
                                "{file_name}", source_file_name
                            )
                            .replace("{err_num}", repr(tet.get_errnum()))
                            .replace("{api_name}", tet.get_apiname() + "()")
                            .replace("{err_msg}", tet.get_errmsg()),
                        ),
                    )
                    return

                # Retrieve all text fragments; This is actually not required
                # for granularity=page, but must be used for other granularities.
                text = tet.get_text(page)

                while text is not None:
                    target_file.write(text)  # print the retrieved text

                    # print a separator between chunks of text
                    target_file.write(os.linesep)

                    text = tet.get_text(page)

                if tet.get_errnum() != 0:
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
                            libs.db.cfg.JOURNAL_ACTION_51_904.replace(
                                "{file_name}", source_file_name
                            )
                            .replace("{page_no}", repr(page_no))
                            .replace("{err_num}", repr(tet.get_errnum()))
                            .replace("{api_name}", tet.get_apiname() + "()")
                            .replace("{err_msg}", tet.get_errmsg()),
                        ),
                    )
                    return

                tet.close_page(page)

            tet.close_document(source_file)

            prepare_document_4_parser()

            libs.cfg.document_child_file_name = (
                libs.cfg.document_stem_name + "." + libs.db.cfg.DOCUMENT_FILE_TYPE_TXT
            )
            libs.cfg.document_child_stem_name = libs.cfg.document_stem_name

            journal_action: str = libs.db.cfg.JOURNAL_ACTION_51_003.replace(
                "{file_name}", libs.cfg.document_child_file_name
            )

            libs.utils.initialise_document_child(journal_action)

            # Text from Document successfully extracted to txt format
            journal_action = libs.db.cfg.JOURNAL_ACTION_51_002.replace(
                "{source_file}", source_file_name
            ).replace("{target_file}", target_file_name)

            libs.utils.finalize_file_conversion(journal_action)
    except tetlib_py.TETException as err:
        libs.cfg.total_erroneous += 1

        if page_no == 0:
            libs.db.orm.update_document_status(
                {
                    libs.db.cfg.DBC_ERROR_CODE: libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PDFLIB,
                    libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
                },
                libs.db.orm.insert_journal(
                    __name__,
                    inspect.stack()[0][3],
                    libs.cfg.document_id,
                    libs.db.cfg.JOURNAL_ACTION_51_905.replace("{file_name}", source_file_name)
                    .replace("{target_name}", target_file_name)
                    .replace("{err_num}", repr(err.errnum()))
                    .replace("{api_name}", err.apiname() + "()")
                    .replace("{err_msg}", err.errmsg()),
                ),
            )
        else:
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
                    .replace("{target_name}", target_file_name)
                    .replace("{page_no}", repr(page_no))
                    .replace("{err_num}", repr(err.errnum()))
                    .replace("{api_name}", err.apiname() + "()")
                    .replace("{err_msg}", err.errmsg()),
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
