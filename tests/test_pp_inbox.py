# pylint: disable=unused-argument
"""Testing Module pp.inbox."""
import os.path
import pathlib
import shutil

import cfg.glob
import db.cls_run
import db.driver
import pytest
import sqlalchemy
import utils

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - accepted - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_process_inbox_accepted_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - accepted duplicate."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name_1: str = "pdf_text_ok"
    file_ext: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            (stem_name_1, file_ext),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    stem_name_2: str = "pdf_text_ok_1"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext)], cfg.glob.setup.directory_inbox_accepted)

    os.rename(
        utils.get_full_name(cfg.glob.setup.directory_inbox_accepted, stem_name_1 + "." + file_ext),
        utils.get_full_name(cfg.glob.setup.directory_inbox_accepted, stem_name_2 + "." + file_ext),
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_process_inbox_accepted_duplicate <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox=(
            [],
            [
                [stem_name_1 + "." + file_ext],
            ],
        ),
        inbox_accepted=(
            [],
            [
                [stem_name_2 + "." + file_ext],
            ],
        ),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - french.
# -----------------------------------------------------------------------------
@pytest.mark.issue
def test_run_action_process_inbox_french(fxtr_setup_logger_environment):
    """Test RUN_ACTION_PROCESS_INBOX - French."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    initial_database_data_path = pathlib.Path(cfg.glob.setup.initial_database_data)
    initial_database_data_path_directory = os.path.dirname(initial_database_data_path)
    initial_database_data_path_file_name = os.path.basename(initial_database_data_path)

    initial_database_data_path_file_name_test = "initial_database_data_french.json"

    # copy test file
    shutil.copy(
        utils.get_full_name(cfg.glob.TESTS_INBOX_NAME, initial_database_data_path_file_name_test),
        utils.get_full_name(initial_database_data_path_directory, initial_database_data_path_file_name),
    )

    db.driver.create_database()

    # -------------------------------------------------------------------------
    # Copy language subdirectory
    pytest.helpers.copy_directories_4_pytest_2_dir(["french"], str(cfg.glob.setup.directory_inbox))

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE, "false"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_process_inbox_french <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        ["french"],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            "docx_french_ok_1.docx",
            "pdf_french_ok_3.jpg",
            "pdf_french_ok_5.pdf",
            "pdf_french_scanned_7.pdf",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    base_directory = str(cfg.glob.setup.directory_inbox)
    language_directory_name = str(utils.get_full_name(base_directory, pathlib.Path("french")))

    assert os.path.isdir(base_directory), "base directory '" + base_directory + "' after processing missing"

    assert os.path.isdir(language_directory_name), (
        "language directory '" + language_directory_name + "' after processing missing"
    )

    assert 0 == len(os.listdir(language_directory_name)), (
        str(len(os.listdir(language_directory_name))) + " files still found after processing"
    )

    # -------------------------------------------------------------------------
    # Check empty language subdirectory
    # TBD

    # -------------------------------------------------------------------------
    # Test not language English in document
    # TBD

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - ignore duplicates.
# -----------------------------------------------------------------------------
def test_run_action_process_inbox_ignore_duplicates(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - ignore duplicates."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_text_ok", "pdf"),
            ("pdf_text_ok_protected", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_IGNORE_DUPLICATES, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_process_inbox_ignore_duplicates <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            "pdf_text_ok_1.pdf",
            "pdf_text_ok_protected_3.pdf",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - normal.
# -----------------------------------------------------------------------------
def test_run_action_process_inbox_normal(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - normal."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name: str = "pdf_scanned_ok"
    file_ext: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name, file_ext)], cfg.glob.setup.directory_inbox)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_TESSERACT])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_process_inbox_normal <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            stem_name + "_1." + file_ext,
            stem_name + "_1_1." + cfg.glob.setup.pdf2image_type,
            stem_name + "_1_1." + cfg.glob.DOCUMENT_FILE_TYPE_PDF,
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - rejected.
# -----------------------------------------------------------------------------
def test_run_action_process_inbox_rejected(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - rejected."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    fxtr_rmdir_opt(cfg.glob.setup.directory_inbox_accepted)

    fxtr_rmdir_opt(cfg.glob.setup.directory_inbox_rejected)

    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("pdf_text_ok", "pdf"),
            ("pdf_text_ok_protected", "pdf"),
            ("pdf_wrong_format", "pdf"),
            ("unknown_file_extension", "xxx"),
            ("unknown_file_extension_protected", "xxx"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_IGNORE_DUPLICATES, "false"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_process_inbox_rejected <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            "pdf_text_ok_1.pdf",
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [
            "pdf_text_ok_protected_3.pdf",
            "pdf_wrong_format_5.pdf",
            "unknown_file_extension_7.xxx",
            "unknown_file_extension_protected_9.xxx",
        ],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - rejected - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_process_inbox_rejected_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - rejected duplicate."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name_1: str = "pdf_wrong_format"
    file_ext: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext)], cfg.glob.setup.directory_inbox)

    stem_name_2: str = "pdf_wrong_format_1"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext)], cfg.glob.setup.directory_inbox_rejected)

    os.rename(
        utils.get_full_name(cfg.glob.setup.directory_inbox_rejected, stem_name_1 + "." + file_ext),
        utils.get_full_name(cfg.glob.setup.directory_inbox_rejected, stem_name_2 + "." + file_ext),
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_process_inbox_rejected_duplicate <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [
            stem_name_1 + "." + file_ext,
        ],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [
            stem_name_2 + "." + file_ext,
        ],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
