"""Testing Module database."""

import pytest
from app import get_config
from app import initialise_logger
from libs.database import check_db_up_to_date
from libs.globals import CONFIG
from libs.globals import DCR_CFG_DATABASE_FILE
from libs.globals import DCR_CFG_DCR_VERSION

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
LOGGER = initialise_logger()


# -----------------------------------------------------------------------------
# Test Function - check_db_up_to_date().
# -----------------------------------------------------------------------------
def test_check_db_up_to_date_no_db(fxtr_remove_opt):
    """#### Test: **No database file existing**."""
    get_config(LOGGER)

    fxtr_remove_opt(CONFIG[DCR_CFG_DATABASE_FILE])

    with pytest.raises(SystemExit) as expt:
        check_db_up_to_date(LOGGER)
        assert expt.type == SystemExit
        assert expt.value.code == 1


def test_check_db_up_to_date_wrong_version(
    fxtr_create_new_db, fxtr_remove_opt
):
    """#### Test: **Wrong database version**."""
    fxtr_create_new_db

    CONFIG[DCR_CFG_DCR_VERSION] = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        check_db_up_to_date(LOGGER)
        assert expt.type == SystemExit
        assert expt.value.code == 1

    fxtr_remove_opt(CONFIG[DCR_CFG_DATABASE_FILE])
