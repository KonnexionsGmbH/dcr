"""Module db.orm.connection: Database Connection Management."""
import db.cfg
import libs.cfg
import libs.utils
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.pool


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
# Prepare the database connection for normal users.
# -----------------------------------------------------------------------------
def prepare_connect_db() -> None:
    """Prepare the database connection for normal users."""
    db.cfg.db_current_database = libs.cfg.config.db_database
    db.cfg.db_current_user = libs.cfg.config.db_user
