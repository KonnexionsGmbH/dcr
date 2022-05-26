# pylint: disable=unused-argument
"""Testing Module nlp.tokenize."""
import os

import cfg.glob
import db.cls_run
import pytest

# -----------------------------------------------------------------------------
# Test RUN_ACTION_TOKENIZE - attributes - true.
# -----------------------------------------------------------------------------
import utils

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


def test_run_action_tokenize_attributes_true(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - attributes - true."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("tokenizer_coverage", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    values_original_spacy = pytest.helpers.set_complete_cfg_spacy("true")

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_SPACY,
        values_original_spacy,
    )

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_tokenize_normal <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "tokenizer_coverage_1.page.json",
                "tokenizer_coverage_1.pdf",
                "tokenizer_coverage_1.word.json",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TOKENIZE - attributes - true - coverage.
# -----------------------------------------------------------------------------
def test_run_action_tokenize_attributes_true_coverage(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - attributes - true - coverage."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("tokenizer_coverage", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "true"),
            (cfg.glob.setup._DCR_CFG_TOKENIZE_2_JSONFILE, "true"),
        ],
    )

    values_original_spacy = pytest.helpers.set_complete_cfg_spacy("true")

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_SPACY,
        values_original_spacy,
    )

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
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
        source_files=[
            ("tokenizer_coverage", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
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
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_tokenize_normal <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "tokenizer_coverage_1.page.json",
                "tokenizer_coverage_1.pdf",
                "tokenizer_coverage_1.word.json",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TOKENIZE - missing input file.
# -----------------------------------------------------------------------------
def test_run_action_tokenize_missing_input_file(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - missing input file."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_tokenize_missing_input_file <=========")

    stem_name_1: str = "case_3_pdf_text_route_inbox_pdflib"
    file_ext_1: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name_1, file_ext_1),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    os.remove(utils.get_full_name(cfg.glob.setup.directory_inbox_accepted, stem_name_1 + "_1.line.json"))

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
