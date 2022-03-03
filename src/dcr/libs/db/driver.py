"""Database Definition Management.

Returns:
    [type]: None.
"""
import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.utils
import psycopg2

# pylint: disable=no-name-in-module
# not testable
# from psycopg2.errors import ObjectInUse
from psycopg2.errors import OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# -----------------------------------------------------------------------------
# Connect to the database.
# -----------------------------------------------------------------------------
def connect_db() -> None:
    """Connect to the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.db.orm.prepare_connect_db()

    try:
        libs.db.cfg.db_driver_conn = psycopg2.connect(
            dbname=libs.db.cfg.db_current_database,
            host=libs.cfg.config[libs.cfg.DCR_CFG_DB_HOST],
            password=libs.cfg.config[libs.cfg.DCR_CFG_DB_PASSWORD],
            port=libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PORT],
            user=libs.db.cfg.db_current_user,
        )
    except OperationalError as err:
        libs.utils.terminate_fatal(
            "No database connection possible - error=" + str(err),
        )

    libs.db.cfg.db_driver_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    libs.utils.progress_msg_connected()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Connect to the admin database.
# -----------------------------------------------------------------------------
def connect_db_admin() -> None:
    """Connect to the admin database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    prepare_connect_db_admin()

    try:
        libs.db.cfg.db_driver_conn = psycopg2.connect(
            dbname=libs.db.cfg.db_current_database,
            host=libs.cfg.config[libs.cfg.DCR_CFG_DB_HOST],
            password=libs.cfg.config[libs.cfg.DCR_CFG_DB_PASSWORD_ADMIN],
            port=libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PORT],
            user=libs.db.cfg.db_current_user,
        )
    except OperationalError as err:
        libs.utils.terminate_fatal(
            "No database connection possible - error=" + str(err),
        )

    libs.db.cfg.db_driver_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    libs.utils.progress_msg_connected()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database.
# -----------------------------------------------------------------------------
def create_database() -> None:
    """Create the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.DCR_CFG_DB_DIALECT not in libs.cfg.config:
        create_database_postgresql()
    elif libs.cfg.config[libs.cfg.DCR_CFG_DB_DIALECT] == libs.db.cfg.DB_DIALECT_POSTGRESQL:
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

    connect_db_admin()

    libs.db.cfg.db_driver_cur = libs.db.cfg.db_driver_conn.cursor()

    libs.db.cfg.db_driver_cur.execute(
        "CREATE USER " + user + " WITH ENCRYPTED PASSWORD '" + password + "'"
    )
    libs.utils.progress_msg("The user '" + user + "' has now been created")

    libs.db.cfg.db_driver_cur.execute("CREATE DATABASE " + database + " WITH OWNER " + user)
    libs.utils.progress_msg("The database '" + database + "' has now been created")

    libs.db.cfg.db_driver_cur.execute(
        "GRANT ALL PRIVILEGES ON DATABASE " + database + " TO " + user
    )
    libs.utils.progress_msg(
        "The user '" + user + "' has now all privileges on database '" + database + "'"
    )

    disconnect_db()

    libs.db.orm.create_schema()

    libs.utils.progress_msg(
        "The database has been successfully created, version number="
        + libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION],
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Disconnect the admin database.
# -----------------------------------------------------------------------------
def disconnect_db() -> None:
    """Disconnect the admin database."""
    if libs.db.cfg.db_driver_cur is None and libs.db.cfg.db_driver_conn is None:
        libs.db.cfg.db_current_database = None
        libs.db.cfg.db_current_user = None
        libs.utils.progress_msg(
            "There is currently no open database connection (psycopg2)",
        )
        return

    if libs.db.cfg.db_driver_cur is not None:
        libs.db.cfg.db_driver_cur.close()
        libs.db.cfg.db_driver_cur = None

    if libs.db.cfg.db_driver_conn is not None:
        libs.db.cfg.db_driver_conn.close()
        libs.db.cfg.db_driver_conn = None

    libs.utils.progress_msg_disconnected()


# -----------------------------------------------------------------------------
# Drop the database.
# -----------------------------------------------------------------------------
def drop_database() -> None:
    """Drop the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.DCR_CFG_DB_DIALECT not in libs.cfg.config:
        drop_database_postgresql()
    elif libs.cfg.config[libs.cfg.DCR_CFG_DB_DIALECT] == libs.db.cfg.DB_DIALECT_POSTGRESQL:
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

    connect_db_admin()

    libs.db.cfg.db_driver_cur = libs.db.cfg.db_driver_conn.cursor()

    libs.db.cfg.db_driver_cur.execute("DROP DATABASE IF EXISTS " + database)

    # not testable
    # try:
    #     libs.db.cfg.db_driver_cur.execute("DROP DATABASE IF EXISTS " + database)
    # except ObjectInUse as err:
    #     libs.utils.terminate_fatal("The database cannot be dropped - error=" + str(err))

    libs.utils.progress_msg("If existing, the database '" + database + "' has now been dropped")

    libs.db.cfg.db_driver_cur.execute("DROP USER IF EXISTS " + user)
    libs.utils.progress_msg("If existing, the user '" + user + "' has now been dropped")

    disconnect_db()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare the database connection for administrators.
