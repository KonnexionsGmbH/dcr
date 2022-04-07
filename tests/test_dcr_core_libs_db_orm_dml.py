# pylint: disable=unused-argument
"""Testing Module dcr_core.libs.db.orm.dml."""
import libs.cfg
import libs.db.cfg
import libs.db.driver
import libs.db.orm.connection
import libs.db.orm.dml
import libs.utils
import pytest
from sqlalchemy import Table

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Database Version - Wrong version number in configuration.
# -----------------------------------------------------------------------------
def test_check_db_up_to_date(fxtr_setup_empty_db_and_inbox):
    """Test Database Version - Wrong version number in configuration."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    current_version = libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]

    libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION] = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        libs.db.orm.connection.connect_db()
        dcr.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION] = current_version

    # -------------------------------------------------------------------------
    libs.db.orm.connection.connect_db()

    dbt = Table(
        libs.db.cfg.DBT_VERSION,
        libs.db.cfg.db_orm_metadata,
        autoload_with=libs.db.cfg.db_orm_engine,
    )

    dbt.drop()

    with pytest.raises(SystemExit) as expt:
        dcr.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    libs.db.orm.connection.connect_db()

    libs.db.orm.dml.insert_dbt_row(libs.db.cfg.DBT_VERSION, {libs.db.cfg.DBC_VERSION: "0.0.0"})

    with pytest.raises(SystemExit) as expt:
        libs.db.orm.dml.select_version_version_unique()

    libs.db.orm.connection.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (orm)"
    assert expt.value.code == 1, "Version not unique (orm)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    libs.db.orm.connection.connect_db()

    with pytest.raises(SystemExit) as expt:
        libs.db.orm.dml.select_version_version_unique()

    libs.db.orm.connection.disconnect_db()

    assert expt.type == SystemExit, "Version missing (orm)"
    assert expt.value.code == 1, "Version missing (orm)"

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
