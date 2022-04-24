# pylint: disable=unused-argument
"""Testing Module dcr.dcr."""
import os
import shutil
from pathlib import Path

import libs.cfg
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


CONFIG_PARAM_NO: int = 27


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
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config(fxtr_setup_logger_environment):
    """Test: get_config()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    libs.cfg.is_ignore_duplicates = False

    dcr.get_config()

    assert len(libs.cfg.config) == CONFIG_PARAM_NO, "config:: complete"

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_IGNORE_DUPLICATES, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    dcr.get_config()

    assert not libs.cfg.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (any not true)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_IGNORE_DUPLICATES, "TruE"),
        ],
    )

    dcr.get_config()

    assert libs.cfg.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: true"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_PDF2IMAGE_TYPE, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        dcr.get_config()

    assert expt.type == SystemExit, "DCR_CFG_PDF2IMAGE_TYPE: invalid"
    assert expt.value.code == 1, "DCR_CFG_PDF2IMAGE_TYPE: invalid"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - missing.
# -----------------------------------------------------------------------------
def test_get_config_missing(fxtr_setup_logger_environment):
    """Test: get_config() - missing."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.get_config()

    assert len(libs.cfg.config) == CONFIG_PARAM_NO, "config:: complete"

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_DIRECTORY_INBOX
    )

    with pytest.raises(SystemExit) as expt:
        dcr.get_config()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX: missing"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    )

    with pytest.raises(SystemExit) as expt:
        dcr.get_config()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED
    )

    with pytest.raises(SystemExit) as expt:
        dcr.get_config()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_IGNORE_DUPLICATES
    )

    libs.cfg.is_ignore_duplicates = False

    dcr.get_config()

    assert not libs.cfg.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (missing)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_PDF2IMAGE_TYPE
    )

    libs.cfg.pdf2image_type = libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_JPEG

    dcr.get_config()

    assert libs.cfg.pdf2image_type == libs.cfg.DCR_CFG_PDF2IMAGE_TYPE_JPEG, (
        "DCR_CFG_PDF2IMAGE_TYPE: default should not be '" + libs.cfg.pdf2image_type + "'"
    )

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_SIMULATE_PARSER
    )

    dcr.get_config()

    assert not libs.cfg.is_simulate_parser, "DCR_CFG_SIMULATE_PARSER: false (missing)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_VERBOSE
    )

    libs.cfg.is_verbose = True

    dcr.get_config()

    assert libs.cfg.is_verbose, "DCR_CFG_VERBOSE: true (missing)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.DCR_CFG_SECTION, libs.cfg.DCR_CFG_VERBOSE_PARSER
    )

    dcr.get_config()

    assert libs.cfg.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (missing)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_simulate_parser(fxtr_setup_logger_environment):
    """Test: test_get_config_simulate_parser()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_SIMULATE_PARSER, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    dcr.get_config()

    assert not libs.cfg.is_simulate_parser, "DCR_CFG_SIMULATE_PARSER: false (not true)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_SIMULATE_PARSER, "tRUE"),
        ],
    )

    dcr.get_config()

    assert libs.cfg.is_simulate_parser, "DCR_CFG_SIMULATE_PARSER: true"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_tetml_line(fxtr_setup_logger_environment):
    """Test: test_get_config_tetml_line()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_TETML_LINE, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    dcr.get_config()

    assert libs.cfg.is_tetml_line, "DCR_CFG_TETML_LINE: true (not false)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_TETML_LINE, "fALSE"),
            (libs.cfg.DCR_CFG_TETML_PAGE, "true"),
        ],
    )

    dcr.get_config()

    assert not libs.cfg.is_tetml_line, "DCR_CFG_TETML_LINE: false"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - tetml_line_page.
