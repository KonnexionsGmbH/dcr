# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module dcr.db.cls_document: Managing the database table document."""
from __future__ import annotations

import os
from typing import ClassVar

import dcr_core.core_glob
import dcr_core.core_utils
import sqlalchemy

import dcr.cfg.glob
import dcr.db.cls_db_core
import dcr.db.cls_run
import dcr.utils


# pylint: disable=duplicate-code
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
class Document:
    """Managing the database table document.

    Returns:
        _type_: Document instance.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    DOCUMENT_DIRECTORY_TYPE_INBOX: ClassVar[str] = "inbox"
    DOCUMENT_DIRECTORY_TYPE_INBOX_ACCEPTED: ClassVar[str] = "inbox_accepted"
    DOCUMENT_DIRECTORY_TYPE_INBOX_REJECTED: ClassVar[str] = "inbox_rejected"

    DOCUMENT_ERROR_CODE_REJ_FILE_DUPL: ClassVar[str] = "Duplicate file"
    DOCUMENT_ERROR_CODE_REJ_FILE_EXT: ClassVar[str] = "Unknown file extension"
    DOCUMENT_ERROR_CODE_REJ_FILE_OPEN: ClassVar[str] = "Issue with file open"
    DOCUMENT_ERROR_CODE_REJ_NO_PDF_FORMAT: ClassVar[str] = "No 'pdf' format"
    DOCUMENT_ERROR_CODE_REJ_PARSER: ClassVar[str] = "Issue with parser"
    DOCUMENT_ERROR_CODE_REJ_PDF2IMAGE: ClassVar[str] = "Issue with pdf2image"
    DOCUMENT_ERROR_CODE_REJ_TESSERACT: ClassVar[str] = "Issue with Tesseract OCR"
    DOCUMENT_ERROR_CODE_REJ_TOKENIZE: ClassVar[str] = "Issue with tokenizing"

    DOCUMENT_STATUS_END: ClassVar[str] = "end"
    DOCUMENT_STATUS_ERROR: ClassVar[str] = "error"
    DOCUMENT_STATUS_START: ClassVar[str] = "start"

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(
        self,
        action_code_last: str,
        directory_name: str,
        file_name: str,
        id_language: int,
        id_run_last: int,
        _row_id: int = 0,
        action_text_last: str = "",
        error_code_last: str = "",
        error_msg_last: str = "",
        error_no: int = 0,
        file_size_bytes: int = 0,
        no_lines_footer: int = 0,
        no_lines_header: int = 0,
        no_lines_toc: int = 0,
        no_lists_bullet: int = 0,
        no_lists_number: int = 0,
        no_tables: int = 0,
        no_pdf_pages: int = 0,
        sha256: str = "",
        status: str = "",
    ) -> None:
        """Initialise the instance.

        Args:
            action_code_last (str):
                    Action code of the last action.
            directory_name (str):
                    The document location.
            file_name (str):
                    The file name.
            id_language (int):
                    The row id of the language
            id_run_last (int):
                    _description_
            _row_id (int, optional):
                    Row id of the last run that processed this document action. Defaults to 0.
            action_text_last (str, optional):
                    Action text (is derived from action_code_last if it is missing). Defaults to "".
            error_code_last (str, optional):
                    The code of the last error that occurred. Defaults to "".
            error_msg_last (str, optional):
                    The message of the last error that occurred. Defaults to "".
            error_no (int, optional):
                    The total number of errors in this document. Defaults to 0.
            file_size_bytes (int, optional):
                    The file size in bytes. Defaults to 0.
            no_lines_footer (int, optional):
                    The number of footer lines. Defaults to 0.
            no_lines_header (int, optional):
                    The number of header lines. Defaults to 0.
            no_lines_toc (int, optional):
                    The number of toc lines. Defaults to 0.
            no_lists_bullet (int, optional):
                    The number of bulleted lists. Defaults to 0.
            no_lists_number (int, optional):
                    The number of numbered lists. Defaults to 0.
            no_tables (int, optional):
                    The number of tables. Defaults to 0.
            no_pdf_pages (int, optional):
                    For a document of the type 'pdf' the number of pages. Defaults to 0.
            sha256 (str, optional):
                    The value of the SHA-256 hash function. Defaults to "".
            status (str, optional):
                    Status. Defaults to "".
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        dcr.utils.check_exists_object(
            is_db_core=True,
        )

        self.document_action_code_last = action_code_last
        self.document_action_text_last = action_text_last
        self.document_directory_name = directory_name
        self.document_error_code_last = error_code_last
        self.document_error_msg_last = error_msg_last
        self.document_error_no = error_no
        self.document_file_name = file_name
        self.document_file_size_bytes = file_size_bytes
        self.document_id = _row_id
        self.document_id_language = id_language
        self.document_id_run_last = id_run_last
        self.document_no_lines_footer = no_lines_footer
        self.document_no_lines_header = no_lines_header
        self.document_no_lines_toc = no_lines_toc
        self.document_no_lists_bullet = no_lists_bullet
        self.document_no_lists_number = no_lists_number
        self.document_no_tables = no_tables
        self.document_no_pdf_pages = no_pdf_pages
        self.document_sha256 = sha256
        self.document_status = status

        if self.document_id == 0:
            self.persist_2_db()

        self._exist = True

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the database columns.
    # -----------------------------------------------------------------------------
    def _get_columns(self) -> dcr.db.cls_db_core.Columns:
        """Get the database columns.

        Returns:
            dcr.db.cls_db_core.Columns:
                    Database columns.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

        self.document_action_text_last = dcr.db.cls_run.Run.get_action_text(self.document_action_code_last)

        return {
            dcr.db.cls_db_core.DBCore.DBC_ACTION_CODE_LAST: self.document_action_code_last,
            dcr.db.cls_db_core.DBCore.DBC_ACTION_TEXT_LAST: self.document_action_text_last,
            dcr.db.cls_db_core.DBCore.DBC_DIRECTORY_NAME: self.document_directory_name,
            dcr.db.cls_db_core.DBCore.DBC_ERROR_CODE_LAST: self.document_error_code_last,
            dcr.db.cls_db_core.DBCore.DBC_ERROR_MSG_LAST: self.document_error_msg_last,
            dcr.db.cls_db_core.DBCore.DBC_ERROR_NO: self.document_error_no,
            dcr.db.cls_db_core.DBCore.DBC_FILE_NAME: self.document_file_name,
            dcr.db.cls_db_core.DBCore.DBC_FILE_SIZE_BYTES: self.document_file_size_bytes,
            dcr.db.cls_db_core.DBCore.DBC_ID_LANGUAGE: self.document_id_language,
            dcr.db.cls_db_core.DBCore.DBC_ID_RUN_LAST: self.document_id_run_last,
            dcr.db.cls_db_core.DBCore.DBC_NO_LINES_FOOTER: self.document_no_lines_footer,
            dcr.db.cls_db_core.DBCore.DBC_NO_LINES_HEADER: self.document_no_lines_header,
            dcr.db.cls_db_core.DBCore.DBC_NO_LINES_TOC: self.document_no_lines_toc,
            dcr.db.cls_db_core.DBCore.DBC_NO_LISTS_BULLET: self.document_no_lists_bullet,
            dcr.db.cls_db_core.DBCore.DBC_NO_LISTS_NUMBER: self.document_no_lists_number,
            dcr.db.cls_db_core.DBCore.DBC_NO_TABLES: self.document_no_tables,
            dcr.db.cls_db_core.DBCore.DBC_NO_PDF_PAGES: self.document_no_pdf_pages,
            dcr.db.cls_db_core.DBCore.DBC_SHA256: self.document_sha256,
            dcr.db.cls_db_core.DBCore.DBC_STATUS: self.document_status,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_DOCUMENT,
            dcr.cfg.glob.db_core.db_orm_metadata,
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_ID,
                sqlalchemy.Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_CREATED_AT,
                sqlalchemy.DateTime,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_MODIFIED_AT,
                sqlalchemy.DateTime,
            ),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_ACTION_CODE_LAST, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_ACTION_TEXT_LAST, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_DIRECTORY_NAME, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_ERROR_CODE_LAST, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_ERROR_MSG_LAST, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_ERROR_NO, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_FILE_NAME, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_FILE_SIZE_BYTES, sqlalchemy.Integer, nullable=True),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_ID_LANGUAGE,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(dcr.db.cls_db_core.DBCore.DBT_LANGUAGE + "." + dcr.db.cls_db_core.DBCore.DBC_ID, ondelete="CASCADE"),
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_ID_RUN_LAST,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(dcr.db.cls_db_core.DBCore.DBT_RUN + "." + dcr.db.cls_db_core.DBCore.DBC_ID, ondelete="CASCADE"),
                nullable=False,
            ),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_NO_LINES_FOOTER, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_NO_LINES_HEADER, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_NO_LINES_TOC, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_NO_LISTS_BULLET, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_NO_LISTS_NUMBER, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_NO_TABLES, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_NO_PDF_PAGES, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_SHA256, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_STATUS, sqlalchemy.String, nullable=False),
        )

        dcr.utils.progress_msg(f"The database table '{dcr.db.cls_db_core.DBCore.DBT_DOCUMENT}' has now been created")

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

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
    # Finalise the current row.
    # -----------------------------------------------------------------------------
    def finalise(self) -> None:
        """Finalise the current row."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        self.document_status = Document.DOCUMENT_STATUS_END

        self.persist_2_db()

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finalise the current row with error.
    # -----------------------------------------------------------------------------
    def finalise_error(self, error_code: str, error_msg: str) -> None:
        """Finalise the current row with error.

        Args:
            error_code (str):
                    Error code.
            error_msg (str):
                    Error message.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        self.document_error_code_last = error_code
        self.document_error_msg_last = error_msg
        self.document_error_no += 1
        self.document_status = Document.DOCUMENT_STATUS_ERROR

        self.persist_2_db()

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise from id.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_id(cls, id_document: int) -> Document:
        """Initialise from id.

        Args:
            id_document (int):
                    The required row id.

        Returns:
            Document:
                    The object instance found.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_DOCUMENT,
            dcr.cfg.glob.db_core.db_orm_metadata,
            autoload_with=dcr.cfg.glob.db_core.db_orm_engine,
        )

        with dcr.cfg.glob.db_core.db_orm_engine.connect() as conn:
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_document,
                )
            ).fetchone()
            conn.close()

        if row is None:
            dcr_core.core_utils.terminate_fatal(
                f"The document with id={id_document} does not exist in the database table 'document'",
            )

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

        return Document.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Document:
        """Initialise from a database row.

        Args:
            row (sqlalchemy.engine.Row):
                    A appropriate database row.

        Returns:
            Document:
                    The object instance matching the specified database row.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[dcr.db.cls_db_core.DBCore.DBC_ID],
            action_code_last=row[dcr.db.cls_db_core.DBCore.DBC_ACTION_CODE_LAST],
            action_text_last=row[dcr.db.cls_db_core.DBCore.DBC_ACTION_TEXT_LAST],
            directory_name=dcr_core.core_utils.get_os_independent_name(row[dcr.db.cls_db_core.DBCore.DBC_DIRECTORY_NAME]),
            error_code_last=row[dcr.db.cls_db_core.DBCore.DBC_ERROR_CODE_LAST],
            error_msg_last=row[dcr.db.cls_db_core.DBCore.DBC_ERROR_MSG_LAST],
            error_no=row[dcr.db.cls_db_core.DBCore.DBC_ERROR_NO],
            file_name=row[dcr.db.cls_db_core.DBCore.DBC_FILE_NAME],
            file_size_bytes=row[dcr.db.cls_db_core.DBCore.DBC_FILE_SIZE_BYTES],
            id_language=row[dcr.db.cls_db_core.DBCore.DBC_ID_LANGUAGE],
            id_run_last=row[dcr.db.cls_db_core.DBCore.DBC_ID_RUN_LAST],
            no_lines_footer=row[dcr.db.cls_db_core.DBCore.DBC_NO_LINES_FOOTER],
            no_lines_header=row[dcr.db.cls_db_core.DBCore.DBC_NO_LINES_HEADER],
            no_lines_toc=row[dcr.db.cls_db_core.DBCore.DBC_NO_LINES_TOC],
            no_lists_bullet=row[dcr.db.cls_db_core.DBCore.DBC_NO_LISTS_BULLET],
            no_lists_number=row[dcr.db.cls_db_core.DBCore.DBC_NO_LISTS_NUMBER],
            no_tables=row[dcr.db.cls_db_core.DBCore.DBC_NO_TABLES],
            no_pdf_pages=row[dcr.db.cls_db_core.DBCore.DBC_NO_PDF_PAGES],
            sha256=row[dcr.db.cls_db_core.DBCore.DBC_SHA256],
            status=row[dcr.db.cls_db_core.DBCore.DBC_STATUS],
        )

    # -----------------------------------------------------------------------------
    # Get the database columns in a tuple.
    # -----------------------------------------------------------------------------
    def get_columns_in_tuple(self, is_file_size_bytes: bool = True, is_sha256: bool = True) -> tuple[int | str, ...]:
        """Get the database columns in a tuple.

        Args:
            is_file_size_bytes (bool, optional):
                    Including column file_size_bytes?. Defaults to True.
            is_sha256 (bool, optional):
                    Including column sha256?. Defaults to True.

        Returns:
            tuple[int | str, ...]:
                        Column values in a tuple.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        columns = [
            self.document_id,
            self.document_action_code_last,
            self.document_action_text_last,
            self.document_directory_name,
            self.document_error_code_last,
            self.document_error_msg_last,
            self.document_error_no,
            self.document_file_name,
        ]

        if is_file_size_bytes:
            columns.append(self.document_file_size_bytes)

        columns = columns + [
            self.document_id_language,
            self.document_id_run_last,
            self.document_no_lines_footer,
            self.document_no_lines_header,
            self.document_no_lines_toc,
            self.document_no_lists_bullet,
            self.document_no_lists_number,
            self.document_no_tables,
            self.document_no_pdf_pages,
        ]

        if is_sha256:
            columns.append(self.document_sha256)

        columns.append(self.document_status)

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

        return tuple(columns)  # type: ignore

    # -----------------------------------------------------------------------------
    # Get the file name from the first processed document.
    # -----------------------------------------------------------------------------
    def get_file_name_next(self) -> str:
        """Get the file name from the first processed document.

        Returns:
            str:    File name of the following action.
        """
        return (
            self.get_stem_name_next()
            + "."
            + (self.get_file_type() if self.get_file_type() != dcr_core.core_glob.FILE_TYPE_TIF else dcr_core.core_glob.FILE_TYPE_TIFF)
        )

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    def get_file_type(self) -> str:
        """Get the file type from the file name.

        Returns:
            str:    File type.
        """
        if self.document_file_name == "":
            return self.document_file_name

        return dcr.utils.get_file_type(dcr_core.core_utils.get_os_independent_name(self.document_file_name))

    # -----------------------------------------------------------------------------
    # Get the full name from a directory name / path and a file name / path.
    # -----------------------------------------------------------------------------
    def get_full_name(self) -> str:
        """Get the full file from a directory name or path and a file name or
        path.

        Returns:
            str:    Full file name.
        """
        return dcr_core.core_utils.get_full_name(
            directory_name=self.document_directory_name,
            file_name=self.document_file_name,
        )

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name.
    # -----------------------------------------------------------------------------
    def get_stem_name(self) -> str:
        """Get the stem name from the file name.

        Returns:
            str:    Stem name.
        """
        if self.document_file_name == "":
            return self.document_file_name

        return dcr_core.core_utils.get_stem_name(str(self.document_file_name))

    # -----------------------------------------------------------------------------
    # Get the stem name from the first processed document.
    # -----------------------------------------------------------------------------
    def get_stem_name_next(self) -> str:
        """Get the stem name from the first processed document.

        Returns:
            str:    Stem name of the following action.
        """
        if self.document_file_name == "":
            return self.document_file_name

        dcr_core.core_utils.check_exists_object(
            is_setup=True,
        )

        if dcr_core.core_glob.setup.doc_id_in_file_name == "none":
            return dcr_core.core_utils.get_stem_name(str(self.document_file_name))

        if dcr_core.core_glob.setup.doc_id_in_file_name == "after":
            return dcr_core.core_utils.get_stem_name(str(self.document_file_name)) + "_" + str(self.document_id)

        return str(self.document_id) + "_" + dcr_core.core_utils.get_stem_name(str(self.document_file_name))

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        if self.document_file_size_bytes == 0:
            self.document_file_size_bytes = os.path.getsize(
                dcr_core.core_utils.get_full_name(self.document_directory_name, self.document_file_name)
            )

        if self.document_no_pdf_pages == 0:
            self.document_no_pdf_pages = dcr.utils.get_pdf_pages_no(
                dcr_core.core_utils.get_full_name(self.document_directory_name, self.document_file_name)
            )

        if self.document_id == 0:
            self.document_status = self.document_status if self.document_status != "" else Document.DOCUMENT_STATUS_START

            self.document_id = dcr.cfg.glob.db_core.insert_dbt_row(  # type: ignore
                table_name=dcr.db.cls_db_core.DBCore.DBT_DOCUMENT,
                columns=self._get_columns(),
            )
        else:
            dcr.cfg.glob.db_core.update_dbt_id(  # type: ignore
                table_name=dcr.db.cls_db_core.DBCore.DBT_DOCUMENT,
                id_where=self.document_id,
                columns=self._get_columns(),
            )

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the duplicate file name based on the hash key.
    # -----------------------------------------------------------------------------
    @classmethod
    def select_duplicate_file_name_by_sha256(cls, id_document: int, sha256: str) -> str:
        """Get the duplicate file name based on the hash key.

        Args:
            id_document (int):
                    Document id.
            sha256 (str):
                    Hash key.

        Returns:
            str | None:
                    The file name found.
        """
        dbt = sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_DOCUMENT,
            dcr.cfg.glob.db_core.db_orm_metadata,
            autoload_with=dcr.cfg.glob.db_core.db_orm_engine,
        )

        with dcr.cfg.glob.db_core.db_orm_engine.connect() as conn:
            stmnt = sqlalchemy.select(dbt.c.file_name).where(
                sqlalchemy.and_(
                    dbt.c.id != id_document,
                    dbt.c.sha256 == sha256,
                )
            )

            dcr.cfg.glob.logger.debug("SQL Statement=%s", stmnt)

            row = conn.execute(stmnt).fetchone()

            conn.close()

            if row is None:
                return ""

            return row[0]  # type: ignore
