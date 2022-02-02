"""Library stub."""

import logging
from os import PathLike

def check_and_create_inboxes(
    logger: logging.Logger,
) -> tuple[PathLike[str] | str, PathLike[str] | str, PathLike[str] | str]: ...
def process_inbox(logger: logging.Logger) -> None: ...
def process_new_input(
    logger: logging.Logger,
    inbox: str,
    inbox_accepted: str,
    inbox_rejected: str,
) -> None: ...
