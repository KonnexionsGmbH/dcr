"""Testing Module conftest."""
import os
from pathlib import Path

import libs.cfg

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - fxtr_mkdir,
#                 fxtr_rmdir,
#                 fxtr_rmdir_opt.
# -----------------------------------------------------------------------------
def test_mkdir_rmdir_rmdir_opt(fxtr_mkdir, fxtr_rmdir, fxtr_rmdir_opt):
    """Test: Pure functionality."""
    directory_name: os.PathLike = Path("tmp")

    fxtr_rmdir_opt(directory_name)

    fxtr_mkdir(directory_name)
    fxtr_rmdir(directory_name)

    fxtr_mkdir(directory_name)
    fxtr_rmdir_opt(directory_name)
    fxtr_rmdir_opt(directory_name)


# -----------------------------------------------------------------------------
# Test Function - fxtr_setup_empty_db_and_inbox
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
def test_setup_empty_db_and_inbox(fxtr_setup_empty_db_and_inbox):
    """Test: Pure functionality."""
    libs.cfg.logger.debug("")
    libs.cfg.logger.debug("===============================================")
    libs.cfg.logger.debug("=======> test_setup_empty_db_and_inbox <=======")
    libs.cfg.logger.debug("===============================================")


# -----------------------------------------------------------------------------
# Test Function - fxtr_setup_logger
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
def test_setup_logger(fxtr_setup_logger):
    """Test: Pure functionality."""
    libs.cfg.logger.debug("")
    libs.cfg.logger.debug("===============================================")
    libs.cfg.logger.debug("=============> test_setup_logger <=============")
    libs.cfg.logger.debug("===============================================")


# -----------------------------------------------------------------------------
# Test Function - fxtr_setup_logger_environment
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
def test_setup_logger_environment(fxtr_setup_logger_environment):
    """Test: Pure functionality."""
    libs.cfg.logger.debug("")
    libs.cfg.logger.debug("===============================================")
    libs.cfg.logger.debug("=======> test_setup_logger_environment <=======")
    libs.cfg.logger.debug("===============================================")
