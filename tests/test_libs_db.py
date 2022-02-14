# pylint: disable=unused-argument
"""Testing Module libs.db."""

import libs.cfg
import libs.db
import pytest
from sqlalchemy import Table
from sqlalchemy import delete

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
dcr.initialise_logger()


# -----------------------------------------------------------------------------
# Test Function - check_db_up_to_date().
# -----------------------------------------------------------------------------
def test_check_db_up_to_date_wrong_version(fxtr_new_db_no_inbox):
    """Test: Wrong database version."""
    libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION] = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        libs.db.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_unique_not_found(fxtr_new_db_no_inbox):
    """Test: Column version not found."""
    libs.db.connect_db()

    with libs.cfg.engine.begin() as conn:
        version = Table(
            libs.db.DBT_VERSION,
            libs.cfg.metadata,
            autoload_with=libs.cfg.engine,
        )
        conn.execute(delete(version))

    with pytest.raises(SystemExit) as expt:
        libs.db.select_version_version_unique()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    libs.db.disconnect_db()


def test_select_version_unique_not_unique(fxtr_new_db_no_inbox):
    """Test: Column version not unique."""
    libs.db.insert_dbt_row(
        libs.db.DBT_VERSION, [{libs.db.DBC_VERSION: "0.0.0"}]
    )

    with pytest.raises(SystemExit) as expt:
        libs.db.select_version_version_unique()

    assert expt.type == SystemExit
    assert expt.value.code == 1
