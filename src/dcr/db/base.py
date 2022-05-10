"""Module db.base: Managing the document status."""
import os
import pathlib

import cfg.glob
import db.dml
import db.run
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
        action_code_last: str = "",
        base_id: int | sqlalchemy.Integer = 0,
        directory_name: str = "",
        error_code: str | sqlalchemy.String = "",
        error_msg: str | sqlalchemy.String = "",
        error_no: int = 0,
        file_name: str = "",
        id_language: int | sqlalchemy.Integer = 0,
        id_run_last: int | sqlalchemy.Integer = 0,
        sha256: str | sqlalchemy.String = "",
            status: str | sqlalchemy.String = "",
    ) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.base_action_code_last: str = action_code_last
        self.base_directory_name: str | sqlalchemy.String = directory_name
        self.base_error_code_last: str | sqlalchemy.String = error_code
        self.base_error_msg_last: str | sqlalchemy.String = error_msg
        self.base_error_no: int = error_no
        self.base_file_name: str = file_name
        self.base_file_size_bytes: int = os.path.getsize(pathlib.Path(directory_name, file_name))
        self.base_id: int | sqlalchemy.Integer = base_id
        self.base_id_language: int | sqlalchemy.Integer = id_language
        self.base_id_run_last: int | sqlalchemy.Integer = id_run_last
        self.base_no_pdf_pages: int = utils.get_pdf_pages_no(str(pathlib.Path(directory_name, file_name)))
        self.base_sha256: str | sqlalchemy.String = sha256
        self.base_status: str | sqlalchemy.String = status if status != "" else cfg.glob.DOCUMENT_STATUS_START

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
            cfg.glob.DBC_ACTION_CODE_LAST: self.base_action_code_last,
            cfg.glob.DBC_ACTION_TEXT_LAST: db.run.Run.get_action_text(self.base_action_code_last),
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
    # Update the current row.
    # -----------------------------------------------------------------------------
    def _update(self) -> None:
        """Update the current row."""
        db.dml.update_dbt_id(
            table_name=cfg.glob.DBT_BASE,
            id_where=self.base_id,
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
        self.base_status = cfg.glob.DOCUMENT_STATUS_END

        self._update()

    # -----------------------------------------------------------------------------
    # Finalise the current row with error.
    # -----------------------------------------------------------------------------
    def finalise_error(self, error_code: str, error_msg: str) -> None:
        """Finalise the current row with error.

        Args:
            error_code (str)                : Error code.
            error_msg (str)                 : Error message.
        """
        self.base_error_code_last = error_code
        self.base_error_msg_last = error_msg
        self.base_error_no += 1
        self.base_status = cfg.glob.DOCUMENT_STATUS_ERROR

        self._update()

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    def get_file_type(self) -> str | None:
        """Get the file type from the file name.

        Returns:
            str | None: File type.
        """
        if self.base_file_name is None:
            return None

        return utils.get_file_type(pathlib.Path(str(self.base_file_name)))

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name.
    # -----------------------------------------------------------------------------
    def get_stem_name(self) -> str | None:
        """Get the stem name from the file name.

        Returns:
            str | None: Stem name.
        """
        if self.base_file_name is None:
            return None

        return utils.get_stem_name(str(self.base_file_name))

    # -----------------------------------------------------------------------------
    # Insert a new row.
    # -----------------------------------------------------------------------------
    def insert(self) -> None:
        """Insert a new row."""
        self.base_id = db.dml.insert_dbt_row(
            table_name=cfg.glob.DBT_BASE,
            columns=self._get_columns(),
        )

    # -----------------------------------------------------------------------------
    # Update the current row.
    # -----------------------------------------------------------------------------
    def update(self) -> None:
        """Update the current row."""
        db.dml.update_dbt_id(
            table_name=cfg.glob.DBT_BASE,
            id_where=self.base_id,
            columns=self._get_columns(),
        )
