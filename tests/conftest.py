# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

# pylint: disable=redefined-outer-name
"""Test Configuration and Fixtures.

Setup test config_setup.dcr.cfg.configurations and store fixtures.

Returns:
    [type]: None.
"""
import configparser
import json
import os
import pathlib
import shutil

import dcr_core.cls_nlp_core
import dcr_core.cls_setup
import dcr_core.cls_text_parser
import dcr_core.cls_tokenizer_spacy
import dcr_core.core_glob
import dcr_core.core_utils
import pytest
import sqlalchemy

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
CONFIG_PARSER: configparser.ConfigParser = configparser.ConfigParser()

FILE_NAME_SETUP_CFG = "setup.cfg"
FILE_NAME_SETUP_CFG_BACKUP = "setup.cfg_backup"


# -----------------------------------------------------------------------------
# Test LineType.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def check_cls_line_type(
    json_file: str,
    target_footer: list[tuple[int, list[int]]],
    target_header: list[tuple[int, list[int]]],
    target_toc: int = 0,
) -> None:
    """Test LineType.

    Args:
        json_file (str): JSON file from text parser.
        target_footer (list[tuple[int, list[int]]]):
                Target footer lines.
        target_header (list[tuple[int, list[int]]]):
                Target header lines.
        target_toc (int):
                Target toc lines.
    """
    instance = dcr_core.cls_text_parser.TextParser.from_files(
        file_encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT, full_name_line=json_file
    )

    actual_footer = []
    actual_header = []

    pages = instance.parse_result_line_document[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGES]

    actual_toc = 0

    for page in pages:
        page_no = page[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]

        actual_page_footer = []
        actual_page_header = []

        for line in page[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES]:
            line_type = line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]
            if line_type == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_FOOTER:
                actual_page_footer.append(int(line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]) - 1)
            elif line_type == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_HEADER:
                actual_page_header.append(int(line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]) - 1)
            elif line_type == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_TOC:
                actual_toc += 1

        if actual_page_footer:
            actual_footer.append((page_no, actual_page_footer))

        if actual_page_header:
            actual_header.append((page_no, actual_page_header))

    assert actual_header == target_header, f"file={json_file} header difference: \ntarget={target_header} \nactual={actual_header}"
    assert actual_footer == target_footer, f"file={json_file} footer difference: \ntarget={target_footer} \nactual={actual_footer}"
    assert actual_toc == target_toc, f"file={json_file} toc difference: \ntarget={target_toc} \nactual={actual_toc}"


