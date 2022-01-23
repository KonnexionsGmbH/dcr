"""
### Module: **Database Definition Management**.

Data definition related processing routines.
"""

import datetime
import logging
import logging.config
import sys
from os import PathLike
from typing import Union

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import ForeignKey
from sqlalchemy.engine import Engine

from db.dml import get_version_number
from db.dml import insert_current_version_number
from utils.constant import DBC_ACTION
from utils.constant import DBC_CREATED_AT
from utils.constant import DBC_DOCUMENT_ID
from utils.constant import DBC_FUNCTION
from utils.constant import DBC_ID
from utils.constant import DBC_MODIFIED_AT
from utils.constant import DBC_MODULE
from utils.constant import DBC_PACKAGE
from utils.constant import DBC_STATUS
from utils.constant import DBC_VERSION
from utils.constant import DBT_DOCUMENT
from utils.constant import DBT_JOURNAL
from utils.constant import DBT_VERSION
from utils.constant import DCR_CFG_DCR_VERSION
from utils.constant import LOGGER_END
from utils.constant import LOGGER_PROGRESS_UPDATE
from utils.constant import LOGGER_START
from utils.db import get_engine
from utils.db import get_metadata


# -----------------------------------------------------------------------------
# Check the existence of the database schema.
# -----------------------------------------------------------------------------


def check_database_version(
    logger: logging.Logger,
    config: dict[str, Union[Engine, PathLike[str], str]],
) -> None:
    """
    #### Function: **Check the existence of the database schema**.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    - **config (dict[str, Union[Engine, PathLike[str], str]])**:
                                   Configuration parameters.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    if config[DCR_CFG_DCR_VERSION] != get_version_number(logger, config):
        logger.error(
            "fatal error: program abort =====> "
            + "database version is "
            + get_version_number(logger, config)
            + " - expected version is "
            + config[DCR_CFG_DCR_VERSION]
            + " <====="
        )
        sys.exit(1)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Check if the current database schema needs an upgrade..
# -----------------------------------------------------------------------------


def check_database_upgrade(
    logger: logging.Logger,
    _config: dict[str, Union[Engine, PathLike[str], str]],
) -> None:
    """
    #### Function: **Check if the current database schema needs an upgrade**.

    **Args**:
    - **logger (logging.Logger)**:                 Current logger.
    - **_config (dict[str, Union[Engine, PathLike[str], str]])**:
                                                   Configuration parameters.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    # TBD: Database upgrade

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database schema.
# -----------------------------------------------------------------------------


def create_database(
    logger: logging.Logger,
    config: dict[str, Union[Engine, PathLike[str], str]],
) -> None:
    """
    #### Function: **Create the database schema**.

    **Args**:
    - **logger (logging.Logger)**:                Current logger.
    - **config (dict[str, Union[Engine, PathLike[str], str]])**:
                                                  Configuration parameters.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    metadata = get_metadata(config)

    create_table_version(metadata)

    create_table_document(metadata)

    create_table_journal(metadata)

    # Implement the database schema
    metadata.create_all(get_engine(config))

    insert_current_version_number(logger, config)

    print(
        LOGGER_PROGRESS_UPDATE
        + str(datetime.datetime.now())
        + " : The database has been created."
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Create or upgrade the database.
# -----------------------------------------------------------------------------


def create_or_upgrade_database(
    logger: logging.Logger,
    config: dict[str, Union[Engine, PathLike[str], str]],
) -> None:
    """
    #### Function: **Create or upgrade the database**.

    **Args**:
    - **logger (logging.Logger)**:                Current logger.
    - **config (dict[str, Union[Engine, PathLike[str], str]])**:
                                                  Configuration parameters.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    is_new: bool = False
    is_upgrade: bool = False

    if not sqlalchemy.inspect(get_engine(config)).has_table(DBT_VERSION):
        create_database(logger, config)
        is_new = True

    # TBD
    # if not is_new:
    #     is_upgrade = check_database_upgrade(logger, config)

    if not (is_new or is_upgrade):
        print(
            LOGGER_PROGRESS_UPDATE
            + str(datetime.datetime.now())
            + " : The database is already up to date."
        )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise the database table document.
# -----------------------------------------------------------------------------


def create_table_document(
    metadata: sqlalchemy.schema.MetaData,
) -> None:
    """
    #### Function: **Initialise the database table `document`**.

    If the database table is not yet included in the database schema, then the
    database table is created.

    **Args**:
    - **metadata (sqlalchemy.schema.MetaData)**: Database schema.
    """
    table_name = DBT_DOCUMENT

    sqlalchemy.Table(
        table_name,
        metadata,
        sqlalchemy.Column(
            DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            DBC_CREATED_AT, sqlalchemy.DateTime, default=datetime.datetime.now
        ),
        sqlalchemy.Column(
            DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
            onupdate=datetime.datetime.now,
        ),
        sqlalchemy.Column(
            DBC_STATUS, sqlalchemy.String, nullable=False, unique=True
        ),
    )


# -----------------------------------------------------------------------------
# Initialise the database table journal.
# -----------------------------------------------------------------------------


def create_table_journal(
    metadata: sqlalchemy.schema.MetaData,
) -> None:
    """
    #### Function: **Initialise the database table `journal`**.

    If the database table is not yet included in the database schema, then the
    database table is created.

    **Args**:
    - **metadata (sqlalchemy.schema.MetaData)**: Database schema.
    """
    table_name = DBT_JOURNAL

    sqlalchemy.Table(
        table_name,
        metadata,
        sqlalchemy.Column(
            DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            DBC_CREATED_AT, sqlalchemy.DateTime, default=datetime.datetime.now
        ),
        sqlalchemy.Column(DBC_ACTION, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            ForeignKey(DBT_DOCUMENT + "." + DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(DBC_FUNCTION, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_MODULE, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_PACKAGE, sqlalchemy.String, nullable=False),
    )


# -----------------------------------------------------------------------------
# Initialise the database table version.
# -----------------------------------------------------------------------------


def create_table_version(
    metadata: sqlalchemy.schema.MetaData,
) -> sqlalchemy.Table:
    """
    #### Function: **Initialise the database table `version`**.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of dcr is
    inserted.

    **Args**:
    - **metadata (sqlalchemy.schema.MetaData)**: Database schema.

    Return:
    - **sqlalchemy.Table**: Schema of database table `version`.
    """
    table_name = DBT_VERSION

    return sqlalchemy.Table(
        table_name,
        metadata,
        sqlalchemy.Column(
            DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            DBC_CREATED_AT, sqlalchemy.DateTime, default=datetime.datetime.now
        ),
        sqlalchemy.Column(
            DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
            onupdate=datetime.datetime.now,
        ),
        sqlalchemy.Column(
            DBC_VERSION, sqlalchemy.String, nullable=False, unique=True
        ),
    )