# -----------------------------------------------------------------------------
def prepare_connect_db_admin() -> None:
    """Prepare the database connection for administrators."""
    libs.db.cfg.db_current_database = libs.cfg.config[libs.cfg.DCR_CFG_DB_DATABASE_ADMIN]
    libs.db.cfg.db_current_user = libs.cfg.config[libs.cfg.DCR_CFG_DB_USER_ADMIN]


# -----------------------------------------------------------------------------
# Get the version number from the database table 'version'.
# -----------------------------------------------------------------------------
def select_version_version_unique() -> str:
    """Get the version number from the database table 'version'.

    Returns:
        str: The version number found.
    """
    libs.db.cfg.db_driver_cur.execute(
        "SELECT "
        + libs.db.cfg.DBC_VERSION
        + " FROM "
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_SCHEMA]
        + "."
        + libs.db.cfg.DBT_VERSION
    )

    current_version: str = ""

    for row in libs.db.cfg.db_driver_cur.fetchall():
        if current_version == "":
            current_version = row[0]
        else:
            libs.utils.terminate_fatal(
                "Column version in database table version not unique",
            )

    if current_version == "":
        libs.utils.terminate_fatal("Column version in database table version not found")

    return current_version


# -----------------------------------------------------------------------------
# Upgrade the current database schema.
# -----------------------------------------------------------------------------
def upgrade_database() -> None:
    """Upgrade the current database schema.

    Check if the current database schema needs to be upgraded and
    perform the necessary steps.
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    connect_db()

    libs.db.cfg.db_driver_cur = libs.db.cfg.db_driver_conn.cursor()

    libs.utils.progress_msg("Upgrade the database tables ...")

    current_version: str = select_version_version_unique()

    if current_version == libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]:
        libs.utils.progress_msg(
            "The database is already up to date, version number=" + current_version,
        )
    else:
        while select_version_version_unique() != libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]:
            upgrade_database_version()

        # not testable
        # libs.utils.progress_msg(
        #     "The database has been successfully upgraded, version number="
        #     + select_version_version_unique(),
        # )

    disconnect_db()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Upgrade the current database schema - from one version to the next.
# -----------------------------------------------------------------------------
def upgrade_database_version() -> None:
    """Upgrade the current database schema - from one version to the next."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    current_version: str = select_version_version_unique()

    if current_version == "0.5.0":
        libs.utils.terminate_fatal(
            "An automatic upgrade of the database version is only "
            + "supported from version 1.0.0."
        )

    # TBD: Template for migration from version 1.0.0 to version x.x.x
    # if current_version == "0.5.0":
    #     upgrade_database_version_0_5_0()
    #     return

    libs.utils.terminate_fatal(
        "Database file has the wrong version, version number=" + current_version,
    )
