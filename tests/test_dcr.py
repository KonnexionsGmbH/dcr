# pylint: disable=unused-argument
"""Testing Module dcr."""
import os

import libs.cfg
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue

CONFIG_PARAM_NO: int = 19


# -----------------------------------------------------------------------------
# Test Function - get_args().
# -----------------------------------------------------------------------------
def test_get_args(fxtr_setup_logger_environment):
    """Test: get_args()."""
    args = dcr.get_args([libs.cfg.DCR_ARGV_0, "AlL"])

    assert len(args) == 4, "arg: all"
    assert not args[libs.cfg.RUN_ACTION_CREATE_DB], "arg: all"
    assert args[libs.cfg.RUN_ACTION_PDF_2_IMAGE], "arg: all"
    assert args[libs.cfg.RUN_ACTION_PROCESS_INBOX], "arg: all"
    assert not args[libs.cfg.RUN_ACTION_UPGRADE_DB], "arg: all"

    # -------------------------------------------------------------------------
    args = dcr.get_args([libs.cfg.DCR_ARGV_0, "Db_C"])

    assert args[libs.cfg.RUN_ACTION_CREATE_DB], "arg: db_c"
    assert not args[libs.cfg.RUN_ACTION_PDF_2_IMAGE], "arg: db_c"
    assert not args[libs.cfg.RUN_ACTION_PROCESS_INBOX], "arg: db_c"
    assert not args[libs.cfg.RUN_ACTION_UPGRADE_DB], "arg: db_c"

    # -------------------------------------------------------------------------
    args = dcr.get_args([libs.cfg.DCR_ARGV_0, "Db_U"])

    assert not args[libs.cfg.RUN_ACTION_CREATE_DB], "arg: db_u"
    assert not args[libs.cfg.RUN_ACTION_PDF_2_IMAGE], "arg: db_u"
    assert not args[libs.cfg.RUN_ACTION_PROCESS_INBOX], "arg: db_u"
    assert args[libs.cfg.RUN_ACTION_UPGRADE_DB], "arg: db_u"

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
        dcr.get_args(["n/a", "second"])

    assert expt.type == SystemExit, "invalid arg"
    assert expt.value.code == 1, "invalid arg"


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config(fxtr_setup_logger_environment):
    """Test: get_config()."""
    # -------------------------------------------------------------------------
    dcr.get_config()

    assert len(libs.cfg.config) == CONFIG_PARAM_NO, "config:: complete"

    # -------------------------------------------------------------------------
    value_original = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_IGNORE_DUPLICATES, "n/a"
    )

    dcr.get_config()

    assert not libs.cfg.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (any not true)"

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_IGNORE_DUPLICATES, value_original
    )

    # -------------------------------------------------------------------------
    value_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_IGNORE_DUPLICATES
    )

    assert not libs.cfg.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (missing)"

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_IGNORE_DUPLICATES, value_original
    )

    # -------------------------------------------------------------------------
    value_original = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_IGNORE_DUPLICATES, "TruE"
    )

    dcr.get_config()

    assert libs.cfg.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: true"

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_IGNORE_DUPLICATES, value_original
    )

    # -------------------------------------------------------------------------
    value_original = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_PDF2IMAGE_TYPE, "n/a"
    )

    with pytest.raises(SystemExit) as expt:
        dcr.get_config()

    assert expt.type == SystemExit, "DCR_CFG_PDF2IMAGE_TYPE: invalid"
    assert expt.value.code == 1, "DCR_CFG_PDF2IMAGE_TYPE: invalid"

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_PDF2IMAGE_TYPE, value_original
    )

    # -------------------------------------------------------------------------
    value_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_PDF2IMAGE_TYPE
    )

    dcr.get_config()

    assert (
        libs.cfg.pdf2image_type == libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_JPEG
    ), "DCR_CFG_PDF2IMAGE_TYPE: default"

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_PDF2IMAGE_TYPE, value_original
    )

    # -------------------------------------------------------------------------
    value_original = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_VERBOSE, "FalsE"
    )

    dcr.get_config()

    assert not libs.cfg.is_verbose, "DCR_CFG_VERBOSE: false"

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_VERBOSE, value_original
    )

    # -------------------------------------------------------------------------
    value_original = pytest.helpers.store_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_VERBOSE, "n/a"
    )

    dcr.get_config()

    assert libs.cfg.is_verbose, "DCR_CFG_VERBOSE: true (not false)"

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_VERBOSE, value_original
    )

    # -------------------------------------------------------------------------
    value_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_VERBOSE
    )

    assert libs.cfg.is_verbose, "DCR_CFG_VERBOSE: true (missing)"

    pytest.helpers.restore_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_VERBOSE, value_original
    )


# -----------------------------------------------------------------------------
# Test Function - get_environment().
# -----------------------------------------------------------------------------
def test_get_environment(fxtr_setup_logger):
    """Test: get_environment()."""
    # -------------------------------------------------------------------------
    os.environ[libs.cfg.DCR_ENVIRONMENT_TYPE] = "n/a"

    with pytest.raises(SystemExit) as expt:
        dcr.get_environment()

    os.environ[libs.cfg.DCR_ENVIRONMENT_TYPE] = libs.cfg.ENVIRONMENT_TYPE_TEST

    assert expt.type == SystemExit, "DCR_ENVIRONMENT_TYPE: invalid"
    assert expt.value.code == 1, "DCR_ENVIRONMENT_TYPE: invalid"

    # -------------------------------------------------------------------------
    os.environ.pop(libs.cfg.DCR_ENVIRONMENT_TYPE)

    with pytest.raises(SystemExit) as expt:
        dcr.get_environment()

    os.environ[libs.cfg.DCR_ENVIRONMENT_TYPE] = libs.cfg.ENVIRONMENT_TYPE_TEST

    assert expt.type == SystemExit, "DCR_ENVIRONMENT_TYPE: missing"
    assert expt.value.code == 1, "DCR_ENVIRONMENT_TYPE: missing"

    # -------------------------------------------------------------------------
    dcr.get_environment()

    assert libs.cfg.environment_type == libs.cfg.ENVIRONMENT_TYPE_TEST, "DCR_ENVIRONMENT_TYPE: ok"


# -----------------------------------------------------------------------------
# Test Function - main().
# -----------------------------------------------------------------------------
def test_main_all(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_ALL_COMPLETE."""
    libs.cfg.logger.info(libs.cfg.LOGGER_START)
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_ALL_COMPLETE])
    libs.cfg.logger.info(libs.cfg.LOGGER_START)


def test_main_db_c(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_CREATE_DB."""
    libs.cfg.logger.info(libs.cfg.LOGGER_START)
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])
    libs.cfg.logger.info(libs.cfg.LOGGER_START)


def test_main_p_i(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_PROCESS_INBOX."""
    libs.cfg.logger.info(libs.cfg.LOGGER_START)
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])
    libs.cfg.logger.info(libs.cfg.LOGGER_START)


def test_main_p_2_i(fxtr_mkdir, fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_PDF_2_IMAGE."""
    libs.cfg.logger.info(libs.cfg.LOGGER_START)
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PDF_2_IMAGE])
    libs.cfg.logger.info(libs.cfg.LOGGER_START)


def test_main_db_u(fxtr_setup_empty_db_and_inbox):
    """Test: main() - RUN_ACTION_UPGRADE_DB."""
    libs.cfg.logger.info(libs.cfg.LOGGER_START)
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])
    libs.cfg.logger.info(libs.cfg.LOGGER_START)
