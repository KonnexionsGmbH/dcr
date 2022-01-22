"""
### Database Definition Management.

Data definition related processing routines.
"""

import datetime
import logging
import logging.config

import sqlalchemy
import sqlalchemy.orm
from db.dml import insert_version_number
from sqlalchemy import ForeignKey
from utils.constant import LOGGER_END
from utils.constant import LOGGER_PROGRESS_UPDATE
from utils.constant import LOGGER_START


# -----------------------------------------------------------------------------
# Check the existence of the database schema.
# -----------------------------------------------------------------------------


def check_schema_existence(
    logger: logging.Logger,
    config: dict[str, str],
    engine: sqlalchemy.engine.base.Engine,
) -> None:
    """
    **Check the existence of the database schema**.

    **Args**:
    - **logger (logging.Logger)**:                Current logger.
    - **config (dict[str, str])**:                Configuration parameters.
    - **engine (sqlalchemy.engine.base.Engine)**: Database state.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    if not sqlalchemy.inspect(engine).has_table("version"):
        create_schema(logger, config, engine)
    else:
        check_schema_upgrade(logger, config, engine)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Check if the current database schema needs to be upgraded...
# -----------------------------------------------------------------------------


def check_schema_upgrade(
    logger: logging.Logger,
    _config: dict[str, str],
    _engine: sqlalchemy.engine.base.Engine,
) -> None:
    """
    **Check if the current database schema needs to be upgraded**.

    **Args**:
    - **logger (logging.Logger)**:                 Current logger.
    - **_config (dict[str, str])**:                Configuration parameters.
    - **_engine (sqlalchemy.engine.base.Engine)**: Database state.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    # TBD: Database upgrade

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database schema.
# -----------------------------------------------------------------------------


def create_schema(
    logger: logging.Logger,
    config: dict[str, str],
    engine: sqlalchemy.engine.base.Engine,
) -> None:
    """
    **Create the database schema**.

    **Args**:
    - **logger (logging.Logger)**:                Current logger.
    - **config (dict[str, str])**:                Configuration parameters.
    - **engine (sqlalchemy.engine.base.Engine)**: Database state.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(LOGGER_START)

    metadata = sqlalchemy.MetaData(engine)

    version = create_table_version(metadata)

    create_table_document(metadata)

    create_table_journal(metadata)

    # Implement the database schema
    metadata.create_all(engine)

    insert_version_number(logger, config, engine, version)

    print(
        LOGGER_PROGRESS_UPDATE
        + str(datetime.datetime.now())
        + " : The database schema has been created."
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
    **Initialise the database table `document`**.

    If the database table is not yet included in the database schema, then the
    database table is created.

    **Args**:
    - **metadata (sqlalchemy.schema.MetaData)**: Database schema.
    """
    table_name = "document"

    sqlalchemy.Table(
        table_name,
        metadata,
        sqlalchemy.Column(
            "id",
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            "created_at", sqlalchemy.DateTime, default=datetime.datetime.now
        ),
        sqlalchemy.Column(
            "modified_at", sqlalchemy.DateTime, onupdate=datetime.datetime.now
        ),
        sqlalchemy.Column(
            "status", sqlalchemy.String, nullable=False, unique=True
        ),
    )


# -----------------------------------------------------------------------------
# Initialise the database table journal.
# -----------------------------------------------------------------------------


def create_table_journal(
    metadata: sqlalchemy.schema.MetaData,
) -> None:
    """
    **Initialise the database table `journal`**.

    If the database table is not yet included in the database schema, then the
    database table is created.

    **Args**:
    - **metadata (sqlalchemy.schema.MetaData)**: Database schema.
    """
    table_name = "journal"

    sqlalchemy.Table(
        table_name,
        metadata,
        sqlalchemy.Column(
            "id",
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            "created_at", sqlalchemy.DateTime, default=datetime.datetime.now
        ),
        sqlalchemy.Column("action", sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            "document_id",
            sqlalchemy.Integer,
            ForeignKey("document.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column("function", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("module", sqlalchemy.String, nullable=False),
        sqlalchemy.Column("package", sqlalchemy.String, nullable=False),
    )


# -----------------------------------------------------------------------------
# Initialise the database table version.
# -----------------------------------------------------------------------------


def create_table_version(
    metadata: sqlalchemy.schema.MetaData,
) -> sqlalchemy.Table:
    """
    **Initialise the database table `version`**.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of dcr is
    inserted.

    **Args**:
    - **metadata (sqlalchemy.schema.MetaData)**: Database schema.

    Return:
    - **sqlalchemy.Table**: Schema of database table `version`.
    """
    table_name = "version"

    return sqlalchemy.Table(
        table_name,
        metadata,
        sqlalchemy.Column(
            "id",
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            "created_at", sqlalchemy.DateTime, default=datetime.datetime.now
        ),
        sqlalchemy.Column(
            "modified_at", sqlalchemy.DateTime, onupdate=datetime.datetime.now
        ),
        sqlalchemy.Column(
            "version", sqlalchemy.String, nullable=False, unique=True
        ),
    )
