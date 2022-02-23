# pylint: disable=unused-argument
"""Testing Module libs.db.driver."""

import libs.cfg
import libs.db.cfg
import libs.db.driver
import libs.db.orm
import pytest
from sqlalchemy import Table
from sqlalchemy import delete

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - connect_db().
# -----------------------------------------------------------------------------
def test_connect_db(fxtr_setup_logger_environment):
    """Test: connect_db()."""
    # -------------------------------------------------------------------------
    config_section = libs.cfg.DCR_CFG_SECTION_TEST
    config_param = libs.cfg.DCR_CFG_DB_CONNECTION_PORT

    value_original = pytest.helpers.store_config_param(config_section, config_param, "9999")

    dcr.get_config()

    with pytest.raises(SystemExit) as expt:
        libs.db.driver.connect_db()

    assert expt.type == SystemExit, "DCR_CFG_DB_CONNECTION_PORT: no database"
    assert expt.value.code == 1, "DCR_CFG_DB_CONNECTION_PORT: no database"

    pytest.helpers.restore_config_param(config_section, config_param, value_original)


# -----------------------------------------------------------------------------
# Test Function - connect_db_admin().
# -----------------------------------------------------------------------------
def test_connect_db_admin(fxtr_setup_logger_environment):
    """Test: connect_db_admin()."""
    # -------------------------------------------------------------------------
    config_section = libs.cfg.DCR_CFG_SECTION_TEST
    config_param = libs.cfg.DCR_CFG_DB_CONNECTION_PORT

    value_original = pytest.helpers.store_config_param(config_section, config_param, "9999")

    dcr.get_config()

    with pytest.raises(SystemExit) as expt:
        libs.db.driver.connect_db_admin()

    assert expt.type == SystemExit, "DCR_CFG_DB_CONNECTION_PORT: no database"
    assert expt.value.code == 1, "DCR_CFG_DB_CONNECTION_PORT: no database"

    pytest.helpers.restore_config_param(config_section, config_param, value_original)


# -----------------------------------------------------------------------------
# Test Function - create_database().
# -----------------------------------------------------------------------------
def test_create_database(fxtr_setup_logger_environment):
    """Test: create_database()."""
    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    # -------------------------------------------------------------------------
    config_section = libs.cfg.DCR_CFG_SECTION
    config_param = libs.cfg.DCR_CFG_DB_DIALECT

    value_original = pytest.helpers.delete_config_param(config_section, config_param)

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    pytest.helpers.restore_config_param(config_section, config_param, value_original)

    # -------------------------------------------------------------------------
    config_section = libs.cfg.DCR_CFG_SECTION
    config_param = libs.cfg.DCR_CFG_DB_DIALECT

    value_original = pytest.helpers.store_config_param(config_section, config_param, "n/a")

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    assert expt.type == SystemExit, "DCR_CFG_DB_DIALECT: unknown DB dialect"
    assert expt.value.code == 1, "DCR_CFG_DB_DIALECT: unknown DB dialect"

    pytest.helpers.restore_config_param(config_section, config_param, value_original)


# -----------------------------------------------------------------------------
# Test Function - drop_database().
# -----------------------------------------------------------------------------
def test_drop_database(fxtr_setup_logger_environment):
    """Test: drop_database()."""
    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])
    libs.db.driver.drop_database()

    # -------------------------------------------------------------------------
    config_section = libs.cfg.DCR_CFG_SECTION
    config_param = libs.cfg.DCR_CFG_DB_DIALECT

    value_original = pytest.helpers.delete_config_param(config_section, config_param)

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])
    libs.db.driver.drop_database()

    pytest.helpers.restore_config_param(config_section, config_param, value_original)

    # -------------------------------------------------------------------------
    config_section = libs.cfg.DCR_CFG_SECTION
    config_param = libs.cfg.DCR_CFG_DB_DIALECT

    value_original = pytest.helpers.store_config_param(config_section, config_param, "n/a")

    dcr.get_config()

    with pytest.raises(SystemExit) as expt:
        libs.db.driver.drop_database()

    assert expt.type == SystemExit, "DCR_CFG_DB_DIALECT: unknown DB dialect"
    assert expt.value.code == 1, "DCR_CFG_DB_DIALECT: unknown DB dialect"

    pytest.helpers.restore_config_param(config_section, config_param, value_original)


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    # -------------------------------------------------------------------------
    libs.db.orm.connect_db()

    libs.db.orm.insert_dbt_row(libs.db.cfg.DBT_VERSION, {libs.db.cfg.DBC_VERSION: "0.0.0"})

    with pytest.raises(SystemExit) as expt:
        libs.db.orm.select_version_version_unique()

    assert expt.type == SystemExit, "Version not unique"
    assert expt.value.code == 1, "Version not unique"

    libs.db.orm.disconnect_db()

    # -------------------------------------------------------------------------
    libs.db.orm.connect_db()

    with libs.db.cfg.db_orm_engine.begin() as conn:
        version = Table(
            libs.db.cfg.DBT_VERSION,
            libs.db.cfg.db_orm_metadata,
            autoload_with=libs.db.cfg.db_orm_engine,
        )
        conn.execute(delete(version))

    with pytest.raises(SystemExit) as expt:
        libs.db.orm.select_version_version_unique()

    assert expt.type == SystemExit, "Version missing"
    assert expt.value.code == 1, "Version missing"

    libs.db.orm.disconnect_db()


# -----------------------------------------------------------------------------
# Test Function - upgrade_database().
# -----------------------------------------------------------------------------
def test_upgrade_database(fxtr_setup_empty_db_and_inbox):
    """Test: upgrade_database()."""
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    # -------------------------------------------------------------------------
    libs.db.orm.connect_db()

    libs.db.orm.update_version_version("0.5.0")

    libs.db.orm.disconnect_db()

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    assert expt.type == SystemExit, "Version < '1.0.0' not supported"
    assert expt.value.code == 1, "Version < '1.0.0' not supported"

    libs.db.orm.disconnect_db()

    # -------------------------------------------------------------------------
    libs.db.orm.connect_db()

    libs.db.orm.update_version_version("0.0.0")

    libs.db.orm.disconnect_db()

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    assert expt.type == SystemExit, "Version unknown"
    assert expt.value.code == 1, "Version unknown"