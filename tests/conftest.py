# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test libs.cfg.configurations and store fixtures.

Returns:
    [type]: None.
"""
import configparser
import logging
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

LOGGER = logging.getLogger(__name__)

TESTS_INBOX = "tests/__PYTEST_FILES__/"


# -----------------------------------------------------------------------------
# Backup the 'setup.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def backup_setup_cfg() -> None:
    """Backup the 'setup.cfg' file."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if not os.path.isfile(FILE_NAME_SETUP_CFG_BACKUP):
        shutil.copy2(FILE_NAME_SETUP_CFG, FILE_NAME_SETUP_CFG_BACKUP)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Copy the test file into the file directory 'inbox'.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_test_file_2_inbox(
    document_id: int, stem_name: str, file_extension: str | None
) -> Tuple[str, str]:
    """Copy the test file into the file directory 'inbox'.

    Args:
        document_id (int): Document id.
        stem_name (str): Stem name.
        file_extension (str|None): File extension.

    Returns:
        Tuple[str, str]: A tuple with source filename and the target filename.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if file_extension is None:
        file_name_source = stem_name
        file_name_target = stem_name
    else:
        file_name_source = stem_name + "." + file_extension
        file_name_target = stem_name + "_" + str(document_id) + "." + file_extension

    shutil.copy(os.path.join(TESTS_INBOX, file_name_source), libs.cfg.directory_inbox)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    CONFIG_PARSER.read(libs.cfg.DCR_CFG_FILE)

    config_value_orig = CONFIG_PARSER[config_section][config_param]

    del CONFIG_PARSER[config_section][config_param]

    with open(libs.cfg.DCR_CFG_FILE, "w", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

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
        libs.cfg.logger.debug("%s: directory_name=%s", libs.cfg.LOGGER_START, str(directory_name))
        libs.cfg.logger.debug("current directory=%s", str(os.getcwd()))

        os.mkdir(directory_name)
        libs.cfg.logger.debug("after:  listdir=%s", str(os.listdir(directory_name)))

        libs.cfg.logger.debug(libs.cfg.LOGGER_END)

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
        libs.cfg.logger.debug("%s: directory_name=%s", libs.cfg.LOGGER_START, str(directory_name))
        libs.cfg.logger.debug("current directory=%s", str(os.getcwd()))

        libs.cfg.logger.debug("before: listdir=%s", str(os.listdir(directory_name)))
        shutil.rmtree(directory_name)

        libs.cfg.logger.debug(libs.cfg.LOGGER_END)

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
        libs.cfg.logger.debug("%s: directory_name=%s", libs.cfg.LOGGER_START, str(directory_name))
        libs.cfg.logger.debug("current directory=%s", str(os.getcwd()))

        if os.path.isdir(directory_name):
            libs.cfg.logger.debug("before: listdir=%s", str(os.listdir(directory_name)))
            fxtr_rmdir(directory_name)

        libs.cfg.logger.debug(libs.cfg.LOGGER_END)

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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    backup_setup_cfg()

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

    restore_setup_cfg()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Fixture - Setup logger.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_logger():
    """Fixture: Setup logger & environment."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dcr.initialise_logger()

    yield

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Fixture - Setup logger & environment.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_logger_environment():
    """Fixture: Setup logger & environment."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.environment_type = libs.cfg.ENVIRONMENT_TYPE_TEST

    backup_setup_cfg()

    dcr.initialise_logger()

    yield

    restore_setup_cfg()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    CONFIG_PARSER[config_section][config_param] = config_value_orig

    with open(libs.cfg.DCR_CFG_FILE, "w", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)

    dcr.get_config()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Restore the 'setup.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def restore_setup_cfg():
    """Restore the 'setup.cfg' file."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    shutil.copy2(FILE_NAME_SETUP_CFG_BACKUP, FILE_NAME_SETUP_CFG)

    os.remove(FILE_NAME_SETUP_CFG_BACKUP)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Run RUN_ACTION_PDF_2_IMAGE.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def run_action_pdf_2_image(
    run_action: str,
    stem_name: str,
    no_inboxes: Tuple[int, int, int],
) -> Tuple[int, int, int]:
    """Run RUN_ACTION_PROCESS_INBOX.

    Args:
        run_action:str: Run action.
        stem_name: str: Stem name.
        no_inboxes: Tuple[int,int,int]: Target number of files in the inbox file directories.

    Returns:
        Tuple[int, int, int]: New number of files in the inboxes.
    """
    file_name_target = stem_name + "_1." + libs.cfg.pdf2image_type

    no_inbox, no_inbox_accepted, no_inbox_rejected = no_inboxes

    show_state_directories("before")

    dcr.main([libs.cfg.DCR_ARGV_0, run_action])

    show_state_directories("after")

    no_inbox_accepted += 1
    verify_action_after(
        libs.cfg.directory_inbox_accepted,
        file_name_target,
        no_inbox,
        no_inbox_accepted,
        no_inbox_rejected,
    )

    return no_inbox, no_inbox_accepted, no_inbox_rejected


