# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import os
import pathlib
from typing import ClassVar
from typing import TypeAlias

Columns: TypeAlias = dict[str, bool | float | int | None | os.PathLike[str] | str]
ColumnValues: TypeAlias = tuple[bool | float | int | None | os.PathLike[str] | str]

class DBCore:
    DBC_ACTION_CODE: ClassVar[str]
    DBC_ACTION_CODE_LAST: ClassVar[str]
    DBC_ACTION_TEXT: ClassVar[str]
    DBC_ACTION_TEXT_LAST: ClassVar[str]
    DBC_ACTIVE: ClassVar[str]
    DBC_CODE_ISO_639_3: ClassVar[str]
    DBC_CODE_ISO_639_3_DEFAULT: ClassVar[str]
    DBC_CODE_PANDOC: ClassVar[str]
    DBC_CODE_PANDOC_DEFAULT: ClassVar[str]
    DBC_CODE_SPACY: ClassVar[str]
    DBC_CODE_TESSERACT: ClassVar[str]
    DBC_CODE_TESSERACT_DEFAULT: ClassVar[str]
    DBC_COLUMN_NO: ClassVar[str]
    DBC_COLUMN_SPAN: ClassVar[str]
    DBC_COORD_LLX: ClassVar[str]
    DBC_COORD_URX: ClassVar[str]
    DBC_CREATED_AT: ClassVar[str]
    DBC_DIRECTORY_NAME: ClassVar[str]
    DBC_DIRECTORY_NAME_INBOX: ClassVar[str]
    DBC_DIRECTORY_TYPE: ClassVar[str]
    DBC_DURATION_NS: ClassVar[str]
    DBC_ERROR_CODE: ClassVar[str]
    DBC_ERROR_CODE_LAST: ClassVar[str]
    DBC_ERROR_MSG: ClassVar[str]
    DBC_ERROR_MSG_LAST: ClassVar[str]
    DBC_ERROR_NO: ClassVar[str]
    DBC_FILE_NAME: ClassVar[str]
    DBC_FILE_SIZE_BYTES: ClassVar[str]
    DBC_ID: ClassVar[str]
    DBC_ID_DOCUMENT: ClassVar[str]
    DBC_ID_LANGUAGE: ClassVar[str]
    DBC_ID_PARENT: ClassVar[str]
    DBC_ID_RUN: ClassVar[str]
    DBC_ID_RUN_LAST: ClassVar[str]
    DBC_ISO_LANGUAGE_NAME: ClassVar[str]
    DBC_ISO_LANGUAGE_NAME_DEFAULT: ClassVar[str]
    DBC_LINE_TYPE: ClassVar[str]
    DBC_MODIFIED_AT: ClassVar[str]
    DBC_NO_CHILDREN: ClassVar[str]
    DBC_NO_LINES_FOOTER: ClassVar[str]
    DBC_NO_LINES_HEADER: ClassVar[str]
    DBC_NO_LINES_TOC: ClassVar[str]
    DBC_NO_LISTS_BULLET: ClassVar[str]
    DBC_NO_LISTS_NUMBER: ClassVar[str]
    DBC_NO_PDF_PAGES: ClassVar[str]
    DBC_NO_TABLES: ClassVar[str]
    DBC_NO_TOKENS_IN_SENT: ClassVar[str]
    DBC_PAGE_DATA: ClassVar[str]
    DBC_PAGE_NO: ClassVar[str]
    DBC_PARA_NO: ClassVar[str]
    DBC_ROW_NO: ClassVar[str]
    DBC_SENT_NO: ClassVar[str]
    DBC_SHA256: ClassVar[str]
    DBC_STATUS: ClassVar[str]
    DBC_TEXT: ClassVar[str]
    DBC_TOKENS: ClassVar[str]
    DBC_TOTAL_ERRONEOUS: ClassVar[str]
    DBC_TOTAL_PROCESSED_OK: ClassVar[str]
    DBC_TOTAL_PROCESSED_TO_BE: ClassVar[str]
    DBC_VERSION: ClassVar[str]
    DBT_ACTION: ClassVar[str]
    DBT_DOCUMENT: ClassVar[str]
    DBT_LANGUAGE: ClassVar[str]
    DBT_RUN: ClassVar[str]
    DBT_TOKEN: ClassVar[str]
    DBT_VERSION: ClassVar[str]
    DB_DIALECT_POSTGRESQL: ClassVar[str]
    JSON_NAME_API_VERSION: str
    JSON_NAME_COLUMN_NAME: str
    JSON_NAME_COLUMN_VALUE: str
    JSON_NAME_DATA: str
    JSON_NAME_ROW: str
    JSON_NAME_ROWS: str
    JSON_NAME_TABLES: str
    JSON_NAME_TABLE_NAME: str

    def __init__(self, is_admin: bool = ...) -> None:
        self._db_current_database = None
        self._db_current_password = None
        self._db_current_user = None
        self._db_driver_conn = None
        self._exist = None
        self.db_orm_engine = None
        self.db_orm_metadata = None
    def _connect_db_admin(self) -> None: ...
    def _connect_db_user(self) -> None: ...
    def _create_database_postgresql(self) -> None: ...
    def _create_db_trigger_created_at(self, table_name: str) -> None: ...
    def _create_db_trigger_function(self, column_name: str) -> None: ...
    def _create_db_trigger_modified_at(self, table_name: str) -> None: ...
    def _create_db_triggers(self, table_names: list[str]) -> None: ...
    def _create_schema(self) -> None: ...
    def _drop_database_postgresql(self) -> None: ...
    def _show_connection_details(self) -> None: ...
    def _upgrade_database_version(self) -> None: ...
    def create_database(self) -> None: ...
    def disconnect_db(self) -> None: ...
    def exists(self) -> bool: ...
    def delete_dbt_id(self, table_name: str, id_where: int) -> None: ...
    def insert_dbt_row(self, table_name: str, columns: Columns) -> int: ...
    def load_db_data_from_json(self, db_initial_data_file: pathlib.Path) -> None: ...
    def update_dbt_id(self, table_name: str, id_where: int, columns: Columns) -> None: ...
    def upgrade_database(self) -> None: ...
