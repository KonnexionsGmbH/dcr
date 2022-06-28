# pylint: disable=unused-argument
"""Testing Module nlp.cls_line_type_table."""

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_run
import nlp.cls_line_type_headers_footers
import nlp.cls_line_type_table
import nlp.cls_line_type_toc
import nlp.cls_nlp_core
import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test LineType Heading - 1.
# -----------------------------------------------------------------------------
def test_line_type_table_1(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Heading - 1."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_table", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TOC, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_REGEXP, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_RULE_FILE, "none"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LINE_TYPE_HEADING, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LINE_TYPE_TABLE, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_line_type_table_2 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_table.line.json",
                "docx_table.line_table.json",
                "docx_table.line_toc.json",
                "docx_table.page.json",
                "docx_table.pdf",
                "docx_table.word.json",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Heading - 2.
# -----------------------------------------------------------------------------
def test_line_type_table_2(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Heading - 2."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_table", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TOC, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LINE_TYPE_HEADING, "false"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_line_type_table_2 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_table.line.json",
                "docx_table.pdf",
                "docx_table.word.json",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test LineType Heading - 3.
# -----------------------------------------------------------------------------
def test_line_type_table_3(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Heading - 3."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_table", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TOC, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_REGEXP, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_MAX_LEVEL, "0"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_TABLE_FILE_INCL_EMPTY_COLUMNS, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LINE_TYPE_HEADING, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LINE_TYPE_TABLE, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_line_type_table_3 <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_table.line.json",
                "docx_table.line_table.json",
                "docx_table.page.json",
                "docx_table.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_table - Action (action_curr).
# -----------------------------------------------------------------------------
def test_line_type_table_missing_dependencies_action_curr(fxtr_setup_logger_environment):
    """Test Function - missing dependencies - line_type_table - Action (action_curr)."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_action_curr=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        nlp.cls_line_type_table.LineTypeTable()

    assert expt.type == SystemExit, "Instance of class 'Action (action_curr)' is missing"
    assert expt.value.code == 1, "Instance of class 'Action (action_curr)' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_table - coverage - exists.
# -----------------------------------------------------------------------------
def test_line_type_table_missing_dependencies_coverage_exists(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_table - coverage - exists."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    cfg.glob.run = db.cls_run.Run(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    cfg.glob.action_curr = db.cls_action.Action(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    cfg.glob.document = db.cls_document.Document(
        action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    cfg.glob.setup = cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    cfg.glob.text_parser = nlp.cls_text_parser.TextParser()

    # -------------------------------------------------------------------------
    instance = nlp.cls_line_type_table.LineTypeTable()

    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_table - Document.
# -----------------------------------------------------------------------------
def test_line_type_table_missing_dependencies_document(fxtr_setup_logger_environment):
    """Test Function - missing dependencies - line_type_table - Document."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.action_curr = db.cls_action.Action(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_document=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        nlp.cls_line_type_table.LineTypeTable()

    assert expt.type == SystemExit, "Instance of class 'Document' is missing"
    assert expt.value.code == 1, "Instance of class 'Document' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_table - Setup.
# -----------------------------------------------------------------------------
def test_line_type_table_missing_dependencies_setup(fxtr_setup_logger_environment):
    """Test Function - missing dependencies - line_type_table - Setup."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.action_curr = db.cls_action.Action(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    cfg.glob.document = db.cls_document.Document(
        action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_setup=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        nlp.cls_line_type_table.LineTypeTable()

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_table - TextParser.
# -----------------------------------------------------------------------------
def test_line_type_table_missing_dependencies_text_parser(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_table - TextParser."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    cfg.glob.run = db.cls_run.Run(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    cfg.glob.action_curr = db.cls_action.Action(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    cfg.glob.document = db.cls_document.Document(
        action_code_last="", directory_name="", file_name="", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    cfg.glob.setup = cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_text_parser=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        nlp.cls_line_type_table.LineTypeTable()

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
