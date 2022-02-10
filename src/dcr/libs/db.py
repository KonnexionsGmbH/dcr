"""Database Definition Management.

Data definition related processing routines.

Returns:
    [type]: None.
"""
import os
from pathlib import Path
from sqlite3 import Error
from typing import Dict
from typing import List

import sqlalchemy
import sqlalchemy.orm
from libs import cfg
from libs import utils
from sqlalchemy import DDL
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint
from sqlalchemy import event
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update


# -----------------------------------------------------------------------------
# Check that the database version is up to date.
# -----------------------------------------------------------------------------
def check_db_up_to_date() -> None:
    """Check that the database version is up-to-date."""
    cfg.logger.debug(cfg.LOGGER_START)

    if not sqlalchemy.inspect(cfg.engine).has_table(cfg.DBT_VERSION):
        utils.terminate_fatal(
            "The database " + get_db_file_name() + " does not yet exist.",
        )

    current_version = select_version_version_unique()

    if cfg.config[cfg.DCR_CFG_DCR_VERSION] != current_version:
        utils.terminate_fatal(
            "Current database version is "
            + current_version
            + " - but expected version is "
            + str(cfg.config[cfg.DCR_CFG_DCR_VERSION]),
        )

    utils.progress_msg(
        "The current version of database "
        + get_db_file_name()
        + " is "
        + current_version,
    )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Connect to the database.
# -----------------------------------------------------------------------------
def connect_db() -> None:
    """Connect to the database."""
    cfg.logger.debug(cfg.LOGGER_START)

    db_file_name = get_db_file_name()

    if not os.path.isfile(db_file_name):
        utils.terminate_fatal(
            "Database file " + db_file_name + " is missing",
        )

    connect_db_core()

    print("")
    utils.progress_msg(
        "The database " + db_file_name + " is now connected",
    )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Connect to the database - core functionality.
# -----------------------------------------------------------------------------
def connect_db_core() -> None:
    """Connect to the database - core functionality."""
    cfg.logger.debug(cfg.LOGGER_START)

    try:
        cfg.metadata = MetaData()
    except Error as err:
        utils.terminate_fatal(
            "SQLAlchemy metadata not accessible - error=" + str(err),
        )
    try:
        cfg.engine = sqlalchemy.create_engine(get_db_url())
    except Error as err:
        utils.terminate_fatal(
            "SQLAlchemy engine not accessible - error=" + str(err),
        )
    try:
        cfg.metadata.bind = cfg.engine
    except Error as err:
        utils.terminate_fatal(
            "SQLAlchemy metadata not connectable with engine - error="
            + str(err),
        )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database.
# -----------------------------------------------------------------------------
def create_database() -> None:
    """Create the database tables."""
    cfg.logger.debug(cfg.LOGGER_START)

    db_file_name = get_db_file_name()

    if os.path.isfile(db_file_name):
        utils.terminate_fatal(
            "Database file " + db_file_name + " is already existing",
        )

    connect_db_core()

    utils.progress_msg("Create the database tables ...")

    create_dbt_document(cfg.DBT_DOCUMENT)
    create_dbt_run(cfg.DBT_RUN)
    create_dbt_version(cfg.DBT_VERSION)
    # FK: document
    # FK: run
    create_dbt_journal(cfg.DBT_JOURNAL)

    # Create the database triggers.
    create_db_triggers(
        [
            cfg.DBT_DOCUMENT,
            cfg.DBT_JOURNAL,
            cfg.DBT_RUN,
            cfg.DBT_VERSION,
        ],
    )

    try:
        cfg.metadata.create_all(cfg.engine)
    except Error as err:
        utils.terminate_fatal(
            "SQLAlchemy 'metadata.create_all(engine)' issue - error="
            + str(err),
        )

    insert_dbt_version_row()

    utils.progress_msg(
        "The database "
        + db_file_name
        + " has been successfully created, version number="
        + cfg.config[cfg.DCR_CFG_DCR_VERSION],
    )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the trigger for the database column created_at.
