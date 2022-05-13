# pylint: disable=unused-argument
"""Testing Module db.driver."""
import cfg.cls_setup
import cfg.glob
import db.cls_run
import db.dml
import db.driver
import pytest
import sqlalchemy

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - connect_db().
# -----------------------------------------------------------------------------
def test_connect_db(fxtr_setup_logger_environment):
    """Test: connect_db()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    config_section = cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST

    values_original = pytest.helpers.backup_config_params(
        config_section,
        [
            (cfg.glob.setup._DCR_CFG_DB_CONNECTION_PORT, "9999"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    with pytest.raises(SystemExit) as expt:
        db.driver.connect_db()

    assert expt.type == SystemExit, "DCR_CFG_DB_CONNECTION_PORT: no database"
    assert expt.value.code == 1, "DCR_CFG_DB_CONNECTION_PORT: no database"

    pytest.helpers.restore_config_params(
        config_section,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - connect_db_admin().
# -----------------------------------------------------------------------------
def test_connect_db_admin(fxtr_setup_logger_environment):
    """Test: connect_db_admin()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    config_section = cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST

    values_original = pytest.helpers.backup_config_params(
        config_section,
        [
            (cfg.glob.setup._DCR_CFG_DB_CONNECTION_PORT, "9999"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    with pytest.raises(SystemExit) as expt:
        db.driver.connect_db_admin()

    assert expt.type == SystemExit, "DCR_CFG_DB_CONNECTION_PORT: no database"
    assert expt.value.code == 1, "DCR_CFG_DB_CONNECTION_PORT: no database"

    pytest.helpers.restore_config_params(
        config_section,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - create_database().
# -----------------------------------------------------------------------------
def test_create_database(fxtr_setup_logger_environment):
    """Test: create_database()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_DB_DIALECT
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DB_DIALECT, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    assert expt.type == SystemExit, "DCR_CFG_DB_DIALECT: unknown DB dialect"
    assert expt.value.code == 1, "DCR_CFG_DB_DIALECT: unknown DB dialect"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_INITIAL_DATABASE_DATA, "unknown_file"),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    assert expt.type == SystemExit, "DCR_CFG_INITIAL_DATABASE_DATA: unknown file"
    assert expt.value.code == 1, "DCR_CFG_INITIAL_DATABASE_DATA: unknown file"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test disconnect without 'db_orm_engine' and 'db_orm_metadata'.
# -----------------------------------------------------------------------------
def test_disconnect(fxtr_setup_empty_db_and_inbox):
    """Test disconnect without 'db_orm_engine' and 'db_orm_metadata'."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE, "true"),
        ],
    )

    db.driver.connect_db()

    cfg.glob.db_current_database = None
    cfg.glob.db_current_user = None

    db.driver.disconnect_db()

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test disconnect without 'db_orm_engine' and 'db_orm_metadata'.
# -----------------------------------------------------------------------------
def test_disconnect_both(fxtr_setup_empty_db_and_inbox):
    """Test disconnect without 'db_orm_engine' and 'db_orm_metadata'."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    cfg.glob.db_orm_engine = None
    cfg.glob.db_orm_metadata = None

    db.driver.disconnect_db()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test disconnect without 'db_orm_engine'.
# -----------------------------------------------------------------------------
def test_disconnect_db_orm_engine(fxtr_setup_empty_db_and_inbox):
    """Test disconnect without 'db_orm_engine'."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    cfg.glob.db_orm_engine = None

    db.driver.disconnect_db()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test disconnect without 'db_orm_metadata'.
# -----------------------------------------------------------------------------
def test_disconnect_db_orm_metadata(fxtr_setup_empty_db_and_inbox):
    """Test disconnect without 'db_orm_metadata'."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    cfg.glob.db_orm_metadata = None

    db.driver.disconnect_db()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - drop_database().
# -----------------------------------------------------------------------------
def test_drop_database(fxtr_setup_logger_environment):
    """Test: drop_database()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])
    db.driver.drop_database()

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.glob.setup._DCR_CFG_SECTION, cfg.glob.setup._DCR_CFG_DB_DIALECT
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])
    db.driver.drop_database()

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DB_DIALECT, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    with pytest.raises(SystemExit) as expt:
        db.driver.drop_database()

    assert expt.type == SystemExit, "DCR_CFG_DB_DIALECT: unknown DB dialect"
    assert expt.value.code == 1, "DCR_CFG_DB_DIALECT: unknown DB dialect"

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - upgrade_database().
# -----------------------------------------------------------------------------
def test_upgrade_database(fxtr_setup_empty_db_and_inbox):
    """Test: upgrade_database()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_UPGRADE_DB])

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    update_version_version("0.5.0")

    db.driver.disconnect_db()

    with pytest.raises(SystemExit) as expt:
        dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_UPGRADE_DB])

    assert expt.type == SystemExit, "Version < '1.0.0' not supported"
    assert expt.value.code == 1, "Version < '1.0.0' not supported"

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    update_version_version("0.0.0")

    db.driver.disconnect_db()

    with pytest.raises(SystemExit) as expt:
        dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_UPGRADE_DB])

    assert expt.type == SystemExit, "Version unknown"
    assert expt.value.code == 1, "Version unknown"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    dbt = sqlalchemy.Table(
        cfg.glob.DBT_VERSION,
        cfg.glob.db_orm_metadata,
        autoload_with=cfg.glob.db_orm_engine,
    )

    with cfg.glob.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(
            sqlalchemy.update(dbt).values(
                {
                    cfg.glob.DBC_VERSION: version,
                }
            )
        )
        conn.close()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
