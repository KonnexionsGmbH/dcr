"""Module db.dml: Database Manipulation Management."""

import cfg.glob
import db.utils
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
import utils


# -----------------------------------------------------------------------------
# Delete a database row based on its id column.
# -----------------------------------------------------------------------------
def delete_dbt_id(
    table_name: str,
    id_where: int | sqlalchemy.Integer,
) -> None:
    """Delete a database row based on its id column.

    Args:
        table_name (str): sqlalchemy.Table name.
        id_where (int | sqlalchemy.Integer): Content of column id.
    """
    dbt = sqlalchemy.Table(table_name, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

    with cfg.glob.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(sqlalchemy.delete(dbt).where(dbt.c.id == id_where))
        conn.close()


# -----------------------------------------------------------------------------
# Preparation of a database table for DML operations.
# -----------------------------------------------------------------------------
def dml_prepare(dbt_name: str) -> sqlalchemy.Table:
    """Preparation of a database table for DML operations.

    Returns:
        sqlalchemy.Table: Database table document,
    """
    # Check the inbox file directories.
    utils.check_directories()

    return sqlalchemy.Table(
        dbt_name,
        cfg.glob.db_orm_metadata,
        autoload_with=cfg.glob.db_orm_engine,
    )


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_dbt_row(
    table_name: str,
    columns: db.utils.Columns,
) -> sqlalchemy.Integer:
    """Insert a new row into a database table.

    Args:
        table_name (str): Table name.
        columns (cfg.glob.TYPE_COLUMNS_INSERT): Pairs of column name and value.

    Returns:
        sqlalchemy.Integer: The last id found.
    """
    dbt = sqlalchemy.Table(table_name, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

    with cfg.glob.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        result = conn.execute(sqlalchemy.insert(dbt).values(columns).returning(dbt.columns.id))
        row = result.fetchone()
        conn.close()

    return row[0]


# -----------------------------------------------------------------------------
# Select the content pages to be processed.
# -----------------------------------------------------------------------------
def select_content_tetml(
    conn: sqlalchemy.engine.Connection, dbt: sqlalchemy.Table, document_id: sqlalchemy.Integer
) -> sqlalchemy.engine.CursorResult:
    """Select the content pages to be processed.

    Args:
        conn (Connection): Database connection.
        dbt (sqlalchemy.Table): database table document.
        document_id (sqlalchemy.Integer): Document id.

    Returns:
        engine.CursorResult: The content pages found.
    """
    return conn.execute(
        sqlalchemy.select(
            dbt.c.id,
            dbt.c.page_no,
            dbt.c.page_data,
        )
        .where(
            dbt.c.document_id == document_id,
        )
        .order_by(dbt.c.id.asc())
    )


# -----------------------------------------------------------------------------
# Select the documents to be processed.
# -----------------------------------------------------------------------------
def select_document(
    conn: sqlalchemy.engine.Connection, dbt: sqlalchemy.Table, next_step: str
) -> sqlalchemy.engine.CursorResult:
    """Select the documents to be processed.

    Args:
        conn (Connection): Database connection.
        dbt (sqlalchemy.Table): database table document.
        next_step (str): Next processing step.

    Returns:
        engine.CursorResult: The documents found.
    """
    return conn.execute(
        sqlalchemy.select(
            dbt.c.id,
            dbt.c.no_children,
            dbt.c.directory_name,
            dbt.c.directory_type,
            dbt.c.document_id_base,
            dbt.c.document_id_parent,
            dbt.c.file_name,
            dbt.c.file_type,
            dbt.c.id_language,
            dbt.c.status,
            dbt.c.stem_name,
        )
        .where(
            sqlalchemy.and_(
                dbt.c.next_step == next_step,
                dbt.c.status.in_(
                    [
                        cfg.glob.DOCUMENT_STATUS_ERROR,
                        cfg.glob.DOCUMENT_STATUS_START,
                    ]
                ),
            )
        )
        .order_by(dbt.c.id.asc())
    )


# -----------------------------------------------------------------------------
# Get the languages to be processed.
# -----------------------------------------------------------------------------
def select_language(conn: sqlalchemy.engine.Connection, dbt: sqlalchemy.Table) -> sqlalchemy.engine.CursorResult:
    """Get the languages to be processed.

    Args:
        conn (Connection): Database connection.
        dbt (sqlalchemy.Table): database table language.

    Returns:
        engine.CursorResult: The languages found.
    """
    return conn.execute(
        sqlalchemy.select(dbt)
        .where(
            dbt.c.active,
        )
        .order_by(dbt.c.id.asc())
    )


# -----------------------------------------------------------------------------
# Get the version number from the database table version.
# -----------------------------------------------------------------------------
def select_version_version_unique() -> str:
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

    with cfg.glob.db_orm_engine.connect() as conn:
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


# -----------------------------------------------------------------------------
# Update a database row based on its id column.
# -----------------------------------------------------------------------------
def update_dbt_id(
    table_name: str,
    id_where: int | sqlalchemy.Integer,
    columns: db.utils.Columns,
) -> None:
    """Update a database row based on its id column.

    Args:
        table_name (str): sqlalchemy.Table name.
        id_where (int | sqlalchemy.Integer): Content of column id.
        columns (Columns): Pairs of column name and value.
    """
    dbt = sqlalchemy.Table(table_name, cfg.glob.db_orm_metadata, autoload_with=cfg.glob.db_orm_engine)

    with cfg.glob.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(sqlalchemy.update(dbt).where(dbt.c.id == id_where).values(columns))
        conn.close()