# -----------------------------------------------------------------------------
# Check the content of database table action.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def check_dbt_action(param: tuple[int, tuple[int, str, str, int, str, int, int, int]]) -> None:
    """Check the content of database table action.

    Args:
        param (tuple[int, tuple[int, str, str, int, str, int, int, int]]):
                tuples with the contents of the table columns.
    """
    (id_row, expected_values) = param

    dbt = dcr.db.cls_action.Action.from_id(id_row)

    actual_values = dbt.get_columns_in_tuple(is_duration_ns=False, is_file_size_bytes=False)

    if expected_values != actual_values:
        print(f"issue with dbt action and id={id_row}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt action and id={id_row} - see above"


# -----------------------------------------------------------------------------
# Check the content of database table document.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def check_dbt_document(param: tuple[int, tuple[int, str, str, int, str, int, int, int]]) -> None:
    """Check the content of database table document.

    Args:
        param (tuple[int, tuple[int, str, str, int, str, int, int, int]]):
                tuples with the contents of the table columns.
    """
    (id_row, expected_values) = param

    dbt = dcr.db.cls_document.Document.from_id(id_row)

    actual_values = dbt.get_columns_in_tuple(is_file_size_bytes=False, is_sha256=False)

    if expected_values != actual_values:
        print(f"issue with dbt document and id={id_row}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt document and id={id_row} - see above"


# -----------------------------------------------------------------------------
# Check the content of database table language.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def check_dbt_language(param: tuple[int, tuple[int, bool, str, str, str, str, str, str, str]]) -> None:
    """Check the content of database table language.

    Args:
        param (tuple[int, tuple[int, bool, str, str, str, str, str, str, str]]):
                tuples with the contents of the table columns.
    """
    (id_row, expected_values) = param

    dbt = dcr.db.cls_language.Language.from_id(id_row)

    actual_values = dbt.get_columns_in_tuple()

    if expected_values != actual_values:
        print(f"issue with dbt language and id={id_row}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt language and id={id_row} - see above"


# -----------------------------------------------------------------------------
# Check the content of database table run.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def check_dbt_run(param: tuple[int, tuple[int, str, str, int, str, int, int, int]]) -> None:
    """Check the content of database table run.

    Args:
        param (tuple[int, tuple[int, str, str, int, str, int, int, int]]):
                tuples with the contents of the table columns.
    """
    (id_row, expected_values) = param

    dbt = dcr.db.cls_run.Run.from_id(id_row)

    actual_values = dbt.get_columns_in_tuple()

    if expected_values != actual_values:
        print(f"issue with dbt run and id={id_row}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt run and id={id_row} - see above"


# -----------------------------------------------------------------------------
# Check the content of database table token.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def check_dbt_token(param: tuple[int, tuple[int, str, str, int, str, int, int, int]]) -> None:
    """Check the content of database table token.

    Args:
        param (tuple[int, tuple[int, str, str, int, str, int, int, int]]):
                tuples with the contents of the table columns.
    """
    (id_row, expected_values) = param

    dbt = dcr.db.cls_token.Token.from_id(id_row)

    actual_values = dbt.get_columns_in_tuple()

    if expected_values != actual_values:
        print(f"issue with dbt token and id={id_row}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt token and id={id_row} - see above"


# -----------------------------------------------------------------------------
# Check the content of database table version.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def check_dbt_version(param: tuple[int, tuple[int, str]]) -> None:
    """Check the content of database table version.

    Args:
        param (tuple[int, tuple[int, str]]):
                tuples with the contents of the table columns.
    """
    (id_row, expected_values) = param

    dbt = dcr.db.cls_version.Version.from_id(id_row)

    actual_values = dbt.get_columns_in_tuple()

    if expected_values != actual_values:
        print(f"issue with dbt version and id={id_row}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt version and id={id_row} - see above"


# -----------------------------------------------------------------------------
# Check data of a the JSON file: line version.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def check_json_line(
    file_name: str,
    no_lines_footer: int = 0,
    no_lines_header: int = 0,
    no_lines_toc: int = 0,
    no_lists_bullet_in_document: int = 0,
    no_lists_number_in_document: int = 0,
    no_tables_in_document: int = 0,
) -> None:
    full_name = dcr_core.core_utils.get_full_name(directory_name=dcr_core.core_glob.setup.directory_inbox_accepted, file_name=file_name)

    try:
        with open(full_name, "r", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            document_json = json.load(file_handle)

            assert document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_FOOTER] == no_lines_footer, (
                f"file={file_name} number line footer: expected={no_lines_footer} - "
                + f"actual={document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_FOOTER]}"
            )
            assert document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADER] == no_lines_header, (
                f"file={file_name} number line header: expected={no_lines_header} - "
                + f"actual={document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADER]}"
            )

            assert document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC] == no_lines_toc, (
                f"file={file_name} number lines toc: expected={no_lines_toc} - "
                + f"actual={document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC]}"
            )

            assert document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET_IN_DOC] == no_lists_bullet_in_document, (
                f"file={file_name} number bulleted lists in document: expected={no_lists_bullet_in_document} - "
                + f"actual={document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET_IN_DOC]}"
            )
            assert document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER_IN_DOC] == no_lists_number_in_document, (
                f"file={file_name} number numbered lists in document: expected={no_lists_number_in_document} - "
                + f"actual={document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER_IN_DOC]}"
            )

            assert document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_TABLES_IN_DOC] == no_tables_in_document, (
                f"file={file_name} number tables in document: expected={no_tables_in_document} - "
                + f"actual={document_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_TABLES_IN_DOC]}"
            )

    except OSError as err:
        assert False, f"file={full_name} problem opening the file: error={err.errno} - {err.strerror}"


# -----------------------------------------------------------------------------
# Delete the original configuration parameter value.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def config_param_delete(config_section: str, config_param: str) -> None:
    """Delete the original configuration parameter value.

    Args:
        config_section (str): Configuration section.
        config_param (str): Configuration parameter.
    """
    CONFIG_PARSER.read(dcr.cfg.cls_setup.Setup._DCR_CFG_FILE)

    del CONFIG_PARSER[config_section][config_param]

    with open(dcr.cfg.cls_setup.Setup._DCR_CFG_FILE, "w", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)


