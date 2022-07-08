# -*- coding: utf-8 -*-

# pylint: disable=unused-argument
"""Testing Module nlp.cls_nlp_core."""

import cfg.cls_setup
import cfg.glob
import nlp.cls_nlp_core
import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy

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
