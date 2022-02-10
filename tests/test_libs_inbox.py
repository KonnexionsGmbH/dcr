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

    inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    shutil.copy(os.path.join(TESTS_INBOX, file_source), inbox)

    print("before: inbox=         ",os.listdir(inbox))

    assert len(os.listdir(inbox)) == 1, "before: inbox should contain one file"
    assert os.path.isfile(os.path.join(inbox , file_source)), "before: inbox should contain source file"

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    print("after: inbox=         ",os.listdir(inbox))
    print("after: inbox_accepted=",os.listdir(inbox_accepted))
    print("after: inbox_rejected=",os.listdir(inbox_rejected))

    assert not os.listdir(inbox), "after: inbox should be empty"
    assert len(os.listdir(inbox_accepted)) == 1, "after: inbox_accepted should contain one file"
    assert os.path.isfile(os.path.join(inbox_accepted , file_target)), "after: inbox should contain target file"
    assert not os.listdir(inbox_rejected), "after: inbox_rejected should be empty"


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

    shutil.copy(os.path.join(TESTS_INBOX, file_source), inbox)

    os.chmod(os.path.join(TESTS_INBOX, file_source), stat.SF_IMMUTABLE)
    
    print("before: inbox=         ",os.listdir(inbox))

    assert len(os.listdir(inbox)) == 1, "before: inbox should contain one file"
    assert os.path.isfile(os.path.join(inbox , file_source)), "before: inbox should contain source file"

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    print("after: inbox=         ",os.listdir(inbox))
    print("after: inbox_accepted=",os.listdir(inbox_accepted))
    print("after: inbox_rejected=",os.listdir(inbox_rejected))

    assert len(os.listdir(inbox)) == 1, "after: inbox should contain one file"
    assert os.path.isfile(os.path.join(inbox , file_source)), "after: inbox should contain source file"
    assert not os.listdir(inbox_accepted), "after: inbox_accepted should be empty"
    assert not os.listdir(inbox_rejected), "after: inbox_rejected should be empty"


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

    shutil.copy(os.path.join(TESTS_INBOX, file_source), inbox)

    print("before: inbox=         ",os.listdir(inbox))

    assert len(os.listdir(inbox)) == 1, "before: inbox should contain one file"
    assert os.path.isfile(os.path.join(inbox , file_source)), "before: inbox should contain source file"

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    print("after: inbox=         ",os.listdir(inbox))
    print("after: inbox_accepted=",os.listdir(inbox_accepted))
    print("after: inbox_rejected=",os.listdir(inbox_rejected))

    assert not os.listdir(inbox), "after: inbox should be empty"
    assert len(os.listdir(inbox_accepted)) == 1, "after: inbox_accepted should contain one file"
    assert os.path.isfile(os.path.join(inbox_accepted , file_target)), "after: inbox should contain target file"
    assert not os.listdir(inbox_rejected), "after: inbox_rejected should be empty"


# -----------------------------------------------------------------------------
# Test File Extension: xxx - unknown_file_extension_protected.
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test_file_unknown_file_extension_ok_protected(fxtr_new_db_empty_inbox):
    """Test: pdf_text_ok."""
    file_source = "unknown_file_extension_protected.xxx"
    file_target = "unknown_file_extension_protected_1.xxx"

    inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX] + "/"
    inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    shutil.copy(os.path.join(TESTS_INBOX, file_source), inbox)

    os.chmod(os.path.join(TESTS_INBOX, file_source), stat.SF_IMMUTABLE)

    print("before: inbox=         ",os.listdir(inbox))

    assert len(os.listdir(inbox)) == 1, "before: inbox should contain one file"
    assert os.path.isfile(os.path.join(inbox , file_source)), "before: inbox should contain source file"

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    print("after: inbox=         ",os.listdir(inbox))
    print("after: inbox_accepted=",os.listdir(inbox_accepted))
    print("after: inbox_rejected=",os.listdir(inbox_rejected))

    assert len(os.listdir(inbox)) == 1, "after: inbox should contain one file"
    assert os.path.isfile(os.path.join(inbox , file_source)), "after: inbox should contain source file"
    assert not os.listdir(inbox_accepted), "after: inbox_accepted should be empty"
    assert not os.listdir(inbox_rejected), "after: inbox_rejected should be empty"

