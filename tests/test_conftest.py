"""Testing Module conftest."""
import os
import pathlib

import dcr.cfg.glob

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
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    directory_path: os.PathLike = pathlib.Path("tmp")

    fxtr_rmdir_opt(directory_path)

    fxtr_mkdir(directory_path)
    fxtr_rmdir(directory_path)

    fxtr_mkdir(directory_path)
    fxtr_rmdir_opt(directory_path)
    fxtr_rmdir_opt(directory_path)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - fxtr_setup_logger
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
def test_setup_logger(fxtr_setup_logger):
    """Test: Pure functionality."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("")
    dcr.cfg.glob.logger.info("===============================================")
    dcr.cfg.glob.logger.info("=============> test_setup_logger <=============")
    dcr.cfg.glob.logger.info("===============================================")

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - fxtr_setup_logger_environment
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
def test_setup_logger_environment(fxtr_setup_logger_environment):
    """Test: Pure functionality."""
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.info("")
    dcr.cfg.glob.logger.info("===============================================")
    dcr.cfg.glob.logger.info("=======> test_setup_logger_environment <=======")
    dcr.cfg.glob.logger.info("===============================================")

    # -------------------------------------------------------------------------
    dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)
