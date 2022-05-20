"""Module db.cls_language: Managing the database table language."""
from __future__ import annotations

import os.path

import cfg.glob
import db.dml
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
import utils
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String


# pylint: disable=R0801
# pylint: disable=R0902
class Language:
    """Managing the language data.

    Returns:
        _type_: Language instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(  # pylint: disable=R0913
        self,
        code_iso_639_3: str | sqlalchemy.String,
        code_pandoc: str | sqlalchemy.String,
        code_spacy: str | sqlalchemy.String,
        code_tesseract: str | sqlalchemy.String,
        iso_language_name: str,
        _row_id: int | sqlalchemy.Integer = 0,
        active: bool | sqlalchemy.Boolean = False,
        directory_name_inbox: str = "",
    ) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.language_active: bool | sqlalchemy.Boolean = active
        self.language_code_iso_639_3: str | sqlalchemy.String = code_iso_639_3
        self.language_code_pandoc: str | sqlalchemy.String = code_pandoc
        self.language_code_spacy: str | sqlalchemy.String = code_spacy
        self.language_code_tesseract: str | sqlalchemy.String = code_tesseract

        if self.language_active and (directory_name_inbox is None or directory_name_inbox == ""):
            self.language_directory_name_inbox: str = str(
                os.path.join(cfg.glob.setup.directory_inbox, iso_language_name.lower())
            )
        else:
            self.language_directory_name_inbox = utils.get_os_independent_name(directory_name_inbox)

        self.language_id: int | sqlalchemy.Integer = _row_id
        self.language_iso_language_name: str = iso_language_name

        self.total_erroneous: int = 0
        self.total_processed: int = 0
        self.total_processed_to_be: int = 0
        self.total_processed_pandoc: int = 0
        self.total_processed_pdf2image = 0
        self.total_processed_pdflib = 0
        self.total_processed_tesseract = 0

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the database columns.
    # -----------------------------------------------------------------------------
    def _get_columns(self) -> db.dml.Columns:
        """Get the database columns.

        Returns:
            db.dml.Columns: Database columns.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return {
            cfg.glob.DBC_ACTIVE: self.language_active,
            cfg.glob.DBC_CODE_ISO_639_3: self.language_code_iso_639_3,
            cfg.glob.DBC_CODE_PANDOC: self.language_code_pandoc,
            cfg.glob.DBC_CODE_SPACY: self.language_code_spacy,
            cfg.glob.DBC_CODE_TESSERACT: self.language_code_tesseract,
            cfg.glob.DBC_DIRECTORY_NAME_INBOX: self.language_directory_name_inbox,
            cfg.glob.DBC_ISO_LANGUAGE_NAME: self.language_iso_language_name,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            cfg.glob.DBT_LANGUAGE,
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

        utils.progress_msg(f"The database table '{cfg.glob.DBT_LANGUAGE}' has now been created")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise from id.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_id(cls, id_language: int | sqlalchemy.Integer) -> Language:
        """Initialise from id."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            cfg.glob.DBT_LANGUAGE,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )

        with cfg.glob.db_orm_engine.connect() as conn:  # type: ignore
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_language,
                )
            ).fetchone()
            conn.close()

        if row is None:
            utils.terminate_fatal(
                f"The language with id={id_language} does not exist in the database table 'language'",
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return Language.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Language:
        """Initialise from a database row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[cfg.glob.DBC_ID],
            active=row[cfg.glob.DBC_ACTIVE],
            code_iso_639_3=row[cfg.glob.DBC_CODE_ISO_639_3],
            code_pandoc=row[cfg.glob.DBC_CODE_PANDOC],
            code_spacy=row[cfg.glob.DBC_CODE_SPACY],
            code_tesseract=row[cfg.glob.DBC_CODE_TESSERACT],
            directory_name_inbox=row[cfg.glob.DBC_DIRECTORY_NAME_INBOX],
            iso_language_name=row[cfg.glob.DBC_ISO_LANGUAGE_NAME],
        )

    # -----------------------------------------------------------------------------
    # Get the database columns in a tuple.
    # -----------------------------------------------------------------------------
    def get_columns_in_tuple(
        self,
    ) -> tuple[
        int | Integer,
        bool | Boolean,
        str | String,
        str | String,
        str | String,
        str | String,
        str | String,
        str | String,
    ]:
        """Get the database columns in a tuple.

            Returns:
                tuple[
            int | Integer,
            bool | Boolean,
            str | String,
            str | String,
            str | String,
            str | String,
            str | String,
            str | String,
        ]: Column values in a tuple.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return (
            self.language_id,
            self.language_active,
            self.language_code_iso_639_3,
            self.language_code_pandoc,
            self.language_code_spacy,
            self.language_code_tesseract,
            self.language_directory_name_inbox,
            self.language_iso_language_name,
        )

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        if self.language_id == 0:
            self.language_id = db.dml.insert_dbt_row(
                cfg.glob.DBT_LANGUAGE,
                self._get_columns(),
            )
        else:
            db.dml.update_dbt_id(
                table_name=cfg.glob.DBT_LANGUAGE,
                id_where=self.language_id,
                columns=self._get_columns(),
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the active languages.
    # -----------------------------------------------------------------------------
    @classmethod
    def select_active_languages(cls, conn: sqlalchemy.engine.Connection) -> sqlalchemy.engine.CursorResult:
        """Get the languages to be processed.

        Args:
            conn (Connection): Database connection.

        Returns:
            engine.CursorResult: The languages found.
        """
        dbt = sqlalchemy.Table(
            cfg.glob.DBT_LANGUAGE,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )

        return conn.execute(
            sqlalchemy.select(dbt)
            .where(
                dbt.c.active,
            )
            .order_by(dbt.c.id.asc())
        )
