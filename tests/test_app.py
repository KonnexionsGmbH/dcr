"""Testing Module app."""

import os

import pytest
from app import get_args
from app import get_config
from app import initialise_logger
from app import main
from conftest import DCR_ARGV_0
from libs.globals import ACTION_ALL_COMPLETE
from libs.globals import ACTION_DB_CREATE_OR_UPGRADE
from libs.globals import ACTION_PROCESS_INBOX
from libs.globals import ACTION_PROCESS_INBOX_OCR
from libs.globals import CONFIG
from libs.globals import DCR_CFG_DATABASE_FILE
from libs.globals import DCR_CFG_DATABASE_URL
from libs.globals import DCR_CFG_DCR_VERSION
from libs.globals import DCR_CFG_DIRECTORY_INBOX
from libs.globals import DCR_CFG_DIRECTORY_INBOX_ACCEPTED
from libs.globals import DCR_CFG_DIRECTORY_INBOX_OCR
from libs.globals import DCR_CFG_DIRECTORY_INBOX_OCR_ACCEPTED
from libs.globals import DCR_CFG_DIRECTORY_INBOX_OCR_REJECTED
from libs.globals import DCR_CFG_DIRECTORY_INBOX_REJECTED

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
LOGGER = initialise_logger()


# -----------------------------------------------------------------------------
# Test Function - get_args().
# -----------------------------------------------------------------------------
def test_get_args_no():
    """Test: No command line arguments found."""
    with pytest.raises(SystemExit) as expt:
        get_args(LOGGER, [])

    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_get_args_one():
    """Test: The specific command line arguments are missing."""
    with pytest.raises(SystemExit) as expt:
        get_args(LOGGER, [""])

    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_get_args_unknown():
    """Test: Unknown command line argument=xxx."""
    with pytest.raises(SystemExit) as expt:
        get_args(LOGGER, ["n/a", "second"])

    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_get_args_valid_1():
    """Test: One valid argument."""
    assert get_args(LOGGER, ["n/a", ACTION_DB_CREATE_OR_UPGRADE]) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: False,
    }


def test_get_args_valid_1_duplicate():
    """Test: Duplicate argument."""
    assert get_args(
        LOGGER,
        ["n/a", ACTION_DB_CREATE_OR_UPGRADE, ACTION_DB_CREATE_OR_UPGRADE],
    ) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: False,
    }


def test_get_args_valid_2():
    """Test: Two valid arguments."""
    assert get_args(
        LOGGER,
        ["n/a", ACTION_DB_CREATE_OR_UPGRADE, ACTION_PROCESS_INBOX_OCR],
    ) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: True,
    }


def test_get_args_valid_new():
    """Test: Special argument `all`."""
    assert get_args(LOGGER, ["n/a", ACTION_ALL_COMPLETE]) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: True,
        ACTION_PROCESS_INBOX_OCR: True,
    }


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config():
    """Test: Completeness."""

    get_config(LOGGER)

    assert len(CONFIG) == 9

    assert (DCR_CFG_DATABASE_FILE in CONFIG) is True
    assert (DCR_CFG_DATABASE_URL in CONFIG) is True
    assert (DCR_CFG_DCR_VERSION in CONFIG) is True
    assert (DCR_CFG_DIRECTORY_INBOX in CONFIG) is True
    assert (DCR_CFG_DIRECTORY_INBOX_ACCEPTED in CONFIG) is True
    assert (DCR_CFG_DIRECTORY_INBOX_OCR in CONFIG) is True
    assert (DCR_CFG_DIRECTORY_INBOX_OCR_ACCEPTED in CONFIG) is True
    assert (DCR_CFG_DIRECTORY_INBOX_OCR_REJECTED in CONFIG) is True
    assert (DCR_CFG_DIRECTORY_INBOX_REJECTED in CONFIG) is True


# -----------------------------------------------------------------------------
# Test Function - main().
# -----------------------------------------------------------------------------
def test_main_p_i_missing_db(fxtr_remove_opt):
    """Test: ACTION_PROCESS_INBOX - DB missing."""
    get_config(LOGGER)

    fxtr_remove_opt(CONFIG[DCR_CFG_DATABASE_FILE])

    with pytest.raises(SystemExit) as expt:
        main([DCR_ARGV_0, ACTION_PROCESS_INBOX])

    assert expt.type == SystemExit
    assert expt.value.code == 1


@pytest.mark.issue
def test_main_d_c_u(fxtr_create_new_db, fxtr_remove_opt):
    """Test: ACTION_DB_CREATE_OR_UPGRADE."""
    fxtr_create_new_db

    main([DCR_ARGV_0, ACTION_DB_CREATE_OR_UPGRADE])

    assert os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]) is True

    fxtr_remove_opt(CONFIG[DCR_CFG_DATABASE_FILE])


@pytest.mark.issue
def test_main_p_i(fxtr_create_new_db, fxtr_mkdir_opt, fxtr_remove_opt):
    """Test: ACTION_PROCESS_INBOX."""
    fxtr_create_new_db

    fxtr_mkdir_opt(CONFIG[DCR_CFG_DIRECTORY_INBOX])

    main([DCR_ARGV_0, ACTION_PROCESS_INBOX])

    fxtr_remove_opt(CONFIG[DCR_CFG_DATABASE_FILE])
