# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test libs.cfg.configurations and store fixtures.

Returns:
    [type]: None.
"""
import configparser
import os
import shutil
from typing import Tuple

import libs.cfg
import libs.db.cfg
import libs.db.driver
import libs.db.orm
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
CONFIG_PARSER: configparser.ConfigParser = configparser.ConfigParser()

FILE_NAME_SETUP_CFG: str = "setup.cfg"
FILE_NAME_SETUP_CFG_BACKUP: str = "setup.cfg_backup"

TESTS_INBOX = "tests/__PYTEST_FILES__/"


# -----------------------------------------------------------------------------
# Backup the 'setup.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def backup_setup_cfg() -> None:
    """Backup the 'setup.cfg' file."""
    if not os.path.isfile(FILE_NAME_SETUP_CFG_BACKUP):
        shutil.copy2(FILE_NAME_SETUP_CFG, FILE_NAME_SETUP_CFG_BACKUP)


# -----------------------------------------------------------------------------
# Copy the test file into the file directory 'inbox'.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_test_file_2_inbox(
    document_id: int, stem_name: str, file_extension: str
) -> Tuple[str, str]:
    """Copy the test file into the file directory 'inbox'.

    Args:
        document_id (int): Document id.
        stem_name (str): Stem name.
        file_extension (str): File extension.

    Returns:
        Tuple[str, str]: A tuple with source filename and the target filename.
    """
    file_name_source = stem_name + "." + file_extension
    file_name_target = stem_name + "_" + str(document_id) + "." + file_extension

    shutil.copy(os.path.join(TESTS_INBOX, file_name_source), libs.cfg.directory_inbox)

    return file_name_source, file_name_target


# -----------------------------------------------------------------------------
# Delete the original configuration parameter value.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def delete_config_param(config_section: str, config_param: str) -> str:
    """Delete the original configuration parameter value.

    Args:
        config_section (str): Configuration section.
        config_param (str): Configuration parameter.

    Returns:
        str: Original configuration parameter value.
    """
    CONFIG_PARSER.read(libs.cfg.DCR_CFG_FILE)

    config_value_orig = CONFIG_PARSER[config_section][config_param]

    del CONFIG_PARSER[config_section][config_param]

    with open(libs.cfg.DCR_CFG_FILE, "w", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)

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
# Fixture - Setup empty database and empty inboxes.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_empty_db_and_inbox(
    fxtr_mkdir,
    fxtr_rmdir_opt,
):
    """Fixture: Setup empty database and empty inboxes."""
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX])
    fxtr_mkdir(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX])
    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED])
    fxtr_mkdir(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED])
    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED])
    fxtr_mkdir(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED])

    yield

    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED])
    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED])
    fxtr_rmdir_opt(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX])

    libs.db.driver.drop_database()


# -----------------------------------------------------------------------------
# Fixture - Setup logger.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_logger():
    """Fixture: Setup logger & environment."""
    dcr.initialise_logger()

    yield


# -----------------------------------------------------------------------------
# Fixture - Setup logger & environment.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_logger_environment():
    """Fixture: Setup logger & environment."""
    libs.cfg.environment_type = libs.cfg.ENVIRONMENT_TYPE_TEST

    pytest.helpers.backup_setup_cfg()

    dcr.initialise_logger()

    yield

    # -------------------------------------------------------------------------
    pytest.helpers.restore_setup_cfg()


# -----------------------------------------------------------------------------
# Restore the original configuration parameter value.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def restore_config_param(
    config_section: str,
    config_param: str,
    config_value_orig: str,
) -> None:
    """Restore the original configuration parameter value.

    Args:
        config_section (str): Configuration section.
        config_param (str): Configuration parameter.
        config_value_orig (str): Original configuration parameter value.
    """
    CONFIG_PARSER[config_section][config_param] = config_value_orig

    with open(libs.cfg.DCR_CFG_FILE, "w", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)

    dcr.get_config()


# -----------------------------------------------------------------------------
# Restore the 'setup.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def restore_setup_cfg():
    """Restore the 'setup.cfg' file."""
    shutil.copy2(FILE_NAME_SETUP_CFG_BACKUP, FILE_NAME_SETUP_CFG)

    os.remove(FILE_NAME_SETUP_CFG_BACKUP)


# -----------------------------------------------------------------------------
# Show the state of the inboxes after the test.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def show_inboxes_after(inbox: str, inbox_accepted: str, inbox_rejected: str) -> None:
    """Show the state of the inboxes after the test.

    Args:
        inbox (str): File directory inbox.
        inbox_accepted (str): File directory inbox_accepted.
        inbox_rejected (str): File directory inbox_rejected.
    """
    # Show the content of the inbox directories.
    print("after: ls inbox=         ", os.listdir(inbox))
    print("after: ls inbox_accepted=", os.listdir(inbox_accepted))
    print("after: ls inbox_rejected=", os.listdir(inbox_rejected))


# -----------------------------------------------------------------------------
# Store and modify the original configuration parameter value.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def store_config_param(
    config_section: str,
    config_param: str,
    config_value_new: str,
) -> str:
    """Store and modify the original configuration parameter value.

    Args:
        config_section (str): Configuration section.
        config_param (str): Configuration parameter.
        config_value_new (str): New configuration parameter value.

    Returns:
        str: Original configuration parameter value.
    """
    CONFIG_PARSER.read(libs.cfg.DCR_CFG_FILE)

    config_value_orig = CONFIG_PARSER[config_section][config_param]

    CONFIG_PARSER[config_section][config_param] = config_value_new

    with open(libs.cfg.DCR_CFG_FILE, "w", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)

    return config_value_orig


# -----------------------------------------------------------------------------
# Verify the inboxes after a successful action.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def verify_action_after(
    directory_name: str,
    file_name: str,
    no_inbox: int,
    no_inbox_accepted: int,
    no_inbox_rejected: int,
) -> None:
    """Verify the inboxes after a successful action.

    Args:
        directory_name (str): Directory name of the new addition.
        file_name (str): File name of the new addition.
        no_inbox (int): Target number of files in the 'inbox' file directory.
        no_inbox_accepted (int): Target number of files in the 'inbox_accepted' file directory.
        no_inbox_rejected (int): Target number of files in the 'inbox_rejected' file directory.
    """
    print(
        "verify_action_after()  - " + libs.cfg.directory_inbox + "          =",
        os.listdir(libs.cfg.directory_inbox),
    )
    print(
        "verify_action_after()  - " + libs.cfg.directory_inbox_accepted + " =",
        os.listdir(libs.cfg.directory_inbox_accepted),
    )
    print(
        "verify_action_after()  - " + libs.cfg.directory_inbox_rejected + " =",
        os.listdir(libs.cfg.directory_inbox_rejected),
    )

    assert len(os.listdir(libs.cfg.directory_inbox)) == no_inbox, "after file directory: inbox"
    assert (
        len(os.listdir(libs.cfg.directory_inbox_accepted)) == no_inbox_accepted
    ), "after file directory: inbox_accepted"
    assert (
        len(os.listdir(libs.cfg.directory_inbox_rejected)) == no_inbox_rejected
    ), "after file directory: inbox_rejected"

    assert os.path.isfile(
        os.path.join(directory_name, file_name)
    ), "after: inbox_accepted should contain target file"


# -----------------------------------------------------------------------------
# Verify the inboxes before the action.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def verify_action_before(
    file_name: str, no_inbox: int, no_inbox_accepted: int, no_inbox_rejected: int
) -> None:
    """Verify the inboxes before the action.

    Args:
        file_name (str): File name of the test file in the file directory 'inbox'.
        no_inbox (int): Target number of files in the 'inbox' file directory.
        no_inbox_accepted (int): Target number of files in the 'inbox_accepted' file directory.
        no_inbox_rejected (int): Target number of files in the 'inbox_rejected' file directory.
    """
    print(
        "verify_action_before() - " + libs.cfg.directory_inbox + "          =",
        os.listdir(libs.cfg.directory_inbox),
    )

    assert len(os.listdir(libs.cfg.directory_inbox)) == no_inbox, "before file directory: inbox"
    assert (
        len(os.listdir(libs.cfg.directory_inbox_accepted)) == no_inbox_accepted
    ), "before file directory: inbox_accepted"
    assert (
        len(os.listdir(libs.cfg.directory_inbox_rejected)) == no_inbox_rejected
    ), "before file directory: inbox_rejected"

    assert os.path.isfile(
        os.path.join(libs.cfg.directory_inbox, file_name)
    ), "before: inbox should contain source file"
