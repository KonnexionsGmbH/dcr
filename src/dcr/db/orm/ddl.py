"""Module db.orm.ddl: Database Definition Management."""
import json
import os
from pathlib import Path
from typing import List

import db.cfg
import db.orm.connection
import db.orm.dml
import libs.cfg
import libs.utils
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import DDL
from sqlalchemy import ForeignKey
from sqlalchemy import event


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
        db.cfg.db_orm_metadata,
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

    libs.utils.progress_msg(f"The trigger function 'function_{column_name}' has now been created")

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
        db.cfg.db_orm_metadata,
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

    libs.utils.progress_msg(f"The trigger 'trigger_created_at_{table_name}' has now been created")

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
        db.cfg.db_orm_metadata,
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

    libs.utils.progress_msg(f"The trigger 'trigger_modified_at_{table_name}' has now been created")

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

    for column_name in [db.cfg.DBC_CREATED_AT, db.cfg.DBC_MODIFIED_AT]:
        create_db_trigger_function(column_name)

    for table_name in table_names:
        create_db_trigger_created_at(table_name)
        create_db_trigger_modified_at(table_name)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table content_tetml_page.
# -----------------------------------------------------------------------------
def create_dbt_content_tetml_page(table_name: str) -> None:
    """Create the database table content_tetml_page.

    Args:
        table_name (str): Table name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            ForeignKey(db.cfg.DBT_DOCUMENT + "." + db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_PAGE_NO,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_PAGE_TEXT,
            sqlalchemy.TEXT,
            nullable=False,
        ),
    )

    libs.utils.progress_msg(f"The database table '{table_name}' has now been created")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table content_tetml_word.
# -----------------------------------------------------------------------------
def create_dbt_content_tetml_word(table_name: str) -> None:
    """Create the database table content_tetml_word.

    Args:
        table_name (str): Table name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            ForeignKey(db.cfg.DBT_DOCUMENT + "." + db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_LINE_IN_PARA_END,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_LINE_IN_PARA_START,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_PAGE_IN_DOC_END,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_PAGE_IN_DOC_START,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_PARA_IN_PAGE_END,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_PARA_IN_PAGE_START,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_SENTENCE,
            sqlalchemy.JSON,
            nullable=False,
        ),
    )

    libs.utils.progress_msg(f"The database table '{table_name}' has now been created")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table content_token.
