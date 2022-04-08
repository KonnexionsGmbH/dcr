# pylint: disable=unused-argument
"""Testing Module db.orm.connection."""
import db.cfg
import db.driver
import db.orm.connection
import db.orm.dml
import libs.cfg
import libs.utils

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test disconnect without 'db_orm_engine' and 'db_orm_metadata'.
# -----------------------------------------------------------------------------
def test_disconnect_both(fxtr_setup_empty_db_and_inbox):
    """Test disconnect without 'db_orm_engine' and 'db_orm_metadata'."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    db.orm.connection.connect_db()

    db.cfg.db_orm_engine = None
    db.cfg.db_orm_metadata = None

    db.orm.connection.disconnect_db()

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test disconnect without 'db_orm_engine'.
# -----------------------------------------------------------------------------
def test_disconnect_db_orm_engine(fxtr_setup_empty_db_and_inbox):
    """Test disconnect without 'db_orm_engine'."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    db.orm.connection.connect_db()

    db.cfg.db_orm_engine = None

    db.orm.connection.disconnect_db()

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test disconnect without 'db_orm_metadata'.
# -----------------------------------------------------------------------------
def test_disconnect_db_orm_metadata(fxtr_setup_empty_db_and_inbox):
    """Test disconnect without 'db_orm_metadata'."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    db.orm.connection.connect_db()

    db.cfg.db_orm_metadata = None

    db.orm.connection.disconnect_db()

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