# -----------------------------------------------------------------------------
def create_db_trigger_created_at(table_name: str) -> None:
    """Create the trigger for the database column created_at.

    Args:
        table_name (str): Table name.
    """
    event.listen(
        cfg.metadata,
        "after_create",
        DDL(
            """
        CREATE TRIGGER IF NOT EXISTS trigger_created_at_xxx AFTER INSERT
        ON xxx FOR EACH ROW
            BEGIN
                UPDATE xxx
                   SET created_at = strftime('%%Y-%%m-%%d %%H:%%M:%%f',
                                             DATETIME('now'))
                 WHERE id = NEW.id;
            END   """.replace(
                "xxx", table_name
            )
        ),
    )


# -----------------------------------------------------------------------------
# Create the trigger for the database column modified_at.
# -----------------------------------------------------------------------------
def create_db_trigger_modified_at(table_name: str) -> None:
    """Create the trigger for the database column modified_at.

    Args:
        table_name (str): Table name.
    """
    event.listen(
        cfg.metadata,
        "after_create",
        DDL(
            """
CREATE TRIGGER IF NOT EXISTS trigger_modified_at_xxx AFTER UPDATE
ON xxx FOR EACH ROW
    BEGIN
        UPDATE xxx
           SET modified_at = strftime('%%Y-%%m-%%d %%H:%%M:%%f',
                                      DATETIME('now'))
         WHERE id = NEW.id;
    END   """.replace(
                "xxx", table_name
            )
        ),
    )


