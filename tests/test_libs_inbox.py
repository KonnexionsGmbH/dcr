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
# Test RUN_ACTION_PROCESS_INBOX - accepted & rejected document files.
# -----------------------------------------------------------------------------
def action_process_inbox_accepted_rejected(
    document_id,
    directory_name,
    stem_name: str,
    file_extension: str,
    no_inboxes: (int, int, int),
) -> Tuple[int, int, int]:
    """Test RUN_ACTION_PROCESS_INBOX - accepted & rejected document files.

    Args:
        document_id (_type_): _description_
        directory_name (str): Directory name of the new addition.
        stem_name (str): Stem name of the new addition.
        file_extension (str): File extension of the new addition.
        no_inboxes Tuple[int,int,int]: Target number of files in the inbox file directories.

    Returns:
        Tuple[int, int, int]: New number of files in the inboxes.
    """
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

    dcr.main([libs.cfg.DCR_ARGV_0, libs.cfg.RUN_ACTION_PROCESS_INBOX])

    no_inbox -= 1
    no_inbox_accepted += 1
    pytest.helpers.verify_action_after(
        directory_name, file_name_target, no_inbox, no_inbox_accepted, no_inbox_rejected
    )

    return no_inbox, no_inbox_accepted, no_inbox_rejected


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

    current_no = action_process_inbox_accepted_rejected(
        current_document_id,
        libs.cfg.directory_inbox_accepted,
        "doc_ok",
        "doc",
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox_accepted_rejected(
        current_document_id,
        libs.cfg.directory_inbox_accepted,
        "docx_ok",
        "docx",
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox_accepted_rejected(
        current_document_id,
        libs.cfg.directory_inbox_accepted,
        "htm_ok",
        "htm",
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox_accepted_rejected(
        current_document_id,
        libs.cfg.directory_inbox_accepted,
        "html_ok",
        "html",
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox_accepted_rejected(
        current_document_id,
        libs.cfg.directory_inbox_accepted,
        "jpeg_pdf_text_ok_1",
        "jpeg",
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox_accepted_rejected(
        current_document_id,
        libs.cfg.directory_inbox_accepted,
        "jpg_pdf_text_ok_1",
        "jpg",
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox_accepted_rejected(
        current_document_id,
        libs.cfg.directory_inbox_accepted,
        "odt_ok",
        "odt",
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox_accepted_rejected(
        current_document_id,
        libs.cfg.directory_inbox_accepted,
        "pdf_scanned_ok",
        "pdf",
        current_no,
    )

    # -------------------------------------------------------------------------
    current_document_id += 2

    current_no = action_process_inbox_accepted_rejected(
        current_document_id,
        libs.cfg.directory_inbox_accepted,
        "pdf_text_ok",
        "pdf",
        current_no,
    )
