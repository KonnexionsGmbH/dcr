# pylint: disable=unused-argument
"""Testing Module dcr.utils."""
import pathlib

import dcr_core.core_glob  # pylint: disable=cyclic-import
import dcr_core.core_utils  # pylint: disable=cyclic-import
import pytest

import dcr.cfg.glob
import dcr.db.cls_db_core
import dcr.utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - get_file_type().
# -----------------------------------------------------------------------------
def test_get_file_type():
    """Test: get_file_type()."""
    assert dcr.utils.get_file_type(None) == ""


# -----------------------------------------------------------------------------
# Test Function - get_full_name().
# -----------------------------------------------------------------------------
def test_get_full_name():
    """Test: get_full_name()."""
    assert dcr_core.core_utils.get_full_name(None, None) == ""

    directory_name = pathlib.Path("D:/SoftDevelopment")

    dcr_core.core_utils.get_full_name(directory_name, "docx_ok.docx")


# -----------------------------------------------------------------------------
# Test Function - get_os_independent_name().
# -----------------------------------------------------------------------------
def test_get_os_independent_name():
    """Test: get_os_independent_name()."""
    file_name = pathlib.Path("D:/SoftDevelopment")

    dcr_core.core_utils.get_os_independent_name(file_name)


# -----------------------------------------------------------------------------
# Test Function - get_path_name().
# -----------------------------------------------------------------------------
def test_get_path_name():
    """Test: get_path_name()."""
    assert dcr.utils.get_path_name(None) == ""


# -----------------------------------------------------------------------------
# Test Function - get_stem_name().
# -----------------------------------------------------------------------------
def test_get_stem_name():
    """Test: get_stem_name()."""
    assert dcr_core.core_utils.get_stem_name(None) == ""


# -----------------------------------------------------------------------------
# Test Function - progress_msg_disconnected() - case 1.
# -----------------------------------------------------------------------------
def test_progress_msg_disconnected_1(fxtr_setup_logger_environment):
    """Test: get_file_type()- case 1."""
    dcr_core.core_glob.setup.is_verbose = True

    # -------------------------------------------------------------------------
    dcr.utils.progress_msg_disconnected()

    # -------------------------------------------------------------------------
    del dcr_core.core_glob.setup

    dcr.utils.progress_msg_connected(
        database=dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE, user=dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE
    )

    # -------------------------------------------------------------------------
    dcr.utils.progress_msg_disconnected()

    # -------------------------------------------------------------------------
    dcr.utils.progress_msg_empty_before("Test")

    with pytest.raises(SystemExit) as expt:
        dcr_core.core_utils.terminate_fatal("Test")

    assert expt.type == SystemExit, "End of programme without object 'dcr.cfg.glob.setup'"
    assert expt.value.code == 1, "End of programme without object 'dcr.cfg.glob.setup'"


# -----------------------------------------------------------------------------
# Test Function - progress_msg_disconnected()- case 1.
# -----------------------------------------------------------------------------
def test_progress_msg_disconnected_2(fxtr_setup_empty_db_and_inbox):
    """Test: get_file_type()."""
    dcr_core.core_glob.setup.is_verbose = True

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    dcr.cfg.glob.db_core.db_current_database = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE
    dcr.cfg.glob.db_core.db_current_user = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE

    dcr.utils.progress_msg_disconnected()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    dcr.cfg.glob.db_core.db_current_database = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE
    dcr.cfg.glob.db_core.db_current_user = ""

    dcr.utils.progress_msg_disconnected()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    dcr.cfg.glob.db_core.db_current_database = ""
    dcr.cfg.glob.db_core.db_current_user = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE

    dcr.utils.progress_msg_disconnected()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    dcr.cfg.glob.db_core.db_current_database = ""
    dcr.cfg.glob.db_core.db_current_user = ""

    dcr.utils.progress_msg_disconnected()
