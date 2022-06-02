"""Module nlp.cls_tokenizer: Store the document tokens page by page in the
database."""

import json
import time

import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_language
import db.cls_run
import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy
import spacy
import spacy.tokens
import utils

# -----------------------------------------------------------------------------
# Global constants.
# -----------------------------------------------------------------------------
ERROR_71_901: str = (
    "71.901 Issue (tkn): Tokenizing the file '{full_name_curr}' failed - " + "error type: '{error_type}' - error: '{error}'."
)


# -----------------------------------------------------------------------------
# Extract the text from the page lines.
# -----------------------------------------------------------------------------
def get_text_from_line_2_page() -> str:
    """Extract the text from the page data.

    Returns:
        str: Reconstructed text.
    """
    line_0_lines = []

    for cfg.glob.text_parser.parse_result_line_0_line in cfg.glob.text_parser.parse_result_line_2_page[
        cfg.glob.text_parser.JSON_NAME_LINES
    ]:
        if (
            cfg.glob.text_parser.parse_result_line_0_line[cfg.glob.text_parser.JSON_NAME_LINE_TYPE]
            == db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY
        ):
            line_0_lines.append(cfg.glob.text_parser.parse_result_line_0_line[cfg.glob.text_parser.JSON_NAME_LINE_TEXT])

    return "\n".join(line_0_lines)


# -----------------------------------------------------------------------------
# Create document tokens (step: tkn).
# -----------------------------------------------------------------------------
def tokenize() -> None:
    """Create document tokens (step: tkn).

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    model_data: spacy.Language
    spacy_model_current: str | None = None

    cfg.glob.text_parser = nlp.cls_text_parser.TextParser()
    cfg.glob.tokenizer_spacy = nlp.cls_tokenizer_spacy.TokenizerSpacy()

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

            cfg.glob.document = db.cls_document.Document.from_id(id_document=cfg.glob.action_curr.action_id_document)

            spacy_model = db.cls_language.Language.LANGUAGES_SPACY[cfg.glob.document.document_id_language]

            if spacy_model != spacy_model_current:
                model_data: spacy.Language = spacy.load(spacy_model)
                spacy_model_current = spacy_model

            tokenize_file(model_data)

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the tokens of a document page by page (step: tkn).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def tokenize_file(model_data: spacy.Language) -> None:
    """Create the tokens of a document page by page.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name_curr = cfg.glob.action_curr.get_full_name()

    if cfg.glob.setup.is_tokenize_2_jsonfile:
        file_name_next = cfg.glob.action_curr.get_stem_name() + "_token." + db.cls_document.Document.DOCUMENT_FILE_TYPE_JSON
        full_name_next = utils.get_full_name(
            cfg.glob.action_curr.action_directory_name,
            file_name_next,
        )
    else:
        full_name_next = None

    try:
        cfg.glob.text_parser = nlp.cls_text_parser.TextParser.from_files(full_name_line=full_name_curr)

        cfg.glob.tokenizer_spacy.token_3_pages = []

        for cfg.glob.text_parser.parse_result_line_2_page in cfg.glob.text_parser.parse_result_line_4_document[
            cfg.glob.text_parser.JSON_NAME_PAGES
        ]:
            # ------------------------------------------------------------------
            # Processing a single page
            # ------------------------------------------------------------------
            page_no = cfg.glob.text_parser.parse_result_line_2_page[cfg.glob.text_parser.JSON_NAME_PAGE_NO]

            text = get_text_from_line_2_page()

            cfg.glob.tokenizer_spacy.token_1_tokens = []

            for token in model_data(text):
                cfg.glob.tokenizer_spacy.token_1_tokens.append(
                    nlp.cls_tokenizer_spacy.TokenizerSpacy.get_token_attributes(token)
                )

            cfg.glob.tokenizer_spacy.token_2_page = {
                cfg.glob.text_parser.JSON_NAME_PAGE_NO: page_no,
                nlp.cls_tokenizer_spacy.TokenizerSpacy.JSON_NAME_NO_TOKENS_IN_PAGE: len(
                    cfg.glob.tokenizer_spacy.token_1_tokens
                ),
                nlp.cls_tokenizer_spacy.TokenizerSpacy.JSON_NAME_TOKENS: cfg.glob.tokenizer_spacy.token_1_tokens,
            }

            if cfg.glob.setup.is_tokenize_2_database:
                cfg.glob.db_core.insert_dbt_row(
                    db.cls_db_core.DBCore.DBT_TOKEN,
                    {
                        db.cls_db_core.DBCore.DBC_ID_DOCUMENT: cfg.glob.document.document_id,
                        db.cls_db_core.DBCore.DBC_PAGE_DATA: cfg.glob.tokenizer_spacy.token_2_page,
                        db.cls_db_core.DBCore.DBC_PAGE_NO: page_no,
                    },
                )

            if cfg.glob.setup.is_tokenize_2_jsonfile:
                cfg.glob.tokenizer_spacy.token_3_pages.append(cfg.glob.tokenizer_spacy.token_2_page)

        if cfg.glob.setup.is_tokenize_2_jsonfile:
            with open(full_name_next, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    {
                        cfg.glob.text_parser.JSON_NAME_DOCUMENT_ID: cfg.glob.document.document_id,
                        cfg.glob.text_parser.JSON_NAME_DOCUMENT_FILE_NAME: cfg.glob.document.document_file_name,
                        cfg.glob.text_parser.JSON_NAME_NO_PAGES_IN_DOC: cfg.glob.text_parser.parse_result_line_4_document[
                            cfg.glob.text_parser.JSON_NAME_NO_PAGES_IN_DOC
                        ],
                        cfg.glob.text_parser.JSON_NAME_PAGES: cfg.glob.tokenizer_spacy.token_3_pages,
                    },
                    file_handle,
                )

        utils.delete_auxiliary_file(full_name_curr)

        cfg.glob.action_curr.finalise()

        cfg.glob.run.run_total_processed_ok += 1
    except FileNotFoundError as err:
        cfg.glob.action_curr.finalise_error(
            error_code=db.cls_document.Document.DOCUMENT_ERROR_CODE_REJ_TOKENIZE,
            error_msg=ERROR_71_901.replace("{full_name_curr}", full_name_curr)
            .replace("{error_type}", str(type(err)))
            .replace("{error}", str(err)),
        )

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