# -----------------------------------------------------------------------------
def create_dbt_content_token(table_name: str) -> None:
    """Create the database table content_token.

    Args:
        table_name (str): Table name.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            ForeignKey(db.cfg.DBT_DOCUMENT + "." + db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_PAGE_NO,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_TOKEN,
            sqlalchemy.JSON,
            nullable=False,
        ),
    )

    libs.utils.progress_msg(f"The database table '{table_name}' has now been created")

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
        db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_CHILD_NO,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(db.cfg.DBC_CURRENT_STEP, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(db.cfg.DBC_DIRECTORY_NAME, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(db.cfg.DBC_DIRECTORY_TYPE, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(
            db.cfg.DBC_DOCUMENT_ID_BASE,
            sqlalchemy.Integer,
            ForeignKey(db.cfg.DBT_DOCUMENT + "." + db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=True,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_DOCUMENT_ID_PARENT,
            sqlalchemy.Integer,
            ForeignKey(db.cfg.DBT_DOCUMENT + "." + db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=True,
        ),
        sqlalchemy.Column(db.cfg.DBC_DURATION_NS, sqlalchemy.BigInteger, nullable=False),
        sqlalchemy.Column(db.cfg.DBC_ERROR_CODE, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(db.cfg.DBC_ERROR_NO, sqlalchemy.BigInteger, nullable=False),
        sqlalchemy.Column(db.cfg.DBC_ERROR_MSG, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(db.cfg.DBC_FILE_NAME, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(db.cfg.DBC_FILE_SIZE_BYTES, sqlalchemy.Integer, nullable=True),
        sqlalchemy.Column(db.cfg.DBC_FILE_TYPE, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(
            db.cfg.DBC_LANGUAGE_ID,
            sqlalchemy.Integer,
            ForeignKey(db.cfg.DBT_LANGUAGE + "." + db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(db.cfg.DBC_NEXT_STEP, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(db.cfg.DBC_PDF_PAGES_NO, sqlalchemy.Integer, nullable=True),
        sqlalchemy.Column(
            db.cfg.DBC_RUN_ID,
            sqlalchemy.Integer,
            ForeignKey(db.cfg.DBT_RUN + "." + db.cfg.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(db.cfg.DBC_SHA256, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(db.cfg.DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(db.cfg.DBC_STEM_NAME, sqlalchemy.String, nullable=True),
    )

    libs.utils.progress_msg(f"The database table '{table_name}' has now been created")

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
        db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(db.cfg.DBC_ACTIVE, sqlalchemy.Boolean, default=True, nullable=False),
        sqlalchemy.Column(
            db.cfg.DBC_CODE_ISO_639_3, sqlalchemy.String, nullable=False, unique=True
        ),
        sqlalchemy.Column(db.cfg.DBC_CODE_PANDOC, sqlalchemy.String, nullable=False, unique=True),
        sqlalchemy.Column(db.cfg.DBC_CODE_SPACY, sqlalchemy.String, nullable=False, unique=True),
        sqlalchemy.Column(
            db.cfg.DBC_CODE_TESSERACT, sqlalchemy.String, nullable=False, unique=True
        ),
        sqlalchemy.Column(
            db.cfg.DBC_DIRECTORY_NAME_INBOX, sqlalchemy.String, nullable=True, unique=True
        ),
        sqlalchemy.Column(
            db.cfg.DBC_ISO_LANGUAGE_NAME, sqlalchemy.String, nullable=False, unique=True
        ),
    )

    libs.utils.progress_msg(f"The database table '{table_name}' has now been created")

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
        db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(db.cfg.DBC_ACTION, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(db.cfg.DBC_RUN_ID, sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column(db.cfg.DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            db.cfg.DBC_TOTAL_ERRONEOUS,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_TOTAL_OK_PROCESSED,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_TOTAL_TO_BE_PROCESSED,
            sqlalchemy.Integer,
            nullable=True,
        ),
    )

    libs.utils.progress_msg(f"The database table '{table_name}' has now been created")

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
        db.cfg.db_orm_metadata,
        sqlalchemy.Column(
            db.cfg.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            db.cfg.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(db.cfg.DBC_VERSION, sqlalchemy.String, nullable=False, unique=True),
    )

    libs.utils.progress_msg(f"The database table '{table_name}' has now been created")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database tables and triggers.
# -----------------------------------------------------------------------------
def create_schema() -> None:
    """Create the database tables and triggers."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    schema = libs.cfg.config[libs.cfg.DCR_CFG_DB_SCHEMA]

    db.orm.connection.connect_db()

    db.cfg.db_orm_engine.execute(sqlalchemy.schema.CreateSchema(schema))

    with db.cfg.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(DDL(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))
        libs.utils.progress_msg(f"If existing, the schema '{schema}' has now been dropped")

        conn.execute(DDL(f"CREATE SCHEMA {schema}"))
        libs.utils.progress_msg(f"The schema '{schema}' has now been created")

        conn.execute(DDL(f"ALTER ROLE {db.cfg.db_current_user} SET search_path = {schema}"))
        conn.execute(DDL(f"SET search_path = {schema}"))
        libs.utils.progress_msg(f"The search path '{schema}' has now been set")

        conn.close()

    create_dbt_language(db.cfg.DBT_LANGUAGE)
    create_dbt_run(db.cfg.DBT_RUN)
    create_dbt_version(db.cfg.DBT_VERSION)
    # FK: language
    # FK: run
    create_dbt_document(db.cfg.DBT_DOCUMENT)
    # FK: document
    create_dbt_content_tetml_page(db.cfg.DBT_CONTENT_TETML_PAGE)
    create_dbt_content_tetml_word(db.cfg.DBT_CONTENT_TETML_WORD)
    create_dbt_content_token(db.cfg.DBT_CONTENT_TOKEN)

    # Create the database triggers.
    create_db_triggers(
        [
            db.cfg.DBT_CONTENT_TETML_PAGE,
            db.cfg.DBT_CONTENT_TETML_WORD,
            db.cfg.DBT_CONTENT_TOKEN,
            db.cfg.DBT_DOCUMENT,
            db.cfg.DBT_LANGUAGE,
            db.cfg.DBT_RUN,
            db.cfg.DBT_VERSION,
        ],
    )

    db.cfg.db_orm_metadata.create_all(db.cfg.db_orm_engine)

    db.orm.dml.insert_dbt_row(
        db.cfg.DBT_LANGUAGE,
        {
            db.cfg.DBC_CODE_ISO_639_3: "eng",
            db.cfg.DBC_CODE_PANDOC: "en",
            db.cfg.DBC_CODE_SPACY: "en_core_web_trf",
            db.cfg.DBC_CODE_TESSERACT: "eng",
            db.cfg.DBC_DIRECTORY_NAME_INBOX: str(libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]),
            db.cfg.DBC_ISO_LANGUAGE_NAME: "English",
        },
    )

    db.orm.dml.insert_dbt_row(
        db.cfg.DBT_VERSION,
        {
            db.cfg.DBC_VERSION: libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION],
        },
    )

    if libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]:
        initial_database_data_path = Path(libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA])
        if os.path.isfile(initial_database_data_path):
            load_db_data_from_json(initial_database_data_path)
        else:
            libs.utils.terminate_fatal(
                f"File with initial database data is missing - "
                f"file name '{libs.cfg.config[libs.cfg.DCR_CFG_INITIAL_DATABASE_DATA]}'"
            )

    # Disconnect from the database.
    db.orm.connection.disconnect_db()

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

        api_version = json_data[db.cfg.JSON_NAME_API_VERSION]
        if api_version != libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]:
            libs.utils.terminate_fatal(
                f"Expected api version is' {libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]}' "
                f"- got '{api_version}'"
            )

        data = json_data[db.cfg.JSON_NAME_DATA]
        for json_table in data[db.cfg.JSON_NAME_TABLES]:
            table_name = json_table[db.cfg.JSON_NAME_TABLE_NAME].lower()

            if table_name not in ["language"]:
                if table_name in [
                    "content_tetml_page",
                    "content_tetml_word",
                    "content_token",
                    "document",
                    "run",
                    "version",
                ]:
                    libs.utils.terminate_fatal(
                        f"The database table '{table_name}' must not be changed via the JSON file."
                    )
                else:
                    libs.utils.terminate_fatal(
                        f"The database table '{table_name}' does not exist in the database."
                    )

            for json_row in json_table[db.cfg.JSON_NAME_ROWS]:
                db_columns = {}

                for json_column in json_row[db.cfg.JSON_NAME_ROW]:
                    db_columns[json_column[db.cfg.JSON_NAME_COLUMN_NAME]] = json_column[
                        db.cfg.JSON_NAME_COLUMN_VALUE
                    ]

                db.orm.dml.insert_dbt_row(
                    table_name,
                    db_columns,
                )
