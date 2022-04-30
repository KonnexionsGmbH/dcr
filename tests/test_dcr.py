# pylint: disable=unused-argument
"""Testing Module dcr.dcr."""
import os
import pathlib
import shutil

import libs.cfg
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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    args = dcr.get_args([libs.cfg.DCR_ARGV_0, "AlL"])

    assert len(args) == 9, "arg: all"
    assert args[libs.cfg.RUN_ACTION_IMAGE_2_PDF], "arg: all"
    assert args[libs.cfg.RUN_ACTION_NON_PDF_2_PDF], "arg: all"
    assert args[libs.cfg.RUN_ACTION_PDF_2_IMAGE], "arg: all"
    assert args[libs.cfg.RUN_ACTION_PROCESS_INBOX], "arg: all"
    assert args[libs.cfg.RUN_ACTION_STORE_FROM_PARSER], "arg: all"
    assert args[libs.cfg.RUN_ACTION_TEXT_FROM_PDF], "arg: all"
    assert args[libs.cfg.RUN_ACTION_TOKENIZE], "arg: all"
    assert not args[libs.cfg.RUN_ACTION_CREATE_DB], "arg: all"
    assert not args[libs.cfg.RUN_ACTION_UPGRADE_DB], "arg: all"

    # -------------------------------------------------------------------------
    args = dcr.get_args([libs.cfg.DCR_ARGV_0, "Db_C"])

    assert args[libs.cfg.RUN_ACTION_CREATE_DB], "arg: db_c"
    assert not args[libs.cfg.RUN_ACTION_IMAGE_2_PDF], "arg: all"
    assert not args[libs.cfg.RUN_ACTION_NON_PDF_2_PDF], "arg: all"
    assert not args[libs.cfg.RUN_ACTION_PDF_2_IMAGE], "arg: db_c"
    assert not args[libs.cfg.RUN_ACTION_PROCESS_INBOX], "arg: db_c"
    assert not args[libs.cfg.RUN_ACTION_STORE_FROM_PARSER], "arg: db_c"
    assert not args[libs.cfg.RUN_ACTION_TEXT_FROM_PDF], "arg: db_c"
    assert not args[libs.cfg.RUN_ACTION_TOKENIZE], "arg: db_c"
    assert not args[libs.cfg.RUN_ACTION_UPGRADE_DB], "arg: db_c"

    # -------------------------------------------------------------------------
    args = dcr.get_args([libs.cfg.DCR_ARGV_0, "Db_U"])

    assert args[libs.cfg.RUN_ACTION_UPGRADE_DB], "arg: db_u"
    assert not args[libs.cfg.RUN_ACTION_CREATE_DB], "arg: db_u"
    assert not args[libs.cfg.RUN_ACTION_IMAGE_2_PDF], "arg: all"
    assert not args[libs.cfg.RUN_ACTION_NON_PDF_2_PDF], "arg: all"
    assert not args[libs.cfg.RUN_ACTION_PDF_2_IMAGE], "arg: db_u"
    assert not args[libs.cfg.RUN_ACTION_PROCESS_INBOX], "arg: db_u"
    assert not args[libs.cfg.RUN_ACTION_STORE_FROM_PARSER], "arg: db_u"
    assert not args[libs.cfg.RUN_ACTION_TEXT_FROM_PDF], "arg: db_u"
    assert not args[libs.cfg.RUN_ACTION_TOKENIZE], "arg: db_u"

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
        dcr.get_args([libs.cfg.INFORMATION_NOT_YET_AVAILABLE, "second"])

    assert expt.type == SystemExit, "invalid arg"
    assert expt.value.code == 1, "invalid arg"

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - main().
# -----------------------------------------------------------------------------
def test_main_all(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_ALL_COMPLETE."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_ALL_COMPLETE])

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


def test_main_db_c(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_CREATE_DB."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


def test_main_p_i(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_PROCESS_INBOX."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


def test_main_p_2_i(fxtr_mkdir, fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_PDF_2_IMAGE."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


def test_main_db_u(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_UPGRADE_DB."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - unknown dbt.
# -----------------------------------------------------------------------------
def test_unknown_dbt(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_CREATE_DB."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    shutil.move(
        pathlib.Path(libs.cfg.config.initial_database_data),
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
    )

    shutil.copyfile(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "test_initial_database_data_unknown_dbt.json"),
        pathlib.Path(libs.cfg.config.initial_database_data),
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    assert expt.type == SystemExit, "api_version: wrong"
    assert expt.value.code == 1, "api_version: wrong"

    # -------------------------------------------------------------------------
    shutil.move(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
        pathlib.Path(libs.cfg.config.initial_database_data),
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - wrong api_version.
# -----------------------------------------------------------------------------
def test_wrong_api_version(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_CREATE_DB."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    shutil.move(
        pathlib.Path(libs.cfg.config.initial_database_data),
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
    )

    shutil.copyfile(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "test_initial_database_data_wrong_api_version.json"),
        pathlib.Path(libs.cfg.config.initial_database_data),
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    assert expt.type == SystemExit, "api_version: wrong"
    assert expt.value.code == 1, "api_version: wrong"

    # -------------------------------------------------------------------------
    shutil.move(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
        pathlib.Path(libs.cfg.config.initial_database_data),
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - wrong dbt.
# -----------------------------------------------------------------------------
def test_wrong_dbt(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_CREATE_DB."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    shutil.move(
        pathlib.Path(libs.cfg.config.initial_database_data),
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
    )

    shutil.copyfile(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "test_initial_database_data_wrong_dbt.json"),
        pathlib.Path(libs.cfg.config.initial_database_data),
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    assert expt.type == SystemExit, "api_version: wrong"
    assert expt.value.code == 1, "api_version: wrong"

    # -------------------------------------------------------------------------
    shutil.move(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
        pathlib.Path(libs.cfg.config.initial_database_data),
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
