"""Database Definition Management.

Data definition related processing routines.

Returns:
    [type]: None.
"""
import logging.config
import os
import sqlite3
from sqlite3 import Error
from typing import Dict

import sqlalchemy
import sqlalchemy.orm
from libs import cfg
from libs import utils
from libs.cfg import config
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update


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

    current_version = select_version_version_unique(logger)

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
        + str(cfg.config[cfg.DCR_CFG_DATABASE_FILE])
        + " is "
        + current_version,
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Connect to the database.
# -----------------------------------------------------------------------------
def connect_db(logger: logging.Logger) -> None:
    """Connect to the database.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    if not os.path.isfile(config[cfg.DCR_CFG_DATABASE_FILE]):
        utils.terminate_fatal(
            logger,
            "Database file "
            + config[cfg.DCR_CFG_DATABASE_FILE]
            + " is missing",
        )

    connect_db_core(logger)

    utils.progress_msg(
        logger,
        "The database "
        + cfg.config[cfg.DCR_CFG_DATABASE_FILE]
        + " is connected",
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Connect to the database - core functionality.
# -----------------------------------------------------------------------------
def connect_db_core(logger: logging.Logger) -> None:
    """Connect to the database - core functionality.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    try:
        cfg.metadata = MetaData()
    except Error as err:
        utils.terminate_fatal(
            logger,
            "SQLAlchemy metadata not accessible - error=" + str(err),
        )
    try:
        cfg.engine = sqlalchemy.create_engine(cfg.config[cfg.DCR_CFG_DATABASE])
    except Error as err:
        utils.terminate_fatal(
            logger,
            "SQLAlchemy engine not accessible - error=" + str(err),
        )
    try:
        cfg.metadata.bind = cfg.engine
    except Error as err:
        utils.terminate_fatal(
            logger,
            "SQLAlchemy metadata not connectable with engine - error="
            + str(err),
        )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database tables.
# -----------------------------------------------------------------------------
def create_db_tables(logger: logging.Logger) -> None:
    """Create the database tables.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    if os.path.isfile(config[cfg.DCR_CFG_DATABASE_FILE]):
        utils.terminate_fatal(
            logger,
            "Database file "
            + config[cfg.DCR_CFG_DATABASE_FILE]
            + " is already existing",
        )

    connect_db_core(logger)

    create_dbt_document()
    create_dbt_run()
    create_dbt_version()
    # FK: document
    # FK: run
    create_dbt_journal()

    try:
        cfg.metadata.create_all(cfg.engine)
    except Error as err:
        utils.terminate_fatal(
            logger,
            "SQLAlchemy 'metadata.create_all(engine)' issue - error="
            + str(err),
        )

    insert_dbt_row(
        logger,
        cfg.DBT_VERSION,
        [{cfg.DBC_VERSION: cfg.config[cfg.DCR_CFG_DCR_VERSION]}],
    )

    disconnect_db(logger)

    utils.progress_msg(
        logger,
        "The database "
        + str(cfg.config[cfg.DCR_CFG_DATABASE_FILE])
        + " has been successfully created, version number="
        + cfg.config[cfg.DCR_CFG_DCR_VERSION],
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the trigger for the database column created_at.
# -----------------------------------------------------------------------------
def create_db_trigger_created_at(
    logger: logging.Logger, conn: sqlite3.Connection, table_name: str
) -> None:
    """Create the trigger for the database column created_at.

    Args:
        logger (logging.Logger): Current logger.
        conn (sqlite3.Connection): Database connection.
        table_name (str): Table name.
    """
    logger.debug(cfg.LOGGER_START)

    sql = """
CREATE TRIGGER IF NOT EXISTS trigger_created_at_xxx AFTER INSERT
ON xxx FOR EACH ROW
    BEGIN
        UPDATE xxx
           SET created_at = strftime('%Y-%m-%d %H:%M:%f', DATETIME('now'))
         WHERE id = NEW.id;
    END   """.replace(
        "xxx", table_name
    )

    try:
        conn.execute(sql)
    except Error as err:
        utils.terminate_fatal(
            logger,
            "Database table "
            + table_name
            + " - create trigger - error="
            + str(err),
        )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the trigger for the database column modified_at.
# -----------------------------------------------------------------------------
def create_db_trigger_modified_at(
    logger: logging.Logger, conn: sqlite3.Connection, table_name: str
) -> None:
    """Create the trigger for the database column modified_at.

    Args:
        logger (logging.Logger): Current logger.
        conn (sqlite3.Connection): Database connection.
        table_name (str): Table name.
    """
    logger.debug(cfg.LOGGER_START)

    sql = """
