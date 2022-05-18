"""Module db.cls_action: Managing the database table  action."""
from __future__ import annotations

import os
import pathlib
import time
from typing import ClassVar
from typing import Tuple
from typing import Union

import cfg.glob
import db.cls_run
import db.dml
import sqlalchemy
import utils
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.engine import Connection


# pylint: disable=R0801
# pylint: disable=R0902
# pylint: disable=R0903
class Action:
    """Managing the document processing steps.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    pdf2image_file_type: ClassVar[str] = ""

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(  # pylint: disable=R0913, R0914
        self,
        action_code: str,
        id_run_last: int | sqlalchemy.Integer,
        _row_id: int | sqlalchemy.Integer = 0,
        action_text: str = "",
        directory_name: str = "",
        directory_type: str = "",
        duration_ns: int = 0,
        error_code_last: str | sqlalchemy.String = "",
        error_msg_last: str | sqlalchemy.String = "",
        error_no: int = 0,
        file_name: str = "",
        file_size_bytes: int = 0,
        id_base: int | sqlalchemy.Integer = 0,
        id_parent: int | sqlalchemy.Integer = 0,
        no_children: int | sqlalchemy.Integer = 0,
        no_pdf_pages: int = 0,
        status: str | sqlalchemy.String = "",
    ) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.action_action_code: str = action_code
        self.action_action_text: str = action_text
        self.action_directory_name: str = utils.get_os_independent_name(directory_name)
        self.action_directory_type: str | sqlalchemy.String = directory_type
        self.action_duration_ns: int | sqlalchemy.BigInteger = duration_ns
        self.action_error_code_last: str | sqlalchemy.String = error_code_last
        self.action_error_msg_last: str | sqlalchemy.String = error_msg_last
        self.action_error_no: int = error_no
        self.action_file_name: str = file_name
        self.action_file_size_bytes: int = file_size_bytes
        self.action_id: int | sqlalchemy.Integer = _row_id
        self.action_id_base: int | sqlalchemy.Integer = id_base
        self.action_id_parent: int | sqlalchemy.Integer = id_parent if id_parent != 0 else 1
        self.action_id_run_last: int | sqlalchemy.Integer = id_run_last
        self.action_no_children: int | sqlalchemy.Integer = no_children
        self.action_no_pdf_pages: int = no_pdf_pages
        self.action_status: str | sqlalchemy.String = status

        if Action.pdf2image_file_type == "":
            Action.pdf2image_file_type = cfg.glob.DOCUMENT_FILE_TYPE_JPG

        if self.action_id == 0:
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

        return {
            cfg.glob.DBC_ACTION_CODE: self.action_action_code,
            cfg.glob.DBC_ACTION_TEXT: cfg.glob.run.get_action_text(self.action_action_code),
            cfg.glob.DBC_DIRECTORY_NAME: self.action_directory_name,
            cfg.glob.DBC_DIRECTORY_TYPE: self.action_directory_type,
            cfg.glob.DBC_DURATION_NS: self.action_duration_ns,
            cfg.glob.DBC_ERROR_CODE_LAST: self.action_error_code_last,
            cfg.glob.DBC_ERROR_MSG_LAST: self.action_error_msg_last,
            cfg.glob.DBC_ERROR_NO: self.action_error_no,
            cfg.glob.DBC_FILE_NAME: self.action_file_name,
            cfg.glob.DBC_FILE_SIZE_BYTES: self.action_file_size_bytes,
            cfg.glob.DBC_ID_BASE: self.action_id_base,
            cfg.glob.DBC_ID_PARENT: self.action_id_parent,
            cfg.glob.DBC_ID_RUN_LAST: self.action_id_run_last,
            cfg.glob.DBC_NO_CHILDREN: self.action_no_children,
            cfg.glob.DBC_NO_PDF_PAGES: self.action_no_pdf_pages,
            cfg.glob.DBC_STATUS: self.action_status,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            cfg.glob.DBT_ACTION,
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
            sqlalchemy.Column(cfg.glob.DBC_ACTION_CODE, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(cfg.glob.DBC_ACTION_TEXT, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(cfg.glob.DBC_DIRECTORY_NAME, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_DIRECTORY_TYPE, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_DURATION_NS, sqlalchemy.BigInteger, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_ERROR_CODE_LAST, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_ERROR_MSG_LAST, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_ERROR_NO, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(cfg.glob.DBC_FILE_NAME, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_FILE_SIZE_BYTES, sqlalchemy.Integer, nullable=True),
            sqlalchemy.Column(
                cfg.glob.DBC_ID_BASE,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(cfg.glob.DBT_BASE + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
                nullable=True,
            ),
            sqlalchemy.Column(
                cfg.glob.DBC_ID_PARENT,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(cfg.glob.DBT_ACTION + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
                nullable=True,
            ),
            sqlalchemy.Column(
                cfg.glob.DBC_ID_RUN_LAST,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(cfg.glob.DBT_RUN + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
                nullable=False,
            ),
            sqlalchemy.Column(cfg.glob.DBC_NO_CHILDREN, sqlalchemy.Integer, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_NO_PDF_PAGES, sqlalchemy.Integer, nullable=True),
            sqlalchemy.Column(cfg.glob.DBC_STATUS, sqlalchemy.String, nullable=False),
        )

        utils.progress_msg(f"The database table '{cfg.glob.DBT_ACTION}' has now been created")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finalise the current action.
    # -----------------------------------------------------------------------------
    def finalise(self) -> None:
        """Finalise the current action."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.action_duration_ns = time.perf_counter_ns() - cfg.glob.start_time_document

        if self.action_file_size_bytes == 0:
            self.action_file_size_bytes = os.path.getsize(
                utils.get_full_name(self.action_directory_name, self.action_file_name)
            )

        if self.action_no_pdf_pages == 0:
            self.action_no_pdf_pages = utils.get_pdf_pages_no(
                utils.get_full_name(self.action_directory_name, self.action_file_name)
            )

        self.action_status = cfg.glob.DOCUMENT_STATUS_END

        self.persist_2_db()

        cfg.glob.base.base_action_code_last = self.action_action_code
        cfg.glob.base.base_id_run_last = cfg.glob.run.run_id
        cfg.glob.base.base_status = cfg.glob.DOCUMENT_STATUS_END

        cfg.glob.base.persist_2_db()  # type: ignore

        if self.action_action_code == db.cls_run.Run.ACTION_CODE_INBOX:
            utils.progress_msg(
                f"Duration: {round(self.action_duration_ns / 1000000000, 2):6.2f} s - "
                f"Document: {cfg.glob.base.base_id:6d} "
                f"[{cfg.glob.base.base_file_name}]"
            )
        else:
            utils.progress_msg(
                f"Duration: {round(self.action_duration_ns / 1000000000, 2):6.2f} s - "
                f"Document: {self.action_id:6d} "
                f"[{self.action_file_name}]"
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finalise the current action with error.
    # -----------------------------------------------------------------------------
    def finalise_error(self, error_code: str, error_msg: str) -> None:
        """Finalise the current action with error.

        Args:
            error_code (str)                : Error code.
            error_msg (str)                 : Error message.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.action_duration_ns = time.perf_counter_ns() - cfg.glob.start_time_document
        self.action_error_code_last = error_code
        self.action_error_msg_last = error_msg
        self.action_error_no += 1
        self.action_status = cfg.glob.DOCUMENT_STATUS_ERROR

        self.persist_2_db()

        cfg.glob.base.base_action_code_last = self.action_action_code
        cfg.glob.base.base_error_code_last = self.action_error_code_last
        cfg.glob.base.base_error_no += 1
        cfg.glob.base.base_error_msg_last = self.action_error_msg_last
        cfg.glob.base.base_id_run_last = cfg.glob.run.run_id
        cfg.glob.base.base_status = cfg.glob.DOCUMENT_STATUS_ERROR

        cfg.glob.base.persist_2_db()  # type: ignore

        if self.action_action_code == db.cls_run.Run.ACTION_CODE_INBOX:
            utils.progress_msg(
                f"Duration: {round(self.action_duration_ns / 1000000000, 2):6.2f} s - "
                f"Document: {cfg.glob.base.base_id:6d} "
                f"[{cfg.glob.base.base_file_name}] - "
                f"Error: {error_msg}."
            )
        else:
            utils.progress_msg(
                f"Duration: {round(self.action_duration_ns / 1000000000, 2):6.2f} s - "
                f"Document: {cfg.glob.action_curr.action_id:6d} "
                f"[{cfg.glob.action_curr.action_file_name}] - "
                f"Error: {error_msg}."
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise from id.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_id(cls, id_action: int | sqlalchemy.Integer) -> Action:
        """Initialise from id."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            cfg.glob.DBT_ACTION,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )

        with cfg.glob.db_orm_engine.connect() as conn:  # type: ignore
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_action,
                )
            ).fetchone()
            conn.close()

        if row is None:
            utils.terminate_fatal(
                f"The action with id={id_action} does not exist in the database table 'action'",
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return Action.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Action:
        """Initialise from a database row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[cfg.glob.DBC_ID],
            action_code=row[cfg.glob.DBC_ACTION_CODE],
            action_text=row[cfg.glob.DBC_ACTION_TEXT],
            directory_name=row[cfg.glob.DBC_DIRECTORY_NAME],
            directory_type=row[cfg.glob.DBC_DIRECTORY_TYPE],
            duration_ns=row[cfg.glob.DBC_DURATION_NS],
            error_code_last=row[cfg.glob.DBC_ERROR_CODE_LAST],
            error_msg_last=row[cfg.glob.DBC_ERROR_MSG_LAST],
            error_no=row[cfg.glob.DBC_ERROR_NO],
            file_name=row[cfg.glob.DBC_FILE_NAME],
            file_size_bytes=row[cfg.glob.DBC_FILE_SIZE_BYTES],
            id_base=row[cfg.glob.DBC_ID_BASE],
            id_parent=row[cfg.glob.DBC_ID_PARENT],
            id_run_last=row[cfg.glob.DBC_ID_RUN_LAST],
            no_children=row[cfg.glob.DBC_NO_CHILDREN],
            no_pdf_pages=row[cfg.glob.DBC_NO_PDF_PAGES],
            status=row[cfg.glob.DBC_STATUS],
        )

    # -----------------------------------------------------------------------------
    # Get the database columns in a tuple.
    # -----------------------------------------------------------------------------
    def get_columns_in_tuple(
        self, is_duration_ns: bool = True, is_file_size_bytes: bool = True
    ) -> Tuple[Union[str, int, Integer, String], ...]:
        """Get the database columns in a tuple.

        Args:
            is_duration_ns (bool, optional): Including column duration_ns? Defaults to True.
            is_file_size_bytes (bool, optional): Including column file_size_bytes?. Defaults to True.

        Returns:
                Tuple[Union[str, int, Integer, String], ...]:
                        Column values in a tuple.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        column_01_05 = (
            self.action_id,
            self.action_action_code,
            self.action_action_text,
            self.action_directory_name,
            self.action_directory_type,
        )

        column_duration_ns = (self.action_duration_ns,)

        column_07_10 = (
            self.action_error_code_last,
            self.action_error_msg_last,
            self.action_error_no,
            self.action_file_name,
        )

        column_file_size_bytes = (self.action_file_size_bytes,)

        column_12_17 = (
            self.action_id_base,
            self.action_id_parent,
            self.action_id_run_last,
            self.action_no_children,
            self.action_no_pdf_pages,
            self.action_status,
        )

        columns = column_01_05 + (column_duration_ns + column_07_10 if is_duration_ns else column_07_10)

        return columns + (column_file_size_bytes + column_12_17 if is_file_size_bytes else column_12_17)

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    def get_file_type(self) -> str:
        """Get the file type from the file name.

        Returns:
            str: File type.
        """
        if self.action_file_name == "":
            return self.action_file_name

        return utils.get_file_type(utils.get_os_independent_name(self.action_file_name))

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
            directory_name=self.action_directory_name,
            file_name=self.action_file_name,
        )

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name.
    # -----------------------------------------------------------------------------
    def get_stem_name(self) -> str:
        """Get the stem name from the file name.

        Returns:
            str: Stem name.
        """
        if self.action_file_name == "":
            return self.action_file_name

        return utils.get_stem_name(str(self.action_file_name))

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        if self.action_id == 0:
            if self.action_file_size_bytes == 0:
                self.action_file_size_bytes = os.path.getsize(
                    utils.get_full_name(self.action_directory_name, self.action_file_name)
                )

            if self.action_no_pdf_pages == 0:
                self.action_no_pdf_pages = utils.get_pdf_pages_no(
                    utils.get_full_name(self.action_directory_name, self.action_file_name)
                )

            self.action_status = self.action_status if self.action_status != "" else cfg.glob.DOCUMENT_STATUS_START

            self.action_id = db.dml.insert_dbt_row(
                table_name=cfg.glob.DBT_ACTION,
                columns=self._get_columns(),
            )
        else:
            if self.action_id_parent == 1:
                if self.action_id_parent != self.action_id:
                    self.action_id_parent = self.action_id

            db.dml.update_dbt_id(
                table_name=cfg.glob.DBT_ACTION,
                id_where=self.action_id,
                columns=self._get_columns(),
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -----------------------------------------------------------------------------
    # Select unprocessed actions based on action_code.
    # -----------------------------------------------------------------------------
    @classmethod
    def select_action_by_action_code(cls, conn: Connection, action_code: str) -> sqlalchemy.engine.CursorResult:
        """Select unprocessed actions based on action_code.

        Args:
            conn (Connection): The database connection.
            action_code (str): The requested action code.

        Returns:
            sqlalchemy.engine.CursorResult: The rows found.
        """
        dbt = sqlalchemy.Table(cfg.glob.DBT_ACTION, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

        stmnt = (
            sqlalchemy.select(dbt)
            .where(
                sqlalchemy.and_(
                    dbt.c.action_code == action_code,
                    dbt.c.status.in_(
                        [
                            cfg.glob.DOCUMENT_STATUS_ERROR,
                            cfg.glob.DOCUMENT_STATUS_START,
                        ]
                    ),
                )
            )
            .order_by(dbt.c.id.asc())
        )

        cfg.glob.logger.debug("SQL Statement=%s", stmnt)

        return conn.execute(stmnt)

    # -----------------------------------------------------------------------------
    # Select unprocessed actions based on action_code und base id.
    # -----------------------------------------------------------------------------
    @classmethod
    def select_action_by_action_code_id_base(
        cls, conn: Connection, action_code: str, id_base: int
    ) -> sqlalchemy.engine.CursorResult:
        """Select unprocessed actions based on action_code und parent id.

        Args:
            conn (Connection): The database connection.
            action_code (str): The requested action code.
            id_base (int): The requested parent id.

        Returns:
            sqlalchemy.engine.CursorResult: The rows found.
        """
        dbt = sqlalchemy.Table(cfg.glob.DBT_ACTION, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

        stmnt = (
            sqlalchemy.select(dbt)
            .where(
                sqlalchemy.and_(
                    dbt.c.action_code == action_code,
                    dbt.c.id_base == id_base,
                    dbt.c.status.in_(
                        [
                            cfg.glob.DOCUMENT_STATUS_ERROR,
                            cfg.glob.DOCUMENT_STATUS_START,
                        ]
                    ),
                )
            )
            .order_by(dbt.c.id.asc())
        )

        cfg.glob.logger.debug("SQL Statement=%s", stmnt)

        return conn.execute(stmnt)

    # -----------------------------------------------------------------------------
    # Select parents with more than one unprocessed child based on action code.
    # -----------------------------------------------------------------------------
    @classmethod
    def select_id_base_by_action_code_pypdf2(cls, conn: Connection, action_code: str) -> sqlalchemy.engine.CursorResult:
        """Select parents with more than one unprocessed child based on action
        code.

        Args:
            conn (Connection): The database connection.
            action_code (str): The requested action code.

        Returns:
            sqlalchemy.engine.CursorResult: The rows found.
        """
        dbt = sqlalchemy.Table(cfg.glob.DBT_ACTION, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

        sub_query = (
            sqlalchemy.select(dbt.c.id_base)
            .where(dbt.c.action_code == action_code)
            .where(
                dbt.c.status.in_(
                    [
                        cfg.glob.DOCUMENT_STATUS_ERROR,
                        cfg.glob.DOCUMENT_STATUS_START,
                    ]
                )
            )
            .group_by(dbt.c.id_base)
            .having(sqlalchemy.func.count(dbt.c.id_base) > 1)
            .scalar_subquery()
        )

        stmnt = (
            sqlalchemy.select(sqlalchemy.func.min(dbt.c.id))
            .where(dbt.c.id_base.in_(sub_query))
            .where(dbt.c.action_code == action_code)
            .where(
                dbt.c.status.in_(
                    [
                        cfg.glob.DOCUMENT_STATUS_ERROR,
                        cfg.glob.DOCUMENT_STATUS_START,
                    ]
                )
            )
            .group_by(dbt.c.id_base)
            .order_by(dbt.c.id_base)
        )

        cfg.glob.logger.debug("SQL Statement=%s", stmnt)

        return conn.execute(stmnt)
