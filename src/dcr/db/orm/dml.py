"""Module db.orm.dml: Database Manipulation Management."""
import os
import time
import typing

import db.cfg
import db.orm.dml
import libs.cfg
import libs.utils
import PyPDF2
import PyPDF2.utils
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm

# -----------------------------------------------------------------------------
# Type declaration.
# -----------------------------------------------------------------------------
Columns: typing.TypeAlias = typing.Dict[str, typing.Union[os.PathLike[str], sqlalchemy.Integer, str]]


# -----------------------------------------------------------------------------
# Determine the number of pages in a pdf document.
# -----------------------------------------------------------------------------
def get_pdf_pages_no(
    file_name: str,
    file_type: str,
) -> int | None:
    """Determine the number of pages in a pdf document.

    Args:
        file_name (str): File name.
        file_type (str): File type.

    Returns:
        sqlalchemy.Integer|None: The number of pages found.
    """
    if file_type != db.cfg.DOCUMENT_FILE_TYPE_PDF:
        return None

    try:
        return PyPDF2.PdfFileReader(file_name).numPages
    except PyPDF2.utils.PdfReadError:
        return -1


# -----------------------------------------------------------------------------
# Insert a new row into a database table.
# -----------------------------------------------------------------------------
def insert_dbt_row(
    table_name: str,
    columns: Columns,
) -> sqlalchemy.Integer:
    """Insert a new row into a database table.

    Args:
        table_name (str): Table name.
        columns (libs.cfg.TYPE_COLUMNS_INSERT): Pairs of column name and value.

    Returns:
        sqlalchemy.Integer: The last id found.
    """
    dbt = sqlalchemy.Table(table_name, db.cfg.db_orm_metadata, autoload_with=db.cfg.db_orm_engine)

    with db.cfg.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        result = conn.execute(sqlalchemy.insert(dbt).values(columns).returning(dbt.columns.id))
        row = result.fetchone()
        conn.close()

    return row[0]


# -----------------------------------------------------------------------------
# Insert a new base document.
# -----------------------------------------------------------------------------
def insert_document_base() -> None:
    """Insert a new base document."""
    file_path = os.path.join(libs.cfg.document_directory_name, libs.cfg.document_file_name)

    libs.cfg.document_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_DOCUMENT,
        {
            db.cfg.DBC_CURRENT_STEP: libs.cfg.document_current_step,
            db.cfg.DBC_DIRECTORY_NAME: libs.cfg.document_directory_name,
            db.cfg.DBC_DIRECTORY_TYPE: libs.cfg.document_directory_type,
            db.cfg.DBC_DURATION_NS: 0,
            db.cfg.DBC_ERROR_NO: 0,
            db.cfg.DBC_FILE_NAME: libs.cfg.document_file_name,
            db.cfg.DBC_FILE_SIZE_BYTES: os.path.getsize(file_path),
            db.cfg.DBC_FILE_TYPE: libs.cfg.document_file_type,
            db.cfg.DBC_LANGUAGE_ID: libs.cfg.language_id,
            db.cfg.DBC_NEXT_STEP: db.cfg.DOCUMENT_STEP_INBOX,
            db.cfg.DBC_PDF_PAGES_NO: get_pdf_pages_no(file_path, libs.cfg.document_file_type),
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_SHA256: libs.cfg.document_sha256,
            db.cfg.DBC_STATUS: db.cfg.DOCUMENT_STATUS_START,
            db.cfg.DBC_STEM_NAME: libs.cfg.document_stem_name,
        },
    )

    libs.cfg.document_id_base = libs.cfg.document_id

    db.orm.dml.update_dbt_id(
        db.cfg.DBT_DOCUMENT,
        libs.cfg.document_id,
        {
            db.cfg.DBC_DOCUMENT_ID_BASE: libs.cfg.document_id_base,
        },
    )


