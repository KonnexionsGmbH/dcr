# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module dcr_core.cls_setup.

Managing the application configuration parameters.
"""
from __future__ import annotations

from typing import ClassVar

import dcr_core.core_utils

import dcr


# pylint: disable=too-many-instance-attributes
class Setup(dcr_core.cls_setup.Setup):
    """Managing the application configuration parameters.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    _CONFIG_PARAM_NO = 129

    _DCR_CFG_DB_CONNECTION_PORT: ClassVar[str] = "db_connection_port"
    _DCR_CFG_DB_CONNECTION_PREFIX: ClassVar[str] = "db_connection_prefix"
    _DCR_CFG_DB_CONTAINER_PORT: ClassVar[str] = "db_container_port"
    _DCR_CFG_DB_DATABASE: ClassVar[str] = "db_database"
    _DCR_CFG_DB_DATABASE_ADMIN: ClassVar[str] = "db_database_admin"
    _DCR_CFG_DB_DIALECT: ClassVar[str] = "db_dialect"
    _DCR_CFG_DB_HOST: ClassVar[str] = "db_host"
    _DCR_CFG_DB_INITIAL_DATA_FILE: ClassVar[str] = "db_initial_data_file"
    _DCR_CFG_DB_PASSWORD: ClassVar[str] = "db_password"
    _DCR_CFG_DB_PASSWORD_ADMIN: ClassVar[str] = "db_password_admin"
    _DCR_CFG_DB_SCHEMA: ClassVar[str] = "db_schema"
    _DCR_CFG_DB_USER: ClassVar[str] = "db_user"
    _DCR_CFG_DB_USER_ADMIN: ClassVar[str] = "db_user_admin"
    _DCR_CFG_DELETE_AUXILIARY_FILES: ClassVar[str] = "delete_auxiliary_files"
    _DCR_CFG_DIRECTORY_INBOX_ACCEPTED: ClassVar[str] = "directory_inbox_accepted"
    _DCR_CFG_DIRECTORY_INBOX_REJECTED: ClassVar[str] = "directory_inbox_rejected"
    _DCR_CFG_DOC_ID_IN_FILE_NAME: ClassVar[str] = "doc_id_in_file_name"
    _DCR_CFG_IGNORE_DUPLICATES: ClassVar[str] = "ignore_duplicates"
    _DCR_CFG_SECTION: ClassVar[str] = "dcr"
    _DCR_CFG_SECTION_ENV_TEST: ClassVar[str] = "dcr.env.test"

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        dcr_core.core_glob.logger.debug(dcr_core.core_glob.LOGGER_START)

        super().__init__()

        # -----------------------------------------------------------------------------
        # DCR configuration.
        # -----------------------------------------------------------------------------
        self.db_connection_port = "5432"
        self.db_connection_prefix = "postgresql+psycopg2://"
        self.db_container_port = "5432"
        self.db_database = "dcr_db_prod"
        self.db_database_admin = "dcr_db_prod_admin"
        self.db_dialect = "postgresql"
        self.db_host = "localhost"
        self.db_initial_data_file = dcr_core.core_utils.get_os_independent_name("data/db_initial_data_file.json")
        self.db_password = "postgresql"  # nosec
        self.db_password_admin = "postgresql"  # nosec
        self.db_schema = "dcr_schema"
        self.db_user = "dcr_user"
        self.db_user_admin = "dcr_user_admin"

        self.is_delete_auxiliary_files = True

        self.directory_inbox_accepted = dcr_core.core_utils.get_os_independent_name("data/inbox_accepted")
        self.directory_inbox_rejected = dcr_core.core_utils.get_os_independent_name("data/inbox_rejected")
        self.doc_id_in_file_name = "none"

        self.is_ignore_duplicates = False

        self._load_config()

        # noinspection PyUnresolvedReferences
        dcr.utils.progress_msg_core("The configuration parameters (dcr) are checked and loaded")

        self._exist = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameters.
    # -----------------------------------------------------------------------------
    def _check_config(self) -> None:
        """Check the configuration parameters."""
        self.db_connection_port = self._determine_config_param_integer(Setup._DCR_CFG_DB_CONNECTION_PORT, self.db_connection_port)
        self.db_container_port = self._determine_config_param_integer(Setup._DCR_CFG_DB_CONTAINER_PORT, self.db_container_port)

        self.is_delete_auxiliary_files = self._determine_config_param_boolean(
            Setup._DCR_CFG_DELETE_AUXILIARY_FILES, self.is_delete_auxiliary_files
        )

        self._check_config_directory_inbox_accepted()
        self._check_config_directory_inbox_rejected()
        self._check_config_doc_id_in_file_name()

        self.is_ignore_duplicates = self._determine_config_param_boolean(Setup._DCR_CFG_IGNORE_DUPLICATES, self.is_ignore_duplicates)

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - directory_inbox_accepted.
    # -----------------------------------------------------------------------------
    def _check_config_directory_inbox_accepted(self) -> None:
        """Check the configuration parameter - directory_inbox_accepted."""
        if Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED in self._config:
            self._config[Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED] = str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED])

            self.directory_inbox_accepted = dcr_core.core_utils.get_os_independent_name(
                str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED])
            )
        else:
            dcr_core.core_utils.terminate_fatal(f"Missing configuration parameter '{Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED}'")

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - directory_inbox_rejected.
    # -----------------------------------------------------------------------------
    def _check_config_directory_inbox_rejected(self) -> None:
        """Check the configuration parameter - directory_inbox_rejected."""
        if Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED in self._config:
            self._config[Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED] = str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED])

            self.directory_inbox_rejected = dcr_core.core_utils.get_os_independent_name(
                str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED])
            )
        else:
            dcr_core.core_utils.terminate_fatal(f"Missing configuration parameter '{Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED}'")

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - doc_id_in_file_name.
    # -----------------------------------------------------------------------------
    def _check_config_doc_id_in_file_name(self) -> None:
        """Check the configuration parameter - doc_id_in_file_name."""
        if Setup._DCR_CFG_DOC_ID_IN_FILE_NAME in self._config:
            if str(self._config[Setup._DCR_CFG_DOC_ID_IN_FILE_NAME]).lower() in {"after", "before"}:
                self.doc_id_in_file_name = str(self._config[Setup._DCR_CFG_DOC_ID_IN_FILE_NAME]).lower()

    # -----------------------------------------------------------------------------
    # Load and check the configuration parameters.
    # -----------------------------------------------------------------------------
    def _load_config(self) -> None:
        """Load and check the configuration parameters."""
        for section in self._config_parser.sections():
            if section in (
                Setup._DCR_CFG_SECTION,
                Setup._DCR_CFG_SECTION + ".env." + self.environment_variant,
            ):
                for (key, value) in self._config_parser.items(section):
                    self._config[key] = value

        for key, item in self._config.items():
            match key:
                case (
                    Setup._DCR_CFG_DB_CONNECTION_PORT
                    | Setup._DCR_CFG_DB_CONTAINER_PORT
                    | Setup._DCR_CFG_DELETE_AUXILIARY_FILES
                    | Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED
                    | Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED
                    | Setup._DCR_CFG_DOC_ID_IN_FILE_NAME
                    | Setup._DCR_CFG_IGNORE_DUPLICATES
                ):
                    continue
                case Setup._DCR_CFG_DB_CONNECTION_PREFIX:
                    self.db_connection_prefix = str(item)
                case Setup._DCR_CFG_DB_DATABASE:
                    self.db_database = str(item)
                case Setup._DCR_CFG_DB_DATABASE_ADMIN:
                    self.db_database_admin = str(item)
                case Setup._DCR_CFG_DB_DIALECT:
                    self.db_dialect = str(item)
                case Setup._DCR_CFG_DB_HOST:
                    self.db_host = str(item)
                case Setup._DCR_CFG_DB_INITIAL_DATA_FILE:
                    self.db_initial_data_file = dcr_core.core_utils.get_os_independent_name(item)
                case Setup._DCR_CFG_DB_PASSWORD:
                    self.db_password = str(item)
                case Setup._DCR_CFG_DB_PASSWORD_ADMIN:
                    self.db_password_admin = str(item)
                case Setup._DCR_CFG_DB_SCHEMA:
                    self.db_schema = str(item)
                case Setup._DCR_CFG_DB_USER:
                    self.db_user = str(item)
                case Setup._DCR_CFG_DB_USER_ADMIN:
                    self.db_user_admin = str(item)
                case _:
                    pass

        self._check_config()
