"""Module db.cls_token: Managing the database table token."""
from __future__ import annotations

import cfg.glob
import db.cls_db_core
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
import utils


class Token:
    """Managing the database table token.

    Returns:
        _type_: Token instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(  # pylint: disable=R0913
        self,
        id_document: int,
        page_data: str,
        page_no: int,
        _row_id: int = 0,
    ) -> None:
        """Initialise the instance.

        Args:
            id_document (int):
                    Row id of the document
            page_data (str):
                    Page data
            page_no (int):
                    Page number.
            _row_id (int, optional):
                    Row id. Defaults to 0.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        try:
            cfg.glob.db_core.exists()  # type: ignore
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'DBCore' does not yet exist.",
            )

        self.token_id: int = _row_id
        self.token_id_document: int = id_document
        self.token_page_data: str = page_data
        self.token_page_no: int = page_no

        if self.token_id == 0:
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
            db.cls_db_core.DBCore.DBC_ID_DOCUMENT: self.token_id_document,
            db.cls_db_core.DBCore.DBC_PAGE_DATA: self.token_page_data,
            db.cls_db_core.DBCore.DBC_PAGE_NO: self.token_page_no,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            db.cls_db_core.DBCore.DBT_TOKEN,
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
            sqlalchemy.Column(
                db.cls_db_core.DBCore.DBC_ID_DOCUMENT,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(
                    db.cls_db_core.DBCore.DBT_DOCUMENT + "." + db.cls_db_core.DBCore.DBC_ID, ondelete="CASCADE"
                ),
                nullable=False,
            ),
            sqlalchemy.Column(
                db.cls_db_core.DBCore.DBC_PAGE_DATA,
                sqlalchemy.JSON,
                nullable=False,
            ),
            sqlalchemy.Column(
                db.cls_db_core.DBCore.DBC_PAGE_NO,
                sqlalchemy.Integer,
                nullable=False,
            ),
        )

        utils.progress_msg(f"The database table '{db.cls_db_core.DBCore.DBT_TOKEN}' has now been created")

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
    # Finalise the current row.
    # -----------------------------------------------------------------------------
    def finalise(self) -> None:
        """Finalise the current row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.persist_2_db()

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

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
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            db.cls_db_core.DBCore.DBT_TOKEN,
            cfg.glob.db_core.db_orm_metadata,
            autoload_with=cfg.glob.db_core.db_orm_engine,
        )

        with cfg.glob.db_core.db_orm_engine.connect() as conn:
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_token,
                )
            ).fetchone()
            conn.close()

        if row is None:
            utils.terminate_fatal(
                f"The token with id={id_token} does not exist in the database table 'token'",
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

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
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[db.cls_db_core.DBCore.DBC_ID],
            id_document=row[db.cls_db_core.DBCore.DBC_ID_DOCUMENT],
            page_data=row[db.cls_db_core.DBCore.DBC_PAGE_DATA],
            page_no=row[db.cls_db_core.DBCore.DBC_PAGE_NO],
        )

    # -----------------------------------------------------------------------------
    # Get the database columns in a tuple.
    # -----------------------------------------------------------------------------
    def get_columns_in_tuple(
        self,
    ) -> tuple[int, int, str, int]:
        """Get the database columns in a tuple.

        Returns:
            tuple[int, int, str, int]:
                    Column values in a tuple.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return (
            self.token_id,
            self.token_id_document,
            self.token_page_data,
            self.token_page_no,
        )

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        if self.token_id == 0:
            self.token_id = cfg.glob.db_core.insert_dbt_row(  # type: ignore
                db.cls_db_core.DBCore.DBT_TOKEN,  # type: ignore
                self._get_columns(),  # type: ignore
            )
        else:
            cfg.glob.db_core.update_dbt_id(  # type: ignore
                table_name=db.cls_db_core.DBCore.DBT_TOKEN,
                id_where=self.token_id,
                columns=self._get_columns(),
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
