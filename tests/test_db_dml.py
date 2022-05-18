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
def test_load_db_data_from_json_content(fxtr_setup_empty_db_and_inbox):
    """Test Load Database Data - disallowed database table."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    initial_database_data_path = pathlib.Path(cfg.glob.setup.initial_database_data)
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    initial_database_data_path_file_name_test = "initial_database_data_content.json"

    # backup original file
    shutil.copy(initial_database_data_path, cfg.glob.TESTS_INBOX_NAME)
    # copy test file
    shutil.copy(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, initial_database_data_path_file_name_test),
        os.path.join(initial_database_data_path_directory, initial_database_data_path_file_name),
    )

    with pytest.raises(SystemExit) as expt:
        db.driver.connect_db()
        db.dml.load_db_data_from_json(initial_database_data_path)

    # restore original file
    shutil.copy(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, initial_database_data_path_file_name),
        initial_database_data_path_directory,
    )

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Load Database Data - initial database data is missing.
# -----------------------------------------------------------------------------
def test_load_db_data_from_json_missing(fxtr_setup_empty_db_and_inbox):
    """Test Load Database Data - initial database data is missing."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    initial_database_data_path = pathlib.Path(cfg.glob.setup.initial_database_data)
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    # backup original file
    shutil.copy(initial_database_data_path, cfg.glob.TESTS_INBOX_NAME)
    # delete original file
    shutil.rmtree(
        os.path.join(initial_database_data_path_directory, initial_database_data_path_file_name),
    )

    with pytest.raises(SystemExit) as expt:
        db.driver.connect_db()
        db.dml.load_db_data_from_json(initial_database_data_path)

    # restore original file
    shutil.copy(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, initial_database_data_path_file_name),
        initial_database_data_path_directory,
    )

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Load Database Data - unknown database table.
# -----------------------------------------------------------------------------
def test_load_db_data_from_json_unknown(fxtr_setup_empty_db_and_inbox):
    """Test Load Database Data - unknown database table."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    initial_database_data_path = pathlib.Path(cfg.glob.setup.initial_database_data)
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    initial_database_data_path_file_name_test = "initial_database_data_unknown.json"

    # backup original file
    shutil.copy(initial_database_data_path, cfg.glob.TESTS_INBOX_NAME)
    # copy test file
    shutil.copy(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, initial_database_data_path_file_name_test),
        os.path.join(initial_database_data_path_directory, initial_database_data_path_file_name),
    )

    with pytest.raises(SystemExit) as expt:
        db.driver.connect_db()
        db.dml.load_db_data_from_json(initial_database_data_path)

    # restore original file
    shutil.copy(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, initial_database_data_path_file_name),
        initial_database_data_path_directory,
    )

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Load Database Data - unexpected api version.
# -----------------------------------------------------------------------------
def test_load_db_data_from_json_version(fxtr_setup_empty_db_and_inbox):
    """Test Load Database Data - unexpected api version."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    initial_database_data_path = pathlib.Path(cfg.glob.setup.initial_database_data)
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    initial_database_data_path_file_name_test = "initial_database_data_version.json"

    # backup original file
    shutil.copy(initial_database_data_path, cfg.glob.TESTS_INBOX_NAME)
    # copy test file
    shutil.copy(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, initial_database_data_path_file_name_test),
        os.path.join(initial_database_data_path_directory, initial_database_data_path_file_name),
    )

    with pytest.raises(SystemExit) as expt:
        db.driver.connect_db()
        db.dml.load_db_data_from_json(initial_database_data_path)

    # restore original file
    shutil.copy(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, initial_database_data_path_file_name),
        initial_database_data_path_directory,
    )

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
