import configparser
from typing import ClassVar

class Setup:
    _CONFIG_PARAM_NO: ClassVar[int]

    _DCR_CFG_CREATE_EXTRA_FILE_HEADING: ClassVar[str]
    _DCR_CFG_CREATE_EXTRA_FILE_LIST_BULLET: ClassVar[str]
    _DCR_CFG_CREATE_EXTRA_FILE_LIST_NUMBER: ClassVar[str]
    _DCR_CFG_CREATE_EXTRA_FILE_TABLE: ClassVar[str]
    _DCR_CFG_FILE: ClassVar[str]
    _DCR_CFG_JSON_INDENT: ClassVar[str]
    _DCR_CFG_JSON_SORT_KEYS: ClassVar[str]
    _DCR_CFG_LT_EXPORT_RULE_FILE_HEADING: ClassVar[str]
    _DCR_CFG_LT_EXPORT_RULE_FILE_LIST_BULLET: ClassVar[str]
    _DCR_CFG_LT_EXPORT_RULE_FILE_LIST_NUMBER: ClassVar[str]
    _DCR_CFG_LT_FOOTER_MAX_DISTANCE: ClassVar[str]
    _DCR_CFG_LT_FOOTER_MAX_LINES: ClassVar[str]
    _DCR_CFG_LT_HEADER_MAX_DISTANCE: ClassVar[str]
    _DCR_CFG_LT_HEADER_MAX_LINES: ClassVar[str]
    _DCR_CFG_LT_HEADING_FILE_INCL_NO_CTX: ClassVar[str]
    _DCR_CFG_LT_HEADING_FILE_INCL_REGEXP: ClassVar[str]
    _DCR_CFG_LT_HEADING_MAX_LEVEL: ClassVar[str]
    _DCR_CFG_LT_HEADING_MIN_PAGES: ClassVar[str]
    _DCR_CFG_LT_HEADING_RULE_FILE: ClassVar[str]
    _DCR_CFG_LT_HEADING_TOLERANCE_LLX: ClassVar[str]
    _DCR_CFG_LT_LIST_BULLET_MIN_ENTRIES: ClassVar[str]
    _DCR_CFG_LT_LIST_BULLET_RULE_FILE: ClassVar[str]
    _DCR_CFG_LT_LIST_BULLET_TOLERANCE_LLX: ClassVar[str]
    _DCR_CFG_LT_LIST_NUMBER_FILE_INCL_REGEXP: ClassVar[str]
    _DCR_CFG_LT_LIST_NUMBER_MIN_ENTRIES: ClassVar[str]
    _DCR_CFG_LT_LIST_NUMBER_RULE_FILE: ClassVar[str]
    _DCR_CFG_LT_LIST_NUMBER_TOLERANCE_LLX: ClassVar[str]
    _DCR_CFG_LT_TABLE_FILE_INCL_EMPTY_COLUMNS: ClassVar[str]
    _DCR_CFG_LT_TOC_LAST_PAGE: ClassVar[str]
    _DCR_CFG_LT_TOC_MIN_ENTRIES: ClassVar[str]
    _DCR_CFG_PDF2IMAGE_TYPE: ClassVar[str]
    _DCR_CFG_SECTION: ClassVar[str]
    _DCR_CFG_SECTION_ENV_TEST: ClassVar[str]
    _DCR_CFG_SECTION_SPACY: ClassVar[str]

    _DCR_CFG_SPACY_IGNORE_BRACKET: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LEFT_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_FOOTER: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_HEADER: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_HEADING: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_LIST_BULLET: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_LIST_NUMBER: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_TABLE: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_LINE_TYPE_TOC: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_QUOTE: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_RIGHT_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_SPACE: ClassVar[str]
    _DCR_CFG_SPACY_IGNORE_STOP: ClassVar[str]

    _DCR_CFG_SPACY_TKN_ATTR_CLUSTER: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_DEP_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_DOC: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_ENT_IOB_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_ENT_KB_ID_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_ENT_TYPE_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_HEAD: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_I: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IDX: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_ALPHA: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_ASCII: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_BRACKET: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_CURRENCY: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_DIGIT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_LEFT_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_LOWER: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_OOV: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_QUOTE: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_RIGHT_PUNCT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_SENT_END: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_SENT_START: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_SPACE: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_STOP: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_TITLE: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_IS_UPPER: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LANG_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LEFT_EDGE: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LEMMA_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LEX: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LEX_ID: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_EMAIL: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_NUM: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LIKE_URL: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_LOWER_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_MORPH: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_NORM_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_ORTH_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_POS_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_PREFIX_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_PROB: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_RANK: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_RIGHT_EDGE: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_SENT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_SENTIMENT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_SHAPE_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_SUFFIX_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_TAG_: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_TENSOR: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_TEXT: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_TEXT_WITH_WS: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_VOCAB: ClassVar[str]
    _DCR_CFG_SPACY_TKN_ATTR_WHITESPACE_: ClassVar[str]

    _DCR_CFG_TESSERACT_TIMEOUT: ClassVar[str]
    _DCR_CFG_TETML_PAGE: ClassVar[str]
    _DCR_CFG_TETML_WORD: ClassVar[str]
    _DCR_CFG_TOKENIZE_2_DATABASE: ClassVar[str]
    _DCR_CFG_TOKENIZE_2_JSONFILE: ClassVar[str]
    _DCR_CFG_VERBOSE: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_HEADERS_FOOTERS: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_HEADING: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_LIST_BULLET: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_LIST_NUMBER: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_TABLE: ClassVar[str]
    _DCR_CFG_VERBOSE_LT_TOC: ClassVar[str]
    _DCR_CFG_VERBOSE_PARSER: ClassVar[str]

    _DCR_ENVIRONMENT_TYPE: ClassVar[str]

    DCR_VERSION: ClassVar[str]

    ENVIRONMENT_TYPE_DEV: ClassVar[str]
    ENVIRONMENT_TYPE_PROD: ClassVar[str]
    ENVIRONMENT_TYPE_TEST: ClassVar[str]

    PDF2IMAGE_TYPE_JPEG: ClassVar[str]
    PDF2IMAGE_TYPE_PNG: ClassVar[str]

    def __init__(self) -> None:
        self._config: dict[str, str] = {}
        self._config_parser: configparser.ConfigParser = configparser.ConfigParser()
        self._exist: bool = False
        self.db_initial_data_file: str = ""
        self.directory_inbox: str = ""
        self.directory_inbox_accepted: str = ""
        self.directory_inbox_rejected: str = ""
        self.environment_variant: str = ""
        self.is_create_extra_file_heading: bool = False
        self.is_create_extra_file_list_bullet: bool = False
        self.is_create_extra_file_list_number: bool = False
        self.is_create_extra_file_table: bool = False
        self.is_json_sort_keys: bool = False
        self.is_lt_heading_file_incl_regexp: bool = False
        self.is_lt_list_number_file_incl_regexp: bool = False
        self.is_lt_table_file_incl_empty_columns: bool = False
        self.is_parsing_line: bool = False
        self.is_parsing_page: bool = False
        self.is_parsing_word: bool = False
        self.is_spacy_ignore_bracket: bool = False
        self.is_spacy_ignore_left_punct: bool = False
        self.is_spacy_ignore_line_type_footer: bool = False
        self.is_spacy_ignore_line_type_header: bool = False
        self.is_spacy_ignore_line_type_heading = False
        self.is_spacy_ignore_line_type_list_bullet = False
        self.is_spacy_ignore_line_type_list_number = False
        self.is_spacy_ignore_line_type_table = False
        self.is_spacy_ignore_line_type_toc: bool = False
        self.is_spacy_ignore_punct: bool = False
        self.is_spacy_ignore_quote: bool = False
        self.is_spacy_ignore_right_punct: bool = False
        self.is_spacy_ignore_space: bool = False
        self.is_spacy_ignore_stop: bool = False
        self.is_spacy_tkn_attr_cluster: bool = False
        self.is_spacy_tkn_attr_dep_: bool = False
        self.is_spacy_tkn_attr_doc: bool = False
        self.is_spacy_tkn_attr_ent_iob_: bool = False
        self.is_spacy_tkn_attr_ent_kb_id_: bool = False
        self.is_spacy_tkn_attr_ent_type_: bool = False
        self.is_spacy_tkn_attr_head: bool = False
        self.is_spacy_tkn_attr_i: bool = False
        self.is_spacy_tkn_attr_idx: bool = False
        self.is_spacy_tkn_attr_is_alpha: bool = False
        self.is_spacy_tkn_attr_is_ascii: bool = False
        self.is_spacy_tkn_attr_is_bracket: bool = False
        self.is_spacy_tkn_attr_is_currency: bool = False
        self.is_spacy_tkn_attr_is_digit: bool = False
        self.is_spacy_tkn_attr_is_left_punct: bool = False
        self.is_spacy_tkn_attr_is_lower: bool = False
        self.is_spacy_tkn_attr_is_oov: bool = False
        self.is_spacy_tkn_attr_is_punct: bool = False
        self.is_spacy_tkn_attr_is_quote: bool = False
        self.is_spacy_tkn_attr_is_right_punct: bool = False
        self.is_spacy_tkn_attr_is_sent_end: bool = False
        self.is_spacy_tkn_attr_is_sent_start: bool = False
        self.is_spacy_tkn_attr_is_space: bool = False
        self.is_spacy_tkn_attr_is_stop: bool = False
        self.is_spacy_tkn_attr_is_title: bool = False
        self.is_spacy_tkn_attr_is_upper: bool = False
        self.is_spacy_tkn_attr_lang_: bool = False
        self.is_spacy_tkn_attr_left_edge: bool = False
        self.is_spacy_tkn_attr_lemma_: bool = False
        self.is_spacy_tkn_attr_lex: bool = False
        self.is_spacy_tkn_attr_lex_id: bool = False
        self.is_spacy_tkn_attr_like_email: bool = False
        self.is_spacy_tkn_attr_like_num: bool = False
        self.is_spacy_tkn_attr_like_url: bool = False
        self.is_spacy_tkn_attr_lower_: bool = False
        self.is_spacy_tkn_attr_morph: bool = False
        self.is_spacy_tkn_attr_norm_: bool = False
        self.is_spacy_tkn_attr_orth_: bool = False
        self.is_spacy_tkn_attr_pos_: bool = False
        self.is_spacy_tkn_attr_prefix_: bool = False
        self.is_spacy_tkn_attr_prob: bool = False
        self.is_spacy_tkn_attr_rank: bool = False
        self.is_spacy_tkn_attr_right_edge: bool = False
        self.is_spacy_tkn_attr_sent: bool = False
        self.is_spacy_tkn_attr_sentiment: bool = False
        self.is_spacy_tkn_attr_shape_: bool = False
        self.is_spacy_tkn_attr_suffix_: bool = False
        self.is_spacy_tkn_attr_tag_: bool = False
        self.is_spacy_tkn_attr_tensor: bool = False
        self.is_spacy_tkn_attr_text: bool = False
        self.is_spacy_tkn_attr_text_with_ws: bool = False
        self.is_spacy_tkn_attr_vocab: bool = False
        self.is_spacy_tkn_attr_whitespace_: bool = False
        self.is_tetml_page: bool = False
        self.is_tetml_word: bool = False
        self.is_tokenize_2_database: bool = False
        self.is_tokenize_2_jsonfile: bool = False
        self.is_verbose: bool = False
        self.is_verbose_lt_headers_footers: bool = False
        self.is_verbose_lt_heading: bool = False
        self.is_verbose_lt_list_bullet: bool = False
        self.is_verbose_lt_list_number: bool = False
        self.is_verbose_lt_table: bool = False
        self.is_verbose_lt_toc: bool = False
        self.json_indent: int = 0
        self.lt_export_rule_file_heading: str = ""
        self.lt_export_rule_file_list_bullet: str = ""
        self.lt_export_rule_file_list_number: str = ""
        self.lt_footer_max_distance: int = 0
        self.lt_footer_max_lines: int = 0
        self.lt_header_max_distance: int = 0
        self.lt_header_max_lines: int = 0
        self.lt_heading_file_incl_no_ctx: int = 0
        self.lt_heading_max_level: int = 0
        self.lt_heading_min_pages: int = 0
        self.lt_heading_rule_file: str = ""
        self.lt_heading_tolerance_llx: int = 0
        self.lt_list_bullet_min_entries: int = 0
        self.lt_list_bullet_rule_file: str = ""
        self.lt_list_bullet_tolerance_llx: int = 0
        self.lt_list_number_min_entries: int = 0
        self.lt_list_number_rule_file: str = ""
        self.lt_list_number_tolerance_llx: int = 0
        self.lt_toc_last_page: int = 0
        self.lt_toc_min_entries: int = 0
        self.pdf2image_type: str = ""
        self.tesseract_timeout: int = 0
        self.verbose_parser: str = ""
        ...
    def _check_config_core(self) -> None: ...
    def _check_config_pdf2image_type(self) -> None: ...
    def _check_config_verbose_parser(self) -> None: ...
    def _determine_config_param_boolean(
        self,
        param: str,
        var: bool,
    ) -> bool: ...
    def _determine_config_param_integer(
        self,
        param: str,
        var: int,
    ) -> int: ...
    def _determine_config_spacy_tkn(self) -> None: ...
    def _determine_config_spacy_tkn_ignore(self) -> None: ...
    def _get_environment_variant(self) -> None: ...
    def _load_config_core(self) -> None: ...
    def exists(self) -> bool: ...
