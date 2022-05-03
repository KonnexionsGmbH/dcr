"""Module cfg.Setup: Managing the application configuration parameters."""
import configparser
import os
import typing

import cfg.glob
import utils


# pylint: disable=R0902
# pylint: disable=R0903
class Setup:
    """Managing the application configuration parameters.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    _DCR_CFG_DB_CONNECTION_PORT: typing.ClassVar[str] = "db_connection_port"
    _DCR_CFG_DB_CONNECTION_PREFIX: typing.ClassVar[str] = "db_connection_prefix"
    _DCR_CFG_DB_CONTAINER_PORT: typing.ClassVar[str] = "db_container_port"
    _DCR_CFG_DB_DATABASE: typing.ClassVar[str] = "db_database"
    _DCR_CFG_DB_DATABASE_ADMIN: typing.ClassVar[str] = "db_database_admin"
    _DCR_CFG_DB_DIALECT: typing.ClassVar[str] = "db_dialect"
    _DCR_CFG_DB_HOST: typing.ClassVar[str] = "db_host"
    _DCR_CFG_DB_PASSWORD: typing.ClassVar[str] = "db_password"
    _DCR_CFG_DB_PASSWORD_ADMIN: typing.ClassVar[str] = "db_password_admin"
    _DCR_CFG_DB_SCHEMA: typing.ClassVar[str] = "db_schema"
    _DCR_CFG_DB_USER: typing.ClassVar[str] = "db_user"
    _DCR_CFG_DB_USER_ADMIN: typing.ClassVar[str] = "db_user_admin"
    _DCR_CFG_DCR_VERSION: typing.ClassVar[str] = "dcr_version"
    _DCR_CFG_DELETE_AUXILIARY_FILES: typing.ClassVar[str] = "delete_auxiliary_files"
    _DCR_CFG_DIRECTORY_INBOX: typing.ClassVar[str] = "directory_inbox"
    _DCR_CFG_DIRECTORY_INBOX_ACCEPTED: typing.ClassVar[str] = "directory_inbox_accepted"
    _DCR_CFG_DIRECTORY_INBOX_REJECTED: typing.ClassVar[str] = "directory_inbox_rejected"
    _DCR_CFG_FILE: typing.ClassVar[str] = "setup.cfg"
    _DCR_CFG_IGNORE_DUPLICATES: typing.ClassVar[str] = "ignore_duplicates"
    _DCR_CFG_INITIAL_DATABASE_DATA: typing.ClassVar[str] = "initial_database_data"
    _DCR_CFG_LINE_FOOTER_MAX_DISTANCE: typing.ClassVar[str] = "line_footer_max_distance"
    _DCR_CFG_LINE_FOOTER_MAX_LINES: typing.ClassVar[str] = "line_footer_max_lines"
    _DCR_CFG_LINE_FOOTER_PREFERENCE: typing.ClassVar[str] = "line_footer_preference"
    _DCR_CFG_LINE_HEADER_MAX_DISTANCE: typing.ClassVar[str] = "line_header_max_distance"
    _DCR_CFG_LINE_HEADER_MAX_LINES: typing.ClassVar[str] = "line_header_max_lines"
    _DCR_CFG_PDF2IMAGE_TYPE: typing.ClassVar[str] = "pdf2image_type"
    _DCR_CFG_SECTION: typing.ClassVar[str] = "dcr"
    _DCR_CFG_SECTION_DEV: typing.ClassVar[str] = "dcr_dev"
    _DCR_CFG_SECTION_PROD: typing.ClassVar[str] = "dcr_prod"
    _DCR_CFG_SECTION_TEST: typing.ClassVar[str] = "dcr_test"
    _DCR_CFG_SIMULATE_PARSER: typing.ClassVar[str] = "simulate_parser"
    _DCR_CFG_SPACY_TKN_ATTR_DEP_: typing.ClassVar[str] = "spacy_tkn_attr_dep_"
    _DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_: typing.ClassVar[str] = "spacy_tkn_attr_ent_iob_"
    _DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_: typing.ClassVar[str] = "spacy_tkn_attr_ent_kb_id_"
    _DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_: typing.ClassVar[str] = "spacy_tkn_attr_ent_type_"
    _DCR_CFG_SPACY_TKN_ATTR_I: typing.ClassVar[str] = "spacy_tkn_attr_i"
    _DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA: typing.ClassVar[str] = "spacy_tkn_attr_is_alpha"
    _DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY: typing.ClassVar[str] = "spacy_tkn_attr_is_currency"
    _DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT: typing.ClassVar[str] = "spacy_tkn_attr_is_digit"
    _DCR_CFG_SPACY_TKN_ATTR_IS_OOV: typing.ClassVar[str] = "spacy_tkn_attr_is_oov"
    _DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT: typing.ClassVar[str] = "spacy_tkn_attr_is_punct"
    _DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END: typing.ClassVar[str] = "spacy_tkn_attr_is_sent_end"
    _DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START: typing.ClassVar[str] = "spacy_tkn_attr_is_sent_start"
    _DCR_CFG_SPACY_TKN_ATTR_IS_STOP: typing.ClassVar[str] = "spacy_tkn_attr_is_stop"
    _DCR_CFG_SPACY_TKN_ATTR_IS_TITLE: typing.ClassVar[str] = "spacy_tkn_attr_is_title"
    _DCR_CFG_SPACY_TKN_ATTR_LANG_: typing.ClassVar[str] = "spacy_tkn_attr_lang_"
    _DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE: typing.ClassVar[str] = "spacy_tkn_attr_left_edge"
    _DCR_CFG_SPACY_TKN_ATTR_LEMMA_: typing.ClassVar[str] = "spacy_tkn_attr_lemma_"
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL: typing.ClassVar[str] = "spacy_tkn_attr_like_email"
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM: typing.ClassVar[str] = "spacy_tkn_attr_like_num"
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_URL: typing.ClassVar[str] = "spacy_tkn_attr_like_url"
    _DCR_CFG_SPACY_TKN_ATTR_NORM_: typing.ClassVar[str] = "spacy_tkn_attr_norm_"
    _DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE: typing.ClassVar[str] = "spacy_tkn_attr_right_edge"
    _DCR_CFG_SPACY_TKN_ATTR_SHAPE_: typing.ClassVar[str] = "spacy_tkn_attr_shape_"
    _DCR_CFG_SPACY_TKN_ATTR_TEXT: typing.ClassVar[str] = "spacy_tkn_attr_text"
    _DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS: typing.ClassVar[str] = "spacy_tkn_attr_text_with_ws"
    _DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_: typing.ClassVar[str] = "spacy_tkn_attr_whitespace_"
    _DCR_CFG_TESSERACT_TIMEOUT: typing.ClassVar[str] = "tesseract_timeout"
    _DCR_CFG_TETML_LINE: typing.ClassVar[str] = "tetml_line"
    _DCR_CFG_TETML_PAGE: typing.ClassVar[str] = "tetml_page"
    _DCR_CFG_TETML_WORD: typing.ClassVar[str] = "tetml_word"
    _DCR_CFG_VERBOSE: typing.ClassVar[str] = "verbose"
    _DCR_CFG_VERBOSE_LINE_TYPE: typing.ClassVar[str] = "verbose_line_type"
    _DCR_CFG_VERBOSE_PARSER: typing.ClassVar[str] = "verbose_parser"

    _DCR_ENVIRONMENT_TYPE: typing.ClassVar[str] = "DCR_ENVIRONMENT_TYPE"

    _ENVIRONMENT_TYPE_DEV: typing.ClassVar[str] = "dev"
    _ENVIRONMENT_TYPE_PROD: typing.ClassVar[str] = "prod"
    _ENVIRONMENT_TYPE_TEST: typing.ClassVar[str] = "test"

    PDF2IMAGE_TYPE_JPEG: typing.ClassVar[str] = "jpeg"
    PDF2IMAGE_TYPE_PNG: typing.ClassVar[str] = "png"

    # -----------------------------------------------------------------------------
    # Initialise and load the application configuration parameters.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:  # pylint: disable=too-many-statements
        """Initialise and load the application configuration parameters."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._get_environment_variant()

        self._config: typing.Dict[str, str] = {}

        self.db_connection_port: str = ""
        self.db_connection_prefix: str = "postgresql+psycopg2://"
        self.db_container_port: str = ""
        self.db_database: str = ""
        self.db_database_admin: str = ""
        self.db_dialect: str = "postgresql"
        self.db_host: str = "localhost"
        self.db_password: str | None = None
        self.db_password_admin: str | None = None
        self.db_schema: str = "dcr_schema"
        self.db_user: str = "postgresql"
        self.db_user_admin: str = "postgresql"
        self.dcr_version: str = "0.9.1"
        self.directory_inbox: str = "data/inbox"
        self.directory_inbox_accepted: str = "data/inbox_accepted"
        self.directory_inbox_rejected: str = "data/inbox_rejected"
        self.initial_database_data: str = "data/initial_database_data.json"
        self.is_delete_auxiliary_files: bool = True
        self.is_ignore_duplicates: bool = False
        self.is_line_footer_preferred: bool = True
        self.is_simulate_parser: bool = False
        self.is_spacy_tkn_attr_dep_: bool = False
        self.is_spacy_tkn_attr_ent_iob_: bool = False
        self.is_spacy_tkn_attr_ent_kb_id_: bool = False
        self.is_spacy_tkn_attr_ent_type_: bool = True
        self.is_spacy_tkn_attr_i: bool = True
        self.is_spacy_tkn_attr_is_alpha: bool = False
        self.is_spacy_tkn_attr_is_currency: bool = True
        self.is_spacy_tkn_attr_is_digit: bool = True
        self.is_spacy_tkn_attr_is_oov: bool = True
        self.is_spacy_tkn_attr_is_punct: bool = True
        self.is_spacy_tkn_attr_is_sent_end: bool = False
        self.is_spacy_tkn_attr_is_sent_start: bool = False
        self.is_spacy_tkn_attr_is_stop: bool = True
        self.is_spacy_tkn_attr_is_title: bool = True
        self.is_spacy_tkn_attr_lang_: bool = False
        self.is_spacy_tkn_attr_left_edge: bool = False
        self.is_spacy_tkn_attr_lemma_: bool = True
        self.is_spacy_tkn_attr_like_email: bool = True
        self.is_spacy_tkn_attr_like_num: bool = True
        self.is_spacy_tkn_attr_like_url: bool = True
        self.is_spacy_tkn_attr_norm_: bool = True
        self.is_spacy_tkn_attr_right_edge: bool = False
        self.is_spacy_tkn_attr_shape_: bool = False
        self.is_spacy_tkn_attr_text: bool = True
        self.is_spacy_tkn_attr_text_with_ws: bool = False
        self.is_spacy_tkn_attr_whitespace_: bool = True
        self.is_tetml_line: bool = True
        self.is_tetml_page: bool = False
        self.is_tetml_word: bool = False
        self.is_verbose: bool = True
        self.is_verbose_line_type: bool = False
        self.line_footer_max_distance: int = 3
        self.line_footer_max_lines: int = 3
        self.line_header_max_distance: int = 3
        self.line_header_max_lines: int = 3
        self.pdf2image_type: str = Setup.PDF2IMAGE_TYPE_JPEG
        self.tesseract_timeout: int = 10
        self.verbose_parser: str = "none"

        self._load_config()  # pylint: disable=E1121

        utils.progress_msg_core("The configuration parameters are checked and loaded")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Check the configuration parameters.
    # -----------------------------------------------------------------------------
    def _check_config(self) -> None:
        """Check the configuration parameters."""
        self._check_config_delete_auxiliary_files()
        self._check_config_directory_inbox()
        self._check_config_directory_inbox_accepted()
        self._check_config_directory_inbox_rejected()
        self._check_config_ignore_duplicates()
        self._check_config_line_footer_preference()
        self._check_config_pdf2image_type()
        self._check_config_simulate_parser()
        self._check_config_spacy_tkn_attr_dep_()
        self._check_config_spacy_tkn_attr_ent_iob_()
        self._check_config_spacy_tkn_attr_ent_kb_id_()
        self._check_config_spacy_tkn_attr_ent_type_()
        self._check_config_spacy_tkn_attr_i()
        self._check_config_spacy_tkn_attr_is_alpha()
        self._check_config_spacy_tkn_attr_is_currency()
        self._check_config_spacy_tkn_attr_is_digit()
        self._check_config_spacy_tkn_attr_is_oov()
        self._check_config_spacy_tkn_attr_is_punct()
        self._check_config_spacy_tkn_attr_is_sent_end()
        self._check_config_spacy_tkn_attr_is_sent_start()
        self._check_config_spacy_tkn_attr_is_stop()
        self._check_config_spacy_tkn_attr_is_title()
        self._check_config_spacy_tkn_attr_lang_()
        self._check_config_spacy_tkn_attr_left_edge()
        self._check_config_spacy_tkn_attr_lemma_()
        self._check_config_spacy_tkn_attr_like_email()
        self._check_config_spacy_tkn_attr_like_num()
        self._check_config_spacy_tkn_attr_like_url()
        self._check_config_spacy_tkn_attr_norm_()
        self._check_config_spacy_tkn_attr_right_edge()
        self._check_config_spacy_tkn_attr_shape_()
        self._check_config_spacy_tkn_attr_text()
        self._check_config_spacy_tkn_attr_text_with_ws()
        self._check_config_spacy_tkn_attr_whitespace_()
        self._check_config_tesseract_timeout()
        self._check_config_tetml_line()
        self._check_config_tetml_page()
        self._check_config_tetml_word()
        self._check_config_verbose()
        self._check_config_verbose_line_type()
        self._check_config_verbose_parser()

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - delete_auxiliary_files.
    # -----------------------------------------------------------------------------
    def _check_config_delete_auxiliary_files(self) -> None:
        """Check the configuration parameter - delete_auxiliary_files."""
        if Setup._DCR_CFG_DELETE_AUXILIARY_FILES in self._config:
            if str(self._config[Setup._DCR_CFG_DELETE_AUXILIARY_FILES]).lower() == "false":
                self.is_delete_auxiliary_files = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - directory_inbox.
    # -----------------------------------------------------------------------------
    def _check_config_directory_inbox(self) -> None:
        """Check the configuration parameter - directory_inbox."""
        if Setup._DCR_CFG_DIRECTORY_INBOX in self._config:
            self._config[Setup._DCR_CFG_DIRECTORY_INBOX] = str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX])

            self.directory_inbox = str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX])
        else:
            utils.terminate_fatal_setup(f"Missing configuration parameter '{Setup._DCR_CFG_DIRECTORY_INBOX}'")

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - directory_inbox_accepted.
    # -----------------------------------------------------------------------------
    def _check_config_directory_inbox_accepted(self) -> None:
        """Check the configuration parameter - directory_inbox_accepted."""
        if Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED in self._config:
            self._config[Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED] = str(
                self._config[Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED]
            )

            self.directory_inbox_accepted = str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED])
        else:
            utils.terminate_fatal_setup(f"Missing configuration parameter '{Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED}'")

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - directory_inbox_rejected.
    # -----------------------------------------------------------------------------
    def _check_config_directory_inbox_rejected(self) -> None:
        """Check the configuration parameter - directory_inbox_rejected."""
        if Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED in self._config:
            self._config[Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED] = str(
                self._config[Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED]
            )

            self.directory_inbox_rejected = str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED])
        else:
            utils.terminate_fatal_setup(f"Missing configuration parameter '{Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED}'")

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - ignore_duplicates.
    # -----------------------------------------------------------------------------
    def _check_config_ignore_duplicates(self) -> None:
        """Check the configuration parameter - ignore_duplicates."""
        if Setup._DCR_CFG_IGNORE_DUPLICATES in self._config:
            if str(self._config[Setup._DCR_CFG_IGNORE_DUPLICATES]).lower() == "true":
                self.is_ignore_duplicates = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - line_footer_preference.
    # -----------------------------------------------------------------------------
    def _check_config_line_footer_preference(self) -> None:
        """Check the configuration parameter - line_footer_preference."""
        if Setup._DCR_CFG_LINE_FOOTER_PREFERENCE in self._config:
            if str(self._config[Setup._DCR_CFG_LINE_FOOTER_PREFERENCE]).lower() == "false":
                self.is_line_footer_preferred = False

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
                utils.terminate_fatal_setup(
                    f"Invalid configuration parameter value for parameter " f"'pdf2image_type': '{self.pdf2image_type}'"
                )

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - simulate_parser.
    # -----------------------------------------------------------------------------
    def _check_config_simulate_parser(self) -> None:
        """Check the configuration parameter - simulate_parser."""
        if Setup._DCR_CFG_SIMULATE_PARSER in self._config:
            if str(self._config[Setup._DCR_CFG_SIMULATE_PARSER]).lower() == "true":
                self.is_simulate_parser = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_dep_.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_dep_(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_dep_."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_DEP_ in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_DEP_]).lower() == "true":
                self.is_spacy_tkn_attr_dep_ = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_ent_iob_.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_ent_iob_(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_ent_iob_."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_ in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_]).lower() == "true":
                self.is_spacy_tkn_attr_ent_iob_ = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_ent_kb_id_.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_ent_kb_id_(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_ent_kb_id_."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_ in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_]).lower() == "true":
                self.is_spacy_tkn_attr_ent_kb_id_ = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - ent_type_.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_ent_type_(self) -> None:
        """Check the configuration parameter - ent_type_."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_ in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_]).lower() == "false":
                self.is_spacy_tkn_attr_ent_type_ = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - i.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_i(self) -> None:
        """Check the configuration parameter - i."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_I in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_I]).lower() == "false":
                self.is_spacy_tkn_attr_i = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_is_alpha.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_is_alpha(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_is_alpha."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA]).lower() == "true":
                self.is_spacy_tkn_attr_is_alpha = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - is_currency.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_is_currency(self) -> None:
        """Check the configuration parameter - is_currency."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY]).lower() == "false":
                self.is_spacy_tkn_attr_is_currency = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - is_digit.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_is_digit(self) -> None:
        """Check the configuration parameter - is_digit."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT]).lower() == "false":
                self.is_spacy_tkn_attr_is_digit = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - is_oov.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_is_oov(self) -> None:
        """Check the configuration parameter - is_oov."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_IS_OOV in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_IS_OOV]).lower() == "false":
                self.is_spacy_tkn_attr_is_oov = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - is_punct.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_is_punct(self) -> None:
        """Check the configuration parameter - is_punct."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT]).lower() == "false":
                self.is_spacy_tkn_attr_is_punct = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_is_sent_end.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_is_sent_end(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_is_sent_end."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END]).lower() == "true":
                self.is_spacy_tkn_attr_is_sent_end = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_is_sent_start.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_is_sent_start(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_is_sent_start."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START]).lower() == "true":
                self.is_spacy_tkn_attr_is_sent_start = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - is_stop.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_is_stop(self) -> None:
        """Check the configuration parameter - is_stop."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_IS_STOP in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_IS_STOP]).lower() == "false":
                self.is_spacy_tkn_attr_is_stop = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - is_title.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_is_title(self) -> None:
        """Check the configuration parameter - is_title."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_IS_TITLE in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_IS_TITLE]).lower() == "false":
                self.is_spacy_tkn_attr_is_title = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_lang_.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_lang_(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_lang_."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_LANG_ in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_LANG_]).lower() == "true":
                self.is_spacy_tkn_attr_lang_ = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_left_edge.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_left_edge(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_left_edge."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE]).lower() == "true":
                self.is_spacy_tkn_attr_left_edge = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - lemma_.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_lemma_(self) -> None:
        """Check the configuration parameter - lemma_."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_LEMMA_ in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_LEMMA_]).lower() == "false":
                self.is_spacy_tkn_attr_lemma_ = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - like_email.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_like_email(self) -> None:
        """Check the configuration parameter - like_email."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL]).lower() == "false":
                self.is_spacy_tkn_attr_like_email = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - like_num.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_like_num(self) -> None:
        """Check the configuration parameter - like_num."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM]).lower() == "false":
                self.is_spacy_tkn_attr_like_num = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - like_url.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_like_url(self) -> None:
        """Check the configuration parameter - like_url."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_URL in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_URL]).lower() == "false":
                self.is_spacy_tkn_attr_like_url = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - norm_.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_norm_(self) -> None:
        """Check the configuration parameter - norm_."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_NORM_ in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_NORM_]).lower() == "false":
                self.is_spacy_tkn_attr_norm_ = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_right_edge.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_right_edge(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_right_edge."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE]).lower() == "true":
                self.is_spacy_tkn_attr_right_edge = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_shape_.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_shape_(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_shape_."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_ in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_]).lower() == "true":
                self.is_spacy_tkn_attr_shape_ = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - text.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_text(self) -> None:
        """Check the configuration parameter - text."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT]).lower() == "false":
                self.is_spacy_tkn_attr_text = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - whitespace_.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_whitespace_(self) -> None:
        """Check the configuration parameter - whitespace_."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_ in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_]).lower() == "false":
                self.is_spacy_tkn_attr_whitespace_ = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - spacy_tkn_attr_text_with_ws.
    # -----------------------------------------------------------------------------
    def _check_config_spacy_tkn_attr_text_with_ws(self) -> None:
        """Check the configuration parameter - spacy_tkn_attr_text_with_ws."""
        if Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS in self._config:
            if str(self._config[Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS]).lower() == "true":
                self.is_spacy_tkn_attr_text_with_ws = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - tesseract_timeout.
    # -----------------------------------------------------------------------------
    def _check_config_tesseract_timeout(self) -> None:
        """Check the configuration parameter - tesseract_timeout."""
        if Setup._DCR_CFG_TESSERACT_TIMEOUT in self._config:
            self.tesseract_timeout = int(str(self._config[Setup._DCR_CFG_TESSERACT_TIMEOUT]))

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - tetml_line.
    # -----------------------------------------------------------------------------
    def _check_config_tetml_line(self) -> None:
        """Check the configuration parameter - tetml_line."""
        if Setup._DCR_CFG_TETML_LINE in self._config:
            if str(self._config[Setup._DCR_CFG_TETML_LINE]).lower() == "false":
                self.is_tetml_line = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - tetml_page.
    # -----------------------------------------------------------------------------
    def _check_config_tetml_page(self) -> None:
        """Check the configuration parameter - tetml_page."""
        if Setup._DCR_CFG_TETML_PAGE in self._config:
            if str(self._config[Setup._DCR_CFG_TETML_PAGE]).lower() == "true":
                self.is_tetml_page = True

        if not self.is_tetml_page:
            if not self.is_tetml_line:
                utils.terminate_fatal_setup(
                    "At least one of the configuration parameters 'tetml_line' or " + "'tetml_page' must be 'true'"
                )

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - tetml_word.
    # -----------------------------------------------------------------------------
    def _check_config_tetml_word(self) -> None:
        """Check the configuration parameter - tetml_word."""
        if Setup._DCR_CFG_TETML_WORD in self._config:
            if str(self._config[Setup._DCR_CFG_TETML_WORD]).lower() == "true":
                self.is_tetml_word = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - verbose.
    # -----------------------------------------------------------------------------
    def _check_config_verbose(self) -> None:
        """Check the configuration parameter - verbose."""
        if Setup._DCR_CFG_VERBOSE in self._config:
            if str(self._config[Setup._DCR_CFG_VERBOSE]).lower() == "false":
                self.is_verbose = False

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - verbose_line_type.
    # -----------------------------------------------------------------------------
    def _check_config_verbose_line_type(self) -> None:
        """Check the configuration parameter - verbose_line_type."""
        if Setup._DCR_CFG_VERBOSE_LINE_TYPE in self._config:
            if str(self._config[Setup._DCR_CFG_VERBOSE_LINE_TYPE]).lower() == "true":
                self.is_verbose_line_type = True

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - verbose_parser.
    # -----------------------------------------------------------------------------
    def _check_config_verbose_parser(self) -> None:
        """Check the configuration parameter - verbose_parser."""
        if Setup._DCR_CFG_VERBOSE_PARSER in self._config:
            if str(self._config[Setup._DCR_CFG_VERBOSE_PARSER]).lower() in ["all", "text"]:
                self.verbose_parser = str(self._config[Setup._DCR_CFG_VERBOSE_PARSER]).lower()

    # -----------------------------------------------------------------------------
    # Determine and check the environment variant.
    # -----------------------------------------------------------------------------
    def _get_environment_variant(self) -> None:
        """Determine and check the environment variant."""
        self.environment_variant = Setup._ENVIRONMENT_TYPE_PROD

        try:
            self.environment_variant = os.environ[Setup._DCR_ENVIRONMENT_TYPE]
        except KeyError:
            utils.terminate_fatal_setup(f"The environment variable '{Setup._DCR_ENVIRONMENT_TYPE}' is missing")

        if self.environment_variant not in [
            Setup._ENVIRONMENT_TYPE_DEV,
            Setup._ENVIRONMENT_TYPE_PROD,
            Setup._ENVIRONMENT_TYPE_TEST,
        ]:
            utils.terminate_fatal_setup(
                f"The environment variable '{Setup._DCR_ENVIRONMENT_TYPE}' "
                f"has the invalid content '{self.environment_variant}'"
            )

        utils.progress_msg_core(f"The run is performed in the environment '{self.environment_variant}'")

    # -----------------------------------------------------------------------------
    # Load and check the configuration parameters.
    # -----------------------------------------------------------------------------
    def _load_config(self) -> None:
        """Load and check the configuration parameters."""
        config_parser = configparser.ConfigParser()
        config_parser.read(Setup._DCR_CFG_FILE)

        for section in config_parser.sections():
            if section == Setup._DCR_CFG_SECTION:
                for (key, value) in config_parser.items(section):
                    self._config[key] = value

        for section in config_parser.sections():
            if section == Setup._DCR_CFG_SECTION + "_" + self.environment_variant:
                for (key, value) in config_parser.items(section):
                    self._config[key] = value

        for key, item in self._config.items():
            match key:
                case Setup._DCR_CFG_DB_CONNECTION_PORT:
                    self.db_connection_port = str(item)
                case Setup._DCR_CFG_DB_CONNECTION_PREFIX:
                    self.db_connection_prefix = str(item)
                case Setup._DCR_CFG_DB_CONTAINER_PORT:
                    self.db_container_port = str(item)
                case Setup._DCR_CFG_DB_DATABASE:
                    self.db_database = str(item)
                case Setup._DCR_CFG_DB_DATABASE_ADMIN:
                    self.db_database_admin = str(item)
                case Setup._DCR_CFG_DB_DIALECT:
                    self.db_dialect = str(item)
                case Setup._DCR_CFG_DB_HOST:
                    self.db_host = str(item)
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
                case Setup._DCR_CFG_DCR_VERSION:
                    self.dcr_version = str(item)
                case (
                    Setup._DCR_CFG_DELETE_AUXILIARY_FILES
                    | Setup._DCR_CFG_DIRECTORY_INBOX
                    | Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED
                    | Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED
                    | Setup._DCR_CFG_IGNORE_DUPLICATES
                    | Setup._DCR_CFG_LINE_FOOTER_PREFERENCE
                    | Setup._DCR_CFG_PDF2IMAGE_TYPE
                    | Setup._DCR_CFG_SIMULATE_PARSER
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_DEP_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_I
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_OOV
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_STOP
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_TITLE
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LANG_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LEMMA_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_URL
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_NORM_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_
                    | Setup._DCR_CFG_TESSERACT_TIMEOUT
                    | Setup._DCR_CFG_TETML_LINE
                    | Setup._DCR_CFG_TETML_PAGE
                    | Setup._DCR_CFG_TETML_WORD
                    | Setup._DCR_CFG_VERBOSE
                    | Setup._DCR_CFG_VERBOSE_LINE_TYPE
                    | Setup._DCR_CFG_VERBOSE_PARSER
                ):
                    continue
                case Setup._DCR_CFG_INITIAL_DATABASE_DATA:
                    self.initial_database_data = str(item)
                case Setup._DCR_CFG_LINE_FOOTER_MAX_DISTANCE:
                    self.line_footer_max_distance = int(item)
                case Setup._DCR_CFG_LINE_FOOTER_MAX_LINES:
                    self.line_footer_max_lines = int(item)
                case Setup._DCR_CFG_LINE_HEADER_MAX_DISTANCE:
                    self.line_header_max_distance = int(item)
                case Setup._DCR_CFG_LINE_HEADER_MAX_LINES:
                    self.line_header_max_lines = int(item)
                case _:
                    utils.terminate_fatal_setup(f"Unknown configuration parameter '{key}'")

        self._check_config()
