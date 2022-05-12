"""Module db.cls_base: Managing the document status."""
from __future__ import annotations

import os
import pathlib

import cfg.glob
import db.cls_run
import db.dml
import sqlalchemy
import utils


# pylint: disable=R0801
# pylint: disable=R0902
# pylint: disable=R0903
class Base:
    """Managing the document status.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(  # pylint: disable=R0913
        self,
        _row_id: int | sqlalchemy.Integer = 0,
        action_code_last: str = "",
        action_text_last: str = "",
        directory_name: str = "",
        error_code_last: str | sqlalchemy.String = "",
        error_msg_last: str | sqlalchemy.String = "",
        error_no: int = 0,
        file_name: str = "",
        file_size_bytes: int = 0,
        id_language: int | sqlalchemy.Integer = 0,
        id_run_last: int | sqlalchemy.Integer = 0,
        no_pdf_pages: int = 0,
        sha256: str | sqlalchemy.String = "",
        status: str | sqlalchemy.String = "",
    ) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.base_action_code_last: str = action_code_last
        self.base_action_text_last: str = action_text_last
        self.base_directory_name: str = directory_name
        self.base_error_code_last: str | sqlalchemy.String = error_code_last
        self.base_error_msg_last: str | sqlalchemy.String = error_msg_last
        self.base_error_no: int = error_no
        self.base_file_name: str = file_name
        self.base_file_size_bytes: int = file_size_bytes
        self.base_id: int | sqlalchemy.Integer = _row_id
        self.base_id_language: int | sqlalchemy.Integer = id_language
        self.base_id_run_last: int | sqlalchemy.Integer = id_run_last
        self.base_no_pdf_pages: int = no_pdf_pages
        self.base_sha256: str | sqlalchemy.String = sha256
        self.base_status: str | sqlalchemy.String = status

        if self.base_id == 0:
            self.persist_2_db()

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the database columns.
    # -----------------------------------------------------------------------------
    def _get_columns(self) -> db.utils.Columns:
        """Get the database columns.

        Returns:
            db.utils.Columns: Database columns.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return {
            cfg.glob.DBC_ACTION_CODE_LAST: self.base_action_code_last,
            cfg.glob.DBC_ACTION_TEXT_LAST: db.cls_run.Run.get_action_text(self.base_action_code_last),
            cfg.glob.DBC_DIRECTORY_NAME: self.base_directory_name,
            cfg.glob.DBC_ERROR_CODE_LAST: self.base_error_code_last,
            cfg.glob.DBC_ERROR_MSG_LAST: self.base_error_msg_last,
            cfg.glob.DBC_ERROR_NO: self.base_error_no,
            cfg.glob.DBC_FILE_NAME: self.base_file_name,
            cfg.glob.DBC_FILE_SIZE_BYTES: self.base_file_size_bytes,
            cfg.glob.DBC_ID_LANGUAGE: self.base_id_language,
            cfg.glob.DBC_ID_RUN_LAST: self.base_id_run_last,
            cfg.glob.DBC_NO_PDF_PAGES: self.base_no_pdf_pages,
            cfg.glob.DBC_SHA256: self.base_sha256,
            cfg.glob.DBC_STATUS: self.base_status,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            cfg.glob.DBT_BASE,
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
            sqlalchemy.Column(cfg.glob.DBC_ACTION_CODE_LAST, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(cfg.glob.DBC_ACTION_TEXT_LAST, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(cfg.glob.DBC_DIRECTORY_NAME, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(cfg.glob.DBC_ERROR_CODE_LAST, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_ERROR_MSG_LAST, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_ERROR_NO, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(cfg.glob.DBC_FILE_NAME, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(cfg.glob.DBC_FILE_SIZE_BYTES, sqlalchemy.Integer, nullable=True),
            sqlalchemy.Column(
                cfg.glob.DBC_ID_LANGUAGE,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(cfg.glob.DBT_LANGUAGE + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
                nullable=False,
            ),
            sqlalchemy.Column(
                cfg.glob.DBC_ID_RUN_LAST,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(cfg.glob.DBT_RUN + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
                nullable=False,
            ),
            sqlalchemy.Column(cfg.glob.DBC_NO_PDF_PAGES, sqlalchemy.Integer, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_ID_RUN_LAST, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(cfg.glob.DBC_SHA256, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_STATUS, sqlalchemy.String, nullable=False),
        )

        utils.progress_msg(f"The database table '{cfg.glob.DBT_BASE}' has now been created")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finalise the current row.
    # -----------------------------------------------------------------------------
    def finalise(self) -> None:
        """Finalise the current row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.base_status = cfg.glob.DOCUMENT_STATUS_END

        self.persist_2_db()

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finalise the current row with error.
    # -----------------------------------------------------------------------------
    def finalise_error(self, error_code: str, error_msg: str) -> None:
        """Finalise the current row with error.

        Args:
            error_code (str)                : Error code.
            error_msg (str)                 : Error message.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.base_error_code_last = error_code
        self.base_error_msg_last = error_msg
        self.base_error_no += 1
        self.base_status = cfg.glob.DOCUMENT_STATUS_ERROR

        self.persist_2_db()

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise from id.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_id(cls, id_base: int | sqlalchemy.Integer) -> Base:
        """Initialise from id."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            cfg.glob.DBT_BASE,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )

        with cfg.glob.db_orm_engine.connect() as conn:  # type: ignore
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_base,
                )
            ).fetchone()
            conn.close()

        if row == ():
            utils.terminate_fatal(
                f"The base with id={id_base} does not exist in the database table 'base'",
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return Base.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Base:
        """Initialise from a database row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[cfg.glob.DBC_ID],
            action_code_last=row[cfg.glob.DBC_ACTION_CODE_LAST],
            action_text_last=row[cfg.glob.DBC_ACTION_TEXT_LAST],
            directory_name=row[cfg.glob.DBC_DIRECTORY_NAME],
            error_code_last=row[cfg.glob.DBC_ERROR_CODE_LAST],
            error_msg_last=row[cfg.glob.DBC_ERROR_MSG_LAST],
            error_no=row[cfg.glob.DBC_ERROR_NO],
            file_name=row[cfg.glob.DBC_FILE_NAME],
            file_size_bytes=row[cfg.glob.DBC_FILE_SIZE_BYTES],
            id_language=row[cfg.glob.DBC_ID_LANGUAGE],
            id_run_last=row[cfg.glob.DBC_ID_RUN_LAST],
            no_pdf_pages=row[cfg.glob.DBC_NO_PDF_PAGES],
            sha256=row[cfg.glob.DBC_SHA256],
            status=row[cfg.glob.DBC_STATUS],
        )

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    def get_file_type(self) -> str:
        """Get the file type from the file name.

        Returns:
            str: File type.
        """
        if self.base_file_name == "":
            return self.base_file_name

        return utils.get_file_type(pathlib.Path(str(self.base_file_name)))

    # -----------------------------------------------------------------------------
    # Get the full file from a directory name or path and a file name or path.
    # -----------------------------------------------------------------------------
    def get_full_name(self) -> str:
        """Get the full file from a directory name or path and a file name or
        path.

        Returns:
            str: Full file name.
        """
        return utils.get_full_name(
            directory_name=self.base_directory_name,
            file_name=self.base_file_name,
        )

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name.
    # -----------------------------------------------------------------------------
    def get_stem_name(self) -> str:
        """Get the stem name from the file name.

        Returns:
            str: Stem name.
        """
        if self.base_file_name == "":
            return self.base_file_name

        return utils.get_stem_name(str(self.base_file_name))

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        if self.base_id == 0:
            self.base_file_size_bytes = os.path.getsize(pathlib.Path(self.base_directory_name, self.base_file_name))
            self.base_no_pdf_pages = utils.get_pdf_pages_no(
                str(pathlib.Path(self.base_directory_name, self.base_file_name))
            )
            self.base_status = self.base_status if self.base_status != "" else cfg.glob.DOCUMENT_STATUS_START

            self.base_id = db.dml.insert_dbt_row(
                table_name=cfg.glob.DBT_BASE,
                columns=self._get_columns(),
            )
        else:
            db.dml.update_dbt_id(
                table_name=cfg.glob.DBT_BASE,
                id_where=self.base_id,
                columns=self._get_columns(),
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
