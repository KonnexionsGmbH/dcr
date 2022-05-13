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
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config(fxtr_setup_logger_environment):
    """Test: get_config()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.setup.is_ignore_duplicates = False

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert len(cfg.glob.setup._config) == cfg.glob.setup._CONFIG_PARAM_NO, "cfg:: complete"

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_IGNORE_DUPLICATES, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert not cfg.glob.setup.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (any not true)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_IGNORE_DUPLICATES, "TruE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: true"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_PDF2IMAGE_TYPE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_PDF2IMAGE_TYPE: invalid"
    assert expt.value.code == 1, "DCR_CFG_PDF2IMAGE_TYPE: invalid"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
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
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_SPACY,
        [
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_CLUSTER, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_DEP_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_DOC, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_HEAD, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_I, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IDX, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_ASCII, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_BRACKET, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_LEFT_PUNCT, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_LOWER, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_OOV, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_QUOTE, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_RIGHT_PUNCT, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_SPACE, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_STOP, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_TITLE, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_IS_UPPER, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LANG_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEMMA_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEX, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LEX_ID, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_URL, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_LOWER_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_MORPH, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_NORM_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_ORTH_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_POS_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_PREFIX_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_PROB, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_RANK, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SENT, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SENTIMENT, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_SUFFIX_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TAG_, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TENSOR, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TEXT, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_VOCAB, "false"),
            (cfg.glob.setup._DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_, "false"),
        ],
    )

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
def test_get_config_line_footer_preference(fxtr_setup_logger_environment):
    """Test: test_get_config_line_footer_preference()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
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
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_LINE_FOOTER_PREFERENCE, "fALSE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert not cfg.glob.setup.is_line_footer_preferred, "DCR_CFG_LINE_FOOTER_PREFERENCE: false"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - missing.
# -----------------------------------------------------------------------------
def test_get_config_missing(fxtr_setup_logger_environment):
    """Test: get_config() - missing."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.setup = cfg.cls_setup.Setup()

    assert len(cfg.glob.setup._config) == cfg.glob.setup._CONFIG_PARAM_NO, "cfg:: complete"

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_DIRECTORY_INBOX
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX: missing"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_ACCEPTED: missing"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_DIRECTORY_INBOX_REJECTED
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"
    assert expt.value.code == 1, "DCR_CFG_DIRECTORY_INBOX_REJECTED: missing"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_IGNORE_DUPLICATES
    )

    cfg.glob.setup.is_ignore_duplicates = False

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert not cfg.glob.setup.is_ignore_duplicates, "DCR_CFG_IGNORE_DUPLICATES: false (missing)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_PDF2IMAGE_TYPE
    )

    cfg.glob.setup.pdf2image_type = cfg.glob.setup.PDF2IMAGE_TYPE_JPEG

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.pdf2image_type == cfg.glob.setup.PDF2IMAGE_TYPE_JPEG, (
        "DCR_CFG_PDF2IMAGE_TYPE: default should not be '" + cfg.glob.setup.pdf2image_type + "'"
    )

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_VERBOSE
    )

    cfg.glob.setup.is_verbose = True

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.is_verbose, "DCR_CFG_VERBOSE: true (missing)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_VERBOSE_PARSER
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (missing)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_tetml_line(fxtr_setup_logger_environment):
    """Test: test_get_config_tetml_line()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_TETML_LINE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.is_tetml_line, "DCR_CFG_TETML_LINE: true (not false)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_TETML_LINE, "fALSE"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert not cfg.glob.setup.is_tetml_line, "DCR_CFG_TETML_LINE: false"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config() - tetml_line_page.
# -----------------------------------------------------------------------------
def test_get_config_tetml_line_page(fxtr_setup_logger_environment):
    """Test: get_config() - tetml_line & tetml_page."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_TETML_LINE, "false"),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "DCR_CFG_TETML_LINE and DCR_CFG_TETML_PAGE: both 'false' not allowed"
    assert expt.value.code == 1, "DCR_CFG_TETML_LINE and DCR_CFG_TETML_PAGE: both 'false' not allowed"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_tetml_page(fxtr_setup_logger_environment):
    """Test: test_get_config_tetml_page()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert not cfg.glob.setup.is_tetml_page, "DCR_CFG_TETML_PAGE: false (not true)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "tRUE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.is_tetml_page, "DCR_CFG_TETML_PAGE: true"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_tetml_word(fxtr_setup_logger_environment):
    """Test: test_get_config_tetml_word()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_TETML_WORD, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert not cfg.glob.setup.is_tetml_word, "DCR_CFG_TETML_WORD: false (not true)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "tRUE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.is_tetml_word, "DCR_CFG_TETML_WORD: true"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
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
        cfg.glob.setup._DCR_CFG_SECTION,
        "UNKNOWN",
        "n/a",
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup = cfg.cls_setup.Setup()

    assert expt.type == SystemExit, "UNKNOWN: unknown"
    assert expt.value.code == 1, "UNKNOWN: unknown"

    pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION,
        "UNKNOWN",
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_verbose(fxtr_setup_logger_environment):
    """Test: get_config_verbose()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE, "FalsE"),
        ],
    )

    cfg.glob.setup.is_verbose = True

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert not cfg.glob.setup.is_verbose, "DCR_CFG_VERBOSE: false"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup.is_verbose = True

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.is_verbose, "DCR_CFG_VERBOSE: true (not false)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config_verbose_line_type(fxtr_setup_logger_environment):
    """Test: test_get_config_verbose_line_type()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE_LINE_TYPE, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert not cfg.glob.setup.is_verbose_line_type, "DCR_CFG_VERBOSE_LINE_TYPE: false (not true)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE_LINE_TYPE, "tRUE"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.is_verbose_line_type, "DCR_CFG_VERBOSE_LINE_TYPE: true"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
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
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE_PARSER, "aLL"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "all", "DCR_CFG_VERBOSE_PARSER: all"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE_PARSER, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "none", "DCR_CFG_VERBOSE_PARSER: none (not all or text)"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE_PARSER, "tEXT"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    assert cfg.glob.setup.verbose_parser == "text", "DCR_CFG_VERBOSE_PARSER: all"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
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

    os.environ[cfg.glob.setup._DCR_ENVIRONMENT_TYPE] = cfg.glob.setup._ENVIRONMENT_TYPE_TEST

    assert expt.type == SystemExit, "_DCR_ENVIRONMENT_TYPE: invalid"
    assert expt.value.code == 1, "_DCR_ENVIRONMENT_TYPE: invalid"

    # -------------------------------------------------------------------------
    os.environ.pop(cfg.glob.setup._DCR_ENVIRONMENT_TYPE)

    with pytest.raises(SystemExit) as expt:
        cfg.glob.setup._get_environment_variant()

    os.environ[cfg.glob.setup._DCR_ENVIRONMENT_TYPE] = cfg.glob.setup._ENVIRONMENT_TYPE_TEST

    assert expt.type == SystemExit, "_DCR_ENVIRONMENT_TYPE: missing"
    assert expt.value.code == 1, "_DCR_ENVIRONMENT_TYPE: missing"

    # -------------------------------------------------------------------------
    cfg.glob.setup._get_environment_variant()

    assert cfg.glob.setup.environment_variant == cfg.glob.setup._ENVIRONMENT_TYPE_TEST, "_DCR_ENVIRONMENT_TYPE: ok"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
