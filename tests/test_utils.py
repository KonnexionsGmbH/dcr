"""Test Module."""

import pytest

from app import initialise_logger
from libs.utils import terminate_fatal

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
LOGGER = initialise_logger()


# -----------------------------------------------------------------------------
# Terminate the application immediately.
# -----------------------------------------------------------------------------
def test_terminate_fatal() -> None:
    """Test Function."""
    with pytest.raises(SystemExit) as expt:
        terminate_fatal(LOGGER, "test error message")
    assert expt.type == SystemExit
    assert expt.value.code == 1
