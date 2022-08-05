import collections
from typing import ClassVar

class NLPCore:
    ParserLineLine = dict[str, int | str]
    ParserLineLines = list[ParserLineLine]

    ParserLinePage = dict[str, int | ParserLineLines]
    ParserLinePages = list[ParserLinePage]

    ParserLineDocument = dict[str, int | ParserLinePages | str]

    ParserPagePara = dict[str, int | str]
    ParserPageParas = list[ParserPagePara]

    ParserPagePage = dict[str, int | ParserPageParas]
    ParserPagePages = list[ParserPagePage]

    ParserPageDocument = dict[str, int | ParserPagePages | str]

    ParserWordWord = dict[str, int | str]
    ParserWordWords = list[ParserWordWord]

    ParserWordLine = dict[str, int | ParserWordWords]
    ParserWordLines = list[ParserWordLine]

    ParserWordPara = dict[str, int | ParserWordLines]
    ParserWordParas = list[ParserWordPara]

    ParserWordPage = dict[str, int | str | ParserWordParas]
    ParserWordPages = list[ParserWordPage]

    ParserWordDocument = dict[str, int | str | ParserWordPages]

    CODE_SPACY_DEFAULT: ClassVar[str]

    ENVIRONMENT_TYPE_DEV: ClassVar[str]
    ENVIRONMENT_TYPE_PROD: ClassVar[str]
    ENVIRONMENT_TYPE_TEST: ClassVar[str]

    JSON_NAME_BULLET: ClassVar[str]
    JSON_NAME_COLUMNS: ClassVar[str]
    JSON_NAME_COLUMN_NO: ClassVar[str]
    JSON_NAME_COLUMN_SPAN: ClassVar[str]
    JSON_NAME_COORD_LLX: ClassVar[str]
    JSON_NAME_COORD_URX: ClassVar[str]
    JSON_NAME_DOC_FILE_NAME: ClassVar[str]
    JSON_NAME_DOC_ID: ClassVar[str]
    JSON_NAME_ENTRIES: ClassVar[str]
    JSON_NAME_ENTRY_NO: ClassVar[str]
    JSON_NAME_FIRST_COLUMN_LLX: ClassVar[str]
    JSON_NAME_FIRST_ENTRY_LLX: ClassVar[str]
    JSON_NAME_FIRST_ROW_LLX: ClassVar[str]
    JSON_NAME_FIRST_ROW_URX: ClassVar[str]
    JSON_NAME_FUNCTION_IS_ASC: ClassVar[str]
    JSON_NAME_HEADING_CTX_LINE: ClassVar[str]
    JSON_NAME_HEADING_LEVEL: ClassVar[str]
    JSON_NAME_HEADING_TEXT: ClassVar[str]
    JSON_NAME_IS_FIRST_TOKEN: ClassVar[str]
    JSON_NAME_LAST_COLUMN_URX: ClassVar[str]
    JSON_NAME_LINES: ClassVar[str]
    JSON_NAME_LINE_NO: ClassVar[str]
    JSON_NAME_LINE_NO_PAGE: ClassVar[str]
    JSON_NAME_LINE_NO_PAGE_FROM: ClassVar[str]
    JSON_NAME_LINE_NO_PAGE_TILL: ClassVar[str]
    JSON_NAME_LINE_TYPE: ClassVar[str]
    JSON_NAME_LINE_TYPE_ANTI_PATTERNS: ClassVar[str]
    JSON_NAME_LINE_TYPE_RULES: ClassVar[str]
    JSON_NAME_LIST_NO: ClassVar[str]
    JSON_NAME_LISTS_BULLET: ClassVar[str]
    JSON_NAME_LISTS_NUMBER: ClassVar[str]
    JSON_NAME_NAME: ClassVar[str]
    JSON_NAME_NO_COLUMNS: ClassVar[str]
    JSON_NAME_NO_ENTRIES: ClassVar[str]
    JSON_NAME_NO_LINES_FOOTER: ClassVar[str]
    JSON_NAME_NO_LINES_HEADER: ClassVar[str]
    JSON_NAME_NO_LINES_IN_DOC: ClassVar[str]
    JSON_NAME_NO_LINES_IN_PAGE: ClassVar[str]
    JSON_NAME_NO_LINES_IN_PARA: ClassVar[str]
    JSON_NAME_NO_LINES_TOC: ClassVar[str]
    JSON_NAME_NO_LISTS_BULLET_IN_DOC: ClassVar[str]
    JSON_NAME_NO_LISTS_NUMBER_IN_DOC: ClassVar[str]
    JSON_NAME_NO_PAGES_IN_DOC: ClassVar[str]
    JSON_NAME_NO_PARAS_IN_DOC: ClassVar[str]
    JSON_NAME_NO_PARAS_IN_PAGE: ClassVar[str]
    JSON_NAME_NO_ROWS: ClassVar[str]
    JSON_NAME_NO_SENTS_IN_DOC: ClassVar[str]
    JSON_NAME_NO_SENTS_IN_PAGE: ClassVar[str]
    JSON_NAME_NO_SENTS_IN_PARA: ClassVar[str]
    JSON_NAME_NO_TABLES_IN_DOC: ClassVar[str]
    JSON_NAME_NO_TITLES_IN_DOC: ClassVar[str]
    JSON_NAME_NO_TOKENS_IN_DOC: ClassVar[str]
    JSON_NAME_NO_TOKENS_IN_PAGE: ClassVar[str]
    JSON_NAME_NO_TOKENS_IN_PARA: ClassVar[str]
    JSON_NAME_NO_TOKENS_IN_SENT: ClassVar[str]
    JSON_NAME_NO_WORDS_IN_DOC: ClassVar[str]
    JSON_NAME_NO_WORDS_IN_LINE: ClassVar[str]
    JSON_NAME_NO_WORDS_IN_PAGE: ClassVar[str]
    JSON_NAME_NO_WORDS_IN_PARA: ClassVar[str]
    JSON_NAME_NUMBER: ClassVar[str]
    JSON_NAME_PAGES: ClassVar[str]
    JSON_NAME_PAGE_NO: ClassVar[str]
    JSON_NAME_PAGE_NO_FROM: ClassVar[str]
    JSON_NAME_PAGE_NO_TILL: ClassVar[str]
    JSON_NAME_PARAS: ClassVar[str]
    JSON_NAME_PARA_NO: ClassVar[str]

    JSON_NAME_REGEXP: ClassVar[str]
    JSON_NAME_ROWS: ClassVar[str]
    JSON_NAME_ROW_NO: ClassVar[str]
    JSON_NAME_SENTS: ClassVar[str]
    JSON_NAME_SENT_NO: ClassVar[str]
    JSON_NAME_START_VALUES: ClassVar[str]
    JSON_NAME_TABLES: ClassVar[str]
    JSON_NAME_TABLE_NO: ClassVar[str]
    JSON_NAME_TEXT: ClassVar[str]
    JSON_NAME_TOC: ClassVar[str]
    JSON_NAME_TITLES: ClassVar[str]
    JSON_NAME_TOKENS: ClassVar[str]
    JSON_NAME_TOKEN_CLUSTER: ClassVar[str]
    JSON_NAME_TOKEN_DEP_: ClassVar[str]
    JSON_NAME_TOKEN_DOC: ClassVar[str]
    JSON_NAME_TOKEN_ENT_IOB_: ClassVar[str]
    JSON_NAME_TOKEN_ENT_KB_ID_: ClassVar[str]
    JSON_NAME_TOKEN_ENT_TYPE_: ClassVar[str]
    JSON_NAME_TOKEN_HEAD: ClassVar[str]
    JSON_NAME_TOKEN_I: ClassVar[str]
    JSON_NAME_TOKEN_IDX: ClassVar[str]
    JSON_NAME_TOKEN_IS_ALPHA: ClassVar[str]
    JSON_NAME_TOKEN_IS_ASCII: ClassVar[str]
    JSON_NAME_TOKEN_IS_BRACKET: ClassVar[str]
    JSON_NAME_TOKEN_IS_CURRENCY: ClassVar[str]
    JSON_NAME_TOKEN_IS_DIGIT: ClassVar[str]
    JSON_NAME_TOKEN_IS_LEFT_PUNCT: ClassVar[str]
    JSON_NAME_TOKEN_IS_LOWER: ClassVar[str]
    JSON_NAME_TOKEN_IS_OOV: ClassVar[str]
    JSON_NAME_TOKEN_IS_PUNCT: ClassVar[str]
    JSON_NAME_TOKEN_IS_QUOTE: ClassVar[str]
    JSON_NAME_TOKEN_IS_RIGHT_PUNCT: ClassVar[str]
    JSON_NAME_TOKEN_IS_SENT_END: ClassVar[str]
    JSON_NAME_TOKEN_IS_SENT_START: ClassVar[str]
    JSON_NAME_TOKEN_IS_SPACE: ClassVar[str]
    JSON_NAME_TOKEN_IS_STOP: ClassVar[str]
    JSON_NAME_TOKEN_IS_TITLE: ClassVar[str]
    JSON_NAME_TOKEN_IS_UPPER: ClassVar[str]
    JSON_NAME_TOKEN_LANG_: ClassVar[str]
    JSON_NAME_TOKEN_LEFT_EDGE: ClassVar[str]
    JSON_NAME_TOKEN_LEMMA_: ClassVar[str]
    JSON_NAME_TOKEN_LEX: ClassVar[str]
    JSON_NAME_TOKEN_LEX_ID: ClassVar[str]
    JSON_NAME_TOKEN_LIKE_EMAIL: ClassVar[str]
    JSON_NAME_TOKEN_LIKE_NUM: ClassVar[str]
    JSON_NAME_TOKEN_LIKE_URL: ClassVar[str]
    JSON_NAME_TOKEN_LOWER_: ClassVar[str]
    JSON_NAME_TOKEN_MORPH: ClassVar[str]
    JSON_NAME_TOKEN_NORM_: ClassVar[str]
    JSON_NAME_TOKEN_ORTH_: ClassVar[str]
    JSON_NAME_TOKEN_POS_: ClassVar[str]
    JSON_NAME_TOKEN_PREFIX_: ClassVar[str]
    JSON_NAME_TOKEN_PROB: ClassVar[str]
    JSON_NAME_TOKEN_RANK: ClassVar[str]
    JSON_NAME_TOKEN_RIGHT_EDGE: ClassVar[str]
    JSON_NAME_TOKEN_SENT: ClassVar[str]
    JSON_NAME_TOKEN_SENTIMENT: ClassVar[str]
    JSON_NAME_TOKEN_SHAPE_: ClassVar[str]
    JSON_NAME_TOKEN_SUFFIX_: ClassVar[str]
    JSON_NAME_TOKEN_TAG_: ClassVar[str]
    JSON_NAME_TOKEN_TENSOR: ClassVar[str]
    JSON_NAME_TOKEN_TEXT: ClassVar[str]
    JSON_NAME_TOKEN_TEXT_WITH_WS: ClassVar[str]
    JSON_NAME_TOKEN_WHITESPACE_: ClassVar[str]
    JSON_NAME_UPPER_RIGHT_X: ClassVar[str]
    JSON_NAME_WORDS: ClassVar[str]
    JSON_NAME_WORD_NO: ClassVar[str]

    LINE_TYPE_BODY: ClassVar[str]
    LINE_TYPE_FOOTER: ClassVar[str]
    LINE_TYPE_HEADER: ClassVar[str]
    LINE_TYPE_HEADING: ClassVar[str]
    LINE_TYPE_LIST_BULLET: ClassVar[str]
    LINE_TYPE_LIST_NUMBER: ClassVar[str]
    LINE_TYPE_TABLE: ClassVar[str]
    LINE_TYPE_TOC: ClassVar[str]

    LOGGER_PROGRESS_UPDATE: ClassVar[str]

    PARSE_NAME_SPACE: ClassVar[str]
    PARSE_ATTR_COL_SPAN: ClassVar[str]
    PARSE_ATTR_LLX: ClassVar[str]
    PARSE_ATTR_URX: ClassVar[str]
    PARSE_ELEM_ACTION: ClassVar[str]
    PARSE_ELEM_ANNOTATIONS: ClassVar[str]
    PARSE_ELEM_ATTACHMENTS: ClassVar[str]
    PARSE_ELEM_AUTHOR: ClassVar[str]
    PARSE_ELEM_BOOKMARK: ClassVar[str]
    PARSE_ELEM_BOOKMARKS: ClassVar[str]
    PARSE_ELEM_BOX: ClassVar[str]
    PARSE_ELEM_CELL: ClassVar[str]
    PARSE_ELEM_CONTENT: ClassVar[str]
    PARSE_ELEM_CREATION: ClassVar[str]
    PARSE_ELEM_CREATION_DATE: ClassVar[str]
    PARSE_ELEM_CREATOR: ClassVar[str]
    PARSE_ELEM_CUSTOM: ClassVar[str]
    PARSE_ELEM_DESTINATIONS: ClassVar[str]
    PARSE_ELEM_DOCUMENT: ClassVar[str]
    PARSE_ELEM_DOCUMENT_INFO: ClassVar[str]
    PARSE_ELEM_ENCRYPTION: ClassVar[str]
    PARSE_ELEM_EXCEPTION: ClassVar[str]
    PARSE_ELEM_FIELDS: ClassVar[str]
    PARSE_ELEM_FROM: ClassVar[int]
    PARSE_ELEM_GRAPHICS: ClassVar[str]
    PARSE_ELEM_JAVA_SCRIPTS: ClassVar[str]
    PARSE_ELEM_LINE: ClassVar[str]
    PARSE_ELEM_METADATA: ClassVar[str]
    PARSE_ELEM_MOD_DATE: ClassVar[str]
    PARSE_ELEM_OPTIONS: ClassVar[str]
    PARSE_ELEM_OUTPUT_INTENTS: ClassVar[str]
    PARSE_ELEM_PAGE: ClassVar[str]
    PARSE_ELEM_PAGES: ClassVar[str]
    PARSE_ELEM_PARA: ClassVar[str]
    PARSE_ELEM_PLACED_IMAGE: ClassVar[str]
    PARSE_ELEM_PRODUCER: ClassVar[str]
    PARSE_ELEM_RESOURCES: ClassVar[str]
    PARSE_ELEM_ROW: ClassVar[str]
    PARSE_ELEM_SIGNATURE_FIELDS: ClassVar[str]
    PARSE_ELEM_TABLE: ClassVar[str]
    PARSE_ELEM_TEXT: ClassVar[str]
    PARSE_ELEM_TITLE: ClassVar[str]
    PARSE_ELEM_WORD: ClassVar[str]
    PARSE_ELEM_XFA: ClassVar[str]

    SEARCH_STRATEGY_LINES: ClassVar[str]
    SEARCH_STRATEGY_TABLE: ClassVar[str]

    def __init__(self) -> None:
        self._exist = None
    @classmethod
    def _convert_roman_2_int(cls, roman_in: str) -> int: ...
    @staticmethod
    def _get_lt_anti_patterns_default_heading() -> list[tuple[str, str]]: ...
    @staticmethod
    def _get_lt_anti_patterns_default_list_bullet(environment_variant: str) -> list[tuple[str, str]]: ...
    @staticmethod
    def _get_lt_anti_patterns_default_list_number(environment_variant: str) -> list[tuple[str, str]]: ...
    @staticmethod
    def _get_lt_rules_default_heading_list_number() -> list[
        tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]
    ]: ...
    @staticmethod
    def _get_lt_rules_default_list_bullet() -> dict[str, int]: ...
    def exists(self) -> bool: ...
    @staticmethod
    def export_rule_file_heading(
        is_verbose: bool, file_name: str, file_encoding: str, json_indent: str, is_json_sort_keys: bool
    ) -> None: ...
    @staticmethod
    def export_rule_file_list_bullet(
        is_verbose: bool,
        file_name: str,
        file_encoding: str,
        json_indent: str,
        is_json_sort_keys: bool,
        environment_variant: str,
    ) -> None: ...
    @staticmethod
    def export_rule_file_list_number(
        is_verbose: bool,
        file_name: str,
        file_encoding: str,
        json_indent: str,
        is_json_sort_keys: bool,
        environment_variant: str,
    ) -> None: ...
    @staticmethod
    def get_lt_anti_patterns_default_heading() -> list[
        tuple[
            str,
            str,
        ]
    ]: ...
    @staticmethod
    def get_lt_anti_patterns_default_list_bullet(
        environment_variant: str,
    ) -> list[tuple[str, str]]: ...
    @staticmethod
    def get_lt_anti_patterns_default_list_number(environment_variant: str) -> list[tuple[str, str]]: ...
    @staticmethod
    def get_lt_rules_default_heading() -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]: ...
    @staticmethod
    def get_lt_rules_default_list_bullet() -> dict[str, int]: ...
    @staticmethod
    def get_lt_rules_default_list_number() -> list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]: ...
    @classmethod
    def is_asc_ignore(cls, _predecessor: str, _successor: str) -> bool: ...
    @classmethod
    def is_asc_lowercase_letters(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_lowercase_letters_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_romans(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_romans_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_strings(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_floats(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_floats_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_integers(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_string_integers_token(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_uppercase_letters(cls, predecessor: str, successor: str) -> bool: ...
    @classmethod
    def is_asc_uppercase_letters_token(cls, predecessor: str, successor: str) -> bool: ...
