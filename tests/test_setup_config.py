# pylint: disable=unused-argument
"""Testing Module setup.config."""
import os

import libs.cfg
import pytest
import setup.config

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


CONFIG_PARAM_NO: int = 33


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config(fxtr_setup_logger_environment):
    """Test: get_config()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    libs.cfg.config.is_ignore_duplicates = False

    libs.cfg.config = setup.config.Config()

    assert len(libs.cfg.config._config) == CONFIG_PARAM_NO, "config:: complete"

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_IGNORE_DUPLICATES, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert not libs.cfg.config.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (any not true)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_IGNORE_DUPLICATES, "TruE"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: true"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_PDF2IMAGE_TYPE, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        libs.cfg.config = setup.config.Config()

    assert expt.type == SystemExit, "DCR_CFG_PDF2IMAGE_TYPE: invalid"
    assert expt.value.code == 1, "DCR_CFG_PDF2IMAGE_TYPE: invalid"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_line_footer_preference(fxtr_setup_logger_environment):
    """Test: test_get_config_line_footer_preference()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (
                libs.cfg.config._DCR_CFG_LINE_FOOTER_PREFERENCE,
                libs.cfg.INFORMATION_NOT_YET_AVAILABLE,
            ),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.is_line_footer_preferred, "DCR_CFG_LINE_FOOTER_PREFERENCE: true (not false)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_LINE_FOOTER_PREFERENCE, "fALSE"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert not libs.cfg.config.is_line_footer_preferred, "DCR_CFG_LINE_FOOTER_PREFERENCE: false"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - missing.
