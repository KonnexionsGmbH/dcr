"""Module dcr.db.cls_token: Managing the database table token."""
from __future__ import annotations

import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm

import dcr.cfg.glob
import dcr.db.cls_db_core
import dcr.utils
import dcr_core.core_utils


class Token:
    """Managing the database table token.

    Returns:
        _type_: Token instance.
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-instance-attributes
    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(
        self,
        id_document: int,
        column_no: int,
        column_span: int,
        coord_llx: float,
        coord_urx: float,
        line_type: str,
        no_tokens_in_sent: int,
        page_no: int,
        para_no: int,
        row_no: int,
        sent_no: int,
        text: str,
        tokens: str,
        _row_id: int = 0,
    ) -> None:
        """Initialise the instance.

        Args:
            id_document (int):
                    Row id of the document
            column_no (int):
                    Column number.
            column_span (int):
                    Column span.
            coord_llx (float):
                    Lower left x coordinate.
            coord_urx (float):
                    upper right x coordinate.
            line_type (str):
                    Line type.
            no_tokens_in_sent (int):
                    Number tokens in sentence.
            page_no (int):
                    Page number.
            para_no (int):
                    Paragraph number.
            row_no (int):
                    Row number.
            sent_no (int):
                    Sentence number.
            text (str):
                    Text.
            tokens (str):
                    Tokens.
            _row_id (int, optional):
                    Row id. Defaults to 0.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        dcr.utils.check_exists_object(
            is_db_core=True,
        )

        self.token_id = _row_id
        self.token_column_no = column_no
        self.token_column_span = column_span
        self.token_coord_llx = coord_llx
        self.token_coord_urx = coord_urx
        self.token_id_document = id_document
        self.token_line_type = line_type
        self.token_no_tokens_in_sent = no_tokens_in_sent
        self.token_page_no = page_no
        self.token_para_no = para_no
        self.token_row_no = row_no
        self.token_sent_no = sent_no
        self.token_text = text
        self.token_tokens = tokens

        if self.token_id == 0:
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

        return {
            dcr.db.cls_db_core.DBCore.DBC_ID_DOCUMENT: self.token_id_document,
            dcr.db.cls_db_core.DBCore.DBC_COLUMN_NO: self.token_column_no,
            dcr.db.cls_db_core.DBCore.DBC_COLUMN_SPAN: self.token_column_span,
            dcr.db.cls_db_core.DBCore.DBC_COORD_LLX: self.token_coord_llx,
            dcr.db.cls_db_core.DBCore.DBC_COORD_URX: self.token_coord_urx,
            dcr.db.cls_db_core.DBCore.DBC_LINE_TYPE: self.token_line_type,
            dcr.db.cls_db_core.DBCore.DBC_NO_TOKENS_IN_SENT: self.token_no_tokens_in_sent,
            dcr.db.cls_db_core.DBCore.DBC_PAGE_NO: self.token_page_no,
            dcr.db.cls_db_core.DBCore.DBC_PARA_NO: self.token_para_no,
            dcr.db.cls_db_core.DBCore.DBC_ROW_NO: self.token_row_no,
            dcr.db.cls_db_core.DBCore.DBC_SENT_NO: self.token_sent_no,
            dcr.db.cls_db_core.DBCore.DBC_TEXT: self.token_text,
            dcr.db.cls_db_core.DBCore.DBC_TOKENS: self.token_tokens,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_TOKEN,
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
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_COLUMN_NO,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_COLUMN_SPAN,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_COORD_LLX,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_COORD_URX,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_ID_DOCUMENT,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(dcr.db.cls_db_core.DBCore.DBT_DOCUMENT + "." + dcr.db.cls_db_core.DBCore.DBC_ID, ondelete="CASCADE"),
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_LINE_TYPE,
                sqlalchemy.String,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_NO_TOKENS_IN_SENT,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_PAGE_NO,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_PARA_NO,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_ROW_NO,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_SENT_NO,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_TEXT,
                sqlalchemy.String,
                nullable=False,
            ),
            sqlalchemy.Column(
                dcr.db.cls_db_core.DBCore.DBC_TOKENS,
                sqlalchemy.JSON,
                nullable=False,
            ),
        )

        dcr.utils.progress_msg(f"The database table '{dcr.db.cls_db_core.DBCore.DBT_TOKEN}' has now been created")

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

        self.persist_2_db()

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise from id.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_id(cls, id_token: int) -> Token:
        """Initialise from row id.

        Args:
            id_token (int):
                    The required row id.

        Returns:
            Token:  The object instance found.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_TOKEN,
            dcr.cfg.glob.db_core.db_orm_metadata,
            autoload_with=dcr.cfg.glob.db_core.db_orm_engine,
        )

        with dcr.cfg.glob.db_core.db_orm_engine.connect() as conn:
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_token,
                )
            ).fetchone()
            conn.close()

        if row is None:
            dcr_core.core_utils.terminate_fatal(
                f"The token with id={id_token} does not exist in the database table 'token'",
            )

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

        return Token.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Token:
        """Initialise from a database row.

        Args:
            row (sqlalchemy.engine.Row):
                    A appropriate database row.

        Returns:
            Token:  The object instance matching the specified database row.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[dcr.db.cls_db_core.DBCore.DBC_ID],
            id_document=row[dcr.db.cls_db_core.DBCore.DBC_ID_DOCUMENT],
            column_no=row[dcr.db.cls_db_core.DBCore.DBC_COLUMN_NO],
            column_span=row[dcr.db.cls_db_core.DBCore.DBC_COLUMN_SPAN],
            coord_llx=row[dcr.db.cls_db_core.DBCore.DBC_COORD_LLX],
            coord_urx=row[dcr.db.cls_db_core.DBCore.DBC_COORD_URX],
            line_type=row[dcr.db.cls_db_core.DBCore.DBC_LINE_TYPE],
            no_tokens_in_sent=row[dcr.db.cls_db_core.DBCore.DBC_NO_TOKENS_IN_SENT],
            page_no=row[dcr.db.cls_db_core.DBCore.DBC_PAGE_NO],
            para_no=row[dcr.db.cls_db_core.DBCore.DBC_PARA_NO],
            row_no=row[dcr.db.cls_db_core.DBCore.DBC_ROW_NO],
            sent_no=row[dcr.db.cls_db_core.DBCore.DBC_SENT_NO],
            text=row[dcr.db.cls_db_core.DBCore.DBC_TEXT],
            tokens=row[dcr.db.cls_db_core.DBCore.DBC_TOKENS],
        )

    # -----------------------------------------------------------------------------
    # Get the database columns in a tuple.
    # -----------------------------------------------------------------------------
    def get_columns_in_tuple(
        self,
    ) -> tuple[int, int, int, int, float, float, str, int, int, int, int, int, str, str]:
        """Get the database columns in a tuple.

        Returns:
            tuple[int, int, str, int]:
                    Column values in a tuple.
        """
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)

        return (
            self.token_id,
            self.token_id_document,
            self.token_column_no,
            self.token_column_span,
            self.token_coord_llx,
            self.token_coord_urx,
            self.token_line_type,
            self.token_no_tokens_in_sent,
            self.token_page_no,
            self.token_para_no,
            self.token_row_no,
            self.token_sent_no,
            self.token_text,
            self.token_tokens,
        )

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_START)

        if self.token_id == 0:
            self.token_id = dcr.cfg.glob.db_core.insert_dbt_row(  # type: ignore
                dcr.db.cls_db_core.DBCore.DBT_TOKEN,  # type: ignore
                self._get_columns(),  # type: ignore
            )
        else:
            dcr.cfg.glob.db_core.update_dbt_id(  # type: ignore
                table_name=dcr.db.cls_db_core.DBCore.DBT_TOKEN,
                id_where=self.token_id,
                columns=self._get_columns(),
            )

        dcr.cfg.glob.logger.debug(dcr.cfg.glob.LOGGER_END)