# -----------------------------------------------------------------------------
# modify configuration parameter values.
# -----------------------------------------------------------------------------
# noinspection PyProtectedMember
@pytest.helpers.register
def config_params_modify(
    config_section: str,
    config_params: list[tuple[str, str]],
) -> None:
    """Backup and modify configuration parameter values.

    Args:
        config_section (str): Configuration section.
        config_params (list[tuple[str, str]]): Configuration parameter modifications.
    """
    CONFIG_PARSER.read(dcr.cfg.cls_setup.Setup._DCR_CFG_FILE)

    for (config_param, config_value) in config_params:
        CONFIG_PARSER[config_section][config_param] = config_value

    with open(dcr.cfg.cls_setup.Setup._DCR_CFG_FILE, "w", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as configfile:
        CONFIG_PARSER.write(configfile)


# -----------------------------------------------------------------------------
# Copy directories from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_directories_4_pytest_2_dir(
    source_directories: list[str],
    target_dir: str,
) -> None:
    """Copy directories from the sample test file directory.

    Args:
        source_directories: list[str]: Source directory names.
        target_dir: str: Target directory.
    """
    assert os.path.isdir(dcr_core.core_utils.get_os_independent_name(get_test_inbox_directory_name())), (
        "source base directory '" + get_test_inbox_directory_name() + "' missing"
    )

    for source in source_directories:
        source_dir = get_test_inbox_directory_name() + "/" + source
        source_path = dcr_core.core_utils.get_full_name(get_test_inbox_directory_name(), pathlib.Path(source))
        assert os.path.isdir(dcr_core.core_utils.get_os_independent_name(source_path)), (
            "source language directory '" + str(source_path) + "' missing"
        )
        target_path = dcr_core.core_utils.get_full_name(target_dir, pathlib.Path(source))
        shutil.copytree(source_dir, target_path)


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_files_4_pytest(file_list: list[tuple[tuple[str, str | None], tuple[pathlib.Path, list[str], str | None]]]) -> None:
    """Copy files from the sample test file directory.

    Args:
        file_list (list[
            tuple[
                tuple[str, str | None],
                tuple[pathlib.Path, list[str], str | None]
            ]
        ]): list of files to be copied.
    """
    assert os.path.isdir(dcr_core.core_utils.get_os_independent_name(get_test_inbox_directory_name())), (
        "source directory '" + get_test_inbox_directory_name() + "' missing"
    )

    for ((source_stem, source_ext), (target_dir, target_file_comp, target_ext)) in file_list:
        source_file_name = source_stem if source_ext is None else source_stem + "." + source_ext
        source_file = dcr_core.core_utils.get_full_name(get_test_inbox_directory_name(), source_file_name)
        assert os.path.isfile(source_file), "source file '" + str(source_file) + "' missing"

        assert os.path.isdir(dcr_core.core_utils.get_os_independent_name(target_dir)), "target directory '" + target_dir + "' missing"
        target_file_name = "_".join(target_file_comp) if target_ext is None else "_".join(target_file_comp) + "." + target_ext
        target_file = dcr_core.core_utils.get_full_name(target_dir, target_file_name)
        assert os.path.isfile(target_file) is False, "target file '" + str(target_file) + "' already existing"

        shutil.copy(source_file, target_file)
        assert os.path.isfile(target_file), "target file '" + str(target_file) + "' is missing"


# -----------------------------------------------------------------------------
# Copy files from the sample test file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def copy_files_4_pytest_2_dir(
    source_files: list[tuple[str, str | None]],
    target_path: pathlib.Path,
) -> None:
    """Copy files from the sample test file directory.

    Args:
        source_files: list[tuple[str, str | None]]: Source file names.
        target_path: Path: Target directory.
    """
    for source_file in source_files:
        (source_stem, source_ext) = source_file
        copy_files_4_pytest([(source_file, (target_path, [source_stem], source_ext))])


# -----------------------------------------------------------------------------
# Create one row in database table action.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def create_action():
    """Create one row in database table action.

    Returns:
        list: Column values
    """
    values = get_values_action()

    instance = dcr.db.cls_action.Action(
        action_code=values[1],
        action_text=values[2],
        directory_name=values[3],
        directory_type=values[4],
        file_name=values[8],
        file_size_bytes=values[9],
        id_document=values[10],
        id_parent=values[11],
        id_run_last=values[12],
        no_children=values[13],
        no_pdf_pages=values[14],
        status=values[15],
    )

    values[0] = instance.action_id

    return values


# -----------------------------------------------------------------------------
# Create one row in database table document.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def create_document():
    """Create one row in database table document.

    Returns:
        list: Column values
    """
    values = get_values_document()

    instance = dcr.db.cls_document.Document(
        action_code_last=values[1],
        directory_name=values[3],
        file_name=values[7],
        file_size_bytes=values[8],
        id_language=values[9],
        id_run_last=values[10],
        no_lines_footer=values[11],
        no_lines_header=values[12],
        no_lines_toc=values[13],
        no_lists_bullet=values[14],
        no_lists_number=values[15],
        no_tables=values[16],
        no_pdf_pages=values[17],
        status=values[18],
    )

    values[0] = instance.document_id

    return values


# -----------------------------------------------------------------------------
# Create one row in database table language.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def create_language():
    """Create one row in database table language.

    Returns:
        list: Column values
    """
    values = get_values_language()

    instance = dcr.db.cls_language.Language(
        active=values[1],
        code_iso_639_3=values[2],
        code_pandoc=values[3],
        code_spacy=values[4],
        code_tesseract=values[5],
        directory_name_inbox=values[6],
        iso_language_name=values[7],
    )

    instance.persist_2_db()

    values[0] = instance.language_id

    return values


# -----------------------------------------------------------------------------
# Create one row in database table run.
# -----------------------------------------------------------------------------
# noinspection PyArgumentlist
@pytest.helpers.register
def create_run():
    """Create one row in database table run.

    Returns:
        list: Column values
    """
    values = get_values_run()

    instance = dcr.db.cls_run.Run(
        _row_id=0,
        action_code=values[1],
        status=values[4],
        total_erroneous=values[5],
    )

    instance.persist_2_db()

    values[0] = instance.run_id

    return values


