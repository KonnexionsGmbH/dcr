"""Module db: Database Definition Management.

Data definition related processing routines.

Returns:
    [type]: None.
"""

import libs.cfg
import libs.db.orm
import libs.utils
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# -----------------------------------------------------------------------------
# Connect to the admin database.
# -----------------------------------------------------------------------------
def connect_db_admin():
    """Connect to the admin database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.db_current_database = libs.cfg.config[libs.cfg.DCR_CFG_DB_DATABASE_ADMIN]
    libs.cfg.db_current_user = libs.cfg.config[libs.cfg.DCR_CFG_DB_USER_ADMIN]

    conn = psycopg2.connect(
        dbname=libs.cfg.db_current_database,
        host=libs.cfg.config[libs.cfg.DCR_CFG_DB_HOST],
        password=libs.cfg.config[libs.cfg.DCR_CFG_DB_PASSWORD_ADMIN],
        port=libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PORT],
        user=libs.cfg.db_current_user,
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    libs.utils.progress_msg_connected()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    return conn


# -----------------------------------------------------------------------------
# Create the database.
# -----------------------------------------------------------------------------
def create_database() -> None:
    """Create the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.DCR_CFG_DB_DIALECT not in libs.cfg.config:
        create_database_postgresql()
    elif libs.cfg.config[libs.cfg.DCR_CFG_DB_DIALECT] == libs.db.orm.DB_DIALECT_POSTGRESQL:
        create_database_postgresql()
    else:
        libs.utils.terminate_fatal(
            "A database dialect '"
            + libs.cfg.config[libs.cfg.DCR_CFG_DB_DIALECT]
            + "' is not supported in DCR"
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the PostgreSQL database.
# -----------------------------------------------------------------------------
def create_database_postgresql() -> None:
    """Create the database tables."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    drop_database_postgresql()

    database = libs.cfg.config[libs.cfg.DCR_CFG_DB_DATABASE]
    password = libs.cfg.config[libs.cfg.DCR_CFG_DB_PASSWORD]
    user = libs.cfg.config[libs.cfg.DCR_CFG_DB_USER]

    conn = connect_db_admin()

    cur = conn.cursor()

    cur.execute("CREATE USER " + user + " WITH ENCRYPTED PASSWORD '" + password + "'")
    libs.utils.progress_msg("The user '" + user + "' has now been created")

    cur.execute("CREATE DATABASE " + database + " WITH OWNER " + user)
    libs.utils.progress_msg("The database '" + database + "' has now been created")

    cur.execute("GRANT ALL PRIVILEGES ON DATABASE " + database + " TO " + user)
    libs.utils.progress_msg(
        "The user '" + user + "' has now all privileges on database '" + database + "'"
    )

    disconnect_db_admin(conn, cur)

    libs.db.orm.create_schema()

    libs.utils.progress_msg(
        "The database has been successfully created, version number="
        + libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION],
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Disconnect the admin database.
# -----------------------------------------------------------------------------
def disconnect_db_admin(conn, cur) -> None:
    """Disconnect the admin database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    cur.close()

    conn.close()

    libs.utils.progress_msg_disconnected()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Drop the database.
# -----------------------------------------------------------------------------
def drop_database() -> None:
    """Drop the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.DCR_CFG_DB_DIALECT not in libs.cfg.config:
        drop_database_postgresql()
    elif libs.cfg.config[libs.cfg.DCR_CFG_DB_DIALECT] == libs.db.orm.DB_DIALECT_POSTGRESQL:
        drop_database_postgresql()
    else:
        libs.utils.terminate_fatal(
            "A database dialect '"
            + libs.cfg.config[libs.cfg.DCR_CFG_DB_DIALECT]
            + "' is not supported in DCR"
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Drop the PostgreSQL database.
# -----------------------------------------------------------------------------
def drop_database_postgresql() -> None:
    """Drop the PostgreSQL database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    database = libs.cfg.config[libs.cfg.DCR_CFG_DB_DATABASE]
    user = libs.cfg.config[libs.cfg.DCR_CFG_DB_USER]

    conn = connect_db_admin()

    cur = conn.cursor()

    cur.execute("DROP DATABASE IF EXISTS " + database)
    libs.utils.progress_msg("If existing, the database '" + database + "' has now been dropped")

    cur.execute("DROP USER IF EXISTS " + user)
    libs.utils.progress_msg("If existing, the user '" + user + "' has now been dropped")

    disconnect_db_admin(conn, cur)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Upgrade the current database schema.
# -----------------------------------------------------------------------------
def upgrade_database() -> None:
    """Upgrade the current database schema.

    Check if the current database schema needs to be upgraded and
    perform the necessary steps.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    connect_db_admin()

    libs.utils.progress_msg("Upgrade the database tables ...")

    current_version: str = libs.db.orm.select_version_version_unique()

    if current_version == libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]:
        libs.utils.progress_msg(
            "The database is already up to date, version number=" + current_version,
        )
    else:
        while (
            libs.db.orm.select_version_version_unique()
            != libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]
        ):
            upgrade_database_version()

        libs.utils.progress_msg(
            "The database has been successfully upgraded, version number="
            + libs.db.orm.select_version_version_unique(),
        )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Upgrade the current database schema - from one version to the next.
# -----------------------------------------------------------------------------
def upgrade_database_version() -> None:
    """Upgrade the current database schema - from one version to the next."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    current_version: str = libs.db.orm.select_version_version_unique()

    if current_version == "0.5.0":
        libs.utils.progress_msg(
            "An automatic upgrade of the database version is only "
            + "supported from version 1.0.0."
        )
        libs.cfg.logger.debug(libs.cfg.LOGGER_END)
        return

    # TBD: Template for migration from version 1.0.0 to version x.x.x
    # if current_version == "0.5.0":
    #     upgrade_database_version_0_5_0()
    #     return

    libs.utils.terminate_fatal(
        "Database file has the wrong version, version number=" + current_version,
    )