# -----------------------------------------------------------------------------
# Insert a new child document of the base document.
# -----------------------------------------------------------------------------
def insert_document_child() -> None:
    """Insert a new child document of the base document."""
    file_path = os.path.join(libs.cfg.document_child_directory_name, libs.cfg.document_child_file_name)

    libs.cfg.document_child_id = db.orm.dml.insert_dbt_row(
        db.cfg.DBT_DOCUMENT,
        {
            db.cfg.DBC_CHILD_NO: libs.cfg.document_child_child_no,
            db.cfg.DBC_CURRENT_STEP: libs.cfg.document_current_step,
            db.cfg.DBC_DIRECTORY_NAME: str(libs.cfg.document_child_directory_name),
            db.cfg.DBC_DIRECTORY_TYPE: libs.cfg.document_child_directory_type,
            db.cfg.DBC_DOCUMENT_ID_BASE: libs.cfg.document_child_id_base,
            db.cfg.DBC_DOCUMENT_ID_PARENT: libs.cfg.document_child_id_parent,
            db.cfg.DBC_DURATION_NS: 0,
            db.cfg.DBC_ERROR_CODE: libs.cfg.document_child_error_code,
            db.cfg.DBC_ERROR_NO: 0,
            db.cfg.DBC_FILE_NAME: libs.cfg.document_child_file_name,
            db.cfg.DBC_FILE_SIZE_BYTES: os.path.getsize(file_path),
            db.cfg.DBC_FILE_TYPE: libs.cfg.document_child_file_type,
            db.cfg.DBC_NEXT_STEP: libs.cfg.document_child_next_step,
            db.cfg.DBC_LANGUAGE_ID: libs.cfg.language_id
            if libs.cfg.run_action == libs.cfg.RUN_ACTION_PROCESS_INBOX
            else libs.cfg.document_child_language_id,
            db.cfg.DBC_PDF_PAGES_NO: get_pdf_pages_no(file_path, libs.cfg.document_child_file_type),
            db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            db.cfg.DBC_STATUS: libs.cfg.document_child_status,
            db.cfg.DBC_STEM_NAME: libs.cfg.document_child_stem_name,
        },
    )


# -----------------------------------------------------------------------------
# Preparation of a database table for DML operations.
# -----------------------------------------------------------------------------
def dml_prepare(dbt_name: str) -> sqlalchemy.Table:
    """Preparation of a database table for DML operations.

    Returns:
        sqlalchemy.Table: Database table document,
    """
    # Check the inbox file directories.
    libs.utils.check_directories()

    return sqlalchemy.Table(
        dbt_name,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )


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
            dbt.c.page_no,
            dbt.c.page_data,
        )
        .where(
            dbt.c.document_id == document_id,
        )
        .order_by(dbt.c.page_no.asc())
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
            dbt.c.child_no,
            dbt.c.directory_name,
            dbt.c.directory_type,
            dbt.c.document_id_base,
            dbt.c.document_id_parent,
            dbt.c.file_name,
            dbt.c.file_type,
            dbt.c.language_id,
            dbt.c.status,
            dbt.c.stem_name,
        )
        .where(
            sqlalchemy.and_(
                dbt.c.next_step == next_step,
                dbt.c.status.in_(
                    [
                        db.cfg.DOCUMENT_STATUS_ERROR,
                        db.cfg.DOCUMENT_STATUS_START,
                    ]
                ),
            )
        )
        .order_by(dbt.c.id.asc())
    )


