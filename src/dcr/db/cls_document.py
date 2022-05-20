"""Module db.cls_document: Managing the database table document."""
from __future__ import annotations

import os
from typing import Tuple
from typing import Union

import cfg.glob
import db.cls_run
import db.dml
import sqlalchemy
import utils
from sqlalchemy import Integer
from sqlalchemy import String


# pylint: disable=R0801
# pylint: disable=R0902
# pylint: disable=R0903
class Document:
    """Managing the database table document.

    Returns:
        _type_: Document instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(  # pylint: disable=R0913
        self,
        action_code_last: str,
        directory_name: str,
        file_name: str,
        id_language: int | sqlalchemy.Integer,
        id_run_last: int | sqlalchemy.Integer,
        _row_id: int | sqlalchemy.Integer = 0,
        action_text_last: str = "",
        error_code_last: str | sqlalchemy.String = "",
        error_msg_last: str | sqlalchemy.String = "",
        error_no: int = 0,
        file_size_bytes: int = 0,
        no_pdf_pages: int = 0,
        sha256: str | sqlalchemy.String = "",
        status: str | sqlalchemy.String = "",
    ) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.document_action_code_last: str = action_code_last
        self.document_action_text_last: str = action_text_last
        self.document_directory_name: str = directory_name
        self.document_error_code_last: str | sqlalchemy.String = error_code_last
        self.document_error_msg_last: str | sqlalchemy.String = error_msg_last
        self.document_error_no: int = error_no
        self.document_file_name: str = file_name
        self.document_file_size_bytes: int = file_size_bytes
        self.document_id: int | sqlalchemy.Integer = _row_id
        self.document_id_language: int | sqlalchemy.Integer = id_language
        self.document_id_run_last: int | sqlalchemy.Integer = id_run_last
        self.document_no_pdf_pages: int = no_pdf_pages
        self.document_sha256: str | sqlalchemy.String = sha256
        self.document_status: str | sqlalchemy.String = status

        if self.document_id == 0:
            self.persist_2_db()

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

        self.document_action_text_last = db.cls_run.Run.get_action_text(self.document_action_code_last)

        return {
            cfg.glob.DBC_ACTION_CODE_LAST: self.document_action_code_last,
            cfg.glob.DBC_ACTION_TEXT_LAST: self.document_action_text_last,
            cfg.glob.DBC_DIRECTORY_NAME: self.document_directory_name,
            cfg.glob.DBC_ERROR_CODE_LAST: self.document_error_code_last,
            cfg.glob.DBC_ERROR_MSG_LAST: self.document_error_msg_last,
            cfg.glob.DBC_ERROR_NO: self.document_error_no,
            cfg.glob.DBC_FILE_NAME: self.document_file_name,
            cfg.glob.DBC_FILE_SIZE_BYTES: self.document_file_size_bytes,
            cfg.glob.DBC_ID_LANGUAGE: self.document_id_language,
            cfg.glob.DBC_ID_RUN_LAST: self.document_id_run_last,
            cfg.glob.DBC_NO_PDF_PAGES: self.document_no_pdf_pages,
            cfg.glob.DBC_SHA256: self.document_sha256,
            cfg.glob.DBC_STATUS: self.document_status,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            cfg.glob.DBT_DOCUMENT,
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
            sqlalchemy.Column(cfg.glob.DBC_SHA256, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_STATUS, sqlalchemy.String, nullable=False),
        )

        utils.progress_msg(f"The database table '{cfg.glob.DBT_DOCUMENT}' has now been created")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finalise the current row.
    # -----------------------------------------------------------------------------
    def finalise(self) -> None:
        """Finalise the current row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.document_status = cfg.glob.DOCUMENT_STATUS_END

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

        self.document_error_code_last = error_code
        self.document_error_msg_last = error_msg
        self.document_error_no += 1
        self.document_status = cfg.glob.DOCUMENT_STATUS_ERROR

        self.persist_2_db()

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise from id.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_id(cls, id_document: int | sqlalchemy.Integer) -> Document:
        """Initialise from id."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            cfg.glob.DBT_DOCUMENT,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )

        with cfg.glob.db_orm_engine.connect() as conn:  # type: ignore
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_document,
                )
            ).fetchone()
            conn.close()

        if row is None:
            utils.terminate_fatal(
                f"The document with id={id_document} does not exist in the database table 'document'",
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return Document.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Document:
        """Initialise from a database row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[cfg.glob.DBC_ID],
            action_code_last=row[cfg.glob.DBC_ACTION_CODE_LAST],
            action_text_last=row[cfg.glob.DBC_ACTION_TEXT_LAST],
            directory_name=utils.get_os_independent_name(row[cfg.glob.DBC_DIRECTORY_NAME]),
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
    # Get the database columns in a tuple.
    # -----------------------------------------------------------------------------
    def get_columns_in_tuple(self, is_file_size_bytes: bool = True) -> Tuple[Union[str, int, Integer, String], ...]:
        """Get the database columns in a tuple.

        Args:
            is_file_size_bytes (bool, optional): Including column file_size_bytes?. Defaults to True.

        Returns:
                Tuple[Union[str, int, Integer, String], ...]:
                        Column values in a tuple.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        column_01_08 = (
            self.document_id,
            self.document_action_code_last,
            self.document_action_text_last,
            self.document_directory_name,
            self.document_error_code_last,
            self.document_error_msg_last,
            self.document_error_no,
            self.document_file_name,
        )

        column_file_size_bytes = (self.document_file_size_bytes,)

        column_10_14 = (
            self.document_id_language,
            self.document_id_run_last,
            self.document_no_pdf_pages,
            self.document_sha256,
            self.document_status,
        )

        return column_01_08 + ((column_file_size_bytes + column_10_14) if is_file_size_bytes else column_10_14)

    # -----------------------------------------------------------------------------
    # Get the file name from the first processed document.
    # -----------------------------------------------------------------------------
    def get_file_name_next(self) -> str:
        """Get the file name from the first processed document.

        Returns:
            str: File name.
        """
        return (
            self.get_stem_name_next()
            + "."
            + (
                self.get_file_type()
                if self.get_file_type() != cfg.glob.DOCUMENT_FILE_TYPE_TIF
                else cfg.glob.DOCUMENT_FILE_TYPE_TIFF
            )
        )

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    def get_file_type(self) -> str:
        """Get the file type from the file name.

        Returns:
            str: File type.
        """
        if self.document_file_name == "":
            return self.document_file_name

        return utils.get_file_type(utils.get_os_independent_name(self.document_file_name))

    # -----------------------------------------------------------------------------
    # Get the full name from a directory name / path and a file name / path.
    # -----------------------------------------------------------------------------
    def get_full_name(self) -> str:
        """Get the full file from a directory name or path and a file name or
        path.

        Returns:
            str: Full file name.
        """
        return utils.get_full_name(
            directory_name=self.document_directory_name,
            file_name=self.document_file_name,
        )

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name.
    # -----------------------------------------------------------------------------
    def get_stem_name(self) -> str:
        """Get the stem name from the file name.

        Returns:
            str: Stem name.
        """
        if self.document_file_name == "":
            return self.document_file_name

        return utils.get_stem_name(str(self.document_file_name))

    # -----------------------------------------------------------------------------
    # Get the stem name from the first processed document.
    # -----------------------------------------------------------------------------
    def get_stem_name_next(self) -> str:
        """Get the stem name from the first processed document.

        Returns:
            str: Stem name.
        """
        if self.document_file_name == "":
            return self.document_file_name

        return utils.get_stem_name(str(self.document_file_name)) + "_" + str(self.document_id)

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        if self.document_file_size_bytes == 0:
            self.document_file_size_bytes = os.path.getsize(
                utils.get_full_name(self.document_directory_name, self.document_file_name)
            )

        if self.document_no_pdf_pages == 0:
            self.document_no_pdf_pages = utils.get_pdf_pages_no(
                utils.get_full_name(self.document_directory_name, self.document_file_name)
            )

        if self.document_id == 0:
            self.document_status = (
                self.document_status if self.document_status != "" else cfg.glob.DOCUMENT_STATUS_START
            )

            self.document_id = db.dml.insert_dbt_row(
                table_name=cfg.glob.DBT_DOCUMENT,
                columns=self._get_columns(),
            )
        else:
            db.dml.update_dbt_id(
                table_name=cfg.glob.DBT_DOCUMENT,
                id_where=self.document_id,
                columns=self._get_columns(),
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the duplicate file name based on the hash key.
    # -----------------------------------------------------------------------------
    @classmethod
    def select_duplicate_file_name_by_sha256(cls, id_document: int | sqlalchemy.Integer, sha256: str) -> str:
        """Get the duplicate file name based on the hash key.

        Args:
            id_document (sqlalchemy.Integer): Document id.
            sha256 (str): Hash key.

        Returns:
            str | None: The file name found.
        """
        dbt = sqlalchemy.Table(
            cfg.glob.DBT_DOCUMENT,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )

        with cfg.glob.db_orm_engine.connect() as conn:  # type: ignore
            stmnt = sqlalchemy.select(dbt.c.file_name).where(
                sqlalchemy.and_(
                    dbt.c.id != id_document,
                    dbt.c.sha256 == sha256,
                )
            )

            cfg.glob.logger.debug("SQL Statement=%s", stmnt)

            row = conn.execute(stmnt).fetchone()

            conn.close()

            if row is None:
                return ""

            return row[0]  # type: ignore