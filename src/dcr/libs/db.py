"""Module db: Database Definition Management.

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
# Global Constants.
# -----------------------------------------------------------------------------
DBC_ACTION: str = "action"
DBC_ACTION_CODE: str = "action_code"
DBC_ACTION_TEXT: str = "action_text"
DBC_CREATED_AT: str = "created_at"
DBC_DOCUMENT_ID: str = "document_id"
DBC_FILE_NAME: str = "file_name"
DBC_FILE_TYPE: str = "file_type"
DBC_FUNCTION_NAME: str = "function_name"
DBC_ID: str = "id"
DBC_INBOX_ABS_NAME: str = "inbox_abs_name"
DBC_INBOX_ACCEPTED_ABS_NAME: str = "inbox_accepted_abs_name"
DBC_INBOX_ACCEPTED_CONFIG: str = "inbox_accepted_config"
DBC_INBOX_CONFIG: str = "inbox_config"
DBC_INBOX_REJECTED_ABS_NAME: str = "inbox_rejected_abs_name"
DBC_INBOX_REJECTED_CONFIG: str = "inbox_rejected_config"
DBC_MODIFIED_AT: str = "modified_at"
DBC_MODULE_NAME: str = "module_name"
DBC_RUN_ID: str = "run_id"
DBC_SHA256: str = "sha256"
DBC_STATUS: str = "status"
DBC_STEM_NAME: str = "stem_name"
DBC_TOTAL_ERRONEOUS: str = "total_erroneous"
DBC_TOTAL_OK_PROCESSED: str = "total_ok_processed"
DBC_TOTAL_TO_BE_PROCESSED: str = "total_to_be_processed"
DBC_VERSION: str = "version"

DBT_DOCUMENT: str = "document"
DBT_JOURNAL: str = "journal"
DBT_RUN: str = "run"
DBT_VERSION: str = "version"


# -----------------------------------------------------------------------------
# Check that the database version is up to date.
# -----------------------------------------------------------------------------
def check_db_up_to_date() -> None:
    """Check that the database version is up-to-date."""
    cfg.logger.debug(cfg.LOGGER_START)

    if not sqlalchemy.inspect(cfg.engine).has_table(DBT_VERSION):
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

    create_dbt_document(DBT_DOCUMENT)
    create_dbt_run(DBT_RUN)
    create_dbt_version(DBT_VERSION)
    # FK: document
    # FK: run
    create_dbt_journal(DBT_JOURNAL)

    # Create the database triggers.
    create_db_triggers(
        [
            DBT_DOCUMENT,
            DBT_JOURNAL,
            DBT_RUN,
            DBT_VERSION,
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
    utils.progress_msg("Create the database triggers ...")

    for table_name in table_names:
        create_db_trigger_created_at(table_name)
        if table_name != DBT_JOURNAL:
            create_db_trigger_modified_at(table_name)


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
            DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(DBC_FILE_NAME, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_FILE_TYPE, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_RUN_ID, sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column(DBC_SHA256, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_STEM_NAME, sqlalchemy.String, nullable=False),
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
            DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(DBC_ACTION_CODE, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_ACTION_TEXT, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            ForeignKey(DBT_DOCUMENT + "." + DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(
            DBC_FUNCTION_NAME, sqlalchemy.String, nullable=False
        ),
        sqlalchemy.Column(DBC_MODULE_NAME, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            DBC_RUN_ID,
            sqlalchemy.Integer,
            ForeignKey(DBT_RUN + "." + DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        UniqueConstraint(
            DBC_DOCUMENT_ID, DBC_ACTION_CODE, name="unique_key_1"
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
            DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(DBC_ACTION, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            DBC_INBOX_ABS_NAME, sqlalchemy.String, nullable=True
        ),
        sqlalchemy.Column(DBC_INBOX_CONFIG, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(
            DBC_INBOX_ACCEPTED_ABS_NAME, sqlalchemy.String, nullable=True
        ),
        sqlalchemy.Column(
            DBC_INBOX_ACCEPTED_CONFIG, sqlalchemy.String, nullable=True
        ),
        sqlalchemy.Column(
            DBC_INBOX_REJECTED_ABS_NAME, sqlalchemy.String, nullable=True
        ),
        sqlalchemy.Column(
            DBC_INBOX_REJECTED_CONFIG, sqlalchemy.String, nullable=True
        ),
        sqlalchemy.Column(DBC_RUN_ID, sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column(DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            DBC_TOTAL_ERRONEOUS,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(
            DBC_TOTAL_OK_PROCESSED,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(
            DBC_TOTAL_TO_BE_PROCESSED,
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
            DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            DBC_VERSION, sqlalchemy.String, nullable=False, unique=True
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
    insert_dbt_row(
        DBT_DOCUMENT,
        [
            {
                DBC_FILE_NAME: cfg.file_name,
                DBC_FILE_TYPE: cfg.file_type,
                DBC_RUN_ID: cfg.run_run_id,
                DBC_SHA256: cfg.sha256,
                DBC_STATUS: cfg.STATUS_INBOX,
                DBC_STEM_NAME: cfg.stem_name,
            },
        ],
    )

    cfg.document_id = select_dbt_id_last(DBT_DOCUMENT)


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
    insert_dbt_row(
        DBT_JOURNAL,
        [
            {
                DBC_ACTION_CODE: action[0:7],
                DBC_ACTION_TEXT: action[7:],
                DBC_DOCUMENT_ID: cfg.document_id,
                DBC_FUNCTION_NAME: function_name,
                DBC_MODULE_NAME: module_name,
                DBC_RUN_ID: cfg.run_id,
            },
        ],
    )

    cfg.journal_id = select_dbt_id_last(DBT_JOURNAL)


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_dbt_row(table_name: str, columns: cfg.Columns) -> None:
    """Insert a new row into a database table.

    Args:
        table_name (str): Table name.
        columns (Columns): Pairs of column name and value.
    """
    dbt = Table(table_name, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(insert(dbt).values(columns))


# -----------------------------------------------------------------------------
# Insert the table run entry.
# -----------------------------------------------------------------------------
def insert_dbt_run_row() -> None:
    """Insert the table run entry."""
    insert_dbt_row(
        DBT_RUN,
        [
            {
                DBC_ACTION: cfg.run_action,
                DBC_RUN_ID: cfg.run_run_id,
                DBC_STATUS: cfg.STATUS_START,
            },
        ],
    )

    cfg.run_id = select_dbt_id_last(DBT_RUN)


# -----------------------------------------------------------------------------
# Insert the table version entry.
# -----------------------------------------------------------------------------
def insert_dbt_version_row() -> None:
    """Create the table version entry."""
    insert_dbt_row(
        DBT_VERSION,
        [{DBC_VERSION: cfg.config[cfg.DCR_CFG_DCR_VERSION]}],
    )


# -----------------------------------------------------------------------------
# Get the last id from a database table.
# -----------------------------------------------------------------------------
def select_dbt_id_last(table_name: str) -> int:
    """Get the last id from a database table.

    Get the version number from the database table `version`.

    Args:
        table_name (str): Database table name.

    Returns:
        int: The last id found.
    """
    dbt = Table(table_name, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect() as conn:
        result = conn.execute(select(func.max(dbt.c.id)))
        row = result.fetchone()

    if row[0] is None:
        return 0

    return row[0]


# -----------------------------------------------------------------------------
# Get the last run_id from database table run.
# -----------------------------------------------------------------------------
def select_run_run_id_last() -> int:
    """Get the last run_id from database table run.

    Returns:
        int: The last run id found.
    """
    dbt = Table(DBT_RUN, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect() as conn:
        result = conn.execute(select(func.max(dbt.c.run_id)))
        row = result.fetchone()

    if row[0] is None:
        return 0

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
    dbt = Table(DBT_VERSION, cfg.metadata, autoload_with=cfg.engine)

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
    dbt = Table(table_name, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(update(dbt).where(dbt.c.id == id_where).values(columns))


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
    update_dbt_id(
        DBT_DOCUMENT,
        cfg.document_id,
        {
            DBC_STATUS: status,
        },
    )

    insert_dbt_journal_row(
        action,
        function_name,
        module_name,
    )


# -----------------------------------------------------------------------------
# Update the database version number.
# -----------------------------------------------------------------------------
def update_version_version(
    version: str,
) -> None:
    """Update the database version number in database table version.

    Args:
        version (str): New version number.
    """
    dbt = Table(DBT_VERSION, cfg.metadata, autoload_with=cfg.engine)

    with cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(
            update(dbt).values(
                {
                    DBC_VERSION: version,
                }
            )
        )


# -----------------------------------------------------------------------------
# Upgrade the current database schema.
# -----------------------------------------------------------------------------
def upgrade_database() -> None:
    """Upgrade the current database schema.

    Check if the current database schema needs to be upgraded and perform the
    necessary steps.
    """
    cfg.logger.debug(cfg.LOGGER_START)

    db_file_name = get_db_file_name()

    if not os.path.isfile(db_file_name):
        utils.terminate_fatal(
            "Database file " + db_file_name + " is missing",
        )

    connect_db_core()

    utils.progress_msg("Upgrade the database tables ...")

    current_version: str = select_version_version_unique()

    if current_version == cfg.config[cfg.DCR_CFG_DCR_VERSION]:
        utils.progress_msg(
            "The database "
            + db_file_name
            + " is already up to date, version number="
            + current_version,
        )
    else:
        while (
            select_version_version_unique()
            != cfg.config[cfg.DCR_CFG_DCR_VERSION]
        ):
            upgrade_database_version()

        utils.progress_msg(
            "The database "
            + db_file_name
            + " has been successfully upgraded, version number="
            + select_version_version_unique(),
        )

    cfg.logger.debug(cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Upgrade the current database schema - from one version to the next.
# -----------------------------------------------------------------------------
def upgrade_database_version() -> None:
    """Upgrade the current database schema - from one version to the next."""
    cfg.logger.debug(cfg.LOGGER_START)

    db_file_name = get_db_file_name()

    current_version: str = select_version_version_unique()

    if current_version == "0.5.0":
        upgrade_database_version_0_5_0()
        return

    utils.terminate_fatal(
        "Database file "
        + db_file_name
        + " has the wrong version, version number="
        + current_version,
    )


# -----------------------------------------------------------------------------
# Upgrade the current database schema - from version 0.5.0.
# -----------------------------------------------------------------------------
def upgrade_database_version_0_5_0() -> None:
    """Upgrade the current database schema - from version 0.5.0."""
    current_version: str = "0.5.0"
    target_version: str = "0.6.0"

    utils.progress_msg(
        "Upgrade step: from version number="
        + current_version
        + " to version number="
        + target_version,
    )

    with cfg.engine.connect().execution_options(autocommit=True) as conn:
        # ---------------------------------------------------------------------
        # Database table: document
        # ---------------------------------------------------------------------
        conn.execute(
            "ALTER TABLE "
            + DBT_DOCUMENT
            + " ADD COLUMN "
            + DBC_SHA256
            + " TEXT DEFAULT 'n/a' NOT NULL"
        )
        conn.execute(
            "ALTER TABLE "
            + DBT_DOCUMENT
            + " ADD COLUMN "
            + DBC_RUN_ID
            + " INTEGER DEFAULT -1 NOT NULL"
        )

        dbt = Table(DBT_DOCUMENT, cfg.metadata, autoload_with=cfg.engine)

        conn.execute(update(dbt).where(dbt.c.run_id == -1).values(run_id=1))

        rows = conn.execute(
            select(dbt.c.file_name, dbt.c.id, dbt.c.status).where(
                dbt.c.sha256 == "n/a"
            )
        )

        for row in rows:
            if row.status in ([]):
                directory: str = cfg.config[
                    cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED
                ]
            else:
                directory: str = cfg.config[
                    cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED
                ]

            sha256: str = utils.get_sha256(
                os.path.join(directory, row.file_name)
            )
            update(dbt).where(dbt.c.id == row.id).values(sha256=sha256)

        # ---------------------------------------------------------------------
        # Database table: run
        # ---------------------------------------------------------------------
        conn.execute(
            "ALTER TABLE "
            + DBT_RUN
            + " ADD COLUMN "
            + DBC_ACTION
            + " TEXT DEFAULT 'n/a' NOT NULL"
        )
        conn.execute(
            "ALTER TABLE "
            + DBT_RUN
            + " ADD COLUMN "
            + DBC_RUN_ID
            + " INTEGER DEFAULT -1 NOT NULL"
        )
        conn.execute(
            "ALTER TABLE "
            + DBT_RUN
            + " RENAME COLUMN total_accepted TO "
            + DBC_TOTAL_OK_PROCESSED
        )
        conn.execute(
            "ALTER TABLE "
            + DBT_RUN
            + " RENAME COLUMN total_new TO "
            + DBC_TOTAL_TO_BE_PROCESSED
        )
        conn.execute(
            "ALTER TABLE "
            + DBT_RUN
            + " RENAME COLUMN total_rejected TO "
            + DBC_TOTAL_ERRONEOUS
        )

        dbt = Table(DBT_RUN, cfg.metadata, autoload_with=cfg.engine)

        conn.execute(
            update(dbt)
            .where(dbt.c.action == "n/a")
            .values(action=cfg.RUN_ACTION_PROCESS_INBOX)
        )

        conn.execute(
            update(dbt).where(dbt.c.run_id == -1).values(run_id=dbt.c.id)
        )

    update_version_version(target_version)