CREATE TRIGGER IF NOT EXISTS trigger_modified_at_xxx AFTER UPDATE
ON xxx FOR EACH ROW
    BEGIN
        UPDATE xxx
           SET modified_at = strftime('%Y-%m-%d %H:%M:%f', DATETIME('now'))
         WHERE id = NEW.id;
    END   """.replace(
        "xxx", table_name
    )

    try:
        conn.execute(sql)
    except Error as err:
        utils.terminate_fatal(
            logger,
            "Database table "
            + table_name
            + " - create trigger - error="
            + str(err),
        )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the triggers for the database tables.
# -----------------------------------------------------------------------------
def create_db_triggers(logger: logging.Logger) -> None:
    """Create the triggers for the database tables.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    if not os.path.isfile(config[cfg.DCR_CFG_DATABASE_FILE]):
        utils.terminate_fatal(
            logger,
            "Database file "
            + config[cfg.DCR_CFG_DATABASE_FILE]
            + " is missing",
        )

    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(config[cfg.DCR_CFG_DATABASE_FILE])
    except Error as err:
        utils.terminate_fatal(
            logger,
            "Database "
            + cfg.DCR_CFG_DATABASE
            + " - open connection - error="
            + str(err),
        )

    sql = """
    SELECT name
      FROM sqlite_schema
     WHERE type = "table"
     ORDER By name
          """

    for row in conn.cursor().execute(sql):
        create_db_trigger_created_at(logger, conn, row[0])
        if row[0] != "journal":
            create_db_trigger_modified_at(logger, conn, row[0])

    try:
        conn.close()
    except Error as err:
        utils.terminate_fatal(
            logger,
            "Database "
            + cfg.DCR_CFG_DATABASE
            + " - close connection - error="
            + str(err),
        )

    utils.progress_msg(
        logger,
        "The database triggers have been successfully created",
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table document.
# -----------------------------------------------------------------------------
def create_dbt_document(table_name: str = cfg.DBT_DOCUMENT) -> None:
    """Create the database table document.

    Args:
        table_name (str): Table name.
    """
    sqlalchemy.Table(
        table_name,
        cfg.metadata,
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
        ),
        sqlalchemy.Column(
            cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
            # onupdate=func.current_timestamp(),
        ),
        sqlalchemy.Column(
            cfg.DBC_STATUS, sqlalchemy.String, nullable=False, unique=True
        ),
    )


