# pylint: disable=unused-argument
"""Testing Module dcr.dcr."""
import os
import pathlib
import shutil

import cfg.glob
import db.run
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
    args = dcr.get_args([cfg.glob.DCR_ARGV_0, "AlL"])

    assert len(args) == 9, "arg: all"
    assert args[db.run.Run.ACTION_CODE_TESSERACT], "arg: all"
    assert args[db.run.Run.ACTION_CODE_PANDOC], "arg: all"
    assert args[db.run.Run.ACTION_CODE_PDF2IMAGE], "arg: all"
    assert args[db.run.Run.ACTION_CODE_INBOX], "arg: all"
    assert args[db.run.Run.ACTION_CODE_PARSER], "arg: all"
    assert args[db.run.Run.ACTION_CODE_PDFLIB], "arg: all"
    assert args[db.run.Run.ACTION_CODE_TOKENIZE], "arg: all"
    assert not args[db.run.Run.ACTION_CODE_CREATE_DB], "arg: all"
    assert not args[db.run.Run.ACTION_CODE_UPGRADE_DB], "arg: all"

    # -------------------------------------------------------------------------
    args = dcr.get_args([cfg.glob.DCR_ARGV_0, "Db_C"])

    assert args[db.run.Run.ACTION_CODE_CREATE_DB], "arg: db_c"
    assert not args[db.run.Run.ACTION_CODE_TESSERACT], "arg: all"
    assert not args[db.run.Run.ACTION_CODE_PANDOC], "arg: all"
    assert not args[db.run.Run.ACTION_CODE_PDF2IMAGE], "arg: db_c"
    assert not args[db.run.Run.ACTION_CODE_INBOX], "arg: db_c"
    assert not args[db.run.Run.ACTION_CODE_PARSER], "arg: db_c"
    assert not args[db.run.Run.ACTION_CODE_PDFLIB], "arg: db_c"
    assert not args[db.run.Run.ACTION_CODE_TOKENIZE], "arg: db_c"
    assert not args[db.run.Run.ACTION_CODE_UPGRADE_DB], "arg: db_c"

    # -------------------------------------------------------------------------
    args = dcr.get_args([cfg.glob.DCR_ARGV_0, "Db_U"])

    assert args[db.run.Run.ACTION_CODE_UPGRADE_DB], "arg: db_u"
    assert not args[db.run.Run.ACTION_CODE_CREATE_DB], "arg: db_u"
    assert not args[db.run.Run.ACTION_CODE_TESSERACT], "arg: all"
    assert not args[db.run.Run.ACTION_CODE_PANDOC], "arg: all"
    assert not args[db.run.Run.ACTION_CODE_PDF2IMAGE], "arg: db_u"
    assert not args[db.run.Run.ACTION_CODE_INBOX], "arg: db_u"
    assert not args[db.run.Run.ACTION_CODE_PARSER], "arg: db_u"
    assert not args[db.run.Run.ACTION_CODE_PDFLIB], "arg: db_u"
    assert not args[db.run.Run.ACTION_CODE_TOKENIZE], "arg: db_u"

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


# -----------------------------------------------------------------------------
# Test Function - main().
# -----------------------------------------------------------------------------
def test_main_all(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_ALL_COMPLETE."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.run.Run.ACTION_CODE_ALL_COMPLETE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


def test_main_db_c(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_CREATE_DB."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.run.Run.ACTION_CODE_CREATE_DB])

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


def test_main_p_i(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_PROCESS_INBOX."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.run.Run.ACTION_CODE_INBOX])

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


def test_main_p_2_i(fxtr_mkdir, fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_PDF_2_IMAGE."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.run.Run.ACTION_CODE_PDF2IMAGE])

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


def test_main_db_u(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_UPGRADE_DB."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.run.Run.ACTION_CODE_UPGRADE_DB])

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - unknown dbt.
# -----------------------------------------------------------------------------
def test_unknown_dbt(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_CREATE_DB."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    shutil.move(
        pathlib.Path(cfg.glob.setup.initial_database_data),
        os.path.join(cfg.glob.TESTS_INBOX_NAME, "initial_database_data.json"),
    )

    shutil.copyfile(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, "test_initial_database_data_unknown_dbt.json"),
        pathlib.Path(cfg.glob.setup.initial_database_data),
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.main([cfg.glob.DCR_ARGV_0, db.run.Run.ACTION_CODE_CREATE_DB])

    assert expt.type == SystemExit, "api_version: wrong"
    assert expt.value.code == 1, "api_version: wrong"

    # -------------------------------------------------------------------------
    shutil.move(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, "initial_database_data.json"),
        pathlib.Path(cfg.glob.setup.initial_database_data),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - wrong api_version.
# -----------------------------------------------------------------------------
def test_wrong_api_version(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_CREATE_DB."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    shutil.move(
        pathlib.Path(cfg.glob.setup.initial_database_data),
        os.path.join(cfg.glob.TESTS_INBOX_NAME, "initial_database_data.json"),
    )

    shutil.copyfile(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, "test_initial_database_data_wrong_api_version.json"),
        pathlib.Path(cfg.glob.setup.initial_database_data),
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.main([cfg.glob.DCR_ARGV_0, db.run.Run.ACTION_CODE_CREATE_DB])

    assert expt.type == SystemExit, "api_version: wrong"
    assert expt.value.code == 1, "api_version: wrong"

    # -------------------------------------------------------------------------
    shutil.move(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, "initial_database_data.json"),
        pathlib.Path(cfg.glob.setup.initial_database_data),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - wrong dbt.
# -----------------------------------------------------------------------------
def test_wrong_dbt(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_CREATE_DB."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    shutil.move(
        pathlib.Path(cfg.glob.setup.initial_database_data),
        os.path.join(cfg.glob.TESTS_INBOX_NAME, "initial_database_data.json"),
    )

    shutil.copyfile(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, "test_initial_database_data_wrong_dbt.json"),
        pathlib.Path(cfg.glob.setup.initial_database_data),
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.main([cfg.glob.DCR_ARGV_0, db.run.Run.ACTION_CODE_CREATE_DB])

    assert expt.type == SystemExit, "api_version: wrong"
    assert expt.value.code == 1, "api_version: wrong"

    # -------------------------------------------------------------------------
    shutil.move(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, "initial_database_data.json"),
        pathlib.Path(cfg.glob.setup.initial_database_data),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