# -----------------------------------------------------------------------------
# Create one row in database table token.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def create_token():
    """Create one row in database table token.

    Returns:
        list: Column values
    """

    values = get_values_token()

    instance = dcr.db.cls_token.Token(
        id_document=values[1],
        column_no=values[2],
        column_span=values[3],
        coord_llx=values[4],
        coord_urx=values[5],
        line_type=values[6],
        no_tokens_in_sent=values[7],
        page_no=values[8],
        para_no=values[9],
        row_no=values[10],
        sent_no=values[11],
        text=values[12],
        tokens=values[13],
    )

    values[0] = instance.token_id

    return values


# -----------------------------------------------------------------------------
# Create one row in database table version.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def create_version():
    """Create one row in database table version.

    Returns:
        list: Column values
    """
    values = get_values_version()

    instance = dcr.db.cls_version.Version(
        version=values[1],
    )

    instance.persist_2_db()

    values[0] = instance.version_id

    return values


# -----------------------------------------------------------------------------
# Delete existing objects.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def delete_existing_object(  # noqa: C901
    is_action_curr: bool = False,
    is_action_next: bool = False,
    is_db_core: bool = False,
    is_document: bool = False,
    is_run: bool = False,
    is_setup: bool = False,
    is_text_parser: bool = False,
) -> None:
    """Delete existing objects.

    Args:
        is_action_curr (bool, optional):
                Check an object of class Action. Defaults to False.
        is_action_next (bool, optional):
                Check an object of class Action . Defaults to False.
        is_db_core (bool, optional):
                Check an object of class DbCore. Defaults to False.
        is_document (bool, optional):
                Check an object of class Document. Defaults to False.
        is_run (bool, optional):
                Check an object of class Run. Defaults to False.
        is_setup (bool, optional):
                Check an object of class Setup. Defaults to False.
        is_text_parser (bool, optional):
                Check an object of class TextParser. Defaults to False.
    """
    if is_action_curr:
        try:
            dcr.cfg.glob.action_curr.exists()  # type: ignore

            del dcr.cfg.glob.action_curr

            dcr.cfg.glob.logger.debug("The existing object 'dcr.cfg.glob.action_curr' of the class Action was deleted.")
        except AttributeError:
            pass

    if is_action_next:
        try:
            dcr.cfg.glob.action_next.exists()  # type: ignore

            del dcr.cfg.glob.action_next

            dcr.cfg.glob.logger.debug("The existing object 'dcr.cfg.glob.action_next' of the class Action was deleted.")
        except AttributeError:
            pass

    if is_db_core:
        try:
            dcr.cfg.glob.db_core.exists()  # type: ignore

            del dcr.cfg.glob.db_core

            dcr.cfg.glob.logger.debug("The existing object 'dcr.cfg.glob.db_core' of the class DBCore was deleted.")
        except AttributeError:
            pass

    if is_document:
        try:
            dcr.cfg.glob.document.exists()  # type: ignore

            del dcr.cfg.glob.document

            dcr.cfg.glob.logger.debug("The existing object 'dcr.cfg.glob.document' of the class Document was deleted.")
        except AttributeError:
            pass

    if is_run:
        try:
            dcr.cfg.glob.run.exists()  # type: ignore

            del dcr.cfg.glob.run

            dcr.cfg.glob.logger.debug("The existing object 'dcr.cfg.glob.run' of the class Run was deleted.")
        except AttributeError:
            pass

    if is_setup:
        try:
            dcr_core.core_glob.setup.exists()  # type: ignore

            del dcr_core.core_glob.setup

            dcr.cfg.glob.logger.debug("The existing object 'dcr_core.base.setup' of the class Setup was deleted.")
        except AttributeError:
            pass

    if is_text_parser:
        try:
            dcr_core.core_glob.text_parser.exists()  # type: ignore

            del dcr_core.core_glob.text_parser

            dcr.cfg.glob.logger.debug("The existing object 'dcr.cfg.glob.text_parser' of the class TextParser was deleted.")
        except AttributeError:
            pass


# -----------------------------------------------------------------------------
# Delete all entries in the database table 'version'.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def delete_version_version():
    """Delete all entries in the database table 'version'."""
    db_core = dcr.db.cls_db_core.DBCore()

    with dcr.cfg.glob.db_core.db_orm_engine.begin() as conn:
        version = sqlalchemy.Table(
            dcr.db.cls_db_core.DBCore.DBT_VERSION,
            dcr.cfg.glob.db_core.db_orm_metadata,
            autoload_with=dcr.cfg.glob.db_core.db_orm_engine,
        )
        conn.execute(sqlalchemy.delete(version))

    db_core.disconnect_db()


