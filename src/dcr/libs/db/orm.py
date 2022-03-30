"""Module libs.db.orm: Database Manipulation Management."""
import json
import os
import time
from pathlib import Path
from typing import Dict
from typing import List

import libs.cfg
import libs.db.cfg
import libs.utils
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import DDL
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import and_
from sqlalchemy import event
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.pool import NullPool


# -----------------------------------------------------------------------------
# Check that the database version is up to date.
# -----------------------------------------------------------------------------
def check_db_up_to_date() -> None:
    """Check that the database version is up-to-date."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.db.cfg.db_orm_engine is None:
        libs.utils.terminate_fatal(
            "The database does not yet exist.",
        )

    if not sqlalchemy.inspect(libs.db.cfg.db_orm_engine).has_table(libs.db.cfg.DBT_VERSION):
        libs.utils.terminate_fatal(
            "The database table 'version' does not yet exist.",
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

    libs.db.cfg.db_orm_metadata = MetaData()

    libs.db.cfg.db_orm_engine = sqlalchemy.create_engine(
        libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PREFIX]
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_HOST]
        + ":"
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PORT]
        + "/"
        + libs.db.cfg.db_current_database
        + "?user="
        + libs.db.cfg.db_current_user
        + "&password="
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_PASSWORD],
        poolclass=NullPool,
    )
    libs.db.cfg.db_orm_engine.connect()

    libs.db.cfg.db_orm_metadata.bind = libs.db.cfg.db_orm_engine

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
        libs.db.cfg.db_orm_metadata,
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
        libs.db.cfg.db_orm_metadata,
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
        libs.db.cfg.db_orm_metadata,
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

    for column_name in [libs.db.cfg.DBC_CREATED_AT, libs.db.cfg.DBC_MODIFIED_AT]:
        create_db_trigger_function(column_name)

    for table_name in table_names:
        create_db_trigger_created_at(table_name)
        if table_name != libs.db.cfg.DBT_JOURNAL:
            create_db_trigger_modified_at(table_name)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table content.
# -----------------------------------------------------------------------------
def create_dbt_content(table_name: str) -> None:
    """Create the database table content.

    Args:
        table_name (str): Table name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        libs.db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            libs.db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            ForeignKey(libs.db.cfg.DBT_DOCUMENT + "." + libs.db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_PAGE_IN_DOCUMENT,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_PARA_IN_PAGE,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_LINE_IN_PARA,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_TOKEN_IN_LINE,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_SENTENCE_IN_PARA,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_TOKEN_IN_SENTENCE,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(libs.db.cfg.DBC_TOKEN_PARSED, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(libs.db.cfg.DBC_TOKEN_STEM, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(libs.db.cfg.DBC_TOKEN_LEMMA, sqlalchemy.String, nullable=True),
    )

    libs.utils.progress_msg("The database table '" + table_name + "' has now been created")

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
        libs.db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            libs.db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_CHILD_NO,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(libs.db.cfg.DBC_DIRECTORY_NAME, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(libs.db.cfg.DBC_DIRECTORY_TYPE, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            libs.db.cfg.DBC_DOCUMENT_ID_BASE,
            sqlalchemy.Integer,
            ForeignKey(libs.db.cfg.DBT_DOCUMENT + "." + libs.db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=True,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_DOCUMENT_ID_PARENT,
            sqlalchemy.Integer,
            ForeignKey(libs.db.cfg.DBT_DOCUMENT + "." + libs.db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=True,
        ),
        sqlalchemy.Column(libs.db.cfg.DBC_ERROR_CODE, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(libs.db.cfg.DBC_FILE_NAME, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(libs.db.cfg.DBC_FILE_TYPE, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            libs.db.cfg.DBC_LANGUAGE_ID,
            sqlalchemy.Integer,
            ForeignKey(libs.db.cfg.DBT_LANGUAGE + "." + libs.db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(libs.db.cfg.DBC_NEXT_STEP, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(libs.db.cfg.DBC_RUN_ID, sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column(libs.db.cfg.DBC_SHA256, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(libs.db.cfg.DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(libs.db.cfg.DBC_STEM_NAME, sqlalchemy.String, nullable=False),
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
        libs.db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            libs.db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(libs.db.cfg.DBC_ACTION_CODE, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(libs.db.cfg.DBC_ACTION_TEXT, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            libs.db.cfg.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            ForeignKey(libs.db.cfg.DBT_DOCUMENT + "." + libs.db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(libs.db.cfg.DBC_DURATION_NS, sqlalchemy.BigInteger, nullable=True),
        sqlalchemy.Column(libs.db.cfg.DBC_FUNCTION_NAME, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(libs.db.cfg.DBC_MODULE_NAME, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            libs.db.cfg.DBC_RUN_ID,
            sqlalchemy.Integer,
            ForeignKey(libs.db.cfg.DBT_RUN + "." + libs.db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
    )

    libs.utils.progress_msg("The database table '" + table_name + "' has now been created")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table language.
# -----------------------------------------------------------------------------
def create_dbt_language(table_name: str) -> None:
    """Create the database table language.

    Args:
        table_name (str): Table name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        libs.db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            libs.db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(libs.db.cfg.DBC_ACTIVE, sqlalchemy.Boolean, default=True, nullable=False),
        sqlalchemy.Column(
            libs.db.cfg.DBC_CODE_ISO_639_3, sqlalchemy.String, nullable=False, unique=True
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_CODE_SPACY, sqlalchemy.String, nullable=False, unique=True
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_CODE_TESSERACT, sqlalchemy.String, nullable=False, unique=True
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_DIRECTORY_NAME_INBOX, sqlalchemy.String, nullable=True, unique=True
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_ISO_LANGUAGE_NAME, sqlalchemy.String, nullable=False, unique=True
        ),
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
        libs.db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            libs.db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(libs.db.cfg.DBC_ACTION, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(libs.db.cfg.DBC_RUN_ID, sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column(libs.db.cfg.DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            libs.db.cfg.DBC_TOTAL_ERRONEOUS,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_TOTAL_OK_PROCESSED,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_TOTAL_TO_BE_PROCESSED,
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
        libs.db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            libs.db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            libs.db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(libs.db.cfg.DBC_VERSION, sqlalchemy.String, nullable=False, unique=True),
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

    libs.db.cfg.db_orm_engine.execute(sqlalchemy.schema.CreateSchema(schema))

    with libs.db.cfg.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(DDL("DROP SCHEMA IF EXISTS " + schema + " CASCADE"))
        libs.utils.progress_msg("If existing, the schema '" + schema + "' has now been dropped")

        conn.execute(DDL("CREATE SCHEMA " + schema))
        libs.utils.progress_msg("The schema '" + schema + "' has now been created")

        conn.execute(
            DDL("ALTER ROLE " + libs.db.cfg.db_current_user + " SET search_path = " + schema)
        )
        conn.execute(DDL("SET search_path = " + schema))
        libs.utils.progress_msg("The search path '" + schema + "' has now been set")

        conn.close()

    create_dbt_language(libs.db.cfg.DBT_LANGUAGE)
    create_dbt_run(libs.db.cfg.DBT_RUN)
    create_dbt_version(libs.db.cfg.DBT_VERSION)
    # FK: language
    create_dbt_document(libs.db.cfg.DBT_DOCUMENT)
    # FK: document
    create_dbt_content(libs.db.cfg.DBT_CONTENT)
    # FK: run
    create_dbt_journal(libs.db.cfg.DBT_JOURNAL)

    # Create the database triggers.
    create_db_triggers(
        [
            libs.db.cfg.DBT_CONTENT,
            libs.db.cfg.DBT_DOCUMENT,
            libs.db.cfg.DBT_JOURNAL,
            libs.db.cfg.DBT_LANGUAGE,
            libs.db.cfg.DBT_RUN,
            libs.db.cfg.DBT_VERSION,
        ],
    )

    libs.db.cfg.db_orm_metadata.create_all(libs.db.cfg.db_orm_engine)

    insert_dbt_row(
        libs.db.cfg.DBT_LANGUAGE,
        {
            libs.db.cfg.DBC_CODE_ISO_639_3: "eng",
            libs.db.cfg.DBC_CODE_SPACY: "en",
            libs.db.cfg.DBC_CODE_TESSERACT: "eng",
            libs.db.cfg.DBC_DIRECTORY_NAME_INBOX: str(
                libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
            ),
            libs.db.cfg.DBC_ISO_LANGUAGE_NAME: "English",
        },
    )

    insert_dbt_row(
        libs.db.cfg.DBT_VERSION,
        {
            libs.db.cfg.DBC_VERSION: libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION],
        },
    )

    if libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]:
        initial_database_data_path = Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA])
        if os.path.isfile(initial_database_data_path):
            load_db_data_from_json(initial_database_data_path)
        else:
            libs.utils.terminate_fatal(
                "File with initial database data is missing - file name '"
                + libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]
                + "'"
            )

    # Disconnect from the database.
    disconnect_db()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Disconnect the database.
# -----------------------------------------------------------------------------
def disconnect_db() -> None:
    """Disconnect the database."""
    if libs.db.cfg.db_orm_metadata is None and libs.db.cfg.db_orm_engine is None:
        libs.db.cfg.db_current_database = None
        libs.db.cfg.db_current_user = None
        libs.utils.progress_msg(
            "There is currently no open database connection (orm)",
        )
        return

    if libs.db.cfg.db_orm_metadata is not None:
        libs.db.cfg.db_orm_metadata.clear()
        libs.db.cfg.db_orm_metadata = None

    if libs.db.cfg.db_orm_engine is not None:
        libs.db.cfg.db_orm_engine.dispose()
        libs.db.cfg.db_orm_engine = None

    libs.utils.progress_msg_disconnected()


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

    dbt = Table(table_name, libs.db.cfg.db_orm_metadata, autoload_with=libs.db.cfg.db_orm_engine)

    with libs.db.cfg.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        result = conn.execute(insert(dbt).values(columns).returning(dbt.columns.id))
        row = result.fetchone()
        conn.close()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    return row[0]


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_journal(
    module_name: str,
    function_name: str,
    document_id: sqlalchemy.Integer,
    journal_action: str,
) -> None:
    """Insert a new row into database table 'journal'.

    Args:
        module_name (str): Module name.
        function_name (str): Function name.
        document_id (sqlalchemy.Integer): Document id.
        journal_action (str): Journal action.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    action_code = journal_action[0:6]

    if action_code in [
        "01.002",
        "11.003",
        "21.003",
        "21.005",
        "31.003",
        "41.003",
        "51.003",
        "61.002",
    ]:
        duration_ns = time.perf_counter_ns() - libs.cfg.start_time_document
        libs.utils.progress_msg(
            f"Time : {duration_ns / 1000000000 :10.2f} s - processing duration "
            + f"of document {libs.cfg.document_file_name}",
        )
    else:
        duration_ns = 0

    insert_dbt_row(
        libs.db.cfg.DBT_JOURNAL,
        {
            libs.db.cfg.DBC_ACTION_CODE: action_code,
            libs.db.cfg.DBC_ACTION_TEXT: journal_action[7:],
            libs.db.cfg.DBC_DOCUMENT_ID: document_id,
            libs.db.cfg.DBC_DURATION_NS: duration_ns,
            libs.db.cfg.DBC_FUNCTION_NAME: function_name,
            libs.db.cfg.DBC_MODULE_NAME: module_name,
            libs.db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
        },
    )

    if journal_action[3:4] == "9":
        if libs.cfg.is_verbose:
            libs.cfg.logger.info(
                "Document: %6d - ActionCode: %s - ActionText: %s",
                libs.cfg.document_id,
                journal_action[0:7],
                journal_action[7:],
            )
        else:
            libs.cfg.logger.debug(
                "Document: %6d - ActionCode: %s - ActionText: %s",
                libs.cfg.document_id,
                journal_action[0:7],
                journal_action[7:],
            )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Load database data from a JSON file.
# -----------------------------------------------------------------------------
def load_db_data_from_json(initial_database_data: Path) -> None:
    """Load database data from a JSON file.

    Args:
        initial_database_data (Path): JSON file.
    """
    with open(initial_database_data, "r", encoding=libs.cfg.FILE_ENCODING_DEFAULT) as json_file:
        json_data = json.load(json_file)

        api_version = json_data[libs.db.cfg.JSON_NAME_API_VERSION]
        if api_version != libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]:
            libs.utils.terminate_fatal(
                f"Expected api version is {libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]} "
                + f"- got {api_version}"
            )

        data = json_data[libs.db.cfg.JSON_NAME_DATA]
        for json_table in data[libs.db.cfg.JSON_NAME_TABLES]:
            table_name = json_table[libs.db.cfg.JSON_NAME_TABLE_NAME].lower()

            if table_name not in ["language"]:
                if table_name in ["content", "document", "journal", "run", "version"]:
                    libs.utils.terminate_fatal(
                        "The database table '"
                        + table_name
                        + "' must not be changed via the JSON file."
                    )
                else:
                    libs.utils.terminate_fatal(
                        "The database table '" + table_name + "' does not exist in the database."
                    )

            for json_row in json_table[libs.db.cfg.JSON_NAME_ROWS]:
                db_columns = {}

                for json_column in json_row[libs.db.cfg.JSON_NAME_ROW]:
                    db_columns[json_column[libs.db.cfg.JSON_NAME_COLUMN_NAME]] = json_column[
                        libs.db.cfg.JSON_NAME_COLUMN_VALUE
                    ]

                insert_dbt_row(
                    table_name,
                    db_columns,
                )


# -----------------------------------------------------------------------------
# Prepare the database connection for normal users.
# -----------------------------------------------------------------------------
def prepare_connect_db() -> None:
    """Prepare the database connection for normal users."""
    libs.db.cfg.db_current_database = libs.cfg.config[libs.cfg.DCR_CFG_DB_DATABASE]
    libs.db.cfg.db_current_user = libs.cfg.config[libs.cfg.DCR_CFG_DB_USER]


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
    dbt = Table(
        libs.db.cfg.DBT_DOCUMENT,
        libs.db.cfg.db_orm_metadata,
        autoload_with=libs.db.cfg.db_orm_engine,
    )

    with libs.db.cfg.db_orm_engine.connect() as conn:
        row = conn.execute(
            #           select(dbt.c.file_name).where(
            select(dbt.c.file_name).where(
                and_(
                    dbt.c.id != document_id,
                    dbt.c.directory_type == libs.db.cfg.DOCUMENT_DIRECTORY_TYPE_INBOX,
                    dbt.c.sha256 == sha256,
                    dbt.c.status == libs.db.cfg.DOCUMENT_STATUS_END,
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
    dbt = Table(
        libs.db.cfg.DBT_RUN, libs.db.cfg.db_orm_metadata, autoload_with=libs.db.cfg.db_orm_engine
    )

    with libs.db.cfg.db_orm_engine.connect() as conn:
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
    dbt = Table(
        libs.db.cfg.DBT_VERSION,
        libs.db.cfg.db_orm_metadata,
        autoload_with=libs.db.cfg.db_orm_engine,
    )

    current_version: str = ""

    with libs.db.cfg.db_orm_engine.connect() as conn:
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

    dbt = Table(table_name, libs.db.cfg.db_orm_metadata, autoload_with=libs.db.cfg.db_orm_engine)

    with libs.db.cfg.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(update(dbt).where(dbt.c.id == id_where).values(columns))
        conn.close()

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

    dbt = Table(
        libs.db.cfg.DBT_VERSION,
        libs.db.cfg.db_orm_metadata,
        autoload_with=libs.db.cfg.db_orm_engine,
    )

    with libs.db.cfg.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(
            update(dbt).values(
                {
                    libs.db.cfg.DBC_VERSION: version,
                }
            )
        )
        conn.close()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
