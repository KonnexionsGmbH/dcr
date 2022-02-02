"""Database Definition Management.

Data definition related processing routines.

Returns:
    [type]: None.
"""

import datetime
import logging.config

import sqlalchemy
import sqlalchemy.orm
from libs import cfg
from libs import utils
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import insert
from sqlalchemy import select


# -----------------------------------------------------------------------------
# Check that the database version is up to date.
# -----------------------------------------------------------------------------
def check_db_up_to_date(logger: logging.Logger) -> None:
    """Check that the database version is up to date.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    if not sqlalchemy.inspect(cfg.engine).has_table(cfg.DBT_VERSION):
        utils.terminate_fatal(
            logger,
            "The database "
            + cfg.config[cfg.DCR_CFG_DATABASE_FILE]
            + " does not yet exist.",
        )

    current_version = select_version_unique(logger)

    if cfg.config[cfg.DCR_CFG_DCR_VERSION] != current_version:
        utils.terminate_fatal(
            logger,
            "Current database version is "
            + current_version
            + " - but expected version is "
            + str(cfg.config[cfg.DCR_CFG_DCR_VERSION]),
        )

    utils.progress_msg(
        logger,
        "The current version of database "
        + str(cfg.config[cfg.DCR_CFG_DATABASE_URL])
        + str(cfg.config[cfg.DCR_CFG_DATABASE_FILE])
        + " is "
        + current_version,
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database schema.
# -----------------------------------------------------------------------------
def create_database(logger: logging.Logger) -> None:
    """Create the database schema.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    create_table_version()

    create_table_document()

    create_table_journal()

    create_table_run()

    # Implement the database schema
    cfg.meta_data.create_all(cfg.engine)

    insert_table(
        logger,
        cfg.DBT_VERSION,
        [{cfg.DBC_VERSION: cfg.config[cfg.DCR_CFG_DCR_VERSION]}],
    )

    utils.progress_msg(
        logger,
        "The database "
        + str(cfg.config[cfg.DCR_CFG_DATABASE_URL])
        + str(cfg.config[cfg.DCR_CFG_DATABASE_FILE])
        + " has been successfully created",
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create or upgrade the database.
# -----------------------------------------------------------------------------
def create_or_upgrade_database(logger: logging.Logger) -> None:
    """Create or upgrade the database.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    is_new: bool = False
    is_upgrade: bool = False

    if not sqlalchemy.inspect(cfg.engine).has_table(cfg.DBT_VERSION):
        create_database(logger)
        is_new = True

    # TBD
    # if not is_new:
    #     is_upgrade = check_database_upgrade(cfg.LOGGER, config)

    if not (is_new or is_upgrade):
        utils.progress_msg(
            logger,
            "The database "
            + str(cfg.config[cfg.DCR_CFG_DATABASE_URL])
            + str(cfg.config[cfg.DCR_CFG_DATABASE_FILE])
            + " is already up to date",
        )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise the database table document.
# -----------------------------------------------------------------------------
def create_table_document() -> None:
    """Initialise the database table document."""
    sqlalchemy.Table(
        cfg.DBT_DOCUMENT,
        cfg.meta_data,
        sqlalchemy.Column(
            cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
            default=datetime.datetime.now,
        ),
        sqlalchemy.Column(
            cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
            onupdate=datetime.datetime.now,
        ),
        sqlalchemy.Column(
            cfg.DBC_STATUS, sqlalchemy.String, nullable=False, unique=True
        ),
    )


# -----------------------------------------------------------------------------
# Initialise the database table journal.
# -----------------------------------------------------------------------------
def create_table_journal() -> None:
    """Initialise the database table journal."""
    sqlalchemy.Table(
        cfg.DBT_JOURNAL,
        cfg.meta_data,
        sqlalchemy.Column(
            cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
            default=datetime.datetime.now,
        ),
        sqlalchemy.Column(cfg.DBC_ACTION, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            cfg.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            ForeignKey(
                cfg.DBT_DOCUMENT + "." + cfg.DBC_ID, ondelete="CASCADE"
            ),
            nullable=False,
        ),
        sqlalchemy.Column(cfg.DBC_FUNCTION, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(cfg.DBC_MODULE, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(cfg.DBC_PACKAGE, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            cfg.DBC_RUN_ID,
            sqlalchemy.Integer,
            ForeignKey(cfg.DBT_RUN + "." + cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
    )


# -----------------------------------------------------------------------------
# Initialise the database table run.
# -----------------------------------------------------------------------------
def create_table_run() -> None:
    """Initialise the database table run."""
    sqlalchemy.Table(
        cfg.DBT_RUN,
        cfg.meta_data,
        sqlalchemy.Column(
            cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
            default=datetime.datetime.now,
        ),
        sqlalchemy.Column(
            cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
            onupdate=datetime.datetime.now,
        ),
        sqlalchemy.Column(
            cfg.DBC_INBOX_ABS_NAME, sqlalchemy.String, nullable=True
        ),
        sqlalchemy.Column(
            cfg.DBC_INBOX_CONFIG, sqlalchemy.String, nullable=True
        ),
        sqlalchemy.Column(
            cfg.DBC_INBOX_ACCEPTED_ABS_NAME, sqlalchemy.String, nullable=True
        ),
        sqlalchemy.Column(
            cfg.DBC_INBOX_ACCEPTED_CONFIG, sqlalchemy.String, nullable=True
        ),
        sqlalchemy.Column(
            cfg.DBC_INBOX_REJECTED_ABS_NAME, sqlalchemy.String, nullable=True
        ),
        sqlalchemy.Column(
            cfg.DBC_INBOX_REJECTED_CONFIG, sqlalchemy.String, nullable=True
        ),
    )


# -----------------------------------------------------------------------------
# Create the table run entry.
# -----------------------------------------------------------------------------
def create_table_run_entry(logger: logging.Logger) -> None:
    """Create the table run entry.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of DCR is
    inserted.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    insert_table(logger, cfg.DBT_RUN, [])

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Initialise the database table version.
# -----------------------------------------------------------------------------
def create_table_version() -> sqlalchemy.Table:
    """Initialise the database table version.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of DCR is
    inserted.

    Returns:
        sqlalchemy.Table: Schema of database table `version`.
    """
    return sqlalchemy.Table(
        cfg.DBT_VERSION,
        cfg.meta_data,
        sqlalchemy.Column(
            cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
            default=datetime.datetime.now,
        ),
        sqlalchemy.Column(
            cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
            onupdate=datetime.datetime.now,
        ),
        sqlalchemy.Column(
            cfg.DBC_VERSION, sqlalchemy.String, nullable=False, unique=True
        ),
    )


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_table(
    logger: logging.Logger, table: str, columns: cfg.Columns
) -> sqlalchemy.Integer:
    """Insert a new row into a database table.

    Args:
        logger (logging.Logger): Current logger.
        table (str): Table name.
        columns (Columns): Pairs of column name and value.

    Returns:
        sqlalchemy.Integer: The primary key of the new row.
    """
    logger.debug(cfg.LOGGER_START)

    dbt = Table(table, cfg.meta_data, autoload_with=cfg.engine)

    with cfg.engine.connect() as conn:
        result = conn.execute(insert(dbt).values(columns))
        row = result.fetchone()

    logger.debug(cfg.LOGGER_END)

    return row.id


# -----------------------------------------------------------------------------
# Get the version number from the database table version.
# -----------------------------------------------------------------------------
def select_version_unique(logger: logging.Logger) -> str:
    """Get the version number.

    Get the version number from the database table `version`.

    Args:
        logger (logging.Logger): Current logger.

    Returns:
        str: The version number found.
    """
    logger.debug(cfg.LOGGER_START)

    dbt = Table(cfg.DBT_VERSION, cfg.meta_data, autoload_with=cfg.engine)

    current_version: str = ""

    with cfg.engine.connect() as conn:
        for row in conn.execute(select(dbt.c.version)):
            if current_version == "":
                current_version = row.version
            else:
                utils.terminate_fatal(
                    logger,
                    "Column version in database table version not unique",
                )

    if current_version == "":
        utils.terminate_fatal(
            logger, "Column version in database table version not found"
        )

    logger.debug(cfg.LOGGER_END)

    return current_version


# -----------------------------------------------------------------------------
# Upgrade the current database schema..
# -----------------------------------------------------------------------------
def upgrade_database(logger: logging.Logger) -> None:
    """Upgrade the current database schema.

    Check if the current database schema needs to be upgraded and perform the
    necessary steps.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    # TBD: Database upgrade

    logger.debug(cfg.LOGGER_END)