# -----------------------------------------------------------------------------
# Fixture - Before any test.
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def fxtr_before_any_test():
    """Fixture Factory: Before any test."""
    CONFIG_PARSER.read(dcr.cfg.cls_setup.Setup._DCR_CFG_FILE)

    # -----------------------------------------------------------------------------
    # Configuration: dcr.
    # -----------------------------------------------------------------------------
    for (config_param, config_value) in (
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_CONNECTION_PORT, "5434"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_CONNECTION_PREFIX, "postgresql+psycopg2://"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_CONTAINER_PORT, "5432"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_DATABASE, "dcr_db_test"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_DATABASE_ADMIN, "dcr_db_test_admin"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_DIALECT, "postgresql"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_HOST, "localhost"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_INITIAL_DATA_FILE, "data/db_initial_data_file_test.json"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_PASSWORD, "postgresql"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_PASSWORD_ADMIN, "postgresql"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_SCHEMA, "dcr_schema"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_USER, "dcr_user"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DB_USER_ADMIN, "dcr_user_admin"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DELETE_AUXILIARY_FILES, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX, "data/inbox_test"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED, "data/inbox_test_accepted"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED, "data/inbox_test_rejected"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_DOC_ID_IN_FILE_NAME, "none"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_IGNORE_DUPLICATES, "false"),
    ):
        CONFIG_PARSER[dcr.cfg.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST][config_param] = config_value

    # -----------------------------------------------------------------------------
    # Configuration: dcr_core.
    # -----------------------------------------------------------------------------
    for (config_param, config_value) in (
        (dcr.cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_HEADING, "true"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, "true"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, "true"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, "true"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_JSON_INDENT, "4"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_JSON_SORT_KEYS, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_HEADING, "tmp/lt_export_rule_heading.json"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_LIST_BULLET, "tmp/lt_export_rule_list_bullet.json"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_EXPORT_RULE_FILE_LIST_NUMBER, "tmp/lt_export_rule_list_number.json"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, "3"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_FOOTER_MAX_LINES, "3"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, "3"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_HEADER_MAX_LINES, "3"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX, "3"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_FILE_INCL_REGEXP, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_MAX_LEVEL, "3"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_MIN_PAGES, "2"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_RULE_FILE, "data/lt_export_rule_heading_test.json"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_HEADING_TOLERANCE_LLX, "5"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES, "2"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_RULE_FILE, "data/lt_export_rule_list_bullet_test.json"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX, "5"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_LIST_NUMBER_FILE_INCL_REGEXP, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_LIST_NUMBER_MIN_ENTRIES, "2"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_LIST_NUMBER_RULE_FILE, "data/lt_export_rule_list_number_test.json"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_LIST_NUMBER_TOLERANCE_LLX, "5"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_TABLE_FILE_INCL_EMPTY_COLUMNS, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_TOC_LAST_PAGE, "5"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_LT_TOC_MIN_ENTRIES, "5"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_PDF2IMAGE_TYPE, dcr_core.cls_setup.Setup.PDF2IMAGE_TYPE_JPEG),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_TESSERACT_TIMEOUT, "30"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_TETML_PAGE, "true"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_TETML_WORD, "true"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_DATABASE, "true"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_TOKENIZE_2_JSONFILE, "true"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_VERBOSE, "true"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_HEADING, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_BULLET, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_LIST_NUMBER, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TABLE, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_VERBOSE_LT_TOC, "false"),
        (dcr.cfg.cls_setup.Setup._DCR_CFG_VERBOSE_PARSER, "none"),
    ):
        CONFIG_PARSER[dcr_core.cls_setup.Setup._DCR_CFG_SECTION_ENV_TEST][config_param] = config_value


# -----------------------------------------------------------------------------
# Fixture - Create a new directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_mkdir():
    """Fixture Factory: Create a new directory."""

    def _fxtr_mkdir(directory_name: str):
        """
        Fixture: Create a new directory.

        Args:
            directory_name (str): The directory name including path.
        """
        os.mkdir(directory_name)

    return _fxtr_mkdir


# -----------------------------------------------------------------------------
# Fixture - Delete a directory.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_rmdir():
    """Fixture Factory: Delete a directory."""

    def _fxtr_rmdir(directory_name: str):
        """
        Fixture: Delete a directory.

        Args:
            directory_name (str): The directory name including path.
        """
        shutil.rmtree(directory_name)

    return _fxtr_rmdir


# -----------------------------------------------------------------------------
# Fixture - Delete a directory if existing.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_rmdir_opt(fxtr_rmdir):
    """Fixture Factory: Delete a directory if existing."""

    def _fxtr_rmdir_opt(directory_name: str):
        """
        Fixture: Delete a directory if existing.

        Args:
            directory_name (str): The directory name including path.
        """
        if os.path.isdir(directory_name):
            fxtr_rmdir(directory_name)

    return _fxtr_rmdir_opt