# -----------------------------------------------------------------------------
# Get the file name of the base document.
# -----------------------------------------------------------------------------
def select_document_base_file_name() -> str | None:
    """Get the file name of the base document.

    Returns:
        str: The file name of the base document found.
    """
    dbt = sqlalchemy.Table(
        db.cfg.DBT_DOCUMENT,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    with db.cfg.db_orm_engine.connect() as conn:
        row = conn.execute(
            sqlalchemy.select(dbt.c.directory_name, dbt.c.file_name).where(
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
    dbt = sqlalchemy.Table(
        db.cfg.DBT_DOCUMENT,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    with db.cfg.db_orm_engine.connect() as conn:
        row = conn.execute(
            sqlalchemy.select(dbt.c.file_name).where(
                sqlalchemy.and_(
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
    dbt = sqlalchemy.Table(
        db.cfg.DBT_DOCUMENT,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    with db.cfg.db_orm_engine.connect() as conn:
        row = conn.execute(
            sqlalchemy.select(dbt.c.file_name).where(
                sqlalchemy.and_(
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
        sqlalchemy.select(
            dbt.c.id,
            dbt.c.directory_name_inbox,
            dbt.c.iso_language_name,
        )
        .where(
            dbt.c.active,
        )
        .order_by(dbt.c.id.asc())
    )


# -----------------------------------------------------------------------------
# Get the last run_id from database table run.
# -----------------------------------------------------------------------------
def select_run_run_id_last() -> int | sqlalchemy.Integer:
    """Get the last run_id from database table run.

    Returns:
        sqlalchemy.Integer: The last run id found.
    """
    dbt = sqlalchemy.Table(db.cfg.DBT_RUN, db.cfg.db_orm_metadata, autoload_with=db.cfg.db_orm_engine)

    with db.cfg.db_orm_engine.connect() as conn:
        row = conn.execute(sqlalchemy.select(sqlalchemy.func.max(dbt.c.run_id))).fetchone()
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
    dbt = sqlalchemy.Table(
        db.cfg.DBT_VERSION,
        db.cfg.db_orm_metadata,
        autoload_with=db.cfg.db_orm_engine,
    )

    current_version: str = ""

    with db.cfg.db_orm_engine.connect() as conn:
        for row in conn.execute(sqlalchemy.select(dbt.c.version)):
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
    columns: typing.Dict[str, str],
) -> None:
    """Update a database row based on its id column.

    Args:
        table_name (str): sqlalchemy.Table name.
        id_where (sqlalchemy.Integer): Content of column id.
        columns (Columns): Pairs of column name and value.
    """
    dbt = sqlalchemy.Table(table_name, db.cfg.db_orm_metadata, autoload_with=db.cfg.db_orm_engine)

    with db.cfg.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(sqlalchemy.update(dbt).where(dbt.c.id == id_where).values(columns))
        conn.close()


# -----------------------------------------------------------------------------
# Update the table 'document' with error information..
# -----------------------------------------------------------------------------
def update_document_error(document_id: sqlalchemy.Integer, error_code: str, error_msg: str) -> None:
    """Update the table 'document' with error information..

    Args:
        document_id (sqlalchemy.Integer): Document id.
        error_code (str)                : Error code.
        error_msg (str)                 : Error message.
    """
    dbt = sqlalchemy.Table(db.cfg.DBT_DOCUMENT, db.cfg.db_orm_metadata, autoload_with=db.cfg.db_orm_engine)

    libs.cfg.total_erroneous += 1

    duration_ns = time.perf_counter_ns() - libs.cfg.start_time_document

    update_dbt_id(
        table_name=db.cfg.DBT_DOCUMENT,
        id_where=document_id,
        columns={
            db.cfg.DBC_DURATION_NS: duration_ns,
            db.cfg.DBC_ERROR_CODE: error_code,
            db.cfg.DBC_ERROR_MSG: error_msg,
            db.cfg.DBC_ERROR_NO: dbt.c.error_no + 1,
            db.cfg.DBC_STATUS: db.cfg.DOCUMENT_STATUS_ERROR,
        },
    )

    if libs.cfg.config.is_verbose:
        libs.utils.progress_msg(
            f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
            f"Document: {libs.cfg.document_id:6d} "
            f"[{db.orm.dml.select_document_file_name_id(libs.cfg.document_id)}] - "
            f"Error: {error_msg} "
        )


# -----------------------------------------------------------------------------
# Update the table 'document' with statistics data.
# -----------------------------------------------------------------------------
def update_document_statistics(
    document_id: sqlalchemy.Integer,
    status: str,
) -> int:
    """Update the table 'document' with statistics data.

    Args:
        document_id (sqlalchemy.Integer): Document id.
        status (str):                     Status.
    """
    duration_ns = time.perf_counter_ns() - libs.cfg.start_time_document

    update_dbt_id(
        table_name=db.cfg.DBT_DOCUMENT,
        id_where=document_id,
        columns={
            db.cfg.DBC_DURATION_NS: duration_ns,
            db.cfg.DBC_STATUS: status,
        },
    )

    return duration_ns
