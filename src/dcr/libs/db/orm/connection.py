"""Module libs.db.orm.connection: Database Connection Management."""
import libs.cfg
import libs.db.cfg
import libs.utils
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import MetaData
from sqlalchemy.pool import NullPool


# -----------------------------------------------------------------------------
# Connect to the database.
# -----------------------------------------------------------------------------
def connect_db() -> None:
    """Connect to the database."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    prepare_connect_db()

    libs.db.cfg.db_orm_metadata = MetaData()

    libs.db.cfg.db_orm_engine = sqlalchemy.create_engine(
        libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PREFIX]
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_HOST]
        + ":"
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_CONNECTION_PORT]
        + "/"
        + libs.db.cfg.db_current_database
        + "?user="
        + libs.db.cfg.db_current_user
        + "&password="
        + libs.cfg.config[libs.cfg.DCR_CFG_DB_PASSWORD],
        poolclass=NullPool,
    )
    libs.db.cfg.db_orm_engine.connect()

    libs.db.cfg.db_orm_metadata.bind = libs.db.cfg.db_orm_engine

    libs.utils.progress_msg_connected()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Disconnect the database.
# -----------------------------------------------------------------------------
def disconnect_db() -> None:
    """Disconnect the database."""
    if libs.db.cfg.db_orm_metadata is None and libs.db.cfg.db_orm_engine is None:
        libs.db.cfg.db_current_database = None
        libs.db.cfg.db_current_user = None
        libs.utils.progress_msg(
            "There is currently no open database connection (orm)",
        )
        return

    if libs.db.cfg.db_orm_metadata is not None:
        libs.db.cfg.db_orm_metadata.clear()
        libs.db.cfg.db_orm_metadata = None

    if libs.db.cfg.db_orm_engine is not None:
        libs.db.cfg.db_orm_engine.dispose()
        libs.db.cfg.db_orm_engine = None

    libs.utils.progress_msg_disconnected()


# -----------------------------------------------------------------------------
# Prepare the database connection for normal users.
# -----------------------------------------------------------------------------
def prepare_connect_db() -> None:
    """Prepare the database connection for normal users."""
    libs.db.cfg.db_current_database = libs.cfg.config[libs.cfg.DCR_CFG_DB_DATABASE]
    libs.db.cfg.db_current_user = libs.cfg.config[libs.cfg.DCR_CFG_DB_USER]