# -----------------------------------------------------------------------------
# Fixture - Setup empty database and empty inboxes.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_empty_db_and_inbox(
    fxtr_mkdir,
    fxtr_rmdir_opt,
):
    """Fixture: Setup empty database and empty inboxes."""
    setup_cfg_backup()

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # restore original file
    shutil.copy(
        dcr_core.core_utils.get_full_name(
            get_test_inbox_directory_name(),
            os.path.basename(pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)),
        ),
        os.path.dirname(pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)),
    )

    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_CREATE_DB])

    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox)
    fxtr_mkdir(dcr_core.core_glob.setup.directory_inbox)
    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox_accepted)
    fxtr_mkdir(dcr_core.core_glob.setup.directory_inbox_accepted)
    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox_rejected)
    fxtr_mkdir(dcr_core.core_glob.setup.directory_inbox_rejected)

    yield

    try:
        dcr_core.core_glob.setup.exists()  # type: ignore

        fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox_rejected)
        fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox_accepted)
        fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox)

        dcr.cfg.glob.db_core._drop_database()
    except AttributeError:
        pass

    setup_cfg_restore()


# -----------------------------------------------------------------------------
# Fixture - Setup empty database and empty inboxes.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_empty_inbox(
    fxtr_mkdir,
    fxtr_rmdir_opt,
):
    """Fixture: Setup empty database and empty inboxes."""
    setup_cfg_backup()

    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # restore original file
    shutil.copy(
        dcr_core.core_utils.get_full_name(
            get_test_inbox_directory_name(),
            os.path.basename(pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)),
        ),
        os.path.dirname(pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)),
    )

    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox)
    fxtr_mkdir(dcr_core.core_glob.setup.directory_inbox)
    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox_accepted)
    fxtr_mkdir(dcr_core.core_glob.setup.directory_inbox_accepted)
    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox_rejected)
    fxtr_mkdir(dcr_core.core_glob.setup.directory_inbox_rejected)

    yield

    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox_rejected)
    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox_accepted)
    fxtr_rmdir_opt(dcr_core.core_glob.setup.directory_inbox)

    dcr.cfg.glob.db_core._drop_database()

    setup_cfg_restore()


# -----------------------------------------------------------------------------
# Fixture - Setup logger.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_logger():
    """Fixture: Setup logger & environment."""
    dcr.launcher.initialise_logger()

    yield


# -----------------------------------------------------------------------------
# Fixture - Setup logger & environment.
# -----------------------------------------------------------------------------
@pytest.fixture()
def fxtr_setup_logger_environment():
    """Fixture: Setup logger & environment."""
    dcr_core.core_glob.setup = dcr.cfg.cls_setup.Setup()

    # restore original file
    shutil.copy(
        dcr_core.core_utils.get_full_name(
            get_test_inbox_directory_name(),
            os.path.basename(pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)),
        ),
        os.path.dirname(pathlib.Path(dcr_core.core_glob.setup.db_initial_data_file)),
    )

    dcr_core.core_glob.setup.environment_type = dcr_core.core_glob.setup.ENVIRONMENT_TYPE_TEST

    setup_cfg_backup()

    dcr.launcher.initialise_logger()

    yield

    setup_cfg_restore()


# -----------------------------------------------------------------------------
# Provide the directory name of the inbox with the test data.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def get_test_inbox_directory_name():
    """Provide the directory name of the inbox with the test data."""
    return "tests/__PYTEST_FILES__/"


# -----------------------------------------------------------------------------
# Provide expected values - database table action.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def get_values_action():
    """Provide expected values - database table action."""
    return [
        None,
        "p_i",
        "inbox         (preprocessor)",
        dcr_core.core_glob.setup.directory_inbox,
        "inbox",
        "",
        "",
        0,
        "pdf_text_ok.pdf",
        53651,
        1,
        None,
        1,
        0,
        3,
        dcr.db.cls_document.Document.DOCUMENT_STATUS_START,
    ]


# -----------------------------------------------------------------------------
# Provide expected values - database table document.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def get_values_document():
    """Provide expected values - database table document."""
    return [
        None,
        "s_p_j_line",
        "parser_line   (nlp)",
        dcr_core.core_glob.setup.directory_inbox,
        "",
        "",
        0,
        "pdf_text_ok.pdf",
        53651,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        dcr.db.cls_document.Document.DOCUMENT_STATUS_START,
    ]


# -----------------------------------------------------------------------------
# Provide expected values - database table language.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def get_values_language() -> list[bool | int | str | None]:
    """Provide expected values - database table language."""
    return [
        None,
        True,
        "xxx_code_iso_639_3",
        "xxx_code_pandoc",
        "xxx_code_spacy",
        "xxx_code_tesseract",
        "xxx_directory_name_inbox",
        "xxx_iso_language_name",
    ]


