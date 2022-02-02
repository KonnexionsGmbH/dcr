"""Test Configuration and Fixtures.

Setup test configurations and store fixtures.

Returns:
    [type]: None.
"""

import os
import shutil

import pytest
from app import get_config
from app import initialise_logger
from app import main
from libs.db import METADATA
from libs.cfg import ACTION_DB_CREATE_OR_UPGRADE
from libs.cfg import config
from libs.cfg import DCR_CFG_DATABASE_FILE
from libs.cfg import DCR_CFG_DIRECTORY_INBOX

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
DCR_ARGV_0 = "src/dcr/app.py"

LOGGER = initialise_logger()

# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Fixture - Create a new directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_mkdir():
    """Fixture Factory: Create a new directory."""

    def _fxtr_mkdir(directory_name: str):
        """
        Fixture: Create a new directory.

        Args:
            directory_name (str): Directory name including path.
        """
        os.mkdir(directory_name)

    return _fxtr_mkdir


# -----------------------------------------------------------------------------
# Fixture - Create a new directory if not existing.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_mkdir_opt(fxtr_mkdir):
    """Fixture Factory: Create a new directory if not existing."""

    def _fxtr_mkdir_opt(directory_name: str):
        """
        Fixture: Create a new directory if not existing.

        Args:
            directory_name (str): Directory name including path.
        """
        if not os.path.isdir(directory_name):
            fxtr_mkdir(directory_name)

    return _fxtr_mkdir_opt


# -----------------------------------------------------------------------------
# Fixture - New empty database and empty inbox.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_new_db_empty_inbox(
    fxtr_mkdir, fxtr_remove, fxtr_remove_opt, fxtr_rmdir, fxtr_rmdir_opt
):
    """Fixture: New empty database, but no inbox directory."""
    get_config(LOGGER)

    fxtr_remove_opt(config[DCR_CFG_DATABASE_FILE])

    fxtr_rmdir_opt(config[DCR_CFG_DIRECTORY_INBOX])

    fxtr_mkdir(config[DCR_CFG_DIRECTORY_INBOX])

    METADATA.clear()

    main([DCR_ARGV_0, ACTION_DB_CREATE_OR_UPGRADE])

    yield

    fxtr_rmdir(config[DCR_CFG_DIRECTORY_INBOX])

    fxtr_remove(config[DCR_CFG_DATABASE_FILE])


# -----------------------------------------------------------------------------
# Fixture - New empty database, but no inbox directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_new_db_no_inbox(fxtr_remove, fxtr_remove_opt, fxtr_rmdir_opt):
    """Fixture: New empty database, but no inbox directory."""
    get_config(LOGGER)

    fxtr_remove_opt(config[DCR_CFG_DATABASE_FILE])

    fxtr_rmdir_opt(config[DCR_CFG_DIRECTORY_INBOX])

    METADATA.clear()

    main([DCR_ARGV_0, ACTION_DB_CREATE_OR_UPGRADE])

    yield

    fxtr_remove(config[DCR_CFG_DATABASE_FILE])


# -----------------------------------------------------------------------------
# Fixture - No database available.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_no_db(fxtr_remove_opt):
    """Fixture: No database available."""
    get_config(LOGGER)

    fxtr_remove_opt(config[DCR_CFG_DATABASE_FILE])

    yield

    fxtr_remove_opt(config[DCR_CFG_DATABASE_FILE])


# -----------------------------------------------------------------------------
# Fixture - Delete a file.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_remove():
    """Fixture Factory: Delete a file."""

    def _fxtr_remove(file_name: str):
        """
        Fixture: Delete a file.

        Args:
            file_name (str): File name including path.
        """
        os.remove(file_name)

    return _fxtr_remove


# -----------------------------------------------------------------------------
# Fixture - Delete a file if existing.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_remove_opt(fxtr_remove):
    """Fixture Factory: Delete a file if existing."""

    def _fxtr_remove_opt(file_name: str):
        """
        Fixture: Delete a file if existing.

        Args:
            file_name (str): File name including path.
        """
        if os.path.isfile(file_name):
            fxtr_remove(file_name)

    return _fxtr_remove_opt


# -----------------------------------------------------------------------------
# Fixture - Delete a directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_rmdir():
    """Fixture Factory: Delete a directory."""

    def _fxtr_rmdir(directory_name: str):
        """
        Fixture: Delete a directory.

        Args:
            directory_name (str): Directory name including path.
        """
        shutil.rmtree(directory_name)

    return _fxtr_rmdir


# -----------------------------------------------------------------------------
# Fixture - Delete a directory if existing.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_rmdir_opt(fxtr_rmdir):
    """Fixture Factory: Delete a directory if existing."""

    def _fxtr_rmdir_opt(directory_name: str):
        """
        Fixture: Delete a directory if existing.

        Args:
            directory_name (str): Directory name including path.
        """
        if os.path.isdir(directory_name):
            fxtr_rmdir(directory_name)

    return _fxtr_rmdir_opt
