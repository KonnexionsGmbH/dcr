"""Testing Module conftest."""
import os
import pathlib

import cfg.glob

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - fxtr_mkdir,
#                 fxtr_rmdir,
#                 fxtr_rmdir_opt.
# -----------------------------------------------------------------------------
def test_mkdir_rmdir_rmdir_opt(fxtr_mkdir, fxtr_rmdir, fxtr_rmdir_opt):
    """Test: Pure functionality."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    directory_path: os.PathLike = pathlib.Path("tmp")

    fxtr_rmdir_opt(directory_path)

    fxtr_mkdir(directory_path)
    fxtr_rmdir(directory_path)

    fxtr_mkdir(directory_path)
    fxtr_rmdir_opt(directory_path)
    fxtr_rmdir_opt(directory_path)

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - fxtr_setup_empty_db_and_inbox
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
def test_setup_empty_db_and_inbox(fxtr_setup_empty_db_and_inbox):
    """Test: Pure functionality."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("")
    cfg.glob.logger.info("===============================================")
    cfg.glob.logger.info("=======> test_setup_empty_db_and_inbox <=======")
    cfg.glob.logger.info("===============================================")

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - fxtr_setup_logger
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
def test_setup_logger(fxtr_setup_logger):
    """Test: Pure functionality."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("")
    cfg.glob.logger.info("===============================================")
    cfg.glob.logger.info("=============> test_setup_logger <=============")
    cfg.glob.logger.info("===============================================")

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - fxtr_setup_logger_environment
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
def test_setup_logger_environment(fxtr_setup_logger_environment):
    """Test: Pure functionality."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("")
    cfg.glob.logger.info("===============================================")
    cfg.glob.logger.info("=======> test_setup_logger_environment <=======")
    cfg.glob.logger.info("===============================================")

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
