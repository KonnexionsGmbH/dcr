# pylint: disable=unused-argument
"""Testing Module libs.inbox."""
import os
import shutil
import stat

import libs.cfg
import libs.db

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue

TESTS_INBOX = "tests/__PYTEST_FILES__/"

dcr.initialise_logger()


# -----------------------------------------------------------------------------
# Show the state of the inboxes after the test.
# -----------------------------------------------------------------------------
def show_inboxes_after(inbox: str, inbox_accepted: str, inbox_rejected: str) -> None:
    """Show the state of the inboxes after the test.

    Args:
        inbox (str): File directory inbox.
        inbox_accepted (str): File directory inbox_accepted.
        inbox_rejected (str): File directory inbox_rejected.
    """
    # Show the content of the inbox directories.
    print("after: ls inbox=         ", os.listdir(inbox))
    print("after: ls inbox_accepted=", os.listdir(inbox_accepted))
    print("after: ls inbox_rejected=", os.listdir(inbox_rejected))


# -----------------------------------------------------------------------------
# Test File Extension: pdf - pdf_text_ok.
# -----------------------------------------------------------------------------
def test_file_extension_pdf_ok(fxtr_new_db_empty_inbox):
    """Test: pdf - pdf_text_ok.pdf.

    The original file is expected in the file directory inbox_accepted.
    """
    inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    file_inbox = os.path.join(inbox, "pdf_text_ok.pdf")
    file_source = os.path.join(TESTS_INBOX, "pdf_text_ok.pdf")
    file_target = os.path.join(inbox_accepted, "pdf_text_ok_1.pdf")

    shutil.copy(file_source, inbox)

    verify_inboxes_before(inbox, inbox_accepted, inbox_rejected, file_inbox)

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    verify_inbox_accepted_after(inbox, inbox_accepted, inbox_rejected, file_target)


# -----------------------------------------------------------------------------
# Test File Extension: pdf - pdf_wrong_format.
# -----------------------------------------------------------------------------
def test_file_extension_pdf_wrong_format(fxtr_new_db_empty_inbox):
    """Test: pdf - pdf_wrong_format.pdf.

    The original file is expected in the file directory inbox_rejected.
    """
    inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    file_inbox = os.path.join(inbox, "pdf_wrong_format.pdf")
    file_source = os.path.join(TESTS_INBOX, "pdf_wrong_format.pdf")
    file_target = os.path.join(inbox_rejected, "pdf_wrong_format_1.pdf")

    shutil.copy(file_source, inbox)

    verify_inboxes_before(inbox, inbox_accepted, inbox_rejected, file_inbox)

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    verify_inbox_rejected_after(inbox, inbox_accepted, inbox_rejected, file_target)


# -----------------------------------------------------------------------------
# Test File Extension: tiff - tiff_pdf_text_ok_1.
# -----------------------------------------------------------------------------
def test_file_extension_tiff_ok(fxtr_new_db_empty_inbox):
    """Test: tiff - tiff_pdf_text_ok_1.tiff.

    The original file is expected in the file directory inbox_accepted.
    """
    inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    file_inbox = os.path.join(inbox, "tiff_pdf_text_ok_1.tiff")
    file_source = os.path.join(TESTS_INBOX, "tiff_pdf_text_ok_1.tiff")
    file_target = os.path.join(inbox_accepted, "tiff_pdf_text_ok_1_1.tiff")

    shutil.copy(file_source, inbox)

    verify_inboxes_before(inbox, inbox_accepted, inbox_rejected, file_inbox)

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    verify_inbox_accepted_after(inbox, inbox_accepted, inbox_rejected, file_target)


# -----------------------------------------------------------------------------
# Test File Extension: xxx - unknown_file_extension.
# -----------------------------------------------------------------------------
def test_file_extension_unknown_ok(fxtr_new_db_empty_inbox):
    """Test: xxx - unknown_file_extension.xxx.

    Due to the unknown file extension, the original file is expected
    in the file directory inbox_rejected.
    """
    inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]

    file_inbox = os.path.join(inbox, "unknown_file_extension.xxx")
    file_source = os.path.join(TESTS_INBOX, "unknown_file_extension.xxx")
    file_target = os.path.join(inbox_rejected, "unknown_file_extension_1.xxx")

    shutil.copy(file_source, inbox)

    verify_inboxes_before(inbox, inbox_accepted, inbox_rejected, file_inbox)

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    verify_inbox_rejected_after(inbox, inbox_accepted, inbox_rejected, file_target)


