"""Testing Module `database`."""
import os

import pytest

from app import get_config
from app import initialise_logger
from app import main
from libs.database import check_db_up_to_date
from libs.globals import ACTION_DB_CREATE_OR_UPGRADE
from libs.globals import CONFIG
from libs.globals import DCR_CFG_DATABASE_FILE
from libs.globals import DCR_CFG_DCR_VERSION
# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
from libs.utils import terminate_fatal

LOGGER = initialise_logger()


# -----------------------------------------------------------------------------
# Test Function - check_db_up_to_date().
# -----------------------------------------------------------------------------
def test_check_db_up_to_date_no_db() -> None:
    """Test: No database file existing."""
    get_config(LOGGER)

    if os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]):
        try:
            os.remove(CONFIG[DCR_CFG_DATABASE_FILE])
        except OSError:
            terminate_fatal(
                LOGGER,
                " : The database file "
                + CONFIG[DCR_CFG_DATABASE_FILE]
                + " can not be deleted"
                + " - error code="
                + OSError.errno
                + " message="
                + OSError.strerror,
            )

    assert os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]) is False

    with pytest.raises(SystemExit) as expt:
        check_db_up_to_date(LOGGER)
        assert expt.type == SystemExit
        assert expt.value.code == 1


def test_check_db_up_to_date_wrong_version() -> None:
    """Test: No database file existing."""
    get_config(LOGGER)

    if os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]):
        try:
            os.remove(CONFIG[DCR_CFG_DATABASE_FILE])
        except OSError:
            terminate_fatal(
                LOGGER,
                " : The database file "
                + CONFIG[DCR_CFG_DATABASE_FILE]
                + " can not be deleted"
                + " - error code="
                + OSError.errno
                + " message="
                + OSError.strerror,
            )

    main(["pytest", ACTION_DB_CREATE_OR_UPGRADE])

    assert os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]) is True

    CONFIG[DCR_CFG_DCR_VERSION] = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        check_db_up_to_date(LOGGER)
        assert expt.type == SystemExit
        assert expt.value.code == 1


def test_check_db_up_to_date() -> None:
    """Test: Functionality."""
    get_config(LOGGER)

    if os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]):
        try:
            os.remove(CONFIG[DCR_CFG_DATABASE_FILE])
        except OSError:
            terminate_fatal(
                LOGGER,
                " : The database file "
                + CONFIG[DCR_CFG_DATABASE_FILE]
                + " can not be deleted"
                + " - error code="
                + OSError.errno
                + " message="
                + OSError.strerror,
            )

    main(["pytest", ACTION_DB_CREATE_OR_UPGRADE])

    assert os.path.isfile(CONFIG[DCR_CFG_DATABASE_FILE]) is True

    check_db_up_to_date(LOGGER)
