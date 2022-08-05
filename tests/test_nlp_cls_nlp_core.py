# pylint: disable=unused-argument
"""Testing Module nlp.cls_nlp_core."""

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr_core.cls_nlp_core

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test NLPCore - Existence.
# -----------------------------------------------------------------------------
def test_cls_nlp_core_exists(fxtr_rmdir_opt, fxtr_setup_logger_environment):
    """Test NLPCore - Existence."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    instance = dcr_core.cls_nlp_core.NLPCore()
    instance.exists()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)
