# pylint: disable=unused-argument
"""Testing Module database."""

import pytest
from libs import cfg
from libs import db
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
    cfg.config[cfg.DCR_CFG_DCR_VERSION] = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        db.check_db_up_to_date(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_unique_not_found(fxtr_new_db_no_inbox):
    """Test: Column version not found."""
    db.connect_db(LOGGER)

    with cfg.engine.begin() as conn:
        version = Table(
            cfg.DBT_VERSION, cfg.metadata, autoload_with=cfg.engine
        )
        conn.execute(delete(version))

    with pytest.raises(SystemExit) as expt:
        db.select_version_version_unique(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1

    db.disconnect_db(LOGGER)


def test_select_version_unique_not_unique(fxtr_new_db_no_inbox):
    """Test: Column version not unique."""
    db.insert_dbt_row(LOGGER, cfg.DBT_VERSION, [{cfg.DBC_VERSION: "0.0.0"}])

    with pytest.raises(SystemExit) as expt:
        db.select_version_version_unique(LOGGER)

    assert expt.type == SystemExit
    assert expt.value.code == 1
