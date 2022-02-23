"""Helper functions.

Returns:
    [type]: None.
"""
import datetime
import hashlib
import pathlib
import sys
import traceback

import libs.cfg
import libs.db.cfg
import libs.db.driver
import libs.utils


# -----------------------------------------------------------------------------
# Get the SHA256 hash string of a file.
# -----------------------------------------------------------------------------
def get_sha256(file: pathlib.Path) -> str:
    """Get the SHA256 hash string of a file.

    Args:
        file (: pathlib.Path): File.

    Returns:
        str: SHA256 hash string.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sha256_hash = hashlib.sha256()

    with open(file, "rb") as file_content:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file_content.read(4096), b""):
            sha256_hash.update(byte_block)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    return sha256_hash.hexdigest()


# -----------------------------------------------------------------------------
# Create a progress message.
# -----------------------------------------------------------------------------
def progress_msg(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    if libs.cfg.is_verbose:
        final_msg: str = (
            libs.cfg.LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg + "."
        )

        print(final_msg)

        libs.cfg.logger.debug(final_msg)


# -----------------------------------------------------------------------------
# Create a progress message: connected to database.
# -----------------------------------------------------------------------------
def progress_msg_connected() -> None:
    """Create a progress message: connected to database."""
    if libs.cfg.is_verbose:
        print("")
        progress_msg(
            "User '"
            + libs.db.cfg.db_current_user
            + "' is now connected to database '"
            + libs.db.cfg.db_current_database
            + "'"
        )


# -----------------------------------------------------------------------------
# Create a progress message: disconnected from database.
# -----------------------------------------------------------------------------
def progress_msg_disconnected() -> None:
    """Create a progress message: disconnected from database."""
    if libs.cfg.is_verbose:
        if libs.db.cfg.db_current_database is None and libs.db.cfg.db_current_user is None:
            print("")
            libs.utils.progress_msg("Database is now disconnected")
            return

        database = (
            "n/a" if libs.db.cfg.db_current_database is None else libs.db.cfg.db_current_database
        )
        user = "n/a" if libs.db.cfg.db_current_user is None else libs.db.cfg.db_current_user

        print("")
        libs.utils.progress_msg(
            "User '" + user + "' is now disconnected from database '" + database + "'"
        )

        libs.db.cfg.db_current_database = None
        libs.db.cfg.db_current_user = None


# -----------------------------------------------------------------------------
# Create a progress message with empty line before.
# -----------------------------------------------------------------------------
def progress_msg_empty_before(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    if libs.cfg.is_verbose:
        print("")
        progress_msg(msg)


# -----------------------------------------------------------------------------
# Terminate the application immediately.
# -----------------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    print("")
    print(libs.cfg.LOGGER_FATAL_HEAD)
    print(libs.cfg.LOGGER_FATAL_HEAD, error_msg, libs.cfg.LOGGER_FATAL_TAIL, sep="")
    print(libs.cfg.LOGGER_FATAL_HEAD)
    libs.cfg.logger.critical(
        "%s%s%s", libs.cfg.LOGGER_FATAL_HEAD, error_msg, libs.cfg.LOGGER_FATAL_TAIL
    )

    traceback.print_exc()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    libs.db.driver.disconnect_db()

    sys.exit(1)
