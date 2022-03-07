"""Module libs.utils: Helper functions."""
import datetime
import hashlib
import inspect
import os
import pathlib
import sys
import traceback

import libs.cfg
import libs.db.cfg
import libs.db.driver
import libs.db.orm
import libs.utils
from sqlalchemy import Table
from sqlalchemy import and_
from sqlalchemy import engine
from sqlalchemy import select
from sqlalchemy.engine import Connection
from sqlalchemy.engine import Row


# -----------------------------------------------------------------------------
# Check the inbox file directories.
# -----------------------------------------------------------------------------
def check_directories() -> None:
    """Check the inbox file directories.

    The file directory inbox_accepted must exist.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if not os.path.isdir(libs.cfg.directory_inbox_accepted):
        libs.utils.terminate_fatal(
            "The inbox_accepted directory with the name "
            + str(libs.cfg.directory_inbox_accepted)
            + " does not exist - error="
            + str(OSError),
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Get the SHA256 hash string of a file.
# -----------------------------------------------------------------------------
def get_sha256(file: pathlib.Path) -> str:
    """Get the SHA256 hash string of a file.

    Args:
        file (: pathlib.Path): File.

    Returns:
        str: SHA256 hash string.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    sha256_hash = hashlib.sha256()

    with open(file, "rb") as file_content:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file_content.read(4096), b""):
            sha256_hash.update(byte_block)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    return sha256_hash.hexdigest()


