from __future__ import annotations

from typing import ClassVar

import dcr_core.cls_setup
import dcr_core.core_utils

class Setup(dcr_core.cls_setup.Setup):
    _DCR_CFG_DB_CONNECTION_PORT: ClassVar[str]
    _DCR_CFG_DB_CONNECTION_PREFIX: ClassVar[str]
    _DCR_CFG_DB_CONTAINER_PORT: ClassVar[str]
    _DCR_CFG_DB_DATABASE: ClassVar[str]
    _DCR_CFG_DB_DATABASE_ADMIN: ClassVar[str]
    _DCR_CFG_DB_DIALECT: ClassVar[str]
    _DCR_CFG_DB_HOST: ClassVar[str]
    _DCR_CFG_DB_INITIAL_DATA_FILE: ClassVar[str]
    _DCR_CFG_DB_PASSWORD: ClassVar[str]
    _DCR_CFG_DB_PASSWORD_ADMIN: ClassVar[str]
    _DCR_CFG_DB_SCHEMA: ClassVar[str]
    _DCR_CFG_DB_USER: ClassVar[str]
    _DCR_CFG_DB_USER_ADMIN: ClassVar[str]
    _DCR_CFG_DELETE_AUXILIARY_FILES: ClassVar[str]
    _DCR_CFG_DIRECTORY_INBOX: ClassVar[str]
    _DCR_CFG_DIRECTORY_INBOX_ACCEPTED: ClassVar[str]
    _DCR_CFG_DIRECTORY_INBOX_REJECTED: ClassVar[str]
    _DCR_CFG_DOC_ID_IN_FILE_NAME: ClassVar[str]
    _DCR_CFG_IGNORE_DUPLICATES: ClassVar[str]
    _DCR_CFG_SECTION: ClassVar[str]
    _DCR_CFG_SECTION_ENV_TEST: ClassVar[str]

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        self._exist: bool = False
        self.db_connection_port: int = 0
        self.db_connection_prefix: str = ""
        self.db_container_port = 5432
        self.db_database: str = ""
        self.db_database_admin: str = ""
        self.db_dialect: str = ""
        self.db_host: str = ""
        self.db_initial_data_file: str = ""
        self.db_password: str = ""  # nosec
        self.db_password_admin: str = ""  # nosec
        self.db_schema: str = ""
        self.db_user: str = ""
        self.db_user_admin: str = ""
        self.directory_inbox: str = ""
        self.directory_inbox_accepted: str = ""
        self.directory_inbox_rejected: str = ""
        self.doc_id_in_file_name: str = ""
        self.is_delete_auxiliary_files: bool = False
        self.is_ignore_duplicates: bool = False
        ...
    def _check_config(self) -> None: ...
    def _check_config_directory_inbox(self) -> None: ...
    def _check_config_directory_inbox_accepted(self) -> None: ...
    def _check_config_directory_inbox_rejected(self) -> None: ...
    def _check_config_doc_id_in_file_name(self) -> None: ...
    def _load_config(self) -> None: ...
