# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module dcr.db.cls_version: Managing the database table version."""
from __future__ import annotations

import dcr_core.core_glob
import dcr_core.core_utils
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
from sqlalchemy import Integer

import dcr.cfg.glob
import dcr.db.cls_db_core
import dcr.utils


class Version:
    """Managing the database table version.

    Returns:
        _type_: Version instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(
        self,
        _row_id: int = 0,
        version: str = "",
    ) -> None:
        """Initialise the instance.

        Args:
            _row_id (int, optional):
                    Row id. Defaults to 0.
            version (str, optional):
                    Version number. Defaults to "".
        """
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dcr.utils.check_exists_object(
            is_db_core=True,
        )

        self.version_id = _row_id
        self.version_version = version

        if self.version_id == 0:
            self.persist_2_db()

        self._exist = True

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Get the database columns.
    # -----------------------------------------------------------------------------
    def _get_columns(self) -> dcr.db.cls_db_core.Columns:
        """Get the database columns.

        Returns:
            dcr.db.cls_db_core.Columns:
                    Database columns.
        """
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return {
            dcr.db.cls_db_core.DBCore.DBC_VERSION: self.version_version,
        }

    # -----------------------------------------------------------------------------
    # Create the database table.
    # -----------------------------------------------------------------------------
    @classmethod
    def create_dbt(cls) -> None:
        """Create the database table."""
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_VERSION,
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
            sqlalchemy.Column(dcr.db.cls_db_core.DBCore.DBC_VERSION, sqlalchemy.String, nullable=False, unique=True),
        )

        dcr.utils.progress_msg(f"The database table '{dcr.db.cls_db_core.DBCore.DBT_VERSION}' has now been created")

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

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
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        self.persist_2_db()

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise from id.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_id(cls, id_version: int) -> Version:
        """Initialise from row id.

        Args:
            id_version (int):
                    The required row id.

        Returns:
            Version:
                    The object instance found.
        """
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        dbt = sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_VERSION,
            dcr.cfg.glob.db_core.db_orm_metadata,
            autoload_with=dcr.cfg.glob.db_core.db_orm_engine,
        )

        with dcr.cfg.glob.db_core.db_orm_engine.connect() as conn:
            row = conn.execute(
                sqlalchemy.select(dbt).where(
                    dbt.c.id == id_version,
                )
            ).fetchone()
            conn.close()

        if row is None:
            dcr_core.core_utils.terminate_fatal(
                f"The version with id={id_version} does not exist in the database table 'version'",
            )

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return Version.from_row(row)  # type: ignore

    # -----------------------------------------------------------------------------
    # Initialise from a database row.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Version:
        """Initialise from a database row.

        Args:
            row (sqlalchemy.engine.Row):
                    A appropriate database row.

        Returns:
            Version:
                    The object instance matching the specified database row.
        """
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return cls(
            _row_id=row[dcr.db.cls_db_core.DBCore.DBC_ID],
            version=row[dcr.db.cls_db_core.DBCore.DBC_VERSION],
        )

    # -----------------------------------------------------------------------------
    # Get the database columns in a tuple.
    # -----------------------------------------------------------------------------
    def get_columns_in_tuple(self) -> tuple[int | Integer, str]:
        """Get the database columns in a tuple.

        Returns:
            tuple[int | Integer, str]:
                    Column values in a tuple.
        """
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

        return (
            self.version_id,
            self.version_version,
        )

    # -----------------------------------------------------------------------------
    # Persist the object in the database.
    # -----------------------------------------------------------------------------
    def persist_2_db(self) -> None:
        """Persist the object in the database."""
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        if self.version_id == 0:
            self.version_id = dcr.cfg.glob.db_core.insert_dbt_row(  # type: ignore
                dcr.db.cls_db_core.DBCore.DBT_VERSION,  # type: ignore
                self._get_columns(),  # type: ignore
            )
        else:
            dcr.cfg.glob.db_core.update_dbt_id(  # type: ignore
                table_name=dcr.db.cls_db_core.DBCore.DBT_VERSION,
                id_where=self.version_id,
                columns=self._get_columns(),
            )

        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)

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
            dcr.db.cls_db_core.DBCore.DBT_VERSION,
            dcr.cfg.glob.db_core.db_orm_metadata,
            autoload_with=dcr.cfg.glob.db_core.db_orm_engine,
        )

        current_version = ""

        with dcr.cfg.glob.db_core.db_orm_engine.connect() as conn:
            for row in conn.execute(sqlalchemy.select(dbt.c.version)):
                if current_version == "":
                    current_version = row.version
                else:
                    dcr_core.core_utils.terminate_fatal(
                        "Column version in database table version not unique",
                    )
            conn.close()

        if current_version == "":
            dcr_core.core_utils.terminate_fatal("Column version in database table version not found")

        return current_version
