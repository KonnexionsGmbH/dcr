"""Testing Module `app`."""
import logging

import pytest

from app import get_args, \
    main
from app import get_config
from app import initialise_logger
from libs.globals import ACTION_DB_CREATE_OR_UPGRADE
from libs.globals import ACTION_NEW_COMPLETE
from libs.globals import ACTION_PROCESS_INBOX
from libs.globals import ACTION_PROCESS_INBOX_OCR
from libs.globals import CONFIG
from libs.globals import DCR_CFG_DATABASE_URL
from libs.globals import DCR_CFG_DCR_VERSION
from libs.globals import DCR_CFG_DIRECTORY_INBOX
from libs.globals import DCR_CFG_DIRECTORY_INBOX_ACCEPTED
from libs.globals import DCR_CFG_DIRECTORY_INBOX_OCR
from libs.globals import DCR_CFG_DIRECTORY_INBOX_OCR_ACCEPTED
from libs.globals import DCR_CFG_DIRECTORY_INBOX_OCR_REJECTED
from libs.globals import DCR_CFG_DIRECTORY_INBOX_REJECTED

# -----------------------------------------------------------------------------
# Constants, Fixtures & Globals.
# -----------------------------------------------------------------------------
LOGGER = initialise_logger()


# -----------------------------------------------------------------------------
# Test Function - get_args().
# -----------------------------------------------------------------------------
def test_get_args_no() -> None:
    """Test: No command line arguments found."""
    with pytest.raises(SystemExit) as expt:
        get_args(LOGGER, [])
    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_get_args_one() -> None:
    """Test: The specific command line arguments are missing."""
    with pytest.raises(SystemExit) as expt:
        get_args(LOGGER, [""])
    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_get_args_unknown() -> None:
    """Test: Unknown command line argument=xxx."""
    with pytest.raises(SystemExit) as expt:
        get_args(LOGGER, ["n/a", "second"])
    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_get_args_valid_1() -> None:
    """Test: One valid argument."""
    assert get_args(LOGGER, ["n/a", ACTION_DB_CREATE_OR_UPGRADE]) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: False,
    }


def test_get_args_valid_1_duplicate() -> None:
    """Test: One valid argument."""
    assert get_args(
        LOGGER,
        ["n/a", ACTION_DB_CREATE_OR_UPGRADE, ACTION_DB_CREATE_OR_UPGRADE],
    ) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: False,
    }


def test_get_args_valid_2() -> None:
    """Test: One valid argument."""
    assert get_args(
        LOGGER, ["n/a", ACTION_DB_CREATE_OR_UPGRADE, ACTION_PROCESS_INBOX_OCR]
    ) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: True,
    }


def test_get_args_valid_complete() -> None:
    """Test: One valid argument."""
    assert get_args(LOGGER, ["n/a", ACTION_NEW_COMPLETE]) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: True,
        ACTION_PROCESS_INBOX_OCR: True,
    }


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config() -> None:
    """Test: Functionality."""
    get_config(LOGGER)

    assert len(CONFIG) == 8

    assert (DCR_CFG_DATABASE_URL in CONFIG) == True
    assert (DCR_CFG_DCR_VERSION in CONFIG) == True
    assert (DCR_CFG_DIRECTORY_INBOX in CONFIG) == True
    assert (DCR_CFG_DIRECTORY_INBOX_ACCEPTED in CONFIG) == True
    assert (DCR_CFG_DIRECTORY_INBOX_OCR in CONFIG) == True
    assert (DCR_CFG_DIRECTORY_INBOX_OCR_ACCEPTED in CONFIG) == True
    assert (DCR_CFG_DIRECTORY_INBOX_OCR_REJECTED in CONFIG) == True
    assert (DCR_CFG_DIRECTORY_INBOX_REJECTED in CONFIG) == True


# -----------------------------------------------------------------------------
# Test Function - initialise_logger().
# -----------------------------------------------------------------------------
def test_initialise_logger() -> None:
    """Test: Functionality."""
    assert type(initialise_logger()) is logging.Logger


# -----------------------------------------------------------------------------
# Test Function - main().
# -----------------------------------------------------------------------------
def test_main() -> None:
    """Test: Functionality."""
    main(["pytest", "new"])
