# pylint: disable=unused-argument
"""Testing Module dcr.dcr."""
import os

import cfg.cls_setup
import cfg.glob
import db.cls_run
import pytest

import dcr
import dcr_core.cfg.glob

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - get_args().
# -----------------------------------------------------------------------------
def test_dcr_get_args(fxtr_setup_logger_environment):
    """Test: get_args()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    args = dcr.get_args([dcr.DCR_ARGV_0, "AlL"])

    assert len(args) == 10, "arg: all"
    assert args[db.cls_run.Run.ACTION_CODE_TESSERACT], "arg: all"
    assert args[db.cls_run.Run.ACTION_CODE_PANDOC], "arg: all"
    assert args[db.cls_run.Run.ACTION_CODE_PDF2IMAGE], "arg: all"
    assert args[db.cls_run.Run.ACTION_CODE_INBOX], "arg: all"
    assert args[db.cls_run.Run.ACTION_CODE_PARSER], "arg: all"
    assert args[db.cls_run.Run.ACTION_CODE_PDFLIB], "arg: all"
    assert args[db.cls_run.Run.ACTION_CODE_TOKENIZE], "arg: all"
    assert not args[db.cls_run.Run.ACTION_CODE_CREATE_DB], "arg: all"
    assert not args[db.cls_run.Run.ACTION_CODE_UPGRADE_DB], "arg: all"

    # -------------------------------------------------------------------------
    args = dcr.get_args([dcr.DCR_ARGV_0, "Db_C"])

    assert args[db.cls_run.Run.ACTION_CODE_CREATE_DB], "arg: db_c"
    assert not args[db.cls_run.Run.ACTION_CODE_TESSERACT], "arg: all"
    assert not args[db.cls_run.Run.ACTION_CODE_PANDOC], "arg: all"
    assert not args[db.cls_run.Run.ACTION_CODE_PDF2IMAGE], "arg: db_c"
    assert not args[db.cls_run.Run.ACTION_CODE_INBOX], "arg: db_c"
    assert not args[db.cls_run.Run.ACTION_CODE_PARSER], "arg: db_c"
    assert not args[db.cls_run.Run.ACTION_CODE_PDFLIB], "arg: db_c"
    assert not args[db.cls_run.Run.ACTION_CODE_TOKENIZE], "arg: db_c"
    assert not args[db.cls_run.Run.ACTION_CODE_UPGRADE_DB], "arg: db_c"

    # -------------------------------------------------------------------------
    args = dcr.get_args([dcr.DCR_ARGV_0, "Db_U"])

    assert args[db.cls_run.Run.ACTION_CODE_UPGRADE_DB], "arg: db_u"
    assert not args[db.cls_run.Run.ACTION_CODE_CREATE_DB], "arg: db_u"
    assert not args[db.cls_run.Run.ACTION_CODE_TESSERACT], "arg: all"
    assert not args[db.cls_run.Run.ACTION_CODE_PANDOC], "arg: all"
    assert not args[db.cls_run.Run.ACTION_CODE_PDF2IMAGE], "arg: db_u"
    assert not args[db.cls_run.Run.ACTION_CODE_INBOX], "arg: db_u"
    assert not args[db.cls_run.Run.ACTION_CODE_PARSER], "arg: db_u"
    assert not args[db.cls_run.Run.ACTION_CODE_PDFLIB], "arg: db_u"
    assert not args[db.cls_run.Run.ACTION_CODE_TOKENIZE], "arg: db_u"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.get_args([])

    assert expt.type == SystemExit, "no args"
    assert expt.value.code == 1, "no args"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.get_args([""])

    assert expt.type == SystemExit, "one arg"
    assert expt.value.code == 1, "one arg"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.get_args([dcr_core.cfg.glob.INFORMATION_NOT_YET_AVAILABLE, "second"])

    assert expt.type == SystemExit, "invalid arg"
    assert expt.value.code == 1, "invalid arg"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - process_export_lt_rules().
# -----------------------------------------------------------------------------
def test_dcr_process_export_lt_rules(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_ALL_COMPLETE - delete_auxiliary_files = true."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    try:
        os.mkdir("tmp")
    except OSError:
        pass

    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_HEADING, "tmp/lt_export_rule_heading.json"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_LIST_BULLET, "tmp/lt_export_rule_list_bullet.json"),
            (cfg.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_LIST_NUMBER, "tmp/lt_export_rule_list_number.json"),
        ],
    )

    # -------------------------------------------------------------------------
    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_EXPORT_LT_RULES])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
