"""Module db.ddl: Database Definition Management."""
import os
import pathlib
from typing import List

import cfg.glob
import db.cls_action
import db.cls_base
import db.cls_language
import db.cls_run
import db.cls_token
import db.cls_version
import db.dml
import db.driver
import sqlalchemy
import sqlalchemy.event
import sqlalchemy.orm
import utils


# -----------------------------------------------------------------------------
# Create the trigger function.
# -----------------------------------------------------------------------------
# pylint: disable=R0801
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

    utils.progress_msg(f"The trigger function 'function_{column_name}' has now been created")

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

    utils.progress_msg(f"The trigger 'trigger_created_at_{table_name}' has now been created")

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

    utils.progress_msg(f"The trigger 'trigger_modified_at_{table_name}' has now been created")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the triggers for the database tables.
# -----------------------------------------------------------------------------
def create_db_triggers(table_names: List[str]) -> None:
    """Create the triggers for the database tables.

    Args:
        table_names (List[str]): Table names.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    utils.progress_msg("Create the database triggers ...")

    for column_name in [cfg.glob.DBC_CREATED_AT, cfg.glob.DBC_MODIFIED_AT]:
        create_db_trigger_function(column_name)

    for table_name in table_names:
        create_db_trigger_created_at(table_name)
        create_db_trigger_modified_at(table_name)

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
        utils.progress_msg(f"If existing, the schema '{schema}' has now been dropped")

        conn.execute(sqlalchemy.DDL(f"CREATE SCHEMA {schema}"))
        utils.progress_msg(f"The schema '{schema}' has now been created")

        conn.execute(sqlalchemy.DDL(f"ALTER ROLE {cfg.glob.db_current_user} SET search_path = {schema}"))
        conn.execute(sqlalchemy.DDL(f"SET search_path = {schema}"))
        utils.progress_msg(f"The search path '{schema}' has now been set")

        conn.close()

    db.cls_language.Language.create_dbt()
    db.cls_run.Run.create_dbt()
    db.cls_version.Version.create_dbt()
    # FK: language
    db.cls_base.Base.create_dbt()
    # FK: run
    db.cls_action.Action.create_dbt()
    # FK: document
    db.cls_token.Token.create_dbt()

    # Create the database triggers.
    create_db_triggers(
        [
            cfg.glob.DBT_ACTION,
            cfg.glob.DBT_BASE,
            cfg.glob.DBT_LANGUAGE,
            cfg.glob.DBT_RUN,
            cfg.glob.DBT_TOKEN,
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
        initial_database_data_path = utils.get_os_independent_name(cfg.glob.setup.initial_database_data)
        if os.path.isfile(initial_database_data_path):
            db.dml.load_db_data_from_json(initial_database_data_path)
        else:
            utils.terminate_fatal(
                f"File with initial database data is missing - " f"file name '{cfg.glob.setup.initial_database_data}'"
            )

    # Disconnect from the database.
    db.driver.disconnect_db()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
