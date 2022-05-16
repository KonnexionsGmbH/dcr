"""Module db.cls_token: Managing the database table token."""
from __future__ import annotations

import cfg.glob
import db.dml
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
import utils


class Token:
    """Managing the token data.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(  # pylint: disable=R0913
        self,
        _row_id: int | sqlalchemy.Integer = 0,
        id_base: int | sqlalchemy.Integer = 0,
        page_data: str | sqlalchemy.String = "",
    ) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.token_id: int | sqlalchemy.Integer = _row_id
        self.token_id_base: int | sqlalchemy.Integer = id_base
        self.token_page_data: str | sqlalchemy.String = page_data

        if self.token_id == 0:
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
            cfg.glob.DBC_ID_BASE: self.token_id_base,
            cfg.glob.DBC_PAGE_DATA: self.token_page_data,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            cfg.glob.DBT_TOKEN,
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
            sqlalchemy.Column(
                cfg.glob.DBC_ID_BASE,
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(cfg.glob.DBT_BASE + "." + cfg.glob.DBC_ID, ondelete="CASCADE"),
                nullable=False,
            ),
            sqlalchemy.Column(
                cfg.glob.DBC_PAGE_NO,
                sqlalchemy.Integer,
                nullable=False,
            ),
            sqlalchemy.Column(
                cfg.glob.DBC_PAGE_DATA,
                sqlalchemy.JSON,
                nullable=False,
            ),
        )

        utils.progress_msg(f"The database table '{cfg.glob.DBT_TOKEN}' has now been created")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

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
    def from_id(cls, id_token: int | sqlalchemy.Integer) -> Token:
        """Initialise from id."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            cfg.glob.DBT_TOKEN,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )

        with cfg.glob.db_orm_engine.connect() as conn:  # type: ignore
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_token,
                )
            ).fetchone()
            conn.close()

        if row == ():
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
        """Initialise from a database row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[cfg.glob.DBC_ID],
            id_base=row[cfg.glob.DBC_ID_BASE],
            page_data=row[cfg.glob.DBC_PAGE_DATA],
        )

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        if self.token_id == 0:
            self.token_id = db.dml.insert_dbt_row(
                cfg.glob.DBT_TOKEN,
                self._get_columns(),
            )
        else:
            db.dml.update_dbt_id(
                table_name=cfg.glob.DBT_TOKEN,
                id_where=self.token_id,
                columns=self._get_columns(),
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)