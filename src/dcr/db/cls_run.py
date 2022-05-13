"""Module db.cls_run: Managing the run statistics."""
from __future__ import annotations

from typing import ClassVar

import cfg.glob
import db.cls_run
import db.dml
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
import utils


# pylint: disable=R0801
# pylint: disable=R0902
class Run:
    """Managing the run data.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    # _ACTION_TEXT_CREATE_DB: ClassVar[str] = "Create Database"
    _ACTION_TEXT_INBOX: ClassVar[str] = "inbox       (preprocessor)"
    _ACTION_TEXT_PANDOC: ClassVar[str] = "pandoc      (preprocessor)"
    _ACTION_TEXT_PARSER: ClassVar[str] = "parser      (nlp)"
    _ACTION_TEXT_PARSER_LINE: ClassVar[str] = "parser_line (nlp)"
    _ACTION_TEXT_PARSER_WORD: ClassVar[str] = "parser_word (nlp)"
    _ACTION_TEXT_PDF2IMAGE: ClassVar[str] = "pdf2image   (preprocessor)"
    _ACTION_TEXT_PDFLIB: ClassVar[str] = "pdflib      (nlp)"
    _ACTION_TEXT_PYPDF2: ClassVar[str] = "pypdf2      (preprocessor)"
    _ACTION_TEXT_TESSERACT: ClassVar[str] = "tesseract   (preprocessor)"
    _ACTION_TEXT_TOKENIZE: ClassVar[str] = "tokenize    (nlp)"
    _ACTION_TEXT_UPGRADE_DB: ClassVar[str] = "Upgrade Database"

    ACTION_CODE_ALL_COMPLETE: ClassVar[str] = "all"
    ACTION_CODE_CREATE_DB: ClassVar[str] = "db_c"
    ACTION_CODE_INBOX: ClassVar[str] = "p_i"
    ACTION_CODE_PANDOC: ClassVar[str] = "n_2_p"
    ACTION_CODE_PARSER: ClassVar[str] = "s_p_j"
    ACTION_CODE_PARSER_LINE: ClassVar[str] = "s_p_j_line"
    ACTION_CODE_PARSER_WORD: ClassVar[str] = "s_p_j_word"
    ACTION_CODE_PDF2IMAGE: ClassVar[str] = "p_2_i"
    ACTION_CODE_PDFLIB: ClassVar[str] = "tet"
    ACTION_CODE_PYPDF2: ClassVar[str] = "pypdf2"
    ACTION_CODE_TESSERACT: ClassVar[str] = "ocr"
    ACTION_CODE_TOKENIZE: ClassVar[str] = "tkn"
    ACTION_CODE_UPGRADE_DB: ClassVar[str] = "db_u"

    id_run_umbrella: ClassVar[int] = 0

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(  # pylint: disable=R0913
        self,
        _row_id: int | sqlalchemy.Integer = 0,
        action_code: str = "",
        action_text: str = "",
        id_run: int | sqlalchemy.Integer = id_run_umbrella,
        status: str | sqlalchemy.String = "",
        total_erroneous: int | sqlalchemy.Integer = 0,
        total_processed_ok: int | sqlalchemy.Integer = 0,
        total_processed_to_be: int | sqlalchemy.Integer = 0,
    ) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        if Run.id_run_umbrella == 0:
            Run.id_run_umbrella = Run.get_id_latest() + 1

        self.run_action_code: str = action_code
        self.run_action_text: str = action_text
        self.run_id: int | sqlalchemy.Integer = _row_id

        self.run_id_run: int | sqlalchemy.Integer = id_run

        if self.run_id_run == 0:
            self.run_id_run = Run.id_run_umbrella

        self.run_status: str | sqlalchemy.String = status
        self.run_total_erroneous: int | sqlalchemy.Integer = total_erroneous
        self.run_total_processed_ok: int | sqlalchemy.Integer = total_processed_ok
        self.run_total_processed_to_be: int | sqlalchemy.Integer = total_processed_to_be

        if self.run_id == 0:
            self.persist_2_db()

        self.total_generated: int = 0
        self.total_processed_pandoc: int = 0
        self.total_processed_pdf2image: int = 0
        self.total_processed_pdflib: int = 0
        self.total_processed_tesseract: int = 0
        self.total_status_error: int = 0
        self.total_status_ready: int = 0

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
            cfg.glob.DBC_ACTION_CODE: self.run_action_code,
            cfg.glob.DBC_ACTION_TEXT: Run.get_action_text(self.run_action_code),
            cfg.glob.DBC_ID_RUN: self.run_id_run,
            cfg.glob.DBC_STATUS: self.run_status,
            cfg.glob.DBC_TOTAL_ERRONEOUS: self.run_total_erroneous,
            cfg.glob.DBC_TOTAL_PROCESSED_OK: self.run_total_processed_ok,
            cfg.glob.DBC_TOTAL_PROCESSED_TO_BE: self.run_total_processed_to_be,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            cfg.glob.DBT_RUN,
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
            sqlalchemy.Column(cfg.glob.DBC_ID_RUN, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(cfg.glob.DBC_STATUS, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(
                cfg.glob.DBC_TOTAL_ERRONEOUS,
                sqlalchemy.Integer,
                nullable=True,
            ),
            sqlalchemy.Column(
                cfg.glob.DBC_TOTAL_PROCESSED_OK,
                sqlalchemy.Integer,
                nullable=True,
            ),
            sqlalchemy.Column(
                cfg.glob.DBC_TOTAL_PROCESSED_TO_BE,
                sqlalchemy.Integer,
                nullable=True,
            ),
        )

        utils.progress_msg(f"The database table '{cfg.glob.DBT_RUN}' has now been created")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finalise the current row.
    # -----------------------------------------------------------------------------
    def finalise(self) -> None:
        """Finalise the current row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.run_status = cfg.glob.DOCUMENT_STATUS_END

        self.persist_2_db()

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise from id.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_id(cls, id_run: int | sqlalchemy.Integer) -> Run:
        """Initialise from id."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            cfg.glob.DBT_RUN,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )

        with cfg.glob.db_orm_engine.connect() as conn:  # type: ignore
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_run,
                )
            ).fetchone()
            conn.close()

        if row == ():
            utils.terminate_fatal(
                f"The run with id={id_run} does not exist in the database table 'run'",
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return Run.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Run:
        """Initialise from a database row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[cfg.glob.DBC_ID],
            action_code=row[cfg.glob.DBC_ACTION_CODE],
            action_text=row[cfg.glob.DBC_ACTION_TEXT],
            id_run=row[cfg.glob.DBC_ID_RUN],
            status=row[cfg.glob.DBC_STATUS],
            total_erroneous=row[cfg.glob.DBC_TOTAL_ERRONEOUS],
            total_processed_ok=row[cfg.glob.DBC_TOTAL_PROCESSED_OK],
            total_processed_to_be=row[cfg.glob.DBC_TOTAL_PROCESSED_TO_BE],
        )

    # -----------------------------------------------------------------------------
    # Get the action text from the action code.
    # -----------------------------------------------------------------------------
    @classmethod
    def get_action_text(cls, action_code: str) -> str:
        """Get the action text from the action code.

        Args:
            action_code (str): Action code.

        Returns:
            str: Action text.
        """
        action_text: str = cfg.glob.INFORMATION_NOT_YET_AVAILABLE

        match action_code:
            # wwe
            # case Run.ACTION_CODE_CREATE_DB:
            #     action_text = Run._ACTION_TEXT_CREATE_DB
            case Run.ACTION_CODE_INBOX:
                action_text = Run._ACTION_TEXT_INBOX
            case Run.ACTION_CODE_PANDOC:
                action_text = Run._ACTION_TEXT_PANDOC
            case Run.ACTION_CODE_PARSER:
                action_text = Run._ACTION_TEXT_PARSER
            case Run.ACTION_CODE_PARSER_LINE:
                action_text = Run._ACTION_TEXT_PARSER_LINE
            case Run.ACTION_CODE_PARSER_WORD:
                action_text = Run._ACTION_TEXT_PARSER_WORD
            case Run.ACTION_CODE_PDF2IMAGE:
                action_text = Run._ACTION_TEXT_PDF2IMAGE
            case Run.ACTION_CODE_PDFLIB:
                action_text = Run._ACTION_TEXT_PDFLIB
            case Run.ACTION_CODE_PYPDF2:
                action_text = Run._ACTION_TEXT_PYPDF2
            case Run.ACTION_CODE_TESSERACT:
                action_text = Run._ACTION_TEXT_TESSERACT
            case Run.ACTION_CODE_TOKENIZE:
                action_text = Run._ACTION_TEXT_TOKENIZE
            case Run.ACTION_CODE_UPGRADE_DB:
                action_text = Run._ACTION_TEXT_UPGRADE_DB
            case _:
                utils.terminate_fatal(
                    f"Action code {action_code} is not supported in function get_action_text()",
                )

        return action_text

    # -----------------------------------------------------------------------------
    # Get the latest id from database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def get_id_latest(cls) -> int:
        """Get the latest id from database table.

        Returns:
            int: Latest id.
        """
        dbt = sqlalchemy.Table(cfg.glob.DBT_RUN, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

        with cfg.glob.db_orm_engine.connect() as conn:  # type: ignore
            row = conn.execute(sqlalchemy.select(sqlalchemy.func.max(dbt.c.id_run))).fetchone()
            conn.close()

        if row == (None,):
            return 0

        return row[0]  # type: ignore

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        if self.run_id == 0:
            self.run_id = db.dml.insert_dbt_row(
                cfg.glob.DBT_RUN,
                self._get_columns(),
            )
            return

        if self.run_total_erroneous == 0 and self.run_total_processed_ok == 0 and self.run_total_processed_to_be == 0:
            db.dml.delete_dbt_id(
                table_name=cfg.glob.DBT_RUN,
                id_where=self.run_id,
            )
        else:
            db.dml.update_dbt_id(
                table_name=cfg.glob.DBT_RUN,
                id_where=self.run_id,
                columns=self._get_columns(),
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
