"""Testing Module conftest."""

import os
from pathlib import Path

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
dcr.initialise_logger()


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


# -----------------------------------------------------------------------------
# Test Function - fxtr_drop_database
#                 fxtr_mkdir,
#                 fxtr_rmdir_opt
# -----------------------------------------------------------------------------
def test_file_ops(fxtr_mkdir, fxtr_drop_database, fxtr_rmdir_opt):
    """Test: Pure functionality."""
    directory_name: os.PathLike = Path("tmp")
    file_name: str = os.path.join(directory_name, "test_file")

    # Create empty file directory.
    fxtr_rmdir_opt(directory_name)
    fxtr_mkdir(directory_name)
    # The file does not yet exist.
    fxtr_drop_database()
    # The file will be created.
    Path(file_name).touch()
    fxtr_drop_database(file_name)
    # The file will be created.
    Path(file_name).touch()
    fxtr_drop_database()
