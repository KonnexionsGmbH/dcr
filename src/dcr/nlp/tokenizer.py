"""Module nlp.cls_tokenizer: Store the document tokens page by page in the
database."""

import time

import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_language
import db.cls_run
import utils

import dcr_core.cfg.glob
import dcr_core.nlp.cls_text_parser
import dcr_core.nlp.cls_tokenizer_spacy
import dcr_core.utils

# -----------------------------------------------------------------------------
# Global constants.
# -----------------------------------------------------------------------------
ERROR_71_901 = "71.901 Issue (tkn): Tokenizing the file '{full_name_curr}' failed - " + "error type: '{error_type}' - error: '{error}'."


# -----------------------------------------------------------------------------
# Create document tokens (step: tkn).
# -----------------------------------------------------------------------------
def tokenize() -> None:
    """Create document tokens (step: tkn).

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    cfg.glob.tokenizer_spacy = dcr_core.nlp.cls_tokenizer_spacy.TokenizerSpacy()

    with cfg.glob.db_core.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(conn=conn, action_code=db.cls_run.Run.ACTION_CODE_TOKENIZE)

        for row in rows:
            # ------------------------------------------------------------------
            # Processing a single document
            # ------------------------------------------------------------------
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_row(row)

            if cfg.glob.action_curr.action_status == db.cls_document.Document.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                cfg.glob.run.total_status_ready += 1

            tokenize_file()

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the tokens of a document page by page (step: tkn).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def tokenize_file() -> None:
    """Create the tokens of a document page by page.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    cfg.glob.document = db.cls_document.Document.from_id(id_document=cfg.glob.action_curr.action_id_document)

    pipeline_name = db.cls_language.Language.LANGUAGES_SPACY[cfg.glob.document.document_id_language]

    full_name_curr = cfg.glob.action_curr.get_full_name()

    if cfg.glob.setup.is_tokenize_2_jsonfile:
        file_name_next = cfg.glob.action_curr.get_stem_name() + "_token." + dcr_core.cfg.glob.FILE_TYPE_JSON
        full_name_next = dcr_core.utils.get_full_name(
            cfg.glob.action_curr.action_directory_name,
            file_name_next,
        )
    else:
        full_name_next = ""

    try:
        dcr_core.cfg.glob.text_parser = dcr_core.nlp.cls_text_parser.TextParser.from_files(full_name_line=full_name_curr)

        cfg.glob.tokenizer_spacy.process_document(full_name=full_name_next, pipeline_name=pipeline_name)

        if cfg.glob.tokenizer_spacy.processing_ok():
            utils.delete_auxiliary_file(full_name_curr)
            cfg.glob.action_curr.finalise()
            cfg.glob.run.run_total_processed_ok += 1

    except FileNotFoundError as err:
        cfg.glob.action_curr.finalise_error(
            error_code=db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_TOKENIZE,
            error_msg=ERROR_71_901.replace("{full_name_curr}", full_name_curr).replace("{error_type}", str(type(err))).replace("{error}", str(err)),
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
