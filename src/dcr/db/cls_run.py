# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module dcr.db.cls_run: Managing the database table run."""
from __future__ import annotations

from typing import ClassVar

import dcr_core.core_glob
import dcr_core.core_utils
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
from sqlalchemy import Integer
from sqlalchemy import String

import dcr.cfg.glob
import dcr.db.cls_db_core
import dcr.utils


# pylint: disable=duplicate-code
# pylint: disable=too-many-instance-attributes
class Run:
    """Managing the database table run.

    Returns:
        _type_: Run instance.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    # _ACTION_TEXT_CREATE_DB: ClassVar[str] = "Create Database"
    _ACTION_TEXT_EXPORT_LT_RULES: ClassVar[str] = "export_lt_rules"
    _ACTION_TEXT_INBOX: ClassVar[str] = "inbox         (preprocessor)"
    _ACTION_TEXT_PANDOC: ClassVar[str] = "pandoc        (preprocessor)"
    _ACTION_TEXT_PARSER: ClassVar[str] = "parser        (nlp)"
    _ACTION_TEXT_PARSER_LINE: ClassVar[str] = "parser_line   (nlp)"
    _ACTION_TEXT_PARSER_PAGE: ClassVar[str] = "parser_page   (nlp)"
    _ACTION_TEXT_PARSER_WORD: ClassVar[str] = "parser_word   (nlp)"
    _ACTION_TEXT_PDF2IMAGE: ClassVar[str] = "pdf2image     (preprocessor)"
    _ACTION_TEXT_PDFLIB: ClassVar[str] = "pdflib        (nlp)"
    _ACTION_TEXT_PYPDF2: ClassVar[str] = "pypdf2        (preprocessor)"
    _ACTION_TEXT_TESSERACT: ClassVar[str] = "tesseract     (preprocessor)"
    _ACTION_TEXT_TOKENIZE: ClassVar[str] = "tokenizer     (nlp)"
    _ACTION_TEXT_TOKENIZE_LINE: ClassVar[str] = "tokenize_line (nlp)"
    _ACTION_TEXT_UPGRADE_DB: ClassVar[str] = "Upgrade Database"

    ACTION_CODE_ALL_COMPLETE: ClassVar[str] = "all"
    ACTION_CODE_CREATE_DB: ClassVar[str] = "db_c"
    ACTION_CODE_EXPORT_LT_RULES: ClassVar[str] = "e_lt"
    ACTION_CODE_INBOX: ClassVar[str] = "p_i"
    ACTION_CODE_PANDOC: ClassVar[str] = "n_2_p"
    ACTION_CODE_PARSER: ClassVar[str] = "s_p_j"
    ACTION_CODE_PARSER_LINE: ClassVar[str] = "s_p_j_line"
    ACTION_CODE_PARSER_PAGE: ClassVar[str] = "s_p_j_page"
    ACTION_CODE_PARSER_WORD: ClassVar[str] = "s_p_j_word"
    ACTION_CODE_PDF2IMAGE: ClassVar[str] = "p_2_i"
    ACTION_CODE_PDFLIB: ClassVar[str] = "tet"
    ACTION_CODE_PYPDF2: ClassVar[str] = "pypdf2"
    ACTION_CODE_TESSERACT: ClassVar[str] = "ocr"
    ACTION_CODE_TOKENIZE: ClassVar[str] = "tkn"
    ACTION_CODE_TOKENIZE_LINE: ClassVar[str] = "tkn_line"
    ACTION_CODE_UPGRADE_DB: ClassVar[str] = "db_u"

    ID_RUN_UMBRELLA: ClassVar[int] = 0

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(
        self,
        action_code: str,
        _row_id: int = 0,
        action_text: str = "",
        id_run: int = ID_RUN_UMBRELLA,
        status: str = "",
        total_erroneous: int = 0,
        total_processed_ok: int = 0,
        total_processed_to_be: int = 0,
    ) -> None:
        """Initialise the instance.

        Args:
            action_code (str):
                    Action code.
            _row_id (int, optional):
                    Row id. Defaults to 0.
            action_text (str, optional):
                    Action text (is derived from action_code if it is missing). Defaults to "".
            id_run (int, optional):
                    Row id of the triggering run. Defaults to id_run_umbrella.
            status (str, optional):
                    Status. Defaults to "".
            total_erroneous (int, optional):
                    Total number of erroneous documents. Defaults to 0.
            total_processed_ok (int, optional):
                    Total number of correctly processed documents. Defaults to 0.
            total_processed_to_be (int, optional):
                    Total number of documents to be processed. Defaults to 0.
        """
        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dcr.utils.check_exists_object(
            is_db_core=True,
        )

        if Run.ID_RUN_UMBRELLA == 0:
            Run.ID_RUN_UMBRELLA = Run.get_id_latest() + 1

        self.run_action_code = action_code
        self.run_action_text = action_text
        self.run_id = _row_id

        self.run_id_run = id_run

        if self.run_id_run == 0:
            self.run_id_run = Run.ID_RUN_UMBRELLA

        self.run_status = status
        self.run_total_erroneous = total_erroneous
        self.run_total_processed_ok = total_processed_ok
        self.run_total_processed_to_be = total_processed_to_be

        if self.run_id == 0:
            self.persist_2_db()

        self.total_generated = 0
        self.total_processed_pandoc = 0
        self.total_processed_pdf2image = 0
        self.total_processed_pdflib = 0
        self.total_processed_tesseract = 0
        self.total_status_error = 0
        self.total_status_ready = 0

        self._exist = True

        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the database columns.
    # -----------------------------------------------------------------------------
    def _get_columns(self) -> dcr.db.cls_db_core.Columns:
        """Get the database columns.

        Returns:
            dcr.db.cls_db_core.Columns:
                    Database columns.
        """
        self.run_action_text = Run.get_action_text(self.run_action_code)

        return {
            dcr.db.cls_db_core.DBCore.DBC_ACTION_CODE: self.run_action_code,
            dcr.db.cls_db_core.DBCore.DBC_ACTION_TEXT: self.run_action_text,
            dcr.db.cls_db_core.DBCore.DBC_ID_RUN: self.run_id_run,
            dcr.db.cls_db_core.DBCore.DBC_STATUS: self.run_status,
            dcr.db.cls_db_core.DBCore.DBC_TOTAL_ERRONEOUS: self.run_total_erroneous,
            dcr.db.cls_db_core.DBCore.DBC_TOTAL_PROCESSED_OK: self.run_total_processed_ok,
            dcr.db.cls_db_core.DBCore.DBC_TOTAL_PROCESSED_TO_BE: self.run_total_processed_to_be,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_RUN,
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
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_ACTION_CODE, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_ACTION_TEXT, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_ID_RUN, sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_STATUS, sqlalchemy.String, nullable=False),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_TOTAL_ERRONEOUS,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_TOTAL_PROCESSED_OK,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_TOTAL_PROCESSED_TO_BE,
                sqlalchemy.Integer,
                nullable=False,
            ),
        )

        dcr.utils.progress_msg(f"The database table '{dcr.db.cls_db_core.DBCore.DBT_RUN}' has now been created")

        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

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
        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        self.run_status = dcr.db.cls_document.Document.DOCUMENT_STATUS_END

        self.persist_2_db()

        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise from id.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_id(cls, id_run: int) -> Run:
        """Initialise from row id.

        Args:
            id_run (int):
                    The required row id.

        Returns:
            Run:    The object instance found.
        """
        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        # dcr_core.core_glob.logger.debug("param id_run=%i", id_run)

        dbt = sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_RUN,
            dcr.cfg.glob.db_core.db_orm_metadata,
            autoload_with=dcr.cfg.glob.db_core.db_orm_engine,
        )

        with dcr.cfg.glob.db_core.db_orm_engine.connect() as conn:
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_run,
                )
            ).fetchone()
            conn.close()

        if row is None:
            dcr_core.core_utils.terminate_fatal(
                f"The run with id={id_run} does not exist in the database table 'run'",
            )

        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return Run.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Run:
        """Initialise from a database row.

        Args:
            row (sqlalchemy.engine.Row):
                    A appropriate database row.

        Returns:
            Run:    The object instance matching the specified database row.
        """
        return cls(
            _row_id=row[dcr.db.cls_db_core.DBCore.DBC_ID],
            action_code=row[dcr.db.cls_db_core.DBCore.DBC_ACTION_CODE],
            action_text=row[dcr.db.cls_db_core.DBCore.DBC_ACTION_TEXT],
            id_run=row[dcr.db.cls_db_core.DBCore.DBC_ID_RUN],
            status=row[dcr.db.cls_db_core.DBCore.DBC_STATUS],
            total_erroneous=row[dcr.db.cls_db_core.DBCore.DBC_TOTAL_ERRONEOUS],
            total_processed_ok=row[dcr.db.cls_db_core.DBCore.DBC_TOTAL_PROCESSED_OK],
            total_processed_to_be=row[dcr.db.cls_db_core.DBCore.DBC_TOTAL_PROCESSED_TO_BE],
        )

    # -----------------------------------------------------------------------------
    # Get the action text from the action code.
    # -----------------------------------------------------------------------------
    @classmethod
    def get_action_text(cls, action_code: str) -> str:
        """Get the action text from the action code.

        Args:
            action_code (str):
                    Action code.

        Returns:
            str:    Action text.
        """
        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        # dcr_core.core_glob.logger.debug("param action_code=%s", action_code)

        action_text = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE

        match action_code:
            case Run.ACTION_CODE_INBOX:
                action_text = Run._ACTION_TEXT_INBOX
            case Run.ACTION_CODE_PANDOC:
                action_text = Run._ACTION_TEXT_PANDOC
            case Run.ACTION_CODE_PARSER:
                action_text = Run._ACTION_TEXT_PARSER
            case Run.ACTION_CODE_PARSER_LINE:
                action_text = Run._ACTION_TEXT_PARSER_LINE
            case Run.ACTION_CODE_PARSER_PAGE:
                action_text = Run._ACTION_TEXT_PARSER_PAGE
            case Run.ACTION_CODE_PARSER_WORD:
                action_text = Run._ACTION_TEXT_PARSER_WORD
            case Run.ACTION_CODE_PDF2IMAGE:
                action_text = Run._ACTION_TEXT_PDF2IMAGE
            case Run.ACTION_CODE_PDFLIB:
                action_text = Run._ACTION_TEXT_PDFLIB
            case Run.ACTION_CODE_TESSERACT:
                action_text = Run._ACTION_TEXT_TESSERACT
            case Run.ACTION_CODE_TOKENIZE:
                action_text = Run._ACTION_TEXT_TOKENIZE
            case Run.ACTION_CODE_TOKENIZE_LINE:
                action_text = Run._ACTION_TEXT_TOKENIZE_LINE
            case _:
                dcr_core.core_utils.terminate_fatal(
                    f"Action code {action_code} is not supported in function get_action_text()",
                )

        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return action_text

    # -----------------------------------------------------------------------------
    # Get the database columns in a tuple.
    # -----------------------------------------------------------------------------
    def get_columns_in_tuple(
        self,
    ) -> tuple[int | Integer, str, str, int | Integer, str | String, int | Integer, int | Integer, int | Integer]:
        """Get the database columns in a tuple.

            Returns:
                tuple[
            int | Integer,
            str,
            str,
            int | Integer,
            str | String,
            int | Integer,
            int | Integer,
            int | Integer,
        ]:          Column values in a tuple.
        """
        return (
            self.run_id,
            self.run_action_code,
            self.run_action_text,
            self.run_id_run,
            self.run_status,
            self.run_total_erroneous,
            self.run_total_processed_ok,
            self.run_total_processed_to_be,
        )

    # -----------------------------------------------------------------------------
    # Get the latest id from database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def get_id_latest(cls) -> int:
        """Get the latest id from database table.

        Returns:
            int:    Latest id.
        """
        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_RUN,
            dcr.cfg.glob.db_core.db_orm_metadata,
            autoload_with=dcr.cfg.glob.db_core.db_orm_engine,
        )

        with dcr.cfg.glob.db_core.db_orm_engine.connect() as conn:
            row = conn.execute(sqlalchemy.select(sqlalchemy.func.max(dbt.c.id_run))).fetchone()
            conn.close()

        if row == (None,):
            # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
            return 0

        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return row[0]  # type: ignore

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        if self.run_id == 0:
            self.run_id = dcr.cfg.glob.db_core.insert_dbt_row(  # type: ignore
                dcr.db.cls_db_core.DBCore.DBT_RUN,  # type: ignore
                self._get_columns(),  # type: ignore
            )
            return

        if self.run_total_erroneous == 0 and self.run_total_processed_ok == 0 and self.run_total_processed_to_be == 0:
            dcr.cfg.glob.db_core.delete_dbt_id(  # type: ignore
                table_name=dcr.db.cls_db_core.DBCore.DBT_RUN,
                id_where=self.run_id,
            )
        else:
            dcr.cfg.glob.db_core.update_dbt_id(  # type: ignore
                table_name=dcr.db.cls_db_core.DBCore.DBT_RUN,
                id_where=self.run_id,
                columns=self._get_columns(),
            )

        # dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
