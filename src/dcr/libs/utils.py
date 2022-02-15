"""Module utils: Helper functions."""
import datetime
import hashlib
import os
import sys

from libs import cfg


# -----------------------------------------------------------------------------
# Get the file name as per inbox.
# -----------------------------------------------------------------------------
def get_file_name_inbox() -> str:
    """Get the file name as per inbox.

    Returns:
        str: File name as per inbox.
    """
    return os.path.join(cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX], cfg.file_name)


# -----------------------------------------------------------------------------
# Get the file name as per inbox accepted.
# -----------------------------------------------------------------------------
def get_file_name_inbox_accepted() -> str:
    """Get the file name as per inbox accepted.

    Returns:
        str: File name as per inbox accepted.
    """
    return os.path.join(
        cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED],
        cfg.stem_name + "_" + str(cfg.document_id) + "." + cfg.file_type,
    )


# -----------------------------------------------------------------------------
# Get the file name as per inbox rejected.
# -----------------------------------------------------------------------------
def get_file_name_inbox_rejected() -> str:
    """Get the file name as per inbox rejected.

    Returns:
        str: File name as per inbox rejected.
    """
    return os.path.join(
        cfg.config[cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED],
        cfg.stem_name + "_" + str(cfg.document_id) + "." + cfg.file_type,
    )


# -----------------------------------------------------------------------------
# Get the SHA256 hash string of a file.
# -----------------------------------------------------------------------------
def get_sha256(file_name: str) -> str:
    """Get the SHA256 hash string of a file.

    Args:
        file_name (str): File name.

    Returns:
        str: SHA256 hash string.
    """
    sha256_hash = hashlib.sha256()

    with open(file_name, "rb") as file:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


# -----------------------------------------------------------------------------
# Terminate the application immediately.
# -----------------------------------------------------------------------------
def progress_msg(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    final_msg: str = (
        cfg.LOGGER_PROGRESS_UPDATE
        + str(datetime.datetime.now())
        + " : "
        + msg
        + "."
    )

    print(final_msg)
    cfg.logger.debug(final_msg)


# -----------------------------------------------------------------------------
# Terminate the application immediately.
# -----------------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message.
    """
    print("")
    print(cfg.LOGGER_FATAL_HEAD)
    print(cfg.LOGGER_FATAL_HEAD, error_msg, cfg.LOGGER_FATAL_TAIL, sep="")
    print(cfg.LOGGER_FATAL_HEAD)
    cfg.logger.critical(
        "%s%s%s", cfg.LOGGER_FATAL_HEAD, error_msg, cfg.LOGGER_FATAL_TAIL
    )
    sys.exit(1)
