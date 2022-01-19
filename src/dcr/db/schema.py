"""Database Schema Management."""

import datetime
import logging
import logging.config

import sqlalchemy
import sqlalchemy.orm


# ----------------------------------------------------------------------------------
# Check the existence of the database schema.
# ----------------------------------------------------------------------------------


def check_schema_existence(logger, config, engine):
    """Check the existence of the database schema.

    Args:
        logger (Logger): Default logger.
        config (dict):   Configuration parameters.
        engine (Engine): Database state.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Start")

    if not sqlalchemy.inspect(engine).has_table("version"):
        create_schema(logger, config, engine)
    else:
        check_schema_upgrade(logger, config, engine)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("End")


# ----------------------------------------------------------------------------------
# Check if the current database schema needs to be upgraded...
# ----------------------------------------------------------------------------------


def check_schema_upgrade(logger, _config, _engine):
    """Check if the current database schema needs to be upgraded.

    Args:
        logger (Logger): Default logger.
        _config (dict):   Configuration parameters.
        _engine (Engine): Database state.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Start")

    # TBD: Database upgrade

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("End")


# ----------------------------------------------------------------------------------
# Create the database schema.
# ----------------------------------------------------------------------------------


def create_schema(logger, config, engine):
    """Create the database schema.

    Args:
        logger (Logger): Default logger.
        config (dict):   Configuration parameters.
        engine (Engine): Database state.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Start")

    metadata = sqlalchemy.MetaData(engine)

    version = create_table_version(metadata, "version")

    create_table_document(metadata, "document")

    # Implement the database schema
    metadata.create_all(engine)

    insert_version_number(logger, config, engine, version)

    print(
        "Progress update + datetime.now() + "
        + str(datetime.datetime.now())
        + " : The database schema has been created."
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("End")


# ----------------------------------------------------------------------------------
# Initialise the database table document.
# ----------------------------------------------------------------------------------


def create_table_document(metadata, table):
    """Initialise the database table document.

    If the database table is not yet included in the database schema, then the
    database table is created.

    Args:
        metadata (MetaData): Database schema.
        table    (str):      Database table name.

    """
    sqlalchemy.Table(
        table,
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


# ----------------------------------------------------------------------------------
# Initialise the database table version.
# ----------------------------------------------------------------------------------


def create_table_version(metadata, table):
    """Initialise the database table version.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of dcr is
    inserted.

    Args:
        metadata (MetaData): Database schema.
        table    (str):      Database table name.

    Return:
        sqlalchemy.Table: Schema of database table version.
    """
    return sqlalchemy.Table(
        table,
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


# ----------------------------------------------------------------------------------
# Initialise the database.
# ----------------------------------------------------------------------------------


def get_engine(logger, config):
    """Initialise the database.

    Args:
        logger (Logger): Default logger.
        config (dict):   Configuration parameters.

    Returns:
        Engine: Database state.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Start")

    engine = sqlalchemy.create_engine(config["database.url"])

    check_schema_existence(logger, config, engine)

    print(
        "Progress update + datetime.now() + "
        + str(datetime.datetime.now())
        + " : The database is ready with version"
        + config["dcr.version"]
        + "."
    )

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("End")

    return engine


# ----------------------------------------------------------------------------------
# Inserts the current version number in the version table.
# ----------------------------------------------------------------------------------


def insert_version_number(logger, config, engine, version):
    """Initialise the database table version.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of dcr is
    inserted.

    Args:
        logger  (Logger):           Default logger.
        config  (dict):             Configuration parameters.
        engine  (Engine):           Database state.
        version (sqlalchemy.Table): Schema of database table version.
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Start")

    with sqlalchemy.orm.Session(engine) as session:
        session.add(version(version=config["dcr.version"]))
        session.commit()

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("End")
