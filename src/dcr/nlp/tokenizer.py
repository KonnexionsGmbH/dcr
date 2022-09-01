# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module nlp.cls_tokenizer: Store the document tokens page by page in the
database."""

import time

import dcr_core.cls_nlp_core
import dcr_core.cls_process
import dcr_core.cls_text_parser
import dcr_core.cls_tokenizer_spacy
import dcr_core.core_glob
import dcr_core.core_utils

import dcr.cfg.glob
import dcr.db.cls_action
import dcr.db.cls_db_core
import dcr.db.cls_document
import dcr.db.cls_language
import dcr.db.cls_run
import dcr.db.cls_token
import dcr.utils


# -----------------------------------------------------------------------------
# Save the tokens sentence by sentence in the database.
# -----------------------------------------------------------------------------
def store_tokens_in_database() -> None:
    """Save the tokens sentence by sentence in the database."""
    # not testable
    if not dcr_core.core_glob.setup.is_tokenize_2_database:
        return

    for page in dcr_core.core_glob.tokenizer_spacy.token_pages:
        page_no = page[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]
        paras = page[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARAS]
        for para in paras:
            para_no = para[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]
            sents = para[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_SENTS]
            for sent in sents:
                if dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO in sent:
                    column_no = sent[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO]
                    row_no = sent[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO]
                else:
                    column_no = 0
                    row_no = 0

                if dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN in sent:
                    column_span = sent[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN]
                else:
                    column_span = 0

                dcr.db.cls_token.Token(
                    id_document=dcr.cfg.glob.document.document_id,
                    column_no=column_no,
                    column_span=column_span,
                    coord_llx=sent[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX],
                    coord_urx=sent[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX],
                    line_type=sent[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE],
                    no_tokens_in_sent=sent[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT],
                    page_no=page_no,
                    para_no=para_no,
                    row_no=row_no,
                    sent_no=sent[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_SENT_NO],
                    text=sent[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT],
                    tokens=sent[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TOKENS],  # type: ignore
                )


# -----------------------------------------------------------------------------
# Create document tokens (step: tkn).
# -----------------------------------------------------------------------------
def tokenize() -> None:
    """Create document tokens (step: tkn).

    TBD
    """
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    dcr_core.core_glob.tokenizer_spacy = dcr_core.cls_tokenizer_spacy.TokenizerSpacy()

    with dcr.cfg.glob.db_core.db_orm_engine.begin() as conn:
        rows = dcr.db.cls_action.Action.select_action_by_action_code(conn=conn, action_code=dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE)

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

            tokenize_file()

        conn.close()

    dcr.utils.show_statistics_total()

    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the tokens of a document page by page (step: tkn).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def tokenize_file() -> None:
    """Create the tokens of a document page by page.

    TBD
    """
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    dcr.cfg.glob.document = dcr.db.cls_document.Document.from_id(id_document=dcr.cfg.glob.action_curr.action_id_document)

    pipeline_name = dcr.db.cls_language.Language.LANGUAGES_SPACY[dcr.cfg.glob.document.document_id_language]

    full_name_curr = dcr.cfg.glob.action_curr.get_full_name()

    if dcr_core.core_glob.setup.is_tokenize_2_jsonfile:
        file_name_next = dcr.cfg.glob.action_curr.get_stem_name() + "_token." + dcr_core.core_glob.FILE_TYPE_JSON
        full_name_next = dcr_core.core_utils.get_full_name_from_components(
            dcr.cfg.glob.action_curr.action_directory_name,
            file_name_next,
        )
    else:
        full_name_next = ""

    (error_code, error_msg) = dcr_core.cls_process.Process.tokenizer(
        full_name_in=full_name_curr,
        full_name_out=full_name_next,
        document_id=dcr.cfg.glob.document.document_id,
        full_name_orig=dcr.cfg.glob.document.document_file_name,
        no_lines_footer=dcr.cfg.glob.document.document_no_lines_footer,
        no_lines_header=dcr.cfg.glob.document.document_no_lines_header,
        no_lines_toc=dcr.cfg.glob.document.document_no_lines_toc,
        pipeline_name=pipeline_name,
    )
    if (error_code, error_msg) != dcr_core.core_glob.RETURN_OK:
        dcr.cfg.glob.action_curr.finalise_error(error_code, error_msg)
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
        return

    store_tokens_in_database()

    dcr.utils.delete_auxiliary_file(full_name_curr)

    dcr.cfg.glob.action_curr.finalise()

    dcr.cfg.glob.run.run_total_processed_ok += 1

    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
