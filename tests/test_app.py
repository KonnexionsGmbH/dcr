"""Testing Module `app`."""
import os
import shutil

import pytest

from app import get_args
from app import get_config
from app import initialise_logger
from app import main
from libs.globals import ACTION_DB_CREATE_OR_UPGRADE
from libs.globals import ACTION_NEW_COMPLETE
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
# Constants, Fixtures & Globals.
# -----------------------------------------------------------------------------
from libs.utils import terminate_fatal

LOGGER = initialise_logger()


def check_directory(directory_name):
    get_config(LOGGER)

    if os.path.isdir(directory_name):
        try:
            shutil.rmtree(directory_name)
        except OSError:
            terminate_fatal(
                LOGGER,
                " : The directory "
                + directory_name
                + " can not be deleted"
                + " - error code="
                + OSError.errno
                + " message="
                + OSError.strerror,
            )

    assert os.path.isdir(directory_name) is False

    try:
        os.mkdir(directory_name)
    except OSError:
        terminate_fatal(
            LOGGER,
            " : The directory "
            + directory_name
            + " can not be created"
            + " - error code="
            + OSError.errno
            + " message="
            + OSError.strerror,
        )

    assert os.path.isdir(directory_name) is True

    try:
        shutil.rmtree(directory_name)
    except OSError:
        terminate_fatal(
            LOGGER,
            " : The directory "
            + directory_name
            + " can not be deleted"
            + " - error code="
            + OSError.errno
            + " message="
            + OSError.strerror,
        )

    assert os.path.isdir(directory_name) is False


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
    """Test: Duplicate argument."""
    assert get_args(
        LOGGER,
        ["n/a", ACTION_DB_CREATE_OR_UPGRADE, ACTION_DB_CREATE_OR_UPGRADE],
    ) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: False,
    }


def test_get_args_valid_2() -> None:
    """Test: Two valid arguments."""
    assert get_args(
        LOGGER,
        ["n/a", ACTION_DB_CREATE_OR_UPGRADE, ACTION_PROCESS_INBOX_OCR],
    ) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: False,
        ACTION_PROCESS_INBOX_OCR: True,
    }


def test_get_args_valid_new() -> None:
    """Test: Special argument `new`."""
    assert get_args(LOGGER, ["n/a", ACTION_NEW_COMPLETE]) == {
        ACTION_DB_CREATE_OR_UPGRADE: True,
        ACTION_PROCESS_INBOX: True,
        ACTION_PROCESS_INBOX_OCR: True,
    }


# -----------------------------------------------------------------------------
# Test Function - get_config().
# -----------------------------------------------------------------------------
def test_get_config() -> None:
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
# Test Environment.
# -----------------------------------------------------------------------------
def test_environ_db_file() -> None:
    """Test: Environment - Database file."""
    get_config(LOGGER)

    if os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]):
        try:
            os.remove(CONFIG[DCR_CFG_DATABASE_FILE])
        except OSError:
            terminate_fatal(
                LOGGER,
                " : The database file "
                + CONFIG[DCR_CFG_DATABASE_FILE]
                + " can not be deleted"
                + " - error code="
                + OSError.errno
                + " message="
                + OSError.strerror,
            )

    assert os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]) is False


def test_environ_dir_inbox_delete() -> None:
    """Test: Environment - Directory inbox."""
    get_config(LOGGER)

    if os.path.isdir(CONFIG[DCR_CFG_DIRECTORY_INBOX]):
        try:
            shutil.rmtree(CONFIG[DCR_CFG_DIRECTORY_INBOX])
        except OSError:
            terminate_fatal(
                LOGGER,
                " : The directory "
                + CONFIG[DCR_CFG_DIRECTORY_INBOX]
                + " can not be deleted"
                + " - error code="
                + OSError.errno
                + " message="
                + OSError.strerror,
            )

    assert os.path.isdir(CONFIG[DCR_CFG_DIRECTORY_INBOX]) is False


def test_environ_dir_inbox_create() -> None:
    """Test: Environment - Directory inbox."""
    check_directory(CONFIG[DCR_CFG_DIRECTORY_INBOX])


def test_environ_dir_inbox_accepted_create() -> None:
    """Test: Environment - Directory inbox_accepted."""
    check_directory(CONFIG[DCR_CFG_DIRECTORY_INBOX_ACCEPTED])


def test_environ_dir_inbox_rejected_create() -> None:
    """Test: Environment - Directory inbox_recjected."""
    check_directory(CONFIG[DCR_CFG_DIRECTORY_INBOX_REJECTED])


def test_environ_dir_inbox_ocr_create() -> None:
    """Test: Environment - Directory inbox_ocr."""
    check_directory(CONFIG[DCR_CFG_DIRECTORY_INBOX_OCR])


def test_environ_dir_inbox_ocr_accepted_create() -> None:
    """Test: Environment - Directory inbox_ocr_accepted."""
    check_directory(CONFIG[DCR_CFG_DIRECTORY_INBOX_OCR_ACCEPTED])


def test_environ_dir_inbox_ocr_rejected_create() -> None:
    """Test: Environment - Directory inbox_ocr_recjected."""
    check_directory(CONFIG[DCR_CFG_DIRECTORY_INBOX_OCR_REJECTED])


# -----------------------------------------------------------------------------
# Test Function - main().
# -----------------------------------------------------------------------------
def test_main_p_i_missing_db() -> None:
    """Test: ACTION_PROCESS_INBOX - DB missing."""
    get_config(LOGGER)

    if not os.path.isdir(CONFIG[DCR_CFG_DIRECTORY_INBOX]):
        try:
            os.mkdir(CONFIG[DCR_CFG_DIRECTORY_INBOX])
        except OSError:
            terminate_fatal(
                LOGGER,
                " : The directory "
                + CONFIG[DCR_CFG_DIRECTORY_INBOX]
                + " can not be created"
                + " - error code="
                + OSError.errno
                + " message="
                + OSError.strerror,
            )

    if os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]):
        try:
            os.remove(CONFIG[DCR_CFG_DATABASE_FILE])
        except OSError:
            terminate_fatal(
                LOGGER,
                " : The directory "
                + CONFIG[DCR_CFG_DATABASE_FILE]
                + " can not be created"
                + " - error code="
                + OSError.errno
                + " message="
                + OSError.strerror,
            )

    with pytest.raises(SystemExit) as expt:
        main(["pytest", ACTION_PROCESS_INBOX])

    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_main_d_c_u() -> None:
    """Test: ACTION_DB_CREATE_OR_UPGRADE."""
    get_config(LOGGER)

    main(["pytest", ACTION_DB_CREATE_OR_UPGRADE])

    assert os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]) is True


def test_main_p_i() -> None:
    """Test: ACTION_PROCESS_INBOX."""
    get_config(LOGGER)

    main(["pytest", ACTION_PROCESS_INBOX])
