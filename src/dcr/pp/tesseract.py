# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module pp.tesseract: Convert image files to pdf documents."""
import os
import time

import dcr_core.core_glob
import dcr_core.core_utils
import dcr_core.processing

import dcr.cfg.glob
import dcr.db.cls_action
import dcr.db.cls_document
import dcr.db.cls_language
import dcr.db.cls_run
import dcr.utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_41_903 = "41.903 Issue (ocr): The target file '{full_name}' already exists."
ERROR_41_904 = "41.904 Issue (pypdf2): The target file '{full_name}' already exists."


# -----------------------------------------------------------------------------
# Convert image files to pdf documents (step: ocr).
# -----------------------------------------------------------------------------
def convert_image_2_pdf() -> None:
    """Convert image files to pdf documents.

    TBD
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    with dcr.cfg.glob.db_core.db_orm_engine.begin() as conn:
        rows = dcr.db.cls_action.Action.select_action_by_action_code(conn=conn, action_code=dcr.db.cls_run.Run.ACTION_CODE_TESSERACT)

        for row in rows:
            dcr.cfg.glob.start_time_document = time.perf_counter_ns()

            dcr.cfg.glob.run.run_total_processed_to_be += 1

            dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_row(row)

            if dcr.cfg.glob.action_curr.action_status == dcr.db.cls_document.Document.DOCUMENT_STATUS_ERROR:
                dcr.cfg.glob.run.total_status_error += 1
            else:
                dcr.cfg.glob.run.total_status_ready += 1

            dcr.cfg.glob.document = dcr.db.cls_document.Document.from_id(id_document=dcr.cfg.glob.action_curr.action_id_document)

            convert_image_2_pdf_file()

        conn.close()

    dcr.utils.show_statistics_total()

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Convert image files to pdf documents (step: ocr).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def convert_image_2_pdf_file() -> None:
    """Convert scanned image pdf documents to image files."""
    full_name_curr = dcr.cfg.glob.action_curr.get_full_name()

    file_name_next = dcr.cfg.glob.action_curr.get_stem_name().replace("[0-9]*", "0") + "." + dcr_core.core_glob.FILE_TYPE_PDF
    full_name_next = dcr_core.core_utils.get_full_name(
        dcr.cfg.glob.action_curr.action_directory_name,
        file_name_next,
    )

    if os.path.exists(full_name_next):
        dcr.cfg.glob.action_curr.finalise_error(
            error_code=dcr.db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=ERROR_41_903.replace("{full_name}", full_name_next),
        )
        return

    (error_code, error_msg, children) = dcr_core.processing.tesseract_process(
        full_name_in=full_name_curr,
        full_name_out=full_name_next,
        language_tesseract=dcr.db.cls_language.Language.LANGUAGES_TESSERACT[dcr.cfg.glob.document.document_id_language],
    )
    if error_code != dcr_core.core_glob.RETURN_OK[0]:
        dcr.cfg.glob.action_curr.finalise_error(error_code, error_msg)
        return

    for full_name in children:
        dcr.utils.delete_auxiliary_file(full_name)

    dcr.cfg.glob.action_curr.finalise()

    dcr.cfg.glob.action_next = dcr.db.cls_action.Action(
        action_code=dcr.db.cls_run.Run.ACTION_CODE_PDFLIB,
        id_run_last=dcr.cfg.glob.run.run_id,
        directory_name=dcr.cfg.glob.action_curr.action_directory_name,
        directory_type=dcr.cfg.glob.action_curr.action_directory_type,
        file_name=file_name_next,
        file_size_bytes=os.path.getsize(full_name_next),
        id_document=dcr.cfg.glob.action_curr.action_id_document,
        id_parent=dcr.cfg.glob.action_curr.action_id,
        no_pdf_pages=dcr.utils.get_pdf_pages_no(full_name_next),
    )

    dcr.cfg.glob.run.run_total_processed_ok += len(children)
