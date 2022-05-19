# pylint: disable=unused-argument
"""Testing Module cfg.cls_setup."""
import os

import cfg.cls_setup
import cfg.glob
import pytest

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Check parameter DELETE_AUXILIARY_FILES - True.
# -----------------------------------------------------------------------------
def check_param_delete_auxiliary_files():
    """Check parameter DELETE_AUXILIARY_FILES - True."""
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert cfg.glob.setup.is_delete_auxiliary_files, "DCR_CFG_DELETE_AUXILIARY_FILES: true (not false)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "fALSE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert not cfg.glob.setup.is_delete_auxiliary_files, "DCR_CFG_DELETE_AUXILIARY_FILES: false"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )


# -----------------------------------------------------------------------------
# Check parameter IGNORE_DUPLICATES - False.
# -----------------------------------------------------------------------------
def check_param_ignore_duplicates():
    """Check parameter IGNORE_DUPLICATES - False."""
    cfg.glob.setup.is_ignore_duplicates = False

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert len(cfg.glob.setup._config) == cfg.glob.setup._CONFIG_PARAM_NO, "cfg:: complete"

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_IGNORE_DUPLICATES, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert not cfg.glob.setup.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (any not true)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_IGNORE_DUPLICATES, "TruE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert cfg.glob.setup.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: true"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )


# -----------------------------------------------------------------------------
# Check parameter LINE_FOOTER_PREFERENCE - True.
# -----------------------------------------------------------------------------
def check_param_line_footer_preference():
    """Check parameter LINE_FOOTER_PREFERENCE - True."""
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (
                cfg.glob.setup._DCR_CFG_LINE_FOOTER_PREFERENCE,
                cfg.glob.INFORMATION_NOT_YET_AVAILABLE,
            ),
        ],
    )
    cfg.glob.setup = cfg.cls_setup.Setup()
    assert cfg.glob.setup.is_line_footer_preferred, "DCR_CFG_LINE_FOOTER_PREFERENCE: true (not false)"
    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_LINE_FOOTER_PREFERENCE, "fALSE"),
        ],
    )
    cfg.glob.setup = cfg.cls_setup.Setup()
    assert not cfg.glob.setup.is_line_footer_preferred, "DCR_CFG_LINE_FOOTER_PREFERENCE: false"
    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )


# -----------------------------------------------------------------------------
# Check parameter TETML_PAGE - False.
# -----------------------------------------------------------------------------
def check_param_tetml_page():
    """Check parameter TETML_PAGE - False."""
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert not cfg.glob.setup.is_tetml_page, "DCR_CFG_TETML_PAGE: false (not true)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "tRUE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert cfg.glob.setup.is_tetml_page, "DCR_CFG_TETML_PAGE: true"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )


# -----------------------------------------------------------------------------
# Check parameter TETML_WORD - False.
# -----------------------------------------------------------------------------
def check_param_tetml_word():
    """Check parameter TETML_WORD - False."""
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TETML_WORD, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert not cfg.glob.setup.is_tetml_word, "DCR_CFG_TETML_WORD: false (not true)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "tRUE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert cfg.glob.setup.is_tetml_word, "DCR_CFG_TETML_WORD: true"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )


