# pylint: disable=unused-argument
"""Testing Module dcr_core.libs.db.orm.ddl."""
import os.path
import shutil
from pathlib import Path

import libs.cfg
import libs.db.cfg
import libs.db.driver
import libs.db.orm.connection
import libs.db.orm.ddl
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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    initial_database_data_path = Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA])
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    initial_database_data_path_file_name_test = "initial_database_data_content.json"

    # backup original file
    shutil.copy(initial_database_data_path, libs.cfg.TESTS_INBOX_NAME)
    # copy test file
    shutil.copy(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, initial_database_data_path_file_name_test),
        os.path.join(initial_database_data_path_directory, initial_database_data_path_file_name),
    )

    with pytest.raises(SystemExit) as expt:
        libs.db.orm.ddl.load_db_data_from_json(initial_database_data_path)

    # restore original file
    shutil.copy(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, initial_database_data_path_file_name),
        initial_database_data_path_directory,
    )

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Load Database Data - unknown database table.
# -----------------------------------------------------------------------------
def test_load_db_data_from_json_unknown(fxtr_setup_empty_db_and_inbox):
    """Test Load Database Data - unknown database table."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    initial_database_data_path = Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA])
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    initial_database_data_path_file_name_test = "initial_database_data_unknown.json"

    # backup original file
    shutil.copy(initial_database_data_path, libs.cfg.TESTS_INBOX_NAME)
    # copy test file
    shutil.copy(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, initial_database_data_path_file_name_test),
        os.path.join(initial_database_data_path_directory, initial_database_data_path_file_name),
    )

    with pytest.raises(SystemExit) as expt:
        libs.db.orm.ddl.load_db_data_from_json(initial_database_data_path)

    # restore original file
    shutil.copy(
        os.path.join(libs.cfg.TESTS_INBOX_NAME, initial_database_data_path_file_name),
        initial_database_data_path_directory,
    )

    assert expt.type == SystemExit
    assert expt.value.code == 1

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
