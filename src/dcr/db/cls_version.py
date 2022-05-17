"""Module db.cls_version: Managing the database table version."""
from __future__ import annotations

import cfg.glob
import db.dml
import db.driver
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
import utils
from sqlalchemy import Integer


class Version:
    """Managing the version data.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(  # pylint: disable=R0913
        self,
        _row_id: int | sqlalchemy.Integer = 0,
        version: str = "",
    ) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.version_id: int | sqlalchemy.Integer = _row_id
        self.version_version: str = version

        if self.version_id == 0:
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
            cfg.glob.DBC_VERSION: self.version_version,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        sqlalchemy.Table(
            cfg.glob.DBT_VERSION,
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
            sqlalchemy.Column(cfg.glob.DBC_VERSION, sqlalchemy.String, nullable=False, unique=True),
        )

        utils.progress_msg(f"The database table '{cfg.glob.DBT_VERSION}' has now been created")

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
    def from_id(cls, id_version: int | sqlalchemy.Integer) -> Version:
        """Initialise from id."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        db.driver.connect_db()

        dbt = sqlalchemy.Table(
            cfg.glob.DBT_VERSION,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )

        with cfg.glob.db_orm_engine.connect() as conn:  # type: ignore
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_version,
                )
            ).fetchone()
            conn.close()

        if row is None:
            utils.terminate_fatal(
                f"The version with id={id_version} does not exist in the database table 'version'",
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return Version.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Version:
        """Initialise from a database row."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return cls(
            _row_id=row[cfg.glob.DBC_ID],
            version=row[cfg.glob.DBC_VERSION],
        )

    # -----------------------------------------------------------------------------
    # Get the database columns in a tuple.
    # -----------------------------------------------------------------------------
    def get_columns_in_tuple(self) -> tuple[int | Integer, str]:
        """Get the database columns in a tuple.

        Returns:
            tuple[int | Integer, str]: Column values in a tuple.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)
        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return (
            self.version_id,
            self.version_version,
        )

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        if self.version_id == 0:
            self.version_id = db.dml.insert_dbt_row(
                cfg.glob.DBT_VERSION,
                self._get_columns(),
            )
        else:
            db.dml.update_dbt_id(
                table_name=cfg.glob.DBT_VERSION,
                id_where=self.version_id,
                columns=self._get_columns(),
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the version number from the database table version.
    # -----------------------------------------------------------------------------
    @classmethod
    def select_version_version_unique(cls) -> str:
        """Get the version number.

        Get the version number from the database table `version`.

        Returns:
            str: The version number found.
        """
        dbt = sqlalchemy.Table(
            cfg.glob.DBT_VERSION,
            cfg.glob.db_orm_metadata,
            autoload_with=cfg.glob.db_orm_engine,
        )

        current_version: str = ""

        with cfg.glob.db_orm_engine.connect() as conn:  # type: ignore
            for row in conn.execute(sqlalchemy.select(dbt.c.version)):
                if current_version == "":
                    current_version = row.version
                else:
                    utils.terminate_fatal(
                        "Column version in database table version not unique",
                    )
            conn.close()

        if current_version == "":
            utils.terminate_fatal("Column version in database table version not found")

        return current_version
