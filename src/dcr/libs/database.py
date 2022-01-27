"""
### Module: **Database Definition Management**.

Data definition related processing routines.
"""

import datetime
import logging
import logging.config
from os import PathLike
from typing import Dict
from typing import TypeAlias
from typing import Union

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import ForeignKey
from sqlalchemy import insert
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy.engine import Engine

from libs.globals import CONFIG
from libs.globals import DCR_CFG_DATABASE_FILE
from libs.globals import DCR_CFG_DATABASE_URL
from libs.globals import DCR_CFG_DCR_VERSION
from libs.globals import LOGGER_END
from libs.globals import LOGGER_PROGRESS_UPDATE
from libs.globals import LOGGER_START
from libs.utils import terminate_fatal

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
Columns: TypeAlias = list[Dict[str, Union[PathLike[str], str]]]

DB_ENGINE: str = "engine"
DB_METADATA: str = "metadata"
DB_REFLECT: str = "reflect"

DBC_ACTION: str = "action"
DBC_CREATED_AT: str = "created_at"
DBC_DOCUMENT_ID: str = "document_id"
DBC_FUNCTION: str = "function"
DBC_ID: str = "id"
DBC_MODIFIED_AT: str = "modified_at"
DBC_MODULE: str = "module"
DBC_PACKAGE: str = "package"
DBC_STATUS: str = "status"
DBC_VERSION: str = "version"

DBT_DOCUMENT: str = "document"
DBT_JOURNAL: str = "journal"
DBT_VERSION: str = "version"

# ENGINE: Engine = sqlalchemy.create_engine(CONFIG[DCR_CFG_DATABASE_URL])
ENGINE: Engine = sqlalchemy.create_engine("sqlite:///data/dcr.db")

METADATA: MetaData = MetaData()


# -----------------------------------------------------------------------------
# Check the existence of the database schema.
# -----------------------------------------------------------------------------
def check_database_version(logger: logging.Logger) -> None:
    """
    #### Function: **Check the existence of the database schema**.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    current_version = select_version_unique(logger)

    if CONFIG[DCR_CFG_DCR_VERSION] != current_version:
        terminate_fatal(
            logger,
            "Current database version is "
            + current_version
            + " - but expected version is "
            + str(CONFIG[DCR_CFG_DCR_VERSION]),
        )

    print(
        LOGGER_PROGRESS_UPDATE,
        str(datetime.datetime.now()),
        " : The current version of database "
        + str(CONFIG[DCR_CFG_DATABASE_URL])
        + str(CONFIG[DCR_CFG_DATABASE_FILE])
        + " is ",
        current_version,
        ".",
        sep="",
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database schema.
# -----------------------------------------------------------------------------
def create_database(logger: logging.Logger) -> None:
    """
    #### Function: **Create the database schema**.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    create_table_version()

    create_table_document()

    create_table_journal()

    # Implement the database schema
    METADATA.create_all(ENGINE)

    insert_table(
        logger, DBT_VERSION, [{DBC_VERSION: CONFIG[DCR_CFG_DCR_VERSION]}]
    )

    print(
        LOGGER_PROGRESS_UPDATE,
        str(datetime.datetime.now()),
        " : The database "
        + str(CONFIG[DCR_CFG_DATABASE_URL])
        + str(CONFIG[DCR_CFG_DATABASE_FILE])
        + " has been successfully created.",
        sep="",
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Create or upgrade the database.
# -----------------------------------------------------------------------------
def create_or_upgrade_database(logger: logging.Logger) -> None:
    """
    #### Function: **Create or upgrade the database**.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    is_new: bool = False
    is_upgrade: bool = False

    if not sqlalchemy.inspect(ENGINE).has_table(DBT_VERSION):
        create_database(logger)
        is_new = True

    # TBD
    # if not is_new:
    #     is_upgrade = check_database_upgrade(LOGGER, config)

    if not (is_new or is_upgrade):
        print(
            LOGGER_PROGRESS_UPDATE,
            str(datetime.datetime.now()),
            " : The database "
            + str(CONFIG[DCR_CFG_DATABASE_URL])
            + str(CONFIG[DCR_CFG_DATABASE_FILE])
            + " is already up to date.",
            sep="",
        )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise the database table document.
# -----------------------------------------------------------------------------
def create_table_document() -> None:
    """
    #### Function: **Initialise the database table `document`**.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    """
    sqlalchemy.Table(
        DBT_DOCUMENT,
        METADATA,
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
def create_table_journal() -> None:
    """#### Function: **Initialise the database table `journal`**."""
    sqlalchemy.Table(
        DBT_JOURNAL,
        METADATA,
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
def create_table_version() -> sqlalchemy.Table:
    """
    #### Function: **Initialise the database table `version`**.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of DCR is
    inserted.

    **Returns**:
    - **sqlalchemy.Table**: Schema of database table `version`.
    """
    return sqlalchemy.Table(
        DBT_VERSION,
        METADATA,
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


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_table(logger: logging.Logger, table: str, columns: Columns) -> None:
    """
    #### Function: **Insert a new row into a database table**.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    - **table (str)**:       Table name.
    - **columns (Columns)**: Column name and value pairs.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    dbt = Table(table, METADATA, autoload_with=ENGINE)

    with ENGINE.connect() as conn:
        conn.execute(insert(dbt).values(columns))

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Get the version number from the database table version.
# -----------------------------------------------------------------------------
def select_version_unique(logger: logging.Logger) -> str:
    """
    #### Function: **Get the version number**.

    Get the version number from the database table `version`.

    **Args**:
    - **logger (logging.Logger)**: Current logger.

    **Returns**:
    - **str**: The version number found.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    dbt = Table(DBT_VERSION, METADATA, autoload_with=ENGINE)

    current_version: str = ""

    with ENGINE.connect() as conn:
        for row in conn.execute(select(dbt.c.version)):
            if current_version == "":
                current_version = row.version
            else:
                terminate_fatal(
                    logger,
                    "Column version in database table version not unique",
                )

    if current_version == "":
        terminate_fatal(
            logger, "Column version in database table version not found"
        )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)

    return current_version


# -----------------------------------------------------------------------------
# Upgrade the current database schema..
# -----------------------------------------------------------------------------
def upgrade_database(logger: logging.Logger) -> None:
    """
    #### Function: **Upgrade the current database schema**.

    Check if the current database schema needs to be upgraded and perform the
    necessary steps.

    **Args**:
    - **logger (logging.Logger)**: Current logger.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    # TBD: Database upgrade

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)