# -----------------------------------------------------------------------------
# Provide expected values - database table run.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def get_values_run() -> list[bool | int | str | None]:
    """Provide expected values - database table run."""
    return [
        None,
        "p_i",
        "inbox         (preprocessor)",
        1,
        dcr.db.cls_document.Document.DOCUMENT_STATUS_START,
        1,
        0,
        0,
    ]


# -----------------------------------------------------------------------------
# Provide expected values - database table token.
# -----------------------------------------------------------------------------
# pylint: disable=duplicate-code
@pytest.helpers.register
def get_values_token() -> list[int | list[dict] | str | None]:
    """Provide expected values - database table token."""
    return [
        None,
        dcr.cfg.glob.document.document_id,
        0,
        2,
        71,
        0,
        "b",
        2,
        2,
        1,
        0,
        1,
        "Start Document ...",
        [
            {
                "tknEntIob_": "O",
                "tknI": 0,
                "tknIsOov": True,
                "tknIsSentStart": True,
                "tknIsTitle": True,
                "tknLemma_": "start",
                "tknNorm_": "start",
                "tknPos_": "VERB",
                "tknTag_": "VB",
                "tknText": "Start",
                "tknWhitespace_": " ",
            },
            {
                "tknEntIob_": "O",
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


# -----------------------------------------------------------------------------
# Provide expected values - database table version.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def get_values_version() -> list[int | str | None]:
    """Provide expected values - database table version."""
    return [
        None,
        "xxx_version",
    ]


# -----------------------------------------------------------------------------
# Help RUN_ACTION_ALL_COMPLETE - duplicate file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def help_run_action_all_complete_duplicate_file(
    file_ext_1: str,
    file_ext_2: str,
    stem_name_1: str,
    stem_name_2: str,
    is_ocr: bool = False,
) -> None:
    """Help RUN_ACTION_ALL_COMPLETE - duplicate file."""
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[(stem_name_1, file_ext_1)], target_path=dcr_core.core_glob.setup.directory_inbox_accepted
    )

    os.rename(
        dcr_core.core_utils.get_full_name(dcr_core.core_glob.setup.directory_inbox_accepted, stem_name_1 + "." + file_ext_1),
        dcr_core.core_utils.get_full_name(dcr_core.core_glob.setup.directory_inbox_accepted, stem_name_2 + "." + file_ext_2),
    )

    # -------------------------------------------------------------------------
    if is_ocr:
        dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])
        dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_PDF2IMAGE])
        dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TESSERACT])
        dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_TESSERACT])
    else:
        dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_ALL_COMPLETE])

        verify_content_of_directory(
            dcr_core.core_glob.setup.directory_inbox,
            [],
            [],
        )

        verify_content_of_directory(
            dcr_core.core_glob.setup.directory_inbox_accepted,
            [],
            [stem_name_1 + "_1." + file_ext_1, stem_name_2 + "." + file_ext_2],
        )

        verify_content_of_directory(
            dcr_core.core_glob.setup.directory_inbox_rejected,
            [],
            [],
        )


# -----------------------------------------------------------------------------
# Help RUN_ACTION_PROCESS_INBOX - normal.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def help_run_action_process_inbox_normal(
    stem_name,
    file_ext,
):
    """Help RUN_ACTION_PROCESS_INBOX - normal."""
    pytest.helpers.copy_files_4_pytest_2_dir(source_files=[(stem_name, file_ext)], target_path=dcr_core.core_glob.setup.directory_inbox)

    # -------------------------------------------------------------------------
    dcr.launcher.main([dcr.launcher.DCR_ARGV_0, dcr.db.cls_run.Run.ACTION_CODE_INBOX])
    # -------------------------------------------------------------------------
    document_id = 1

    file_p_i = (
        dcr_core.core_glob.setup.directory_inbox_accepted,
        [stem_name, str(document_id)],
        file_ext,
    )

    verify_content_of_directory(
        dcr_core.core_glob.setup.directory_inbox,
        [],
        [],
    )

    verify_content_of_directory(
        dcr_core.core_glob.setup.directory_inbox_accepted,
        [],
        [stem_name + "_" + str(document_id) + "." + file_ext],
    )

    verify_content_of_directory(
        dcr_core.core_glob.setup.directory_inbox_rejected,
        [],
        [],
    )

    return document_id, file_p_i


# -----------------------------------------------------------------------------
# Set all spaCy configuration parameters to the same logical value.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def set_complete_cfg_spacy(false_or_true: str):
    """Set all spaCy configuration parameters to the same logical value."""
    return pytest.helpers.config_params_modify(
        dcr_core.cls_setup.Setup._DCR_CFG_SECTION_SPACY,
        [
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_BRACKET, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_LEFT_PUNCT, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_PUNCT, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_QUOTE, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_SPACE, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_IGNORE_STOP, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_CLUSTER, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_DEP_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_DOC, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_HEAD, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_I, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IDX, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_ASCII, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_BRACKET, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_LEFT_PUNCT, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_LOWER, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_OOV, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_QUOTE, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_RIGHT_PUNCT, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SPACE, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_STOP, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_TITLE, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_IS_UPPER, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LANG_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LEMMA_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LEX, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LEX_ID, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_URL, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_LOWER_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_MORPH, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_NORM_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_ORTH_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_POS_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_PREFIX_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_PROB, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_RANK, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_SENT, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_SENTIMENT, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_SUFFIX_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_TAG_, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_TENSOR, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_VOCAB, false_or_true),
            (dcr.cfg.cls_setup.Setup._DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_, false_or_true),
        ],
    )


