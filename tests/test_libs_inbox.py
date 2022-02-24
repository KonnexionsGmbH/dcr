# pylint: disable=unused-argument
"""Testing Module libs.inbox."""
from typing import Tuple

import libs.cfg
import libs.db
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PDF_2_IMAGE.
# -----------------------------------------------------------------------------
def action_pdf_2_image(
    run_action: str,
    stem_name: str,
    no_inboxes: Tuple[int, int, int],
) -> Tuple[int, int, int]:
    """Test RUN_ACTION_PROCESS_INBOX.

    Args:
        run_action:str: Run action.
        stem_name: str: Stem name.
        no_inboxes Tuple[int,int,int]: Target number of files in the inbox file directories.

    Returns:
        Tuple[int, int, int]: New number of files in the inboxes.
    """
    file_name_target = stem_name + "_1." + libs.cfg.pdf2image_type

    no_inbox, no_inbox_accepted, no_inbox_rejected = no_inboxes

    dcr.main([libs.cfg.DCR_ARGV_0, run_action])

    no_inbox_accepted += 1
    pytest.helpers.verify_action_after(
        libs.cfg.directory_inbox_accepted,
        file_name_target,
        no_inbox,
        no_inbox_accepted,
        no_inbox_rejected,
    )

    return no_inbox, no_inbox_accepted, no_inbox_rejected


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX.
# -----------------------------------------------------------------------------
def action_process_inbox(
    run_action: str,
    document_id,
    file: Tuple[str, str, str],
    no_inboxes: Tuple[int, int, int],
) -> Tuple[int, int, int]:
    """Test RUN_ACTION_PROCESS_INBOX.

    Args:
        run_action:str: Run action.
        document_id (_type_): Document id
        file: Tuple[str, str, str]: Directory_name, stem name and file extension.
        no_inboxes Tuple[int,int,int]: Target number of files in the inbox file directories.

    Returns:
        Tuple[int, int, int]: New number of files in the inboxes.
    """
    directory_name, stem_name, file_extension = file

    file_name_source, file_name_target = pytest.helpers.copy_test_file_2_inbox(
        document_id, stem_name, file_extension
    )

    no_inbox, no_inbox_accepted, no_inbox_rejected = no_inboxes

    no_inbox += 1
    pytest.helpers.verify_action_before(
        file_name_source,
        no_inbox,
        no_inbox_accepted,
        no_inbox_rejected,
    )

    dcr.main([libs.cfg.DCR_ARGV_0, run_action])

    no_inbox -= 1
    if directory_name == libs.cfg.directory_inbox_accepted:
        no_inbox_accepted += 1
    if directory_name == libs.cfg.directory_inbox_rejected:
        no_inbox_rejected += 1
    pytest.helpers.verify_action_after(
        directory_name, file_name_target, no_inbox, no_inbox_accepted, no_inbox_rejected
    )

    return no_inbox, no_inbox_accepted, no_inbox_rejected


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PDF_2_IMAGE.
# -----------------------------------------------------------------------------
def test_run_action_pdf_2_image(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PDF_2_IMAGE."""
    # -------------------------------------------------------------------------
    current_document_id: int = 0

    libs.cfg.directory_inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    current_no_inbox: int = 0

    libs.cfg.directory_inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    current_no_inbox_accepted: int = 0

    libs.cfg.directory_inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]
    current_no_inbox_rejected: int = 0

    current_no = (current_no_inbox, current_no_inbox_accepted, current_no_inbox_rejected)

    # -------------------------------------------------------------------------
    current_document_id += 1

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "pdf_scanned_ok", "pdf"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_no = action_pdf_2_image(
        libs.cfg.RUN_ACTION_PDF_2_IMAGE,
        "pdf_scanned_ok_1",
        current_no,
    )

    # -------------------------------------------------------------------------
    print("Directory: inbox          - Number of files:", current_no[0])
    print("Directory: inbox_accepted - Number of files:", current_no[1])
    print("Directory: inbox_rejected - Number of files:", current_no[2])


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX.
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test_run_action_process_inbox(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX."""
    # -------------------------------------------------------------------------
    current_document_id: int = 0

    libs.cfg.directory_inbox = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX]
    current_no_inbox: int = 0

    libs.cfg.directory_inbox_accepted = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
    current_no_inbox_accepted: int = 0

    libs.cfg.directory_inbox_rejected = libs.cfg.config[libs.cfg.DCR_CFG_DIRECTORY_INBOX_REJECTED]
    current_no_inbox_rejected: int = 0

    current_no = (current_no_inbox, current_no_inbox_accepted, current_no_inbox_rejected)

    # -------------------------------------------------------------------------
    current_document_id += 1

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "doc_ok", "doc"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "docx_ok", "docx"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "htm_ok", "htm"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "html_ok", "html"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "jpeg_pdf_text_ok_1", "jpeg"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "jpg_pdf_text_ok_1", "jpg"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "odt_ok", "odt"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "pdf_scanned_ok", "pdf"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "pdf_text_ok", "pdf"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_rejected, "pdf_text_ok_protected", "pdf"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_rejected, "pdf_wrong_format", "pdf"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "png_pdf_text_ok_1", "png"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "rtf_ok", "rtf"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "tiff_pdf_text_ok_1", "tiff"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_accepted, "txt_ok", "txt"),
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox(
        libs.cfg.RUN_ACTION_PROCESS_INBOX,
        current_document_id,
        (libs.cfg.directory_inbox_rejected, "unknown_file_extension", "xxx"),
        current_no,
    )

    # -------------------------------------------------------------------------
    print("Directory: inbox          - Number of files:", current_no[0])
    print("Directory: inbox_accepted - Number of files:", current_no[1])
    print("Directory: inbox_rejected - Number of files:", current_no[2])
