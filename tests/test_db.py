# pylint: disable=unused-argument
"""Testing Module database."""

import pytest
from libs.cfg import DBC_VERSION
from libs.cfg import DBT_VERSION
from libs.cfg import DCR_CFG_DCR_VERSION
from libs.cfg import config
from libs.cfg import engine
from libs.cfg import metadata
from libs.db import check_db_up_to_date
from libs.db import insert_dbt_row
from libs.db import select_version_version_unique
from sqlalchemy import Table
from sqlalchemy import delete

from dcr import initialise_logger

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
LOGGER = initialise_logger()


# -----------------------------------------------------------------------------
# Test Function - check_db_up_to_date().
# -----------------------------------------------------------------------------
def test_check_db_up_to_date_wrong_version(fxtr_new_db_no_inbox):
    """Test: Wrong database version."""
    config[DCR_CFG_DCR_VERSION] = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        check_db_up_to_date(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_unique_not_found(fxtr_new_db_no_inbox):
    """Test: Column version not found."""
    with engine.begin() as conn:
        version = Table(DBT_VERSION, metadata, autoload_with=engine)
        conn.execute(delete(version))

    with pytest.raises(SystemExit) as expt:
        select_version_version_unique(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_select_version_unique_not_unique(fxtr_new_db_no_inbox):
    """Test: Column version not unique."""
    insert_dbt_row(LOGGER, DBT_VERSION, [{DBC_VERSION: "0.0.0"}])

    with pytest.raises(SystemExit) as expt:
        select_version_version_unique(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1