# -----------------------------------------------------------------------------
# Run RUN_ACTION_PROCESS_INBOX.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def run_action_process_inbox(
    run_action: str,
    document_id,
    file: Tuple[str, str, str | None],
    no_inboxes: Tuple[int, int, int],
) -> Tuple[int, int, int]:
    """Run RUN_ACTION_PROCESS_INBOX.

    Args:
        run_action:str: Run action.
        document_id (_type_): Document id
        file: Tuple[str, str, str|None]: Directory_name, stem name and file extension.
        no_inboxes: Tuple[int,int,int]: Target number of files in the inbox file directories.

    Returns:
        Tuple[int, int, int]: New number of files in the inboxes.
    """
    directory_name, stem_name, file_extension = file

    file_name_source, file_name_target = copy_test_file_2_inbox(
        document_id, stem_name, file_extension
    )

    no_inbox, no_inbox_accepted, no_inbox_rejected = no_inboxes

    no_inbox += 1
    # verify_action_before(
    #     file_name_source,
    #     no_inbox,
    #     no_inbox_accepted,
    #     no_inbox_rejected,
    # )

    show_state_directories("before")

    dcr.main([libs.cfg.DCR_ARGV_0, run_action])

    show_state_directories("after")

    if file_extension is None:
        directory_name = libs.cfg.directory_inbox
    else:
        no_inbox -= 1
        if directory_name == libs.cfg.directory_inbox_accepted:
            no_inbox_accepted += 1
        if directory_name == libs.cfg.directory_inbox_rejected:
            no_inbox_rejected += 1

    # verify_action_after(
    #     directory_name, file_name_target, no_inbox, no_inbox_accepted, no_inbox_rejected
    # )

    return no_inbox, no_inbox_accepted, no_inbox_rejected


# -----------------------------------------------------------------------------
# Setup RUN_ACTION_...
# -----------------------------------------------------------------------------
@pytest.helpers.register
def run_action_setup() -> Tuple[int, Tuple[int, int, int]]:
    """Setup RUN_ACTION_...

    Returns:
        Tuple[int, Tuple[int, int,int]]: (current_document_id, (current_no_inbox,
                                                                current_no_inbox_accepted,
                                                                current_no_inbox_rejected)).
    """
    libs.cfg.directory_inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    libs.cfg.directory_inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    libs.cfg.directory_inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    return 1, (0, 0, 0)


# -----------------------------------------------------------------------------
# Runs before all tests.
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup():
    """Runs before all tests."""
    dcr.initialise_logger()


# -----------------------------------------------------------------------------
# Show the state of the directories.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def show_state_directories(comment:str) -> None:
    """Show the state of the directories.

    Args:
        comment (str): Comment.
    """
    if os.path.isdir(libs.cfg.directory_inbox):
        libs.cfg.logger.debug(
            "show_state_directories(%s)  - %s         =%s",
            comment,
            str(libs.cfg.directory_inbox),
            os.listdir(libs.cfg.directory_inbox),
        )
    else:
        libs.cfg.logger.debug(
            comment,
            "show_state_directories(%s)  - %s          =%s",
            str(libs.cfg.directory_inbox),
            "missing",
        )

    if os.path.isdir(libs.cfg.directory_inbox):
        libs.cfg.logger.debug(
            "show_state_directories(%s)  - %s=%s",
            comment,
            str(libs.cfg.directory_inbox_accepted),
            os.listdir(libs.cfg.directory_inbox_accepted),
        )
    else:
        libs.cfg.logger.debug(
            comment,
            "show_state_directories(%s)  - %s=%s",
            str(libs.cfg.directory_inbox_accepted),
            "missing",
        )

    if os.path.isdir(libs.cfg.directory_inbox):
        libs.cfg.logger.debug(
            "show_state_directories(%s)  - %s=%s",
            comment,
            str(libs.cfg.directory_inbox_rejected),
            os.listdir(libs.cfg.directory_inbox_rejected),
        )
    else:
        libs.cfg.logger.debug(
            comment,
            "show_state_directories(%s)  - %s=%s",
            str(libs.cfg.directory_inbox_rejected),
            "missing",
        )


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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    CONFIG_PARSER.read(libs.cfg.DCR_CFG_FILE)

    config_value_orig = CONFIG_PARSER[config_section][config_param]

    CONFIG_PARSER[config_section][config_param] = config_value_new

    with open(libs.cfg.DCR_CFG_FILE, "w", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

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

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

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

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
