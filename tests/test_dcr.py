# pylint: disable=unused-argument
"""Testing Module dcr.dcr."""

import cfg.glob
import db.cls_run
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - get_args().
# -----------------------------------------------------------------------------
def test_get_args(fxtr_setup_logger_environment):
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
        dcr.get_args([cfg.glob.INFORMATION_NOT_YET_AVAILABLE, "second"])

    assert expt.type == SystemExit, "invalid arg"
    assert expt.value.code == 1, "invalid arg"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
