"""Module libs.pandoc: Convert non-pdf documents to pdf files."""
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

    with libs.db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, libs.db.cfg.DOCUMENT_NEXT_STEP_PANDOC)

        for row in rows:
            libs.utils.start_document_processing(row, libs.db.cfg.JOURNAL_ACTION_31_001)

            convert_non_pdf_2_pdf_file()

        conn.close()

    libs.utils.progress_msg(
        f"Number documents to be processed:  {libs.cfg.total_to_be_processed:6d}"
    )

    if libs.cfg.total_to_be_processed > 0:
        libs.utils.progress_msg(
            f"Number status pdflib_tet_ready:    {libs.cfg.total_status_ready:6d}"
        )
        libs.utils.progress_msg(
            f"Number status pdflib_tet_error:    {libs.cfg.total_status_error:6d}"
        )
        libs.utils.progress_msg(
            f"Number documents converted:        {libs.cfg.total_ok_processed:6d}"
        )
        libs.utils.progress_msg(f"Number documents erroneous:        {libs.cfg.total_erroneous:6d}")
        libs.utils.progress_msg(
            "The involved documents in the file directory "
            + "'inbox_accepted' are converted to a pdf format "
            + "for further processing",
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert non-pdf documents to pdf files (step: n_2_p).
# -----------------------------------------------------------------------------
def convert_non_pdf_2_pdf_file() -> None:
    """Convert scanned image pdf documents to image files."""
    source_file = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    target_file = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_stem_name + "." + libs.db.cfg.DOCUMENT_FILE_TYPE_PDF,
    )

    # Convert the document
    output = pypandoc.convert_file(
        source_file, libs.db.cfg.DOCUMENT_FILE_TYPE_PDF, outputfile=target_file
    )

    if output != "":
        libs.cfg.total_erroneous += 1

        libs.db.orm.update_document_status(
            {
                libs.db.cfg.DBC_ERROR_CODE: libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PANDOC,
                libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_ERROR,
            },
            libs.db.orm.insert_journal(
                __name__,
                inspect.stack()[0][3],
                libs.cfg.document_id,
                libs.db.cfg.JOURNAL_ACTION_31_901.replace("{source_file}", source_file)
                .replace("{target_file}", target_file)
                .replace("{output}", output),
            ),
        )
    else:
        prepare_document_pandoc()

        libs.cfg.document_child_file_name = target_file
        libs.cfg.document_child_stem_name = libs.cfg.document_stem_name

        journal_action: str = libs.db.cfg.JOURNAL_ACTION_31_003.replace(
            "{file_name}", libs.cfg.document_child_file_name
        )

        libs.utils.initialise_document_child(journal_action)

        # Document successfully converted to pdf format
        journal_action = libs.db.cfg.JOURNAL_ACTION_31_002.replace(
            "{source_file}", source_file
        ).replace(f"{target_file}", target_file)

        libs.utils.finalize_file_conversion(journal_action)


# -----------------------------------------------------------------------------
# Prepare the base child document data - pandoc.
# -----------------------------------------------------------------------------
def prepare_document_pandoc() -> None:
    """Prepare the child document data - Pandoc."""
    libs.cfg.document_child_child_no = None
    libs.cfg.document_child_directory_name = libs.cfg.document_directory_name
    libs.cfg.document_child_directory_type = libs.cfg.document_directory_type
    libs.cfg.document_child_error_code = None

    libs.cfg.document_child_file_type = libs.db.cfg.DOCUMENT_FILE_TYPE_PDF

    libs.cfg.document_child_id_base = libs.cfg.document_id_base
    libs.cfg.document_child_id_parent = libs.cfg.document_id

    libs.cfg.document_child_next_step = libs.db.cfg.DOCUMENT_NEXT_STEP_PDFLIB
    libs.cfg.document_child_status = libs.db.cfg.DOCUMENT_STATUS_START
