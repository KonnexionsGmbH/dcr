# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test libs.cfg.configurations and store fixtures.

Returns:
    [type]: None.
"""
import configparser
import os
import shutil
from pathlib import Path
from typing import List
from typing import Tuple

import libs.cfg
import libs.db.cfg
import libs.db.driver
import libs.db.orm
import libs.utils
import pytest
from sqlalchemy import Table
from sqlalchemy import delete

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
CONFIG_PARSER: configparser.ConfigParser = configparser.ConfigParser()

FILE_NAME_SETUP_CFG: str = "setup.cfg"
FILE_NAME_SETUP_CFG_BACKUP: str = "setup.cfg_backup"

TESTS_INBOX = libs.utils.str_2_path("tests/__PYTEST_FILES__/")


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
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_files_from_pytest(
    file_list: List[Tuple[Tuple[str, str | None], Tuple[Path, List[str], str | None]]]
) -> None:
    """Copy files from the sample test file directory.

    Args:
        file_list (List[Tuple[Tuple[str, str | None], Tuple[Path, List[str], str | None]]]):
                  List of files to be copied.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    assert os.path.isdir(TESTS_INBOX), "source directory missing"

    for ((source_stem, source_ext), (target_dir, target_file_comp, target_ext)) in file_list:
        source_file_name = source_stem if source_ext is None else source_stem + "." + source_ext
        source_file = os.path.join(TESTS_INBOX, source_file_name)
        libs.cfg.logger.debug("source file=%s", source_file)
        assert os.path.isfile(source_file), "source file missing"

        assert os.path.isdir(target_dir), "target directory missing"
        target_file_name = (
            "_".join(target_file_comp)
            if target_ext is None
            else "_".join(target_file_comp) + "." + target_ext
        )
        target_file = os.path.join(target_dir, target_file_name)
        libs.cfg.logger.debug("target file=%s", target_file)
        assert os.path.isfile(target_file) is False, "target file already existing"

        shutil.copy(source_file, target_file)
        assert os.path.isfile(target_file), "target file missing"

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_files_from_pytest_2_dir(
    source_files: List[Tuple[str, str | None]],
    target_dir: Path,
) -> None:
    """Copy files from the sample test file directory.

    Args:
        source_files: List[Tuple[str, str | None]]: Source file name.
        target_dir: Path: Target directory.
    """
    for source_file in source_files:
        (source_stem, source_ext) = source_file
        copy_files_from_pytest([(source_file, (target_dir, [source_stem], source_ext))])


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
# Delete all entries in the database table 'version'.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def delete_version_version():
    """Delete all entries in the database table 'version'."""
    libs.db.orm.connect_db()

    with libs.db.cfg.db_orm_engine.begin() as conn:
        version = Table(
            libs.db.cfg.DBT_VERSION,
            libs.db.cfg.db_orm_metadata,
            autoload_with=libs.db.cfg.db_orm_engine,
        )
        conn.execute(delete(version))

    libs.db.orm.disconnect_db()


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

    fxtr_rmdir_opt(libs.cfg.directory_inbox)
    fxtr_mkdir(libs.cfg.directory_inbox)
    fxtr_rmdir_opt(libs.cfg.directory_inbox_accepted)
    fxtr_mkdir(libs.cfg.directory_inbox_accepted)
    fxtr_rmdir_opt(libs.cfg.directory_inbox_rejected)
    fxtr_mkdir(libs.cfg.directory_inbox_rejected)

    yield

    fxtr_rmdir_opt(libs.cfg.directory_inbox_rejected)
    fxtr_rmdir_opt(libs.cfg.directory_inbox_accepted)
    fxtr_rmdir_opt(libs.cfg.directory_inbox)

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
# Help RUN_ACTION_ALL_COMPLETE - duplicate file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def help_run_action_all_complete_duplicate_file(
    file_ext_1: str, file_ext_2: str, stem_name_1: str, stem_name_2: str
) -> None:
    """Help RUN_ACTION_ALL_COMPLETE - duplicate file."""
    pytest.helpers.copy_files_from_pytest_2_dir(
        [(stem_name_1, file_ext_1)], libs.cfg.directory_inbox_accepted
    )

    os.rename(
        os.path.join(libs.cfg.directory_inbox_accepted, stem_name_1 + "." + file_ext_1),
        os.path.join(libs.cfg.directory_inbox_accepted, stem_name_2 + "." + file_ext_2),
    )

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_ALL_COMPLETE])
    # -------------------------------------------------------------------------
    no_files_expected = (0, 2, 0)

    file_1 = (
        libs.cfg.directory_inbox_accepted,
        [stem_name_1 + "_1"],
        file_ext_1,
    )
    file_2 = (
        libs.cfg.directory_inbox_accepted,
        [stem_name_2],
        file_ext_2,
    )

    pytest.helpers.verify_content_inboxes(
        [
            file_1,
            file_2,
        ],
        no_files_expected,
    )


