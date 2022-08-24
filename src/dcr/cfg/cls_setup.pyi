# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from __future__ import annotations

import dcr_core.cls_setup
import dcr_core.core_utils

class Setup(dcr_core.cls_setup.Setup):
    _DCR_CFG_DB_CONNECTION_PORT: str
    _DCR_CFG_DB_CONNECTION_PREFIX: str
    _DCR_CFG_DB_CONTAINER_PORT: str
    _DCR_CFG_DB_DATABASE: str
    _DCR_CFG_DB_DATABASE_ADMIN: str
    _DCR_CFG_DB_DIALECT: str
    _DCR_CFG_DB_HOST: str
    _DCR_CFG_DB_INITIAL_DATA_FILE: str
    _DCR_CFG_DB_PASSWORD: str
    _DCR_CFG_DB_PASSWORD_ADMIN: str
    _DCR_CFG_DB_SCHEMA: str
    _DCR_CFG_DB_USER: str
    _DCR_CFG_DB_USER_ADMIN: str
    _DCR_CFG_DELETE_AUXILIARY_FILES: str
    _DCR_CFG_DIRECTORY_INBOX_ACCEPTED: str
    _DCR_CFG_DIRECTORY_INBOX_REJECTED: str
    _DCR_CFG_DOC_ID_IN_FILE_NAME: str
    _DCR_CFG_IGNORE_DUPLICATES: str

    def __init__(self) -> None:
        self.db_connection_port = None
        self.db_connection_prefix: str
        self.db_container_port = None
        self.db_database: str
        self.db_database_admin: str
        self.db_dialect: str
        self.db_host: str
        self.db_initial_data_file: str
        self.db_password: str
        self.db_password_admin: str
        self.db_schema: str
        self.db_user: str
        self.db_user_admin: str
        self.directory_inbox_accepted: str
        self.directory_inbox_rejected: str
        self.doc_id_in_file_name: str
        self.is_delete_auxiliary_files: bool
        self.is_ignore_duplicates = None
    def _check_config(self) -> None: ...
    def _check_config_directory_inbox_accepted(self) -> None: ...
    def _check_config_directory_inbox_rejected(self) -> None: ...
    def _check_config_doc_id_in_file_name(self) -> None: ...
    def _load_config(self) -> None: ...
