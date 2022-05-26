# pylint: disable=unused-argument
"""Testing Module db.dml."""
import os
import pathlib
import shutil

import cfg.glob
import db.dml
import db.driver
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
    with pytest.raises(SystemExit) as expt:
        dcr.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    current_version = cfg.glob.setup.dcr_version

    cfg.glob.setup.dcr_version = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        db.driver.connect_db()
        dcr.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    cfg.glob.setup.dcr_version = current_version

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    dbt = sqlalchemy.Table(
        cfg.glob.DBT_VERSION,
        cfg.glob.db_orm_metadata,
        autoload_with=cfg.glob.db_orm_engine,
    )

    dbt.drop()

    with pytest.raises(SystemExit) as expt:
        dcr.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1

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
        db.driver.create_database()

    assert expt.type == SystemExit
    assert expt.value.code == 1

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
        db.driver.create_database()

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
        db.driver.create_database()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
