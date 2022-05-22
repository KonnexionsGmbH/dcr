# pylint: disable=unused-argument
"""Testing Module dcr.utils."""
import pathlib

import pytest

import cfg.glob
import utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - get_file_type().
# -----------------------------------------------------------------------------
def test_get_file_type():
    """Test: get_file_type()."""
    assert "" == utils.get_file_type(None)


# -----------------------------------------------------------------------------
# Test Function - get_full_name().
# -----------------------------------------------------------------------------
def test_get_full_name():
    """Test: get_full_name()."""
    assert "" == utils.get_full_name(None, None)

    directory_name = pathlib.Path("D:/SoftDevelopment")

    utils.get_full_name(directory_name, "docx_ok.docx")


# -----------------------------------------------------------------------------
# Test Function - get_os_independent_name().
# -----------------------------------------------------------------------------
def test_get_os_independent_name():
    """Test: get_os_independent_name()."""
    file_name = pathlib.Path("D:/SoftDevelopment")

    utils.get_os_independent_name(file_name)


# -----------------------------------------------------------------------------
# Test Function - get_path_name().
# -----------------------------------------------------------------------------
def test_get_path_namee():
    """Test: get_path_name()."""
    assert "" == utils.get_path_name(None)


# -----------------------------------------------------------------------------
# Test Function - get_stem_name().
# -----------------------------------------------------------------------------
def test_get_stem_name():
    """Test: get_stem_name()."""
    assert "" == utils.get_stem_name(None)


# -----------------------------------------------------------------------------
# Test Function - progress_msg_disconnected().
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test_progress_msg_disconnected(fxtr_setup_logger_environment):
    """Test: get_file_type()."""
    cfg.glob.setup.is_verbose = True
    cfg.glob.db_current_database = None
    cfg.glob.db_current_user = None

    utils.progress_msg_disconnected()

    del cfg.glob.setup

    utils.progress_msg_connected()

    utils.progress_msg_disconnected()

    utils.progress_msg_empty_before("Test")

    with pytest.raises(SystemExit) as expt:
        utils.terminate_fatal("Test")

    assert expt.type == SystemExit, "End of programme without object 'cfg.glob.setup'"
    assert expt.value.code == 1, "End of programme without object 'cfg.glob.setup'"

