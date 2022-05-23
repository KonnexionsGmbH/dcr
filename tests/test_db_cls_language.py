# pylint: disable=unused-argument
"""Testing Module db.cls_language"""
import cfg.glob
import db.cls_version
import db.dml
import db.driver
import pytest

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - language.
# -----------------------------------------------------------------------------
def test_missing_dependencies_language(fxtr_setup_logger):
    """# Test Function - missing dependencies - action - case 1.
."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    try:
        cfg.glob.setup.exists()  # type: ignore

        del cfg.glob.setup

        cfg.glob.logger.debug("The existing object 'cfg.glob.setup' of the class Setup was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_language.Language(
            active=True,
            code_iso_639_3="",
            code_pandoc="",
            code_spacy="",
            code_tesseract="",
            iso_language_name="",
        )

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
