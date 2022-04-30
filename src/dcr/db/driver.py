"""Module db.driver: Database Definition Management."""
import db.cfg
import db.ddl
import db.dml
import libs.cfg
import libs.utils
import psycopg2
import psycopg2.errors
import psycopg2.extensions
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.pool

# pylint: disable=no-name-in-module


# -----------------------------------------------------------------------------
# Connect to the database.
# -----------------------------------------------------------------------------
def connect_db() -> None:
    """Connect to the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    prepare_connect_db()

    db.cfg.db_orm_metadata = sqlalchemy.MetaData()

    db.cfg.db_orm_engine = sqlalchemy.create_engine(
        libs.cfg.config.db_connection_prefix
        + libs.cfg.config.db_host
        + ":"
        + libs.cfg.config.db_connection_port
        + "/"
        + db.cfg.db_current_database
        + "?user="
        + db.cfg.db_current_user
        + "&password="
        + libs.cfg.config.db_password,
        poolclass=sqlalchemy.pool.NullPool,
    )

    db.cfg.db_orm_engine.connect()

    db.cfg.db_orm_metadata.bind = db.cfg.db_orm_engine

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
        db.cfg.db_driver_conn = psycopg2.connect(
            dbname=db.cfg.db_current_database,
            host=libs.cfg.config.db_host,
            password=libs.cfg.config.db_password_admin,
            port=libs.cfg.config.db_connection_port,
            user=db.cfg.db_current_user,
        )
    except psycopg2.OperationalError as err:
        libs.utils.terminate_fatal(
            f"No database connection possible - error={str(err)}",
        )

    db.cfg.db_driver_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    libs.utils.progress_msg_connected()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database.
# -----------------------------------------------------------------------------
def create_database() -> None:
    """Create the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.config.db_dialect == db.cfg.DB_DIALECT_POSTGRESQL:
        create_database_postgresql()
    else:
        libs.utils.terminate_fatal(f"A database dialect '{libs.cfg.config.db_dialect}' " f"is not supported in DCR")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the PostgreSQL database.
# -----------------------------------------------------------------------------
def create_database_postgresql() -> None:
    """Create the database tables."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    drop_database_postgresql()

    database = libs.cfg.config.db_database
    password = libs.cfg.config.db_password
    user = libs.cfg.config.db_user

    connect_db_admin()

    db.cfg.db_driver_cur = db.cfg.db_driver_conn.cursor()

    db.cfg.db_driver_cur.execute("CREATE USER " + user + " WITH ENCRYPTED PASSWORD '" + password + "'")
    libs.utils.progress_msg(f"The user '{user}' has now been created")

    db.cfg.db_driver_cur.execute("CREATE DATABASE " + database + " WITH OWNER " + user)
    libs.utils.progress_msg("The database '{database}' has now been created")

    db.cfg.db_driver_cur.execute("GRANT ALL PRIVILEGES ON DATABASE " + database + " TO " + user)
    libs.utils.progress_msg("The user '{user}' has now all privileges on database '{database}'")

    disconnect_db()

    db.ddl.create_schema()

    libs.utils.progress_msg(
        f"The database has been successfully created, " f"version number='{libs.cfg.config.dcr_version}"
    )

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Disconnect the database.
# -----------------------------------------------------------------------------
def disconnect_db() -> None:
    """Disconnect the database."""
    if db.cfg.db_orm_metadata is None and db.cfg.db_orm_engine is None:
        db.cfg.db_current_database = None
        db.cfg.db_current_user = None
        libs.utils.progress_msg(
            "There is currently no open database connection (orm)",
        )
        return

    if db.cfg.db_orm_metadata is not None:
        db.cfg.db_orm_metadata.clear()
        db.cfg.db_orm_metadata = None

    if db.cfg.db_orm_engine is not None:
        db.cfg.db_orm_engine.dispose()
        db.cfg.db_orm_engine = None

    libs.utils.progress_msg_disconnected()


# -----------------------------------------------------------------------------
# Drop the database.
# -----------------------------------------------------------------------------
def drop_database() -> None:
    """Drop the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    if libs.cfg.config.db_dialect == db.cfg.DB_DIALECT_POSTGRESQL:
        drop_database_postgresql()
    else:
        libs.utils.terminate_fatal(f"A database dialect '{libs.cfg.config.db_dialect}' " f"is not supported in DCR")

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Drop the PostgreSQL database.
# -----------------------------------------------------------------------------
def drop_database_postgresql() -> None:
    """Drop the PostgreSQL database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    database = libs.cfg.config.db_database
    user = libs.cfg.config.db_user

    connect_db_admin()

    db.cfg.db_driver_cur = db.cfg.db_driver_conn.cursor()

    db.cfg.db_driver_cur.execute("DROP DATABASE IF EXISTS " + database)

    libs.utils.progress_msg(f"If existing, the database '{database}' has now been dropped")

    db.cfg.db_driver_cur.execute("DROP USER IF EXISTS " + user)
    libs.utils.progress_msg(f"If existing, the user '{user}' has now been dropped")

    disconnect_db()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare the database connection for normal users.
# -----------------------------------------------------------------------------
def prepare_connect_db() -> None:
    """Prepare the database connection for normal users."""
    db.cfg.db_current_database = libs.cfg.config.db_database
    db.cfg.db_current_user = libs.cfg.config.db_user


# -----------------------------------------------------------------------------
# Prepare the database connection for administrators.
# -----------------------------------------------------------------------------
def prepare_connect_db_admin() -> None:
    """Prepare the database connection for administrators."""
    db.cfg.db_current_database = libs.cfg.config.db_database_admin
    db.cfg.db_current_user = libs.cfg.config.db_user_admin


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

    db.cfg.db_driver_cur = db.cfg.db_driver_conn.cursor()

    libs.utils.progress_msg("Upgrade the database tables ...")

    current_version: str = db.dml.select_version_version_unique()

    if current_version == libs.cfg.config.dcr_version:
        libs.utils.progress_msg(f"The database is already up to date, version number='{current_version}'")
    else:
        while db.dml.select_version_version_unique() != libs.cfg.config.dcr_version:
            upgrade_database_version()

    disconnect_db()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Upgrade the current database schema - from one version to the next.
# -----------------------------------------------------------------------------
def upgrade_database_version() -> None:
    """Upgrade the current database schema - from one version to the next."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    current_version: str = db.dml.select_version_version_unique()

    if current_version == "0.5.0":
        libs.utils.terminate_fatal(
            "An automatic upgrade of the database version is only " + "supported from version 1.0.0."
        )

    # TBD: Template for migration from version 1.0.0 to version x.x.x
    # if current_version == "0.5.0":
    #     upgrade_database_version_0_5_0()
    #     return

    libs.utils.terminate_fatal(
        "Database file has the wrong version, version number=" + current_version,
    )
