# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

# pylint: disable=unused-argument
"""Testing Module dcr.dcr."""
import os

import dcr_core.cls_setup
import dcr_core.core_glob
import pytest

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_run
import dcr.launcher

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - get_args().
# -----------------------------------------------------------------------------
def test_dcr_get_args(fxtr_setup_logger_environment):
    """Test: get_args()."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    args = dcr.launcher.get_args([dcr.launcher.DCR_ARGV_0, "AlL"])

    assert len(args) == 10, "arg: all"
    assert args[dcr.db.cls_run.Run.ACTION_CODE_TESSERACT], "arg: all"
    assert args[dcr.db.cls_run.Run.ACTION_CODE_PANDOC], "arg: all"
    assert args[dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE], "arg: all"
    assert args[dcr.db.cls_run.Run.ACTION_CODE_INBOX], "arg: all"
    assert args[dcr.db.cls_run.Run.ACTION_CODE_PARSER], "arg: all"
    assert args[dcr.db.cls_run.Run.ACTION_CODE_PDFLIB], "arg: all"
    assert args[dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE], "arg: all"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_CREATE_DB], "arg: all"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_UPGRADE_DB], "arg: all"

    # -------------------------------------------------------------------------
    args = dcr.launcher.get_args([dcr.launcher.DCR_ARGV_0, "Db_C"])

    assert args[dcr.db.cls_run.Run.ACTION_CODE_CREATE_DB], "arg: db_c"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_TESSERACT], "arg: all"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_PANDOC], "arg: all"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE], "arg: db_c"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_INBOX], "arg: db_c"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_PARSER], "arg: db_c"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_PDFLIB], "arg: db_c"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE], "arg: db_c"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_UPGRADE_DB], "arg: db_c"

    # -------------------------------------------------------------------------
    args = dcr.launcher.get_args([dcr.launcher.DCR_ARGV_0, "Db_U"])

    assert args[dcr.db.cls_run.Run.ACTION_CODE_UPGRADE_DB], "arg: db_u"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_CREATE_DB], "arg: db_u"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_TESSERACT], "arg: all"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_PANDOC], "arg: all"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE], "arg: db_u"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_INBOX], "arg: db_u"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_PARSER], "arg: db_u"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_PDFLIB], "arg: db_u"
    assert not args[dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE], "arg: db_u"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.launcher.get_args([])

    assert expt.type == SystemExit, "no args"
    assert expt.value.code == 1, "no args"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.launcher.get_args([""])

    assert expt.type == SystemExit, "one arg"
    assert expt.value.code == 1, "one arg"

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.launcher.get_args([dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE, "second"])

    assert expt.type == SystemExit, "invalid arg"
    assert expt.value.code == 1, "invalid arg"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - process_export_lt_rules().
# -----------------------------------------------------------------------------
def test_dcr_process_export_lt_rules(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_ALL_COMPLETE - delete_auxiliary_files = true."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    try:
        os.mkdir("tmp")
    except OSError:
        pass

    # -------------------------------------------------------------------------
    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_EXPORT_LT_RULES])

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
