"""
### Database Schema Management.

Database schema-related processing routines.
"""

import datetime
import logging
import logging.config

import sqlalchemy
import sqlalchemy.orm
from db.ddl import check_schema_existence
from utils.constant import LOGGER_END
from utils.constant import LOGGER_PROGRESS_UPDATE
from utils.constant import LOGGER_START


# -----------------------------------------------------------------------------
# Initialise the database.
# -----------------------------------------------------------------------------


def get_engine(
    logger: logging.Logger, config: dict[str, str]
) -> sqlalchemy.engine.base.Engine:
    """
    **Initialise the database**.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    - **config (dict[str, str])**: Configuration parameters.

    Returns:
    - **sqlalchemy.engine.base.Engine**: Database state.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    engine = sqlalchemy.create_engine(config["database_url"])

    check_schema_existence(logger, config, engine)

    print(
        LOGGER_PROGRESS_UPDATE
        + str(datetime.datetime.now())
        + " : The database is ready with version "
        + config["dcr_version"]
        + "."
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)

    return engine
