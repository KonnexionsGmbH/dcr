# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module nlp.pdflib: Extract text from pdf documents."""
import os
import time

import dcr_core.core_glob
import dcr_core.core_utils
import dcr_core.processing

import dcr.cfg.glob
import dcr.db.cls_action
import dcr.db.cls_document
import dcr.db.cls_run
import dcr.utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_51_904 = "51.904 Issue (pdflib): The target file '{full_name}' already exists."

LINE_TET_DOCUMENT_OPT_LIST = "engines={noannotation noimage text notextcolor novector}"
LINE_TET_PAGE_OPT_LIST = "granularity=line"
LINE_XML_VARIATION = "line."

PAGE_TET_DOCUMENT_OPT_LIST = "engines={noannotation noimage text notextcolor novector} " + "lineseparator=U+0020"
PAGE_TET_PAGE_OPT_LIST = "granularity=page"
PAGE_XML_VARIATION = "page."

WORD_TET_DOCUMENT_OPT_LIST = "engines={noannotation noimage text notextcolor novector}"
WORD_TET_PAGE_OPT_LIST = "granularity=word tetml={elements={line}}"
WORD_XML_VARIATION = "word."


# -----------------------------------------------------------------------------
# Extract text from pdf documents (step: tet).
# -----------------------------------------------------------------------------
def extract_text_from_pdf() -> None:
    """Extract text from pdf documents.

    TBD
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    with dcr.cfg.glob.db_core.db_orm_engine.begin() as conn:
        rows = dcr.db.cls_action.Action.select_action_by_action_code(conn=conn, action_code=dcr.db.cls_run.Run.ACTION_CODE_PDFLIB)

        for row in rows:
            dcr.cfg.glob.start_time_document = time.perf_counter_ns()

            dcr.cfg.glob.run.run_total_processed_to_be += 1

            dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_row(row)

            if dcr.cfg.glob.action_curr.action_status == dcr.db.cls_document.Document.DOCUMENT_STATUS_ERROR:
                dcr.cfg.glob.run.total_status_error += 1
            else:
                dcr.cfg.glob.run.total_status_ready += 1

            dcr.cfg.glob.document = dcr.db.cls_document.Document.from_id(id_document=dcr.cfg.glob.action_curr.action_id_document)

            is_no_error = extract_text_from_pdf_file(
                document_opt_list=LINE_TET_DOCUMENT_OPT_LIST,
                page_opt_list=LINE_TET_PAGE_OPT_LIST,
                xml_variation=LINE_XML_VARIATION,
            )

            if dcr_core.core_glob.setup.is_tetml_page:
                if is_no_error:
                    is_no_error = extract_text_from_pdf_file(
                        document_opt_list=PAGE_TET_DOCUMENT_OPT_LIST,
                        page_opt_list=PAGE_TET_PAGE_OPT_LIST,
                        xml_variation=PAGE_XML_VARIATION,
                    )

            if dcr_core.core_glob.setup.is_tetml_word:
                if is_no_error:
                    is_no_error = extract_text_from_pdf_file(
                        document_opt_list=WORD_TET_DOCUMENT_OPT_LIST,
                        page_opt_list=WORD_TET_PAGE_OPT_LIST,
                        xml_variation=WORD_XML_VARIATION,
                    )

            if is_no_error:
                dcr.utils.delete_auxiliary_file(dcr.cfg.glob.action_curr.get_full_name())

                dcr.cfg.glob.action_curr.finalise()

                dcr.cfg.glob.run.run_total_processed_ok += 1

        conn.close()

    dcr.utils.show_statistics_total()

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Extract text from a pdf document (step: tet).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def extract_text_from_pdf_file(document_opt_list: str, page_opt_list: str, xml_variation: str) -> bool:
    """Extract text from a pdf document (step: tet) - method line."""
    full_name_curr = dcr.cfg.glob.action_curr.get_full_name()

    file_name_next = dcr.cfg.glob.action_curr.get_stem_name() + "." + xml_variation + dcr_core.core_glob.FILE_TYPE_XML
    full_name_next = dcr_core.core_utils.get_full_name(
        dcr.cfg.glob.action_curr.action_directory_name,
        file_name_next,
    )

    if os.path.exists(full_name_next):
        dcr.cfg.glob.action_curr.finalise_error(
            error_code=dcr.db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_FILE_DUPL,
            error_msg=ERROR_51_904.replace("{full_name}", full_name_next),
        )

        return False

    (error_code, error_msg) = dcr_core.processing.pdflib_process(
        full_name_in=full_name_curr,
        full_name_out=full_name_next,
        document_opt_list=document_opt_list,
        page_opt_list=page_opt_list,
    )
    if (error_code, error_msg) != dcr_core.core_glob.RETURN_OK:
        dcr.cfg.glob.action_curr.finalise_error(error_code, error_msg)
        return False

    if xml_variation == LINE_XML_VARIATION:
        action_code = dcr.db.cls_run.Run.ACTION_CODE_PARSER_LINE
    elif xml_variation == PAGE_XML_VARIATION:
        action_code = dcr.db.cls_run.Run.ACTION_CODE_PARSER_PAGE
    else:
        action_code = dcr.db.cls_run.Run.ACTION_CODE_PARSER_WORD

    dcr.db.cls_action.Action(
        action_code=action_code,
        id_run_last=dcr.cfg.glob.run.run_id,
        directory_name=dcr.cfg.glob.action_curr.action_directory_name,
        directory_type=dcr.cfg.glob.action_curr.action_directory_type,
        file_name=file_name_next,
        file_size_bytes=os.path.getsize(full_name_next),
        id_document=dcr.cfg.glob.action_curr.action_id_document,
        id_parent=dcr.cfg.glob.action_curr.action_id,
        no_pdf_pages=dcr.cfg.glob.action_curr.action_no_pdf_pages,
        status=dcr.db.cls_document.Document.DOCUMENT_STATUS_START,
    )

    return True
