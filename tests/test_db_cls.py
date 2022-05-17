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
import db.driver
import pytest

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue
MISSING_ID: int = 4711


# -----------------------------------------------------------------------------
# Check existing language object.
# -----------------------------------------------------------------------------
def check_existing_language():
    """Check existing language object."""
    expected_values = (1, True, "eng", "en", "en_core_web_trf", "eng", "data/inbox_test", "English")

    instance = db.cls_language.Language.from_id(expected_values[0])

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print(f"issue with dbt language instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt language id={expected_values[0]} - see above"


# -----------------------------------------------------------------------------
# Check existing run object.
# -----------------------------------------------------------------------------
def check_existing_run():
    """Check existing run object."""
    expected_values = (1, db.cls_run.Run.ACTION_CODE_INBOX, "inbox         (preprocessor)", 1, "end", 0, 1, 1)

    instance = db.cls_run.Run.from_id(expected_values[0])

    actual_values = instance.get_columns_in_tuple()

    if actual_values != expected_values:
        print(f"issue with dbt run instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt run id={expected_values[0]} - see above"


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
    expected_values = (1, db.cls_run.Run.ACTION_CODE_INBOX, "inbox         (preprocessor)", 1, "start", 1, 0, 0)

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
    expected_values = (1, db.cls_run.Run.ACTION_CODE_INBOX, "inbox         (preprocessor)", 1, "end", 1, 0, 0)

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

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
