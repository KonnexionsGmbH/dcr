"""Module db.cls_action: Managing the database table action."""
from __future__ import annotations

import os
import time
from typing import ClassVar

import cfg.glob
import db.cls_db_core
import db.cls_document
import db.cls_run
import sqlalchemy
import utils
from sqlalchemy.engine import Connection

import dcr_core.cfg.glob
import dcr_core.utils


# pylint: disable=duplicate-code
# pylint: disable=too-many-instance-attributes
class Action:
    """Managing the database table action.

    Returns:
        _type_: Action instance.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    PDF2IMAGE_FILE_TYPE: ClassVar[str] = ""

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(  # pylint: disable=too-many-arguments
        self,
        action_code: str,
        id_run_last: int,
        _row_id: int = 0,
        action_text: str = "",
        directory_name: str = "",
        directory_type: str = "",
        duration_ns: int = 0,
        error_code_last: str = "",
        error_msg_last: str = "",
        error_no: int = 0,
        file_name: str = "",
        file_size_bytes: int = 0,
        id_document: int = 0,
        id_parent: int = 0,
        no_children: int = 0,
        no_pdf_pages: int = 0,
        status: str = "",
    ) -> None:
        """Initialise the instance.

        Args:
            action_code (str):
                    Action code.
            id_run_last (int):
                    Row id of the last run that processed this document action.
            _row_id (int, optional):
                    Row id. Defaults to 0.
            action_text (str, optional):
                    Action text (is derived from action_code if it is missing). Defaults to "".
            directory_name (str, optional):
                    The document location. Defaults to "".
            directory_type (str, optional):
                    The type of document location (accepted / rejected). Defaults to "".
            duration_ns (int, optional):
                    The processing time in nanoseconds. Defaults to 0.
            error_code_last (str, optional):
                    The code of the last error that occurred. Defaults to "".
            error_msg_last (str, optional):
                    The message of the last error that occurred. Defaults to "".
            error_no (int, optional):
                    The total number of errors in this document action. Defaults to 0.
            file_name (str, optional):
                    The file name. Defaults to "".
            file_size_bytes (int, optional):
                    The file size in bytes. Defaults to 0.
            id_document (int, optional):
                    The row id of the associated document. Defaults to 0.
            id_parent (int, optional):
                    The row id of the parent action. Defaults to 0.
            no_children (int, optional):
                    For a document of type scanned 'pdf', the number of image files created. Defaults to 0.
            no_pdf_pages (int, optional):
                    For a document of the type 'pdf' the number of pages. Defaults to 0.
            status (str, optional):
                    Status. Defaults to "".
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.check_exists_object(
            is_db_core=True,
            is_run=True,
        )

        self.action_action_code = action_code
        self.action_action_text = action_text
        self.action_directory_name = dcr_core.utils.get_os_independent_name(directory_name)
        self.action_directory_type = directory_type
        self.action_duration_ns = duration_ns
        self.action_error_code_last = error_code_last
        self.action_error_msg_last = error_msg_last
        self.action_error_no = error_no
        self.action_file_name = file_name
        self.action_file_size_bytes = file_size_bytes
        self.action_id = _row_id
        self.action_id_document = id_document
        self.action_id_parent = id_parent if id_parent != 0 else 1
        self.action_id_run_last = id_run_last
        self.action_no_children = no_children
        self.action_no_pdf_pages = no_pdf_pages
        self.action_status = status

        if Action.PDF2IMAGE_FILE_TYPE == "":
            Action.PDF2IMAGE_FILE_TYPE = dcr_core.cfg.glob.FILE_TYPE_JPEG

        if self.action_id == 0:
            self.persist_2_db()

        self._exist = True

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the database columns.
    # -----------------------------------------------------------------------------
    def _get_columns(self) -> db.cls_db_core.Columns:
        """Get the database columns.

        Returns:
            db.cls_db_core.Columns:
                    Database columns.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return {
            db.cls_db_core.DBCore.DBC_ACTION_CODE: self.action_action_code,
            db.cls_db_core.DBCore.DBC_ACTION_TEXT: cfg.glob.run.get_action_text(self.action_action_code),
            db.cls_db_core.DBCore.DBC_DIRECTORY_NAME: self.action_directory_name,
            db.cls_db_core.DBCore.DBC_DIRECTORY_TYPE: self.action_directory_type,
            db.cls_db_core.DBCore.DBC_DURATION_NS: self.action_duration_ns,
            db.cls_db_core.DBCore.DBC_ERROR_CODE_LAST: self.action_error_code_last,
            db.cls_db_core.DBCore.DBC_ERROR_MSG_LAST: self.action_error_msg_last,
            db.cls_db_core.DBCore.DBC_ERROR_NO: self.action_error_no,
            db.cls_db_core.DBCore.DBC_FILE_NAME: self.action_file_name,
            db.cls_db_core.DBCore.DBC_FILE_SIZE_BYTES: self.action_file_size_bytes,
            db.cls_db_core.DBCore.DBC_ID_DOCUMENT: self.action_id_document,
            db.cls_db_core.DBCore.DBC_ID_PARENT: self.action_id_parent,
            db.cls_db_core.DBCore.DBC_ID_RUN_LAST: self.action_id_run_last,
            db.cls_db_core.DBCore.DBC_NO_CHILDREN: self.action_no_children,
            db.cls_db_core.DBCore.DBC_NO_PDF_PAGES: self.action_no_pdf_pages,
            db.cls_db_core.DBCore.DBC_STATUS: self.action_status,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            db.cls_db_core.DBCore.DBT_ACTION,
            cfg.glob.db_core.db_orm_metadata,
            sqlalchemy.Column(
                db.cls_db_core.DBCore.DBC_ID,
                sqlalchemy.Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
            ),
            sqlalchemy.Column(
                db.cls_db_core.DBCore.DBC_CREATED_AT,
                sqlalchemy.DateTime,
            ),
            sqlalchemy.Column(
                db.cls_db_core.DBCore.DBC_MODIFIED_AT,
                sqlalchemy.DateTime,
            ),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_ACTION_CODE, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_ACTION_TEXT, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_DIRECTORY_NAME, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_DIRECTORY_TYPE, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_DURATION_NS, sqlalchemy.BigInteger, nullable=True),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_ERROR_CODE_LAST, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_ERROR_MSG_LAST, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_ERROR_NO, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_FILE_NAME, sqlalchemy.String, nullable=True),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_FILE_SIZE_BYTES, sqlalchemy.Integer, nullable=True),
            sqlalchemy.Column(
                db.cls_db_core.DBCore.DBC_ID_DOCUMENT,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(db.cls_db_core.DBCore.DBT_DOCUMENT + "." + db.cls_db_core.DBCore.DBC_ID, ondelete="CASCADE"),
                nullable=True,
            ),
            sqlalchemy.Column(
                db.cls_db_core.DBCore.DBC_ID_PARENT,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(db.cls_db_core.DBCore.DBT_ACTION + "." + db.cls_db_core.DBCore.DBC_ID, ondelete="CASCADE"),
                nullable=True,
            ),
            sqlalchemy.Column(
                db.cls_db_core.DBCore.DBC_ID_RUN_LAST,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(db.cls_db_core.DBCore.DBT_RUN + "." + db.cls_db_core.DBCore.DBC_ID, ondelete="CASCADE"),
                nullable=False,
            ),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_NO_CHILDREN, sqlalchemy.Integer, nullable=True),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_NO_PDF_PAGES, sqlalchemy.Integer, nullable=True),
            sqlalchemy.Column(db.cls_db_core.DBCore.DBC_STATUS, sqlalchemy.String, nullable=False),
        )

        utils.progress_msg(f"The database table '{db.cls_db_core.DBCore.DBT_ACTION}' has now been created")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

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
    # Finalise the current action.
    # -----------------------------------------------------------------------------
    def finalise(self) -> None:
        """Finalise the current action."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.action_duration_ns = time.perf_counter_ns() - cfg.glob.start_time_document

        self.action_status = db.cls_document.Document.DOCUMENT_STATUS_END

        self.persist_2_db()

        utils.check_exists_object(
            is_document=True,
        )

        cfg.glob.document.document_action_code_last = self.action_action_code
        cfg.glob.document.document_id_run_last = cfg.glob.run.run_id
        cfg.glob.document.document_status = db.cls_document.Document.DOCUMENT_STATUS_END

        cfg.glob.document.persist_2_db()  # type: ignore

        if self.action_action_code == db.cls_run.Run.ACTION_CODE_INBOX:
            utils.progress_msg(
                f"Duration: {round(self.action_duration_ns / 1000000000, 2):6.2f} s - "
                f"Document: {cfg.glob.document.document_id:6d} "
                f"[{cfg.glob.document.document_file_name}]"
            )
        else:
            utils.progress_msg(
                f"Duration: {round(self.action_duration_ns / 1000000000, 2):6.2f} s - " f"Document: {self.action_id:6d} " f"[{self.action_file_name}]"
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finalise the current action with error.
    # -----------------------------------------------------------------------------
    def finalise_error(self, error_code: str, error_msg: str) -> None:
        """Finalise the current action with error.

        Args:
            error_code (str):
                    Error code.
            error_msg (str):
                    Error message.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.action_duration_ns = time.perf_counter_ns() - cfg.glob.start_time_document
        self.action_error_code_last = error_code
        self.action_error_msg_last = error_msg
        self.action_error_no += 1
        self.action_status = db.cls_document.Document.DOCUMENT_STATUS_ERROR

        self.persist_2_db()

        utils.check_exists_object(
            is_document=True,
        )

        cfg.glob.document.document_action_code_last = self.action_action_code
        cfg.glob.document.document_error_code_last = self.action_error_code_last
        cfg.glob.document.document_error_no += 1
        cfg.glob.document.document_error_msg_last = self.action_error_msg_last
        cfg.glob.document.document_id_run_last = cfg.glob.run.run_id
        cfg.glob.document.document_status = db.cls_document.Document.DOCUMENT_STATUS_ERROR

        cfg.glob.document.persist_2_db()  # type: ignore

        if self.action_action_code == db.cls_run.Run.ACTION_CODE_INBOX:
            utils.progress_msg(
                f"Duration: {round(self.action_duration_ns / 1000000000, 2):6.2f} s - "
                f"Document: {cfg.glob.document.document_id:6d} "
                f"[{cfg.glob.document.document_file_name}] - "
                f"Error: {error_msg}."
            )
        else:
            utils.check_exists_object(
                is_action_curr=True,
            )

            cfg.glob.run.run_total_erroneous += 1

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
    def from_id(cls, id_action: int) -> Action:
        """Initialise from row id.

        Args:
            id_action (int):
                    The required row id.

        Returns:
            Action: The object instance found.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            db.cls_db_core.DBCore.DBT_ACTION,
            cfg.glob.db_core.db_orm_metadata,
            autoload_with=cfg.glob.db_core.db_orm_engine,
        )

        with cfg.glob.db_core.db_orm_engine.connect() as conn:
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_action,
                )
            ).fetchone()
            conn.close()

        if row is None:
            dcr_core.utils.terminate_fatal(
                f"The action with id={id_action} does not exist in the database table 'action'",
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return Action.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Action:
        """Initialise from a database row.

        Args:
            row (sqlalchemy.engine.Row):
                    A appropriate database row.

        Returns:
            Run:    The object instance matching the specified database row.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[db.cls_db_core.DBCore.DBC_ID],
            action_code=row[db.cls_db_core.DBCore.DBC_ACTION_CODE],
            action_text=row[db.cls_db_core.DBCore.DBC_ACTION_TEXT],
            directory_name=row[db.cls_db_core.DBCore.DBC_DIRECTORY_NAME],
            directory_type=row[db.cls_db_core.DBCore.DBC_DIRECTORY_TYPE],
            duration_ns=row[db.cls_db_core.DBCore.DBC_DURATION_NS],
            error_code_last=row[db.cls_db_core.DBCore.DBC_ERROR_CODE_LAST],
            error_msg_last=row[db.cls_db_core.DBCore.DBC_ERROR_MSG_LAST],
            error_no=row[db.cls_db_core.DBCore.DBC_ERROR_NO],
            file_name=row[db.cls_db_core.DBCore.DBC_FILE_NAME],
            file_size_bytes=row[db.cls_db_core.DBCore.DBC_FILE_SIZE_BYTES],
            id_document=row[db.cls_db_core.DBCore.DBC_ID_DOCUMENT],
            id_parent=row[db.cls_db_core.DBCore.DBC_ID_PARENT],
            id_run_last=row[db.cls_db_core.DBCore.DBC_ID_RUN_LAST],
            no_children=row[db.cls_db_core.DBCore.DBC_NO_CHILDREN],
            no_pdf_pages=row[db.cls_db_core.DBCore.DBC_NO_PDF_PAGES],
            status=row[db.cls_db_core.DBCore.DBC_STATUS],
        )

    # -----------------------------------------------------------------------------
    # Get the database columns in a tuple.
    # -----------------------------------------------------------------------------
    def get_columns_in_tuple(self, is_duration_ns: bool = True, is_file_size_bytes: bool = True) -> tuple[int | str, ...]:
        """Get the database columns in a tuple.

        Args:
            is_duration_ns (bool, optional):
                    Including column duration_ns?. Defaults to True.
            is_file_size_bytes (bool, optional):
                    Including column file_size_bytes?. Defaults to True.

        Returns:
            tuple[int | str, ...]:
                        Column values in a tuple.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        columns = [
            self.action_id,
            self.action_action_code,
            self.action_action_text,
            self.action_directory_name,
            self.action_directory_type,
        ]

        if is_duration_ns:
            columns.append(self.action_duration_ns)

        columns = columns + [
            self.action_error_code_last,
            self.action_error_msg_last,
            self.action_error_no,
            self.action_file_name,
        ]

        if is_file_size_bytes:
            columns.append(self.action_file_size_bytes)

        columns = columns + [
            self.action_id_document,
            self.action_id_parent,
            self.action_id_run_last,
            self.action_no_children,
            self.action_no_pdf_pages,
            self.action_status,
        ]

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return tuple(columns)  # type: ignore

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    def get_file_type(self) -> str:
        """Get the file type from the file name.

        Returns:
            str:    File type.
        """
        if self.action_file_name == "":
            return self.action_file_name

        return utils.get_file_type(dcr_core.utils.get_os_independent_name(self.action_file_name))

    # -----------------------------------------------------------------------------
    # Get the full file from a directory name or path and a file name or path.
    # -----------------------------------------------------------------------------
    def get_full_name(self) -> str:
        """Get the full file from a directory name or path and a file name or
        path.

        Returns:
            str:    Full file name.
        """
        return dcr_core.utils.get_full_name(
            directory_name=self.action_directory_name,
            file_name=self.action_file_name,
        )

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name.
    # -----------------------------------------------------------------------------
    def get_stem_name(self) -> str:
        """Get the stem name from the file name.

        Returns:
            str:    Stem name.
        """
        if self.action_file_name == "":
            return self.action_file_name

        return dcr_core.utils.get_stem_name(str(self.action_file_name))

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        full_name = dcr_core.utils.get_full_name(self.action_directory_name, self.action_file_name)
        if os.path.exists(full_name):
            if self.action_file_size_bytes == 0:
                self.action_file_size_bytes = os.path.getsize(full_name)

            if self.action_no_pdf_pages == 0:
                self.action_no_pdf_pages = utils.get_pdf_pages_no(full_name)

        if self.action_id == 0:
            self.action_status = self.action_status if self.action_status != "" else db.cls_document.Document.DOCUMENT_STATUS_START

            self.action_id = cfg.glob.db_core.insert_dbt_row(  # type: ignore
                table_name=db.cls_db_core.DBCore.DBT_ACTION,
                columns=self._get_columns(),
            )
        else:
            if self.action_id_parent == 1:
                if self.action_id_parent != self.action_id:
                    self.action_id_parent = self.action_id

            cfg.glob.db_core.update_dbt_id(  # type: ignore
                table_name=db.cls_db_core.DBCore.DBT_ACTION,
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
            conn (Connection):
                    The database connection.
            action_code (str):
                    The requested action code.

        Returns:
            sqlalchemy.engine.CursorResult:
                    The rows found.
        """
        dbt = sqlalchemy.Table(
            db.cls_db_core.DBCore.DBT_ACTION,
            cfg.glob.db_core.db_orm_metadata,
            autoload_with=cfg.glob.db_core.db_orm_engine,
        )

        stmnt = (
            sqlalchemy.select(dbt)
            .where(
                sqlalchemy.and_(
                    dbt.c.action_code == action_code,
                    dbt.c.status.in_(
                        [
                            db.cls_document.Document.DOCUMENT_STATUS_ERROR,
                            db.cls_document.Document.DOCUMENT_STATUS_START,
                        ]
                    ),
                )
            )
            .order_by(dbt.c.id.asc())
        )

        cfg.glob.logger.debug("SQL Statement=%s", stmnt)

        return conn.execute(stmnt)

    # -----------------------------------------------------------------------------
    # Select unprocessed actions based on action_code und document id.
    # -----------------------------------------------------------------------------
    @classmethod
    def select_action_by_action_code_id_document(cls, conn: Connection, action_code: str, id_document: int) -> sqlalchemy.engine.CursorResult:
        """Select unprocessed actions based on action_code und parent id.

        Args:
            conn (Connection):
                    The database connection.
            action_code (str):
                    The requested action code.
            id_document (int):
                    The requested parent id.

        Returns:
            sqlalchemy.engine.CursorResult:
                    The rows found.
        """
        dbt = sqlalchemy.Table(
            db.cls_db_core.DBCore.DBT_ACTION,
            cfg.glob.db_core.db_orm_metadata,
            autoload_with=cfg.glob.db_core.db_orm_engine,
        )

        stmnt = (
            sqlalchemy.select(dbt)
            .where(
                sqlalchemy.and_(
                    dbt.c.action_code == action_code,
                    dbt.c.id_document == id_document,
                    dbt.c.status.in_(
                        [
                            db.cls_document.Document.DOCUMENT_STATUS_ERROR,
                            db.cls_document.Document.DOCUMENT_STATUS_START,
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
    def select_id_document_by_action_code_pypdf2(cls, conn: Connection, action_code: str) -> sqlalchemy.engine.CursorResult:
        """Select parents with more than one unprocessed child based on action
        code.

        Args:
            conn (Connection):
                    The database connection.
            action_code (str):
                    The requested action code.

        Returns:
            sqlalchemy.engine.CursorResult:
                    The rows found.
        """
        dbt = sqlalchemy.Table(
            db.cls_db_core.DBCore.DBT_ACTION,
            cfg.glob.db_core.db_orm_metadata,
            autoload_with=cfg.glob.db_core.db_orm_engine,
        )

        sub_query = (
            sqlalchemy.select(dbt.c.id_document)
            .where(dbt.c.action_code == action_code)
            .where(
                dbt.c.status.in_(
                    [
                        db.cls_document.Document.DOCUMENT_STATUS_ERROR,
                        db.cls_document.Document.DOCUMENT_STATUS_START,
                    ]
                )
            )
            .group_by(dbt.c.id_document)
            .having(sqlalchemy.func.count(dbt.c.id_document) > 1)
            .scalar_subquery()
        )

        stmnt = (
            sqlalchemy.select(sqlalchemy.func.min(dbt.c.id))
            .where(dbt.c.id_document.in_(sub_query))
            .where(dbt.c.action_code == action_code)
            .where(
                dbt.c.status.in_(
                    [
                        db.cls_document.Document.DOCUMENT_STATUS_ERROR,
                        db.cls_document.Document.DOCUMENT_STATUS_START,
                    ]
                )
            )
            .group_by(dbt.c.id_document)
            .order_by(dbt.c.id_document)
        )

        cfg.glob.logger.debug("SQL Statement=%s", stmnt)

        return conn.execute(stmnt)
