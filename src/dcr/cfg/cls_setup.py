"""Module cfg.cls_setup: Managing the application configuration parameters."""
from __future__ import annotations

import configparser
import os
from typing import ClassVar

import utils

import dcr_core.utils


# pylint: disable=too-many-instance-attributes
class Setup:
    """Managing the application configuration parameters.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    _CONFIG_PARAM_NO = 28

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
    _DCR_CFG_DIRECTORY_INBOX: ClassVar[str] = "directory_inbox"
    _DCR_CFG_DIRECTORY_INBOX_ACCEPTED: ClassVar[str] = "directory_inbox_accepted"
    _DCR_CFG_DIRECTORY_INBOX_REJECTED: ClassVar[str] = "directory_inbox_rejected"
    _DCR_CFG_DOC_ID_IN_FILE_NAME: ClassVar[str] = "doc_id_in_file_name"
    _DCR_CFG_FILE: ClassVar[str] = "setup.cfg"
    _DCR_CFG_IGNORE_DUPLICATES: ClassVar[str] = "ignore_duplicates"
    _DCR_CFG_JSON_INDENT: ClassVar[str] = "json_indent"
    _DCR_CFG_JSON_SORT_KEYS: ClassVar[str] = "json_sort_keys"
    _DCR_CFG_PDF2IMAGE_TYPE: ClassVar[str] = "pdf2image_type"
    _DCR_CFG_SECTION: ClassVar[str] = "dcr"
    _DCR_CFG_SECTION_ENV_TEST: ClassVar[str] = "dcr.env.test"

    _DCR_CFG_TESSERACT_TIMEOUT: ClassVar[str] = "tesseract_timeout"
    _DCR_CFG_TETML_PAGE: ClassVar[str] = "tetml_page"
    _DCR_CFG_TETML_WORD: ClassVar[str] = "tetml_word"
    _DCR_CFG_TOKENIZE_2_DATABASE: ClassVar[str] = "tokenize_2_database"
    _DCR_CFG_TOKENIZE_2_JSONFILE: ClassVar[str] = "tokenize_2_jsonfile"
    _DCR_CFG_VERBOSE: ClassVar[str] = "verbose"

    _DCR_ENVIRONMENT_TYPE: ClassVar[str] = "DCR_ENVIRONMENT_TYPE"

    DCR_VERSION: ClassVar[str] = "0.9.4"

    ENVIRONMENT_TYPE_DEV: ClassVar[str] = "dev"
    ENVIRONMENT_TYPE_PROD: ClassVar[str] = "prod"
    ENVIRONMENT_TYPE_TEST: ClassVar[str] = "test"

    PDF2IMAGE_TYPE_JPEG: ClassVar[str] = "jpeg"
    PDF2IMAGE_TYPE_PNG: ClassVar[str] = "png"

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        self._get_environment_variant()

        self._config: dict[str, str] = {}

        # -----------------------------------------------------------------------------
        # DCR configuration.
        # -----------------------------------------------------------------------------
        self.db_connection_port = 5432
        self.db_connection_prefix = "postgresql+psycopg2://"
        self.db_container_port = 5432
        self.db_database = "dcr_db_prod"
        self.db_database_admin = "dcr_db_prod_admin"
        self.db_dialect = "postgresql"
        self.db_host = "localhost"
        self.db_initial_data_file = dcr_core.utils.get_os_independent_name("data/db_initial_data_file.json")
        self.db_password = "postgresql"  # nosec
        self.db_password_admin = "postgresql"  # nosec
        self.db_schema = "dcr_schema"
        self.db_user = "dcr_user"
        self.db_user_admin = "dcr_user_admin"

        self.is_delete_auxiliary_files = True

        self.directory_inbox = dcr_core.utils.get_os_independent_name("data/inbox")
        self.directory_inbox_accepted = dcr_core.utils.get_os_independent_name("data/inbox_accepted")
        self.directory_inbox_rejected = dcr_core.utils.get_os_independent_name("data/inbox_rejected")
        self.doc_id_in_file_name = "none"

        self.is_ignore_duplicates = False

        self.json_indent = 4

        self.is_json_sort_keys = False

        self.lt_footer_max_distance = 3
        self.lt_footer_max_lines = 3
        self.lt_header_max_distance = 3
        self.lt_header_max_lines = 3
        self.lt_heading_file_incl_no_ctx = 1

        self.is_lt_heading_file_incl_regexp = False

        self.lt_export_rule_file_heading = "data/lt_export_rule_heading.json"
        self.lt_export_rule_file_list_bullet = "data/lt_export_rule_list_bullet.json"
        self.lt_export_rule_file_list_number = "data/lt_export_rule_list_number.json"
        self.lt_heading_max_level = 3
        self.lt_heading_min_pages = 2
        self.lt_heading_rule_file = "none"
        self.lt_heading_tolerance_llx = 5
        self.lt_list_bullet_min_entries = 2
        self.lt_list_bullet_rule_file = "none"
        self.lt_list_bullet_tolerance_llx = 5

        self.is_lt_list_number_file_incl_regexp = False

        self.lt_list_number_min_entries = 2
        self.lt_list_number_rule_file = "none"
        self.lt_list_number_tolerance_llx = 5

        self.is_lt_table_file_incl_empty_columns = True

        self.lt_toc_last_page = 5
        self.lt_toc_min_entries = 5

        self.pdf2image_type = Setup.PDF2IMAGE_TYPE_JPEG
        self.tesseract_timeout = 10

        self.is_tetml_page = False
        self.is_tetml_word = False

        self.is_tokenize_2_database = True
        self.is_tokenize_2_jsonfile = True
        self.is_verbose = True
        self.is_verbose_lt_headers_footers = False
        self.is_verbose_lt_heading = False
        self.is_verbose_lt_list_bullet = False
        self.is_verbose_lt_list_number = False
        self.is_verbose_lt_table = False
        self.is_verbose_lt_toc = False

        self._load_config()

        utils.progress_msg_core("The configuration parameters are checked and loaded")

        self._exist = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameters.
    # -----------------------------------------------------------------------------
    def _check_config(self) -> None:
        """Check the configuration parameters."""
        self.db_connection_port = self._determine_config_param_integer(Setup._DCR_CFG_DB_CONNECTION_PORT, self.db_connection_port)
        self.db_container_port = self._determine_config_param_integer(Setup._DCR_CFG_DB_CONTAINER_PORT, self.db_container_port)

        self.is_delete_auxiliary_files = self._determine_config_param_boolean(Setup._DCR_CFG_DELETE_AUXILIARY_FILES, self.is_delete_auxiliary_files)

        self._check_config_directory_inbox()
        self._check_config_directory_inbox_accepted()
        self._check_config_directory_inbox_rejected()
        self._check_config_doc_id_in_file_name()

        self.is_ignore_duplicates = self._determine_config_param_boolean(Setup._DCR_CFG_IGNORE_DUPLICATES, self.is_ignore_duplicates)

        self.json_indent = self._determine_config_param_integer(Setup._DCR_CFG_JSON_INDENT, self.json_indent)

        self.is_json_sort_keys = self._determine_config_param_boolean(Setup._DCR_CFG_JSON_SORT_KEYS, self.is_json_sort_keys)

        self._check_config_pdf2image_type()

        self.tesseract_timeout = self._determine_config_param_integer(Setup._DCR_CFG_TESSERACT_TIMEOUT, self.tesseract_timeout)

        self.is_tetml_page = self._determine_config_param_boolean(Setup._DCR_CFG_TETML_PAGE, self.is_tetml_page)
        self.is_tetml_word = self._determine_config_param_boolean(Setup._DCR_CFG_TETML_WORD, self.is_tetml_word)

        self.is_tokenize_2_database = self._determine_config_param_boolean(Setup._DCR_CFG_TOKENIZE_2_DATABASE, self.is_tokenize_2_database)
        self.is_tokenize_2_jsonfile = self._determine_config_param_boolean(Setup._DCR_CFG_TOKENIZE_2_JSONFILE, self.is_tokenize_2_jsonfile)
        if not self.is_tokenize_2_database:
            if not self.is_tokenize_2_jsonfile:
                dcr_core.utils.terminate_fatal(
                    "At least one of the configuration parameters 'tokenize_2_database' or " + "'tokenize_2_jsonfile' must be 'true'"
                )

        self.is_verbose = self._determine_config_param_boolean(Setup._DCR_CFG_VERBOSE, self.is_verbose)

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - directory_inbox.
    # -----------------------------------------------------------------------------
    def _check_config_directory_inbox(self) -> None:
        """Check the configuration parameter - directory_inbox."""
        if Setup._DCR_CFG_DIRECTORY_INBOX in self._config:
            self._config[Setup._DCR_CFG_DIRECTORY_INBOX] = str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX])

            self.directory_inbox = dcr_core.utils.get_os_independent_name(str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX]))
        else:
            dcr_core.utils.terminate_fatal(f"Missing configuration parameter '{Setup._DCR_CFG_DIRECTORY_INBOX}'")

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - directory_inbox_accepted.
    # -----------------------------------------------------------------------------
    def _check_config_directory_inbox_accepted(self) -> None:
        """Check the configuration parameter - directory_inbox_accepted."""
        if Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED in self._config:
            self._config[Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED] = str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED])

            self.directory_inbox_accepted = dcr_core.utils.get_os_independent_name(str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED]))
        else:
            dcr_core.utils.terminate_fatal(f"Missing configuration parameter '{Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED}'")

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - directory_inbox_rejected.
    # -----------------------------------------------------------------------------
    def _check_config_directory_inbox_rejected(self) -> None:
        """Check the configuration parameter - directory_inbox_rejected."""
        if Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED in self._config:
            self._config[Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED] = str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED])

            self.directory_inbox_rejected = dcr_core.utils.get_os_independent_name(str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED]))
        else:
            dcr_core.utils.terminate_fatal(f"Missing configuration parameter '{Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED}'")

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - doc_id_in_file_name.
    # -----------------------------------------------------------------------------
    def _check_config_doc_id_in_file_name(self) -> None:
        """Check the configuration parameter - doc_id_in_file_name."""
        if Setup._DCR_CFG_DOC_ID_IN_FILE_NAME in self._config:
            if str(self._config[Setup._DCR_CFG_DOC_ID_IN_FILE_NAME]).lower() in {"after", "before"}:
                self.doc_id_in_file_name = str(self._config[Setup._DCR_CFG_DOC_ID_IN_FILE_NAME]).lower()

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - pdf2image_type.
    # -----------------------------------------------------------------------------
    def _check_config_pdf2image_type(self) -> None:
        """Check the configuration parameter - pdf2image_type."""
        if Setup._DCR_CFG_PDF2IMAGE_TYPE in self._config:
            self.pdf2image_type = str(self._config[Setup._DCR_CFG_PDF2IMAGE_TYPE])
            if self.pdf2image_type not in [
                Setup.PDF2IMAGE_TYPE_JPEG,
                Setup.PDF2IMAGE_TYPE_PNG,
            ]:
                dcr_core.utils.terminate_fatal(f"Invalid configuration parameter value for parameter " f"'pdf2image_type': '{self.pdf2image_type}'")

    # -----------------------------------------------------------------------------
    # Determine a boolean configuration parameter.
    # -----------------------------------------------------------------------------
    def _determine_config_param_boolean(
        self,
        param: str,
        var: bool,
    ) -> bool:
        """Determine a boolean configuration parameter.

        Args:
            param (str): Parameter name.
            var (bool): Default parameter value.

        Returns:
            bool: Specified value.
        """
        if var and param in self._config:
            if str(self._config[param]).lower() == "false":
                return False
        elif not var and param in self._config:
            if str(self._config[param]).lower() == "true":
                return True

        return var

    # -----------------------------------------------------------------------------
    # Determine a integer configuration parameter.
    # -----------------------------------------------------------------------------
    def _determine_config_param_integer(
        self,
        param: str,
        var: int,
    ) -> int:
        """Determine a integer configuration parameter.

        Args:
            param (str): Parameter name.
            var (int): Default parameter value.

        Returns:
            int: Specified value.
        """
        if param in self._config:
            return int(str(self._config[param]))

        return var

    # -----------------------------------------------------------------------------
    # Determine and check the environment variant.
    # -----------------------------------------------------------------------------
    def _get_environment_variant(self) -> None:
        """Determine and check the environment variant."""
        self.environment_variant = Setup.ENVIRONMENT_TYPE_PROD

        try:
            self.environment_variant = os.environ[Setup._DCR_ENVIRONMENT_TYPE]
        except KeyError:
            dcr_core.utils.terminate_fatal(f"The environment variable '{Setup._DCR_ENVIRONMENT_TYPE}' is missing")

        if self.environment_variant not in [
            Setup.ENVIRONMENT_TYPE_DEV,
            Setup.ENVIRONMENT_TYPE_PROD,
            Setup.ENVIRONMENT_TYPE_TEST,
        ]:
            dcr_core.utils.terminate_fatal(
                f"The environment variable '{Setup._DCR_ENVIRONMENT_TYPE}' " f"has the invalid content '{self.environment_variant}'"
            )

    # -----------------------------------------------------------------------------
    # Load and check the configuration parameters.
    # -----------------------------------------------------------------------------
    def _load_config(self) -> None:
        """Load and check the configuration parameters."""
        config_parser = configparser.ConfigParser()
        config_parser.read(Setup._DCR_CFG_FILE)

        for section in config_parser.sections():
            if section in (
                Setup._DCR_CFG_SECTION,
                Setup._DCR_CFG_SECTION + ".env." + self.environment_variant,
            ):
                for (key, value) in config_parser.items(section):
                    self._config[key] = value

        for key, item in self._config.items():
            match key:
                case (
                    Setup._DCR_CFG_DB_CONNECTION_PORT
                    | Setup._DCR_CFG_DB_CONTAINER_PORT
                    | Setup._DCR_CFG_DELETE_AUXILIARY_FILES
                    | Setup._DCR_CFG_DIRECTORY_INBOX
                    | Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED
                    | Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED
                    | Setup._DCR_CFG_DOC_ID_IN_FILE_NAME
                    | Setup._DCR_CFG_IGNORE_DUPLICATES
                    | Setup._DCR_CFG_JSON_INDENT
                    | Setup._DCR_CFG_JSON_SORT_KEYS
                    | Setup._DCR_CFG_PDF2IMAGE_TYPE
                    | Setup._DCR_CFG_TESSERACT_TIMEOUT
                    | Setup._DCR_CFG_TETML_PAGE
                    | Setup._DCR_CFG_TETML_WORD
                    | Setup._DCR_CFG_TOKENIZE_2_DATABASE
                    | Setup._DCR_CFG_TOKENIZE_2_JSONFILE
                    | Setup._DCR_CFG_VERBOSE
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
                    self.db_initial_data_file = dcr_core.utils.get_os_independent_name(item)
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
                    dcr_core.utils.terminate_fatal(f"dcr: unknown configuration parameter '{key}'")

        self._check_config()

    # -----------------------------------------------------------------------------
    # Check the object existence.
    # -----------------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns:
            bool:   Always true
        """
        return self._exist
