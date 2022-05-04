# pylint: disable=unused-argument
"""Testing Module db.ddl."""
import os.path
import pathlib
import shutil

import cfg.glob
import db.ddl
import db.driver
import pytest

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


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
        db.ddl.load_db_data_from_json(initial_database_data_path)

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
        db.ddl.load_db_data_from_json(initial_database_data_path)

    # restore original file
    shutil.copy(
        os.path.join(cfg.glob.TESTS_INBOX_NAME, initial_database_data_path_file_name),
        initial_database_data_path_directory,
    )

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
