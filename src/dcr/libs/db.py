"""Database Definition Management.

Data definition related processing routines.

Returns:
    [type]: None.
"""
import logging.config
import os
import sqlite3
from pathlib import Path
from sqlite3 import Error
from typing import Dict

import sqlalchemy
import sqlalchemy.orm
from libs import cfg
from libs import utils
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint
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
            "The database " + get_db_file_name() + " does not yet exist.",
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
        + get_db_file_name()
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

    db_file_name = get_db_file_name()

    if not os.path.isfile(db_file_name):
        utils.terminate_fatal(
            logger,
            "Database file " + db_file_name + " is missing",
        )

    connect_db_core(logger)

    utils.progress_msg(
        logger,
        "The database " + db_file_name + " is connected",
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
        cfg.engine = sqlalchemy.create_engine(get_db_url())
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

    db_file_name = get_db_file_name()

    if os.path.isfile(db_file_name):
        utils.terminate_fatal(
            logger,
            "Database file " + db_file_name + " is already existing",
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

    disconnect_db(logger)

    utils.progress_msg(
        logger,
        "The database "
        + db_file_name
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

    db_file_name = get_db_file_name()

    if not os.path.isfile(db_file_name):
        utils.terminate_fatal(
            logger,
            "Database file " + db_file_name + " is missing",
        )

    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(db_file_name)
    except Error as err:
        utils.terminate_fatal(
            logger,
            "Database "
            + db_file_name
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
            + db_file_name
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
        ),
        sqlalchemy.Column(
            cfg.DBC_FILE_NAME, sqlalchemy.String, nullable=False
        ),
        sqlalchemy.Column(
            cfg.DBC_FILE_TYPE, sqlalchemy.String, nullable=False
        ),
        sqlalchemy.Column(cfg.DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            cfg.DBC_STEM_NAME, sqlalchemy.String, nullable=False
        ),
    )


# -----------------------------------------------------------------------------
# Create the table document entry.
# -----------------------------------------------------------------------------
def create_dbt_document_row(logger: logging.Logger) -> None:
    """Create the table document entry.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    insert_dbt_row(
        logger,
        cfg.DBT_DOCUMENT,
        [
            {
                cfg.DBC_FILE_NAME: cfg.CURRENT_FILE_NAME,
                cfg.DBC_FILE_TYPE: cfg.CURRENT_FILE_TYPE,
                cfg.DBC_STATUS: cfg.STATUS_START,
                cfg.DBC_STEM_NAME: cfg.CURRENT_STEM_NAME,
            },
        ],
    )

    cfg.document_id = select_dbt_id_last(logger, cfg.DBT_DOCUMENT)

    logger.debug(cfg.LOGGER_END)


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
        sqlalchemy.Column(
            cfg.DBC_ACTION_CODE, sqlalchemy.String, nullable=False
        ),
        sqlalchemy.Column(
            cfg.DBC_ACTION_TEXT, sqlalchemy.String, nullable=False
        ),
        sqlalchemy.Column(
            cfg.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            ForeignKey(
                cfg.DBT_DOCUMENT + "." + cfg.DBC_ID, ondelete="CASCADE"
            ),
            nullable=False,
        ),
        sqlalchemy.Column(
            cfg.DBC_FUNCTION_NAME, sqlalchemy.String, nullable=False
        ),
        sqlalchemy.Column(
            cfg.DBC_MODULE_NAME, sqlalchemy.String, nullable=False
        ),
        sqlalchemy.Column(
            cfg.DBC_RUN_ID,
            sqlalchemy.Integer,
            ForeignKey(cfg.DBT_RUN + "." + cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        UniqueConstraint(
            cfg.DBC_DOCUMENT_ID, cfg.DBC_ACTION_CODE, name="unique_key_1"
        ),
    )


# -----------------------------------------------------------------------------
# Create the table journal entry.
# -----------------------------------------------------------------------------
def create_dbt_journal_row(
    logger: logging.Logger, action: str, module_name: str, function_name: str
) -> None:
    """Create the table journal entry.

    Args:
        logger (logging.Logger): Current logger.
        action (str): Current action.
        module_name (str): Current module.
        function_name (str): Current function.
    """
    logger.debug(cfg.LOGGER_START)

    insert_dbt_row(
        logger,
        cfg.DBT_JOURNAL,
        [
            {
                cfg.DBC_ACTION_CODE: action[0:7],
                cfg.DBC_ACTION_TEXT: action[7:],
                cfg.DBC_DOCUMENT_ID: cfg.document_id,
                cfg.DBC_FUNCTION_NAME: function_name,
                cfg.DBC_MODULE_NAME: module_name,
                cfg.DBC_RUN_ID: cfg.run_id,
            },
        ],
    )

    cfg.journal_id = select_dbt_id_last(logger, cfg.DBT_JOURNAL)

    logger.debug(cfg.LOGGER_END)


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

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    insert_dbt_row(logger, cfg.DBT_RUN, [{cfg.DBC_STATUS: cfg.STATUS_START}])

    cfg.run_id = select_dbt_id_last(logger, cfg.DBT_RUN)

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create and initialise the database table version.
# -----------------------------------------------------------------------------
def create_dbt_version(
    table_name: str = cfg.DBT_VERSION,
) -> None:
    """Create and initialise the database table version.

    If the database table is not yet included in the database schema, then the
    database table is created and the current version number of DCR is
    inserted.

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
        ),
        sqlalchemy.Column(
            cfg.DBC_VERSION, sqlalchemy.String, nullable=False, unique=True
        ),
    )


# -----------------------------------------------------------------------------
# Create the table version entry.
# -----------------------------------------------------------------------------
def create_dbt_version_row(logger: logging.Logger) -> None:
    """Create the table version entry.

    Args:
        logger (logging.Logger): Current logger.
    """
    logger.debug(cfg.LOGGER_START)

    connect_db_core(logger)

    insert_dbt_row(
        logger,
        cfg.DBT_VERSION,
        [{cfg.DBC_VERSION: cfg.config[cfg.DCR_CFG_DCR_VERSION]}],
    )

    disconnect_db(logger)

    logger.debug(cfg.LOGGER_END)


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
        "The database " + get_db_file_name() + " is disconnected",
    )

    logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Get the database file name.
# -----------------------------------------------------------------------------
def get_db_file_name() -> str:
    """Get the database file name.

    Returns:
        str: [description]: Database file name.
    """
    return os.path.join(
        os.getcwd(), Path(cfg.config[cfg.DCR_CFG_DATABASE_FILE])
    )


# -----------------------------------------------------------------------------
# Get the database url.
# -----------------------------------------------------------------------------
def get_db_url() -> str:
    """Get the database url.

    Returns:
        str: [description]: Database url.
    """
    return cfg.config[cfg.DCR_CFG_DATABASE_URL] + get_db_file_name()


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
