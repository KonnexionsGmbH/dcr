# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test config_setup.cfg.configurations and store fixtures.

Returns:
    [type]: None.
"""
import configparser
import os
import pathlib
import shutil
import typing

import cfg.glob
import cfg.setup
import db.driver
import pytest
import sqlalchemy

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
CONFIG_PARSER: configparser.ConfigParser = configparser.ConfigParser()

FILE_NAME_SETUP_CFG: str = "cfg.cfg"
FILE_NAME_SETUP_CFG_BACKUP: str = "cfg.cfg_backup"


# -----------------------------------------------------------------------------
# Backup and modify configuration parameter values.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def backup_config_params(
    config_section: str,
    config_params: typing.List[typing.Tuple[str, str]],
) -> typing.List[typing.Tuple[str, str]]:
    """Backup and modify configuration parameter values.

    Args:
        config_section (str): Configuration section.
        config_params (typing.List[typing.Tuple[str, str]]): Configuration parameter modifications.

    Returns:
        typing.List[typing.Tuple[str, str]]: Original configuration parameter.
    """
    config_params_backup: typing.List[typing.Tuple[str, str]] = []

    CONFIG_PARSER.read(cfg.glob.setup._DCR_CFG_FILE)

    for (config_param, config_value) in config_params:
        config_params_backup.append((config_param, CONFIG_PARSER[config_section][config_param]))
        CONFIG_PARSER[config_section][config_param] = config_value

    with open(cfg.glob.setup._DCR_CFG_FILE, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)

    return config_params_backup


# -----------------------------------------------------------------------------
# Backup the 'cfg.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def backup_setup_cfg() -> None:
    """Backup the 'cfg.cfg' file."""
    if not os.path.isfile(FILE_NAME_SETUP_CFG_BACKUP):
        shutil.copy2(FILE_NAME_SETUP_CFG, FILE_NAME_SETUP_CFG_BACKUP)


# -----------------------------------------------------------------------------
# Copy directories from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_directories_4_pytest_2_dir(
    source_directories: typing.List[str],
    target_dir: str,
) -> None:
    """Copy directories from the sample test file directory.

    Args:
        source_directories: typing.List[str]: Source directory names.
        target_dir: str: Target directory.
    """
    assert os.path.isdir(cfg.glob.TESTS_INBOX_NAME), "source base directory '" + cfg.glob.TESTS_INBOX_NAME + "' missing"

    for source in source_directories:
        source_dir = cfg.glob.TESTS_INBOX_NAME + "/" + source
        source_path = os.path.join(cfg.glob.TESTS_INBOX_NAME, pathlib.Path(source))
        assert os.path.isdir(source_path), "source language directory '" + str(source_path) + "' missing"
        target_path = os.path.join(target_dir, pathlib.Path(source))
        shutil.copytree(source_dir, target_path)


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_files_4_pytest(
    file_list: typing.List[
        typing.Tuple[typing.Tuple[str, str | None], typing.Tuple[pathlib.Path, typing.List[str], str | None]]
    ]
) -> None:
    """Copy files from the sample test file directory.

    Args:
        file_list (typing.List[
            typing.Tuple[
                typing.Tuple[str, str | None],
                typing.Tuple[pathlib.Path, typing.List[str], str | None]
            ]
        ]): typing.List of files to be copied.
    """
    assert os.path.isdir(cfg.glob.TESTS_INBOX_NAME), "source directory '" + cfg.glob.TESTS_INBOX_NAME + "' missing"

    for ((source_stem, source_ext), (target_dir, target_file_comp, target_ext)) in file_list:
        source_file_name = source_stem if source_ext is None else source_stem + "." + source_ext
        source_file = os.path.join(cfg.glob.TESTS_INBOX_NAME, source_file_name)
        assert os.path.isfile(source_file), "source file '" + str(source_file) + "' missing"

        assert os.path.isdir(target_dir), "target directory '" + target_dir + "' missing"
        target_file_name = (
            "_".join(target_file_comp) if target_ext is None else "_".join(target_file_comp) + "." + target_ext
        )
        target_file = os.path.join(target_dir, target_file_name)
        assert os.path.isfile(target_file) is False, "target file '" + str(target_file) + "' already existing"

        shutil.copy(source_file, target_file)
        assert os.path.isfile(target_file), "target file '" + str(target_file) + "' is missing"


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_files_4_pytest_2_dir(
    source_files: typing.List[typing.Tuple[str, str | None]],
    target_path: pathlib.Path,
) -> None:
    """Copy files from the sample test file directory.

    Args:
        source_files: typing.List[typing.Tuple[str, str | None]]: Source file names.
        target_path: Path: Target directory.
    """
    for source_file in source_files:
        (source_stem, source_ext) = source_file
        copy_files_4_pytest([(source_file, (target_path, [source_stem], source_ext))])


# -----------------------------------------------------------------------------
# Delete the original configuration parameter value.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def delete_config_param(config_section: str, config_param: str) -> typing.List[typing.Tuple[str, str]]:
    """Delete the original configuration parameter value.

    Args:
        config_section (str): Configuration section.
        config_param (str): Configuration parameter.

    Returns:
        typing.List[typing.Tuple[str,str]]: Original configuration parameter.
    """
    CONFIG_PARSER.read(cfg.glob.setup._DCR_CFG_FILE)

    config_value_orig = CONFIG_PARSER[config_section][config_param]

    del CONFIG_PARSER[config_section][config_param]

    with open(cfg.glob.setup._DCR_CFG_FILE, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)

    return [(config_param, config_value_orig)]


# -----------------------------------------------------------------------------
# Delete all entries in the database table 'version'.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def delete_version_version():
    """Delete all entries in the database table 'version'."""
    db.driver.connect_db()

    with cfg.glob.db_orm_engine.begin() as conn:
        version = sqlalchemy.Table(
            cfg.glob.DBT_VERSION,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )
        conn.execute(sqlalchemy.delete(version))

    db.driver.disconnect_db()


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
    backup_setup_cfg()

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_CREATE_DB])

    fxtr_rmdir_opt(cfg.glob.setup.directory_inbox)
    fxtr_mkdir(cfg.glob.setup.directory_inbox)
    fxtr_rmdir_opt(cfg.glob.setup.directory_inbox_accepted)
    fxtr_mkdir(cfg.glob.setup.directory_inbox_accepted)
    fxtr_rmdir_opt(cfg.glob.setup.directory_inbox_rejected)
    fxtr_mkdir(cfg.glob.setup.directory_inbox_rejected)

    yield

    fxtr_rmdir_opt(cfg.glob.setup.directory_inbox_rejected)
    fxtr_rmdir_opt(cfg.glob.setup.directory_inbox_accepted)
    fxtr_rmdir_opt(cfg.glob.setup.directory_inbox)

    db.driver.drop_database()

    restore_setup_cfg()


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
    cfg.glob.config = cfg.setup.Setup()

    cfg.glob.setup.environment_type = cfg.glob.setup._ENVIRONMENT_TYPE_TEST

    backup_setup_cfg()

    dcr.initialise_logger()

    yield

    restore_setup_cfg()


# -----------------------------------------------------------------------------
# Help RUN_ACTION_ALL_COMPLETE - duplicate file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def help_run_action_all_complete_duplicate_file(
    file_ext_1: str, file_ext_2: str, stem_name_1: str, stem_name_2: str
) -> None:
    """Help RUN_ACTION_ALL_COMPLETE - duplicate file."""
    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext_1)], cfg.glob.setup.directory_inbox_accepted)

    os.rename(
        os.path.join(cfg.glob.setup.directory_inbox_accepted, stem_name_1 + "." + file_ext_1),
        os.path.join(cfg.glob.setup.directory_inbox_accepted, stem_name_2 + "." + file_ext_2),
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_ALL_COMPLETE])

    # -------------------------------------------------------------------------
    verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [stem_name_1 + "_1." + file_ext_1, stem_name_2 + "." + file_ext_2],
    )

    verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )


# -----------------------------------------------------------------------------
# Help RUN_ACTION_PROCESS_INBOX - normal.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def help_run_action_process_inbox_normal(
    stem_name,
    file_ext,
):
    """Help RUN_ACTION_PROCESS_INBOX - normal."""
    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name, file_ext)], cfg.glob.setup.directory_inbox)

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])
    # -------------------------------------------------------------------------
    document_id: int = 1

    file_p_i = (
        cfg.glob.setup.directory_inbox_accepted,
        [stem_name, str(document_id)],
        file_ext,
    )

    verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [stem_name + "_" + str(document_id) + "." + file_ext],
    )

    verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    return document_id, file_p_i


# -----------------------------------------------------------------------------
# Insert a new configuration parameter.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def insert_config_param(
    config_section: str,
    config_param: str,
    config_value_new: str,
) -> None:
    """Insert a new configuration parameter.

    Args:
        config_section (str): Configuration section.
        config_param (str): Configuration parameter.
        config_value_new (str): New configuration parameter value.
    """
    CONFIG_PARSER.read(cfg.glob.setup._DCR_CFG_FILE)

    CONFIG_PARSER[config_section][config_param] = config_value_new

    with open(cfg.glob.setup._DCR_CFG_FILE, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)


# -----------------------------------------------------------------------------
# Restore the original configuration parameter.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def restore_config_params(
    config_section: str,
    config_params: typing.List[typing.Tuple[str, str]],
) -> None:
    """Restore the original configuration parameter.

    Args:
        config_section (str): Configuration section.
        config_params (typing.List[typing.Tuple[str, str]]): Configuration parameter modifications.
    """
    for (config_param, config_value) in config_params:
        CONFIG_PARSER[config_section][config_param] = config_value

    with open(cfg.glob.setup._DCR_CFG_FILE, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)

    cfg.glob.config = cfg.setup.Setup()


# -----------------------------------------------------------------------------
# Restore the 'cfg.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def restore_setup_cfg():
    """Restore the 'cfg.cfg' file."""
    shutil.copy2(FILE_NAME_SETUP_CFG_BACKUP, FILE_NAME_SETUP_CFG)

    os.remove(FILE_NAME_SETUP_CFG_BACKUP)


# -----------------------------------------------------------------------------
# Run before all tests.
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_dcr():
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
    CONFIG_PARSER.read(cfg.glob.setup._DCR_CFG_FILE)

    config_value_orig = CONFIG_PARSER[config_section][config_param]

    CONFIG_PARSER[config_section][config_param] = config_value_new

    with open(cfg.glob.setup._DCR_CFG_FILE, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)

    return config_value_orig


# -----------------------------------------------------------------------------
# Verify the content of a file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def verify_content_of_directory(
    directory_name: str,
    expected_directories: typing.List[str],
    expected_files: typing.List[str],
) -> None:
    """Verify the content of a file directory.

    Args:
        directory_name: str:
                   Name of the file directory to be checked.
        expected_directories: typing.List[str]:
                   typing.List of the expected directory names.
        expected_files: typing.List[str]:
                   typing.List of the expected file names.
    """
    cfg.glob.logger.info("directory name   =%s", directory_name)

    directory_content = os.listdir(directory_name)
    cfg.glob.logger.info("existing directory content=%s", str(directory_content))
    cfg.glob.logger.info("expected directory content=%s", str(expected_directories))
    cfg.glob.logger.info("expected file      content=%s", str(expected_files))

    # check directory content against expectations
    for elem in directory_content:
        elem_path = os.path.join(directory_name, elem)
        if os.path.isdir(elem_path):
            assert elem in expected_directories, f"directory {elem} was not expected"
        else:
            assert elem in expected_files, f"file {elem} was not expected"

    # check expected directories against directory content
    for elem in expected_directories:
        assert elem in directory_content, f"expected directory {elem} is missing"
        elem_path = os.path.join(directory_name, elem)
        assert os.path.isdir(elem_path), f"expected directory {elem} is a file"

    # check expected files against directory content
    for elem in expected_files:
        assert elem in directory_content, f"expected file {elem} is missing"
        elem_path = os.path.join(directory_name, elem)
        assert os.path.isfile(elem_path), f"expected file {elem} is a directory"