# -----------------------------------------------------------------------------
# Help RUN_ACTION_PROCESS_INBOX - normal.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def help_run_action_process_inbox_normal(file_ext, stem_name):
    """Help RUN_ACTION_PROCESS_INBOX - normal."""
    pytest.helpers.copy_files_from_pytest_2_dir([(stem_name, file_ext)], libs.cfg.directory_inbox)

    # -------------------------------------------------------------------------
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])
    # -------------------------------------------------------------------------
    document_id: int = 1

    no_files_expected = (0, 1, 0)

    file_p_i = (
        libs.cfg.directory_inbox_accepted,
        [stem_name, str(document_id)],
        file_ext,
    )

    files_to_be_checked = [
        file_p_i,
    ]

    pytest.helpers.verify_content_inboxes(
        files_to_be_checked,
        no_files_expected,
    )

    return document_id, file_p_i


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
# Run before all tests.
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup():
    """Run before all tests."""
    dcr.initialise_logger()


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
# Verify the contents of the inbox file directories.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def verify_content_inboxes(
    file_list: List[Tuple[Path, List[str], str | None]],
    no_of_files: Tuple[int | None, int | None, int | None],
) -> None:
    """Verify the contents of the inbox file directories.

    Args:
        file_list: List[Tuple[Path, List[str], str | None]]:
                   List of files to be checked.
        no_of_files: Tuple[int | None, int | None, int | None]:
                     Expected number of files in the file directories
                     inbox, inbox_accepted and inbox_rejected
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.logger.info("files to be checked=%s", str(file_list))

    for (directory, file_comp, ext) in file_list:
        assert os.path.isdir(directory), "directory to be checked missing"
        file_name = "_".join(file_comp) if ext is None else "_".join(file_comp) + "." + ext
        file = os.path.join(directory, file_name)
        libs.cfg.logger.debug("file to be checked=%s", file)
        assert os.path.isfile(file), "file to be checked is missing"

    libs.cfg.logger.info("no. files expected =%s", str(no_of_files))

    (no_inbox, no_accepted, no_rejected) = no_of_files

    if no_inbox is None:
        assert os.path.isdir(libs.cfg.directory_inbox) is False, "directory inbox is existing"
    else:
        libs.cfg.logger.debug(
            "content directory %s=%s",
            libs.cfg.directory_inbox,
            str(os.listdir(libs.cfg.directory_inbox)),
        )
        assert (
            len(os.listdir(libs.cfg.directory_inbox)) == no_inbox
        ), "no files in directory inbox is unexpected"

    if no_accepted is None:
        assert (
            os.path.isdir(libs.cfg.directory_inbox_accepted) is False
        ), "directory inbox_accepted is existing"
    else:
        libs.cfg.logger.debug(
            "content directory %s=%s",
            libs.cfg.directory_inbox_accepted,
            str(os.listdir(libs.cfg.directory_inbox_accepted)),
        )
        assert (
            len(os.listdir(libs.cfg.directory_inbox_accepted)) == no_accepted
        ), "no files in directory inbox_accepted is unexpected"

    if no_rejected is None:
        assert (
            os.path.isdir(libs.cfg.directory_inbox_rejected) is False
        ), "directory inbox_rejected is existing"
    else:
        libs.cfg.logger.debug(
            "content directory %s=%s",
            libs.cfg.directory_inbox_rejected,
            str(os.listdir(libs.cfg.directory_inbox_rejected)),
        )
        assert (
            len(os.listdir(libs.cfg.directory_inbox_rejected)) == no_rejected
        ), "no files in directory inbox_rejected is unexpected"

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