# -----------------------------------------------------------------------------
def test_get_config_missing(fxtr_setup_logger_environment):
    """Test: get_config() - missing."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    libs.cfg.config = setup.config.Config()

    assert len(libs.cfg.config._config) == CONFIG_PARAM_NO, "config:: complete"

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION, libs.cfg.config._DCR_CFG_DIRECTORY_INBOX
    )

    with pytest.raises(SystemExit) as expt:
        libs.cfg.config = setup.config.Config()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX: missing"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION, libs.cfg.config._DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    )

    with pytest.raises(SystemExit) as expt:
        libs.cfg.config = setup.config.Config()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION, libs.cfg.config._DCR_CFG_DIRECTORY_INBOX_REJECTED
    )

    with pytest.raises(SystemExit) as expt:
        libs.cfg.config = setup.config.Config()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION, libs.cfg.config._DCR_CFG_IGNORE_DUPLICATES
    )

    libs.cfg.config.is_ignore_duplicates = False

    libs.cfg.config = setup.config.Config()

    assert not libs.cfg.config.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (missing)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION, libs.cfg.config._DCR_CFG_PDF2IMAGE_TYPE
    )

    libs.cfg.config.pdf2image_type = libs.cfg.config.PDF2IMAGE_TYPE_JPEG

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.pdf2image_type == libs.cfg.config.PDF2IMAGE_TYPE_JPEG, (
        "DCR_CFG_PDF2IMAGE_TYPE: default should not be '" + libs.cfg.config.pdf2image_type + "'"
    )

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION, libs.cfg.config._DCR_CFG_SIMULATE_PARSER
    )

    libs.cfg.config = setup.config.Config()

    assert not libs.cfg.config.is_simulate_parser, "DCR_CFG_SIMULATE_PARSER: false (missing)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION, libs.cfg.config._DCR_CFG_VERBOSE
    )

    libs.cfg.config.is_verbose = True

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.is_verbose, "DCR_CFG_VERBOSE: true (missing)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION, libs.cfg.config._DCR_CFG_VERBOSE_PARSER
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (missing)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
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
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_SIMULATE_PARSER, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert not libs.cfg.config.is_simulate_parser, "DCR_CFG_SIMULATE_PARSER: false (not true)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_SIMULATE_PARSER, "tRUE"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.is_simulate_parser, "DCR_CFG_SIMULATE_PARSER: true"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
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
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_TETML_LINE, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.is_tetml_line, "DCR_CFG_TETML_LINE: true (not false)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_TETML_LINE, "fALSE"),
            (libs.cfg.config._DCR_CFG_TETML_PAGE, "true"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert not libs.cfg.config.is_tetml_line, "DCR_CFG_TETML_LINE: false"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
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
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_TETML_LINE, "false"),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        libs.cfg.config = setup.config.Config()

    assert expt.type == SystemExit, "DCR_CFG_TETML_LINE and DCR_CFG_TETML_PAGE: both 'false' not allowed"
    assert expt.value.code == 1, "DCR_CFG_TETML_LINE and DCR_CFG_TETML_PAGE: both 'false' not allowed"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
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
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_TETML_PAGE, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert not libs.cfg.config.is_tetml_page, "DCR_CFG_TETML_PAGE: false (not true)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_TETML_PAGE, "tRUE"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.is_tetml_page, "DCR_CFG_TETML_PAGE: true"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
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
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_TETML_WORD, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert not libs.cfg.config.is_tetml_word, "DCR_CFG_TETML_WORD: false (not true)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_TETML_WORD, "tRUE"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.is_tetml_word, "DCR_CFG_TETML_WORD: true"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - unknown.
# -----------------------------------------------------------------------------
def test_get_config_unknown(fxtr_setup_logger_environment):
    """Test: get_config() - unknown."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    libs.cfg.config = setup.config.Config()

    assert len(libs.cfg.config._config) == CONFIG_PARAM_NO, "config:: complete"

    # -------------------------------------------------------------------------
    pytest.helpers.insert_config_param(
        libs.cfg.config._DCR_CFG_SECTION,
        "UNKNOWN",
        "n/a",
    )

    with pytest.raises(SystemExit) as expt:
        libs.cfg.config = setup.config.Config()

    assert expt.type == SystemExit, "UNKNOWN: unknown"
    assert expt.value.code == 1, "UNKNOWN: unknown"

    pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION,
        "UNKNOWN",
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
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_VERBOSE, "FalsE"),
        ],
    )

    libs.cfg.config.is_verbose = True

    libs.cfg.config = setup.config.Config()

    assert not libs.cfg.config.is_verbose, "DCR_CFG_VERBOSE: false"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_VERBOSE, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    libs.cfg.config.is_verbose = True

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.is_verbose, "DCR_CFG_VERBOSE: true (not false)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_verbose_line_type(fxtr_setup_logger_environment):
    """Test: test_get_config_verbose_line_type()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_VERBOSE_LINE_TYPE, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert not libs.cfg.config.is_verbose_line_type, "DCR_CFG_VERBOSE_LINE_TYPE: false (not true)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_VERBOSE_LINE_TYPE, "tRUE"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.is_verbose_line_type, "DCR_CFG_VERBOSE_LINE_TYPE: true"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
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
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_VERBOSE_PARSER, "aLL"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.verbose_parser == "all", "DCR_CFG_VERBOSE_PARSER: all"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_VERBOSE_PARSER, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (not all or text)"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_VERBOSE_PARSER, "tEXT"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    assert libs.cfg.config.verbose_parser == "text", "DCR_CFG_VERBOSE_PARSER: all"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
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
    os.environ[libs.cfg.config._DCR_ENVIRONMENT_TYPE] = libs.cfg.INFORMATION_NOT_YET_AVAILABLE

    with pytest.raises(SystemExit) as expt:
        libs.cfg.config._get_environment_variant()

    os.environ[libs.cfg.config._DCR_ENVIRONMENT_TYPE] = libs.cfg.config._ENVIRONMENT_TYPE_TEST

    assert expt.type == SystemExit, "_DCR_ENVIRONMENT_TYPE: invalid"
    assert expt.value.code == 1, "_DCR_ENVIRONMENT_TYPE: invalid"

    # -------------------------------------------------------------------------
    os.environ.pop(libs.cfg.config._DCR_ENVIRONMENT_TYPE)

    with pytest.raises(SystemExit) as expt:
        libs.cfg.config._get_environment_variant()

    os.environ[libs.cfg.config._DCR_ENVIRONMENT_TYPE] = libs.cfg.config._ENVIRONMENT_TYPE_TEST

    assert expt.type == SystemExit, "_DCR_ENVIRONMENT_TYPE: missing"
    assert expt.value.code == 1, "_DCR_ENVIRONMENT_TYPE: missing"

    # -------------------------------------------------------------------------
    libs.cfg.config._get_environment_variant()

    assert libs.cfg.config.environment_variant == libs.cfg.config._ENVIRONMENT_TYPE_TEST, "_DCR_ENVIRONMENT_TYPE: ok"

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
