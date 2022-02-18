# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test libs.cfg.configurations and store fixtures.

Returns:
    [type]: None.
"""

import os
import shutil

import libs.cfg
import libs.db.orm
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
dcr.initialise_logger()


# -----------------------------------------------------------------------------
# Fixture - Drop the database.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_drop_database():
    """Fixture Factory: Drop the database."""

    def drop_database():
        """Fixture: Drop the database."""
        dcr.get_config()

        drop_database()

    return drop_database


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
            directory_name (str): The directory name including path.
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
            directory_name (str): The directory name including path.
        """
        if not os.path.isdir(directory_name):
            fxtr_mkdir(directory_name)

    return _fxtr_mkdir_opt


# -----------------------------------------------------------------------------
# Fixture - New empty database and empty inbox.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_new_db_empty_inbox(fxtr_mkdir, fxtr_drop_database, fxtr_rmdir, fxtr_rmdir_opt):
    """Fixture: New empty database and empty inbox directories."""
    dcr.get_config()

    fxtr_drop_database()

    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX])
    fxtr_mkdir(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX])
    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED])
    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED])

    if libs.cfg.metadata is not None:
        libs.cfg.metadata.clear()

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    yield

    fxtr_rmdir(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX])

    fxtr_drop_database()


# -----------------------------------------------------------------------------
# Fixture - New empty database, but no inbox directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_new_db_no_inbox(fxtr_drop_database, fxtr_rmdir_opt):
    """Fixture: New empty database, but no inbox directory."""
    dcr.get_config()

    fxtr_drop_database()

    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX])

    if libs.cfg.metadata is not None:
        libs.cfg.metadata.clear()

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    yield

    fxtr_drop_database()


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
            directory_name (str): The directory name including path.
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
            directory_name (str): The directory name including path.
        """
        if os.path.isdir(directory_name):
            fxtr_rmdir(directory_name)

    return _fxtr_rmdir_opt
