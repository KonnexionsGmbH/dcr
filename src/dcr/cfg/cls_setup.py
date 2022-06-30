"""Module cfg.cls_setup: Managing the application configuration parameters."""
from __future__ import annotations

import configparser
import os
from typing import ClassVar

import cfg.glob
import utils


# pylint: disable=too-many-instance-attributes
class Setup:
    """Managing the application configuration parameters.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    _CONFIG_PARAM_NO = 125

    _DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET: ClassVar[str] = "create_extra_file_list_bullet"
    _DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER: ClassVar[str] = "create_extra_file_list_number"
    _DCR_CFG_CREATE_EXTRA_FILE_TABLE: ClassVar[str] = "create_extra_file_table"
    _DCR_CFG_CREATE_EXTRA_FILE_TOC: ClassVar[str] = "create_extra_file_toc"
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
    _DCR_CFG_LT_FOOTER_MAX_DISTANCE: ClassVar[str] = "lt_footer_max_distance"
    _DCR_CFG_LT_FOOTER_MAX_LINES: ClassVar[str] = "lt_footer_max_lines"
    _DCR_CFG_LT_HEADER_MAX_DISTANCE: ClassVar[str] = "lt_header_max_distance"
    _DCR_CFG_LT_HEADER_MAX_LINES: ClassVar[str] = "lt_header_max_lines"
    _DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX: ClassVar[str] = "lt_heading_file_incl_no_ctx"
    _DCR_CFG_LT_HEADING_FILE_INCL_REGEXP: ClassVar[str] = "lt_heading_file_incl_regexp"
    _DCR_CFG_LT_HEADING_MAX_LEVEL: ClassVar[str] = "lt_heading_max_level"
    _DCR_CFG_LT_HEADING_MIN_PAGES: ClassVar[str] = "lt_heading_min_pages"
    _DCR_CFG_LT_HEADING_RULE_FILE: ClassVar[str] = "lt_heading_rule_file"
    _DCR_CFG_LT_HEADING_TOLERANCE_LLX: ClassVar[str] = "lt_heading_tolerance_llx"
    _DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES: ClassVar[str] = "lt_list_bullet_min_entries"
    _DCR_CFG_LT_LIST_BULLET_RULE_FILE: ClassVar[str] = "lt_list_bullet_rule_file"
    _DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX: ClassVar[str] = "lt_list_bullet_tolerance_llx"
    _DCR_CFG_LT_LIST_NUMBER_MIN_ENTRIES: ClassVar[str] = "lt_list_number_min_entries"
    _DCR_CFG_LT_LIST_NUMBER_RULE_FILE: ClassVar[str] = "lt_list_number_rule_file"
    _DCR_CFG_LT_LIST_NUMBER_TOLERANCE_LLX: ClassVar[str] = "lt_list_number_tolerance_llx"
    _DCR_CFG_LT_TABLE_FILE_INCL_EMPTY_COLUMNS: ClassVar[str] = "lt_table_file_incl_empty_columns"
    _DCR_CFG_LT_TOC_LAST_PAGE: ClassVar[str] = "lt_toc_last_page"
    _DCR_CFG_LT_TOC_MIN_ENTRIES: ClassVar[str] = "lt_toc_min_entries"
    _DCR_CFG_PDF2IMAGE_TYPE: ClassVar[str] = "pdf2image_type"
    _DCR_CFG_SECTION: ClassVar[str] = "dcr"
    _DCR_CFG_SECTION_ENV_TEST: ClassVar[str] = "dcr.env.test"
    _DCR_CFG_SECTION_SPACY: ClassVar[str] = "dcr.spacy"

    _DCR_CFG_SPACY_IGNORE_BRACKET: ClassVar[str] = "spacy_ignore_bracket"
    _DCR_CFG_SPACY_IGNORE_LEFT_PUNCT: ClassVar[str] = "spacy_ignore_left_punct"
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_FOOTER: ClassVar[str] = "spacy_ignore_line_type_footer"
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_HEADER: ClassVar[str] = "spacy_ignore_line_type_header"
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_HEADING: ClassVar[str] = "spacy_ignore_line_type_heading"
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_LIST_BULLETED: ClassVar[str] = "spacy_ignore_line_type_list_bulleted"
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_LIST_NUMBERED: ClassVar[str] = "spacy_ignore_line_type_list_numbered"
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_TABLE: ClassVar[str] = "spacy_ignore_line_type_table"
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_TOC: ClassVar[str] = "spacy_ignore_line_type_toc"
    _DCR_CFG_SPACY_IGNORE_PUNCT: ClassVar[str] = "spacy_ignore_punct"
    _DCR_CFG_SPACY_IGNORE_QUOTE: ClassVar[str] = "spacy_ignore_quote"
    _DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT: ClassVar[str] = "spacy_ignore_right_punct"
    _DCR_CFG_SPACY_IGNORE_SPACE: ClassVar[str] = "spacy_ignore_space"
    _DCR_CFG_SPACY_IGNORE_STOP: ClassVar[str] = "spacy_ignore_stop"

    _DCR_CFG_SPACY_TKN_ATTR_CLUSTER: ClassVar[str] = "spacy_tkn_attr_cluster"
    _DCR_CFG_SPACY_TKN_ATTR_DEP_: ClassVar[str] = "spacy_tkn_attr_dep_"
    _DCR_CFG_SPACY_TKN_ATTR_DOC: ClassVar[str] = "spacy_tkn_attr_doc"
    _DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_: ClassVar[str] = "spacy_tkn_attr_ent_iob_"
    _DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_: ClassVar[str] = "spacy_tkn_attr_ent_kb_id_"
    _DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_: ClassVar[str] = "spacy_tkn_attr_ent_type_"
    _DCR_CFG_SPACY_TKN_ATTR_HEAD: ClassVar[str] = "spacy_tkn_attr_head"
    _DCR_CFG_SPACY_TKN_ATTR_I: ClassVar[str] = "spacy_tkn_attr_i"
    _DCR_CFG_SPACY_TKN_ATTR_IDX: ClassVar[str] = "spacy_tkn_attr_idx"
    _DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA: ClassVar[str] = "spacy_tkn_attr_is_alpha"
    _DCR_CFG_SPACY_TKN_ATTR_IS_ASCII: ClassVar[str] = "spacy_tkn_attr_is_ascii"
    _DCR_CFG_SPACY_TKN_ATTR_IS_BRACKET: ClassVar[str] = "spacy_tkn_attr_is_bracket"
    _DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY: ClassVar[str] = "spacy_tkn_attr_is_currency"
    _DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT: ClassVar[str] = "spacy_tkn_attr_is_digit"
    _DCR_CFG_SPACY_TKN_ATTR_IS_LEFT_PUNCT: ClassVar[str] = "spacy_tkn_attr_is_left_punct"
    _DCR_CFG_SPACY_TKN_ATTR_IS_LOWER: ClassVar[str] = "spacy_tkn_attr_is_lower"
    _DCR_CFG_SPACY_TKN_ATTR_IS_OOV: ClassVar[str] = "spacy_tkn_attr_is_oov"
    _DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT: ClassVar[str] = "spacy_tkn_attr_is_punct"
    _DCR_CFG_SPACY_TKN_ATTR_IS_QUOTE: ClassVar[str] = "spacy_tkn_attr_is_quote"
    _DCR_CFG_SPACY_TKN_ATTR_IS_RIGHT_PUNCT: ClassVar[str] = "spacy_tkn_attr_is_right_punct"
    _DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END: ClassVar[str] = "spacy_tkn_attr_is_sent_end"
    _DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START: ClassVar[str] = "spacy_tkn_attr_is_sent_start"
    _DCR_CFG_SPACY_TKN_ATTR_IS_SPACE: ClassVar[str] = "spacy_tkn_attr_is_space"
    _DCR_CFG_SPACY_TKN_ATTR_IS_STOP: ClassVar[str] = "spacy_tkn_attr_is_stop"
    _DCR_CFG_SPACY_TKN_ATTR_IS_TITLE: ClassVar[str] = "spacy_tkn_attr_is_title"
    _DCR_CFG_SPACY_TKN_ATTR_IS_UPPER: ClassVar[str] = "spacy_tkn_attr_is_upper"
    _DCR_CFG_SPACY_TKN_ATTR_LANG_: ClassVar[str] = "spacy_tkn_attr_lang_"
    _DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE: ClassVar[str] = "spacy_tkn_attr_left_edge"
    _DCR_CFG_SPACY_TKN_ATTR_LEMMA_: ClassVar[str] = "spacy_tkn_attr_lemma_"
    _DCR_CFG_SPACY_TKN_ATTR_LEX: ClassVar[str] = "spacy_tkn_attr_lex"
    _DCR_CFG_SPACY_TKN_ATTR_LEX_ID: ClassVar[str] = "spacy_tkn_attr_lex_id"
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL: ClassVar[str] = "spacy_tkn_attr_like_email"
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM: ClassVar[str] = "spacy_tkn_attr_like_num"
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_URL: ClassVar[str] = "spacy_tkn_attr_like_url"
    _DCR_CFG_SPACY_TKN_ATTR_LOWER_: ClassVar[str] = "spacy_tkn_attr_lower_"
    _DCR_CFG_SPACY_TKN_ATTR_MORPH: ClassVar[str] = "spacy_tkn_attr_morph"
    _DCR_CFG_SPACY_TKN_ATTR_NORM_: ClassVar[str] = "spacy_tkn_attr_norm_"
    _DCR_CFG_SPACY_TKN_ATTR_ORTH_: ClassVar[str] = "spacy_tkn_attr_orth_"
    _DCR_CFG_SPACY_TKN_ATTR_POS_: ClassVar[str] = "spacy_tkn_attr_pos_"
    _DCR_CFG_SPACY_TKN_ATTR_PREFIX_: ClassVar[str] = "spacy_tkn_attr_prefix_"
    _DCR_CFG_SPACY_TKN_ATTR_PROB: ClassVar[str] = "spacy_tkn_attr_prob"
    _DCR_CFG_SPACY_TKN_ATTR_RANK: ClassVar[str] = "spacy_tkn_attr_rank"
    _DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE: ClassVar[str] = "spacy_tkn_attr_right_edge"
    _DCR_CFG_SPACY_TKN_ATTR_SENT: ClassVar[str] = "spacy_tkn_attr_sent"
    _DCR_CFG_SPACY_TKN_ATTR_SENTIMENT: ClassVar[str] = "spacy_tkn_attr_sentiment"
    _DCR_CFG_SPACY_TKN_ATTR_SHAPE_: ClassVar[str] = "spacy_tkn_attr_shape_"
    _DCR_CFG_SPACY_TKN_ATTR_SUFFIX_: ClassVar[str] = "spacy_tkn_attr_suffix_"
    _DCR_CFG_SPACY_TKN_ATTR_TAG_: ClassVar[str] = "spacy_tkn_attr_tag_"
    _DCR_CFG_SPACY_TKN_ATTR_TENSOR: ClassVar[str] = "spacy_tkn_attr_tensor"
    _DCR_CFG_SPACY_TKN_ATTR_TEXT: ClassVar[str] = "spacy_tkn_attr_text"
    _DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS: ClassVar[str] = "spacy_tkn_attr_text_with_ws"
    _DCR_CFG_SPACY_TKN_ATTR_VOCAB: ClassVar[str] = "spacy_tkn_attr_vocab"
    _DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_: ClassVar[str] = "spacy_tkn_attr_whitespace_"

    _DCR_CFG_TESSERACT_TIMEOUT: ClassVar[str] = "tesseract_timeout"
    _DCR_CFG_TETML_PAGE: ClassVar[str] = "tetml_page"
    _DCR_CFG_TETML_WORD: ClassVar[str] = "tetml_word"
    _DCR_CFG_TOKENIZE_2_DATABASE: ClassVar[str] = "tokenize_2_database"
    _DCR_CFG_TOKENIZE_2_JSONFILE: ClassVar[str] = "tokenize_2_jsonfile"
    _DCR_CFG_VERBOSE: ClassVar[str] = "verbose"
    _DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS: ClassVar[str] = "verbose_lt_headers_footers"
    _DCR_CFG_VERBOSE_LT_HEADING: ClassVar[str] = "verbose_lt_heading"
    _DCR_CFG_VERBOSE_LT_LIST_BULLET: ClassVar[str] = "verbose_lt_list_bullet"
    _DCR_CFG_VERBOSE_LT_LIST_NUMBER: ClassVar[str] = "verbose_lt_list_number"
    _DCR_CFG_VERBOSE_LT_TABLE: ClassVar[str] = "verbose_lt_table"
    _DCR_CFG_VERBOSE_LT_TOC: ClassVar[str] = "verbose_lt_toc"
    _DCR_CFG_VERBOSE_PARSER: ClassVar[str] = "verbose_parser"

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
    # pylint: disable=too-many-statements
    def __init__(self) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._get_environment_variant()

        self._config: dict[str, str] = {}

        # -----------------------------------------------------------------------------
        # DCR configuration.
        # -----------------------------------------------------------------------------
        self.is_create_extra_file_list_bullet = True
        self.is_create_extra_file_list_number = True
        self.is_create_extra_file_table = True
        self.is_create_extra_file_toc = True

        self.db_connection_port = 5432
        self.db_connection_prefix = "postgresql+psycopg2://"
        self.db_container_port = 5432
        self.db_database = "dcr_db_prod"
        self.db_database_admin = "dcr_db_prod_admin"
        self.db_dialect = "postgresql"
        self.db_host = "localhost"
        self.db_initial_data_file = utils.get_os_independent_name("data/db_initial_data_file.json")
        self.db_password = "postgresql"  # nosec
        self.db_password_admin = "postgresql"  # nosec
        self.db_schema = "dcr_schema"
        self.db_user = "dcr_user"
        self.db_user_admin = "dcr_user_admin"

        self.is_delete_auxiliary_files = True

        self.directory_inbox = utils.get_os_independent_name("data/inbox")
        self.directory_inbox_accepted = utils.get_os_independent_name("data/inbox_accepted")
        self.directory_inbox_rejected = utils.get_os_independent_name("data/inbox_rejected")
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

        self.lt_heading_max_level = 3
        self.lt_heading_min_pages = 2
        self.lt_heading_rule_file = "none"
        self.lt_heading_tolerance_llx = 5
        self.lt_list_bullet_min_entries = 2
        self.lt_list_bullet_rule_file = "none"
        self.lt_list_bullet_tolerance_llx = 5
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

        self.verbose_parser = "none"

        # -----------------------------------------------------------------------------
        # Spacy ignore tokens.
        # -----------------------------------------------------------------------------
        self.is_spacy_ignore_bracket = True
        self.is_spacy_ignore_left_punct = True
        self.is_spacy_ignore_line_type_footer = True
        self.is_spacy_ignore_line_type_header = True
        self.is_spacy_ignore_line_type_heading = False
        self.is_spacy_ignore_line_type_list_bulleted = False
        self.is_spacy_ignore_line_type_list_numbered = False
        self.is_spacy_ignore_line_type_table = False
        self.is_spacy_ignore_line_type_toc = True
        self.is_spacy_ignore_punct = True
        self.is_spacy_ignore_quote = True
        self.is_spacy_ignore_right_punct = True
        self.is_spacy_ignore_space = True
        self.is_spacy_ignore_stop = True

        # -----------------------------------------------------------------------------
        # spaCy token attributes.
        # -----------------------------------------------------------------------------
        self.is_spacy_tkn_attr_cluster = False
        self.is_spacy_tkn_attr_dep_ = False
        self.is_spacy_tkn_attr_doc = False
        self.is_spacy_tkn_attr_ent_iob_ = False
        self.is_spacy_tkn_attr_ent_kb_id_ = False
        self.is_spacy_tkn_attr_ent_type_ = True
        self.is_spacy_tkn_attr_head = False
        self.is_spacy_tkn_attr_i = True
        self.is_spacy_tkn_attr_idx = False
        self.is_spacy_tkn_attr_is_alpha = False
        self.is_spacy_tkn_attr_is_ascii = False
        self.is_spacy_tkn_attr_is_bracket = False
        self.is_spacy_tkn_attr_is_currency = True
        self.is_spacy_tkn_attr_is_digit = True
        self.is_spacy_tkn_attr_is_left_punct = False
        self.is_spacy_tkn_attr_is_lower = False
        self.is_spacy_tkn_attr_is_oov = True
        self.is_spacy_tkn_attr_is_punct = True
        self.is_spacy_tkn_attr_is_quote = False
        self.is_spacy_tkn_attr_is_right_punct = False
        self.is_spacy_tkn_attr_is_sent_end = False
        self.is_spacy_tkn_attr_is_sent_start = False
        self.is_spacy_tkn_attr_is_space = False
        self.is_spacy_tkn_attr_is_stop = True
        self.is_spacy_tkn_attr_is_title = True
        self.is_spacy_tkn_attr_is_upper = False
        self.is_spacy_tkn_attr_lang_ = False
        self.is_spacy_tkn_attr_left_edge = False
        self.is_spacy_tkn_attr_lemma_ = True
        self.is_spacy_tkn_attr_lex = False
        self.is_spacy_tkn_attr_lex_id = False
        self.is_spacy_tkn_attr_like_email = True
        self.is_spacy_tkn_attr_like_num = True
        self.is_spacy_tkn_attr_like_url = True
        self.is_spacy_tkn_attr_lower_ = False
        self.is_spacy_tkn_attr_morph = False
        self.is_spacy_tkn_attr_norm_ = True
        self.is_spacy_tkn_attr_orth_ = False
        self.is_spacy_tkn_attr_pos_ = True
        self.is_spacy_tkn_attr_prefix_ = False
        self.is_spacy_tkn_attr_prob = False
        self.is_spacy_tkn_attr_rank = False
        self.is_spacy_tkn_attr_right_edge = False
        self.is_spacy_tkn_attr_sent = False
        self.is_spacy_tkn_attr_sentiment = False
        self.is_spacy_tkn_attr_shape_ = False
        self.is_spacy_tkn_attr_suffix_ = False
        self.is_spacy_tkn_attr_tag_ = True
        self.is_spacy_tkn_attr_tensor = False
        self.is_spacy_tkn_attr_text = True
        self.is_spacy_tkn_attr_text_with_ws = False
        self.is_spacy_tkn_attr_vocab = False
        self.is_spacy_tkn_attr_whitespace_ = True

        self._load_config()

        utils.progress_msg_core("The configuration parameters are checked and loaded")

        self._exist = True

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Check the configuration parameters.
    # -----------------------------------------------------------------------------
    def _check_config(self) -> None:
        """Check the configuration parameters."""
        self.is_create_extra_file_list_bullet = self._determine_config_param_boolean(
            Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET, self.is_create_extra_file_list_bullet
        )
        self.is_create_extra_file_list_number = self._determine_config_param_boolean(
            Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER, self.is_create_extra_file_list_number
        )
        self.is_create_extra_file_table = self._determine_config_param_boolean(
            Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE, self.is_create_extra_file_table
        )
        self.is_create_extra_file_toc = self._determine_config_param_boolean(
            Setup._DCR_CFG_CREATE_EXTRA_FILE_TOC, self.is_create_extra_file_toc
        )
        self.db_connection_port = self._determine_config_param_integer(
            Setup._DCR_CFG_DB_CONNECTION_PORT, self.db_connection_port
        )
        self.db_container_port = self._determine_config_param_integer(
            Setup._DCR_CFG_DB_CONTAINER_PORT, self.db_container_port
        )

        self.is_delete_auxiliary_files = self._determine_config_param_boolean(
            Setup._DCR_CFG_DELETE_AUXILIARY_FILES, self.is_delete_auxiliary_files
        )

        self._check_config_directory_inbox()
        self._check_config_directory_inbox_accepted()
        self._check_config_directory_inbox_rejected()
        self._check_config_doc_id_in_file_name()

        self.is_ignore_duplicates = self._determine_config_param_boolean(
            Setup._DCR_CFG_IGNORE_DUPLICATES, self.is_ignore_duplicates
        )

        self.json_indent = self._determine_config_param_integer(Setup._DCR_CFG_JSON_INDENT, self.json_indent)

        self.is_json_sort_keys = self._determine_config_param_boolean(Setup._DCR_CFG_JSON_SORT_KEYS, self.is_json_sort_keys)

        self.lt_footer_max_distance = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE, self.lt_footer_max_distance
        )
        self.lt_footer_max_lines = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_FOOTER_MAX_LINES, self.lt_footer_max_lines
        )
        self.lt_header_max_distance = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE, self.lt_header_max_distance
        )
        self.lt_header_max_lines = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_HEADER_MAX_LINES, self.lt_header_max_lines
        )
        self.lt_heading_file_incl_no_ctx = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX, self.lt_heading_file_incl_no_ctx
        )
        self.is_lt_heading_file_incl_regexp = self._determine_config_param_boolean(
            Setup._DCR_CFG_LT_HEADING_FILE_INCL_REGEXP, self.is_lt_heading_file_incl_regexp
        )
        self.lt_heading_max_level = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_HEADING_MAX_LEVEL, self.lt_heading_max_level
        )
        self.lt_heading_min_pages = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_HEADING_MIN_PAGES, self.lt_heading_min_pages
        )
        self.lt_heading_tolerance_llx = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_HEADING_TOLERANCE_LLX, self.lt_heading_tolerance_llx
        )
        self.lt_list_bullet_min_entries = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX, self.lt_list_bullet_min_entries
        )
        self.lt_list_bullet_tolerance_llx = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES, self.lt_list_bullet_tolerance_llx
        )
        self.lt_list_number_min_entries = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_LIST_NUMBER_MIN_ENTRIES, self.lt_list_number_min_entries
        )
        self.lt_list_number_tolerance_llx = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_LIST_NUMBER_MIN_ENTRIES, self.lt_list_number_tolerance_llx
        )
        self.is_lt_table_file_incl_empty_columns = self._determine_config_param_boolean(
            Setup._DCR_CFG_LT_TABLE_FILE_INCL_EMPTY_COLUMNS, self.is_lt_table_file_incl_empty_columns
        )
        self.lt_toc_last_page = self._determine_config_param_integer(Setup._DCR_CFG_LT_TOC_LAST_PAGE, self.lt_toc_last_page)
        self.lt_toc_min_entries = self._determine_config_param_integer(
            Setup._DCR_CFG_LT_TOC_MIN_ENTRIES, self.lt_toc_min_entries
        )

        self._check_config_pdf2image_type()

        self._determine_config_spacy_tkn()
        self._determine_config_spacy_tkn_ignore()

        self.tesseract_timeout = self._determine_config_param_integer(
            Setup._DCR_CFG_TESSERACT_TIMEOUT, self.tesseract_timeout
        )

        self.is_tetml_page = self._determine_config_param_boolean(Setup._DCR_CFG_TETML_PAGE, self.is_tetml_page)
        self.is_tetml_word = self._determine_config_param_boolean(Setup._DCR_CFG_TETML_WORD, self.is_tetml_word)

        self.is_tokenize_2_database = self._determine_config_param_boolean(
            Setup._DCR_CFG_TOKENIZE_2_DATABASE, self.is_tokenize_2_database
        )
        self.is_tokenize_2_jsonfile = self._determine_config_param_boolean(
            Setup._DCR_CFG_TOKENIZE_2_JSONFILE, self.is_tokenize_2_jsonfile
        )
        if not self.is_tokenize_2_database:
            if not self.is_tokenize_2_jsonfile:
                utils.terminate_fatal_setup(
                    "At least one of the configuration parameters 'tokenize_2_database' or "
                    + "'tokenize_2_jsonfile' must be 'true'"
                )

        self.is_verbose = self._determine_config_param_boolean(Setup._DCR_CFG_VERBOSE, self.is_verbose)
        self.is_verbose_lt_headers_footers = self._determine_config_param_boolean(
            Setup._DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS, self.is_verbose_lt_headers_footers
        )
        self.is_verbose_lt_heading = self._determine_config_param_boolean(
            Setup._DCR_CFG_VERBOSE_LT_HEADING, self.is_verbose_lt_heading
        )
        self.is_verbose_lt_list_bullet = self._determine_config_param_boolean(
            Setup._DCR_CFG_VERBOSE_LT_LIST_BULLET, self.is_verbose_lt_list_bullet
        )
        self.is_verbose_lt_list_number = self._determine_config_param_boolean(
            Setup._DCR_CFG_VERBOSE_LT_LIST_NUMBER, self.is_verbose_lt_list_number
        )
        self.is_verbose_lt_table = self._determine_config_param_boolean(
            Setup._DCR_CFG_VERBOSE_LT_TABLE, self.is_verbose_lt_table
        )
        self.is_verbose_lt_toc = self._determine_config_param_boolean(Setup._DCR_CFG_VERBOSE_LT_TOC, self.is_verbose_lt_toc)
        self._check_config_verbose_parser()

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - directory_inbox.
    # -----------------------------------------------------------------------------
    def _check_config_directory_inbox(self) -> None:
        """Check the configuration parameter - directory_inbox."""
        if Setup._DCR_CFG_DIRECTORY_INBOX in self._config:
            self._config[Setup._DCR_CFG_DIRECTORY_INBOX] = str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX])

            self.directory_inbox = utils.get_os_independent_name(str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX]))
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

            self.directory_inbox_accepted = utils.get_os_independent_name(
                str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED])
            )
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

            self.directory_inbox_rejected = utils.get_os_independent_name(
                str(self._config[Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED])
            )
        else:
            utils.terminate_fatal_setup(f"Missing configuration parameter '{Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED}'")

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
                utils.terminate_fatal_setup(
                    f"Invalid configuration parameter value for parameter " f"'pdf2image_type': '{self.pdf2image_type}'"
                )

    # -----------------------------------------------------------------------------
    # Check the configuration parameter - verbose_parser.
    # -----------------------------------------------------------------------------
    def _check_config_verbose_parser(self) -> None:
        """Check the configuration parameter - verbose_parser."""
        if Setup._DCR_CFG_VERBOSE_PARSER in self._config:
            if str(self._config[Setup._DCR_CFG_VERBOSE_PARSER]).lower() in {"all", "text"}:
                self.verbose_parser = str(self._config[Setup._DCR_CFG_VERBOSE_PARSER]).lower()

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
    # Determine a spaCy token configuration parameter.
    # -----------------------------------------------------------------------------
    def _determine_config_spacy_tkn(self) -> None:
        """Determine a spaCy token configuration parameter."""
        self.is_spacy_tkn_attr_cluster = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_CLUSTER, self.is_spacy_tkn_attr_cluster
        )
        self.is_spacy_tkn_attr_dep_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_DEP_, self.is_spacy_tkn_attr_dep_
        )
        self.is_spacy_tkn_attr_doc = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_DOC, self.is_spacy_tkn_attr_doc
        )
        self.is_spacy_tkn_attr_ent_iob_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_, self.is_spacy_tkn_attr_ent_iob_
        )
        self.is_spacy_tkn_attr_ent_kb_id_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_, self.is_spacy_tkn_attr_ent_kb_id_
        )
        self.is_spacy_tkn_attr_ent_type_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_, self.is_spacy_tkn_attr_ent_type_
        )
        self.is_spacy_tkn_attr_head = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_HEAD, self.is_spacy_tkn_attr_head
        )
        self.is_spacy_tkn_attr_i = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_I, self.is_spacy_tkn_attr_i
        )
        self.is_spacy_tkn_attr_idx = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IDX, self.is_spacy_tkn_attr_idx
        )
        self.is_spacy_tkn_attr_is_alpha = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA, self.is_spacy_tkn_attr_is_alpha
        )
        self.is_spacy_tkn_attr_is_ascii = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_ASCII, self.is_spacy_tkn_attr_is_ascii
        )
        self.is_spacy_tkn_attr_is_bracket = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_BRACKET, self.is_spacy_tkn_attr_is_bracket
        )
        self.is_spacy_tkn_attr_is_currency = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY, self.is_spacy_tkn_attr_is_currency
        )
        self.is_spacy_tkn_attr_is_digit = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT, self.is_spacy_tkn_attr_is_digit
        )
        self.is_spacy_tkn_attr_is_left_punct = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_LEFT_PUNCT, self.is_spacy_tkn_attr_is_left_punct
        )
        self.is_spacy_tkn_attr_is_lower = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_LOWER, self.is_spacy_tkn_attr_is_lower
        )
        self.is_spacy_tkn_attr_is_oov = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_OOV, self.is_spacy_tkn_attr_is_oov
        )
        self.is_spacy_tkn_attr_is_punct = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT, self.is_spacy_tkn_attr_is_punct
        )
        self.is_spacy_tkn_attr_is_quote = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_QUOTE, self.is_spacy_tkn_attr_is_quote
        )
        self.is_spacy_tkn_attr_is_right_punct = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_RIGHT_PUNCT, self.is_spacy_tkn_attr_is_right_punct
        )
        self.is_spacy_tkn_attr_is_sent_end = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END, self.is_spacy_tkn_attr_is_sent_end
        )
        self.is_spacy_tkn_attr_is_sent_start = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START, self.is_spacy_tkn_attr_is_sent_start
        )
        self.is_spacy_tkn_attr_is_space = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SPACE, self.is_spacy_tkn_attr_is_space
        )
        self.is_spacy_tkn_attr_is_stop = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_STOP, self.is_spacy_tkn_attr_is_stop
        )
        self.is_spacy_tkn_attr_is_title = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_TITLE, self.is_spacy_tkn_attr_is_title
        )
        self.is_spacy_tkn_attr_is_upper = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_IS_UPPER, self.is_spacy_tkn_attr_is_upper
        )
        self.is_spacy_tkn_attr_lang_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_LANG_, self.is_spacy_tkn_attr_lang_
        )
        self.is_spacy_tkn_attr_left_edge = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE, self.is_spacy_tkn_attr_left_edge
        )
        self.is_spacy_tkn_attr_lemma_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_LEMMA_, self.is_spacy_tkn_attr_lemma_
        )
        self.is_spacy_tkn_attr_lex = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_LEX, self.is_spacy_tkn_attr_lex
        )
        self.is_spacy_tkn_attr_lex_id = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_LEX_ID, self.is_spacy_tkn_attr_lex_id
        )
        self.is_spacy_tkn_attr_like_email = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL, self.is_spacy_tkn_attr_like_email
        )
        self.is_spacy_tkn_attr_like_num = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM, self.is_spacy_tkn_attr_like_num
        )
        self.is_spacy_tkn_attr_like_url = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_URL, self.is_spacy_tkn_attr_like_url
        )
        self.is_spacy_tkn_attr_lower_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_LOWER_, self.is_spacy_tkn_attr_lower_
        )
        self.is_spacy_tkn_attr_morph = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_MORPH, self.is_spacy_tkn_attr_morph
        )
        self.is_spacy_tkn_attr_norm_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_NORM_, self.is_spacy_tkn_attr_norm_
        )
        self.is_spacy_tkn_attr_orth_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_ORTH_, self.is_spacy_tkn_attr_orth_
        )
        self.is_spacy_tkn_attr_pos_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_POS_, self.is_spacy_tkn_attr_pos_
        )
        self.is_spacy_tkn_attr_prefix_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_PREFIX_, self.is_spacy_tkn_attr_prefix_
        )
        self.is_spacy_tkn_attr_prob = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_PROB, self.is_spacy_tkn_attr_prob
        )
        self.is_spacy_tkn_attr_rank = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_RANK, self.is_spacy_tkn_attr_rank
        )
        self.is_spacy_tkn_attr_right_edge = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE, self.is_spacy_tkn_attr_right_edge
        )
        self.is_spacy_tkn_attr_sent = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_SENT, self.is_spacy_tkn_attr_sent
        )
        self.is_spacy_tkn_attr_sentiment = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_SENTIMENT, self.is_spacy_tkn_attr_sentiment
        )
        self.is_spacy_tkn_attr_shape_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_, self.is_spacy_tkn_attr_shape_
        )
        self.is_spacy_tkn_attr_suffix_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_SUFFIX_, self.is_spacy_tkn_attr_suffix_
        )
        self.is_spacy_tkn_attr_tag_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_TAG_, self.is_spacy_tkn_attr_tag_
        )
        self.is_spacy_tkn_attr_tensor = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_TENSOR, self.is_spacy_tkn_attr_tensor
        )
        self.is_spacy_tkn_attr_text = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT, self.is_spacy_tkn_attr_text
        )
        self.is_spacy_tkn_attr_text_with_ws = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS, self.is_spacy_tkn_attr_text_with_ws
        )
        self.is_spacy_tkn_attr_vocab = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_VOCAB, self.is_spacy_tkn_attr_vocab
        )
        self.is_spacy_tkn_attr_whitespace_ = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_, self.is_spacy_tkn_attr_whitespace_
        )

    # -----------------------------------------------------------------------------
    # Determine a spaCy token configuration parameter to ignore the token creation.
    # -----------------------------------------------------------------------------
    def _determine_config_spacy_tkn_ignore(self) -> None:
        """Determine a spaCy token configuration parameter to ignore the token
        creation."""
        self.is_spacy_ignore_bracket = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_BRACKET, self.is_spacy_ignore_bracket
        )
        self.is_spacy_ignore_left_punct = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_LEFT_PUNCT, self.is_spacy_ignore_left_punct
        )
        self.is_spacy_ignore_line_type_footer = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_FOOTER, self.is_spacy_ignore_line_type_footer
        )
        self.is_spacy_ignore_line_type_header = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_HEADER, self.is_spacy_ignore_line_type_header
        )
        self.is_spacy_ignore_line_type_heading = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_HEADING, self.is_spacy_ignore_line_type_heading
        )
        self.is_spacy_ignore_line_type_list_bulleted = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_LIST_BULLETED, self.is_spacy_ignore_line_type_list_bulleted
        )
        self.is_spacy_ignore_line_type_list_numbered = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_LIST_NUMBERED, self.is_spacy_ignore_line_type_list_numbered
        )
        self.is_spacy_ignore_line_type_table = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_TABLE, self.is_spacy_ignore_line_type_table
        )
        self.is_spacy_ignore_line_type_toc = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_TOC, self.is_spacy_ignore_line_type_toc
        )
        self.is_spacy_ignore_punct = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_PUNCT, self.is_spacy_ignore_punct
        )
        self.is_spacy_ignore_quote = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_QUOTE, self.is_spacy_ignore_quote
        )
        self.is_spacy_ignore_right_punct = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT, self.is_spacy_ignore_right_punct
        )
        self.is_spacy_ignore_space = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_SPACE, self.is_spacy_ignore_space
        )
        self.is_spacy_ignore_stop = self._determine_config_param_boolean(
            Setup._DCR_CFG_SPACY_IGNORE_STOP, self.is_spacy_ignore_stop
        )

    # -----------------------------------------------------------------------------
    # Determine and check the environment variant.
    # -----------------------------------------------------------------------------
    def _get_environment_variant(self) -> None:
        """Determine and check the environment variant."""
        self.environment_variant = Setup.ENVIRONMENT_TYPE_PROD

        try:
            self.environment_variant = os.environ[Setup._DCR_ENVIRONMENT_TYPE]
        except KeyError:
            utils.terminate_fatal_setup(f"The environment variable '{Setup._DCR_ENVIRONMENT_TYPE}' is missing")

        if self.environment_variant not in [
            Setup.ENVIRONMENT_TYPE_DEV,
            Setup.ENVIRONMENT_TYPE_PROD,
            Setup.ENVIRONMENT_TYPE_TEST,
        ]:
            utils.terminate_fatal_setup(
                f"The environment variable '{Setup._DCR_ENVIRONMENT_TYPE}' "
                f"has the invalid content '{self.environment_variant}'"
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
                Setup._DCR_CFG_SECTION_SPACY,
            ):
                for (key, value) in config_parser.items(section):
                    self._config[key] = value

        for key, item in self._config.items():
            match key:
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
                    self.db_initial_data_file = utils.get_os_independent_name(item)
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
                case (
                    Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET
                    | Setup._DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER
                    | Setup._DCR_CFG_CREATE_EXTRA_FILE_TABLE
                    | Setup._DCR_CFG_CREATE_EXTRA_FILE_TOC
                    | Setup._DCR_CFG_DB_CONNECTION_PORT
                    | Setup._DCR_CFG_DB_CONTAINER_PORT
                    | Setup._DCR_CFG_DELETE_AUXILIARY_FILES
                    | Setup._DCR_CFG_DIRECTORY_INBOX
                    | Setup._DCR_CFG_DIRECTORY_INBOX_ACCEPTED
                    | Setup._DCR_CFG_DIRECTORY_INBOX_REJECTED
                    | Setup._DCR_CFG_DOC_ID_IN_FILE_NAME
                    | Setup._DCR_CFG_IGNORE_DUPLICATES
                    | Setup._DCR_CFG_JSON_INDENT
                    | Setup._DCR_CFG_JSON_SORT_KEYS
                    | Setup._DCR_CFG_LT_FOOTER_MAX_DISTANCE
                    | Setup._DCR_CFG_LT_FOOTER_MAX_LINES
                    | Setup._DCR_CFG_LT_HEADER_MAX_DISTANCE
                    | Setup._DCR_CFG_LT_HEADER_MAX_LINES
                    | Setup._DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX
                    | Setup._DCR_CFG_LT_HEADING_FILE_INCL_REGEXP
                    | Setup._DCR_CFG_LT_HEADING_MAX_LEVEL
                    | Setup._DCR_CFG_LT_HEADING_MIN_PAGES
                    | Setup._DCR_CFG_LT_HEADING_TOLERANCE_LLX
                    | Setup._DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES
                    | Setup._DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX
                    | Setup._DCR_CFG_LT_LIST_NUMBER_MIN_ENTRIES
                    | Setup._DCR_CFG_LT_LIST_NUMBER_TOLERANCE_LLX
                    | Setup._DCR_CFG_LT_TABLE_FILE_INCL_EMPTY_COLUMNS
                    | Setup._DCR_CFG_LT_TOC_LAST_PAGE
                    | Setup._DCR_CFG_LT_TOC_MIN_ENTRIES
                    | Setup._DCR_CFG_PDF2IMAGE_TYPE
                    | Setup._DCR_CFG_SPACY_IGNORE_BRACKET
                    | Setup._DCR_CFG_SPACY_IGNORE_LEFT_PUNCT
                    | Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_FOOTER
                    | Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_HEADER
                    | Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_HEADING
                    | Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_LIST_BULLETED
                    | Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_LIST_NUMBERED
                    | Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_TABLE
                    | Setup._DCR_CFG_SPACY_IGNORE_LINE_TYPE_TOC
                    | Setup._DCR_CFG_SPACY_IGNORE_PUNCT
                    | Setup._DCR_CFG_SPACY_IGNORE_QUOTE
                    | Setup._DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT
                    | Setup._DCR_CFG_SPACY_IGNORE_SPACE
                    | Setup._DCR_CFG_SPACY_IGNORE_STOP
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_CLUSTER
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_DEP_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_DOC
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_HEAD
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_I
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IDX
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_ASCII
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_BRACKET
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_LEFT_PUNCT
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_LOWER
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_OOV
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_QUOTE
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_RIGHT_PUNCT
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_SPACE
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_STOP
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_TITLE
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_IS_UPPER
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LANG_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LEMMA_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LEX
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LEX_ID
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LIKE_URL
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_LOWER_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_MORPH
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_NORM_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_ORTH_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_POS_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_PREFIX_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_PROB
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_RANK
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_SENT
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_SENTIMENT
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_SHAPE_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_SUFFIX_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_TAG_
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_TENSOR
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_VOCAB
                    | Setup._DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_
                    | Setup._DCR_CFG_TESSERACT_TIMEOUT
                    | Setup._DCR_CFG_TETML_PAGE
                    | Setup._DCR_CFG_TETML_WORD
                    | Setup._DCR_CFG_TOKENIZE_2_DATABASE
                    | Setup._DCR_CFG_TOKENIZE_2_JSONFILE
                    | Setup._DCR_CFG_VERBOSE
                    | Setup._DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS
                    | Setup._DCR_CFG_VERBOSE_LT_HEADING
                    | Setup._DCR_CFG_VERBOSE_LT_LIST_BULLET
                    | Setup._DCR_CFG_VERBOSE_LT_LIST_NUMBER
                    | Setup._DCR_CFG_VERBOSE_LT_TABLE
                    | Setup._DCR_CFG_VERBOSE_LT_TOC
                    | Setup._DCR_CFG_VERBOSE_PARSER
                ):
                    continue
                case Setup._DCR_CFG_LT_HEADING_RULE_FILE:
                    self.lt_heading_rule_file = utils.get_os_independent_name(item)
                case Setup._DCR_CFG_LT_LIST_BULLET_RULE_FILE:
                    self.lt_list_bullet_rule_file = utils.get_os_independent_name(item)
                case Setup._DCR_CFG_LT_LIST_NUMBER_RULE_FILE:
                    self.lt_list_number_rule_file = utils.get_os_independent_name(item)
                case _:
                    utils.terminate_fatal_setup(f"Unknown configuration parameter '{key}'")

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