# -----------------------------------------------------------------------------
# Backup the 'setup.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def setup_cfg_backup() -> None:
    """Backup the 'setup.cfg' file."""
    if os.path.isfile(FILE_NAME_SETUP_CFG_BACKUP):
        shutil.copy2(FILE_NAME_SETUP_CFG_BACKUP, FILE_NAME_SETUP_CFG)
    else:
        shutil.copy2(FILE_NAME_SETUP_CFG, FILE_NAME_SETUP_CFG_BACKUP)


# -----------------------------------------------------------------------------
# Restore the 'setup.cfg' file.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def setup_cfg_restore():
    """Restore the 'setup.cfg' file."""
    if os.path.isfile(FILE_NAME_SETUP_CFG_BACKUP):
        shutil.copy2(FILE_NAME_SETUP_CFG_BACKUP, FILE_NAME_SETUP_CFG)
        os.remove(FILE_NAME_SETUP_CFG_BACKUP)
    else:
        assert False, f"The backup copy {FILE_NAME_SETUP_CFG_BACKUP} is missing"


# -----------------------------------------------------------------------------
# Run before all tests.
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_dcr():
    """Run before all tests."""
    dcr.launcher.initialise_logger()


# -----------------------------------------------------------------------------
# Verify the content of a file directory.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def verify_content_of_directory(
    directory_name: str,
    expected_directories: list[str],
    expected_files: list[str],
) -> None:
    """Verify the content of a file directory.

    Args:
        directory_name: str:
                   Name of the file directory to be checked.
        expected_directories: list[str]:
                   list of the expected directory names.
        expected_files: list[str]:
                   list of the expected file names.
    """
    dcr.cfg.glob.logger.info("directory name   =%s", directory_name)

    directory_content = os.listdir(directory_name)
    dcr.cfg.glob.logger.info("existing directory content=%s", str(directory_content))
    dcr.cfg.glob.logger.info("expected directory content=%s", str(expected_directories))
    dcr.cfg.glob.logger.info("expected file      content=%s", str(expected_files))

    # check directory content against expectations
    for elem in directory_content:
        elem_path = dcr_core.core_utils.get_full_name(directory_name, elem)
        if os.path.isdir(elem_path):
            assert elem in expected_directories, f"directory {elem} was not expected"
        else:
            assert elem in expected_files, f"file {elem} was not expected"

    # check expected directories against directory content
    for elem in expected_directories:
        assert elem in directory_content, f"expected directory {elem} is missing"
        elem_path = dcr_core.core_utils.get_full_name(directory_name, elem)
        assert os.path.isdir(dcr_core.core_utils.get_os_independent_name(elem_path)), f"expected directory {elem} is a file"

    # check expected files against directory content
    for elem in expected_files:
        assert elem in directory_content, f"expected file {elem} is missing"
        elem_path = dcr_core.core_utils.get_full_name(directory_name, elem)
        assert os.path.isfile(elem_path), f"expected file {elem} is a directory"


# -----------------------------------------------------------------------------
# Verify the content of an inbox directories.
# -----------------------------------------------------------------------------
@pytest.helpers.register
def verify_content_of_inboxes(
    inbox: tuple[list[str], list[str]] = ([], []),
    inbox_accepted: tuple[list[str], list[str]] = ([], []),
    inbox_rejected: tuple[list[str], list[str]] = ([], []),
) -> None:
    """Verify the content of an inbox directories..

    Args:
        inbox: tuple[list[str],list[str]]:
                   An optional list of expected directories and
                   an optional list of expected files in the inbox directory.
        inbox_accepted: tuple[list[str],list[str]]:
                   An optional list of expected directories and
                   an optional list of expected files in the inbox_accepted directory.
        inbox_rejected: tuple[list[str],list[str]]:
                   An optional list of expected directories and
                   an optional list of expected files in the inbox_rejected directory.
    """
    verify_content_of_directory(
        directory_name=dcr_core.core_glob.setup.directory_inbox,
        expected_directories=inbox[0],
        expected_files=inbox[1],
    )

    verify_content_of_directory(
        directory_name=dcr_core.core_glob.setup.directory_inbox_accepted,
        expected_directories=inbox_accepted[0],
        expected_files=inbox_accepted[1],
    )
    verify_content_of_directory(
        directory_name=dcr_core.core_glob.setup.directory_inbox_rejected,
        expected_directories=inbox_rejected[0],
        expected_files=inbox_rejected[1],
    )
