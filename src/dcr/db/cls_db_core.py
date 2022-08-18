# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module dcr.db.cls_vdb_core: Managing the database."""
from __future__ import annotations

import json
import os
import pathlib
from typing import ClassVar
from typing import TypeAlias

import dcr_core.cls_nlp_core
import dcr_core.cls_setup
import dcr_core.core_glob
import dcr_core.core_utils
import psycopg2
import psycopg2.errors
import psycopg2.extensions
import sqlalchemy
import sqlalchemy.event
import sqlalchemy.exc
import sqlalchemy.orm
import sqlalchemy.pool
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

import dcr.cfg.cls_setup

# -----------------------------------------------------------------------------
# Type declaration.
# -----------------------------------------------------------------------------
Columns: TypeAlias = dict[str, bool | float | int | None | os.PathLike[str] | str]

ColumnValues: TypeAlias = tuple[bool | float | int | None | os.PathLike[str] | str]


class DBCore:
    """Managing the database.

    Returns:
        _type_: Version instance.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    DB_DIALECT_POSTGRESQL: ClassVar[str] = "postgresql"

    DBC_ACTION_CODE: ClassVar[str] = "action_code"
    DBC_ACTION_CODE_LAST: ClassVar[str] = "action_code_last"
    DBC_ACTION_TEXT: ClassVar[str] = "action_text"
    DBC_ACTION_TEXT_LAST: ClassVar[str] = "action_text_last"
    DBC_ACTIVE: ClassVar[str] = "active"
    DBC_CODE_ISO_639_3: ClassVar[str] = "code_iso_639_3"
    DBC_CODE_ISO_639_3_DEFAULT: ClassVar[str] = "eng"
    DBC_CODE_PANDOC: ClassVar[str] = "code_pandoc"
    DBC_CODE_PANDOC_DEFAULT: ClassVar[str] = "en"
    DBC_CODE_SPACY: ClassVar[str] = "code_spacy"
    DBC_CODE_TESSERACT: ClassVar[str] = "code_tesseract"
    DBC_CODE_TESSERACT_DEFAULT: ClassVar[str] = "eng"
    DBC_COLUMN_NO: ClassVar[str] = "column_no"
    DBC_COLUMN_SPAN: ClassVar[str] = "column_span"
    DBC_COORD_LLX: ClassVar[str] = "coord_llx"
    DBC_COORD_URX: ClassVar[str] = "coord_urx"
    DBC_CREATED_AT: ClassVar[str] = "created_at"
    DBC_DIRECTORY_NAME: ClassVar[str] = "directory_name"
    DBC_DIRECTORY_NAME_INBOX: ClassVar[str] = "directory_name_inbox"
    DBC_DIRECTORY_TYPE: ClassVar[str] = "directory_type"
    DBC_DURATION_NS: ClassVar[str] = "duration_ns"
    DBC_ERROR_CODE: ClassVar[str] = "error_code"
    DBC_ERROR_CODE_LAST: ClassVar[str] = "error_code_last"
    DBC_ERROR_MSG: ClassVar[str] = "error_msg"
    DBC_ERROR_MSG_LAST: ClassVar[str] = "error_msg_last"
    DBC_ERROR_NO: ClassVar[str] = "error_no"
    DBC_FILE_NAME: ClassVar[str] = "file_name"
    DBC_FILE_SIZE_BYTES: ClassVar[str] = "file_size_bytes"
    DBC_ID: ClassVar[str] = "id"
    DBC_ID_DOCUMENT: ClassVar[str] = "id_document"
    DBC_ID_LANGUAGE: ClassVar[str] = "id_language"
    DBC_ID_PARENT: ClassVar[str] = "id_parent"
    DBC_ID_RUN: ClassVar[str] = "id_run"
    DBC_ID_RUN_LAST: ClassVar[str] = "id_run_last"
    DBC_ISO_LANGUAGE_NAME: ClassVar[str] = "iso_language_name"
    DBC_ISO_LANGUAGE_NAME_DEFAULT: ClassVar[str] = "English"
    DBC_LINE_TYPE: ClassVar[str] = "line_type"
    DBC_MODIFIED_AT: ClassVar[str] = "modified_at"
    DBC_NO_CHILDREN: ClassVar[str] = "no_children"
    DBC_NO_LINES_FOOTER: ClassVar[str] = "no_lines_footer"
    DBC_NO_LINES_HEADER: ClassVar[str] = "no_lines_header"
    DBC_NO_LINES_TOC: ClassVar[str] = "no_lines_toc"
    DBC_NO_LISTS_BULLET: ClassVar[str] = "no_lists_bullet"
    DBC_NO_LISTS_NUMBER: ClassVar[str] = "no_lists_number"
    DBC_NO_PDF_PAGES: ClassVar[str] = "no_pdf_pages"
    DBC_NO_TABLES: ClassVar[str] = "no_tables"
    DBC_NO_TOKENS_IN_SENT: ClassVar[str] = "no_tokens_in_sent"
    DBC_PAGE_DATA: ClassVar[str] = "page_data"
    DBC_PAGE_NO: ClassVar[str] = "page_no"
    DBC_PARA_NO: ClassVar[str] = "para_no"
    DBC_ROW_NO: ClassVar[str] = "row_no"
    DBC_SENT_NO: ClassVar[str] = "sent_no"
    DBC_SHA256: ClassVar[str] = "sha256"
    DBC_STATUS: ClassVar[str] = "status"
    DBC_TEXT: ClassVar[str] = "text"
    DBC_TOKENS: ClassVar[str] = "tokens"
    DBC_TOTAL_ERRONEOUS: ClassVar[str] = "total_erroneous"
    DBC_TOTAL_PROCESSED_OK: ClassVar[str] = "total_processed_ok"
    DBC_TOTAL_PROCESSED_TO_BE: ClassVar[str] = "total_processed_to_be"
    DBC_VERSION: ClassVar[str] = "version"

    DBT_ACTION: ClassVar[str] = "action"
    DBT_DOCUMENT: ClassVar[str] = "document"
    DBT_LANGUAGE: ClassVar[str] = "language"
    DBT_RUN: ClassVar[str] = "run"
    DBT_TOKEN: ClassVar[str] = "token"
    DBT_VERSION: ClassVar[str] = "version"

    JSON_NAME_API_VERSION = "apiVersion"
    JSON_NAME_COLUMN_NAME = "columnName"
    JSON_NAME_COLUMN_VALUE = "columnValue"
    JSON_NAME_DATA = "data"
    JSON_NAME_ROW = "row"
    JSON_NAME_ROWS = "rows"
    JSON_NAME_TABLES = "tables"
    JSON_NAME_TABLE_NAME = "tableName"

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(
        self,
        is_admin: bool = False,
    ) -> None:
        """Initialise the instance.

        Args:
            is_admin (bool, optional):
                    Administrator access. Defaults to False.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        dcr_core.core_utils.check_exists_object(
            is_setup=True,
        )

        self._db_current_database = ""
        self._db_current_password = ""  # nosec
        self._db_current_user = ""

        if is_admin:
            self._db_driver_conn = self._connect_db_admin()
        else:
            (self.db_orm_engine, self.db_orm_metadata) = self._connect_db_user()

        dcr.utils.progress_msg_connected(database=self._db_current_database, user=self._db_current_user)

        self._exist = True

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Create a database connection for the database administrator.
    # -----------------------------------------------------------------------------
    def _connect_db_admin(self) -> psycopg2.extensions.connection:
        """Create a database connection for the database administrator.

        Returns:
            psycopg2.connection: Database connection.
        """
        dcr.cfg.glob.logger.debug("Attempting to connect to a administration  database")

        self._db_current_database = dcr_core.core_glob.setup.db_database_admin
        self._db_current_password = dcr_core.core_glob.setup.db_password_admin
        self._db_current_user = dcr_core.core_glob.setup.db_user_admin

        self._show_connection_details()

        try:
            self._db_driver_conn = psycopg2.connect(
                dbname=self._db_current_database,
                host=dcr_core.core_glob.setup.db_host,
                password=self._db_current_password,
                port=dcr_core.core_glob.setup.db_connection_port,
                user=self._db_current_user,
            )
        except psycopg2.OperationalError as err:
            dcr_core.core_utils.terminate_fatal(
                f"There is no database connection for the administrator possible - error={str(err)}",
            )

        self._db_driver_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        dcr.cfg.glob.logger.debug("The database engine is ready for the administrator")

        return self._db_driver_conn

    # -----------------------------------------------------------------------------
    # Create a database connection for a database user.
    # -----------------------------------------------------------------------------
    def _connect_db_user(self) -> tuple[Engine, MetaData]:
        """Create a database connection for a database user.

        Returns:
            tuple[Engine,MetaData]: Database engine and metadata
        """
        dcr.cfg.glob.logger.debug("Attempting to connect to a user database")

        self._db_current_database = dcr_core.core_glob.setup.db_database
        self._db_current_password = dcr_core.core_glob.setup.db_password
        self._db_current_user = dcr_core.core_glob.setup.db_user

        self._show_connection_details()

        self.db_orm_engine = sqlalchemy.create_engine(
            dcr_core.core_glob.setup.db_connection_prefix
            + dcr_core.core_glob.setup.db_host
            + ":"
            + str(dcr_core.core_glob.setup.db_connection_port)
            + "/"
            + self._db_current_database
            + "?user="
            + self._db_current_user
            + "&password="
            + self._db_current_password,
            poolclass=sqlalchemy.pool.NullPool,
        )

        try:
            conn = self.db_orm_engine.connect()
            conn.close()
        except sqlalchemy.exc.OperationalError as err:
            dcr_core.core_utils.terminate_fatal(
                f"No database connection possible - error={str(err)}",
            )

        dcr.cfg.glob.logger.debug("The database engine is ready for the user")

        self.db_orm_metadata = sqlalchemy.MetaData()
        self.db_orm_metadata.bind = self.db_orm_engine

        dcr.cfg.glob.logger.debug("Database metadata are ready")

        return self.db_orm_engine, self.db_orm_metadata

    # -----------------------------------------------------------------------------
    # Create the PostgreSQL database.
    # -----------------------------------------------------------------------------
    def _create_database_postgresql(self) -> None:
        """Create the database tables."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        self._drop_database_postgresql()

        database = dcr_core.core_glob.setup.db_database
        password = dcr_core.core_glob.setup.db_password
        user = dcr_core.core_glob.setup.db_user

        self._db_driver_conn.cursor().execute("CREATE USER " + user + " WITH ENCRYPTED PASSWORD '" + password + "'")
        dcr.utils.progress_msg(f"The user '{user}' has now been created")

        self._db_driver_conn.cursor().execute("CREATE DATABASE " + database + " WITH OWNER " + user)
        dcr.utils.progress_msg(f"The database '{database}' has now been created")

        self._db_driver_conn.cursor().execute("GRANT ALL PRIVILEGES ON DATABASE " + database + " TO " + user)
        dcr.utils.progress_msg(f"The user '{user}' has now all privileges on database '{database}'")

        self._db_driver_conn.close()

        self._create_schema()

        dcr.utils.progress_msg(f"The database has been successfully created, " f"version number='{dcr_core.cls_setup.Setup.DCR_VERSION}'")

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Create the trigger function.
    # -----------------------------------------------------------------------------
    # pylint: disable=duplicate-code
    def _create_db_trigger_function(self, column_name: str) -> None:
        """Create the trigger function.

        Args:
            column_name (str): Column name.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        sqlalchemy.event.listen(
            self.db_orm_metadata,
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

        dcr.utils.progress_msg(f"The trigger function 'function_{column_name}' has now been created")

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Create the trigger for the database column created_at.
    # -----------------------------------------------------------------------------
    def _create_db_trigger_created_at(self, table_name: str) -> None:
        """Create the trigger for the database column created_at.

        Args:
            table_name (str): Table name.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        sqlalchemy.event.listen(
            self.db_orm_metadata,
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

        dcr.utils.progress_msg(f"The trigger 'trigger_created_at_{table_name}' has now been created")

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Create the trigger for the database column modified_at.
    # -----------------------------------------------------------------------------
    def _create_db_trigger_modified_at(self, table_name: str) -> None:
        """Create the trigger for the database column modified_at.

        Args:
            table_name (str): Table name.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        sqlalchemy.event.listen(
            self.db_orm_metadata,
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

        dcr.utils.progress_msg(f"The trigger 'trigger_modified_at_{table_name}' has now been created")

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Create the triggers for the database tables.
    # -----------------------------------------------------------------------------
    def _create_db_triggers(self, table_names: list[str]) -> None:
        """Create the triggers for the database tables.

        Args:
            table_names (list[str]): Table names.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        dcr.utils.progress_msg("Create the database triggers ...")

        for column_name in (DBCore.DBC_CREATED_AT, DBCore.DBC_MODIFIED_AT):
            self._create_db_trigger_function(column_name)

        for table_name in table_names:
            self._create_db_trigger_created_at(table_name)
            self._create_db_trigger_modified_at(table_name)

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Create the database tables and triggers.
    # -----------------------------------------------------------------------------
    def _create_schema(self) -> None:
        """Create the database tables and triggers."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        self._connect_db_user()

        schema = dcr_core.core_glob.setup.db_schema

        self.db_orm_engine.execute(sqlalchemy.schema.CreateSchema(schema))

        with self.db_orm_engine.connect().execution_options(autocommit=True) as conn:
            conn.execute(sqlalchemy.DDL(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))
            dcr.utils.progress_msg(f"If existing, the schema '{schema}' has now been dropped")

            conn.execute(sqlalchemy.DDL(f"CREATE SCHEMA {schema}"))
            dcr.utils.progress_msg(f"The schema '{schema}' has now been created")

            conn.execute(sqlalchemy.DDL(f"ALTER ROLE {self._db_current_user} SET search_path = {schema}"))
            conn.execute(sqlalchemy.DDL(f"SET search_path = {schema}"))
            dcr.utils.progress_msg(f"The search path '{schema}' has now been set")

            conn.close()

        dcr.db.cls_language.Language.create_dbt()
        dcr.db.cls_run.Run.create_dbt()
        dcr.db.cls_version.Version.create_dbt()
        # FK: language
        dcr.db.cls_document.Document.create_dbt()
        # FK: run
        dcr.db.cls_action.Action.create_dbt()
        # FK: document
        dcr.db.cls_token.Token.create_dbt()

        # Create the database triggers.
        self._create_db_triggers(
            [
                DBCore.DBT_ACTION,
                DBCore.DBT_DOCUMENT,
                DBCore.DBT_LANGUAGE,
                DBCore.DBT_RUN,
                DBCore.DBT_TOKEN,
                DBCore.DBT_VERSION,
            ],
        )

        self.db_orm_metadata.create_all(self.db_orm_engine)

        self.insert_dbt_row(
            DBCore.DBT_LANGUAGE,
            {
                DBCore.DBC_CODE_ISO_639_3: DBCore.DBC_CODE_ISO_639_3_DEFAULT,
                DBCore.DBC_CODE_PANDOC: DBCore.DBC_CODE_PANDOC_DEFAULT,
                DBCore.DBC_CODE_SPACY: dcr_core.cls_nlp_core.NLPCore.CODE_SPACY_DEFAULT,
                DBCore.DBC_CODE_TESSERACT: DBCore.DBC_CODE_TESSERACT_DEFAULT,
                DBCore.DBC_DIRECTORY_NAME_INBOX: dcr_core.core_glob.setup.directory_inbox,
                DBCore.DBC_ISO_LANGUAGE_NAME: DBCore.DBC_ISO_LANGUAGE_NAME_DEFAULT,
            },
        )

        self.insert_dbt_row(
            DBCore.DBT_VERSION,
            {
                DBCore.DBC_VERSION: dcr_core.cls_setup.Setup.DCR_VERSION,
            },
        )

        if dcr_core.core_glob.setup.db_initial_data_file:
            db_initial_data_file_path = dcr_core.core_utils.get_os_independent_name(dcr_core.core_glob.setup.db_initial_data_file)
            if os.path.isfile(db_initial_data_file_path):
                self.load_db_data_from_json(pathlib.Path(db_initial_data_file_path))
                dcr.utils.progress_msg(
                    "Initial database data was successfully loaded from the " f"file {dcr_core.core_glob.setup.db_initial_data_file}"
                )
            else:
                dcr_core.core_utils.terminate_fatal(
                    "File with initial database data is missing - " f"file name '{dcr_core.core_glob.setup.db_initial_data_file}'"
                )

        # Disconnect from the database.
        self.disconnect_db()

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Drop the database.
    # -----------------------------------------------------------------------------
    def _drop_database(self) -> None:
        """Drop the database."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        if dcr_core.core_glob.setup.db_dialect == DBCore.DB_DIALECT_POSTGRESQL:
            self._drop_database_postgresql()
        else:
            dcr_core.core_utils.terminate_fatal(f"A database dialect '{dcr_core.core_glob.setup.db_dialect}' " f"is not supported in DCR")

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Drop the PostgreSQL database.
    # -----------------------------------------------------------------------------
    def _drop_database_postgresql(self) -> None:
        """Drop the PostgreSQL database."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        database = dcr_core.core_glob.setup.db_database
        user = dcr_core.core_glob.setup.db_user

        try:
            self._db_driver_conn.cursor().execute("DROP DATABASE IF EXISTS " + database)
            dcr.utils.progress_msg(f"If existing, the database '{database}' has now been dropped")
        except AttributeError:
            pass
        except psycopg2.errors.InterfaceError:  # pylint: disable=no-member
            pass
        # not testable
        except psycopg2.errors.ObjectInUse as err:  # pylint: disable=no-member
            dcr_core.core_utils.terminate_fatal(
                f"The database can currently not be dropped - error={str(err)}",
            )

        try:
            self._db_driver_conn.cursor().execute("DROP USER IF EXISTS " + user)
            dcr.utils.progress_msg(f"If existing, the user '{user}' has now been dropped")
        except psycopg2.errors.InterfaceError:  # pylint: disable=no-member
            pass
        except AttributeError:
            pass

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Show the details of the projected database connection.
    # -----------------------------------------------------------------------------
    def _show_connection_details(self) -> None:
        """Show the details of the projected database connection."""
        dcr.cfg.glob.logger.debug("Database connection parameter: host:    '%s'", dcr_core.core_glob.setup.db_host)
        dcr.cfg.glob.logger.debug("Database connection parameter: port:    '%s'", dcr_core.core_glob.setup.db_connection_port)
        dcr.cfg.glob.logger.debug("Database connection parameter: database '%s'", self._db_current_database)
        dcr.cfg.glob.logger.debug("Database connection parameter: user     '%s'", self._db_current_user)

        if dcr_core.core_glob.setup.environment_variant in [
            dcr_core.cls_setup.Setup.ENVIRONMENT_TYPE_DEV,
            dcr_core.cls_setup.Setup.ENVIRONMENT_TYPE_TEST,
        ]:
            dcr.cfg.glob.logger.debug("Database connection parameter: password '%s'", self._db_current_password)

    # -----------------------------------------------------------------------------
    # Upgrade the current database schema - from one version to the next.
    # -----------------------------------------------------------------------------
    def _upgrade_database_version(self) -> None:
        """Upgrade the current database schema - from one version to the next."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        if (current_version := dcr.db.cls_version.Version.select_version_version_unique()) < "1.0.0":
            dcr_core.core_utils.terminate_fatal("An automatic upgrade of the database version is only " + "supported from version 1.0.0.")

        # not testable
        self._connect_db_admin()

        # TBD: Template for migration from version 1.0.0 to version x.x.x
        # if current_version == "0.5.0":
        #     _upgrade_database_version_0_5_0()
        #     return

        dcr_core.core_utils.terminate_fatal(
            "Database file has the wrong version, version number=" + current_version,
        )

    # -----------------------------------------------------------------------------
    # Create the database.
    # -----------------------------------------------------------------------------
    def create_database(self) -> None:
        """Create the database."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        if dcr_core.core_glob.setup.db_dialect == DBCore.DB_DIALECT_POSTGRESQL:
            self._create_database_postgresql()
        else:
            dcr_core.core_utils.terminate_fatal(f"A database dialect '{dcr_core.core_glob.setup.db_dialect}' " f"is not supported in DCR")

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Disconnect the database.
    # -----------------------------------------------------------------------------
    def disconnect_db(self) -> None:
        """Disconnect the database."""
        self.db_orm_metadata.clear()
        # try:
        #     self.db_orm_metadata.clear()
        # except:
        #     dcr.utils.progress_msg(
        #         "There are currently no database metadata available",
        #     )

        self.db_orm_engine.dispose()
        # try:
        #     self.db_orm_engine.dispose()
        # except:
        #     dcr.utils.progress_msg(
        #         "There is currently database engine available",
        #     )

        self._db_current_database = ""
        self._db_current_user = ""

        dcr.utils.progress_msg_disconnected()

    # -----------------------------------------------------------------------------
    # Check the object existence.
    # -----------------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns:
            bool:   Always true
        """
        return self._exist

    # -----------------------------------------------------------------------------
    # Delete a database row based on its id column.
    # -----------------------------------------------------------------------------
    def delete_dbt_id(
        self,
        table_name: str,
        id_where: int,
    ) -> None:
        """Delete a database row based on its id column.

        Args:
            table_name (str): sqlalchemy.Table name.
            id_where (int): Content of column id.
        """
        dbt = sqlalchemy.Table(table_name, self.db_orm_metadata, autoload_with=self.db_orm_engine)

        with self.db_orm_engine.connect().execution_options(autocommit=True) as conn:
            conn.execute(sqlalchemy.delete(dbt).where(dbt.c.id == id_where))

            conn.close()

    # -----------------------------------------------------------------------------
    # Insert a new row into a database table.
    # -----------------------------------------------------------------------------
    def insert_dbt_row(
        self,
        table_name: str,
        columns: Columns,
    ) -> int:
        """Insert a new row into a database table.

        Args:
            table_name (str): Table name.
            columns (dcr.cfg.glob.TYPE_COLUMNS_INSERT): Pairs of column name and value.

        Returns:
            int: The last id found.
        """
        dbt = sqlalchemy.Table(table_name, self.db_orm_metadata, autoload_with=self.db_orm_engine)

        with self.db_orm_engine.connect().execution_options(autocommit=True) as conn:
            result = conn.execute(sqlalchemy.insert(dbt).values(columns).returning(dbt.columns.id))
            row = result.fetchone()

            conn.close()

        return row[0]  # type: ignore

    # -----------------------------------------------------------------------------
    # Load database data from a JSON file.
    # -----------------------------------------------------------------------------
    def load_db_data_from_json(self, db_initial_data_file: pathlib.Path) -> None:
        """Load database data from a JSON file.

        Args:
            db_initial_data_file (Path): JSON file.
        """
        with open(db_initial_data_file, "r", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            api_version = json_data[DBCore.JSON_NAME_API_VERSION]
            if api_version != dcr_core.cls_setup.Setup.DCR_VERSION:
                dcr_core.core_utils.terminate_fatal(
                    f"Expected api version is' {dcr_core.cls_setup.Setup.DCR_VERSION}' " f"- got '{api_version}'"
                )

            data = json_data[DBCore.JSON_NAME_DATA]
            for json_table in data[DBCore.JSON_NAME_TABLES]:
                table_name = json_table[DBCore.JSON_NAME_TABLE_NAME].lower()

                if table_name not in ["language"]:
                    if table_name in {
                        "action",
                        "document",
                        "run",
                        "token",
                        "version",
                    }:
                        dcr_core.core_utils.terminate_fatal(f"The database table '{table_name}' must not be changed via the JSON file.")
                    else:
                        dcr_core.core_utils.terminate_fatal(f"The database table '{table_name}' does not exist in the database.")

                for json_row in json_table[DBCore.JSON_NAME_ROWS]:
                    db_columns = {}

                    for json_column in json_row[DBCore.JSON_NAME_ROW]:
                        db_columns[json_column[DBCore.JSON_NAME_COLUMN_NAME]] = json_column[DBCore.JSON_NAME_COLUMN_VALUE]

                    self.insert_dbt_row(
                        table_name,
                        db_columns,
                    )

    # -----------------------------------------------------------------------------
    # Update a database row based on its id column.
    # -----------------------------------------------------------------------------
    def update_dbt_id(
        self,
        table_name: str,
        id_where: int,
        columns: Columns,
    ) -> None:
        """Update a database row based on its id column.

        Args:
            table_name (str): sqlalchemy.Table name.
            id_where (int): Content of column id.
            columns (Columns): Pairs of column name and value.
        """
        dbt = sqlalchemy.Table(table_name, self.db_orm_metadata, autoload_with=self.db_orm_engine)

        with self.db_orm_engine.connect().execution_options(autocommit=True) as conn:
            conn.execute(sqlalchemy.update(dbt).where(dbt.c.id == id_where).values(columns))

            conn.close()

    # -----------------------------------------------------------------------------
    # Upgrade the current database schema.
    # -----------------------------------------------------------------------------
    def upgrade_database(self) -> None:
        """Upgrade the current database schema.

        Check if the current database schema needs to be upgraded and
        perform the necessary steps.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        dcr.utils.progress_msg("Upgrade the database tables ...")

        current_version = dcr.db.cls_version.Version.select_version_version_unique()

        self._db_driver_conn = self._connect_db_admin()

        if current_version == dcr_core.cls_setup.Setup.DCR_VERSION:
            dcr.utils.progress_msg(f"The database is already up to date, version number='{current_version}'")
        else:
            while dcr.db.cls_version.Version.select_version_version_unique() != dcr_core.cls_setup.Setup.DCR_VERSION:
                self._upgrade_database_version()

        self.disconnect_db()

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)
