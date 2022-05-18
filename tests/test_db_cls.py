# pylint: disable=unused-argument
"""Testing Module db.cls."""

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_base
import db.cls_language
import db.cls_run
import db.cls_token
import db.cls_version
import db.dml
import db.driver
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue
import utils

MISSING_ID: int = 4711


# -----------------------------------------------------------------------------
# Check existing language object.
# -----------------------------------------------------------------------------
def check_existing_language():
    """Check existing language object."""
    expected_values = (1, True, "eng", "en", "en_core_web_trf", "eng", utils.get_os_independent_name("data/inbox_test"), "English")

    instance = db.cls_language.Language.from_id(expected_values[0])

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print(f"issue with dbt language instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt language id={expected_values[0]} - see above"


# -----------------------------------------------------------------------------
# Check existing action object.
# -----------------------------------------------------------------------------
def check_existing_action():
    """Check existing action object."""
    expected_values = (
        1,
        db.cls_run.Run.ACTION_CODE_INBOX,
        db.cls_run.Run.get_action_text(db.cls_run.Run.ACTION_CODE_INBOX),
        cfg.glob.setup.directory_inbox,
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
        cfg.glob.DOCUMENT_STATUS_END,
    )

    instance = db.cls_action.Action.from_id(expected_values[0])

    actual_values = instance.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != expected_values:
        print(f"issue with dbt action instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt action id={expected_values[0]} - see above"


# -----------------------------------------------------------------------------
# Check existing base object.
# -----------------------------------------------------------------------------
def check_existing_base():
    """Check existing base object."""
    expected_values = (
        1,
        db.cls_run.Run.ACTION_CODE_PARSER_LINE,
        db.cls_run.Run.get_action_text(db.cls_run.Run.ACTION_CODE_PARSER_LINE),
        cfg.glob.setup.directory_inbox,
        "",
        "",
        0,
        "pdf_text_ok.pdf",
        53651,
        1,
        7,
        3,
        "e2402cc28e178911ee5941b1f9ac0d596beb7730f101da715f996dc992acbe25",
        cfg.glob.DOCUMENT_STATUS_END,
    )

    instance = db.cls_base.Base.from_id(expected_values[0])

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print(f"issue with dbt base instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt base id={expected_values[0]} - see above"

    # -----------------------------------------------------------------------------
    # Get the duplicate file name based on the hash key.
    # -----------------------------------------------------------------------------
    db.cls_base.Base.select_duplicate_file_name_by_sha256(MISSING_ID, expected_values[12])

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name - positive.
    # -----------------------------------------------------------------------------
    instance.get_stem_name()

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    instance.base_file_name = ""

    instance.get_file_type()

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name - negative.
    # -----------------------------------------------------------------------------
    instance.get_stem_name()

    # -----------------------------------------------------------------------------
    # Get the stem name from the first processed document.
    # -----------------------------------------------------------------------------
    instance.get_stem_name_next()

    # -----------------------------------------------------------------------------
    # Finalise the current row with error.
    # -----------------------------------------------------------------------------
    instance.finalise_error("error_code", "error_msg")


# -----------------------------------------------------------------------------
# Check existing run object.
# -----------------------------------------------------------------------------
def check_existing_run():
    """Check existing run object."""
    expected_values = (
        1,
        db.cls_run.Run.ACTION_CODE_INBOX,
        db.cls_run.Run.get_action_text(db.cls_run.Run.ACTION_CODE_INBOX),
        1,
        cfg.glob.DOCUMENT_STATUS_END,
        0,
        1,
        1,
    )

    instance = db.cls_run.Run.from_id(expected_values[0])

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print(f"issue with dbt run instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt run id={expected_values[0]} - see above"


# -----------------------------------------------------------------------------
# Check existing token object.
# -----------------------------------------------------------------------------
def check_existing_token():
    """Check existing token object."""
    expected_values = (1, True, "eng", "en", "en_core_web_trf", "eng", "data/inbox_test", "English")

    instance = db.cls_token.Token.from_id(expected_values[0])

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print(f"issue with dbt token instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt token id={expected_values[0]} - see above"


# -----------------------------------------------------------------------------
# Check existing version object.
# -----------------------------------------------------------------------------
def check_existing_version():
    """Check existing version object."""
    expected_values = (1, cfg.glob.setup.dcr_version)

    instance = db.cls_version.Version.from_id(expected_values[0])

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print(f"issue with dbt version instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt version id={expected_values[0]} - see above"


# -----------------------------------------------------------------------------
# Check missing action object.
# -----------------------------------------------------------------------------
def check_missing_action():
    """Check missing action object."""
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_action.Action.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt action instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt action instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing base object.
# -----------------------------------------------------------------------------
def check_missing_base():
    """Check missing base object."""
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_base.Base.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt base instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt base instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing language object.
# -----------------------------------------------------------------------------
def check_missing_language():
    """Check missing language object."""
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_language.Language.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt language instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt language instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing run object.
# -----------------------------------------------------------------------------
def check_missing_run():
    """Check missing run object."""
    db.driver.connect_db()

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
            action_code=cfg.glob.INFORMATION_NOT_YET_AVAILABLE,
            total_erroneous=1,
        )

    assert expt.type == SystemExit, f"invalid action code={cfg.glob.INFORMATION_NOT_YET_AVAILABLE}"
    assert expt.value.code == 1, f"invalid action code={cfg.glob.INFORMATION_NOT_YET_AVAILABLE}"

    # -----------------------------------------------------------------------------
    # Untested action codes.
    # -----------------------------------------------------------------------------
    db.driver.connect_db()

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
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_token.Token.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt token instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt token instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing version object.
# -----------------------------------------------------------------------------
def check_missing_version():
    """Check missing version object."""
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt version instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt version instance id={MISSING_ID}"

    # -----------------------------------------------------------------------------
    # Column version in database table version not found.
    # -----------------------------------------------------------------------------
    db.driver.connect_db()

    db.dml.delete_dbt_id(
        table_name=cfg.glob.DBT_VERSION,
        id_where=1,
    )

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    assert expt.type == SystemExit, "issue column version in database table version not found"
    assert expt.value.code == 1, "issue column version in database table version not found"

    # -----------------------------------------------------------------------------
    # Column version in database table version not unique.
    # -----------------------------------------------------------------------------
    db.driver.connect_db()

    instance = db.cls_version.Version(
        version="1",
    )

    instance.persist_2_db()

    instance = db.cls_version.Version(
        version="2",
    )

    instance.persist_2_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    assert expt.type == SystemExit, "issue column version in database table version not unique"
    assert expt.value.code == 1, "issue column version in database table version not unique"


# -----------------------------------------------------------------------------
# Check new action object.
# -----------------------------------------------------------------------------
def check_new_action():
    """Check new action object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = (
        5,
        db.cls_run.Run.ACTION_CODE_INBOX,
        db.cls_run.Run.get_action_text(db.cls_run.Run.ACTION_CODE_INBOX),
        cfg.glob.setup.directory_inbox,
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
        cfg.glob.DOCUMENT_STATUS_START,
    )

    instance = db.cls_action.Action(
        action_code=expected_values[1],
        action_text=expected_values[2],
        directory_name=expected_values[3],
        directory_type=expected_values[4],
        file_name=expected_values[8],
        file_size_bytes=expected_values[9],
        id_base=expected_values[10],
        id_parent=expected_values[10],
        id_run_last=expected_values[11],
        no_children=expected_values[12],
        no_pdf_pages=expected_values[14],
        status=expected_values[15],
    )

    instance.persist_2_db()

    actual_values = instance.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != expected_values:
        print("issue with new dbt action instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt action instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values = (
        5,
        db.cls_run.Run.ACTION_CODE_INBOX,
        db.cls_run.Run.get_action_text(db.cls_run.Run.ACTION_CODE_INBOX),
        cfg.glob.setup.directory_inbox,
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
        cfg.glob.DOCUMENT_STATUS_END,
    )

    instance.action_status = expected_values[14]

    instance.persist_2_db()

    actual_values = instance.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != expected_values:
        print("issue with updated dbt action instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt action instance - see above"


# -----------------------------------------------------------------------------
# Check new base object.
# -----------------------------------------------------------------------------
def check_new_base():
    """Check new base object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = (
        1,
        db.cls_run.Run.ACTION_CODE_PARSER_LINE,
        db.cls_run.Run.get_action_text(db.cls_run.Run.ACTION_CODE_PARSER_LINE),
        cfg.glob.setup.directory_inbox,
        "",
        "",
        0,
        "pdf_text_ok.pdf",
        53651,
        1,
        1,
        3,
        "e2402cc28e178911ee5941b1f9ac0d596beb7730f101da715f996dc992acbe25",
        cfg.glob.DOCUMENT_STATUS_START,
    )

    instance = db.cls_base.Base(
        action_code_last=expected_values[1],
        directory_name=expected_values[3],
        file_name=expected_values[7],
        file_size_bytes=expected_values[8],
        id_language=expected_values[9],
        id_run_last=expected_values[10],
        no_pdf_pages=expected_values[11],
        sha256=expected_values[12],
        status=expected_values[13],
    )

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print("issue with new dbt base instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt base instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values = (
        1,
        db.cls_run.Run.ACTION_CODE_PARSER_LINE,
        db.cls_run.Run.get_action_text(db.cls_run.Run.ACTION_CODE_PARSER_LINE),
        cfg.glob.setup.directory_inbox,
        "",
        "",
        0,
        "pdf_text_ok.pdf",
        53651,
        1,
        1,
        3,
        "e2402cc28e178911ee5941b1f9ac0d596beb7730f101da715f996dc992acbe25",
        cfg.glob.DOCUMENT_STATUS_END,
    )

    instance.base_status = expected_values[13]

    instance.finalise()

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print("issue with updated dbt base instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt base instance - see above"


# -----------------------------------------------------------------------------
# Check new language object.
# -----------------------------------------------------------------------------
def check_new_language():
    """Check new language object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = (
        5,
        True,
        "xxx_code_iso_639_3",
        "xxx_code_pandoc",
        "xxx_code_spacy",
        "xxx_code_tesseract",
        "xxx_directory_name_inbox",
        "xxx_iso_language_name",
    )

    instance = db.cls_language.Language(
        active=expected_values[1],
        code_iso_639_3=expected_values[2],
        code_pandoc=expected_values[3],
        code_spacy=expected_values[4],
        code_tesseract=expected_values[5],
        directory_name_inbox=expected_values[6],
        iso_language_name=expected_values[7],
    )

    instance.persist_2_db()

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print("issue with new dbt language instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt language instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values = (
        5,
        True,
        "xxx_code_iso_639_3",
        "xxx_code_pandoc",
        "xxx_code_spacy",
        "xxx_code_tesseract",
        "",
        "xxx_iso_language_name",
    )

    instance.language_directory_name_inbox = expected_values[6]

    instance.persist_2_db()

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print("issue with updated dbt language instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt language instance - see above"


# -----------------------------------------------------------------------------
# Check new run object.
# -----------------------------------------------------------------------------
def check_new_run():
    """Check new run object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = (
        1,
        db.cls_run.Run.ACTION_CODE_INBOX,
        db.cls_run.Run.get_action_text(db.cls_run.Run.ACTION_CODE_INBOX),
        1,
        cfg.glob.DOCUMENT_STATUS_START,
        1,
        0,
        0,
    )

    instance = db.cls_run.Run(
        _row_id=0,
        action_code=expected_values[1],
        status=expected_values[4],
        total_erroneous=1,
    )

    instance.persist_2_db()

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print("issue with new dbt run instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt run instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values = (
        1,
        db.cls_run.Run.ACTION_CODE_INBOX,
        "inbox         (preprocessor)",
        1,
        cfg.glob.DOCUMENT_STATUS_END,
        1,
        0,
        0,
    )

    instance.run_status = expected_values[4]

    instance.persist_2_db()

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print("issue with updated dbt run instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt run instance - see above"

    # -----------------------------------------------------------------------------
    # Delete object.
    # -----------------------------------------------------------------------------
    db.cls_run.Run.id_run_umbrella = 0

    db.cls_run.Run(
        _row_id=0,
        action_code=expected_values[1],
        status=expected_values[4],
        total_erroneous=0,
    )

    instance.persist_2_db()


# -----------------------------------------------------------------------------
# Check new token object.
# -----------------------------------------------------------------------------
def check_new_token():
    """Check new token object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = (
        5,
        True,
        "xxx_code_iso_639_3",
        "xxx_code_pandoc",
        "xxx_code_spacy",
        "xxx_code_tesseract",
        "xxx_directory_name_inbox",
        "xxx_iso_token_name",
    )

    instance = db.cls_token.Token(
        active=expected_values[1],
        code_iso_639_3=expected_values[2],
        code_pandoc=expected_values[3],
        code_spacy=expected_values[4],
        code_tesseract=expected_values[5],
        directory_name_inbox=expected_values[6],
        iso_token_name=expected_values[7],
    )

    instance.persist_2_db()

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print("issue with new dbt token instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt token instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values = (
        5,
        True,
        "xxx_code_iso_639_3",
        "xxx_code_pandoc",
        "xxx_code_spacy",
        "xxx_code_tesseract",
        "",
        "xxx_iso_token_name",
    )

    instance.token_directory_name_inbox = expected_values[6]

    instance.persist_2_db()

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print("issue with updated dbt token instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt token instance - see above"


# -----------------------------------------------------------------------------
# Check new version object.
# -----------------------------------------------------------------------------
def check_new_version():
    """Check new version object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = (
        2,
        "xxx_version",
    )

    instance = db.cls_version.Version(
        version=expected_values[1],
    )

    instance.persist_2_db()

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print("issue with new dbt version instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt version instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values = (
        2,
        "",
    )

    instance.version_version = expected_values[1]

    instance.finalise()

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
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
        [
            ("pdf_text_ok", "pdf"),
        ],
        cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_ALL_COMPLETE])

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    check_existing_language()
    check_existing_run()
    check_existing_version()

    check_existing_base()

    check_existing_action()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing objects.
# -----------------------------------------------------------------------------
def test_missing_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing objects."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    check_missing_language()
    check_missing_run()
    check_missing_version()

    check_missing_base()

    check_missing_action()

    check_missing_token()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - new objects.
# -----------------------------------------------------------------------------
def test_new_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - new objects."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    check_new_language()
    check_new_run()
    check_new_version()

    check_new_base()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
