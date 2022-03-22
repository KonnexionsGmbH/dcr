"""Module libs.pandocdcr: Convert non-pdf documents to pdf files."""
import inspect
import os

import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.utils
import pypandoc


# -----------------------------------------------------------------------------
# Convert non-pdf documents to pdf files (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf() -> None:
    """Convert non-pdf documents to pdf files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = libs.utils.select_document_prepare()

    libs.utils.reset_statistics()

    with libs.db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, libs.db.cfg.DOCUMENT_NEXT_STEP_PANDOC)

        for row in rows:
            libs.utils.start_document_processing(
                module_name=__name__,
                function_name=inspect.stack()[0][3],
                document=row,
                journal_action=libs.db.cfg.JOURNAL_ACTION_31_001,
            )

            convert_non_pdf_2_pdf_file()

        conn.close()

    libs.utils.show_statistics()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert a non-pdf document to a pdf file (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf_file() -> None:
    """Convert a non-pdf document to a pdf file."""
    source_file_name, target_file_name = libs.utils.prepare_file_names()

    if os.path.exists(target_file_name):
        libs.utils.report_document_error(
            module_name=__name__,
            function_name=inspect.stack()[0][3],
            error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            journal_action=libs.db.cfg.JOURNAL_ACTION_31_903.replace(
                "{file_name}", target_file_name
            ),
        )
        return

    # Convert the document
    try:
        output = pypandoc.convert_file(
            source_file_name,
            libs.db.cfg.DOCUMENT_FILE_TYPE_PDF,
            extra_args=(["--pdf-engine=" + libs.cfg.PANDIOC_PDF_ENGINE_XELATEX]),
            outputfile=target_file_name,
        )

        # not testable
        if output != "":
            libs.utils.report_document_error(
                module_name=__name__,
                function_name=inspect.stack()[0][3],
                error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PANDOC,
                journal_action=libs.db.cfg.JOURNAL_ACTION_31_901.replace(
                    "{source_file}", source_file_name
                )
                .replace("{target_file}", target_file_name)
                .replace("{output}", output),
            )
        else:
            libs.utils.prepare_document_4_pdflib()

            libs.cfg.document_child_file_name = (
                libs.cfg.document_stem_name + "." + libs.db.cfg.DOCUMENT_FILE_TYPE_PDF
            )
            libs.cfg.document_child_stem_name = libs.cfg.document_stem_name

            journal_action: str = libs.db.cfg.JOURNAL_ACTION_31_003.replace(
                "{file_name}", libs.cfg.document_child_file_name
            )

            libs.utils.initialise_document_child(journal_action)

            # Document successfully converted to pdf format
            libs.utils.finalize_file_processing(
                module_name=__name__,
                function_name=inspect.stack()[0][3],
                journal_action=libs.db.cfg.JOURNAL_ACTION_31_002.replace(
                    "{source_file}", source_file_name
                ).replace("{target_file}", target_file_name),
            )
    # not testable
    except RuntimeError as err:
        libs.utils.report_document_error(
            module_name=__name__,
            function_name=inspect.stack()[0][3],
            error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE,
            journal_action=libs.db.cfg.JOURNAL_ACTION_31_902.replace(
                "{file_name}", source_file_name
            ).replace("{error_msg}", str(str(err).encode("utf-8"))),
        )
