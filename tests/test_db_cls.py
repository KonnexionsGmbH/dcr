# pylint: disable=unused-argument
"""Testing Module db.cls_..."""
import time

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_db_core
import db.cls_document
import db.cls_language
import db.cls_run
import db.cls_token
import db.cls_version
import pytest

import dcr
import dcr_core.cfg.cls_setup
import dcr_core.cfg.glob
import dcr_core.utils

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
        db.cls_run.Run.ACTION_CODE_INBOX,
        db.cls_run.Run.get_action_text(db.cls_run.Run.ACTION_CODE_INBOX),
        dcr_core.cfg.glob.setup.directory_inbox,
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
        db.cls_document.Document.DOCUMENT_STATUS_END,
    )

    cfg.glob.action_curr = db.cls_action.Action.from_id(expected_values[0])

    actual_values = cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != tuple(expected_values):
        print(f"issue with dbt action instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt action id={expected_values[0]} - see above"

    cfg.glob.action_curr.exists()

    # -----------------------------------------------------------------------------
    # Finalise the current action with error.
    # -----------------------------------------------------------------------------
    cfg.glob.action_curr.finalise_error("error_code", "error_msg")

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    cfg.glob.action_curr.get_file_type()

    cfg.glob.action_curr.action_file_name = ""

    cfg.glob.action_curr.get_file_type()

    cfg.glob.action_curr.action_file_name = expected_values[8]

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name.
    # -----------------------------------------------------------------------------
    cfg.glob.action_curr.get_stem_name()

    cfg.glob.action_curr.action_file_name = ""

    cfg.glob.action_curr.get_stem_name()

    cfg.glob.action_curr.action_file_name = expected_values[8]

    # -----------------------------------------------------------------------------
    # Select unprocessed actions based on action_code und document id.
    # -----------------------------------------------------------------------------
    with cfg.glob.db_core.db_orm_engine.begin() as conn:
        cfg.glob.action_curr.select_action_by_action_code_id_document(conn=conn, action_code=db.cls_run.Run.ACTION_CODE_INBOX, id_document=1)


# -----------------------------------------------------------------------------
# Check existing document object.
# -----------------------------------------------------------------------------
def check_existing_document():
    """Check existing document object."""
    expected_values = pytest.helpers.get_values_document()

    expected_values[0] = 1
    expected_values[1] = "tkn"
    expected_values[2] = "tokenize      (nlp)"
    expected_values[10] = 8
    expected_values[11] = 0
    expected_values[12] = 0
    expected_values[13] = 0
    expected_values[14] = 0
    expected_values[15] = 2
    expected_values[16] = 0
    expected_values[17] = 3
    expected_values[18] = db.cls_document.Document.DOCUMENT_STATUS_END

    cfg.glob.document = db.cls_document.Document.from_id(expected_values[0])

    actual_values = cfg.glob.document.get_columns_in_tuple(is_sha256=False)

    if actual_values != tuple(expected_values):
        print(f"issue with dbt document cfg.glob.document id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt document id={expected_values[0]} - see above"

    cfg.glob.document.exists()

    cfg.glob.document.get_columns_in_tuple()

    # -----------------------------------------------------------------------------
    # Get the duplicate file name based on the hash key.
    # -----------------------------------------------------------------------------
    db.cls_document.Document.select_duplicate_file_name_by_sha256(MISSING_ID, expected_values[18])

    # -----------------------------------------------------------------------------
    # Finalise the current row with error.
    # -----------------------------------------------------------------------------
    cfg.glob.document.finalise_error("error_code", "error_msg")

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    cfg.glob.document.document_file_name = ""

    cfg.glob.document.get_file_type()

    cfg.glob.document.document_file_name = expected_values[7]

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name - positive.
    # -----------------------------------------------------------------------------
    cfg.glob.document.get_stem_name()

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name - negative.
    # -----------------------------------------------------------------------------
    cfg.glob.document.document_file_name = ""

    cfg.glob.document.get_stem_name()

    cfg.glob.document.document_file_name = expected_values[7]

    # -----------------------------------------------------------------------------
    # Get the stem name from the first processed document.
    # -----------------------------------------------------------------------------
    cfg.glob.document.document_file_name = ""

    cfg.glob.document.get_stem_name_next()

    cfg.glob.document.document_file_name = expected_values[7]


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
        dcr_core.utils.get_os_independent_name("data/inbox_test"),
        "English",
    ]

    cfg.glob.language = db.cls_language.Language.from_id(expected_values[0])

    if (actual_values := cfg.glob.language.get_columns_in_tuple()) != tuple(expected_values):
        print(f"issue with dbt language cfg.glob.language id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt language id={expected_values[0]} - see above"

    cfg.glob.language.exists()


# -----------------------------------------------------------------------------
# Check existing run object.
# -----------------------------------------------------------------------------
def check_existing_run():
    """Check existing run object."""
    expected_values = pytest.helpers.get_values_run()

    expected_values[0] = 1
    expected_values[4] = db.cls_document.Document.DOCUMENT_STATUS_END
    expected_values[5] = 0
    expected_values[6] = 1
    expected_values[7] = 1

    cfg.glob.run = db.cls_run.Run.from_id(expected_values[0])

    if (actual_values := cfg.glob.run.get_columns_in_tuple()) != tuple(expected_values):
        print(f"issue with dbt run cfg.glob.run id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt run id={expected_values[0]} - see above"

    cfg.glob.run.exists()


# -----------------------------------------------------------------------------
# Check existing token object.
# -----------------------------------------------------------------------------
# pylint: disable=duplicate-code
def check_existing_token():
    """Check existing token object."""
    cfg.glob.db_core = db.cls_db_core.DBCore()

    expected_values = [
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
                "tknI": 0,
                "tknIsOov": True,
                "tknIsTitle": True,
                "tknLemma_": "start",
                "tknNorm_": "start",
                "tknPos_": "VERB",
                "tknTag_": "VB",
                "tknText": "Start",
                "tknWhitespace_": " ",
            },
            {
                "tknI": 1,
                "tknIsOov": True,
                "tknIsTitle": True,
                "tknLemma_": "document",
                "tknNorm_": "document",
                "tknPos_": "NOUN",
                "tknTag_": "NN",
                "tknText": "Document",
                "tknWhitespace_": " ",
            },
        ],
    ]

    cfg.glob.token = db.cls_token.Token.from_id(expected_values[0])

    if (actual_values := cfg.glob.token.get_columns_in_tuple()) != tuple(expected_values):
        print(f"issue with dbt token cfg.glob.token id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt token id={expected_values[0]} - see above"

    cfg.glob.token.exists()


# -----------------------------------------------------------------------------
# Check existing version object.
# -----------------------------------------------------------------------------
def check_existing_version():
    """Check existing version object."""
    expected_values = [1, dcr_core.cfg.cls_setup.Setup.DCR_VERSION]

    cfg.glob.version = db.cls_version.Version.from_id(expected_values[0])

    if (actual_values := cfg.glob.version.get_columns_in_tuple()) != tuple(expected_values):
        print(f"issue with dbt version cfg.glob.version id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt version id={expected_values[0]} - see above"

    cfg.glob.version.exists()


# -----------------------------------------------------------------------------
# Check missing action object.
# -----------------------------------------------------------------------------
def check_missing_action():
    """Check missing action object."""
    with pytest.raises(SystemExit) as expt:
        db.cls_action.Action.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt action instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt action instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing document object.
# -----------------------------------------------------------------------------
def check_missing_document():
    """Check missing document object."""
    with pytest.raises(SystemExit) as expt:
        db.cls_document.Document.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt document instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt document instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing language object.
# -----------------------------------------------------------------------------
def check_missing_language():
    """Check missing language object."""
    with pytest.raises(SystemExit) as expt:
        db.cls_language.Language.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt language instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt language instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing run object.
# -----------------------------------------------------------------------------
def check_missing_run():
    """Check missing run object."""
    with pytest.raises(SystemExit) as expt:
        db.cls_run.Run.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt run instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt run instance id={MISSING_ID}"

    # -----------------------------------------------------------------------------
    # Invalid action code.
    # -----------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_run.Run(
            _row_id=0,
            action_code=dcr_core.cfg.glob.INFORMATION_NOT_YET_AVAILABLE,
            total_erroneous=1,
        )

    assert expt.type == SystemExit, f"invalid action code={dcr_core.cfg.glob.INFORMATION_NOT_YET_AVAILABLE}"
    assert expt.value.code == 1, f"invalid action code={dcr_core.cfg.glob.INFORMATION_NOT_YET_AVAILABLE}"

    # -----------------------------------------------------------------------------
    # Untested action codes.
    # -----------------------------------------------------------------------------
    db.cls_run.Run(
        action_code=db.cls_run.Run.ACTION_CODE_PARSER_PAGE,
    )

    db.cls_run.Run(
        action_code=db.cls_run.Run.ACTION_CODE_PARSER_WORD,
    )

    db.cls_run.Run(
        action_code=db.cls_run.Run.ACTION_CODE_TOKENIZE_LINE,
    )


# -----------------------------------------------------------------------------
# Check missing token object.
# -----------------------------------------------------------------------------
def check_missing_token():
    """Check missing token object."""
    with pytest.raises(SystemExit) as expt:
        db.cls_token.Token.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt token instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt token instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing version object.
# -----------------------------------------------------------------------------
def check_missing_version():
    """Check missing version object."""
    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt version instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt version instance id={MISSING_ID}"

    # -----------------------------------------------------------------------------
    # Column version in database table version not found.
    # -----------------------------------------------------------------------------
    cfg.glob.db_core.delete_dbt_id(
        table_name=db.cls_db_core.DBCore.DBT_VERSION,
        id_where=1,
    )

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    assert expt.type == SystemExit, "issue column version in database table version not found"
    assert expt.value.code == 1, "issue column version in database table version not found"

    # -----------------------------------------------------------------------------
    # Column version in database table version not unique.
    # -----------------------------------------------------------------------------
    cfg.glob.version = db.cls_version.Version(
        version="1",
    )

    cfg.glob.version.persist_2_db()

    cfg.glob.version = db.cls_version.Version(
        version="2",
    )

    cfg.glob.version.persist_2_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

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
        target_path=dcr_core.cfg.glob.setup.directory_inbox,
    )

    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_action()

    cfg.glob.action_curr = db.cls_action.Action.from_id(expected_values[0])

    actual_values = cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != tuple(expected_values):
        print("issue with new dbt action instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt action instance - see above"

    cfg.glob.action_curr = db.cls_action.Action(
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
    cfg.glob.action_curr = db.cls_action.Action.from_id(expected_values[0])

    expected_values[15] = db.cls_document.Document.DOCUMENT_STATUS_END

    cfg.glob.action_curr.action_status = expected_values[15]

    cfg.glob.action_curr.persist_2_db()

    actual_values = cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False)

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

    instance = db.cls_action.Action(
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

    cfg.glob.document = db.cls_document.Document.from_id(expected_values[0])

    actual_values = cfg.glob.document.get_columns_in_tuple(is_sha256=False)

    if actual_values != tuple(expected_values):
        print("issue with new dbt document cfg.glob.document:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt document cfg.glob.document - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[18] = db.cls_document.Document.DOCUMENT_STATUS_END

    cfg.glob.document.document_status = expected_values[18]

    cfg.glob.document.finalise()

    actual_values = cfg.glob.document.get_columns_in_tuple(is_sha256=False)

    if actual_values != tuple(expected_values):
        print("issue with updated dbt document cfg.glob.document:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt document cfg.glob.document - see above"


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

    cfg.glob.language = db.cls_language.Language.from_id(expected_values[0])

    if (actual_values := cfg.glob.language.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with new dbt language instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt language instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[6] = ""

    cfg.glob.language.language_directory_name_inbox = expected_values[6]

    cfg.glob.language.persist_2_db()

    if (actual_values := cfg.glob.language.get_columns_in_tuple()) != tuple(expected_values):
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

    cfg.glob.run = db.cls_run.Run.from_id(expected_values[0])

    if (actual_values := cfg.glob.run.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with new dbt run instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt run instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[4] = db.cls_document.Document.DOCUMENT_STATUS_END

    cfg.glob.run.run_status = expected_values[4]

    cfg.glob.run.persist_2_db()

    if (actual_values := cfg.glob.run.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with updated dbt run instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt run instance - see above"

    # -----------------------------------------------------------------------------
    # Delete object.
    # -----------------------------------------------------------------------------
    db.cls_run.Run.ID_RUN_UMBRELLA = 0

    db.cls_run.Run(
        _row_id=0,
        action_code=expected_values[1],
        status=expected_values[4],
        total_erroneous=0,
    )

    cfg.glob.run.persist_2_db()


# -----------------------------------------------------------------------------
# Check new token object.
# -----------------------------------------------------------------------------
def check_new_token():
    """Check new token object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_token()

    cfg.glob.token = db.cls_token.Token.from_id(expected_values[0])

    if (actual_values := cfg.glob.token.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with new dbt token instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt token instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[3] = 2

    cfg.glob.token.token_page_no = expected_values[3]

    cfg.glob.token.persist_2_db()

    if (actual_values := cfg.glob.token.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with updated dbt token instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt token instance - see above"

    cfg.glob.token.finalise()


# -----------------------------------------------------------------------------
# Check new version object.
# -----------------------------------------------------------------------------
def check_new_version():
    """Check new version object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_version()

    cfg.glob.version = db.cls_version.Version.from_id(expected_values[0])

    if (actual_values := cfg.glob.version.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with new dbt version instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt version instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[1] = ""

    cfg.glob.version.version_version = expected_values[1]

    cfg.glob.version.finalise()

    if (actual_values := cfg.glob.version.get_columns_in_tuple()) != tuple(expected_values):
        print("issue with updated dbt version instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt version instance - see above"


# -----------------------------------------------------------------------------
# Test Function - existing objects.
# -----------------------------------------------------------------------------
def test_existing_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - existing objects."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=dcr_core.cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    db.cls_run.Run.ID_RUN_UMBRELLA = 0

    pytest.helpers.config_params_modify(
        dcr_core.cfg.cls_setup.Setup._DCR_CFG_SECTION_SPACY,
        [
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_BRACKET, "true"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_LEFT_PUNCT, "true"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_PUNCT, "true"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_QUOTE, "true"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT, "true"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_SPACE, "true"),
            (dcr_core.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_BRACKET, "true"),
        ],
    )

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_ALL_COMPLETE])

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    check_existing_language()
    check_existing_run()
    check_existing_version()

    check_existing_document()

    check_existing_action()

    check_existing_token()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - action - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_action_0(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - action - case0."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_action.Action(
            action_code=db.cls_run.Run.ACTION_CODE_INBOX,
            directory_name="",
            file_name="",
            id_document=0,
            id_run_last=0,
        )

    assert expt.type == SystemExit, "Instance of class 'DBCore' is missing"
    assert expt.value.code == 1, "Instance of class 'DBCore' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - action - case 1.
# -----------------------------------------------------------------------------
def test_missing_dependencies_action_1(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - action - case 1."""
    pytest.helpers.delete_existing_object(is_run=True)

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    directory_name = dcr_core.cfg.glob.setup.directory_inbox
    file_name = "pdf_text_ok.pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
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
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_action_curr=True, is_document=True, is_run=True)

    # -------------------------------------------------------------------------
    cfg.glob.start_time_document = time.perf_counter_ns()

    directory_name = dcr_core.cfg.glob.setup.directory_inbox
    file_name = "pdf_text_ok.pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
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
    with pytest.raises(SystemExit) as expt:
        local_action.finalise_error("error_code", "error_msg")

    assert expt.type == SystemExit, "Class Action requires class Document (finalise_error)"
    assert expt.value.code == 1, "Class Action requires class Document (finalise_error)"

    # -------------------------------------------------------------------------
    cfg.glob.document = db.cls_document.Document.from_id(1)

    local_action.action_action_code = db.cls_run.Run.ACTION_CODE_PDF2IMAGE

    with pytest.raises(SystemExit) as expt:
        local_action.finalise_error("error_code", "error_msg")

    assert expt.type == SystemExit, "Class Action requires class Action (finalise_error)"
    assert expt.value.code == 1, "Class Action requires class Action (finalise_error)"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - db_core - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_db_core_0(fxtr_setup_empty_db_and_inbox):
    """# Test Function - missing dependencies - db_core - case 0.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_setup=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_db_core.DBCore()

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - document - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_document_0(fxtr_setup_logger):
    """# Test Function - missing dependencies - document - case 0.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_document.Document(
            action_code_last=db.cls_run.Run.ACTION_CODE_INBOX,
            directory_name="",
            file_name="",
            id_language=0,
            id_run_last=0,
        )

    assert expt.type == SystemExit, "Instance of class 'DBCore' is missing"
    assert expt.value.code == 1, "Instance of class 'DBCore' is missing"


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - document - case 1.
# -----------------------------------------------------------------------------
def test_missing_dependencies_document_1(fxtr_setup_empty_db_and_inbox):
    """# Test Function - missing dependencies - document - case 1."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    cfg.glob.db_document = db.cls_document.Document(
        action_code_last="", directory_name="", file_name="dummy", id_language=0, id_run_last=0, _row_id=4711
    )

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_setup=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        cfg.glob.db_document.get_stem_name_next()

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - language - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_language_0(fxtr_setup_logger):
    """# Test Function - missing dependencies - language - case 0.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_language.Language(
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
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - language - case 1.
# -----------------------------------------------------------------------------
def test_missing_dependencies_language_1(fxtr_setup_empty_db_and_inbox):
    """# Test Function - missing dependencies - language - case 1.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_setup=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_language.Language(
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
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - run - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_run_0(fxtr_setup_logger):
    """# Test Function - missing dependencies - run - case 0.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_run.Run(
            action_code=db.cls_run.Run.ACTION_CODE_INBOX,
        )

    assert expt.type == SystemExit, "Instance of class 'DBCore' is missing"
    assert expt.value.code == 1, "Instance of class 'DBCore' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - token - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_token_0(fxtr_setup_logger):
    """# Test Function - missing dependencies - token - case 0.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_token.Token(
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
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - version - case 0.
# -----------------------------------------------------------------------------
def test_missing_dependencies_version_0(fxtr_setup_logger):
    """# Test Function - missing dependencies - version - case 0.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.delete_existing_object(is_db_core=True)

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version()

    assert expt.type == SystemExit, "Instance of class 'DBCore' is missing"
    assert expt.value.code == 1, "Instance of class 'DBCore' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing objects.
# -----------------------------------------------------------------------------
def test_missing_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing objects."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    check_missing_language()
    check_missing_run()
    check_missing_version()

    check_missing_document()

    check_missing_action()

    check_missing_token()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - new objects.
# -----------------------------------------------------------------------------
def test_new_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - new objects.

    Based on document 'pdf_test_ok.pdf'.
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    # -------------------------------------------------------------------------
    cfg.glob.start_time_document = time.perf_counter_ns()

    db.cls_run.Run.ID_RUN_UMBRELLA = 0

    check_new_language()
    check_new_run()
    check_new_version()

    check_new_document()

    check_new_action()

    cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=True, is_file_size_bytes=True)
    cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False, is_file_size_bytes=False)

    check_new_token()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique_driver(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    cfg.glob.db_core.insert_dbt_row(db.cls_db_core.DBCore.DBT_VERSION, {db.cls_db_core.DBCore.DBC_VERSION: "0.0.0"})

    cfg.glob.db_core.disconnect_db()

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    cfg.glob.db_core.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (driver)"
    assert expt.value.code == 1, "Version not unique (driver)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    cfg.glob.db_core = db.cls_db_core.DBCore()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    cfg.glob.db_core.disconnect_db()

    assert expt.type == SystemExit, "Version missing (driver)"
    assert expt.value.code == 1, "Version missing (driver)"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique_orm(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.db_core = db.cls_db_core.DBCore()

    cfg.glob.db_core.insert_dbt_row(db.cls_db_core.DBCore.DBT_VERSION, {db.cls_db_core.DBCore.DBC_VERSION: "0.0.0"})

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    cfg.glob.db_core.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (orm)"
    assert expt.value.code == 1, "Version not unique (orm)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    cfg.glob.db_core = db.cls_db_core.DBCore()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    cfg.glob.db_core.disconnect_db()

    assert expt.type == SystemExit, "Version missing (orm)"
    assert expt.value.code == 1, "Version missing (orm)"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
