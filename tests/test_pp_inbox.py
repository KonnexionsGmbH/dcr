# pylint: disable=unused-argument
"""Testing Module pp.inbox."""
import os.path
import pathlib

import cfg.glob
import db.driver
import libs.utils
import pytest
import sqlalchemy

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - accepted.
# -----------------------------------------------------------------------------
def test_run_action_process_inbox_accepted(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - accepted."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        [
            ("docx_ok", "docx"),
            ("jpeg_pdf_text_ok", "jpeg"),
            ("jpg_pdf_text_ok", "jpg"),
            ("odt_ok", "odt"),
            ("pdf_text_ok", "pdf"),
            ("png_pdf_text_ok", "png"),
            ("README.md", None),
            ("rtf_ok", "rtf"),
            ("tiff_pdf_text_ok", "tiff"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_process_inbox_accepted <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        ["README.md"],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [
            "docx_ok_1.docx",
            "jpeg_pdf_text_ok_3.jpeg",
            "jpg_pdf_text_ok_5.jpg",
            "odt_ok_7.odt",
            "pdf_text_ok_9.pdf",
            "png_pdf_text_ok_11.png",
            "rtf_ok_13.rtf",
            "tiff_pdf_text_ok_15.tiff",
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
# Test RUN_ACTION_PROCESS_INBOX - accepted - delete_auxiliary_file.
# -----------------------------------------------------------------------------
def test_run_action_process_inbox_accepted_delete_auxiliary_file(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - accepted delete_auxiliary_file."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name_1: str = "pdf_text_ok"
    file_ext: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext)], cfg.glob.setup.directory_inbox)

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    db.driver.connect_db()

    libs.utils.delete_auxiliary_file(os.path.join(cfg.glob.setup.directory_inbox_accepted, "pdf_text_ok_1.pdf"))

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        values_original,
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_process_inbox_accepted_duplicate <=========")

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
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - accepted - duplicate.
# -----------------------------------------------------------------------------
def test_run_action_process_inbox_accepted_duplicate(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - accepted duplicate."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name_1: str = "pdf_text_ok"
    file_ext: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext)], cfg.glob.setup.directory_inbox)

    stem_name_2: str = "pdf_text_ok_1"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext)], cfg.glob.setup.directory_inbox_accepted)

    os.rename(
        os.path.join(cfg.glob.setup.directory_inbox_accepted, stem_name_1 + "." + file_ext),
        os.path.join(cfg.glob.setup.directory_inbox_accepted, stem_name_2 + "." + file_ext),
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_process_inbox_accepted_duplicate <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [stem_name_1 + "." + file_ext],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [stem_name_2 + "." + file_ext],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - accepted - duplicate - verbose.
# -----------------------------------------------------------------------------
def test_run_action_process_inbox_accepted_duplicate_verbose(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - accepted duplicate verbose."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    stem_name_1: str = "pdf_text_ok"
    file_ext: str = "pdf"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext)], cfg.glob.setup.directory_inbox)

    stem_name_2: str = "pdf_text_ok_1"

    pytest.helpers.copy_files_4_pytest_2_dir([(stem_name_1, file_ext)], cfg.glob.setup.directory_inbox_accepted)

    os.rename(
        os.path.join(cfg.glob.setup.directory_inbox_accepted, stem_name_1 + "." + file_ext),
        os.path.join(cfg.glob.setup.directory_inbox_accepted, stem_name_2 + "." + file_ext),
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    # -------------------------------------------------------------------------
    cfg.glob.logger.info("=========> test_run_action_process_inbox_accepted_duplicate <=========")

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox,
        [],
        [stem_name_1 + "." + file_ext],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_accepted,
        [],
        [stem_name_2 + "." + file_ext],
    )

    pytest.helpers.verify_content_of_directory(
        cfg.glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_INBOX - french.
# -----------------------------------------------------------------------------
def test_run_action_process_inbox_french(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_INBOX - French."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    # Copy language subdirectory
    pytest.helpers.copy_directories_4_pytest_2_dir(["french"], str(cfg.glob.setup.directory_inbox))

    # -------------------------------------------------------------------------
    # Connect to the database.
    db.driver.connect_db()

    dbt = sqlalchemy.Table(
        cfg.glob.DBT_LANGUAGE,
        cfg.glob.db_orm_metadata,
        autoload_with=cfg.glob.db_orm_engine,
    )

    with cfg.glob.db_orm_engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(
            sqlalchemy.update(dbt).where(dbt.c.iso_language_name == "French").values({cfg.glob.DBC_ACTIVE: True})
        )
        conn.close()

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_VERBOSE, "false"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
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
    language_directory_name = str(os.path.join(base_directory, pathlib.Path("french")))

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
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_IGNORE_DUPLICATES, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
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
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PDF_2_IMAGE])

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_IMAGE_2_PDF])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
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
        cfg.glob.setup._DCR_CFG_SECTION,
        [
            (cfg.glob.setup._DCR_CFG_IGNORE_DUPLICATES, "false"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION,
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
        os.path.join(cfg.glob.setup.directory_inbox_rejected, stem_name_1 + "." + file_ext),
        os.path.join(cfg.glob.setup.directory_inbox_rejected, stem_name_2 + "." + file_ext),
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, cfg.glob.RUN_ACTION_PROCESS_INBOX])

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
