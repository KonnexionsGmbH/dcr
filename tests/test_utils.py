# -*- coding: utf-8 -*-

# pylint: disable=unused-argument
"""Testing Module dcr.utils."""
import pathlib

import cfg.glob
import db.cls_db_core
import pytest
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
    assert utils.get_file_type(None) == ""


# -----------------------------------------------------------------------------
# Test Function - get_full_name().
# -----------------------------------------------------------------------------
def test_get_full_name():
    """Test: get_full_name()."""
    assert utils.get_full_name(None, None) == ""

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
def test_get_path_name():
    """Test: get_path_name()."""
    assert utils.get_path_name(None) == ""


# -----------------------------------------------------------------------------
# Test Function - get_stem_name().
# -----------------------------------------------------------------------------
def test_get_stem_name():
    """Test: get_stem_name()."""
    assert utils.get_stem_name(None) == ""


# -----------------------------------------------------------------------------
# Test Function - progress_msg_disconnected() - case 1.
# -----------------------------------------------------------------------------
def test_progress_msg_disconnected_1(fxtr_setup_logger_environment):
    """Test: get_file_type()- case 1."""
    cfg.glob.setup.is_verbose = True

    # -------------------------------------------------------------------------
    utils.progress_msg_disconnected()

    # -------------------------------------------------------------------------
    del cfg.glob.setup

    utils.progress_msg_connected(
        database=cfg.glob.INFORMATION_NOT_YET_AVAILABLE, user=cfg.glob.INFORMATION_NOT_YET_AVAILABLE
    )

    # -------------------------------------------------------------------------
    utils.progress_msg_disconnected()

    # -------------------------------------------------------------------------
    utils.progress_msg_empty_before("Test")

    with pytest.raises(SystemExit) as expt:
        utils.terminate_fatal("Test")

    assert expt.type == SystemExit, "End of programme without object 'cfg.glob.setup'"
    assert expt.value.code == 1, "End of programme without object 'cfg.glob.setup'"


# -----------------------------------------------------------------------------
# Test Function - progress_msg_disconnected()- case 1.
# -----------------------------------------------------------------------------
def test_progress_msg_disconnected_2(fxtr_setup_empty_db_and_inbox):
    """Test: get_file_type()."""
    cfg.glob.setup.is_verbose = True

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    cfg.glob.db_core.db_current_database = cfg.glob.INFORMATION_NOT_YET_AVAILABLE
    cfg.glob.db_core.db_current_user = cfg.glob.INFORMATION_NOT_YET_AVAILABLE

    utils.progress_msg_disconnected()

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    cfg.glob.db_core.db_current_database = cfg.glob.INFORMATION_NOT_YET_AVAILABLE
    cfg.glob.db_core.db_current_user = ""

    utils.progress_msg_disconnected()

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    cfg.glob.db_core.db_current_database = ""
    cfg.glob.db_core.db_current_user = cfg.glob.INFORMATION_NOT_YET_AVAILABLE

    utils.progress_msg_disconnected()

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    cfg.glob.db_core.db_current_database = ""
    cfg.glob.db_core.db_current_user = ""

    utils.progress_msg_disconnected()
