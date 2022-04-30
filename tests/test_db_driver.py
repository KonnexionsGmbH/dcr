# pylint: disable=unused-argument
"""Testing Module db.driver."""
import db.cfg
import db.driver
import db.orm.dml
import libs.cfg
import pytest
import setup.config
import sqlalchemy

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - create_database().
# -----------------------------------------------------------------------------
def test_create_database(fxtr_setup_logger_environment):
    """Test: create_database()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION, libs.cfg.config._DCR_CFG_DB_DIALECT
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_DB_DIALECT, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    assert expt.type == SystemExit, "DCR_CFG_DB_DIALECT: unknown DB dialect"
    assert expt.value.code == 1, "DCR_CFG_DB_DIALECT: unknown DB dialect"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_INITIAL_DATABASE_DATA, "unknown_file"),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    assert expt.type == SystemExit, "DCR_CFG_INITIAL_DATABASE_DATA: unknown file"
    assert expt.value.code == 1, "DCR_CFG_INITIAL_DATABASE_DATA: unknown file"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - drop_database().
# -----------------------------------------------------------------------------
def test_drop_database(fxtr_setup_logger_environment):
    """Test: drop_database()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])
    db.driver.drop_database()

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        libs.cfg.config._DCR_CFG_SECTION, libs.cfg.config._DCR_CFG_DB_DIALECT
    )

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])
    db.driver.drop_database()

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        [
            (libs.cfg.config._DCR_CFG_DB_DIALECT, libs.cfg.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    libs.cfg.config = setup.config.Config()

    with pytest.raises(SystemExit) as expt:
        db.driver.drop_database()

    assert expt.type == SystemExit, "DCR_CFG_DB_DIALECT: unknown DB dialect"
    assert expt.value.code == 1, "DCR_CFG_DB_DIALECT: unknown DB dialect"

    pytest.helpers.restore_config_params(
        libs.cfg.config._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    db.orm.dml.insert_dbt_row(db.cfg.DBT_VERSION, {db.cfg.DBC_VERSION: "0.0.0"})

    db.driver.disconnect_db()

    db.driver.connect_db()

    db.cfg.db_driver_cur = db.cfg.db_driver_conn.cursor()

    with pytest.raises(SystemExit) as expt:
        db.orm.dml.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (driver)"
    assert expt.value.code == 1, "Version not unique (driver)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    db.driver.connect_db()

    db.cfg.db_driver_cur = db.cfg.db_driver_conn.cursor()

    with pytest.raises(SystemExit) as expt:
        db.orm.dml.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version missing (driver)"
    assert expt.value.code == 1, "Version missing (driver)"

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - upgrade_database().
# -----------------------------------------------------------------------------
def test_upgrade_database(fxtr_setup_empty_db_and_inbox):
    """Test: upgrade_database()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    update_version_version("0.5.0")

    db.driver.disconnect_db()

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    assert expt.type == SystemExit, "Version < '1.0.0' not supported"
    assert expt.value.code == 1, "Version < '1.0.0' not supported"

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    update_version_version("0.0.0")

    db.driver.disconnect_db()

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    assert expt.type == SystemExit, "Version unknown"
    assert expt.value.code == 1, "Version unknown"

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Update the database version number.
# -----------------------------------------------------------------------------
def update_version_version(
    version: str,
) -> None:
    """Update the database version number in database table version.

    Args:
        version (str): New version number.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = sqlalchemy.Table(
        db.cfg.DBT_VERSION,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    with db.cfg.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(
            sqlalchemy.update(dbt).values(
                {
                    db.cfg.DBC_VERSION: version,
                }
            )
        )
        conn.close()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
