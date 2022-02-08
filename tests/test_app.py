# pylint: disable=unused-argument
"""Testing Module dcr."""

import libs.cfg
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
LOGGER = dcr.initialise_logger()


# -----------------------------------------------------------------------------
# Test Function - get_args().
# -----------------------------------------------------------------------------
def test_get_args_no():
    """Test: No command line arguments found."""
    with pytest.raises(SystemExit) as expt:
        dcr.get_args(LOGGER, [])

    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_get_args_one():
    """Test: The specific command line arguments are missing."""
    with pytest.raises(SystemExit) as expt:
        dcr.get_args(LOGGER, [""])

    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_get_args_unknown():
    """Test: Unknown command line argument=xxx."""
    with pytest.raises(SystemExit) as expt:
        dcr.get_args(LOGGER, ["n/a", "second"])

    assert expt.type == SystemExit
    assert expt.value.code == 1


# -----------------------------------------------------------------------------
# Test Function - main().
# -----------------------------------------------------------------------------
def test_main_all(fxtr_new_db_empty_inbox):
    """Test: ACTION_ALL_COMPLETE."""
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_ALL_COMPLETE])


def test_main_p_i_no_db(fxtr_no_db):
    """Test: ACTION_PROCESS_INBOX - DB missing."""
    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_main_p_i_no_inbox(fxtr_new_db_no_inbox):
    """Test: ACTION_PROCESS_INBOX - Inbox missing."""
    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    assert expt.type == SystemExit
    assert expt.value.code == 1


def test_main_p_i(fxtr_new_db_empty_inbox):
    """Test: ACTION_PROCESS_INBOX."""
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])
