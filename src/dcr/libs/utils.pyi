"""Library stub."""

import logging

def progress_msg(logger: logging.Logger, msg: str) -> None: ...
def terminate_fatal(logger: logging.Logger, error_msg: str) -> None: ...