# -----------------------------------------------------------------------------
# Check parameter TOKENIZE_2_DATABASE - True.
# -----------------------------------------------------------------------------
def check_param_tokenize_2_database():
    """Check parameter TOKENIZE_2_DATABASE - True."""
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TOKENIZE_2_DATABASE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert cfg.glob.setup.is_tokenize_2_database, "DCR_CFG_TOKENIZE_2_DATABASE: true (not false)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TOKENIZE_2_DATABASE, "fALSE"),
            (cfg.glob.setup._DCR_CFG_TOKENIZE_2_JSONFILE, "tRUE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert not cfg.glob.setup.is_tokenize_2_database, "DCR_CFG_TOKENIZE_2_DATABASE: false"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )


# -----------------------------------------------------------------------------
# Check parameter TOKENIZE_2_JSONFILE - False.
# -----------------------------------------------------------------------------
def check_param_tokenize_2_jsonfile():
    """Check parameter TOKENIZE_2_JSONFILE - False."""
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TOKENIZE_2_JSONFILE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert not cfg.glob.setup.is_tokenize_2_jsonfile, "DCR_CFG_TOKENIZE_2_JSONFILE: false (not true)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TOKENIZE_2_JSONFILE, "tRUE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert cfg.glob.setup.is_tokenize_2_jsonfile, "DCR_CFG_TOKENIZE_2_JSONFILE: true"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TOKENIZE_2_DATABASE, "fALSE"),
            (cfg.glob.setup._DCR_CFG_TOKENIZE_2_JSONFILE, "fALSE"),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "both DCR_CFG_TOKENIZE_2_DATABASE and DCR_CFG_TOKENIZE_2_JSONFILE false"
    assert expt.value.code == 1, "both DCR_CFG_TOKENIZE_2_DATABASE and DCR_CFG_TOKENIZE_2_JSONFILE false"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )


# -----------------------------------------------------------------------------
# Check parameter VERBOSE - True.
# -----------------------------------------------------------------------------
def check_param_verbose():
    """Check parameter VERBOSE - True."""
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert cfg.glob.setup.is_verbose, "DCR_CFG_VERBOSE: true (not false)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE, "fALSE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert not cfg.glob.setup.is_verbose, "DCR_CFG_VERBOSE: false"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )


