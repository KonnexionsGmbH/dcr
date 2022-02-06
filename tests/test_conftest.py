"""Testing Module conftest."""

import os
from pathlib import Path

import touch

from dcr import initialise_logger

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
LOGGER = initialise_logger()


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
    fxtr_mkdir_opt(directory_name)
    # The directory already exists.
    fxtr_mkdir_opt(directory_name)
    fxtr_rmdir(directory_name)
    # The directory no longer exists
    fxtr_mkdir(directory_name)
    fxtr_rmdir(directory_name)
    # The directory no longer exists
    fxtr_rmdir_opt(directory_name)


# -----------------------------------------------------------------------------
# Test Function - fxtr_mkdir_opt,
#                 fxtr_remove,
#                 fxtr_remove_opt,
#                 fxtr_rmdir_opt
# -----------------------------------------------------------------------------
def test_file_ops(
    fxtr_mkdir_opt, fxtr_remove, fxtr_remove_opt, fxtr_rmdir_opt
):
    """Test: Pure functionality."""
    directory_name: os.PathLike = Path("tmp")
    file_name: str = os.path.join(directory_name, "test_file")

    # Create empty file directory.
    fxtr_rmdir_opt(directory_name)
    fxtr_mkdir_opt(directory_name)
    # The file does not yet exist.
    fxtr_remove_opt(file_name)
    # The file will be created.
    touch.touch(file_name)
    fxtr_remove(file_name)
    # The file will be created.
    touch.touch(file_name)
    fxtr_remove_opt(file_name)
    fxtr_remove_opt(file_name)