# -----------------------------------------------------------------------------
# Initialise a new child document of the base document.
# -----------------------------------------------------------------------------
def initialise_document_child(journal_action: str) -> None:
    """Initialise a new child document of the base document.

    Prepares a new document for one of the file directories
    'inbox_accepted' or 'inbox_rejected'.

    Args:
        journal_action (str): Journal action data.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.document_child_id = libs.db.orm.insert_dbt_row(
        libs.db.cfg.DBT_DOCUMENT,
        {
            libs.db.cfg.DBC_CHILD_NO: libs.cfg.document_child_child_no,
            libs.db.cfg.DBC_DIRECTORY_NAME: str(libs.cfg.document_child_directory_name),
            libs.db.cfg.DBC_DIRECTORY_TYPE: libs.cfg.document_child_directory_type,
            libs.db.cfg.DBC_DOCUMENT_ID_BASE: libs.cfg.document_child_id_base,
            libs.db.cfg.DBC_DOCUMENT_ID_PARENT: libs.cfg.document_child_id_parent,
            libs.db.cfg.DBC_ERROR_CODE: libs.cfg.document_child_error_code,
            libs.db.cfg.DBC_FILE_NAME: libs.cfg.document_child_file_name,
            libs.db.cfg.DBC_FILE_TYPE: libs.cfg.document_child_file_type,
            libs.db.cfg.DBC_NEXT_STEP: libs.cfg.document_child_next_step,
            libs.db.cfg.DBC_RUN_ID: libs.cfg.run_run_id,
            libs.db.cfg.DBC_STATUS: libs.cfg.document_child_status,
            libs.db.cfg.DBC_STEM_NAME: libs.cfg.document_child_stem_name,
        },
    )

    # pylint: disable=expression-not-assigned
    libs.db.orm.insert_journal(
        __name__,
        inspect.stack()[0][3],
        libs.cfg.document_child_id,
        journal_action,
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create a progress message.
# -----------------------------------------------------------------------------
def progress_msg(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    if libs.cfg.is_verbose:
        final_msg: str = (
            libs.cfg.LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg + "."
        )

        print(final_msg)

        libs.cfg.logger.debug(final_msg)


# -----------------------------------------------------------------------------
# Create a progress message: connected to database.
# -----------------------------------------------------------------------------
def progress_msg_connected() -> None:
    """Create a progress message: connected to database."""
    if libs.cfg.is_verbose:
        print("")
        progress_msg(
            "User '"
            + libs.db.cfg.db_current_user
            + "' is now connected to database '"
            + libs.db.cfg.db_current_database
            + "'"
        )


# -----------------------------------------------------------------------------
# Create a progress message: disconnected from database.
# -----------------------------------------------------------------------------
def progress_msg_disconnected() -> None:
    """Create a progress message: disconnected from database."""
    if libs.cfg.is_verbose:
        if libs.db.cfg.db_current_database is None and libs.db.cfg.db_current_user is None:
            print("")
            libs.utils.progress_msg("Database is now disconnected")
            return

        database = (
            "n/a" if libs.db.cfg.db_current_database is None else libs.db.cfg.db_current_database
        )
        user = "n/a" if libs.db.cfg.db_current_user is None else libs.db.cfg.db_current_user

        print("")
        libs.utils.progress_msg(
            "User '" + user + "' is now disconnected from database '" + database + "'"
        )

        libs.db.cfg.db_current_database = None
        libs.db.cfg.db_current_user = None


# -----------------------------------------------------------------------------
# Create a progress message with empty line before.
# -----------------------------------------------------------------------------
def progress_msg_empty_before(msg: str) -> None:
    """Create a progress message.

    Args:
        msg (str): Progress message.
    """
    if libs.cfg.is_verbose:
        print("")
        progress_msg(msg)


# -----------------------------------------------------------------------------
# Select the documents to be processed.
# -----------------------------------------------------------------------------
def select_documents(conn: Connection, dbt: Table, next_step: str) -> engine.CursorResult:
    """Select the documents to be processed.

    Args:
        conn (Connection): Database connection.
        dbt (Table): database table documents.
        next_step (str): Next processing step.

    Returns:
        engine.CursorResult: The documents found.
    """
    return conn.execute(
        select(
            dbt.c.id,
            dbt.c.directory_name,
            dbt.c.directory_type,
            dbt.c.document_id_base,
            dbt.c.document_id_parent,
            dbt.c.file_name,
            dbt.c.file_type,
            dbt.c.status,
            dbt.c.stem_name,
        )
        .where(
            and_(
                dbt.c.next_step == next_step,
                dbt.c.status.in_(
                    [
                        libs.db.cfg.DOCUMENT_STATUS_ERROR,
                        libs.db.cfg.DOCUMENT_STATUS_START,
                    ]
                ),
            )
        )
        .order_by(dbt.c.id.desc())
    )


# -----------------------------------------------------------------------------
# Start document processing.
# -----------------------------------------------------------------------------
def start_document_processing(document: Row, journal_action: str) -> None:
    """Start document processing.

    Args:
        document (Row): Database row document.
        journal_action (str): Journal action.
    """
    libs.cfg.total_to_be_processed += 1

    libs.cfg.document_directory_name = document.directory_name
    libs.cfg.document_directory_type = document.directory_type
    libs.cfg.document_file_name = document.file_name
    libs.cfg.document_file_type = document.file_type
    libs.cfg.document_id = document.id
    libs.cfg.document_id_base = document.document_id_base
    libs.cfg.document_id_parent = document.document_id_parent
    libs.cfg.document_status = document.status
    libs.cfg.document_stem_name = document.stem_name

    libs.db.orm.update_document_status(
        {
            libs.db.cfg.DBC_STATUS: libs.db.cfg.DOCUMENT_STATUS_START,
        },
        libs.db.orm.insert_journal(
            __name__,
            inspect.stack()[0][3],
            libs.cfg.document_id,
            journal_action.replace("{file_name}", libs.cfg.document_file_name),
        ),
    )

    if libs.cfg.document_status == libs.db.cfg.DOCUMENT_STATUS_START:
        libs.cfg.total_status_ready += 1
    else:
        # not testable
        libs.cfg.total_status_error += 1


# -----------------------------------------------------------------------------
# Convert a string into a file path.
# -----------------------------------------------------------------------------
def str_2_path(param: str) -> pathlib.Path:
    """Convert a string into a file path.

    Args:
        param (str): text parameter.

    Returns:
        pathlib.Path: File path.
    """
    return pathlib.Path(os.path.join(os.getcwd(), *param.split("/" if "/" in param else "\\")))


# -----------------------------------------------------------------------------
# Terminate the application immediately.
# -----------------------------------------------------------------------------
def terminate_fatal(error_msg: str) -> None:
    """Terminate the application immediately.

    Args:
        error_msg (str): Error message.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    print("")
    print(libs.cfg.LOGGER_FATAL_HEAD)
    print(libs.cfg.LOGGER_FATAL_HEAD, error_msg, libs.cfg.LOGGER_FATAL_TAIL, sep="")
    print(libs.cfg.LOGGER_FATAL_HEAD)
    libs.cfg.logger.critical(
        "%s%s%s", libs.cfg.LOGGER_FATAL_HEAD, error_msg, libs.cfg.LOGGER_FATAL_TAIL
    )

    traceback.print_exc(chain=True)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    libs.db.driver.disconnect_db()

    sys.exit(1)
