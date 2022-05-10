"""Module db.action: Managing the document processing steps."""
import os
import pathlib
import time

import cfg.glob
import db.dml
import sqlalchemy
import utils


# pylint: disable=R0801
# pylint: disable=R0902
# pylint: disable=R0903
class Action:
    """Managing the document processing steps.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(  # pylint: disable=R0913, R0914
        self,
        action_code: str = "",
        action_id: int | sqlalchemy.Integer = 0,
        directory_name: str = "",
        directory_type: str = "",
        duration_ns: int = 0,
        error_code: str | sqlalchemy.String = "",
        error_msg: str | sqlalchemy.String = "",
        error_no: int = 0,
        file_name: str = "",
        file_size_bytes: int = 0,
        id_base: int | sqlalchemy.Integer = 0,
        id_parent: int | sqlalchemy.Integer = 0,
        id_run_last: int | sqlalchemy.Integer = 0,
        no_children: int | sqlalchemy.Integer = 0,
        no_pdf_pages: int = 0,
        status: str | sqlalchemy.String = "",
    ) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.action_action_code: str = action_code
        self.action_directory_name: str = directory_name
        self.action_directory_type: str | sqlalchemy.String = directory_type
        self.action_duration_ns: int | sqlalchemy.BigInteger = duration_ns
        self.action_error_code_last: str | sqlalchemy.String = error_code
        self.action_error_msg_last: str | sqlalchemy.String = error_msg
        self.action_error_no: int = error_no
        self.action_file_name: str = file_name
        self.action_file_size_bytes: int = file_size_bytes
        self.action_id: int | sqlalchemy.Integer = action_id
        self.action_id_base: int | sqlalchemy.Integer = id_base
        self.action_id_parent: int | sqlalchemy.Integer = id_parent if id_parent !=0 else 1
        self.action_id_run_last: int | sqlalchemy.Integer = id_run_last
        self.action_no_children: int | sqlalchemy.Integer = no_children
        self.action_no_pdf_pages: int = no_pdf_pages
        self.action_status: str | sqlalchemy.String = status if status != "" else cfg.glob.DOCUMENT_STATUS_START

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the database columns.
    # -----------------------------------------------------------------------------
    def _get_columns(self) -> db.utils.Columns:
        """Get the database columns.

        Returns:
            db.utils.Columns: Database columns.
        """
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
    # Update the current row.
    # -----------------------------------------------------------------------------
    def _update(self) -> None:
        """Update the current row."""
        if self.action_id_parent == 1:
            if self.action_id_parent != self.action_id:
                self.action_id_parent = self.action_id

        db.dml.update_dbt_id(
            table_name=cfg.glob.DBT_ACTION,
            id_where=self.action_id,
            columns=self._get_columns(),
        )

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
        self.action_duration_ns = time.perf_counter_ns() - cfg.glob.start_time_document

        if self.action_file_size_bytes == 0:
            self.action_file_size_bytes = os.path.getsize(
                pathlib.Path(self.action_directory_name, self.action_file_name)
            )

        if self.action_no_pdf_pages == 0:
            self.action_no_pdf_pages = utils.get_pdf_pages_no(
                str(pathlib.Path(self.action_directory_name, self.action_file_name))
            )

        self.action_status = cfg.glob.DOCUMENT_STATUS_END

        self._update()

        cfg.glob.base.base_action_code_last = self.action_action_code
        cfg.glob.base.base_id_run_last = cfg.glob.run.run_id
        cfg.glob.base.base_status = cfg.glob.DOCUMENT_STATUS_END

        cfg.glob.base.update()

        utils.progress_msg(
            f"Duration: {round(self.action_duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {self.action_id_parent:6d} "
            f"[{self.action_file_name}]"
        )

    # -----------------------------------------------------------------------------
    # Finalise the current action with error.
    # -----------------------------------------------------------------------------
    def finalise_error(self, error_code: str, error_msg: str) -> None:
        """Finalise the current action with error.

        Args:
            error_code (str)                : Error code.
            error_msg (str)                 : Error message.
        """
        self.action_duration_ns = time.perf_counter_ns() - cfg.glob.start_time_document
        self.action_error_code_last = error_code
        self.action_error_msg_last = error_msg
        self.action_error_no += 1
        self.action_status = cfg.glob.DOCUMENT_STATUS_ERROR

        self._update()

        cfg.glob.base.base_action_code_last = self.action_action_code
        cfg.glob.base.base_error_code_last = self.action_error_code_last
        cfg.glob.base.base_error_no += 1
        cfg.glob.base.base_error_msg_last = self.action_error_msg_last
        cfg.glob.base.base_id_run_last = cfg.glob.run.run_id
        cfg.glob.base.base_status = cfg.glob.DOCUMENT_STATUS_ERROR

        cfg.glob.base.update()

        utils.progress_msg(
            f"Duration: {round(self.action_duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {cfg.glob.base.base_id:6d} "
            f"[{cfg.glob.base.base_file_name}] - "
            f"Error: {error_msg} "
        )

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    def get_file_type(self) -> str | None:
        """Get the file type from the file name.

        Returns:
            str | None: File type.
        """
        if self.action_file_name is None:
            return None

        return utils.get_file_type(pathlib.Path(str(self.action_file_name)))

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name.
    # -----------------------------------------------------------------------------
    def get_in_stem_name(self) -> str | None:
        """Get the stem name from the file name.

        Returns:
            str | None: Stem name.
        """
        if self.action_file_name is None:
            return None

        return utils.get_stem_name(str(self.action_file_name))

    # -----------------------------------------------------------------------------
    # Insert a new row.
    # -----------------------------------------------------------------------------
    def insert(self) -> None:
        """Insert a new row."""
        self.action_id = db.dml.insert_dbt_row(
            table_name=cfg.glob.DBT_ACTION,
            columns=self._get_columns(),
        )
