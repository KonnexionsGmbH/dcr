# pylint: disable=unused-argument
"""Testing Module nlp.cls_nlp_core."""
import cfg.cls_setup
import cfg.glob
import nlp.cls_nlp_core
import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy
import pytest

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test NLPCore - Existence.
# -----------------------------------------------------------------------------
def test_cls_nlp_core_exists(fxtr_rmdir_opt, fxtr_setup_logger_environment):
    """Test NLPCore - Existence."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    instance = nlp.cls_nlp_core.NLPCore()
    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test NLPCore - Export heading rules.
# -----------------------------------------------------------------------------
def test_cls_nlp_core_export_heading(fxtr_rmdir_opt, fxtr_setup_logger_environment):
    """Test NLPCore - Export heading rules."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_HEADING, "tmp/lt_export_rule_heading.json"),
        ],
    )

    # -------------------------------------------------------------------------
    instance = nlp.cls_nlp_core.NLPCore()
    instance.export_rule_file_heading()

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test NLPCore - Export bulleted list rules.
# -----------------------------------------------------------------------------
def test_cls_nlp_core_export_list_bullet(fxtr_rmdir_opt, fxtr_setup_logger_environment):
    """Test NLPCore - Export bulleted list rules."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_LIST_BULLET, "tmp/lt_export_rule_list_bullet.json"),
        ],
    )

    # -------------------------------------------------------------------------
    instance = nlp.cls_nlp_core.NLPCore()
    instance.export_rule_file_list_bullet()

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test NLPCore - Export numbered list rules.
# -----------------------------------------------------------------------------
def test_cls_nlp_core_export_list_number(fxtr_rmdir_opt, fxtr_setup_logger_environment):
    """Test NLPCore - Export numbered list rules."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_LIST_NUMBER, "tmp/lt_export_rule_list_number.json"),
        ],
    )

    # -------------------------------------------------------------------------
    instance = nlp.cls_nlp_core.NLPCore()
    instance.export_rule_file_list_number()

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
