"""Testing Module cfg.cls_..."""
import os

import cfg.cls_setup
import cfg.glob
import pytest

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Check parameter complete.
# -----------------------------------------------------------------------------
def check_param_complete():
    """Check parameter complete."""
    cfg.glob.setup = cfg.cls_setup.Setup()

    assert len(cfg.glob.setup._config) == cfg.glob.setup._CONFIG_PARAM_NO, "cfg:: complete"


# -----------------------------------------------------------------------------
# Check parameter TOKENIZE_2_.
# -----------------------------------------------------------------------------
def check_param_tokenize_2_():
    """Check parameter TOKENIZE_2_."""
    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "fALSE"),
            (cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "fALSE"),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "both DCR_CFG_TOKENIZE_2_DATABASE and DCR_CFG_TOKENIZE_2_JSONFILE false"
    assert expt.value.code == 1, "both DCR_CFG_TOKENIZE_2_DATABASE and DCR_CFG_TOKENIZE_2_JSONFILE false"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )


# -----------------------------------------------------------------------------
# Test Function - get_config() - 1.
# -----------------------------------------------------------------------------
def test_get_config_1(fxtr_setup_logger_environment):
    """Test: get_config() - 1."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_PDF2IMAGE_TYPE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_PDF2IMAGE_TYPE: invalid"
    assert expt.value.code == 1, "DCR_CFG_PDF2IMAGE_TYPE: invalid"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - 2.
# -----------------------------------------------------------------------------
def test_get_config_2(fxtr_setup_logger_environment):
    """Test: test_get_config - 2."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    check_param_complete()

    check_param_tokenize_2_()

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
        cfg.cls_setup.Setup._DCR_CFG_SECTION_SPACY,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.setup._determine_config_param_integer(cfg.glob.INFORMATION_NOT_YET_AVAILABLE, 4711)

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
        cfg.cls_setup.Setup._DCR_CFG_SECTION_SPACY,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_doc_id_in_file_name(fxtr_setup_logger_environment):
    """Test: get_config_doc_id_in_file_name()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "aFTER"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.doc_id_in_file_name == "after", "DCR_CFG_DOC_ID_IN_FILE_NAME: after"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "bEFORE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.doc_id_in_file_name == "before", "DCR_CFG_DOC_ID_IN_FILE_NAME: before"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.doc_id_in_file_name == "none", "DCR_CFG_DOC_ID_IN_FILE_NAME: none (not after or before)"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - missing.
# -----------------------------------------------------------------------------
def test_get_config_missing(fxtr_setup_logger_environment):
    """Test: get_config() - missing."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(cfg.cls_setup.Setup._DCR_CFG_SECTION, cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX)
    values_original_test = pytest.helpers.delete_config_param(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX: missing"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_test,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(cfg.cls_setup.Setup._DCR_CFG_SECTION, cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED)
    values_original_test = pytest.helpers.delete_config_param(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_test,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(cfg.cls_setup.Setup._DCR_CFG_SECTION, cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED)
    values_original_test = pytest.helpers.delete_config_param(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_test,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_IGNORE_DUPLICATES
    )

    cfg.glob.setup.is_ignore_duplicates = False

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert not cfg.glob.setup.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (missing)"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_PDF2IMAGE_TYPE)

    cfg.glob.setup.pdf2image_type = cfg.glob.setup.PDF2IMAGE_TYPE_JPEG

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.pdf2image_type == cfg.glob.setup.PDF2IMAGE_TYPE_JPEG, (
        "DCR_CFG_PDF2IMAGE_TYPE: default should not be '" + cfg.glob.setup.pdf2image_type + "'"
    )

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(cfg.cls_setup.Setup._DCR_CFG_SECTION, cfg.cls_setup.Setup._DCR_CFG_VERBOSE)
    values_original_test = pytest.helpers.delete_config_param(cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_VERBOSE)

    cfg.glob.setup.is_verbose = True

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.is_verbose, "DCR_CFG_VERBOSE: true (missing)"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION,
        values_original,
    )
    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original_test,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(cfg.cls_setup.Setup._DCR_CFG_SECTION, cfg.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER)
    values_original_test = pytest.helpers.delete_config_param(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (missing)"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )
    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
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
    pytest.helpers.insert_config_param(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        "UNKNOWN",
        "n/a",
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "UNKNOWN: unknown"
    assert expt.value.code == 1, "UNKNOWN: unknown"

    pytest.helpers.delete_config_param(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
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
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, "aLL"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "all", "DCR_CFG_VERBOSE_PARSER: all"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (not all or text)"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, "tEXT"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "text", "DCR_CFG_VERBOSE_PARSER: all"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
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
