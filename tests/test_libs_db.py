# pylint: disable=unused-argument
"""Testing Module libs.db."""
import os
import shutil

import libs.cfg
import libs.db
import pytest
from sqlalchemy import Table
from sqlalchemy import delete

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue

TESTS_DATABASES = "tests/__PYTEST_FILES__/DATABASES/"
TESTS_INBOX = "tests/__PYTEST_FILES__/"

dcr.initialise_logger()


# -----------------------------------------------------------------------------
# Test Database Version - Wrong version number in configuration.
# -----------------------------------------------------------------------------
def test_check_db_up_to_date_wrong_version(fxtr_new_db_no_inbox):
    """Test: Wrong version number in configuration."""
    libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION] = "0.0.0"

    with pytest.raises(SystemExit) as expt:
        libs.db.check_db_up_to_date()

    assert expt.type == SystemExit
    assert expt.value.code == 1


# -----------------------------------------------------------------------------
# Test Database Version - No row in table version.
# -----------------------------------------------------------------------------
def test_select_version_unique_not_found(fxtr_new_db_no_inbox):
    """Test: No row in table version."""
    libs.db.connect_db()

    with libs.cfg.engine.begin() as conn:
        version = Table(
            libs.db.DBT_VERSION,
            libs.cfg.metadata,
            autoload_with=libs.cfg.engine,
        )
        conn.execute(delete(version))

    with pytest.raises(SystemExit) as expt:
        libs.db.select_version_version_unique()

    assert expt.type == SystemExit
    assert expt.value.code == 1

    libs.db.disconnect_db()


# -----------------------------------------------------------------------------
# Test Database Version - More than one row in table version.
# -----------------------------------------------------------------------------
def test_select_version_unique_not_unique(fxtr_new_db_no_inbox):
    """Test: More than one row in table version."""
    libs.db.insert_dbt_row(
        libs.db.DBT_VERSION, [{libs.db.DBC_VERSION: "0.0.0"}]
    )

    with pytest.raises(SystemExit) as expt:
        libs.db.select_version_version_unique()

    assert expt.type == SystemExit
    assert expt.value.code == 1


# -----------------------------------------------------------------------------
# Test Database Upgrade - No database file existing.
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test_upgrade_no_database_file(fxtr_no_db):
    """Test: No database file existing."""
    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    assert expt.type == SystemExit
    assert expt.value.code == 1


# -----------------------------------------------------------------------------
# Test Database Upgrade - Database is up to date.
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test_upgrade_up_to_date_already(fxtr_no_db):
    """Test: Database is up to date."""
    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_CREATE_DB])

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    assert (
        libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]
        == libs.db.select_version_version_unique()
    )


# -----------------------------------------------------------------------------
# Test Database Upgrade - Wrong version in database table version.
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test_upgrade_0_1_3(fxtr_no_db):
    """Test: Wrong version in database table version."""
    shutil.copy(
        TESTS_DATABASES + "dcr.db_0.1.3",
        libs.cfg.config[libs.cfg.DCR_CFG_DATABASE_FILE],
    )

    with pytest.raises(SystemExit) as expt:
        dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    assert expt.type == SystemExit
    assert expt.value.code == 1


# -----------------------------------------------------------------------------
# Test Database Upgrade - Upgrade from database table version 0.5.0.
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test_upgrade_0_5_0(fxtr_nothing):
    """Test: Upgrade from database table version 0.5.0."""
    shutil.copy(
        TESTS_DATABASES + "dcr.db_0.5.0",
        libs.cfg.config[libs.cfg.DCR_CFG_DATABASE_FILE],
    )

    inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    shutil.copytree(TESTS_INBOX, inbox_accepted)
    shutil.copytree(TESTS_INBOX, inbox_rejected)

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_UPGRADE_DB])

    assert (
        libs.cfg.config[libs.cfg.DCR_CFG_DCR_VERSION]
        == libs.db.select_version_version_unique()
    )
