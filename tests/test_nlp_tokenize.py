# pylint: disable=unused-argument
"""Testing Module nlp.tokenize."""

import cfg.glob
import db.cls_run
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TOKENIZE - attributes - true.
# -----------------------------------------------------------------------------
def test_run_action_tokenize_attributes_true(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - attributes - true."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("tokenizer_coverage", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    values_original_spacy = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_SPACY,
        [
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_CLUSTER, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_DEP_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_DOC, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_HEAD, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_I, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IDX, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_ASCII, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_BRACKET, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_LEFT_PUNCT, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_LOWER, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_OOV, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_QUOTE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_RIGHT_PUNCT, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_SPACE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_STOP, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_TITLE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_UPPER, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LANG_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEMMA_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEX, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEX_ID, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_URL, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LOWER_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_MORPH, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_NORM_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_ORTH_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_POS_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_PREFIX_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_PROB, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_RANK, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SENT, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SENTIMENT, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SUFFIX_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TAG_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TENSOR, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TEXT, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_VOCAB, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_SPACY,
        values_original_spacy,
    )

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_tokenize_normal <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            "tokenizer_coverage_1.page.json",
            "tokenizer_coverage_1.pdf",
            "tokenizer_coverage_1.word.json",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TOKENIZE - coverage.
# -----------------------------------------------------------------------------
def test_run_action_tokenize_coverage(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - coverage."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("tokenizer_coverage", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    values_original_spacy = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_SPACY,
        [
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_DEP_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LANG_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_SPACY,
        values_original_spacy,
    )

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_tokenize_normal <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            "tokenizer_coverage_1.page.json",
            "tokenizer_coverage_1.pdf",
            "tokenizer_coverage_1.word.json",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