# -----------------------------------------------------------------------------
# Create the database table journal.
# -----------------------------------------------------------------------------
def create_dbt_journal(table_name: str = cfg.DBT_JOURNAL) -> None:
    """Create the database table journal.

    Args:
        table_name (str): Table name.
    """
    sqlalchemy.Table(
        table_name,
        cfg.metadata,
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
# Create the database table run.
# -----------------------------------------------------------------------------
def create_dbt_run(table_name: str = cfg.DBT_RUN) -> None:
    """Create the database table run.

    Args:
        table_name (str): Table name.
    """
    sqlalchemy.Table(
        table_name,
        cfg.metadata,
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
        ),
        sqlalchemy.Column(
            cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
            # onupdate=func.current_timestamp(),
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
        sqlalchemy.Column(cfg.DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            cfg.DBC_TOTAL_ACCEPTED,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(
            cfg.DBC_TOTAL_NEW,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(
            cfg.DBC_TOTAL_REJECTED,
            sqlalchemy.Integer,
            nullable=True,
        ),
    )


# -----------------------------------------------------------------------------
# Create the table run entry.
# -----------------------------------------------------------------------------
def create_dbt_run_row(logger: logging.Logger) -> None:
    """Create the table run entry.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of DCR is
    inserted.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    insert_dbt_row(
        logger, cfg.DBT_RUN, [{cfg.DBC_STATUS: cfg.DBC_STATUS_START}]
    )

    cfg.run_id = select_dbt_id_last(logger, cfg.DBT_RUN)

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create and initialise the database table version.
# -----------------------------------------------------------------------------
def create_dbt_version(
    table_name: str = cfg.DBT_VERSION,
) -> sqlalchemy.Table:
    """Create and initialise the database table version.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of DCR is
    inserted.

    Args:
        table_name (str): Table name.
    Returns:
        sqlalchemy.Table: Schema of database table `version`.
    """
    dbt = sqlalchemy.Table(
        table_name,
        cfg.metadata,
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
        ),
        sqlalchemy.Column(
            cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
            # onupdate=func.current_timestamp(),
        ),
        sqlalchemy.Column(
            cfg.DBC_VERSION, sqlalchemy.String, nullable=False, unique=True
        ),
    )

    return dbt


# -----------------------------------------------------------------------------
# Disconnect the database.
# -----------------------------------------------------------------------------
def disconnect_db(logger: logging.Logger) -> None:
    """Disconnect the database.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    try:
        cfg.metadata.clear()
    except Error as err:
        utils.terminate_fatal(
            logger,
            "SQLAlchemy metadata could not be cleared - error=" + str(err),
        )

    try:
        cfg.engine.dispose()
    except Error as err:
        utils.terminate_fatal(
            logger,
            "SQLAlchemy engine could not be disposed - error=" + str(err),
        )

    utils.progress_msg(
        logger,
        "The database "
        + cfg.config[cfg.DCR_CFG_DATABASE_FILE]
        + " is disconnected",
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_dbt_row(
    logger: logging.Logger, table_name: str, columns: cfg.Columns
) -> None:
    """Insert a new row into a database table.

    Args:
        logger (logging.Logger): Current logger.
        table_name (str): Table name.
        columns (Columns): Pairs of column name and value.
    """
    logger.debug(cfg.LOGGER_START)

    dbt = Table(table_name, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(insert(dbt).values(columns))

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Get the last id from a database table.
# -----------------------------------------------------------------------------
def select_dbt_id_last(
    logger: logging.Logger, table_name: str
) -> sqlalchemy.Integer:
    """Get the last id from a database table.

    Get the version number from the database table `version`.

    Args:
        logger (logging.Logger): Current logger.
        table_name (str): Database table name.

    Returns:
        sqlalchemy.Integer: The last id found.
    """
    logger.debug(cfg.LOGGER_START)

    dbt = Table(table_name, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect() as conn:
        result = conn.execute(select(func.max(dbt.c.id)))
        row = result.fetchone()

    logger.debug(cfg.LOGGER_END)

    return row[0]


# -----------------------------------------------------------------------------
# Get the version number from the database table version.
# -----------------------------------------------------------------------------
def select_version_version_unique(logger: logging.Logger) -> str:
    """Get the version number.

    Get the version number from the database table `version`.

    Args:
        logger (logging.Logger): Current logger.

    Returns:
        str: The version number found.
    """
    logger.debug(cfg.LOGGER_START)

    dbt = Table(cfg.DBT_VERSION, cfg.metadata, autoload_with=cfg.engine)

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
# Update a database row based on its id column.
# -----------------------------------------------------------------------------
def update_dbt_id(
    logger: logging.Logger,
    table_name: str,
    id_where: sqlalchemy.Integer,
    columns: Dict[str, str],
) -> None:
    """Update a database row based on its id column.

    Args:
        logger (logging.Logger): Current logger.
        table_name (str): Table name.
        id_where (sqlalchemy.Integer): Content of column id.
        columns (Columns): Pairs of column name and value.
    """
    logger.debug(cfg.LOGGER_START)

    dbt = Table(table_name, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(update(dbt).where(dbt.c.id == id_where).values(columns))

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Upgrade the current database schema..
# -----------------------------------------------------------------------------
def upgrade_db(logger: logging.Logger) -> None:
    """Upgrade the current database schema.

    Check if the current database schema needs to be upgraded and perform the
    necessary steps.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    # TBD: Database upgrade

    logger.debug(cfg.LOGGER_END)
