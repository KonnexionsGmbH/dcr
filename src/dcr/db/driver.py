"""Module db.driver: Database Administration."""
import cfg.glob
import db.ddl
import db.dml
import psycopg2
import psycopg2.errors
import psycopg2.extensions
import sqlalchemy
import sqlalchemy.exc
import sqlalchemy.orm
import sqlalchemy.pool
import utils

# pylint: disable=no-name-in-module


# -----------------------------------------------------------------------------
# Connect to the database.
# -----------------------------------------------------------------------------
def connect_db() -> None:
    """Connect to the database."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    print("wwe 100")

    prepare_connect_db()

    cfg.glob.db_orm_metadata = sqlalchemy.MetaData()

    cfg.glob.db_orm_engine = sqlalchemy.create_engine(
        cfg.glob.setup.db_connection_prefix
        + cfg.glob.setup.db_host
        + ":"
        + cfg.glob.setup.db_connection_port
        + "/"
        + cfg.glob.db_current_database
        + "?user="
        + cfg.glob.db_current_user
        + "&password="
        + cfg.glob.setup.db_password,
        poolclass=sqlalchemy.pool.NullPool,
    )

    try:
        cfg.glob.db_orm_engine.connect()
    except sqlalchemy.exc.OperationalError as err:
        utils.terminate_fatal(
            f"No database connection possible - error={str(err)}",
        )

    cfg.glob.db_orm_metadata.bind = cfg.glob.db_orm_engine

    utils.progress_msg_connected()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Connect to the admin database.
# -----------------------------------------------------------------------------
def connect_db_admin() -> None:
    """Connect to the admin database."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    prepare_connect_db_admin()

    try:
        cfg.glob.db_driver_conn = psycopg2.connect(
            dbname=cfg.glob.db_current_database,
            host=cfg.glob.setup.db_host,
            password=cfg.glob.setup.db_password_admin,
            port=cfg.glob.setup.db_connection_port,
            user=cfg.glob.db_current_user,
        )
    except psycopg2.OperationalError as err:
        utils.terminate_fatal(
            f"No database connection possible - error={str(err)}",
        )

    cfg.glob.db_driver_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    utils.progress_msg_connected()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the database.
# -----------------------------------------------------------------------------
def create_database() -> None:
    """Create the database."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    if cfg.glob.setup.db_dialect == cfg.glob.DB_DIALECT_POSTGRESQL:
        create_database_postgresql()
    else:
        utils.terminate_fatal(f"A database dialect '{cfg.glob.setup.db_dialect}' " f"is not supported in DCR")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Create the PostgreSQL database.
# -----------------------------------------------------------------------------
def create_database_postgresql() -> None:
    """Create the database tables."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    drop_database_postgresql()

    database = cfg.glob.setup.db_database
    password = cfg.glob.setup.db_password
    user = cfg.glob.setup.db_user

    connect_db_admin()

    cfg.glob.db_driver_cur = cfg.glob.db_driver_conn.cursor()

    cfg.glob.db_driver_cur.execute("CREATE USER " + user + " WITH ENCRYPTED PASSWORD '" + password + "'")
    utils.progress_msg(f"The user '{user}' has now been created")

    cfg.glob.db_driver_cur.execute("CREATE DATABASE " + database + " WITH OWNER " + user)
    utils.progress_msg("The database '{database}' has now been created")

    cfg.glob.db_driver_cur.execute("GRANT ALL PRIVILEGES ON DATABASE " + database + " TO " + user)
    utils.progress_msg("The user '{user}' has now all privileges on database '{database}'")

    disconnect_db()

    db.ddl.create_schema()

    utils.progress_msg(f"The database has been successfully created, " f"version number='{cfg.glob.setup.dcr_version}")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Disconnect the database.