# -----------------------------------------------------------------------------
# Check parameter VERBOSE_LINE_TYPE - False.
# -----------------------------------------------------------------------------
def check_param_verbose_line_type():
    """Check parameter VERBOSE_LINE_TYPE - False."""
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE_LINE_TYPE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert not cfg.glob.setup.is_verbose_line_type, "DCR_CFG_VERBOSE_LINE_TYPE: false (not true)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE_LINE_TYPE, "tRUE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()
    assert cfg.glob.setup.is_verbose_line_type, "DCR_CFG_VERBOSE_LINE_TYPE: true"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config(fxtr_setup_logger_environment):
    """Test: get_config()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_PDF2IMAGE_TYPE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_PDF2IMAGE_TYPE: invalid"
    assert expt.value.code == 1, "DCR_CFG_PDF2IMAGE_TYPE: invalid"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - coverage - false.
# -----------------------------------------------------------------------------
def test_get_config_coverage_false(fxtr_setup_logger_environment):
    """Test: test_get_config_coverage_false()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.set_complete_cfg_spacy("false")

    cfg.glob.setup = cfg.cls_setup.Setup()

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_SPACY,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - coverage - true.
# -----------------------------------------------------------------------------
def test_get_config_coverage_true(fxtr_setup_logger_environment):
    """Test: test_get_config_coverage_true()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.set_complete_cfg_spacy("true")

    cfg.glob.setup = cfg.cls_setup.Setup()

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_SPACY,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_logical_false(fxtr_setup_logger_environment):
    """Test: test_get_config_tetml()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    check_param_ignore_duplicates()

    check_param_tetml_page()

    check_param_tetml_word()

    check_param_tokenize_2_jsonfile()

    check_param_verbose_line_type()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_logical_true(fxtr_setup_logger_environment):
    """Test: test_get_config_tetml()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    check_param_delete_auxiliary_files()

    check_param_line_footer_preference()

    check_param_tokenize_2_database()

    check_param_verbose()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - missing.
# -----------------------------------------------------------------------------
def test_get_config_missing(fxtr_setup_logger_environment):  # pylint: disable=R0915
    """Test: get_config() - missing."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.setup = cfg.cls_setup.Setup()

    assert len(cfg.glob.setup._config) == cfg.glob.setup._CONFIG_PARAM_NO, "cfg:: complete"

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_DIRECTORY_INBOX
    )
    values_original_test = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST, cfg.glob.setup._DCR_CFG_DIRECTORY_INBOX
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX: missing"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_test,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    )
    values_original_test = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST, cfg.glob.setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_test,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_DIRECTORY_INBOX_REJECTED
    )
    values_original_test = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST, cfg.glob.setup._DCR_CFG_DIRECTORY_INBOX_REJECTED
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_test,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST, cfg.glob.setup._DCR_CFG_IGNORE_DUPLICATES
    )

    cfg.glob.setup.is_ignore_duplicates = False

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert not cfg.glob.setup.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (missing)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST, cfg.glob.setup._DCR_CFG_PDF2IMAGE_TYPE
    )

    cfg.glob.setup.pdf2image_type = cfg.glob.setup.PDF2IMAGE_TYPE_JPEG

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.pdf2image_type == cfg.glob.setup.PDF2IMAGE_TYPE_JPEG, (
        "DCR_CFG_PDF2IMAGE_TYPE: default should not be '" + cfg.glob.setup.pdf2image_type + "'"
    )

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_VERBOSE
    )
    values_original_test = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST, cfg.glob.setup._DCR_CFG_VERBOSE
    )

    cfg.glob.setup.is_verbose = True

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.is_verbose, "DCR_CFG_VERBOSE: true (missing)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )
    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_test,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_VERBOSE_PARSER
    )
    values_original_test = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST, cfg.glob.setup._DCR_CFG_VERBOSE_PARSER
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (missing)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_test,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - unknown.
# -----------------------------------------------------------------------------
def test_get_config_unknown(fxtr_setup_logger_environment):
    """Test: get_config() - unknown."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.setup = cfg.cls_setup.Setup()

    assert len(cfg.glob.setup._config) == cfg.glob.setup._CONFIG_PARAM_NO, "cfg:: complete"

    # -------------------------------------------------------------------------
    pytest.helpers.insert_config_param(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        "UNKNOWN",
        "n/a",
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "UNKNOWN: unknown"
    assert expt.value.code == 1, "UNKNOWN: unknown"

    pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        "UNKNOWN",
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_verbose_parser(fxtr_setup_logger_environment):
    """Test: get_config_verbose_parser()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE_PARSER, "aLL"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "all", "DCR_CFG_VERBOSE_PARSER: all"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE_PARSER, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (not all or text)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE_PARSER, "tEXT"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "text", "DCR_CFG_VERBOSE_PARSER: all"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_environment().
# -----------------------------------------------------------------------------
def test_get_environment(fxtr_setup_logger):
    """Test: get_environment()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.setup = cfg.cls_setup.Setup()

    os.environ[cfg.glob.setup._DCR_ENVIRONMENT_TYPE] = cfg.glob.INFORMATION_NOT_YET_AVAILABLE

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup._get_environment_variant()

    os.environ[cfg.glob.setup._DCR_ENVIRONMENT_TYPE] = cfg.glob.setup.ENVIRONMENT_TYPE_TEST

    assert expt.type == SystemExit, "_DCR_ENVIRONMENT_TYPE: invalid"
    assert expt.value.code == 1, "_DCR_ENVIRONMENT_TYPE: invalid"

    # -------------------------------------------------------------------------
    os.environ.pop(cfg.glob.setup._DCR_ENVIRONMENT_TYPE)

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup._get_environment_variant()

    os.environ[cfg.glob.setup._DCR_ENVIRONMENT_TYPE] = cfg.glob.setup.ENVIRONMENT_TYPE_TEST

    assert expt.type == SystemExit, "_DCR_ENVIRONMENT_TYPE: missing"
    assert expt.value.code == 1, "_DCR_ENVIRONMENT_TYPE: missing"

    # -------------------------------------------------------------------------
    cfg.glob.setup._get_environment_variant()

    assert cfg.glob.setup.environment_variant == cfg.glob.setup.ENVIRONMENT_TYPE_TEST, "_DCR_ENVIRONMENT_TYPE: ok"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
