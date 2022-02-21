"""Module db: Database Definition Management.

Data definition related processing routines.

Returns:
    [type]: None.
"""
from sqlite3 import Error
from typing import Dict
from typing import List

import libs.cfg
import libs.utils
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import DDL
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint
from sqlalchemy import and_
from sqlalchemy import event
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.engine import Connection
from sqlalchemy.exc import InternalError
from sqlalchemy.exc import OperationalError

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
DB_DIALECT_POSTGRESQL: str = "postgresql"

DBC_ACTION: str = "action"
DBC_ACTION_CODE: str = "action_code"
DBC_ACTION_TEXT: str = "action_text"
DBC_CREATED_AT: str = "created_at"
DBC_DOCUMENT_ID: str = "document_id"
DBC_DOCUMENT_ID_PARENT: str = "document_id_parent"
DBC_FILE_NAME: str = "file_name"
DBC_FILE_TYPE: str = "file_type"
DBC_FUNCTION_NAME: str = "function_name"
DBC_ID: str = "id"
DBC_INBOX_ABS_NAME: str = "inbox_abs_name"
DBC_INBOX_ACCEPTED_ABS_NAME: str = "inbox_accepted_abs_name"
DBC_INBOX_REJECTED_ABS_NAME: str = "inbox_rejected_abs_name"
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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if not sqlalchemy.inspect(libs.cfg.engine).has_table(DBT_VERSION):
        libs.utils.terminate_fatal(
            "The database does not yet exist.",
        )

    current_version = select_version_version_unique()

    if libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION] != current_version:
        libs.utils.terminate_fatal(
            "Current database version is "
            + current_version
            + " - but expected version is "
            + str(libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]),
        )

    libs.utils.progress_msg(
        "The current version of database is " + current_version,
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Connect to the database.
# -----------------------------------------------------------------------------
def connect_db() -> None:
    """Connect to the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    prepare_connect_db()

    try:
        libs.cfg.metadata = MetaData()
    except Error as err:
        libs.utils.terminate_fatal(
            "SQLAlchemy metadata not accessible - error=" + str(err),
        )
    try:
        libs.cfg.engine = sqlalchemy.create_engine(
            libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PREFIX]
            + libs.cfg.config[libs.cfg.DCR_CFG_DB_HOST]
            + ":"
            + libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PORT]
            + "/"
            + libs.cfg.db_current_database
            + "?user="
            + libs.cfg.db_current_user
            + "&password="
            + libs.cfg.config[libs.cfg.DCR_CFG_DB_PASSWORD]
        )

        conn: Connection | None = None

        try:
            conn = libs.cfg.engine.connect()
        except OperationalError as err:
            libs.utils.terminate_fatal(
                "No database connection possible - error=" + str(err),
            )

        conn.close()
    except InternalError as err:
        libs.utils.terminate_fatal(
            "SQLAlchemy engine not accessible - error=" + str(err),
        )
    try:
        libs.cfg.metadata.bind = libs.cfg.engine
    except Error as err:
        libs.utils.terminate_fatal(
            "SQLAlchemy metadata not connectable with engine - error=" + str(err),
        )

    libs.utils.progress_msg_connected()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the trigger function.
# -----------------------------------------------------------------------------
def create_db_trigger_function(column_name: str) -> None:
    """Create the trigger function.

    Args:
        column_name (str): Column name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    event.listen(
        libs.cfg.metadata,
        "after_create",
        DDL(
            """
CREATE FUNCTION function_{column_name}()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
$$
BEGIN
    NEW.{column_name} = NOW();
    RETURN NEW;
END;
$$
            """.replace(
                "{column_name}", column_name
            )
        ),
    )

    libs.utils.progress_msg(
        "The trigger function 'function_" + column_name + "' has now been created"
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the trigger for the database column created_at.
# -----------------------------------------------------------------------------
def create_db_trigger_created_at(table_name: str) -> None:
    """Create the trigger for the database column created_at.

    Args:
        table_name (str): Table name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    event.listen(
        libs.cfg.metadata,
        "after_create",
        DDL(
            """
CREATE TRIGGER trigger_created_at_{table_name}
    BEFORE INSERT
    ON {table_name}
    FOR EACH ROW
    EXECUTE PROCEDURE function_created_at()
    """.replace(
                "{table_name}", table_name
            )
        ),
    )

    libs.utils.progress_msg(
        "The trigger 'trigger_created_at_" + table_name + "' has now been created"
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the trigger for the database column modified_at.
# -----------------------------------------------------------------------------
def create_db_trigger_modified_at(table_name: str) -> None:
    """Create the trigger for the database column modified_at.

    Args:
        table_name (str): Table name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    event.listen(
        libs.cfg.metadata,
        "after_create",
        DDL(
            """
CREATE TRIGGER trigger_modified_at_{table_name}
    BEFORE UPDATE
    ON {table_name}
    FOR EACH ROW
    EXECUTE PROCEDURE function_modified_at()
    """.replace(
                "{table_name}", table_name
            )
        ),
    )

    libs.utils.progress_msg(
        "The trigger 'trigger_modified_at_" + table_name + "' has now been created"
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the triggers for the database tables.
# -----------------------------------------------------------------------------
def create_db_triggers(table_names: List[str]) -> None:
    """Create the triggers for the database tables.

    Args:
        table_names (List[str]): Table names.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.utils.progress_msg("Create the database triggers ...")

    for column_name in [DBC_CREATED_AT, DBC_MODIFIED_AT]:
        create_db_trigger_function(column_name)

    for table_name in table_names:
        create_db_trigger_created_at(table_name)
        if table_name != DBT_JOURNAL:
            create_db_trigger_modified_at(table_name)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table document.
# -----------------------------------------------------------------------------
def create_dbt_document(table_name: str) -> None:
    """Create the database table document.

    Args:
        table_name (str): Table name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        libs.cfg.metadata,
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
            DBC_DOCUMENT_ID_PARENT,
            sqlalchemy.Integer,
            ForeignKey(DBT_DOCUMENT + "." + DBC_ID, ondelete="CASCADE"),
            nullable=True,
        ),
        sqlalchemy.Column(DBC_FILE_NAME, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_FILE_TYPE, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_INBOX_ABS_NAME, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(DBC_INBOX_ACCEPTED_ABS_NAME, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(DBC_INBOX_REJECTED_ABS_NAME, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(DBC_RUN_ID, sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column(DBC_SHA256, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_STEM_NAME, sqlalchemy.String, nullable=False),
    )

    libs.utils.progress_msg("The database table '" + table_name + "' has now been created")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table journal.
# -----------------------------------------------------------------------------
def create_dbt_journal(table_name: str) -> None:
    """Create the database table journal.

    Args:
        table_name (str): Table name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        libs.cfg.metadata,
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
        sqlalchemy.Column(DBC_FUNCTION_NAME, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(DBC_MODULE_NAME, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            DBC_RUN_ID,
            sqlalchemy.Integer,
            ForeignKey(DBT_RUN + "." + DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        UniqueConstraint(DBC_DOCUMENT_ID, DBC_ACTION_CODE, name="unique_key_1"),
    )

    libs.utils.progress_msg("The database table '" + table_name + "' has now been created")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table run.
# -----------------------------------------------------------------------------
def create_dbt_run(table_name: str) -> None:
    """Create the database table run.

    Args:
        table_name (str): Table name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        libs.cfg.metadata,
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

    libs.utils.progress_msg("The database table '" + table_name + "' has now been created")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        libs.cfg.metadata,
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
        sqlalchemy.Column(DBC_VERSION, sqlalchemy.String, nullable=False, unique=True),
    )

    libs.utils.progress_msg("The database table '" + table_name + "' has now been created")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database tables and triggers.
# -----------------------------------------------------------------------------
def create_schema() -> None:
    """Create the database tables and triggers."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    schema = libs.cfg.config[libs.cfg.DCR_CFG_DB_SCHEMA]

    connect_db()

    libs.cfg.engine.execute(sqlalchemy.schema.CreateSchema(schema))

    with libs.cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(DDL("DROP SCHEMA IF EXISTS " + schema + " CASCADE"))
        libs.utils.progress_msg("If existing, the schema '" + schema + "' has now been dropped")

        conn.execute(DDL("CREATE SCHEMA " + schema))
        libs.utils.progress_msg("The schema '" + schema + "' has now been created")

        conn.execute(DDL("ALTER ROLE " + libs.cfg.db_current_user + " SET search_path = " + schema))
        conn.execute(DDL("SET search_path = " + schema))
        libs.utils.progress_msg("The search path '" + schema + "' has now been set")

        conn.close()

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

    libs.cfg.metadata.create_all(libs.cfg.engine)

    insert_dbt_row(DBT_VERSION, {DBC_VERSION: libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]})

    # Disconnect from the database.
    disconnect_db()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Disconnect the database.
# -----------------------------------------------------------------------------
def disconnect_db() -> None:
    """Disconnect the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    try:
        libs.cfg.metadata.clear()
    except Error as err:
        libs.utils.terminate_fatal(
            "SQLAlchemy metadata could not be cleared - error=" + str(err),
        )

    try:
        libs.cfg.engine.dispose()
    except Error as err:
        libs.utils.terminate_fatal(
            "SQLAlchemy engine could not be disposed - error=" + str(err),
        )

    libs.utils.progress_msg_disconnected()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Get the database url.
# -----------------------------------------------------------------------------
def get_db_url() -> str:
    """Get the database url.

    Returns:
        str: [description]: Database url.
    """
    return (
        libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PREFIX]
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_HOST]
        + ":"
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PORT]
        + "/"
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_DATABASE]
        + "?user="
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_USER]
        + "&password="
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_PASSWORD]
    )


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_dbt_row(
    table_name: str,
    columns: libs.cfg.Columns,
) -> sqlalchemy.Integer:
    """Insert a new row into a database table.

    Args:
        table_name (str): Table name.
        columns (libs.cfg.TYPE_COLUMNS_INSERT): Pairs of column name and value.

    Returns:
        sqlalchemy.Integer: The last id found.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = Table(table_name, libs.cfg.metadata, autoload_with=libs.cfg.engine)

    with libs.cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(insert(dbt).values(columns))
        conn.close()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    return select_dbt_id_last(table_name)


# -----------------------------------------------------------------------------
# Prepare the database connection for normal users.
# -----------------------------------------------------------------------------
def prepare_connect_db() -> None:
    """Prepare the database connection for normal users."""
    if libs.cfg.is_docker_container:
        libs.utils.start_db_docker_container()

    libs.cfg.db_current_database = libs.cfg.config[libs.cfg.DCR_CFG_DB_DATABASE]
    libs.cfg.db_current_user = libs.cfg.config[libs.cfg.DCR_CFG_DB_USER]


# -----------------------------------------------------------------------------
# Get the last id from a database table.
# -----------------------------------------------------------------------------
def select_dbt_id_last(table_name: str) -> int | sqlalchemy.Integer:
    """Get the last id from a database table.

    Args:
        table_name (str): Database table name.

    Returns:
        sqlalchemy.Integer: The last id found.
    """
    dbt = Table(table_name, libs.cfg.metadata, autoload_with=libs.cfg.engine)

    with libs.cfg.engine.connect() as conn:
        result = conn.execute(select(func.max(dbt.c.id)))
        row = result.fetchone()
        conn.close()

    if row[0] == "None":
        return 0

    return row[0]


# -----------------------------------------------------------------------------
# Get the filename of an accepted document based on the hash key.
# -----------------------------------------------------------------------------
def select_document_file_name_sha256(document_id: sqlalchemy.Integer, sha256: str) -> str | None:
    """Get the filename of an accepted document based on the hash key.

    Args:
        document_id (sqlalchemy.Integer): Document id.
        sha256 (str): Hash key.

    Returns:
        str: The file name found.
    """
    dbt = Table(DBT_DOCUMENT, libs.cfg.metadata, autoload_with=libs.cfg.engine)

    with libs.cfg.engine.connect() as conn:
        row = conn.execute(
            select(dbt.c.file_name).where(
                and_(
                    dbt.c.id != document_id,
                    dbt.c.sha256 == sha256,
                    dbt.c.inbox_rejected_abs_name is None,
                )
            )
        ).fetchone()
        conn.close()

    if row is None:
        return row

    return row[0]


# -----------------------------------------------------------------------------
# Get the last run_id from database table run.
# -----------------------------------------------------------------------------
def select_run_run_id_last() -> int | sqlalchemy.Integer:
    """Get the last run_id from database table run.

    Returns:
        sqlalchemy.Integer: The last run id found.
    """
    dbt = Table(DBT_RUN, libs.cfg.metadata, autoload_with=libs.cfg.engine)

    with libs.cfg.engine.connect() as conn:
        row = conn.execute(select(func.max(dbt.c.run_id))).fetchone()
        conn.close()

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
    dbt = Table(DBT_VERSION, libs.cfg.metadata, autoload_with=libs.cfg.engine)

    current_version: str = ""

    with libs.cfg.engine.connect() as conn:
        for row in conn.execute(select(dbt.c.version)):
            if current_version == "":
                current_version = row.version
            else:
                libs.utils.terminate_fatal(
                    "Column version in database table version not unique",
                )
        conn.close()

    if current_version == "":
        libs.utils.terminate_fatal("Column version in database table version not found")

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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = Table(table_name, libs.cfg.metadata, autoload_with=libs.cfg.engine)

    with libs.cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(update(dbt).where(dbt.c.id == id_where).values(columns))
        conn.close()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Update the document and create a new journal entry.
# -----------------------------------------------------------------------------
def update_document_status(
    document_columns: libs.cfg.Columns,
    journal_columns: libs.cfg.Columns,
) -> None:
    """Update the document and create a new journal entry.

    Args:
        document_columns (libs.cfg.Columns): Columns regarding
                                        database table document.
        journal_columns (libs.cfg.Columns): Columns regarding
                                       database table journal.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    update_dbt_id(
        DBT_DOCUMENT,
        libs.cfg.document_id,
        document_columns,
    )

    insert_dbt_row(
        DBT_JOURNAL,
        journal_columns | {DBC_DOCUMENT_ID: libs.cfg.document_id, DBC_RUN_ID: libs.cfg.run_run_id},
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


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
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = Table(DBT_VERSION, libs.cfg.metadata, autoload_with=libs.cfg.engine)

    with libs.cfg.engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(
            update(dbt).values(
                {
                    DBC_VERSION: version,
                }
            )
        )
        conn.close()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