# -----------------------------------------------------------------------------
# Create the triggers for the database tables.
# -----------------------------------------------------------------------------
def create_db_triggers(table_names: List[str]) -> None:
    """Create the triggers for the database tables.

    Args:
        table_names (List[str]): Table names.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    utils.progress_msg("Create the database triggers ...")

    for table_name in table_names:
        create_db_trigger_created_at(table_name)
        if table_name != cfg.DBT_JOURNAL:
            create_db_trigger_modified_at(table_name)

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table document.
# -----------------------------------------------------------------------------
def create_dbt_document(table_name: str) -> None:
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
# Create the database table journal.
# -----------------------------------------------------------------------------
def create_dbt_journal(table_name: str) -> None:
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
# Create the database table run.
# -----------------------------------------------------------------------------
def create_dbt_run(table_name: str) -> None:
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
# Create and initialise the database table version.
# -----------------------------------------------------------------------------
def create_dbt_version(
    table_name: str,
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
# Disconnect the database.
# -----------------------------------------------------------------------------
def disconnect_db() -> None:
    """Disconnect the database."""
    cfg.logger.debug(cfg.LOGGER_START)

    try:
        cfg.metadata.clear()
    except Error as err:
        utils.terminate_fatal(
            "SQLAlchemy metadata could not be cleared - error=" + str(err),
        )

    try:
        cfg.engine.dispose()
    except Error as err:
        utils.terminate_fatal(
            "SQLAlchemy engine could not be disposed - error=" + str(err),
        )

    print("")
    utils.progress_msg(
        "The database " + get_db_file_name() + " is now disconnected",
    )

    cfg.logger.debug(cfg.LOGGER_END)


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
# Insert the table document entry.
# -----------------------------------------------------------------------------
def insert_dbt_document_row() -> None:
    """Insert the table document entry."""
    cfg.logger.debug(cfg.LOGGER_START)

    insert_dbt_row(
        cfg.DBT_DOCUMENT,
        [
            {
                cfg.DBC_FILE_NAME: cfg.file_name,
                cfg.DBC_FILE_TYPE: cfg.file_type,
                cfg.DBC_STATUS: cfg.STATUS_INBOX,
                cfg.DBC_STEM_NAME: cfg.stem_name,
            },
        ],
    )

    cfg.document_id = select_dbt_id_last(cfg.DBT_DOCUMENT)

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Insert the table journal entry.
# -----------------------------------------------------------------------------
def insert_dbt_journal_row(
    action: str,
    function_name: str,
    module_name: str,
) -> None:
    """Insert the table journal entry.

    Args:
        action (str): Current action.
        function_name (str): Name of the originating function.
        module_name (str): Name of the originating module.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    insert_dbt_row(
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

    cfg.journal_id = select_dbt_id_last(cfg.DBT_JOURNAL)

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_dbt_row(table_name: str, columns: cfg.Columns) -> None:
    """Insert a new row into a database table.

    Args:
        table_name (str): Table name.
        columns (Columns): Pairs of column name and value.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    dbt = Table(table_name, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(insert(dbt).values(columns))

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Insert the table run entry.
# -----------------------------------------------------------------------------
def insert_dbt_run_row() -> None:
    """Insert the table run entry."""
    cfg.logger.debug(cfg.LOGGER_START)

    insert_dbt_row(cfg.DBT_RUN, [{cfg.DBC_STATUS: cfg.STATUS_START}])

    cfg.run_id = select_dbt_id_last(cfg.DBT_RUN)

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Insert the table version entry.
# -----------------------------------------------------------------------------
def insert_dbt_version_row() -> None:
    """Create the table version entry."""
    cfg.logger.debug(cfg.LOGGER_START)

    connect_db_core()

    insert_dbt_row(
        cfg.DBT_VERSION,
        [{cfg.DBC_VERSION: cfg.config[cfg.DCR_CFG_DCR_VERSION]}],
    )

    disconnect_db()

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Get the last id from a database table.
# -----------------------------------------------------------------------------
def select_dbt_id_last(table_name: str) -> sqlalchemy.Integer:
    """Get the last id from a database table.

    Get the version number from the database table `version`.

    Args:
        table_name (str): Database table name.

    Returns:
        sqlalchemy.Integer: The last id found.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    dbt = Table(table_name, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect() as conn:
        result = conn.execute(select(func.max(dbt.c.id)))
        row = result.fetchone()

    cfg.logger.debug(cfg.LOGGER_END)

    return row[0]


# -----------------------------------------------------------------------------
# Get the version number from the database table version.
# -----------------------------------------------------------------------------
def select_version_version_unique() -> str:
    """Get the version number.

    Get the version number from the database table `version`.

    Returns:
        str: The version number found.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    dbt = Table(cfg.DBT_VERSION, cfg.metadata, autoload_with=cfg.engine)

    current_version: str = ""

    with cfg.engine.connect() as conn:
        for row in conn.execute(select(dbt.c.version)):
            if current_version == "":
                current_version = row.version
            else:
                utils.terminate_fatal(
                    "Column version in database table version not unique",
                )

    if current_version == "":
        utils.terminate_fatal(
            "Column version in database table version not found"
        )

    cfg.logger.debug(cfg.LOGGER_END)

    return current_version


# -----------------------------------------------------------------------------
# Update a database row based on its id column.
# -----------------------------------------------------------------------------
def update_dbt_id(
    table_name: str,
    id_where: sqlalchemy.Integer,
    columns: Dict[str, str],
) -> None:
    """Update a database row based on its id column.

    Args:
        table_name (str): Table name.
        id_where (sqlalchemy.Integer): Content of column id.
        columns (Columns): Pairs of column name and value.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    dbt = Table(table_name, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(update(dbt).where(dbt.c.id == id_where).values(columns))

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Update the document status and create a new journal entry.
# -----------------------------------------------------------------------------
def update_document_status(
    action: str,
    function_name: str,
    module_name: str,
    status: str,
) -> None:
    """Update the document status and create a new journal entry.

    Args:
        action (str): Current action.
        function_name (str): Name of the originating function.
        module_name (str): Name of the originating module.
        status (str): Current document status.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    update_dbt_id(
        cfg.DBT_DOCUMENT,
        cfg.document_id,
        {
            cfg.DBC_STATUS: status,
        },
    )

    insert_dbt_journal_row(
        action,
        function_name,
        module_name,
    )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Upgrade the current database schema..
# -----------------------------------------------------------------------------
def upgrade_db() -> None:
    """Upgrade the current database schema.

    Check if the current database schema needs to be upgraded and perform the
    necessary steps.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    # TBD: Database upgrade

    cfg.logger.debug(cfg.LOGGER_END)