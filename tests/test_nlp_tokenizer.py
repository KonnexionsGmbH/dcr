# pylint: disable=unused-argument
"""Testing Module nlp.tokenizer."""
import os
import pathlib
import shutil

import cfg.cls_setup
import cfg.glob
import db.cls_db_core
import db.cls_run
import launcher
import pytest

import dcr_core.cls_setup
import dcr_core.core_glob
import dcr_core.core_utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TOKENIZE - attributes - true.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("spacy_ignore", ["false", "true"])
def test_run_action_tokenize_attributes_true(spacy_ignore: str, fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - attributes - true."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("tokenizer_coverage", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_SPACY,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_BRACKET, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_LEFT_PUNCT, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_PUNCT, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_QUOTE, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_SPACE, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_STOP, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_STOP, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_TITLE, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_, "true"),
        ],
    )

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

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
@pytest.mark.parametrize("spacy_ignore", ["false", "true"])
def test_run_action_tokenize_attributes_false_true_coverage(spacy_ignore: str, fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - attributes - false & true - coverage."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("tokenizer_coverage", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.set_complete_cfg_spacy(spacy_ignore)

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TOKENIZE - coverage.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("spacy_ignore", ["false", "true"])
def test_run_action_tokenize_coverage(spacy_ignore: str, fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - coverage."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_table", "pdf"),
            ("tokenizer_coverage", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_SPACY,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_BRACKET, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_LEFT_PUNCT, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_PUNCT, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_QUOTE, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_SPACE, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_STOP, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_DEP_, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_BRACKET, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_LEFT_PUNCT, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_QUOTE, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_RIGHT_PUNCT, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SPACE, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LANG_, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS, "true"),
        ],
    )

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_tokenize_normal <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "pdf_table.pdf",
                "pdf_table.line_token.json",
                "pdf_table.page.json",
                "pdf_table.word.json",
                "tokenizer_coverage.line_token.json",
                "tokenizer_coverage.page.json",
                "tokenizer_coverage.pdf",
                "tokenizer_coverage.word.json",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - french.
# -----------------------------------------------------------------------------
def test_run_action_tokenize_french(fxtr_setup_empty_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - French."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db_initial_data_file_path = pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)

    # copy test file
    shutil.copy(
        dcr_core.core_utils.get_full_name(pytest.helpers.get_test_inbox_directory_name(), "db_initial_data_file_french.json"),
        dcr_core.core_utils.get_full_name(os.path.dirname(db_initial_data_file_path), os.path.basename(db_initial_data_file_path)),
    )

    cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)

    cfg.glob.db_core.create_database()

    # -------------------------------------------------------------------------
    # Copy language subdirectory
    pytest.helpers.copy_directories_4_pytest_2_dir(source_directories=["french"], target_dir=str(dcr_core.core_glob.setup.directory_inbox))

    # -------------------------------------------------------------------------
    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_TOKENIZE - missing input file.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("spacy_ignore", ["false", "true"])
def test_run_action_tokenize_missing_input_file(spacy_ignore: str, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_TOKENIZE - missing input file."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_tokenize_missing_input_file <=========")

    stem_name_1 = "case_3_pdf_text_route_inbox_pdflib"
    file_ext_1 = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name_1, file_ext_1),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )

    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_SPACY,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_BRACKET, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_LEFT_PUNCT, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_PUNCT, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_QUOTE, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_SPACE, spacy_ignore),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_STOP, spacy_ignore),
        ],
    )

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    os.remove(dcr_core.core_utils.get_full_name(dcr_core.core_glob.setup.directory_inbox_accepted, stem_name_1 + "_1.line.json"))

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
