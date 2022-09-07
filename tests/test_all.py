# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Testing Module all."""

import dcr_core.cls_setup
import dcr_core.core_glob
import dcr_core.core_utils
import pytest

import dcr.cfg.cls_setup
import dcr.cfg.glob
import dcr.db.cls_action
import dcr.db.cls_db_core
import dcr.db.cls_document
import dcr.db.cls_language
import dcr.db.cls_run
import dcr.db.cls_token
import dcr.db.cls_version
import dcr.launcher

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=unused-argument
# @pytest.mark.issue


# -----------------------------------------------------------------------------
# Check the database content.
# -----------------------------------------------------------------------------
def check_db_content() -> None:
    """Check the database content."""
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    check_db_content_action()

    check_db_content_document()

    check_db_content_language()

    check_db_content_run()

    check_db_content_version()

    # -----------------------------------------------------------------------------
    # Database table language.
    # -----------------------------------------------------------------------------
    pytest.helpers.check_dbt_language(
        (
            1,
            (
                1,
                True,
                "eng",
                "en",
                "en_core_web_trf",
                "eng",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test"),
                "English",
            ),
        )
    )
    pytest.helpers.check_dbt_language(
        (
            2,
            (
                2,
                True,
                "deu",
                "de",
                "de_dep_news_trf",
                "deu",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test\\deutsch"),
                "Deutsch",
            ),
        )
    )
    pytest.helpers.check_dbt_language((3, (3, False, "fra", "fr", "fr_dep_news_trf", "fra", "", "French")))
    pytest.helpers.check_dbt_language((4, (4, False, "ita", "it", "it_core_news_lg", "ita", "", "Italian")))

    # -----------------------------------------------------------------------------
    # Database table run.
    # -----------------------------------------------------------------------------
    pytest.helpers.check_dbt_run((1, (1, "p_i", "inbox         (preprocessor)", 1, "end", 1, 5, 6)))
    pytest.helpers.check_dbt_run((2, (2, "p_2_i", "pdf2image     (preprocessor)", 1, "end", 0, 2, 2)))
    pytest.helpers.check_dbt_run((3, (3, "ocr", "tesseract     (preprocessor)", 1, "end", 0, 4, 3)))
    pytest.helpers.check_dbt_run((4, (4, "n_2_p", "pandoc        (preprocessor)", 1, "end", 0, 1, 1)))
    pytest.helpers.check_dbt_run((5, (5, "tet", "pdflib        (nlp)", 1, "end", 0, 5, 5)))
    pytest.helpers.check_dbt_run((6, (6, "s_p_j", "parser        (nlp)", 1, "end", 0, 5, 5)))
    pytest.helpers.check_dbt_run((7, (7, "tkn", "tokenizer     (nlp)", 1, "end", 0, 5, 5)))

    # -----------------------------------------------------------------------------
    # Database table version.
    # -----------------------------------------------------------------------------
    pytest.helpers.check_dbt_version((1, (1, dcr_core.cls_setup.Setup.DCR_VERSION)))


