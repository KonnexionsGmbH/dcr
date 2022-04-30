# pylint: disable=unused-argument
"""Testing Module db.driver."""
import db.cfg
import db.driver
import db.orm.dml
import libs.cfg
import libs.utils
import pytest
import setup.config

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - connect_db().
# -----------------------------------------------------------------------------
def test_connect_db(fxtr_setup_logger_environment):
    """Test: connect_db()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    config_section = libs.cfg.config._DCR_CFG_SECTION_TEST

    values_original = pytest.helpers.backup_config_params(
        config_section,
        [
            (libs.cfg.config._DCR_CFG_DB_CONNECTION_PORT, "9999"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    with pytest.raises(SystemExit) as expt:
        db.driver.connect_db()

    assert expt.type == SystemExit, "DCR_CFG_DB_CONNECTION_PORT: no database"
    assert expt.value.code == 1, "DCR_CFG_DB_CONNECTION_PORT: no database"

    pytest.helpers.restore_config_params(
        config_section,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - connect_db_admin().
# -----------------------------------------------------------------------------
def test_connect_db_admin(fxtr_setup_logger_environment):
    """Test: connect_db_admin()."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    config_section = libs.cfg.config._DCR_CFG_SECTION_TEST

    values_original = pytest.helpers.backup_config_params(
        config_section,
        [
            (libs.cfg.config._DCR_CFG_DB_CONNECTION_PORT, "9999"),
        ],
    )

    libs.cfg.config = setup.config.Config()

    with pytest.raises(SystemExit) as expt:
        db.driver.connect_db_admin()

    assert expt.type == SystemExit, "DCR_CFG_DB_CONNECTION_PORT: no database"
    assert expt.value.code == 1, "DCR_CFG_DB_CONNECTION_PORT: no database"

    pytest.helpers.restore_config_params(
        config_section,
        values_original,
    )

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test disconnect without 'db_orm_engine' and 'db_orm_metadata'.
# -----------------------------------------------------------------------------
def test_disconnect_both(fxtr_setup_empty_db_and_inbox):
    """Test disconnect without 'db_orm_engine' and 'db_orm_metadata'."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    db.cfg.db_orm_engine = None
    db.cfg.db_orm_metadata = None

    db.driver.disconnect_db()

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test disconnect without 'db_orm_engine'.
# -----------------------------------------------------------------------------
def test_disconnect_db_orm_engine(fxtr_setup_empty_db_and_inbox):
    """Test disconnect without 'db_orm_engine'."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    db.cfg.db_orm_engine = None

    db.driver.disconnect_db()

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Test disconnect without 'db_orm_metadata'.
# -----------------------------------------------------------------------------
def test_disconnect_db_orm_metadata(fxtr_setup_empty_db_and_inbox):
    """Test disconnect without 'db_orm_metadata'."""
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    db.cfg.db_orm_metadata = None

    db.driver.disconnect_db()

    # -------------------------------------------------------------------------
    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
