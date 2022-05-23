# pylint: disable=unused-argument
"""Testing Module db.cls_version"""
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
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique_driver(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    db.dml.insert_dbt_row(cfg.glob.DBT_VERSION, {cfg.glob.DBC_VERSION: "0.0.0"})

    db.driver.disconnect_db()

    db.driver.connect_db()

    cfg.glob.db_driver_cur = cfg.glob.db_driver_conn.cursor()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (driver)"
    assert expt.value.code == 1, "Version not unique (driver)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    db.driver.connect_db()

    cfg.glob.db_driver_cur = cfg.glob.db_driver_conn.cursor()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version missing (driver)"
    assert expt.value.code == 1, "Version missing (driver)"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique_orm(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    db.dml.insert_dbt_row(cfg.glob.DBT_VERSION, {cfg.glob.DBC_VERSION: "0.0.0"})

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (orm)"
    assert expt.value.code == 1, "Version not unique (orm)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version missing (orm)"
    assert expt.value.code == 1, "Version missing (orm)"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
