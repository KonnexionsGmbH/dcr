"""Module utils: Helper functions."""
import datetime
import hashlib
import sys

from libs import cfg


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
    cfg.logger.debug(cfg.LOGGER_START)

    sha256_hash = hashlib.sha256()

    with open(file_name, "rb") as file:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)

    cfg.logger.debug(cfg.LOGGER_END)

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
    cfg.logger.debug(cfg.LOGGER_START)

    print("")
    print(cfg.LOGGER_FATAL_HEAD)
    print(cfg.LOGGER_FATAL_HEAD, error_msg, cfg.LOGGER_FATAL_TAIL, sep="")
    print(cfg.LOGGER_FATAL_HEAD)
    cfg.logger.critical(
        "%s%s%s", cfg.LOGGER_FATAL_HEAD, error_msg, cfg.LOGGER_FATAL_TAIL
    )

    cfg.logger.debug(cfg.LOGGER_END)

    sys.exit(1)
