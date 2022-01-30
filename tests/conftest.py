"""
### Module: **Test Configuration and Fixtures**.

Setup test configurations and store fixtures.
"""

import os
import shutil

import pytest
from app import get_config
from app import initialise_logger
from app import main
from libs.globals import ACTION_DB_CREATE_OR_UPGRADE
from libs.globals import CONFIG
from libs.globals import DCR_CFG_DATABASE_FILE
from libs.utils import print_fixture_end
from libs.utils import print_fixture_start

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
DCR_ARGV_0 = "src/dcr/app.py"

LOGGER = initialise_logger()


# -----------------------------------------------------------------------------
# Fixture - Create new database.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_create_new_db(fxtr_remove_opt):
    """#### Fixture: **Create a new database**."""
    print_fixture_start("fxtr_create_new_db")

    get_config(LOGGER)

    fxtr_remove_opt(CONFIG[DCR_CFG_DATABASE_FILE])

    main([DCR_ARGV_0, ACTION_DB_CREATE_OR_UPGRADE])

    print_fixture_end("fxtr_create_new_db")


# -----------------------------------------------------------------------------
# Fixture - Create a new directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_mkdir():
    """#### Fixture Factory: **Create a new directory**."""

    def _fxtr_mkdir(directory_name: str):
        """
        #### Fixture: **Create a new directory**.

        **Args**:
        - **directory_name (str)**: Directory name including path.
        """
        print_fixture_start("fxtr_mkdir")
        os.mkdir(directory_name)
        print_fixture_end("fxtr_mkdir")

    return _fxtr_mkdir


# -----------------------------------------------------------------------------
# Fixture - Create a new directory if not existing.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_mkdir_opt(fxtr_mkdir):
    """#### Fixture Factory: **Create a new directory if not existing**."""

    def _fxtr_mkdir_opt(directory_name: str):
        """
        #### Fixture: **Create a new directory if not existing**.

        **Args**:
        - **directory_name (str)**: Directory name including path.
        """
        print_fixture_start("fxtr_mkdir_opt")
        if not os.path.isdir(directory_name):
            fxtr_mkdir(directory_name)
        print_fixture_end("fxtr_mkdir_opt")

    return _fxtr_mkdir_opt


# -----------------------------------------------------------------------------
# Fixture - Delete a file.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_remove():
    """#### Fixture Factory: **Delete a file**."""

    def _fxtr_remove(file_name: str):
        """
        #### Fixture: **Delete a file**.

        **Args**:
        - **file_name (str)**: File name including path.
        """
        print_fixture_start("fxtr_remove")
        os.remove(file_name)
        print_fixture_end("fxtr_remove")

    return _fxtr_remove


# -----------------------------------------------------------------------------
# Fixture - Delete a file if existing.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_remove_opt(fxtr_remove):
    """#### Fixture Factory: **Delete a file if existing**."""

    def _fxtr_remove_opt(file_name: str):
        """
        #### Fixture: **Delete a file if existing**.

        **Args**:
        - **file_name (str)**: File name including path.
        """
        print_fixture_start("fxtr_remove_opt")
        if os.path.isfile(file_name):
            fxtr_remove(file_name)
        print_fixture_end("fxtr_remove_opt")

    return _fxtr_remove_opt


# -----------------------------------------------------------------------------
# Fixture - Delete a directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_rmdir():
    """#### Fixture Factory: **Delete a directory**."""

    def _fxtr_rmdir(directory_name: str):
        """
        #### Fixture: **Delete a directory**.

        **Args**:
        - **directory_name (str)**: Directory name including path.
        """
        print_fixture_start("fxtr_rmdir")
        shutil.rmtree(directory_name)
        print_fixture_end("fxtr_rmdir")

    return _fxtr_rmdir


# -----------------------------------------------------------------------------
# Fixture - Delete a directory if existing.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_rmdir_opt(fxtr_rmdir):
    """#### Fixture Factory: **Delete a directory if existing**."""

    def _fxtr_rmdir_opt(directory_name: str):
        """
        #### Fixture: **Delete a directory if existing**.

        **Args**:
        - **directory_name (str)**: Directory name including path.
        """
        print_fixture_start("fxtr_rmdir_opt")
        if os.path.isdir(directory_name):
            fxtr_rmdir(directory_name)
        print_fixture_end("fxtr_rmdir_opt")

    return _fxtr_rmdir_opt
