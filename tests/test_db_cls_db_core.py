# pylint: disable=unused-argument
"""Testing Module db.cls_db_core."""
import os
import pathlib
import shutil

import cfg.cls_setup
import cfg.glob
import db.cls_db_core
import db.cls_run
import launcher
import pytest
import sqlalchemy

import dcr_core.core_glob
import dcr_core.core_utils

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
        launcher.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    current_version = dcr_core.cls_setup.Setup.DCR_VERSION

    dcr_core.cls_setup.Setup.DCR_VERSION = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore()
        launcher.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    dcr_core.cls_setup.Setup.DCR_VERSION = current_version

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    dbt = sqlalchemy.Table(
        db.cls_db_core.DBCore.DBT_VERSION,
        cfg.glob.db_core.db_orm_metadata,
        autoload_with=cfg.glob.db_core.db_orm_engine,
    )

    dbt.drop()

    with pytest.raises(SystemExit) as expt:
        launcher.check_db_up_to_date()

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

    pytest.helpers.config_params_modify(
        config_section,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DB_CONNECTION_PORT, "9999"),
        ],
    )

    dcr_core.core_glob.setup = cfg.cls_setup.Setup()

    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore()

    assert expt.type == SystemExit, "DCR_CFG_DB_CONNECTION_PORT: no database"
    assert expt.value.code == 1, "DCR_CFG_DB_CONNECTION_PORT: no database"

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

    pytest.helpers.config_params_modify(
        config_section,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DB_CONNECTION_PORT, "9999"),
        ],
    )

    dcr_core.core_glob.setup = cfg.cls_setup.Setup()

    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)

    assert expt.type == SystemExit, "DCR_CFG_DB_CONNECTION_PORT: no database"
    assert expt.value.code == 1, "DCR_CFG_DB_CONNECTION_PORT: no database"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - create_database().
# -----------------------------------------------------------------------------
def test_create_database(fxtr_setup_logger_environment):
    """Test: create_database()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    # -------------------------------------------------------------------------
    pytest.helpers.config_param_delete(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT
    )

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT, dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    assert expt.type == SystemExit, "DCR_CFG_DB_DIALECT: unknown DB dialect"
    assert expt.value.code == 1, "DCR_CFG_DB_DIALECT: unknown DB dialect"

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DB_INITIAL_DATA_FILE, "unknown_file"),
        ],
    )

    with pytest.raises(SystemExit) as expt:
        launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    assert expt.type == SystemExit, "DCR_CFG_DB_INITIAL_DATA_FILE: unknown file"
    assert expt.value.code == 1, "DCR_CFG_DB_INITIAL_DATA_FILE: unknown file"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - drop_database().
# -----------------------------------------------------------------------------
def test_drop_database_01(fxtr_setup_empty_db_and_inbox):
    """Test: drop_database()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)

    cfg.glob.db_core._drop_database()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


def test_drop_database_02(fxtr_setup_empty_db_and_inbox):
    """Test: drop_database()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_param_delete(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST, cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT
    )

    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_CREATE_DB])

    cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)

    cfg.glob.db_core._drop_database()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


def test_drop_database_03(fxtr_setup_empty_db_and_inbox):
    """Test: drop_database()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT, dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE),
        ],
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup = cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core._drop_database()

    assert expt.type == SystemExit, "DCR_CFG_DB_DIALECT: unknown DB dialect"
    assert expt.value.code == 1, "DCR_CFG_DB_DIALECT: unknown DB dialect"

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT, db.cls_db_core.DBCore.DB_DIALECT_POSTGRESQL),
        ],
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.setup = cfg.cls_setup.Setup()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Load Database Data - disallowed database table.
# -----------------------------------------------------------------------------
def test_load_db_data_from_json_content(fxtr_setup_logger_environment):
    """Test Load Database Data - disallowed database table."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db_initial_data_file_path = pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)
    db_initial_data_file_path_directory = os.path.dirname(db_initial_data_file_path)
    db_initial_data_file_path_file_name = os.path.basename(db_initial_data_file_path)

    db_initial_data_file_path_file_name_test = "db_initial_data_file_content.json"

    # copy test file
    shutil.copy(
        dcr_core.core_utils.get_full_name(
            pytest.helpers.get_test_inbox_directory_name(), db_initial_data_file_path_file_name_test
        ),
        dcr_core.core_utils.get_full_name(db_initial_data_file_path_directory, db_initial_data_file_path_file_name),
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

    db_initial_data_file_path = pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)
    db_initial_data_file_path_directory = os.path.dirname(db_initial_data_file_path)
    db_initial_data_file_path_file_name = os.path.basename(db_initial_data_file_path)

    # delete original file
    if pathlib.Path(db_initial_data_file_path):
        os.remove(db_initial_data_file_path)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_core = db.cls_db_core.DBCore(is_admin=True)
        cfg.glob.db_core.create_database()

    # restore original file
    shutil.copy(
        dcr_core.core_utils.get_full_name(
            pytest.helpers.get_test_inbox_directory_name(), db_initial_data_file_path_file_name
        ),
        db_initial_data_file_path_directory,
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
    db_initial_data_file_path = pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)
    db_initial_data_file_path_directory = os.path.dirname(db_initial_data_file_path)
    db_initial_data_file_path_file_name = os.path.basename(db_initial_data_file_path)

    db_initial_data_file_path_file_name_test = "db_initial_data_file_unknown.json"

    # copy test file
    shutil.copy(
        dcr_core.core_utils.get_full_name(
            pytest.helpers.get_test_inbox_directory_name(), db_initial_data_file_path_file_name_test
        ),
        dcr_core.core_utils.get_full_name(db_initial_data_file_path_directory, db_initial_data_file_path_file_name),
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
    db_initial_data_file_path = pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)
    db_initial_data_file_path_directory = os.path.dirname(db_initial_data_file_path)
    db_initial_data_file_path_file_name = os.path.basename(db_initial_data_file_path)

    db_initial_data_file_path_file_name_test = "db_initial_data_file_version.json"

    # copy test file
    shutil.copy(
        dcr_core.core_utils.get_full_name(
            pytest.helpers.get_test_inbox_directory_name(), db_initial_data_file_path_file_name_test
        ),
        dcr_core.core_utils.get_full_name(db_initial_data_file_path_directory, db_initial_data_file_path_file_name),
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
    launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_UPGRADE_DB])

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    update_version_version("0.5.0")

    cfg.glob.db_core.disconnect_db()

    with pytest.raises(SystemExit) as expt:
        launcher.main([launcher.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_UPGRADE_DB])

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
