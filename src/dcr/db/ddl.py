"""Module db.ddl: Database Definition Management."""
import json
import os
import pathlib
import typing

import cfg.glob
import comm.utils
import db.dml
import db.driver
import sqlalchemy
import sqlalchemy.event
import sqlalchemy.orm


# -----------------------------------------------------------------------------
# Create the trigger function.
# -----------------------------------------------------------------------------
def create_db_trigger_function(column_name: str) -> None:
    """Create the trigger function.

    Args:
        column_name (str): Column name.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.event.listen(
        cfg.glob.db_orm_metadata,
        "after_create",
        sqlalchemy.DDL(
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

    comm.utils.progress_msg(f"The trigger function 'function_{column_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the trigger for the database column created_at.
# -----------------------------------------------------------------------------
def create_db_trigger_created_at(table_name: str) -> None:
    """Create the trigger for the database column created_at.

    Args:
        table_name (str): Table name.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.event.listen(
        cfg.glob.db_orm_metadata,
        "after_create",
        sqlalchemy.DDL(
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

    comm.utils.progress_msg(f"The trigger 'trigger_created_at_{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the trigger for the database column modified_at.
# -----------------------------------------------------------------------------
def create_db_trigger_modified_at(table_name: str) -> None:
    """Create the trigger for the database column modified_at.

    Args:
        table_name (str): Table name.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.event.listen(
        cfg.glob.db_orm_metadata,
        "after_create",
        sqlalchemy.DDL(
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

    comm.utils.progress_msg(f"The trigger 'trigger_modified_at_{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the triggers for the database tables.
# -----------------------------------------------------------------------------
def create_db_triggers(table_names: typing.List[str]) -> None:
    """Create the triggers for the database tables.

    Args:
        table_names (List[str]): Table names.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    comm.utils.progress_msg("Create the database triggers ...")

    for column_name in [cfg.glob.DBC_CREATED_AT, cfg.glob.DBC_MODIFIED_AT]:
        create_db_trigger_function(column_name)

    for table_name in table_names:
        create_db_trigger_created_at(table_name)
        create_db_trigger_modified_at(table_name)

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table content_tetml_line.
# -----------------------------------------------------------------------------
def create_dbt_content_tetml_line(table_name: str) -> None:
    """Create the database table content_tetml_line.

    Args:
        table_name (str): Table name.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        cfg.glob.db_orm_metadata,
        sqlalchemy.Column(
            cfg.glob.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey(cfg.glob.DBT_DOCUMENT + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_PAGE_NO,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_PAGE_DATA,
            sqlalchemy.JSON,
            nullable=False,
        ),
    )

    comm.utils.progress_msg(f"The database table '{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table content_tetml_page.
# -----------------------------------------------------------------------------
def create_dbt_content_tetml_page(table_name: str) -> None:
    """Create the database table content_tetml_page.

    Args:
        table_name (str): Table name.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        cfg.glob.db_orm_metadata,
        sqlalchemy.Column(
            cfg.glob.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey(cfg.glob.DBT_DOCUMENT + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_PAGE_NO,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_PAGE_DATA,
            sqlalchemy.TEXT,
            nullable=False,
        ),
    )

    comm.utils.progress_msg(f"The database table '{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table content_tetml_word.
# -----------------------------------------------------------------------------
def create_dbt_content_tetml_word(table_name: str) -> None:
    """Create the database table content_tetml_word.

    Args:
        table_name (str): Table name.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        cfg.glob.db_orm_metadata,
        sqlalchemy.Column(
            cfg.glob.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey(cfg.glob.DBT_DOCUMENT + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_PAGE_NO,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_PAGE_DATA,
            sqlalchemy.JSON,
            nullable=False,
        ),
    )

    comm.utils.progress_msg(f"The database table '{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table content_token.
# -----------------------------------------------------------------------------
def create_dbt_content_token(table_name: str) -> None:
    """Create the database table content_token.

    Args:
        table_name (str): Table name.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        cfg.glob.db_orm_metadata,
        sqlalchemy.Column(
            cfg.glob.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_DOCUMENT_ID,
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey(cfg.glob.DBT_DOCUMENT + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_PAGE_NO,
            sqlalchemy.Integer,
            nullable=False,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_PAGE_DATA,
            sqlalchemy.JSON,
            nullable=False,
        ),
    )

    comm.utils.progress_msg(f"The database table '{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table document.
# -----------------------------------------------------------------------------
def create_dbt_document(table_name: str) -> None:
    """Create the database table document.

    Args:
        table_name (str): Table name.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        cfg.glob.db_orm_metadata,
        sqlalchemy.Column(
            cfg.glob.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_CHILD_NO,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(cfg.glob.DBC_CURRENT_STEP, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(cfg.glob.DBC_DIRECTORY_NAME, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(cfg.glob.DBC_DIRECTORY_TYPE, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(
            cfg.glob.DBC_DOCUMENT_ID_BASE,
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey(cfg.glob.DBT_DOCUMENT + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
            nullable=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_DOCUMENT_ID_PARENT,
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey(cfg.glob.DBT_DOCUMENT + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
            nullable=True,
        ),
        sqlalchemy.Column(cfg.glob.DBC_DURATION_NS, sqlalchemy.BigInteger, nullable=False),
        sqlalchemy.Column(cfg.glob.DBC_ERROR_CODE, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(cfg.glob.DBC_ERROR_NO, sqlalchemy.BigInteger, nullable=False),
        sqlalchemy.Column(cfg.glob.DBC_ERROR_MSG, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(cfg.glob.DBC_FILE_NAME, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(cfg.glob.DBC_FILE_SIZE_BYTES, sqlalchemy.Integer, nullable=True),
        sqlalchemy.Column(cfg.glob.DBC_FILE_TYPE, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(
            cfg.glob.DBC_LANGUAGE_ID,
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey(cfg.glob.DBT_LANGUAGE + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(cfg.glob.DBC_NEXT_STEP, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(cfg.glob.DBC_PDF_PAGES_NO, sqlalchemy.Integer, nullable=True),
        sqlalchemy.Column(
            cfg.glob.DBC_RUN_ID,
            sqlalchemy.Integer,
            sqlalchemy.ForeignKey(cfg.glob.DBT_RUN + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
            nullable=False,
        ),
        sqlalchemy.Column(cfg.glob.DBC_SHA256, sqlalchemy.String, nullable=True),
        sqlalchemy.Column(cfg.glob.DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(cfg.glob.DBC_STEM_NAME, sqlalchemy.String, nullable=True),
    )

    comm.utils.progress_msg(f"The database table '{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table language.
# -----------------------------------------------------------------------------
def create_dbt_language(table_name: str) -> None:
    """Create the database table language.

    Args:
        table_name (str): Table name.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        cfg.glob.db_orm_metadata,
        sqlalchemy.Column(
            cfg.glob.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(cfg.glob.DBC_ACTIVE, sqlalchemy.Boolean, default=True, nullable=False),
        sqlalchemy.Column(cfg.glob.DBC_CODE_ISO_639_3, sqlalchemy.String, nullable=False, unique=True),
        sqlalchemy.Column(cfg.glob.DBC_CODE_PANDOC, sqlalchemy.String, nullable=False, unique=True),
        sqlalchemy.Column(cfg.glob.DBC_CODE_SPACY, sqlalchemy.String, nullable=False, unique=True),
        sqlalchemy.Column(cfg.glob.DBC_CODE_TESSERACT, sqlalchemy.String, nullable=False, unique=True),
        sqlalchemy.Column(cfg.glob.DBC_DIRECTORY_NAME_INBOX, sqlalchemy.String, nullable=True, unique=True),
        sqlalchemy.Column(cfg.glob.DBC_ISO_LANGUAGE_NAME, sqlalchemy.String, nullable=False, unique=True),
    )

    comm.utils.progress_msg(f"The database table '{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database table run.
# -----------------------------------------------------------------------------
def create_dbt_run(table_name: str) -> None:
    """Create the database table run.

    Args:
        table_name (str): Table name.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        cfg.glob.db_orm_metadata,
        sqlalchemy.Column(
            cfg.glob.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(cfg.glob.DBC_ACTION, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(cfg.glob.DBC_RUN_ID, sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column(cfg.glob.DBC_STATUS, sqlalchemy.String, nullable=False),
        sqlalchemy.Column(
            cfg.glob.DBC_TOTAL_ERRONEOUS,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_TOTAL_OK_PROCESSED,
            sqlalchemy.Integer,
            nullable=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_TOTAL_TO_BE_PROCESSED,
            sqlalchemy.Integer,
            nullable=True,
        ),
    )

    comm.utils.progress_msg(f"The database table '{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    sqlalchemy.Table(
        table_name,
        cfg.glob.db_orm_metadata,
        sqlalchemy.Column(
            cfg.glob.DBC_ID,
            sqlalchemy.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_CREATED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(
            cfg.glob.DBC_MODIFIED_AT,
            sqlalchemy.DateTime,
        ),
        sqlalchemy.Column(cfg.glob.DBC_VERSION, sqlalchemy.String, nullable=False, unique=True),
    )

    comm.utils.progress_msg(f"The database table '{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database tables and triggers.
# -----------------------------------------------------------------------------
def create_schema() -> None:
    """Create the database tables and triggers."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    schema = cfg.glob.setup.db_schema

    db.driver.connect_db()

    cfg.glob.db_orm_engine.execute(sqlalchemy.schema.CreateSchema(schema))

    with cfg.glob.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(sqlalchemy.DDL(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))
        comm.utils.progress_msg(f"If existing, the schema '{schema}' has now been dropped")

        conn.execute(sqlalchemy.DDL(f"CREATE SCHEMA {schema}"))
        comm.utils.progress_msg(f"The schema '{schema}' has now been created")

        conn.execute(sqlalchemy.DDL(f"ALTER ROLE {cfg.glob.db_current_user} SET search_path = {schema}"))
        conn.execute(sqlalchemy.DDL(f"SET search_path = {schema}"))
        comm.utils.progress_msg(f"The search path '{schema}' has now been set")

        conn.close()

    create_dbt_language(cfg.glob.DBT_LANGUAGE)
    create_dbt_run(cfg.glob.DBT_RUN)
    create_dbt_version(cfg.glob.DBT_VERSION)
    # FK: language
    # FK: run
    create_dbt_document(cfg.glob.DBT_DOCUMENT)
    # FK: document
    create_dbt_content_tetml_line(cfg.glob.DBT_CONTENT_TETML_LINE)
    create_dbt_content_tetml_page(cfg.glob.DBT_CONTENT_TETML_PAGE)
    create_dbt_content_tetml_word(cfg.glob.DBT_CONTENT_TETML_WORD)
    create_dbt_content_token(cfg.glob.DBT_CONTENT_TOKEN)

    # Create the database triggers.
    create_db_triggers(
        [
            cfg.glob.DBT_CONTENT_TETML_LINE,
            cfg.glob.DBT_CONTENT_TETML_PAGE,
            cfg.glob.DBT_CONTENT_TETML_WORD,
            cfg.glob.DBT_CONTENT_TOKEN,
            cfg.glob.DBT_DOCUMENT,
            cfg.glob.DBT_LANGUAGE,
            cfg.glob.DBT_RUN,
            cfg.glob.DBT_VERSION,
        ],
    )

    cfg.glob.db_orm_metadata.create_all(cfg.glob.db_orm_engine)

    db.dml.insert_dbt_row(
        cfg.glob.DBT_LANGUAGE,
        {
            cfg.glob.DBC_CODE_ISO_639_3: "eng",
            cfg.glob.DBC_CODE_PANDOC: "en",
            cfg.glob.DBC_CODE_SPACY: "en_core_web_trf",
            cfg.glob.DBC_CODE_TESSERACT: "eng",
            cfg.glob.DBC_DIRECTORY_NAME_INBOX: cfg.glob.setup.directory_inbox,
            cfg.glob.DBC_ISO_LANGUAGE_NAME: "English",
        },
    )

    db.dml.insert_dbt_row(
        cfg.glob.DBT_VERSION,
        {
            cfg.glob.DBC_VERSION: cfg.glob.setup.dcr_version,
        },
    )

    if cfg.glob.setup.initial_database_data:
        initial_database_data_path = pathlib.Path(cfg.glob.setup.initial_database_data)
        if os.path.isfile(initial_database_data_path):
            load_db_data_from_json(initial_database_data_path)
        else:
            comm.utils.terminate_fatal(
                f"File with initial database data is missing - " f"file name '{cfg.glob.setup.initial_database_data}'"
            )

    # Disconnect from the database.
    db.driver.disconnect_db()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Load database data from a JSON file.
# -----------------------------------------------------------------------------
def load_db_data_from_json(initial_database_data: pathlib.Path) -> None:
    """Load database data from a JSON file.

    Args:
        initial_database_data (Path): JSON file.
    """
    with open(initial_database_data, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as json_file:
        json_data = json.load(json_file)

        api_version = json_data[cfg.glob.JSON_NAME_API_VERSION]
        if api_version != cfg.glob.setup.dcr_version:
            comm.utils.terminate_fatal(
                f"Expected api version is' {cfg.glob.setup.dcr_version}' " f"- got '{api_version}'"
            )

        data = json_data[cfg.glob.JSON_NAME_DATA]
        for json_table in data[cfg.glob.JSON_NAME_TABLES]:
            table_name = json_table[cfg.glob.JSON_NAME_TABLE_NAME].lower()

            if table_name not in ["language"]:
                if table_name in [
                    "content_tetml_line",
                    "content_tetml_page",
                    "content_tetml_word",
                    "content_token",
                    "document",
                    "run",
                    "version",
                ]:
                    comm.utils.terminate_fatal(
                        f"The database table '{table_name}' must not be changed via the JSON file."
                    )
                else:
                    comm.utils.terminate_fatal(f"The database table '{table_name}' does not exist in the database.")

            for json_row in json_table[cfg.glob.JSON_NAME_ROWS]:
                db_columns = {}

                for json_column in json_row[cfg.glob.JSON_NAME_ROW]:
                    db_columns[json_column[cfg.glob.JSON_NAME_COLUMN_NAME]] = json_column[
                        cfg.glob.JSON_NAME_COLUMN_VALUE
                    ]

                db.dml.insert_dbt_row(
                    table_name,
                    db_columns,
                )
