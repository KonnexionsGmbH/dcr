# pylint: disable=unused-argument
"""Testing Module database."""

import libs.cfg
import libs.db
import pytest
from sqlalchemy import Table
from sqlalchemy import delete

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
LOGGER = dcr.initialise_logger()


# -----------------------------------------------------------------------------
# Test Function - check_db_up_to_date().
# -----------------------------------------------------------------------------
def test_check_db_up_to_date_wrong_version(fxtr_new_db_no_inbox):
    """Test: Wrong database version."""
    libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION] = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        libs.db.check_db_up_to_date(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_unique_not_found(fxtr_new_db_no_inbox):
    """Test: Column version not found."""
    libs.db.connect_db(LOGGER)

    with libs.cfg.engine.begin() as conn:
        version = Table(
            libs.cfg.DBT_VERSION,
            libs.cfg.metadata,
            autoload_with=libs.cfg.engine,
        )
        conn.execute(delete(version))

    with pytest.raises(SystemExit) as expt:
        libs.db.select_version_version_unique(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1

    libs.db.disconnect_db(LOGGER)


def test_select_version_unique_not_unique(fxtr_new_db_no_inbox):
    """Test: Column version not unique."""
    libs.db.insert_dbt_row(
        LOGGER, libs.cfg.DBT_VERSION, [{libs.cfg.DBC_VERSION: "0.0.0"}]
    )

    with pytest.raises(SystemExit) as expt:
        libs.db.select_version_version_unique(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1
