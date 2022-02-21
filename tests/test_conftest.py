"""Testing Module conftest."""

import os
from pathlib import Path

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - fxtr_no_db_docker_container
# -----------------------------------------------------------------------------
def test_db_docker_container(fxtr_no_db_docker_container, fxtr_setup_logger_environment):
    """Test: Pure functionality."""
    fxtr_setup_logger_environment()

    fxtr_no_db_docker_container()

    fxtr_no_db_docker_container()


# -----------------------------------------------------------------------------
# Test Function - fxtr_mkdir,
#                 fxtr_mkdir_opt,
#                 fxtr_rmdir,
#                 fxtr_rmdir_opt.
# -----------------------------------------------------------------------------
def test_dir_ops(fxtr_mkdir, fxtr_mkdir_opt, fxtr_rmdir, fxtr_rmdir_opt):
    """Test: Pure functionality."""
    directory_name: os.PathLike = Path("tmp")

    # It is not known whether the directory is already in place.
    fxtr_mkdir_opt(directory_name)
    # The directory already exists.
    fxtr_mkdir_opt(directory_name)
    fxtr_rmdir(directory_name)
    # The directory no longer exists
    fxtr_mkdir(directory_name)
    fxtr_rmdir(directory_name)
    # The directory no longer exists
    fxtr_rmdir_opt(directory_name)
