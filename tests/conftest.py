# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test libs.cfg.configurations and store fixtures.

Returns:
    [type]: None.
"""
import configparser
import locale
import os
import shutil
from typing import Callable
from typing import Tuple

import libs.cfg
import libs.db.cfg
import libs.db.orm
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
dcr.initialise_logger()


# -----------------------------------------------------------------------------
# Backup the 'setup.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def backup_setup_cfg(
    fxtr_setup_logger_environment: Callable,
) -> Tuple[configparser.ConfigParser, str, str]:
    """Backup the 'setup.cfg' file.

    Args:
        fxtr_setup_logger_environment (_type_): _description_

    Returns:
        Tuple(configparser.ConfigParser,str,str): Configparser and file names.
    """
    fxtr_setup_logger_environment()

    # -------------------------------------------------------------------------
    setup_cfg: str = "setup.cfg"
    setup_cfg_backup: str = "setup.cfg_backup"

    if not os.path.isfile(setup_cfg_backup):
        shutil.copy2(setup_cfg, setup_cfg_backup)

    # -------------------------------------------------------------------------
    config_parser = configparser.ConfigParser()

    return config_parser, setup_cfg, setup_cfg_backup


# -----------------------------------------------------------------------------
# Delete the original configuration parameter value.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def delete_config_param(
    config_parser: configparser.ConfigParser, config_section: str, config_param: str
) -> str:
    """Delete the original configuration parameter value.

    Args:
        config_parser (configparser): Configuration parser.
        config_section (str): Configuration section.
        config_param (str): Configuration parameter.

    Returns:
        str: Original configuration parameter value.
    """
    config_parser.read(libs.cfg.DCR_CFG_FILE)

    config_value_orig = config_parser[config_section][config_param]

    del config_parser[config_section][config_param]

    with open(libs.cfg.DCR_CFG_FILE, "w", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as configfile:
        config_parser.write(configfile)

    return config_value_orig


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
def fxtr_new_db_empty_inbox(
    fxtr_mkdir,
    fxtr_rmdir_opt,
    fxtr_setup_logger_environment,
):
    """Fixture: New empty database and empty inbox directories."""
    fxtr_setup_logger_environment()

    dcr.get_config()

    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX])
    fxtr_mkdir(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX])
    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED])
    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED])

    if libs.db.cfg.metadata is not None:
        libs.db.cfg.metadata.clear()

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    yield

    libs.db.orm.disconnect_db()

    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX])
    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED])
    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED])


# -----------------------------------------------------------------------------
# Fixture - No database Docker container.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_no_db_docker_container(fxtr_setup_logger_environment):
    """Fixture Factory: No database Docker container."""

    def drop_database():
        """Fixture: Drop the database."""
        fxtr_setup_logger_environment()

        dcr.get_config()

        del libs.cfg.config[libs.cfg.DCR_CFG_DB_DOCKER_CONTAINER]

    return drop_database


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


# -----------------------------------------------------------------------------
# Fixture - Setup logger.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_logger():
    """Fixture Factory: Setup logger."""

    def _fxtr_setup_logger():
        """Fixture: Setup logger."""
        # Initialise the logging functionality.
        dcr.initialise_logger()

        libs.cfg.logger.debug(libs.cfg.LOGGER_START)
        libs.cfg.logger.info("Start dcr.py")

        print("Start dcr.py")

        locale.setlocale(locale.LC_ALL, libs.cfg.LOCALE)

    return _fxtr_setup_logger


# -----------------------------------------------------------------------------
# Fixture - Setup logger & environment.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_logger_environment(fxtr_setup_logger):
    """Fixture Factory: Setup logger & environment."""

    def _fxtr_setup_logger_environment():
        """Fixture: Setup logger & environment."""
        fxtr_setup_logger()

        # Load the environment variables.
        dcr.get_environment()

    return _fxtr_setup_logger_environment


# -----------------------------------------------------------------------------
# Restore the original configuration parameter value.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def restore_config_param(
    config_parser: configparser.ConfigParser,
    config_section: str,
    config_param: str,
    config_value_orig: str,
) -> None:
    """Restore the original configuration parameter value.

    Args:
        config_parser (configparser): Configuration parser.
        config_section (str): Configuration section.
        config_param (str): Configuration parameter.
        config_value_orig (str): Original configuration parameter value.
    """
    config_parser[config_section][config_param] = config_value_orig

    with open(libs.cfg.DCR_CFG_FILE, "w", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as configfile:
        config_parser.write(configfile)

    dcr.get_config()


# -----------------------------------------------------------------------------
# Restore the 'setup.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def restore_setup_cfg(setup_cfg, setup_cfg_backup):
    """Restore the 'setup.cfg' file.

    Args:
        setup_cfg (_type_): Target file name.
        setup_cfg_backup (_type_): Source file name.
    """
    shutil.copy2(setup_cfg_backup, setup_cfg)

    os.remove(setup_cfg_backup)


# -----------------------------------------------------------------------------
# Store and modify the original configuration parameter value.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def store_config_param(
    config_parser: configparser.ConfigParser,
    config_section: str,
    config_param: str,
    config_value_new: str,
) -> str:
    """Store and modify the original configuration parameter value.

    Args:
        config_parser (configparser): Configuration parser.
        config_section (str): Configuration section.
        config_param (str): Configuration parameter.
        config_value_new (str): New configuration parameter value.

    Returns:
        str: Original configuration parameter value.
    """
    config_parser.read(libs.cfg.DCR_CFG_FILE)

    config_value_orig = config_parser[config_section][config_param]

    config_parser[config_section][config_param] = config_value_new

    with open(libs.cfg.DCR_CFG_FILE, "w", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as configfile:
        config_parser.write(configfile)

    return config_value_orig
