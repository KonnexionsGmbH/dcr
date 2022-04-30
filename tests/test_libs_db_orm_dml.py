# pylint: disable=unused-argument
"""Testing Module db.dml."""
import db.cfg
import db.dml
import db.driver
import libs.cfg
import libs.utils
import pytest
import sqlalchemy

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
    current_version = libs.cfg.config.dcr_version

    libs.cfg.config.dcr_version = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        db.driver.connect_db()
        dcr.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    libs.cfg.config.dcr_version = current_version

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    dbt = sqlalchemy.Table(
        db.cfg.DBT_VERSION,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
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
    db.driver.connect_db()

    db.dml.insert_dbt_row(db.cfg.DBT_VERSION, {db.cfg.DBC_VERSION: "0.0.0"})

    with pytest.raises(SystemExit) as expt:
        db.dml.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (orm)"
    assert expt.value.code == 1, "Version not unique (orm)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.dml.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version missing (orm)"
    assert expt.value.code == 1, "Version missing (orm)"

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
