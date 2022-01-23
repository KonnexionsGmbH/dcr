"""
### Module: **Database Schema Management**.

Database schema-related processing routines.
"""

import logging
import logging.config
import sys
from os import PathLike
from typing import Union

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy.engine import Engine

from utils.constant import DBC_VERSION
from utils.constant import DBT_VERSION
from utils.constant import DCR_CFG_DCR_VERSION
from utils.constant import LOGGER_END
from utils.constant import LOGGER_START
from utils.db import get_engine
from utils.db import get_metadata


# -----------------------------------------------------------------------------
# Get the version number from the database table version.
# -----------------------------------------------------------------------------


def get_version_number(
    logger: logging.Logger,
    config: dict[str, Union[Engine, PathLike[str], str]],
) -> str:
    """
    #### Function: **Get the version number.**.

    Get the version number from the database table `version`.

    **Args**:
    - **logger  (logging.Logger):**                Current logger.
    - **config  (dict[str, Union[Engine, PathLike[str], str]]):**
                                                   Configuration parameters.
    - **version (sqlalchemy.Table):**              Schema of database table
                                                   `version`.

    **Returns**:
    - **str**: The version number found.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    current_version: str = ""

    with get_engine(config).connect() as conn:
        for row in conn.execute(select(DBT_VERSION, DBC_VERSION)):
            if current_version == "":
                current_version = row.getattr(DBT_VERSION, DBC_VERSION)
            else:
                logger.error(
                    "fatal error: program abort =====> "
                    + "current version in database table version is not unique"
                    + " <====="
                )
                sys.exit(1)

    if current_version == "":
        logger.error(
            "fatal error: program abort =====> "
            + "current version in database table version is missing"
            + " <====="
        )
        sys.exit(1)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)

    return current_version


# -----------------------------------------------------------------------------
# Inserts the current version number into the database table version.
# -----------------------------------------------------------------------------


def insert_current_version_number(
    logger: logging.Logger,
    config: dict[str, Union[Engine, PathLike[str], str]],
) -> None:
    """
    #### Function: **Insert the current version number.**.

    Inserts the current version number from the configuration parameters
    into the database table `version`.

    **Args**:
    - **logger  (logging.Logger):**                Current logger.
    - **config  (dict[str, Union[Engine, PathLike[str], str]]):**
                                                   Configuration parameters.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    version = Table(
        DBT_VERSION, get_metadata(config), autoload_with=get_engine(config)
    )

    with get_engine(config).connect() as conn:
        conn.execute(
            insert(version), [{DBT_VERSION: config[DCR_CFG_DCR_VERSION]}]
        )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)
