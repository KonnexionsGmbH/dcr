# pylint: disable=unused-argument
"""Testing Module db.cls_action"""
import time

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_document
import db.cls_language
import db.cls_run
import db.cls_token
import db.cls_version
import db.dml
import db.driver
import pytest

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=C0302
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - action - case 1.
# -----------------------------------------------------------------------------
def test_missing_dependencies_action_1(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - action - case 1."""
    try:
        cfg.glob.run.exists()  # type: ignore

        del cfg.glob.run

        cfg.glob.logger.debug("The existing object 'cfg.glob.run' of the class Run was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    directory_name = cfg.glob.setup.directory_inbox
    file_name = "pdf_text_ok.pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    values_run = pytest.helpers.create_run()

    values_document = pytest.helpers.create_document()

    with pytest.raises(SystemExit) as expt:
        db.cls_action.Action(
            action_code=db.cls_run.Run.ACTION_CODE_INBOX,
            directory_name=directory_name,
            file_name=file_name,
            id_document=values_document[0],
            id_run_last=values_run[0],
        )

    assert expt.type == SystemExit, "Class Action requires class Run"
    assert expt.value.code == 1, "Class Action requires class Run"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - action - case 2.
# -----------------------------------------------------------------------------
def test_missing_dependencies_action_2(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - action - case 2."""
    try:
        cfg.glob.action_curr.exists()  # type: ignore

        del cfg.glob.action_curr

        cfg.glob.logger.debug("The existing object 'cfg.glob.action_curr' of the class Action was deleted.")
    except AttributeError:
        pass

    try:
        cfg.glob.document.exists()  # type: ignore

        del cfg.glob.document

        cfg.glob.logger.debug("The existing object 'cfg.glob.document' of the class Document was deleted.")
    except AttributeError:
        pass

    try:
        cfg.glob.run.exists()  # type: ignore

        del cfg.glob.run

        cfg.glob.logger.debug("The existing object 'cfg.glob.run' of the class Run was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.start_time_document = time.perf_counter_ns()

    directory_name = cfg.glob.setup.directory_inbox
    file_name = "pdf_text_ok.pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    values_run = pytest.helpers.create_run()

    cfg.glob.run = db.cls_run.Run.from_id(values_run[0])

    # -----------------------------------------------------------------------------
    cfg.glob.language = db.cls_language.Language.from_id(1)

    cfg.glob.language.persist_2_db()

    # -------------------------------------------------------------------------
    # _expected_values_document = pytest.helpers.create_document()
    values_document = pytest.helpers.create_document()

    # -------------------------------------------------------------------------
    local_action = db.cls_action.Action(
        action_code="p_i",
        directory_name=directory_name,
        file_name=file_name,
        id_document=values_document[0],
        id_run_last=values_run[0],
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        local_action.finalise()

    assert expt.type == SystemExit, "Class Action requires class Document (finalise)"
    assert expt.value.code == 1, "Class Action requires class Document (finalise)"

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        local_action.finalise_error("error_code", "error_msg")

    assert expt.type == SystemExit, "Class Action requires class Document (finalise_error)"
    assert expt.value.code == 1, "Class Action requires class Document (finalise_error)"

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    cfg.glob.document = db.cls_document.Document.from_id(1)

    local_action.action_action_code = db.cls_run.Run.ACTION_CODE_PDF2IMAGE

    with pytest.raises(SystemExit) as expt:
        local_action.finalise_error("error_code", "error_msg")

    assert expt.type == SystemExit, "Class Action requires class Action (finalise_error)"
    assert expt.value.code == 1, "Class Action requires class Action (finalise_error)"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
