# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module nlp.parser: Store the document structure from the parser result."""
import os
import time

import dcr_core.cls_nlp_core
import dcr_core.cls_text_parser
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
TETML_TYPE_LINE = "line"
TETML_TYPE_PAGE = "page"
TETML_TYPE_WORD = "word"


# -----------------------------------------------------------------------------
# Parse the TETML files (step: s_p_j).
# -----------------------------------------------------------------------------
def parse_tetml() -> None:
    """Parse the TETML files.

    TBD
    """
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    for (tetml_type, action_code, is_parsing_line, is_parsing_page, is_parsing_word,) in (
        (
            TETML_TYPE_LINE,
            dcr.db.cls_run.Run.ACTION_CODE_PARSER_LINE,
            True,
            False,
            False,
        ),
        (
            TETML_TYPE_PAGE,
            dcr.db.cls_run.Run.ACTION_CODE_PARSER_PAGE,
            False,
            True,
            False,
        ),
        (
            TETML_TYPE_WORD,
            dcr.db.cls_run.Run.ACTION_CODE_PARSER_WORD,
            False,
            False,
            True,
        ),
    ):
        dcr.utils.progress_msg(f"Start of processing for tetml type '{tetml_type}'")

        dcr_core.core_glob.setup.is_parsing_line = is_parsing_line
        dcr_core.core_glob.setup.is_parsing_page = is_parsing_page
        dcr_core.core_glob.setup.is_parsing_word = is_parsing_word

        with dcr.cfg.glob.db_core.db_orm_engine.begin() as conn:
            rows = dcr.db.cls_action.Action.select_action_by_action_code(conn=conn, action_code=action_code)

            for row in rows:
                # ------------------------------------------------------------------
                # Processing a single document
                # ------------------------------------------------------------------
                dcr.cfg.glob.start_time_document = time.perf_counter_ns()

                dcr.cfg.glob.run.run_total_processed_to_be += 1

                dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_row(row)

                if dcr.cfg.glob.action_curr.action_status == dcr.db.cls_document.Document.DOCUMENT_STATUS_ERROR:
                    dcr.cfg.glob.run.total_status_error += 1
                else:
                    dcr.cfg.glob.run.total_status_ready += 1

                dcr.cfg.glob.document = dcr.db.cls_document.Document.from_id(id_document=dcr.cfg.glob.action_curr.action_id_document)

                parse_tetml_file()

            conn.close()
        dcr.utils.progress_msg(f"End   of processing for tetml type '{tetml_type}'")

    dcr.utils.show_statistics_total()

    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Parse the TETML file (step: s_p_j).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def parse_tetml_file() -> None:
    """Parse the TETML file.

    TBD
    """
    full_name_curr = dcr.cfg.glob.action_curr.get_full_name()

    file_name_next = dcr.cfg.glob.action_curr.get_stem_name() + "." + dcr_core.core_glob.FILE_TYPE_JSON
    full_name_next = dcr_core.core_utils.get_full_name(
        dcr.cfg.glob.action_curr.action_directory_name,
        file_name_next,
    )

    if dcr_core.core_glob.setup.is_parsing_line:
        status = dcr.db.cls_document.Document.DOCUMENT_STATUS_START
    else:
        status = dcr.db.cls_document.Document.DOCUMENT_STATUS_END

    dcr.cfg.glob.action_next = dcr.db.cls_action.Action(
        action_code=dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE,
        id_run_last=dcr.cfg.glob.run.run_id,
        directory_name=dcr.cfg.glob.action_curr.action_directory_name,
        directory_type=dcr.cfg.glob.action_curr.action_directory_type,
        file_name=file_name_next,
        id_document=dcr.cfg.glob.action_curr.action_id_document,
        id_parent=dcr.cfg.glob.action_curr.action_id,
        no_pdf_pages=dcr.cfg.glob.action_curr.action_no_pdf_pages,
        status=status,
    )

    (error_code, error_msg) = dcr_core.processing.parser_process(
        full_name_in=dcr.cfg.glob.action_curr.get_full_name(),
        full_name_out=dcr.cfg.glob.action_next.get_full_name(),
        document_id=dcr.cfg.glob.action_curr.action_id_document,
        file_name_orig=dcr.cfg.glob.document.document_file_name,
        no_pdf_pages=dcr.cfg.glob.action_curr.action_no_pdf_pages,
    )
    if (error_code, error_msg) != dcr_core.core_glob.RETURN_OK:
        dcr.cfg.glob.action_curr.finalise_error(error_code, error_msg)
        return

    dcr.cfg.glob.run.run_total_processed_ok += 1

    if dcr_core.core_glob.setup.is_parsing_line:
        if (
            dcr_core.core_glob.line_type_headers_footers.no_lines_footer != 0  # pylint: disable=too-many-boolean-expressions
            or dcr_core.core_glob.line_type_headers_footers.no_lines_header != 0
            or dcr_core.core_glob.line_type_list_bullet.no_lists != 0
            or dcr_core.core_glob.line_type_list_number.no_lists != 0
            or dcr_core.core_glob.line_type_table.no_tables != 0
            or dcr_core.core_glob.line_type_toc.no_lines_toc != 0
        ):
            dcr.cfg.glob.document.document_no_lines_footer = dcr_core.core_glob.line_type_headers_footers.no_lines_footer
            dcr.cfg.glob.document.document_no_lines_header = dcr_core.core_glob.line_type_headers_footers.no_lines_header
            dcr.cfg.glob.document.document_no_lines_toc = dcr_core.core_glob.line_type_toc.no_lines_toc
            dcr.cfg.glob.document.document_no_lists_bullet = dcr_core.core_glob.line_type_list_bullet.no_lists
            dcr.cfg.glob.document.document_no_lists_number = dcr_core.core_glob.line_type_list_number.no_lists
            dcr.cfg.glob.document.document_no_tables = dcr_core.core_glob.line_type_table.no_tables
            dcr.cfg.glob.document.persist_2_db()  # type: ignore

    dcr.cfg.glob.action_next.action_file_size_bytes = (os.path.getsize(full_name_next),)

    dcr.cfg.glob.action_curr.finalise()

    dcr.utils.delete_auxiliary_file(full_name_curr)
