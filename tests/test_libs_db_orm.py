# pylint: disable=unused-argument
"""Testing Module libs.db.orm."""

import libs.cfg
import libs.db.cfg
import libs.db.orm
import pytest

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue

TESTS_INBOX = "tests/__PYTEST_FILES__/"


# -----------------------------------------------------------------------------
# Test Database Version - Wrong version number in configuration.
# -----------------------------------------------------------------------------
def test_check_db_up_to_date(fxtr_setup_empty_db_and_inbox):
    """Test Database Version - Wrong version number in configuration."""
    libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION] = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        libs.db.orm.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1
