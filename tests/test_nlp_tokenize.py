# pylint: disable=unused-argument
"""Testing Module nlp.tokenize."""

import cfg.glob
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
            ("pdf_mini", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_DEP_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LANG_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_LINE, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_TEXT_FROM_PDF])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_STORE_FROM_PARSER])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_TOKENIZE])

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
            "pdf_mini_1.pdf",
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
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_DEP_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LANG_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_, "true"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_LINE, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_TEXT_FROM_PDF])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_STORE_FROM_PARSER])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_TOKENIZE])

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
            "tokenizer_coverage_1.pdf",
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
# Test RUN_ACTION_TOKENIZE - normal.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("tetml_line, tetml_page", [("false", "true"), ("true", "false"), ("true", "true")])
def test_run_action_tokenize_normal(tetml_line: str, tetml_page: str, fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - normal."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_mini", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_LINE, tetml_line),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, tetml_page),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_TEXT_FROM_PDF])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_STORE_FROM_PARSER])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_TOKENIZE])

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
            "pdf_mini_1.pdf",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