# -----------------------------------------------------------------------------
# Show and verify the state of the inbox after the test.
# -----------------------------------------------------------------------------
def verify_inbox_after(
    inbox: str, inbox_accepted: str, inbox_rejected: str, file_inbox: str
) -> None:
    """Show and verify the state of the inbox after the test.

    Args:
        inbox (str): File directory inbox.
        inbox_accepted (str): File directory inbox_accepted.
        inbox_rejected (str): File directory inbox_rejected.
        file_inbox (str): The test file in the file directory input.
    """
    # Show the content of the inbox directories.
    show_inboxes_after(inbox, inbox_accepted, inbox_rejected)

    # Verify the content of the inbox directories.
    assert len(os.listdir(inbox)) == 1, "after: inbox should contain one file"
    assert os.path.isfile(file_inbox), "after: inbox should contain source file"
    assert not os.listdir(inbox_accepted), "after: inbox_accepted should be empty"
    assert not os.listdir(inbox_rejected), "after: inbox_rejected should be empty"


# -----------------------------------------------------------------------------
# Show and verify the state of the inbox_accepted after the test.
# -----------------------------------------------------------------------------
def verify_inbox_accepted_after(
    inbox: str, inbox_accepted: str, inbox_rejected: str, file_target: str
) -> None:
    """Show and verify the state of the inbox_accepted after the test.

    Args:
        inbox (str): File directory inbox.
        inbox_accepted (str): File directory inbox_accepted.
        inbox_rejected (str): File directory inbox_rejected.
        file_target (str): Expected file in the file directory input_accepted.
    """
    # Show the content of the inbox directories.
    show_inboxes_after(inbox, inbox_accepted, inbox_rejected)

    # Verify the content of the inbox directories.
    assert not os.listdir(inbox), "after: inbox should be empty"
    assert len(os.listdir(inbox_accepted)) == 1, "after: inbox_accepted should contain one file"
    assert os.path.isfile(file_target), "after: inbox_accepted should contain target file"
    assert not os.listdir(inbox_rejected), "after: inbox_rejected should be empty"


# -----------------------------------------------------------------------------
# Show and verify the state of the inbox_rejected after the test.
# -----------------------------------------------------------------------------
def verify_inbox_rejected_after(
    inbox: str, inbox_accepted: str, inbox_rejected: str, file_target: str
) -> None:
    """Show and verify the state of the inbox_rejected after the test.

    Args:
        inbox (str): File directory inbox.
        inbox_accepted (str): File directory inbox_accepted.
        inbox_rejected (str): File directory inbox_rejected.
        file_target (str): Expected file in the file directory input_rejected.
    """
    # Show the content of the inbox directories.
    show_inboxes_after(inbox, inbox_accepted, inbox_rejected)

    # Verify the content of the inbox directories.
    assert not os.listdir(inbox), "after: inbox should be empty"
    assert not os.listdir(inbox_accepted), "after: inbox_accepted should be empty"
    assert len(os.listdir(inbox_rejected)) == 1, "after: inbox_rejected should contain one file"
    assert os.path.isfile(file_target), "after: inbox_rejected should contain target file"


# -----------------------------------------------------------------------------
# Show and verify the state of the inboxes before the test.
# -----------------------------------------------------------------------------
def verify_inboxes_before(
    inbox: str, inbox_accepted: str, inbox_rejected: str, file_inbox: str
) -> None:
    """Show and verify the state of the inboxes before the test.

    Args:
        inbox (str): File directory inbox.
        inbox_accepted (str): File directory inbox_accepted.
        inbox_rejected (str): File directory inbox_rejected.
        file_inbox (str): The test file in the file directory input.
    """
    # Show the content of the inbox directories.
    print("before: ls inbox=         ", os.listdir(inbox))
    print("before: file_inbox=       ", file_inbox)
    print(
        "before:    S_IMODE=       ",
        oct(stat.S_IMODE(os.stat(file_inbox).st_mode)),
    )
    if os.path.isdir(inbox_accepted):
        print("before: ls inbox_accepted=", os.listdir(inbox_accepted))
    if os.path.isdir(inbox_rejected):
        print("before: ls inbox_rejected=", os.listdir(inbox_rejected))

    # Verify the content of the inbox directories.
    assert len(os.listdir(inbox)) == 1, "before: inbox should contain one file"
    assert os.path.isfile(file_inbox), "before: inbox should contain source file"
    if os.path.isdir(inbox_accepted):
        assert not os.listdir(inbox_accepted), "before: inbox_accepted should be empty"
    if os.path.isdir(inbox_rejected):
        assert not os.listdir(inbox_rejected), "before: inbox_rejected should be empty"
