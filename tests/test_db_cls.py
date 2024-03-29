# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

# pylint: disable=unused-argument
"""Testing Module dcr.db.cls_..."""
import time

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
# @pytest.mark.issue
MISSING_ID = 4711


# -----------------------------------------------------------------------------
# Check existing action object.
# -----------------------------------------------------------------------------
def check_existing_action():
    """Check existing action object."""
    expected_values = (
        1,
        dcr.db.cls_run.Run.ACTION_CODE_INBOX,
        dcr.db.cls_run.Run.get_action_text(dcr.db.cls_run.Run.ACTION_CODE_INBOX),
        dcr_core.core_glob.setup.directory_inbox,
        "inbox",
        "",
        "",
        0,
        "pdf_text_ok.pdf",
        53651,
        1,
        1,
        1,
        0,
        3,
        dcr.db.cls_document.Document.DOCUMENT_STATUS_END,
    )

    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_id(expected_values[0])

    actual_values = dcr.cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != tuple(expected_values):
        print(f"issue with dbt action instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt action id={expected_values[0]} - see above"

    dcr.cfg.glob.action_curr.exists()

    # -----------------------------------------------------------------------------
    # Finalise the current action with error.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.action_curr.finalise_error("error_code", "error_msg")

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.action_curr.get_file_type()

    dcr.cfg.glob.action_curr.action_file_name = ""

    dcr.cfg.glob.action_curr.get_file_type()

    dcr.cfg.glob.action_curr.action_file_name = expected_values[8]

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.action_curr.get_stem_name()

    dcr.cfg.glob.action_curr.action_file_name = ""

    dcr.cfg.glob.action_curr.get_stem_name()

    dcr.cfg.glob.action_curr.action_file_name = expected_values[8]

    # -----------------------------------------------------------------------------
    # Select unprocessed actions based on action_code und document id.
    # -----------------------------------------------------------------------------
    with dcr.cfg.glob.db_core.db_orm_engine.begin() as conn:
        dcr.cfg.glob.action_curr.select_action_by_action_code_id_document(
            conn=conn, action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX, id_document=1
        )


# -----------------------------------------------------------------------------
# Check existing document object.
# -----------------------------------------------------------------------------
def check_existing_document():
    """Check existing document object."""
    expected_values = pytest.helpers.get_values_document()

    expected_values[0] = 1
    expected_values[1] = "tkn"
    expected_values[2] = "tokenizer     (nlp)"
    expected_values[10] = 7
    expected_values[11] = 0
    expected_values[12] = 0
    expected_values[13] = 0
    expected_values[14] = 0
    expected_values[15] = 2
    expected_values[16] = 0
    expected_values[17] = 3
    expected_values[18] = dcr.db.cls_document.Document.DOCUMENT_STATUS_END

    dcr.cfg.glob.document = dcr.db.cls_document.Document.from_id(expected_values[0])

    actual_values = dcr.cfg.glob.document.get_columns_in_tuple(is_sha256=False)

    if actual_values != tuple(expected_values):
        print(f"issue with dbt document dcr.cfg.glob.document id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt document id={expected_values[0]} - see above"

    dcr.cfg.glob.document.exists()

    dcr.cfg.glob.document.get_columns_in_tuple()

    # -----------------------------------------------------------------------------
    # Get the duplicate file name based on the hash key.
    # -----------------------------------------------------------------------------
    dcr.db.cls_document.Document.select_duplicate_file_name_by_sha256(MISSING_ID, expected_values[18])

    # -----------------------------------------------------------------------------
    # Finalise the current row with error.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.document.finalise_error("error_code", "error_msg")

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.document.document_file_name = ""

    dcr.cfg.glob.document.get_file_type()

    dcr.cfg.glob.document.document_file_name = expected_values[7]

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name - positive.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.document.get_stem_name()

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name - negative.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.document.document_file_name = ""

    dcr.cfg.glob.document.get_stem_name()

    dcr.cfg.glob.document.document_file_name = expected_values[7]

    # -----------------------------------------------------------------------------
    # Get the stem name from the first processed document.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.document.document_file_name = ""

    dcr.cfg.glob.document.get_stem_name_next()

    dcr.cfg.glob.document.document_file_name = expected_values[7]


# -----------------------------------------------------------------------------
# Check existing language object.
# -----------------------------------------------------------------------------
def check_existing_language():
    """Check existing language object."""
    expected_values = [
        1,
        True,
        "eng",
        "en",
        "en_core_web_trf",
        "eng",
        dcr_core.core_utils.get_os_independent_name("data/inbox_test"),
        "English",
    ]

    dcr.cfg.glob.language = dcr.db.cls_language.Language.from_id(expected_values[0])

    if (actual_values := dcr.cfg.glob.language.get_columns_in_tuple()) != tuple(expected_values):
        print(f"issue with dbt language dcr.cfg.glob.language id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt language id={expected_values[0]} - see above"

    dcr.cfg.glob.language.exists()


# -----------------------------------------------------------------------------
# Check existing run object.
# -----------------------------------------------------------------------------
def check_existing_run():
    """Check existing run object."""
    expected_values = pytest.helpers.get_values_run()

    expected_values[0] = 1
    expected_values[4] = dcr.db.cls_document.Document.DOCUMENT_STATUS_END
    expected_values[5] = 0
    expected_values[6] = 1
    expected_values[7] = 1

    dcr.cfg.glob.run = dcr.db.cls_run.Run.from_id(expected_values[0])

    if (actual_values := dcr.cfg.glob.run.get_columns_in_tuple()) != tuple(expected_values):
        print(f"issue with dbt run dcr.cfg.glob.run id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt run id={expected_values[0]} - see above"

    dcr.cfg.glob.run.exists()


# -----------------------------------------------------------------------------
# Check existing token object.
# -----------------------------------------------------------------------------
# pylint: disable=duplicate-code
def check_existing_token():
    """Check existing token object."""
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    expected_values = (
        1,
        1,
        0,
        0,
        71,
        152,
        "b",
        2,
        1,
        1,
        0,
        1,
        "Start Document ...",
        [
            {
                "tknCluster": 0,
                "tknDep_": "ROOT",
                "tknDoc": "Start Document ...",
                "tknEntIob_": "O",
                "tknHead": 0,
                "tknI": 0,
                "tknIdx": 0,
                "tknIsAlpha": True,
                "tknIsAscii": True,
                "tknIsOov": True,
                "tknIsSentStart": True,
                "tknIsTitle": True,
                "tknLang_": "en",
                "tknLeftEdge": 0,
                "tknLemma_": "start",
                "tknLex": "Start",
                "tknLexId": 18446744073709551615,
                "tknLower_": "start",
                "tknMorph": "VerbForm=Inf",
                "tknNorm_": "start",
                "tknOrth_": "Start",
                "tknPos_": "VERB",
                "tknPrefix_": "S",
                "tknProb": -20.0,
                "tknRightEdge": 2,
                "tknSent": "Start Document ...",
                "tknSentiment": 0.0,
                "tknShape_": "Xxxxx",
                "tknSuffix_": "art",
                "tknTag_": "VB",
                "tknText": "Start",
                "tknTextWithWs": "Start ",
                "tknWhitespace_": " ",
            },
            {
                "tknCluster": 0,
                "tknDep_": "dobj",
                "tknDoc": "Start Document ...",
                "tknEntIob_": "O",
                "tknHead": 0,
                "tknI": 1,
                "tknIdx": 6,
                "tknIsAlpha": True,
                "tknIsAscii": True,
                "tknIsOov": True,
                "tknIsTitle": True,
                "tknLang_": "en",
                "tknLeftEdge": 1,
                "tknLemma_": "document",
                "tknLex": "Document",
                "tknLexId": 18446744073709551615,
                "tknLower_": "document",
                "tknMorph": "Number=Sing",
                "tknNorm_": "document",
                "tknOrth_": "Document",
                "tknPos_": "NOUN",
                "tknPrefix_": "D",
                "tknProb": -20.0,
                "tknRightEdge": 1,
                "tknSent": "Start Document ...",
                "tknSentiment": 0.0,
                "tknShape_": "Xxxxx",
                "tknSuffix_": "ent",
                "tknTag_": "NN",
                "tknText": "Document",
                "tknTextWithWs": "Document ",
                "tknWhitespace_": " ",
            },
        ],
    )

    dcr.cfg.glob.token = dcr.db.cls_token.Token.from_id(expected_values[0])

    if (actual_values := dcr.cfg.glob.token.get_columns_in_tuple()) != tuple(expected_values):
        print(f"issue with dbt token dcr.cfg.glob.token id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt token id={expected_values[0]} - see above"

    dcr.cfg.glob.token.exists()


# -----------------------------------------------------------------------------
# Check existing version object.
# -----------------------------------------------------------------------------
def check_existing_version():
    """Check existing version object."""
    expected_values = [1, dcr_core.cls_setup.Setup.DCR_VERSION]

    dcr.cfg.glob.version = dcr.db.cls_version.Version.from_id(expected_values[0])

    if (actual_values := dcr.cfg.glob.version.get_columns_in_tuple()) != tuple(expected_values):
        print(f"issue with dbt version dcr.cfg.glob.version id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt version id={expected_values[0]} - see above"

    dcr.cfg.glob.version.exists()


# -----------------------------------------------------------------------------
# Check missing action object.
# -----------------------------------------------------------------------------
def check_missing_action():
    """Check missing action object."""
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_action.Action.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt action instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt action instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing document object.
# -----------------------------------------------------------------------------
def check_missing_document():
    """Check missing document object."""
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_document.Document.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt document instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt document instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing language object.
# -----------------------------------------------------------------------------
def check_missing_language():
    """Check missing language object."""
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_language.Language.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt language instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt language instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing run object.
# -----------------------------------------------------------------------------
def check_missing_run():
    """Check missing run object."""
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_run.Run.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt run instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt run instance id={MISSING_ID}"

    # -----------------------------------------------------------------------------
    # Invalid action code.
    # -----------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_run.Run(
            _row_id=0,
            action_code=dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE,
            total_erroneous=1,
        )

    assert expt.type == SystemExit, f"invalid action code={dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE}"
    assert expt.value.code == 1, f"invalid action code={dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE}"

    # -----------------------------------------------------------------------------
    # Untested action codes.
    # -----------------------------------------------------------------------------
    dcr.db.cls_run.Run(
        action_code=dcr.db.cls_run.Run.ACTION_CODE_PARSER_PAGE,
    )

    dcr.db.cls_run.Run(
        action_code=dcr.db.cls_run.Run.ACTION_CODE_PARSER_WORD,
    )

    dcr.db.cls_run.Run(
        action_code=dcr.db.cls_run.Run.ACTION_CODE_TOKENIZE_LINE,
    )


# -----------------------------------------------------------------------------
# Check missing token object.
# -----------------------------------------------------------------------------
def check_missing_token():
    """Check missing token object."""
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_token.Token.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt token instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt token instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing version object.
# -----------------------------------------------------------------------------
def check_missing_version():
    """Check missing version object."""
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_version.Version.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt version instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt version instance id={MISSING_ID}"

    # -----------------------------------------------------------------------------
    # Column version in database table version not found.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.db_core.delete_dbt_id(
        table_name=dcr.db.cls_db_core.DBCore.DBT_VERSION,
        id_where=1,
    )

    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_version.Version.select_version_version_unique()

    assert expt.type == SystemExit, "issue column version in database table version not found"
    assert expt.value.code == 1, "issue column version in database table version not found"

    # -----------------------------------------------------------------------------
    # Column version in database table version not unique.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.version = dcr.db.cls_version.Version(
        version="1",
    )

    dcr.cfg.glob.version.persist_2_db()

    dcr.cfg.glob.version = dcr.db.cls_version.Version(
        version="2",
    )

    dcr.cfg.glob.version.persist_2_db()

    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_version.Version.select_version_version_unique()

    assert expt.type == SystemExit, "issue column version in database table version not unique"
    assert expt.value.code == 1, "issue column version in database table version not unique"


# -----------------------------------------------------------------------------
# Check new action object.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def check_new_action():
    """Check new action object."""

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_action()

    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_id(expected_values[0])

    actual_values = dcr.cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != tuple(expected_values):
        print("issue with new dbt action instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt action instance - see above"

    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action(
        action_code=expected_values[1],
        action_text=expected_values[2],
        directory_name=expected_values[3],
        directory_type=expected_values[4],
        file_name=expected_values[8],
        file_size_bytes=0,
        id_document=expected_values[10],
        id_parent=expected_values[11],
        id_run_last=expected_values[12],
        no_children=expected_values[13],
        no_pdf_pages=0,
        status=expected_values[15],
    )

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    dcr.cfg.glob.action_curr = dcr.db.cls_action.Action.from_id(expected_values[0])

    expected_values[15] = dcr.db.cls_document.Document.DOCUMENT_STATUS_END

    dcr.cfg.glob.action_curr.action_status = expected_values[15]

    dcr.cfg.glob.action_curr.persist_2_db()

    actual_values = dcr.cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != tuple(expected_values):
        print("issue with updated dbt action instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt action instance - see above"

    # -----------------------------------------------------------------------------
    # coverage.
    # -----------------------------------------------------------------------------
    expected_values[0] = 5
    expected_values[1] = "s_p_j_line"
    expected_values[2] = "parser_line   (nlp)"

    instance = dcr.db.cls_action.Action(
        _row_id=0,
        action_code=expected_values[1],
        action_text=expected_values[2],
        directory_name=expected_values[3],
        directory_type=expected_values[4],
        file_name=expected_values[8],
        file_size_bytes=expected_values[9],
        id_document=expected_values[10],
        id_parent=expected_values[11],
        id_run_last=expected_values[12],
        no_children=expected_values[13],
        no_pdf_pages=expected_values[14],
        status=expected_values[15],
    )

    instance.action_file_size_bytes = 0
    instance.action_no_pdf_pages = 0

    instance.finalise()

    instance.finalise_error("error_code", "error_msg")


# -----------------------------------------------------------------------------
# Check new document object.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def check_new_document():
    """Check new document object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_document()

    dcr.cfg.glob.document = dcr.db.cls_document.Document.from_id(expected_values[0])

    actual_values = dcr.cfg.glob.document.get_columns_in_tuple(is_sha256=False)

    if actual_values != tuple(expected_values):
        print("issue with new dbt document dcr.cfg.glob.document:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt document dcr.cfg.glob.document - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[18] = dcr.db.cls_document.Document.DOCUMENT_STATUS_END

    dcr.cfg.glob.document.document_status = expected_values[18]

    dcr.cfg.glob.document.finalise()

    actual_values = dcr.cfg.glob.document.get_columns_in_tuple(is_sha256=False)

    if actual_values != tuple(expected_values):
        print("issue with updated dbt document dcr.cfg.glob.document:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt document dcr.cfg.glob.document - see above"


# -----------------------------------------------------------------------------
# Check new language object.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def check_new_language():
    """Check new language object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_language()

    dcr.cfg.glob.language = dcr.db.cls_language.Language.from_id(expected_values[0])

    if (actual_values := dcr.cfg.glob.language.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with new dbt language instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt language instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[6] = ""

    dcr.cfg.glob.language.language_directory_name_inbox = expected_values[6]

    dcr.cfg.glob.language.persist_2_db()

    if (actual_values := dcr.cfg.glob.language.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with updated dbt language instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt language instance - see above"


# -----------------------------------------------------------------------------
# Check new run object.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def check_new_run():
    """Check new run object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_run()

    dcr.cfg.glob.run = dcr.db.cls_run.Run.from_id(expected_values[0])

    if (actual_values := dcr.cfg.glob.run.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with new dbt run instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt run instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[4] = dcr.db.cls_document.Document.DOCUMENT_STATUS_END

    dcr.cfg.glob.run.run_status = expected_values[4]

    dcr.cfg.glob.run.persist_2_db()

    if (actual_values := dcr.cfg.glob.run.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with updated dbt run instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt run instance - see above"

    # -----------------------------------------------------------------------------
    # Delete object.
    # -----------------------------------------------------------------------------
    dcr.db.cls_run.Run.ID_RUN_UMBRELLA = 0

    dcr.db.cls_run.Run(
        _row_id=0,
        action_code=expected_values[1],
        status=expected_values[4],
        total_erroneous=0,
    )

    dcr.cfg.glob.run.persist_2_db()


# -----------------------------------------------------------------------------
# Check new token object.
# -----------------------------------------------------------------------------
def check_new_token():
    """Check new token object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_token()

    dcr.cfg.glob.token = dcr.db.cls_token.Token.from_id(expected_values[0])

    if (actual_values := dcr.cfg.glob.token.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with new dbt token instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt token instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[3] = 2

    dcr.cfg.glob.token.token_page_no = expected_values[3]

    dcr.cfg.glob.token.persist_2_db()

    if (actual_values := dcr.cfg.glob.token.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with updated dbt token instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt token instance - see above"

    dcr.cfg.glob.token.finalise()


# -----------------------------------------------------------------------------
# Check new version object.
# -----------------------------------------------------------------------------
def check_new_version():
    """Check new version object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_version()

    dcr.cfg.glob.version = dcr.db.cls_version.Version.from_id(expected_values[0])

    if (actual_values := dcr.cfg.glob.version.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with new dbt version instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt version instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[1] = ""

    dcr.cfg.glob.version.version_version = expected_values[1]

    dcr.cfg.glob.version.finalise()

    if (actual_values := dcr.cfg.glob.version.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with updated dbt version instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt version instance - see above"


# -----------------------------------------------------------------------------
# Test Function - existing objects.
# -----------------------------------------------------------------------------
def test_existing_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - existing objects."""
    try:
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)
    except AttributeError:
        dcr_core.core_glob.initialise_logger()
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=dcr_core.core_glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.db.cls_run.Run.ID_RUN_UMBRELLA = 0

    pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_CORE_SPACY,
        [
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_BRACKET, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_LEFT_PUNCT, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_PUNCT, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_QUOTE, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_SPACE, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_BRACKET, "true"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_RANK, "false"),
            (dcr_core.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_VOCAB, "false"),
        ],
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_ALL_COMPLETE])

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    check_existing_language()
    check_existing_run()
    check_existing_version()

    check_existing_document()

    check_existing_action()

    check_existing_token()

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - action - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_action_0(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - action - case0."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_action.Action(
            action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
            directory_name="",
            file_name="",
            id_document=0,
            id_run_last=0,
        )

    assert expt.type == SystemExit, "Instance of class 'DBCore' is missing"
    assert expt.value.code == 1, "Instance of class 'DBCore' is missing"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - action - case 1.
# -----------------------------------------------------------------------------
def test_missing_dependencies_action_1(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - action - case 1."""
    pytest.helpers.delete_existing_object(is_run=True)

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    directory_name = dcr_core.core_glob.setup.directory_inbox
    file_name = "pdf_text_ok.pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    values_run = pytest.helpers.create_run()

    values_document = pytest.helpers.create_document()

    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_action.Action(
            action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
            directory_name=directory_name,
            file_name=file_name,
            id_document=values_document[0],
            id_run_last=values_run[0],
        )

    assert expt.type == SystemExit, "Class Action requires class Run"
    assert expt.value.code == 1, "Class Action requires class Run"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - action - case 2.
# -----------------------------------------------------------------------------
def test_missing_dependencies_action_2(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - action - case 2."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_action_curr=True, is_document=True, is_run=True)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.start_time_document = time.perf_counter_ns()

    directory_name = dcr_core.core_glob.setup.directory_inbox
    file_name = "pdf_text_ok.pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    values_run = pytest.helpers.create_run()

    dcr.cfg.glob.run = dcr.db.cls_run.Run.from_id(values_run[0])

    # -----------------------------------------------------------------------------
    dcr.cfg.glob.language = dcr.db.cls_language.Language.from_id(1)

    dcr.cfg.glob.language.persist_2_db()

    # -------------------------------------------------------------------------
    # _expected_values_document = pytest.helpers.create_document()
    values_document = pytest.helpers.create_document()

    # -------------------------------------------------------------------------
    local_action = dcr.db.cls_action.Action(
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
    with pytest.raises(SystemExit) as expt:
        local_action.finalise_error("error_code", "error_msg")

    assert expt.type == SystemExit, "Class Action requires class Document (finalise_error)"
    assert expt.value.code == 1, "Class Action requires class Document (finalise_error)"

    # -------------------------------------------------------------------------
    dcr.cfg.glob.document = dcr.db.cls_document.Document.from_id(1)

    local_action.action_action_code = dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE

    with pytest.raises(SystemExit) as expt:
        local_action.finalise_error("error_code", "error_msg")

    assert expt.type == SystemExit, "Class Action requires class Action (finalise_error)"
    assert expt.value.code == 1, "Class Action requires class Action (finalise_error)"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - db_core - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_db_core_0(fxtr_setup_empty_db_and_inbox):
    """# Test Function - missing dependencies - db_core - case 0.
    ."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_setup=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_db_core.DBCore()

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - document - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_document_0(fxtr_setup_logger):
    """# Test Function - missing dependencies - document - case 0.
    ."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_document.Document(
            action_code_last=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
            directory_name="",
            file_name="",
            id_language=0,
            id_run_last=0,
        )

    assert expt.type == SystemExit, "Instance of class 'DBCore' is missing"
    assert expt.value.code == 1, "Instance of class 'DBCore' is missing"


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - language - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_language_0(fxtr_setup_logger):
    """# Test Function - missing dependencies - language - case 0.
    ."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_language.Language(
            active=True,
            code_iso_639_3="",
            code_pandoc="",
            code_spacy="",
            code_tesseract="",
            iso_language_name="",
        )

    assert expt.type == SystemExit, "Instance of class 'DBCore' is missing"
    assert expt.value.code == 1, "Instance of class 'DBCore' is missing"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - language - case 1.
# -----------------------------------------------------------------------------
def test_missing_dependencies_language_1(fxtr_setup_empty_db_and_inbox):
    """# Test Function - missing dependencies - language - case 1.
    ."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_setup=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_language.Language(
            active=True,
            code_iso_639_3="",
            code_pandoc="",
            code_spacy="",
            code_tesseract="",
            iso_language_name="",
        )

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - run - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_run_0(fxtr_setup_logger):
    """# Test Function - missing dependencies - run - case 0.
    ."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_run.Run(
            action_code=dcr.db.cls_run.Run.ACTION_CODE_INBOX,
        )

    assert expt.type == SystemExit, "Instance of class 'DBCore' is missing"
    assert expt.value.code == 1, "Instance of class 'DBCore' is missing"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - token - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_token_0(fxtr_setup_logger):
    """# Test Function - missing dependencies - token - case 0.
    ."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_token.Token(
            id_document=0,
            column_no=0,
            column_span=0,
            line_type="",
            coord_llx=0,
            coord_urx=0,
            no_tokens_in_sent=0,
            page_no=0,
            para_no=0,
            row_no=0,
            sent_no=0,
            text="",
            tokens="",
        )

    assert expt.type == SystemExit, "Instance of class 'DBCore' is missing"
    assert expt.value.code == 1, "Instance of class 'DBCore' is missing"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - version - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_version_0(fxtr_setup_logger):
    """# Test Function - missing dependencies - version - case 0.
    ."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_version.Version()

    assert expt.type == SystemExit, "Instance of class 'DBCore' is missing"
    assert expt.value.code == 1, "Instance of class 'DBCore' is missing"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing objects.
# -----------------------------------------------------------------------------
def test_missing_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing objects."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    check_missing_language()
    check_missing_run()
    check_missing_version()

    check_missing_document()

    check_missing_action()

    check_missing_token()

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - new objects.
# -----------------------------------------------------------------------------
def test_new_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - new objects.

    Based on document 'pdf_test_ok.pdf'.
    """
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.start_time_document = time.perf_counter_ns()

    dcr.db.cls_run.Run.ID_RUN_UMBRELLA = 0

    check_new_language()
    check_new_run()
    check_new_version()

    check_new_document()

    check_new_action()

    dcr.cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=True, is_file_size_bytes=True)
    dcr.cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False, is_file_size_bytes=False)

    check_new_token()

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique_driver(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    dcr.cfg.glob.db_core.insert_dbt_row(dcr.db.cls_db_core.DBCore.DBT_VERSION, {dcr.db.cls_db_core.DBCore.DBC_VERSION: "0.0.0"})

    dcr.cfg.glob.db_core.disconnect_db()

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_version.Version.select_version_version_unique()

    dcr.cfg.glob.db_core.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (driver)"
    assert expt.value.code == 1, "Version not unique (driver)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_version.Version.select_version_version_unique()

    dcr.cfg.glob.db_core.disconnect_db()

    assert expt.type == SystemExit, "Version missing (driver)"
    assert expt.value.code == 1, "Version missing (driver)"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique_orm(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

    # -------------------------------------------------------------------------
    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    dcr.cfg.glob.db_core.insert_dbt_row(dcr.db.cls_db_core.DBCore.DBT_VERSION, {dcr.db.cls_db_core.DBCore.DBC_VERSION: "0.0.0"})

    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_version.Version.select_version_version_unique()

    dcr.cfg.glob.db_core.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (orm)"
    assert expt.value.code == 1, "Version not unique (orm)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    dcr.cfg.glob.db_core = dcr.db.cls_db_core.DBCore()

    with pytest.raises(SystemExit) as expt:
        dcr.db.cls_version.Version.select_version_version_unique()

    dcr.cfg.glob.db_core.disconnect_db()

    assert expt.type == SystemExit, "Version missing (orm)"
    assert expt.value.code == 1, "Version missing (orm)"

    # -------------------------------------------------------------------------
    dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_END)
