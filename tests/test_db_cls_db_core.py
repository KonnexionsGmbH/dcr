# pylint: disable=unused-argument
"""Testing Module db.cls_db_core."""
import os
import pathlib
import shutil

import cfg.cls_setup
import cfg.glob
import db.cls_db_core
import db.cls_run
import pytest
import sqlalchemy
import utils

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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    cfg.glob.db_core.db_orm_engine = None

    with pytest.raises(SystemExit) as expt:
        dcr.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    current_version = cfg.cls_setup.Setup.DCR_VERSION

    cfg.cls_setup.Setup.DCR_VERSION = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore()
        dcr.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    cfg.cls_setup.Setup.DCR_VERSION = current_version

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    dbt = sqlalchemy.Table(
        db.cls_db_core.DBCore.DBT_VERSION,
        cfg.glob.db_core.db_orm_metadata,
        autoload_with=cfg.glob.db_core.db_orm_engine,
    )

    dbt.drop()

    with pytest.raises(SystemExit) as expt:
        dcr.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - connect_db().
# -----------------------------------------------------------------------------
def test_connect_db(fxtr_setup_logger_environment):
    """Test: connect_db()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    config_section = cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST

    values_original = pytest.helpers.backup_config_params(
        config_section,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DB_CONNECTION_PORT, "9999"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore()

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
    config_section = cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST

    values_original = pytest.helpers.backup_config_params(
        config_section,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DB_CONNECTION_PORT, "9999"),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)

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
    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    assert expt.type == SystemExit, "DCR_CFG_DB_DIALECT: unknown DB dialect"
    assert expt.value.code == 1, "DCR_CFG_DB_DIALECT: unknown DB dialect"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_INITIAL_DATABASE_DATA, "unknown_file"),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    assert expt.type == SystemExit, "DCR_CFG_INITIAL_DATABASE_DATA: unknown file"
    assert expt.value.code == 1, "DCR_CFG_INITIAL_DATABASE_DATA: unknown file"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - drop_database().
# -----------------------------------------------------------------------------
def test_drop_database(fxtr_setup_logger_environment):
    """Test: drop_database()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)

    cfg.glob.db_core._drop_database()

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.delete_config_param(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)

    cfg.glob.db_core._drop_database()

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT, cfg.glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    cfg.glob.setup = cfg.cls_setup.Setup()

    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core._drop_database()

    assert expt.type == SystemExit, "DCR_CFG_DB_DIALECT: unknown DB dialect"
    assert expt.value.code == 1, "DCR_CFG_DB_DIALECT: unknown DB dialect"

    pytest.helpers.restore_config_params(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Load Database Data - disallowed database table.
# -----------------------------------------------------------------------------
def test_load_db_data_from_json_content(fxtr_setup_logger_environment):
    """Test Load Database Data - disallowed database table."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    initial_database_data_path = pathlib.Path(cfg.glob.setup.initial_database_data)
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    initial_database_data_path_file_name_test = "initial_database_data_content.json"

    # copy test file
    shutil.copy(
        utils.get_full_name(pytest.helpers.get_test_inbox_directory_name(), initial_database_data_path_file_name_test),
        utils.get_full_name(initial_database_data_path_directory, initial_database_data_path_file_name),
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)
        cfg.glob.db_core.create_database()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Load Database Data - initial database data file is missing.
# -----------------------------------------------------------------------------
def test_load_db_data_from_json_missing(fxtr_setup_logger_environment):
    """Test Load Database Data - initial database data is missing."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    initial_database_data_path = pathlib.Path(cfg.glob.setup.initial_database_data)
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    # delete original file
    if pathlib.Path(initial_database_data_path):
        os.remove(initial_database_data_path)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)
        cfg.glob.db_core.create_database()

    # restore original file
    shutil.copy(
        utils.get_full_name(pytest.helpers.get_test_inbox_directory_name(), initial_database_data_path_file_name),
        initial_database_data_path_directory,
    )

    assert expt.type == SystemExit, "Initial database data file is missing."
    assert expt.value.code == 1, "Initial database data file is missing."

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Load Database Data - unknown database table.
# -----------------------------------------------------------------------------
def test_load_db_data_from_json_unknown(fxtr_setup_logger_environment):
    """Test Load Database Data - unknown database table."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    initial_database_data_path = pathlib.Path(cfg.glob.setup.initial_database_data)
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    initial_database_data_path_file_name_test = "initial_database_data_unknown.json"

    # copy test file
    shutil.copy(
        utils.get_full_name(pytest.helpers.get_test_inbox_directory_name(), initial_database_data_path_file_name_test),
        utils.get_full_name(initial_database_data_path_directory, initial_database_data_path_file_name),
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)
        cfg.glob.db_core.create_database()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Load Database Data - unexpected api version.
# -----------------------------------------------------------------------------
def test_load_db_data_from_json_version(fxtr_setup_logger_environment):
    """Test Load Database Data - unexpected api version."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    initial_database_data_path = pathlib.Path(cfg.glob.setup.initial_database_data)
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    initial_database_data_path_file_name_test = "initial_database_data_version.json"

    # copy test file
    shutil.copy(
        utils.get_full_name(pytest.helpers.get_test_inbox_directory_name(), initial_database_data_path_file_name_test),
        utils.get_full_name(initial_database_data_path_directory, initial_database_data_path_file_name),
    )

    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)
        cfg.glob.db_core.create_database()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - upgrade_database().
# -----------------------------------------------------------------------------
def test_upgrade_database(fxtr_setup_empty_db_and_inbox):
    """Test: upgrade_database()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_UPGRADE_DB])

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    update_version_version("0.5.0")

    cfg.glob.db_core.disconnect_db()

    with pytest.raises(SystemExit) as expt:
        dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_UPGRADE_DB])

    assert expt.type == SystemExit, "Version < '1.0.0' not supported"
    assert expt.value.code == 1, "Version < '1.0.0' not supported"

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
        db.cls_db_core.DBCore.DBT_VERSION,
        cfg.glob.db_core.db_orm_metadata,
        autoload_with=cfg.glob.db_core.db_orm_engine,
    )

    with cfg.glob.db_core.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(
            sqlalchemy.update(dbt).values(
                {
                    db.cls_db_core.DBCore.DBC_VERSION: version,
                }
            )
        )
        conn.close()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
