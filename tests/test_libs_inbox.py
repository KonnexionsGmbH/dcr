# pylint: disable=unused-argument
"""Testing Module libs.inbox."""
import os
import shutil
import stat

import libs.cfg
import libs.db
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue

TESTS_INBOX = "tests/inbox/"

dcr.initialise_logger()

# -----------------------------------------------------------------------------
# Test File Extension: pdf - pdf_text_ok.
# -----------------------------------------------------------------------------
def test_file_extension_pdf_ok(fxtr_new_db_empty_inbox):
    """Test: pdf_text_ok."""
    file_source = "pdf_text_ok.pdf"
    file_target = "pdf_text_ok_1.pdf"

    inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX] + "/"
    inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    shutil.copy(TESTS_INBOX + file_source, inbox)

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    # Directory inbox ist empty
    assert not os.listdir(inbox)
    # Directory inbox_accepted contains exactly one file
    assert len(os.listdir(inbox_accepted)) == 1
    assert os.path.isfile(inbox_accepted + "/" + file_target)
    # Directory inbox_rejected ist empty
    assert not os.listdir(inbox_rejected)


# -----------------------------------------------------------------------------
# Test File Extension: pdf - pdf_text_ok_protected.
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test_file_extension_pdf_ok_protected(fxtr_new_db_empty_inbox):
    """Test: pdf_text_ok."""
    file_source = "pdf_text_ok_protected.pdf"
    file_target = "pdf_text_ok_protected_1.pdf"

    inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX] + "/"
    inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    shutil.copy(TESTS_INBOX + file_source, inbox)

    os.chmod(inbox + file_source, stat.SF_IMMUTABLE)

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    # Directory inbox ist empty
    assert not os.listdir(inbox)
    # Directory inbox_accepted contains exactly one file
    assert len(os.listdir(inbox_accepted)) == 1
    assert os.path.isfile(inbox_accepted + "/" + file_target)
    # Directory inbox_rejected ist empty
    assert not os.listdir(inbox_rejected)


# -----------------------------------------------------------------------------
# Test File Extension: xxx - unknown_file_extension.
# -----------------------------------------------------------------------------
def test_file_unknown_file_extension_ok(fxtr_new_db_empty_inbox):
    """Test: pdf_text_ok."""
    file_source = "unknown_file_extension.xxx"
    file_target = "unknown_file_extension_1.xxx"

    inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX] + "/"
    inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    shutil.copy(TESTS_INBOX + file_source, inbox)

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    # Directory inbox ist empty
    assert not os.listdir(inbox)
    # Directory inbox_accepted ist empty
    assert not os.listdir(inbox_accepted)
    # Directory inbox_rejected contains exactly one file
    assert len(os.listdir(inbox_rejected)) == 1
    assert os.path.isfile(inbox_rejected + "/" + file_target)
