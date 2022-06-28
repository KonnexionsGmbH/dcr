# pylint: disable=unused-argument
"""Testing Module nlp.cls_line_type_headers_footers."""
import os.path

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_run
import nlp.cls_line_type_headers_footers
import nlp.cls_line_type_toc
import nlp.cls_nlp_core
import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=duplicate-code
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test LineType Header & Footers.
# -----------------------------------------------------------------------------
def test_cls_line_type_headers_footers(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType Header & Footers."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("p_1_h_0_f_0", "pdf"),
            ("p_2_h_0_f_0", "pdf"),
            ("p_2_h_0_f_2", "pdf"),
            ("p_2_h_1_f_0", "pdf"),
            ("p_2_h_1_f_1", "pdf"),
            ("p_2_h_2_f_0", "pdf"),
            ("p_2_h_2_f_2", "pdf"),
            ("p_3_h_0_f_4", "pdf"),
            ("p_3_h_2_f_2", "pdf"),
            ("p_3_h_3_f_3", "pdf"),
            ("p_3_h_4_f_0", "pdf"),
            ("p_3_h_4_f_4", "pdf"),
            ("p_4_h_4_f_4_different_first", "pdf"),
            ("p_4_h_4_f_4_different_last", "pdf"),
            ("p_4_h_4_f_4_empty_first", "pdf"),
            ("p_4_h_4_f_4_empty_last", "pdf"),
            ("p_5_h_0_f_0", "pdf"),
            ("p_5_h_0_f_2", "pdf"),
            ("p_5_h_2_f_0", "pdf"),
            ("p_5_h_2_f_2", "pdf"),
            ("p_5_h_4_f_4_different_both", "pdf"),
            ("p_5_h_4_f_4_empty_both", "pdf"),
            ("p_5_h_4_f_4_empty_center", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LINE_TYPE_HEADERS_FOOTERS, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LINE_TYPE_TOC, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, "false"),
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
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_1_h_0_f_0_1.line.json")),
        target_footer=[],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_0_f_0_2.line.json")),
        target_footer=[],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_0_f_2_3.line.json")),
        target_footer=[(1, [0, 1]), (2, [0, 1])],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_1_f_0_4.line.json")),
        target_footer=[],
        target_header=[(1, [0]), (2, [0])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_1_f_1_5.line.json")),
        target_footer=[(1, [4]), (2, [4])],
        target_header=[(1, [0]), (2, [0])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_2_f_0_6.line.json")),
        target_footer=[(1, [0, 1]), (2, [0, 1])],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_2_f_2_7.line.json")),
        target_footer=[(1, [1, 2, 3]), (2, [1, 2, 3])],
        target_header=[(1, [0]), (2, [0])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_3_h_0_f_4_8.line.json")),
        target_footer=[(1, [4, 5, 6]), (2, [4, 5, 6]), (3, [4, 5, 6])],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_3_h_2_f_2_9.line.json")),
        target_footer=[(1, [5, 6]), (2, [5, 6]), (3, [5, 6])],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_3_h_3_f_3_10.line.json")),
        target_footer=[(1, [6, 7, 8]), (2, [6, 7, 8]), (3, [6, 7, 8])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_3_h_4_f_0_11.line.json")),
        target_footer=[],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_3_h_4_f_4_12.line.json")),
        target_footer=[(1, [8, 9, 10]), (2, [8, 9, 10]), (3, [8, 9, 10])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_different_first_13.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_different_last_14.line.json")),
        target_footer=[(1, [8, 9, 10]), (2, [8, 9, 10]), (3, [8, 9, 10])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_empty_first_15.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_empty_last_16.line.json")),
        target_footer=[(1, [8, 9, 10]), (2, [8, 9, 10]), (3, [8, 9, 10])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_0_f_0_17.line.json")),
        target_footer=[],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_0_f_2_18.line.json")),
        target_footer=[(1, [5, 6]), (2, [5, 6]), (3, [5, 6]), (4, [3, 4]), (5, [5, 6])],
        target_header=[],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_2_f_0_19.line.json")),
        target_footer=[],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1]), (4, [0, 1]), (5, [0, 1])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_2_f_2_20.line.json")),
        target_footer=[(1, [5, 6]), (2, [5, 6]), (3, [5, 6]), (4, [5, 6]), (5, [5, 6])],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1]), (4, [0, 1]), (5, [0, 1])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_4_f_4_different_both_21.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_4_f_4_empty_both_22.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_4_f_4_empty_center_23.line.json")),
        target_footer=[],
        target_header=[],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_headers_footers - Action (action_curr).
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_headers_footers_action_curr(fxtr_setup_logger_environment):
    """Test Function - missing dependencies - line_type_headers_footers - Action (action_curr)."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_action_curr=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        nlp.cls_line_type_headers_footers.LineTypeHeaderFooters()

    assert expt.type == SystemExit, "Instance of class 'Action (action_curr)' is missing"
    assert expt.value.code == 1, "Instance of class 'Action (action_curr)' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_headers_footers - coverage - exists.
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_headers_footers_coverage_exists(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_headers_footers - coverage - exists."""
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
    cfg.glob.text_parser = nlp.cls_text_parser.TextParser()

    cfg.glob.text_parser.exists()

    # -------------------------------------------------------------------------
    instance = nlp.cls_line_type_headers_footers.LineTypeHeaderFooters()

    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_headers_footers - document.
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_headers_footers_document(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_headers_footers - document."""
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
    cfg.glob.text_parser = nlp.cls_text_parser.TextParser()

    cfg.glob.text_parser.exists()

    # -------------------------------------------------------------------------
    instance = nlp.cls_line_type_headers_footers.LineTypeHeaderFooters()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_document=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        instance._store_results()

    assert expt.type == SystemExit, "Instance of class 'Document' is missing"
    assert expt.value.code == 1, "Instance of class 'Document' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_headers_footers - Setup.
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_headers_footers_setup(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_headers_footers - Setup."""
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
    pytest.helpers.delete_existing_object(is_setup=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        nlp.cls_line_type_headers_footers.LineTypeHeaderFooters()

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_headers_footers - TextParser.
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_headers_footers_text_parser(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_headers_footers - TextParser."""
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
    pytest.helpers.delete_existing_object(is_text_parser=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        nlp.cls_line_type_headers_footers.LineTypeHeaderFooters()

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
