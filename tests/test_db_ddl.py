# pylint: disable=unused-argument
"""Testing Module db.ddl."""
import os
import pathlib
import shutil

import cfg.glob
import db.ddl
import db.driver
import pytest
import utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


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
        db.driver.create_database()

    # restore original file
    shutil.copy(
        utils.get_full_name(pytest.helpers.get_test_inbox_directory_name(), initial_database_data_path_file_name),
        initial_database_data_path_directory,
    )

    assert expt.type == SystemExit, "Initial database data file is missing."
    assert expt.value.code == 1, "Initial database data file is missing."

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
