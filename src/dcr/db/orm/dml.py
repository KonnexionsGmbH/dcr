"""Module db.orm.dml: Database Manipulation Management."""
import os
import time
from typing import Dict

import db.cfg
import db.orm.dml
import libs.cfg
import libs.utils
import sqlalchemy.orm
from sqlalchemy import Table
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_dbt_row(
    table_name: str,
    columns: libs.cfg.Columns,
) -> sqlalchemy.Integer:
    """Insert a new row into a database table.

    Args:
        table_name (str): Table name.
        columns (libs.cfg.TYPE_COLUMNS_INSERT): Pairs of column name and value.

    Returns:
        sqlalchemy.Integer: The last id found.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = Table(table_name, db.cfg.db_orm_metadata, autoload_with=db.cfg.db_orm_engine)

    with db.cfg.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        result = conn.execute(insert(dbt).values(columns).returning(dbt.columns.id))
        row = result.fetchone()
        conn.close()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    return row[0]


# -----------------------------------------------------------------------------
# Insert a new error message into the database 'journal'.
# -----------------------------------------------------------------------------
def insert_journal_error(
    document_id: sqlalchemy.Integer,
    error: str,
) -> None:
    """Insert a new error message into the database 'journal'.

    Args:
        document_id (sqlalchemy.Integer): Document id.
        error (str): Error message.
    """
    duration_ns = time.perf_counter_ns() - libs.cfg.start_time_document

    insert_dbt_row(
        db.cfg.DBT_JOURNAL,
        {
            db.cfg.DBC_CURRENT_STEP: libs.cfg.document_current_step,
            db.cfg.DBC_DOCUMENT_ID: document_id,
            db.cfg.DBC_DURATION_NS: duration_ns,
            db.cfg.DBC_ERROR_CODE: error[0:6],
            db.cfg.DBC_ERROR_TEXT: error[7:],
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
        },
    )

    if libs.cfg.is_verbose:
        libs.utils.progress_msg(
            f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {libs.cfg.document_id:6d} "
            f"[{db.orm.dml.select_document_file_name_id(libs.cfg.document_id)}] - "
            f"Error: {error} "
        )


# -----------------------------------------------------------------------------
# Insert a new statistics message into the database 'journal'.
# -----------------------------------------------------------------------------
def insert_journal_statistics(
    document_id: sqlalchemy.Integer,
) -> None:
    """Insert a new statistics message into the database 'journal'.

    Args:
        document_id (sqlalchemy.Integer): Document id.
    """
    duration_ns = time.perf_counter_ns() - libs.cfg.start_time_document

    insert_dbt_row(
        db.cfg.DBT_JOURNAL,
        {
            db.cfg.DBC_CURRENT_STEP: libs.cfg.document_current_step,
            db.cfg.DBC_DOCUMENT_ID: document_id,
            db.cfg.DBC_DURATION_NS: duration_ns,
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
        },
    )

    if libs.cfg.is_verbose:
        libs.utils.progress_msg(
            f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {libs.cfg.document_id:6d} "
            f"[{db.orm.dml.select_document_file_name_id(libs.cfg.document_id)}]"
        )


# -----------------------------------------------------------------------------
# Get the file name of the base document.
# -----------------------------------------------------------------------------
def select_document_base_file_name() -> str | None:
    """Get the file name of the base document.

    Returns:
        str: The file name of the base document found.
    """
    dbt = Table(
        db.cfg.DBT_DOCUMENT,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    with db.cfg.db_orm_engine.connect() as conn:
        row = conn.execute(
            select(dbt.c.directory_name, dbt.c.file_name).where(
                dbt.c.document_id_parent == libs.cfg.document_id_base,
            )
        ).fetchone()
        conn.close()

    return str(os.path.join(row[0], row[1]))


# -----------------------------------------------------------------------------
# Get the file name of a document based on the document_id.
# -----------------------------------------------------------------------------
def select_document_file_name_id(document_id: sqlalchemy.Integer) -> str | None:
    """Get the file name of a document based on the document_id.

    Args:
        document_id (sqlalchemy.Integer): Document id.

    Returns:
        str: The file name found.
    """
    dbt = Table(
        db.cfg.DBT_DOCUMENT,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    with db.cfg.db_orm_engine.connect() as conn:
        row = conn.execute(
            select(dbt.c.file_name).where(
                and_(
                    dbt.c.id == document_id,
                )
            )
        ).fetchone()
        conn.close()

    return row[0]


# -----------------------------------------------------------------------------
# Get the file name of an accepted document based on the hash key.
# -----------------------------------------------------------------------------
def select_document_file_name_sha256(document_id: sqlalchemy.Integer, sha256: str) -> str | None:
    """Get the file name of an accepted document based on the hash key.

    Args:
        document_id (sqlalchemy.Integer): Document id.
        sha256 (str): Hash key.

    Returns:
        str: The file name found.
    """
    dbt = Table(
        db.cfg.DBT_DOCUMENT,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    with db.cfg.db_orm_engine.connect() as conn:
        row = conn.execute(
            select(dbt.c.file_name).where(
                and_(
                    dbt.c.id != document_id,
                    dbt.c.directory_type == db.cfg.DOCUMENT_DIRECTORY_TYPE_INBOX,
                    dbt.c.sha256 == sha256,
                    dbt.c.status == db.cfg.DOCUMENT_STATUS_END,
                )
            )
        ).fetchone()
        conn.close()

    if row is None:
        return row

    return row[0]


# -----------------------------------------------------------------------------
# Get the last run_id from database table run.
# -----------------------------------------------------------------------------
def select_run_run_id_last() -> int | sqlalchemy.Integer:
    """Get the last run_id from database table run.

    Returns:
        sqlalchemy.Integer: The last run id found.
    """
    dbt = Table(db.cfg.DBT_RUN, db.cfg.db_orm_metadata, autoload_with=db.cfg.db_orm_engine)

    with db.cfg.db_orm_engine.connect() as conn:
        row = conn.execute(select(func.max(dbt.c.run_id))).fetchone()
        conn.close()

    if row[0] is None:
        return 0

    return row[0]


# -----------------------------------------------------------------------------
# Get the version number from the database table version.
# -----------------------------------------------------------------------------
def select_version_version_unique() -> str:
    """Get the version number.

    Get the version number from the database table `version`.

    Returns:
        str: The version number found.
    """
    dbt = Table(
        db.cfg.DBT_VERSION,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    current_version: str = ""

    with db.cfg.db_orm_engine.connect() as conn:
        for row in conn.execute(select(dbt.c.version)):
            if current_version == "":
                current_version = row.version
            else:
                libs.utils.terminate_fatal(
                    "Column version in database table version not unique",
                )
        conn.close()

    if current_version == "":
        libs.utils.terminate_fatal("Column version in database table version not found")

    return current_version


# -----------------------------------------------------------------------------
# Update a database row based on its id column.
# -----------------------------------------------------------------------------
def update_dbt_id(
    table_name: str,
    id_where: sqlalchemy.Integer,
    columns: Dict[str, str],
) -> None:
    """Update a database row based on its id column.

    Args:
        table_name (str): Table name.
        id_where (sqlalchemy.Integer): Content of column id.
        columns (Columns): Pairs of column name and value.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = Table(table_name, db.cfg.db_orm_metadata, autoload_with=db.cfg.db_orm_engine)

    with db.cfg.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(update(dbt).where(dbt.c.id == id_where).values(columns))
        conn.close()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