# -----------------------------------------------------------------------------
# Check the database content - database table action.
# -----------------------------------------------------------------------------
def check_db_content_action() -> None:
    """Check the database content - database table action."""
    pytest.helpers.check_dbt_action(
        (
            1,
            (
                1,
                "p_i",
                "inbox         (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test"),
                "inbox",
                "",
                "",
                0,
                "docx_ok.docx",
                1,
                1,
                1,
                0,
                -1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            2,
            (
                2,
                "n_2_p",
                "pandoc        (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "docx_ok_1.docx",
                1,
                2,
                1,
                0,
                -1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            3,
            (
                3,
                "p_i",
                "inbox         (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test"),
                "inbox",
                "",
                "",
                0,
                "jpeg_pdf_text_ok.jpeg",
                2,
                3,
                1,
                0,
                -1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            4,
            (
                4,
                "ocr",
                "tesseract     (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "jpeg_pdf_text_ok_2.jpeg",
                2,
                3,
                1,
                0,
                -1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            5,
            (
                5,
                "p_i",
                "inbox         (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test"),
                "inbox",
                "",
                "",
                0,
                "pdf_scanned_ok.pdf",
                3,
                5,
                1,
                0,
                1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            6,
            (
                6,
                "p_2_i",
                "pdf2image     (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "pdf_scanned_ok_3.pdf",
                3,
                5,
                1,
                1,
                1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            7,
            (
                7,
                "p_i",
                "inbox         (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test"),
                "inbox",
                "",
                "",
                0,
                "pdf_text_ok.pdf",
                4,
                7,
                1,
                0,
                3,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            8,
            (
                8,
                "tet",
                "pdflib        (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "pdf_text_ok_4.pdf",
                4,
                7,
                1,
                0,
                3,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            9,
            (
                9,
                "p_i",
                "inbox         (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test"),
                "inbox",
                "No 'pdf' format",
                "01.903 Issue (p_i): Runtime error with fitz.open() processing of "
                + "file 'pdf_wrong_format.pdf' - error: 'cannot open broken document'.",
                1,
                "pdf_wrong_format.pdf",
                5,
                9,
                1,
                0,
                -1,
                "error",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            10,
            (
                10,
                "p_i",
                "inbox         (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test"),
                "inbox",
                "",
                "",
                0,
                "translating_sql_into_relational_algebra_p01_02.pdf",
                6,
                10,
                1,
                0,
                2,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            11,
            (
                11,
                "p_2_i",
                "pdf2image     (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "translating_sql_into_relational_algebra_p01_02_6.pdf",
                6,
                10,
                1,
                2,
                2,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            12,
            (
                12,
                "ocr",
                "tesseract     (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "pdf_scanned_ok_3_[0-9]*.jpeg",
                3,
                6,
                2,
                1,
                1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            13,
            (
                13,
                "ocr",
                "tesseract     (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "translating_sql_into_relational_algebra_p01_02_6_[0-9]*.jpeg",
                6,
                11,
                2,
                2,
                2,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            14,
            (
                14,
                "tet",
                "pdflib        (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "jpeg_pdf_text_ok_2.pdf",
                2,
                4,
                3,
                0,
                1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            15,
            (
                15,
                "tet",
                "pdflib        (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "pdf_scanned_ok_3_0.pdf",
                3,
                12,
                3,
                0,
                1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            16,
            (
                16,
                "tet",
                "pdflib        (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "translating_sql_into_relational_algebra_p01_02_6_0.pdf",
                6,
                13,
                3,
                0,
                2,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            17,
            (
                17,
                "tet",
                "pdflib        (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "docx_ok_1.pdf",
                1,
                2,
                4,
                0,
                2,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            18,
            (
                18,
                "s_p_j_line",
                "parser_line   (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "pdf_text_ok_4.line.xml",
                4,
                8,
                5,
                0,
                3,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            19,
            (
                19,
                "s_p_j_line",
                "parser_line   (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "jpeg_pdf_text_ok_2.line.xml",
                2,
                14,
                5,
                0,
                1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            20,
            (
                20,
                "s_p_j_line",
                "parser_line   (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "pdf_scanned_ok_3_0.line.xml",
                3,
                15,
                5,
                0,
                1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            21,
            (
                21,
                "s_p_j_line",
                "parser_line   (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "translating_sql_into_relational_algebra_p01_02_6_0.line.xml",
                6,
                16,
                5,
                0,
                2,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            22,
            (
                22,
                "s_p_j_line",
                "parser_line   (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "docx_ok_1.line.xml",
                1,
                17,
                5,
                0,
                2,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            23,
            (
                23,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "pdf_text_ok_4.line.json",
                4,
                18,
                6,
                0,
                3,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            24,
            (
                24,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "jpeg_pdf_text_ok_2.line.json",
                2,
                19,
                6,
                0,
                1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            25,
            (
                25,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "pdf_scanned_ok_3_0.line.json",
                3,
                20,
                6,
                0,
                1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            26,
            (
                26,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "translating_sql_into_relational_algebra_p01_02_6_0.line.json",
                6,
                21,
                6,
                0,
                2,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_action(
        (
            27,
            (
                27,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test_accepted"),
                "inbox_accepted",
                "",
                "",
                0,
                "docx_ok_1.line.json",
                1,
                22,
                6,
                0,
                2,
                "end",
            ),
        )
    )


# -----------------------------------------------------------------------------
# Check the database content - database table document.
# -----------------------------------------------------------------------------
def check_db_content_document() -> None:
    """Check the database content - database table document."""
    pytest.helpers.check_dbt_document(
        (
            1,
            (
                1,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "docx_ok.docx",
                1,
                7,
                1,
                0,
                0,
                0,
                3,
                0,
                -1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_document(
        (
            2,
            (
                2,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "jpeg_pdf_text_ok.jpeg",
                1,
                7,
                0,
                1,
                0,
                0,
                0,
                0,
                -1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_document(
        (
            3,
            (
                3,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "pdf_scanned_ok.pdf",
                1,
                7,
                1,
                0,
                0,
                0,
                0,
                3,
                1,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_document(
        (
            4,
            (
                4,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "pdf_text_ok.pdf",
                1,
                7,
                0,
                0,
                0,
                0,
                2,
                0,
                3,
                "end",
            ),
        )
    )
    pytest.helpers.check_dbt_document(
        (
            5,
            (
                5,
                "p_i",
                "inbox         (preprocessor)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
                "No 'pdf' format",
                "01.903 Issue (p_i): Runtime error with fitz.open() processing of "
                + "file 'pdf_wrong_format.pdf' - error: 'cannot open broken document'.",
                1,
                "pdf_wrong_format.pdf",
                1,
                1,
                0,
                0,
                0,
                0,
                0,
                0,
                -1,
                "error",
            ),
        )
    )
    pytest.helpers.check_dbt_document(
        (
            6,
            (
                6,
                "tkn",
                "tokenizer     (nlp)",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test"),
                "",
                "",
                0,
                "translating_sql_into_relational_algebra_p01_02.pdf",
                1,
                7,
                0,
                1,
                0,
                2,
                2,
                0,
                2,
                "end",
            ),
        )
    )


# -----------------------------------------------------------------------------
# Check the database content - database table language.
# -----------------------------------------------------------------------------
def check_db_content_language() -> None:
    """Check the database content - database table language."""
    pytest.helpers.check_dbt_language(
        (
            1,
            (
                1,
                True,
                "eng",
                "en",
                "en_core_web_trf",
                "eng",
                dcr_core.core_utils.get_os_independent_name("data/inbox_test"),
                "English",
            ),
        )
    )
    pytest.helpers.check_dbt_language(
        (
            2,
            (
                2,
                True,
                "deu",
                "de",
                "de_dep_news_trf",
                "deu",
                dcr_core.core_utils.get_os_independent_name("data\\inbox_test\\deutsch"),
                "Deutsch",
            ),
        )
    )
    pytest.helpers.check_dbt_language((3, (3, False, "fra", "fr", "fr_dep_news_trf", "fra", "", "French")))
    pytest.helpers.check_dbt_language((4, (4, False, "ita", "it", "it_core_news_lg", "ita", "", "Italian")))


# -----------------------------------------------------------------------------
# Check the database content- database table run.
# -----------------------------------------------------------------------------
def check_db_content_run() -> None:  #
    """Check the database content- database table run."""
    pytest.helpers.check_dbt_run((1, (1, "p_i", "inbox         (preprocessor)", 1, "end", 1, 5, 6)))
    pytest.helpers.check_dbt_run((2, (2, "p_2_i", "pdf2image     (preprocessor)", 1, "end", 0, 2, 2)))
    pytest.helpers.check_dbt_run((3, (3, "ocr", "tesseract     (preprocessor)", 1, "end", 0, 4, 3)))
    pytest.helpers.check_dbt_run((4, (4, "n_2_p", "pandoc        (preprocessor)", 1, "end", 0, 1, 1)))
    pytest.helpers.check_dbt_run((5, (5, "tet", "pdflib        (nlp)", 1, "end", 0, 5, 5)))
    pytest.helpers.check_dbt_run((6, (6, "s_p_j", "parser        (nlp)", 1, "end", 0, 5, 5)))
    pytest.helpers.check_dbt_run((7, (7, "tkn", "tokenizer     (nlp)", 1, "end", 0, 5, 5)))


# -----------------------------------------------------------------------------
# Check the database content - database table version.
# -----------------------------------------------------------------------------
def check_db_content_version() -> None:
    """Check the database content - database table version."""
    pytest.helpers.check_dbt_version((1, (1, dcr_core.cls_setup.Setup.DCR_VERSION)))


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_ALL_COMPLETE - delete_auxiliary_files = true.
# -----------------------------------------------------------------------------
def test_run_action_process_all_complete_auxiliary_deleted(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_ALL_COMPLETE - delete_auxiliary_files = true."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
        ],
    )

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_ok", "docx"),
            ("jpeg_pdf_text_ok", "jpeg"),
            ("pdf_scanned_ok", "pdf"),
            ("pdf_text_ok", "pdf"),
            ("pdf_wrong_format", "pdf"),
            ("README", "md"),
            ("translating_sql_into_relational_algebra_p01_02", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.db.cls_run.Run.ID_RUN_UMBRELLA = 0

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_ALL_COMPLETE])

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.info("=========> test_run_action_process_all_complete_auxiliary_deleted <=========")

    check_db_content()

    pytest.helpers.verify_content_of_inboxes(
        inbox=(
            [],
            ["README.md"],
        ),
        inbox_accepted=(
            [],
            [
                "docx_ok_1.docx",
                "jpeg_pdf_text_ok_2.jpeg",
                "pdf_scanned_ok_3.pdf",
                "pdf_text_ok_4.pdf",
                "translating_sql_into_relational_algebra_p01_02_6.pdf",
            ],
        ),
        inbox_rejected=(
            [],
            ["pdf_wrong_format_5.pdf"],
        ),
    )


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_ALL_COMPLETE - empty.
# -----------------------------------------------------------------------------
def test_run_action_process_all_complete_auxiliary_empty(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_ALL_COMPLETE - empty."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("empty_docx", "docx"),
            ("empty_jpg", "jpg"),
            ("empty_pdf_scanned", "pdf"),
            ("empty_pdf_text", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_ALL_COMPLETE])

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_ALL_COMPLETE - delete_auxiliary_files = false.
# -----------------------------------------------------------------------------
def test_run_action_process_all_complete_auxiliary_kept(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_ALL_COMPLETE - delete_auxiliary_files = false."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        ],
    )

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_ok", "docx"),
            ("jpeg_pdf_text_ok", "jpeg"),
            ("pdf_scanned_ok", "pdf"),
            ("pdf_text_ok", "pdf"),
            ("translating_sql_into_relational_algebra_p01_02", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_ALL_COMPLETE])

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.info("=========> test_run_action_process_all_complete_auxiliary_kept <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_ok_1.docx",
                "docx_ok_1.line.json",
                "docx_ok_1.line.xml",
                "docx_ok_1.pdf",
                "jpeg_pdf_text_ok_2.jpeg",
                "jpeg_pdf_text_ok_2.line.json",
                "jpeg_pdf_text_ok_2.line.xml",
                "jpeg_pdf_text_ok_2.pdf",
                "pdf_scanned_ok_3.pdf",
                "pdf_scanned_ok_3_1.jpeg",
                "pdf_scanned_ok_3_0.line.json",
                "pdf_scanned_ok_3_0.line.xml",
                "pdf_scanned_ok_3_0.pdf",
                "pdf_text_ok_4.line.json",
                "pdf_text_ok_4.line.xml",
                "pdf_text_ok_4.pdf",
                "translating_sql_into_relational_algebra_p01_02_5.pdf",
                "translating_sql_into_relational_algebra_p01_02_5_0.line.json",
                "translating_sql_into_relational_algebra_p01_02_5_0.line.xml",
                "translating_sql_into_relational_algebra_p01_02_5_0.pdf",
                "translating_sql_into_relational_algebra_p01_02_5_1.jpeg",
                "translating_sql_into_relational_algebra_p01_02_5_2.jpeg",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test RUN_ACTION_PROCESS_ALL_COMPLETE - status: error.
# -----------------------------------------------------------------------------
def test_run_action_process_all_complete_auxiliary_status_error(fxtr_setup_empty_db_and_inbox):
    """Test RUN_ACTION_PROCESS_ALL_COMPLETE - status: error."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.config_params_modify(
        dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "after"),
        ],
    )
    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_ENV_TEST,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_PAGE, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TETML_WORD, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "false"),
        ],
    )

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("docx_ok", "docx"),
            ("jpeg_pdf_text_ok", "jpeg"),
            ("pdf_scanned_ok", "pdf"),
            ("pdf_text_ok", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.db.cls_run.Run.ID_RUN_UMBRELLA = 0

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_id(6)
    dcr.cfg.glob.action_curr.action_status = dcr.db.cls_document.Document.DOCUMENT_STATUS_ERROR
    dcr.cfg.glob.action_curr.persist_2_db()

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE])

    # -------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_id(4)
    dcr.cfg.glob.action_curr.action_status = dcr.db.cls_document.Document.DOCUMENT_STATUS_ERROR
    dcr.cfg.glob.action_curr.persist_2_db()

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TESSERACT])

    # -------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_id(2)
    dcr.cfg.glob.action_curr.action_status = dcr.db.cls_document.Document.DOCUMENT_STATUS_ERROR
    dcr.cfg.glob.action_curr.persist_2_db()

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PANDOC])

    # -------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_id(8)
    dcr.cfg.glob.action_curr.action_status = dcr.db.cls_document.Document.DOCUMENT_STATUS_ERROR
    dcr.cfg.glob.action_curr.persist_2_db()

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDFLIB])

    # -------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_id(13)
    dcr.cfg.glob.action_curr.action_status = dcr.db.cls_document.Document.DOCUMENT_STATUS_ERROR
    dcr.cfg.glob.action_curr.persist_2_db()

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PARSER])

    # -------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_id(17)
    dcr.cfg.glob.action_curr.action_status = dcr.db.cls_document.Document.DOCUMENT_STATUS_ERROR
    dcr.cfg.glob.action_curr.persist_2_db()

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE])

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.info("=========> test_run_action_process_all_complete_auxiliary_status_error <=========")

    pytest.helpers.verify_content_of_inboxes(
        inbox_accepted=(
            [],
            [
                "docx_ok_1.docx",
                "jpeg_pdf_text_ok_2.jpeg",
                "pdf_scanned_ok_3.pdf",
                "pdf_text_ok_4.pdf",
            ],
        ),
    )

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
