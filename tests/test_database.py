"""Testing Module database."""

import pytest
from app import initialise_logger
from libs.database import DBC_VERSION
from libs.database import DBT_VERSION
from libs.database import ENGINE
from libs.database import METADATA
from libs.database import check_db_up_to_date
from libs.database import insert_table
from libs.database import select_version_unique
from libs.globals import CONFIG
from libs.globals import DCR_CFG_DCR_VERSION
from sqlalchemy import Table
from sqlalchemy import delete

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
LOGGER = initialise_logger()


# -----------------------------------------------------------------------------
# Test Function - check_db_up_to_date().
# -----------------------------------------------------------------------------
def test_check_db_up_to_date_wrong_version(fxtr_new_db_no_inbox):
    """Test: Wrong database version."""
    CONFIG[DCR_CFG_DCR_VERSION] = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        check_db_up_to_date(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1


# -----------------------------------------------------------------------------
# Test Function - select_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_unique_not_found(fxtr_new_db_no_inbox):
    """Test: Column version not found."""
    with ENGINE.begin() as conn:
        version = Table(DBT_VERSION, METADATA, autoload_with=ENGINE)
        conn.execute(delete(version))

    with pytest.raises(SystemExit) as expt:
        select_version_unique(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_select_version_unique_not_unique(fxtr_new_db_no_inbox):
    """Test: Column version not unique."""
    insert_table(LOGGER, DBT_VERSION, [{DBC_VERSION: "0.0.0"}])

    with pytest.raises(SystemExit) as expt:
        select_version_unique(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1
