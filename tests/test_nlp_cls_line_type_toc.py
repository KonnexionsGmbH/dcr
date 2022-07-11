# pylint: disable=unused-argument
"""Testing Module nlp.cls_line_type_toc."""
import os.path

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_run
import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy
import pytest

import dcr
import dcr_core.cfg.glob
import dcr_core.nlp.cls_line_type_toc

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=duplicate-code
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test LineType TOC.
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("lt_toc_last_page", ["0", "5"])
def test_line_type_toc(lt_toc_last_page: str, fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType TOC."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_toc_line_bullet_list", "pdf"),
            ("pdf_toc_table_bullet_list", "pdf"),
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
            (cfg.cls_setup.Setup._DCR_CFG_LT_TOC_LAST_PAGE, lt_toc_last_page),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS, "false"),
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TOC, "false"),
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
    if lt_toc_last_page == "0":
        target_toc_exp_line = 0
        target_toc_exp_table = 0
    else:
        target_toc_exp_line = 7
        target_toc_exp_table = 15

    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "pdf_toc_line_bullet_list_1.line.json")),
        target_footer=[(1, [2, 3]), (2, [10, 11]), (3, [10, 11]), (4, [10, 11]), (5, [6, 7]), (6, [6, 7]), (7, [6, 7])],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1]), (4, [0, 1]), (5, [0, 1]), (6, [0, 1]), (7, [0, 1])],
        target_toc=target_toc_exp_line,
    )
    pytest.helpers.check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "pdf_toc_table_bullet_list_2.line.json")),
        target_footer=[(1, [17, 18]), (2, [10, 11]), (3, [9, 10, 11]), (4, [6, 7]), (5, [6, 7]), (6, [6, 7])],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1]), (4, [0, 1]), (5, [0, 1]), (6, [0, 1])],
        target_toc=target_toc_exp_table,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type_toc - coverage - exists.
# -----------------------------------------------------------------------------
def test_line_type_toc_missing_dependencies_coverage_exists(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - line_type_toc - coverage - exists."""
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
    dcr_core.cfg.glob.text_parser = nlp.cls_text_parser.TextParser()

    dcr_core.cfg.glob.text_parser.exists()

    # -------------------------------------------------------------------------
    instance = dcr_core.nlp.cls_line_type_toc.LineTypeToc(
        action_file_name=cfg.glob.action_curr.action_file_name,
        is_verbose_lt_toc=cfg.glob.setup.is_verbose_lt_toc,
        lt_toc_last_page=cfg.glob.setup.lt_toc_last_page,
        lt_toc_min_entries=cfg.glob.setup.lt_toc_min_entries,
    )

    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