# -----------------------------------------------------------------------------
def test_get_config_tetml_line_page(fxtr_setup_logger_environment):
    """Test: get_config() - tetml_line & tetml_page."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_TETML_LINE, "false"),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        dcr.get_config()

    assert (
        expt.type == SystemExit
    ), "DCR_CFG_TETML_LINE and DCR_CFG_TETML_PAGE: both 'false' not allowed"
    assert (
        expt.value.code == 1
    ), "DCR_CFG_TETML_LINE and DCR_CFG_TETML_PAGE: both 'false' not allowed"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_tetml_page(fxtr_setup_logger_environment):
    """Test: test_get_config_tetml_page()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_TETML_PAGE, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    dcr.get_config()

    assert not libs.cfg.is_tetml_page, "DCR_CFG_TETML_PAGE: false (not true)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_TETML_PAGE, "tRUE"),
        ],
    )

    dcr.get_config()

    assert libs.cfg.is_tetml_page, "DCR_CFG_TETML_PAGE: true"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_tetml_word(fxtr_setup_logger_environment):
    """Test: test_get_config_tetml_word()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_TETML_WORD, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    dcr.get_config()

    assert not libs.cfg.is_tetml_word, "DCR_CFG_TETML_WORD: false (not true)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_TETML_WORD, "tRUE"),
        ],
    )

    dcr.get_config()

    assert libs.cfg.is_tetml_word, "DCR_CFG_TETML_WORD: true"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_verbose(fxtr_setup_logger_environment):
    """Test: get_config_verbose()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_VERBOSE, "FalsE"),
        ],
    )

    libs.cfg.is_verbose = True

    dcr.get_config()

    assert not libs.cfg.is_verbose, "DCR_CFG_VERBOSE: false"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_VERBOSE, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    libs.cfg.is_verbose = True

    dcr.get_config()

    assert libs.cfg.is_verbose, "DCR_CFG_VERBOSE: true (not false)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_verbose_parser(fxtr_setup_logger_environment):
    """Test: get_config_verbose_parser()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_VERBOSE_PARSER, "aLL"),
        ],
    )

    dcr.get_config()

    assert libs.cfg.verbose_parser == "all", "DCR_CFG_VERBOSE_PARSER: all"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_VERBOSE_PARSER, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    dcr.get_config()

    assert libs.cfg.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (not all or text)"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.DCR_CFG_SECTION,
        [
            (libs.cfg.DCR_CFG_VERBOSE_PARSER, "tEXT"),
        ],
    )

    dcr.get_config()

    assert libs.cfg.verbose_parser == "text", "DCR_CFG_VERBOSE_PARSER: all"

    pytest.helpers.restore_config_params(
        libs.cfg.DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_environment().
# -----------------------------------------------------------------------------
def test_get_environment(fxtr_setup_logger):
    """Test: get_environment()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    os.environ[libs.cfg.DCR_ENVIRONMENT_TYPE] = libs.cfg.INFORMATION_NOT_YET_AVAILABLE

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
        Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]),
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
    )

    shutil.copyfile(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "test_initial_database_data_unknown_dbt.json"),
        Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]),
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    assert expt.type == SystemExit, "api_version: wrong"
    assert expt.value.code == 1, "api_version: wrong"

    # -------------------------------------------------------------------------
    shutil.move(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
        Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]),
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
        Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]),
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
    )

    shutil.copyfile(
        os.path.join(
            libs.cfg.TESTS_INBOX_NAME, "test_initial_database_data_wrong_api_version.json"
        ),
        Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]),
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    assert expt.type == SystemExit, "api_version: wrong"
    assert expt.value.code == 1, "api_version: wrong"

    # -------------------------------------------------------------------------
    shutil.move(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
        Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]),
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
        Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]),
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
    )

    shutil.copyfile(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "test_initial_database_data_wrong_dbt.json"),
        Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]),
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    assert expt.type == SystemExit, "api_version: wrong"
    assert expt.value.code == 1, "api_version: wrong"

    # -------------------------------------------------------------------------
    shutil.move(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, "initial_database_data.json"),
        Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]),
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