# -----------------------------------------------------------------------------
def disconnect_db() -> None:
    """Disconnect the database."""
    if cfg.glob.db_orm_metadata is None and cfg.glob.db_orm_engine is None:
        cfg.glob.db_current_database = None
        cfg.glob.db_current_user = None
        utils.progress_msg(
            "There is currently no open database connection (orm)",
        )
        return

    if cfg.glob.db_orm_metadata is not None:
        cfg.glob.db_orm_metadata.clear()
        cfg.glob.db_orm_metadata = None

    if cfg.glob.db_orm_engine is not None:
        cfg.glob.db_orm_engine.dispose()
        cfg.glob.db_orm_engine = None

    utils.progress_msg_disconnected()


# -----------------------------------------------------------------------------
# Drop the database.
# -----------------------------------------------------------------------------
def drop_database() -> None:
    """Drop the database."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    if cfg.glob.setup.db_dialect == cfg.glob.DB_DIALECT_POSTGRESQL:
        drop_database_postgresql()
    else:
        utils.terminate_fatal(f"A database dialect '{cfg.glob.setup.db_dialect}' " f"is not supported in DCR")

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Drop the PostgreSQL database.
# -----------------------------------------------------------------------------
def drop_database_postgresql() -> None:
    """Drop the PostgreSQL database."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    database = cfg.glob.setup.db_database
    user = cfg.glob.setup.db_user

    connect_db_admin()

    cfg.glob.db_driver_cur = cfg.glob.db_driver_conn.cursor()

    try:
        cfg.glob.db_driver_cur.execute("DROP DATABASE IF EXISTS " + database)
    except psycopg2.errors.ObjectInUse as err:  # pylint: disable=no-member
        utils.terminate_fatal(
            f"The database can currently not be dropped - error={str(err)}",
        )

    utils.progress_msg(f"If existing, the database '{database}' has now been dropped")

    cfg.glob.db_driver_cur.execute("DROP USER IF EXISTS " + user)
    utils.progress_msg(f"If existing, the user '{user}' has now been dropped")

    disconnect_db()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Prepare the database connection for normal users.
# -----------------------------------------------------------------------------
def prepare_connect_db() -> None:
    """Prepare the database connection for normal users."""
    cfg.glob.db_current_database = cfg.glob.setup.db_database
    cfg.glob.db_current_user = cfg.glob.setup.db_user


# -----------------------------------------------------------------------------
# Prepare the database connection for administrators.
# -----------------------------------------------------------------------------
def prepare_connect_db_admin() -> None:
    """Prepare the database connection for administrators."""
    cfg.glob.db_current_database = cfg.glob.setup.db_database_admin
    cfg.glob.db_current_user = cfg.glob.setup.db_user_admin


# -----------------------------------------------------------------------------
# Upgrade the current database schema.
# -----------------------------------------------------------------------------
def upgrade_database() -> None:
    """Upgrade the current database schema.

    Check if the current database schema needs to be upgraded and
    perform the necessary steps.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    connect_db()

    cfg.glob.db_driver_cur = cfg.glob.db_driver_conn.cursor()

    utils.progress_msg("Upgrade the database tables ...")

    current_version: str = db.dml.select_version_version_unique()

    if current_version == cfg.glob.setup.dcr_version:
        utils.progress_msg(f"The database is already up to date, version number='{current_version}'")
    else:
        while db.dml.select_version_version_unique() != cfg.glob.setup.dcr_version:
            upgrade_database_version()

    disconnect_db()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Upgrade the current database schema - from one version to the next.
# -----------------------------------------------------------------------------
def upgrade_database_version() -> None:
    """Upgrade the current database schema - from one version to the next."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    current_version: str = db.dml.select_version_version_unique()

    if current_version == "0.5.0":
        utils.terminate_fatal("An automatic upgrade of the database version is only " + "supported from version 1.0.0.")

    # TBD: Template for migration from version 1.0.0 to version x.x.x
    # if current_version == "0.5.0":
    #     upgrade_database_version_0_5_0()
    #     return

    utils.terminate_fatal(
        "Database file has the wrong version, version number=" + current_version,
    )
