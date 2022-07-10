# pylint: disable=unused-argument
"""Testing Module nlp.cls_nlp_core."""

import cfg.cls_setup
import cfg.glob

import dcr_core.nlp.cls_nlp_core

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
    instance = dcr_core.nlp.cls_nlp_core.NLPCore()
    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
