"""Module libs.tesseractdcr: Convert image documents to pdf files."""
import inspect
import os

import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.utils
import pytesseract
from pytesseract import TesseractError


# -----------------------------------------------------------------------------
# Convert image documents to pdf files (step: ocr).
# -----------------------------------------------------------------------------
def convert_image_2_pdf() -> None:
    """Convert image documents to pdf files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = libs.utils.select_document_prepare()

    libs.utils.reset_statistics_total()

    with libs.db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, libs.db.cfg.DOCUMENT_NEXT_STEP_TESSERACT)

        for row in rows:
            libs.utils.start_document_processing(
                module_name=__name__,
                function_name=inspect.stack()[0][3],
                document=row,
                journal_action=libs.db.cfg.JOURNAL_ACTION_41_001,
            )

            convert_image_2_pdf_file()

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert image documents to pdf files (step: ocr).
# -----------------------------------------------------------------------------
def convert_image_2_pdf_file() -> None:
    """Convert scanned image pdf documents to image files."""
    source_file_name, target_file_name = libs.utils.prepare_file_names()

    if os.path.exists(target_file_name):
        libs.utils.report_document_error(
            module_name=__name__,
            function_name=inspect.stack()[0][3],
            error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            journal_action=libs.db.cfg.JOURNAL_ACTION_41_903.replace(
                "{file_name}", target_file_name
            ),
        )
        return

    # Convert the document
    try:
        pdf = pytesseract.image_to_pdf_or_hocr(
            source_file_name, extension="pdf", timeout=libs.cfg.tesseract_timeout
        )
        with open(target_file_name, "w+b") as target_file:
            # pdf type is bytes by default
            target_file.write(pdf)

        libs.utils.prepare_document_4_next_step(
            next_file_type=libs.db.cfg.DOCUMENT_FILE_TYPE_PDF,
            next_step=libs.db.cfg.DOCUMENT_NEXT_STEP_PDFLIB,
        )

        libs.cfg.document_child_file_name = (
            libs.cfg.document_stem_name + "." + libs.db.cfg.DOCUMENT_FILE_TYPE_PDF
        )
        libs.cfg.document_child_stem_name = libs.cfg.document_stem_name

        journal_action: str = libs.db.cfg.JOURNAL_ACTION_41_003.replace(
            "{file_name}", libs.cfg.document_child_file_name
        )

        libs.utils.initialise_document_child(journal_action)

        # Document successfully converted to pdf format
        libs.utils.finalize_file_processing(
            module_name=__name__,
            function_name=inspect.stack()[0][3],
            journal_action=libs.db.cfg.JOURNAL_ACTION_41_002.replace(
                "{source_file}", source_file_name
            ).replace("{target_file}", target_file_name),
        )
    except TesseractError as err_t:
        libs.utils.report_document_error(
            module_name=__name__,
            function_name=inspect.stack()[0][3],
            error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_TESSERACT,
            journal_action=libs.db.cfg.JOURNAL_ACTION_41_902.replace(
                "{source_file}", source_file_name
            )
            .replace("{target_file}", target_file_name)
            .replace("{error_status}", str(err_t.status))
            .replace("{error}", err_t.message),
        )
    except RuntimeError as err:
        libs.utils.report_document_error(
            module_name=__name__,
            function_name=inspect.stack()[0][3],
            error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_TESSERACT,
            journal_action=libs.db.cfg.JOURNAL_ACTION_41_901.replace(
                "{source_file}", source_file_name
            )
            .replace("{target_file}", target_file_name)
            .replace("{type_error}", str(type(err)))
            .replace("{error}", str(err)),
        )
