"""
### Database Schema Management.

Database schema-related processing routines.
"""

import logging
import logging.config

import sqlalchemy.orm
from sqlalchemy import insert
from utils.constant import LOGGER_END
from utils.constant import LOGGER_START


# -----------------------------------------------------------------------------
# Inserts the current version number in the version table.
# -----------------------------------------------------------------------------


def insert_version_number(
    logger: logging.Logger,
    config: dict[str, str],
    engine: sqlalchemy.engine.base.Engine,
    version: sqlalchemy.Table,
) -> None:
    """
    **Initialise the database table version**.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of dcr is
    inserted.

    **Args**:
    - **logger  (logging.Logger):**   Current logger.
    - **config  (dict[str, str]):**   Configuration parameters.
    - **engine  (sqlalchemy.engine.base.Engine)**:
                                      Database state.
    - **version (sqlalchemy.Table):** Schema of database table `version`.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    with engine.connect() as conn:
        conn.execute(insert(version), [{"version": config["dcr_version"]}])
        conn.commit()

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)
