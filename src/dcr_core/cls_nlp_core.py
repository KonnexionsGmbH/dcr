import collections
import json
import re
from typing import ClassVar

import dcr_core.core_utils


class NLPCore:
    """Managing the NLP processing.

    Returns:
        _type_: LineType instance.
    """

    # -----------------------------------------------------------------------------
    # Global type aliases.
    # -----------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    CODE_SPACY_DEFAULT: ClassVar[str] = "en_core_web_trf"

    ENVIRONMENT_TYPE_DEV: ClassVar[str] = "dev"
    ENVIRONMENT_TYPE_PROD: ClassVar[str] = "prod"
    ENVIRONMENT_TYPE_TEST: ClassVar[str] = "test"

    JSON_NAME_BULLET: ClassVar[str] = "bullet"

    JSON_NAME_COLUMNS: ClassVar[str] = "columns"
    JSON_NAME_COLUMN_NO: ClassVar[str] = "columnNo"
    JSON_NAME_COLUMN_SPAN: ClassVar[str] = "columnSpan"
    JSON_NAME_COORD_LLX: ClassVar[str] = "coordLLX"
    JSON_NAME_COORD_URX: ClassVar[str] = "coordURX"
    JSON_NAME_DOC_FILE_NAME: ClassVar[str] = "documentFileName"

    JSON_NAME_DOC_ID: ClassVar[str] = "documentId"

    JSON_NAME_ENTRIES: ClassVar[str] = "entries"
    JSON_NAME_ENTRY_NO: ClassVar[str] = "entryNo"

    JSON_NAME_FIRST_COLUMN_LLX: ClassVar[str] = "firstColumnLLX"
    JSON_NAME_FIRST_ENTRY_LLX: ClassVar[str] = "firstEntryLLX"
    JSON_NAME_FIRST_ROW_LLX: ClassVar[str] = "firstRowLLX"
    JSON_NAME_FIRST_ROW_URX: ClassVar[str] = "firstRowURX"
    JSON_NAME_FUNCTION_IS_ASC: ClassVar[str] = "functionIsAsc"

    JSON_NAME_HEADING_CTX_LINE: ClassVar[str] = "headingCtxLine"
    JSON_NAME_HEADING_LEVEL: ClassVar[str] = "headingLevel"
    JSON_NAME_HEADING_TEXT: ClassVar[str] = "headingText"

    JSON_NAME_IS_FIRST_TOKEN: ClassVar[str] = "isFirstToken"

    JSON_NAME_LAST_COLUMN_URX: ClassVar[str] = "lastColumnURX"
    JSON_NAME_LINES: ClassVar[str] = "lines"
    JSON_NAME_LINE_NO: ClassVar[str] = "lineNo"
    JSON_NAME_LINE_NO_PAGE: ClassVar[str] = "lineNoPage"
    JSON_NAME_LINE_NO_PAGE_FROM: ClassVar[str] = "lineNoPageFrom"
    JSON_NAME_LINE_NO_PAGE_TILL: ClassVar[str] = "lineNoPageTill"
    JSON_NAME_LINE_TYPE: ClassVar[str] = "lineType"
    JSON_NAME_LINE_TYPE_ANTI_PATTERNS: ClassVar[str] = "lineTypeAntiPatterns"
    JSON_NAME_LINE_TYPE_RULES: ClassVar[str] = "lineTypeRules"
    JSON_NAME_LIST_NO: ClassVar[str] = "listNo"
    JSON_NAME_LISTS_BULLET: ClassVar[str] = "listsBullet"
    JSON_NAME_LISTS_NUMBER: ClassVar[str] = "listsNumber"

    JSON_NAME_NAME: ClassVar[str] = "name"
    JSON_NAME_NO_COLUMNS: ClassVar[str] = "noColumns"
    JSON_NAME_NO_ENTRIES: ClassVar[str] = "noEntries"
    JSON_NAME_NO_LINES_FOOTER: ClassVar[str] = "noLinesFooter"
    JSON_NAME_NO_LINES_HEADER: ClassVar[str] = "noLinesHeader"
    JSON_NAME_NO_LINES_IN_DOC: ClassVar[str] = "noLinesInDocument"
    JSON_NAME_NO_LINES_IN_PAGE: ClassVar[str] = "noLinesInPage"
    JSON_NAME_NO_LINES_IN_PARA: ClassVar[str] = "noLinesInParagraph"
    JSON_NAME_NO_LINES_TOC: ClassVar[str] = "noLinesToc"
    JSON_NAME_NO_LISTS_BULLET_IN_DOC: ClassVar[str] = "noListsBulletInDocument"
    JSON_NAME_NO_LISTS_NUMBER_IN_DOC: ClassVar[str] = "noListsNumberInDocument"
    JSON_NAME_NO_PAGES_IN_DOC: ClassVar[str] = "noPagesInDocument"
    JSON_NAME_NO_PARAS_IN_DOC: ClassVar[str] = "noParagraphsInDocument"
    JSON_NAME_NO_PARAS_IN_PAGE: ClassVar[str] = "noParagraphsInPage"
    JSON_NAME_NO_ROWS: ClassVar[str] = "noRows"
    JSON_NAME_NO_SENTS_IN_DOC: ClassVar[str] = "noSentencesInDocument"
    JSON_NAME_NO_SENTS_IN_PAGE: ClassVar[str] = "noSentencesInPage"
    JSON_NAME_NO_SENTS_IN_PARA: ClassVar[str] = "noSentencesInParagraph"
    JSON_NAME_NO_TABLES_IN_DOC: ClassVar[str] = "noTablesInDocument"
    JSON_NAME_NO_TITLES_IN_DOC: ClassVar[str] = "noTitlesInDocument"
    JSON_NAME_NO_TOKENS_IN_DOC: ClassVar[str] = "noTokensInDocument"
    JSON_NAME_NO_TOKENS_IN_PAGE: ClassVar[str] = "noTokensInPage"
    JSON_NAME_NO_TOKENS_IN_PARA: ClassVar[str] = "noTokensInParagraph"
    JSON_NAME_NO_TOKENS_IN_SENT: ClassVar[str] = "noTokensInSentence"
    JSON_NAME_NO_WORDS_IN_DOC: ClassVar[str] = "noWordsInDocument"
    JSON_NAME_NO_WORDS_IN_LINE: ClassVar[str] = "noWordsInLine"
    JSON_NAME_NO_WORDS_IN_PAGE: ClassVar[str] = "noWordsInPage"
    JSON_NAME_NO_WORDS_IN_PARA: ClassVar[str] = "noWordsInParagraph"
    JSON_NAME_NUMBER: ClassVar[str] = "number"

    JSON_NAME_PAGES: ClassVar[str] = "pages"
    JSON_NAME_PAGE_NO: ClassVar[str] = "pageNo"
    JSON_NAME_PAGE_NO_FROM: ClassVar[str] = "pageNoFrom"
    JSON_NAME_PAGE_NO_TILL: ClassVar[str] = "pageNoTill"
    JSON_NAME_PARAS: ClassVar[str] = "paragraphs"
    JSON_NAME_PARA_NO: ClassVar[str] = "paragraphNo"

    JSON_NAME_REGEXP: ClassVar[str] = "regexp"
    JSON_NAME_ROWS: ClassVar[str] = "rows"
    JSON_NAME_ROW_NO: ClassVar[str] = "rowNo"

    JSON_NAME_SENTS: ClassVar[str] = "sentences"
    JSON_NAME_SENT_NO: ClassVar[str] = "sentenceNo"
    JSON_NAME_START_VALUES: ClassVar[str] = "startValues"

    JSON_NAME_TABLES: ClassVar[str] = "tables"
    JSON_NAME_TABLE_NO: ClassVar[str] = "tableNo"
    JSON_NAME_TEXT: ClassVar[str] = "text"
    JSON_NAME_TOC: ClassVar[str] = "toc"
    JSON_NAME_TITLES: ClassVar[str] = "titles"
    JSON_NAME_TOKENS: ClassVar[str] = "tokens"

    JSON_NAME_TOKEN_CLUSTER: ClassVar[str] = "tknCluster"
    JSON_NAME_TOKEN_DEP_: ClassVar[str] = "tknDep_"
    JSON_NAME_TOKEN_DOC: ClassVar[str] = "tknDoc"
    JSON_NAME_TOKEN_ENT_IOB_: ClassVar[str] = "tknEntIob_"
    JSON_NAME_TOKEN_ENT_KB_ID_: ClassVar[str] = "tknEntKbId_"
    JSON_NAME_TOKEN_ENT_TYPE_: ClassVar[str] = "tknEntType_"
    JSON_NAME_TOKEN_HEAD: ClassVar[str] = "tknHead"
    JSON_NAME_TOKEN_I: ClassVar[str] = "tknI"
    JSON_NAME_TOKEN_IDX: ClassVar[str] = "tknIdx"
    JSON_NAME_TOKEN_IS_ALPHA: ClassVar[str] = "tknIsAlpha"
    JSON_NAME_TOKEN_IS_ASCII: ClassVar[str] = "tknIsAscii"
    JSON_NAME_TOKEN_IS_BRACKET: ClassVar[str] = "tknIsBracket"
    JSON_NAME_TOKEN_IS_CURRENCY: ClassVar[str] = "tknIsCurrency"
    JSON_NAME_TOKEN_IS_DIGIT: ClassVar[str] = "tknIsDigit"
    JSON_NAME_TOKEN_IS_LEFT_PUNCT: ClassVar[str] = "tknIsLeftPunct"
    JSON_NAME_TOKEN_IS_LOWER: ClassVar[str] = "tknIsLower"
    JSON_NAME_TOKEN_IS_OOV: ClassVar[str] = "tknIsOov"
    JSON_NAME_TOKEN_IS_PUNCT: ClassVar[str] = "tknIsPunct"
    JSON_NAME_TOKEN_IS_QUOTE: ClassVar[str] = "tknIsQuote"
    JSON_NAME_TOKEN_IS_RIGHT_PUNCT: ClassVar[str] = "tknIsRightPunct"
    JSON_NAME_TOKEN_IS_SENT_END: ClassVar[str] = "tknIsSentEnd"
    JSON_NAME_TOKEN_IS_SENT_START: ClassVar[str] = "tknIsSentStart"
    JSON_NAME_TOKEN_IS_SPACE: ClassVar[str] = "tknIsSpace"
    JSON_NAME_TOKEN_IS_STOP: ClassVar[str] = "tknIsStop"
    JSON_NAME_TOKEN_IS_TITLE: ClassVar[str] = "tknIsTitle"
    JSON_NAME_TOKEN_IS_UPPER: ClassVar[str] = "tknIsUpper"
    JSON_NAME_TOKEN_LANG_: ClassVar[str] = "tknLang_"
    JSON_NAME_TOKEN_LEFT_EDGE: ClassVar[str] = "tknLeftEdge"
    JSON_NAME_TOKEN_LEMMA_: ClassVar[str] = "tknLemma_"
    JSON_NAME_TOKEN_LEX: ClassVar[str] = "tknLex"
    JSON_NAME_TOKEN_LEX_ID: ClassVar[str] = "tknLexId"
    JSON_NAME_TOKEN_LIKE_EMAIL: ClassVar[str] = "tknLikeEmail"
    JSON_NAME_TOKEN_LIKE_NUM: ClassVar[str] = "tknLikeNum"
    JSON_NAME_TOKEN_LIKE_URL: ClassVar[str] = "tknLikeUrl"
    JSON_NAME_TOKEN_LOWER_: ClassVar[str] = "tknLower_"
    JSON_NAME_TOKEN_MORPH: ClassVar[str] = "tknMorph"
    JSON_NAME_TOKEN_NORM_: ClassVar[str] = "tknNorm_"
    JSON_NAME_TOKEN_ORTH_: ClassVar[str] = "tknOrth_"
    JSON_NAME_TOKEN_POS_: ClassVar[str] = "tknPos_"
    JSON_NAME_TOKEN_PREFIX_: ClassVar[str] = "tknPrefix_"
    JSON_NAME_TOKEN_PROB: ClassVar[str] = "tknProb"
    JSON_NAME_TOKEN_RANK: ClassVar[str] = "tknRank"
    JSON_NAME_TOKEN_RIGHT_EDGE: ClassVar[str] = "tknRightEdge"
    JSON_NAME_TOKEN_SENT: ClassVar[str] = "tknSent"
    JSON_NAME_TOKEN_SENTIMENT: ClassVar[str] = "tknSentiment"
    JSON_NAME_TOKEN_SHAPE_: ClassVar[str] = "tknShape_"
    JSON_NAME_TOKEN_SUFFIX_: ClassVar[str] = "tknSuffix_"
    JSON_NAME_TOKEN_TAG_: ClassVar[str] = "tknTag_"
    JSON_NAME_TOKEN_TENSOR: ClassVar[str] = "tknTensor"
    JSON_NAME_TOKEN_TEXT: ClassVar[str] = "tknText"
    JSON_NAME_TOKEN_TEXT_WITH_WS: ClassVar[str] = "tknTextWithWs"
    JSON_NAME_TOKEN_WHITESPACE_: ClassVar[str] = "tknWhitespace_"

    JSON_NAME_UPPER_RIGHT_X: ClassVar[str] = "upperRightX"

    JSON_NAME_WORDS: ClassVar[str] = "words"
    JSON_NAME_WORD_NO: ClassVar[str] = "wordNo"

    LINE_TYPE_BODY: ClassVar[str] = "b"
    LINE_TYPE_FOOTER: ClassVar[str] = "f"
    LINE_TYPE_HEADER: ClassVar[str] = "h"
    LINE_TYPE_HEADING: ClassVar[str] = "h_"
    LINE_TYPE_LIST_BULLET: ClassVar[str] = "lb"
    LINE_TYPE_LIST_NUMBER: ClassVar[str] = "ln"
    LINE_TYPE_TABLE: ClassVar[str] = "tab"
    LINE_TYPE_TOC: ClassVar[str] = "toc"

    LOGGER_PROGRESS_UPDATE: ClassVar[str] = "Progress update "

    PARSE_NAME_SPACE: ClassVar[str] = "{http://www.pdflib.com/XML/TET5/TET-5.0}"

    PARSE_ATTR_COL_SPAN: ClassVar[str] = "colSpan"
    PARSE_ATTR_LLX: ClassVar[str] = "llx"
    PARSE_ATTR_URX: ClassVar[str] = "urx"

    PARSE_ELEM_ACTION: ClassVar[str] = "Action"
    PARSE_ELEM_ANNOTATIONS: ClassVar[str] = "Annotations"
    PARSE_ELEM_ATTACHMENTS: ClassVar[str] = "Attachments"
    PARSE_ELEM_AUTHOR: ClassVar[str] = "Author"
    PARSE_ELEM_BOOKMARK: ClassVar[str] = "Bookmark"
    PARSE_ELEM_BOOKMARKS: ClassVar[str] = "Bookmarks"
    PARSE_ELEM_BOX: ClassVar[str] = "Box"
    PARSE_ELEM_CELL: ClassVar[str] = "Cell"
    PARSE_ELEM_CONTENT: ClassVar[str] = "Content"
    PARSE_ELEM_CREATION: ClassVar[str] = "Creation"
    PARSE_ELEM_CREATION_DATE: ClassVar[str] = "CreationDate"
    PARSE_ELEM_CREATOR: ClassVar[str] = "Creator"
    PARSE_ELEM_CUSTOM: ClassVar[str] = "Custom"
    PARSE_ELEM_DESTINATIONS: ClassVar[str] = "Destinations"
    PARSE_ELEM_DOCUMENT: ClassVar[str] = "Document"
    PARSE_ELEM_DOCUMENT_INFO: ClassVar[str] = "DocInfo"
    PARSE_ELEM_ENCRYPTION: ClassVar[str] = "Encryption"
    PARSE_ELEM_EXCEPTION: ClassVar[str] = "Exception"
    PARSE_ELEM_FIELDS: ClassVar[str] = "Fields"
    PARSE_ELEM_FROM: ClassVar[int] = len(PARSE_NAME_SPACE)
    PARSE_ELEM_GRAPHICS: ClassVar[str] = "Graphics"
    PARSE_ELEM_JAVA_SCRIPTS: ClassVar[str] = "JavaScripts"
    PARSE_ELEM_LINE: ClassVar[str] = "Line"
    PARSE_ELEM_METADATA: ClassVar[str] = "Metadata"
    PARSE_ELEM_MOD_DATE: ClassVar[str] = "ModDate"
    PARSE_ELEM_OPTIONS: ClassVar[str] = "Options"
    PARSE_ELEM_OUTPUT_INTENTS: ClassVar[str] = "OutputIntents"
    PARSE_ELEM_PAGE: ClassVar[str] = "Page"
    PARSE_ELEM_PAGES: ClassVar[str] = "Pages"
    PARSE_ELEM_PARA: ClassVar[str] = "Para"
    PARSE_ELEM_PLACED_IMAGE: ClassVar[str] = "PlacedImage"
    PARSE_ELEM_PRODUCER: ClassVar[str] = "Producer"
    PARSE_ELEM_RESOURCES: ClassVar[str] = "Resources"
    PARSE_ELEM_ROW: ClassVar[str] = "Row"
    PARSE_ELEM_SIGNATURE_FIELDS: ClassVar[str] = "SignatureFields"
    PARSE_ELEM_TABLE: ClassVar[str] = "Table"
    PARSE_ELEM_TEXT: ClassVar[str] = "Text"
    PARSE_ELEM_TITLE: ClassVar[str] = "Title"
    PARSE_ELEM_WORD: ClassVar[str] = "Word"
    PARSE_ELEM_XFA: ClassVar[str] = "XFA"

    SEARCH_STRATEGY_LINES: ClassVar[str] = "lines"
    SEARCH_STRATEGY_TABLE: ClassVar[str] = "table"

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        self._exist = True

    # -----------------------------------------------------------------------------
    # Convert a roman numeral to integer.
    # -----------------------------------------------------------------------------
    @classmethod
    def _convert_roman_2_int(cls, roman_in: str) -> int:
        """Convert a roman numeral to integer.

        Args:
            roman_in (str):
                    The roman numeral.

        Returns:
            int:    The corresponding integer.
        """
        roman = re.match(  # type: ignore
            "(m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3}))" + "|(M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))",
            roman_in,
        ).group(0)

        tallies = {
            "i": 1,
            "v": 5,
            "x": 10,
            "l": 50,
            "c": 100,
            "d": 500,
            "m": 1000,
            # specify more numerals if you wish
        }

        integer: int = 0

        for i in range(len(roman) - 1):
            left = roman[i]
            right = roman[i + 1]
            if tallies[left] < tallies[right]:
                integer -= tallies[left]
            else:
                integer += tallies[left]

        integer += tallies[roman[-1]]

        return integer

    # -----------------------------------------------------------------------------
    # Get the default heading line type anti-patterns.
    # -----------------------------------------------------------------------------
    # 1: rule_name
    # 2: regexp_str:
    #           regular expression
    # -----------------------------------------------------------------------------
    @staticmethod
    def _get_lt_anti_patterns_default_heading() -> list[tuple[str, str]]:
        """Get the default heading line type anti-patterns.

        Returns:
            list[tuple[str, str]]:
                The heading line type anti-patterns.
        """
        return [
            ("9 AAA aaa", r"^\d+[ ][A-Z]+ [A-Z][a-z]+"),
            ("A A ", r"^[A-Z] [A-Z] "),
            ("A AAA Aaa", r"^[A-Z][ ]+[A-Z]+ [A-Z]*[a-z]+"),
            ("a) * a)", r"^[a-z]{1}\) [a-z A-Z0-9\.!\?]* [a-z]{1}\)"),
        ]

    # -----------------------------------------------------------------------------
    # Get the default bulleted list line type anti-patterns.
    # -----------------------------------------------------------------------------
    # 1: rule_name
    # 2: regexp_str:
    #           regular expression
    # -----------------------------------------------------------------------------
    @staticmethod
    def _get_lt_anti_patterns_default_list_bullet(environment_variant: str) -> list[tuple[str, str]]:
        """Get the default bulleted list line type anti-patterns.

        Returns:
            list[tuple[str, str]]:
                The bulleted list line type anti-patterns.
        """
        if environment_variant == NLPCore.ENVIRONMENT_TYPE_TEST:
            return [
                ("n/a", r"^_n/a_$"),
            ]

        return []

    # -----------------------------------------------------------------------------
    # Get the default numbered list line type anti-patterns.
    # -----------------------------------------------------------------------------
    # 1: rule_name
    # 2: regexp_str:
    #           regular expression
    # -----------------------------------------------------------------------------
    @staticmethod
    def _get_lt_anti_patterns_default_list_number(environment_variant: str) -> list[tuple[str, str]]:
        """Get the default numbered list line type anti-patterns.

        Args:
            environment_variant (str):
                    Environment variant: dev, prod or test.

        Returns:
            list[tuple[str, str]]:
                The numbered list line type anti-patterns.
        """
        if environment_variant == NLPCore.ENVIRONMENT_TYPE_TEST:
            return [
                ("n/a", r"^_n/a_$"),
            ]

        return []

    # -----------------------------------------------------------------------------
    # Get the default heading & numbered list line type rules.
    # -----------------------------------------------------------------------------
    # 1: rule_name
    # 2: is_first_token:
    #           True:  apply rule to first token (split)
    #           False: apply rule to beginning of line
    # 3: regexp_str:
    #           regular expression
    # 4: function_is_asc:
    #           compares predecessor and successor
    # 5: start_values:
    #           list of strings
    # -----------------------------------------------------------------------------
    @staticmethod
    def _get_lt_rules_default_heading_list_number() -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
        """Get the default heading & numbered list line type rules.

        Returns:
            list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
                    The heading & numbered list line type rules.
        """
        return [
            (
                "(999)",
                True,
                r"\(\d+\)$",
                NLPCore.is_asc_string_integers,
                ["(1)"],
            ),
            (
                "(A)",
                True,
                r"\([A-Z]\)$",
                NLPCore.is_asc_uppercase_letters,
                ["(A)"],
            ),
            (
                "(ROM)",
                True,
                r"\(M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$",
                NLPCore.is_asc_romans,
                ["(I)"],
            ),
            (
                "(a)",
                True,
                r"\([a-z]\)$",
                NLPCore.is_asc_lowercase_letters,
                ["(a)"],
            ),
            (
                "(rom)",
                True,
                r"\(m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$",
                NLPCore.is_asc_romans,
                ["(i)"],
            ),
            (
                "[999]",
                True,
                r"\[\d+\]$",
                NLPCore.is_asc_string_integers,
                ["[1]"],
            ),
            (
                "[A]",
                True,
                r"\[[A-Z]\]$",
                NLPCore.is_asc_uppercase_letters,
                ["[A]"],
            ),
            (
                "[ROM]",
                True,
                r"\[M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\]$",
                NLPCore.is_asc_romans,
                ["[I]"],
            ),
            (
                "[a]",
                True,
                r"\[[a-z]\]$",
                NLPCore.is_asc_lowercase_letters,
                ["[a]"],
            ),
            (
                "[rom]",
                True,
                r"\[m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\]$",
                NLPCore.is_asc_romans,
                ["[i]"],
            ),
            (
                "999)",
                True,
                r"\d+\)$",
                NLPCore.is_asc_string_integers,
                ["1)"],
            ),
            (
                "999.",
                False,
                r"\d+\.",
                NLPCore.is_asc_string_integers,
                ["1."],
            ),
            (
                "999.999",
                True,
                r"\d+\.\d{1,3}$",
                NLPCore.is_asc_string_floats,
                ["0.0", "0.1", "0.01", "0.001"],
            ),
            (
                "A)",
                True,
                r"[A-Z]\)$",
                NLPCore.is_asc_uppercase_letters,
                ["A)"],
            ),
            (
                "A.",
                False,
                r"[A-Z]\.",
                NLPCore.is_asc_uppercase_letters,
                ["A."],
            ),
            (
                "ROM)",
                True,
                r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$",
                NLPCore.is_asc_romans,
                ["I)"],
            ),
            (
                "ROM.",
                False,
                r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.",
                NLPCore.is_asc_romans,
                ["I."],
            ),
            (
                "a)",
                True,
                r"[a-z]\)$",
                NLPCore.is_asc_lowercase_letters,
                ["a)"],
            ),
            (
                "a.",
                False,
                r"[a-z]\.",
                NLPCore.is_asc_lowercase_letters,
                ["a."],
            ),
            (
                "rom)",
                True,
                r"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$",
                NLPCore.is_asc_romans,
                ["i)"],
            ),
            (
                "rom.",
                False,
                r"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\.",
                NLPCore.is_asc_romans,
                ["i."],
            ),
            (
                "999",
                False,
                r"\d+[ ]+[A-Z][a-zA-Z]+",
                NLPCore.is_asc_string_integers_token,
                ["1 "],
            ),
            (
                "A",
                False,
                r"[A-Z][ ]+[A-Z][a-zA-Z]+",
                NLPCore.is_asc_uppercase_letters_token,
                ["A "],
            ),
            (
                "ROM",
                False,
                r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})[ ]+[A-Z][a-zA-Z]+",
                NLPCore.is_asc_romans_token,
                ["I "],
            ),
            (
                "a",
                False,
                r"[a-z][ ]+[A-Z][a-zA-Z]+",
                NLPCore.is_asc_lowercase_letters_token,
                ["a "],
            ),
            (
                "rom",
                False,
                r"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})[ ]+[A-Z][a-zA-Z]+",
                NLPCore.is_asc_romans_token,
                ["i "],
            ),
        ]

    # -----------------------------------------------------------------------------
    # Get the default bulleted list line type rules.
    # -----------------------------------------------------------------------------
    # 1: bullet character(s)
    # -----------------------------------------------------------------------------
    @staticmethod
    def _get_lt_rules_default_list_bullet() -> dict[str, int]:
        """Get the default bulleted list line type rules.

        Returns:
            dict[str, int]:
                The bulleted list line type rules.
        """
        return {
            "\u002D": 0,
            "\u002E": 0,
            "\u006F": 0,
            "\u00B0": 0,
            "\u00B7": 0,
            "\u00BA": 0,
            "\u2022": 0,
            "\u2023": 0,
            "\u2043": 0,
            "\u204C": 0,
            "\u204D": 0,
            "\u2218": 0,
            "\u2219": 0,
            "\u22C4": 0,
            "\u22C5": 0,
            "\u22C6": 0,
            "\u25CB": 0,
            "\u25CF": 0,
            "\u25D8": 0,
            "\u25E6": 0,
            "\u2605": 0,
            "\u2606": 0,
            "\u2609": 0,
            "\u2619": 0,
            "\u2662": 0,
            "\u2666": 0,
            "\u26AC": 0,
            "\u26B9": 0,
            "\u2765": 0,
            "\u2767": 0,
            "\u29BE": 0,
            "\u29BF": 0,
        }

    # -----------------------------------------------------------------------------
    # Check the object existence.
    # -----------------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns:
            bool:   Always true
        """
        return self._exist

    # -----------------------------------------------------------------------------
    # Export the default heading line type rules.
    # -----------------------------------------------------------------------------
    @staticmethod
    def export_rule_file_heading(is_verbose: bool, file_name: str, file_encoding: str, json_indent: str, is_json_sort_keys: bool) -> None:
        """Export the default heading line type rules.

        Args:
            is_verbose (bool):
                    If true, processing results are reported.
            file_name (str):
                    File name of the output file.
            file_encoding (str):
                    The encoding of the output file.
            json_indent (str):
                    Indent level for pretty-printing the JSON output.
            is_json_sort_keys (bool):
                    If true, the output of the JSON dictionaries will be sorted by key.
        """
        anti_patterns = []

        for name, regexp in NLPCore.get_lt_anti_patterns_default_heading():
            anti_patterns.append(
                {
                    NLPCore.JSON_NAME_NAME: name,
                    NLPCore.JSON_NAME_REGEXP: regexp,
                }
            )

        rules = []

        for name, is_first_token, regexp, function_is_asc, start_values in NLPCore.get_lt_rules_default_heading():
            rules.append(
                {
                    NLPCore.JSON_NAME_NAME: name,
                    NLPCore.JSON_NAME_IS_FIRST_TOKEN: is_first_token,
                    NLPCore.JSON_NAME_REGEXP: regexp,
                    NLPCore.JSON_NAME_FUNCTION_IS_ASC: function_is_asc.__qualname__[15:],
                    NLPCore.JSON_NAME_START_VALUES: start_values,
                }
            )

        with open(file_name, "w", encoding=file_encoding) as file_handle:
            # {
            #     "lineTypeListAntiPatterns": [
            #       (name, regexp),
            #     ]
            #     "lineTypeRules": [
            #       {
            #          "name": "xxx",
            #          "isFirstToken": bool,
            #          "regexp": "xxx",
            #          "functionIsAsc": "xxx",
            #          "startValues": ["xxx"]
            #       },
            #     ]
            # }
            json.dump(
                {
                    NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS: anti_patterns,
                    NLPCore.JSON_NAME_LINE_TYPE_RULES: rules,
                },
                file_handle,
                indent=json_indent,
                sort_keys=is_json_sort_keys,
            )

        if len(anti_patterns) > 0:
            dcr_core.core_utils.progress_msg(is_verbose, f"{len(anti_patterns):3d} heading       line type anti-pattern(s) exported")
        if len(rules) > 0:
            dcr_core.core_utils.progress_msg(is_verbose, f"{len(rules):3d} heading       line type rule(s)         exported")

    # -----------------------------------------------------------------------------
    # Export the default bulleted list line type rules.
    # -----------------------------------------------------------------------------
    @staticmethod
    def export_rule_file_list_bullet(
        is_verbose: bool,
        file_name: str,
        file_encoding: str,
        json_indent: str,
        is_json_sort_keys: bool,
        environment_variant: str,
    ) -> None:
        """Export the default bulleted list line type rules.

        Args:
            is_verbose (bool):
                    If true, processing results are reported.
            file_name (str):
                    File name of the output file.
            file_encoding (str):
                    The encoding of the output file.
            json_indent (str):
                    Indent level for pretty-printing the JSON output.
            is_json_sort_keys (bool):
                    If true, the output of the JSON dictionaries will be sorted by key.
            environment_variant (str):
                    Environment variant: dev, prod or test.
        """
        anti_patterns = []

        for name, regexp in NLPCore.get_lt_anti_patterns_default_list_bullet(environment_variant):
            anti_patterns.append(
                {
                    NLPCore.JSON_NAME_NAME: name,
                    NLPCore.JSON_NAME_REGEXP: regexp,
                }
            )

        rules = []

        for rule in NLPCore.get_lt_rules_default_list_bullet():
            rules.append(rule)

        with open(file_name, "w", encoding=file_encoding) as file_handle:
            #     "lineTypeListAntiPatterns": [
            #       (name, regexp),
            #     ]
            # {
            #     "lineTypeListRules": [
            #       regexp,
            #     ]
            # }
            json.dump(
                {
                    NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS: anti_patterns,
                    NLPCore.JSON_NAME_LINE_TYPE_RULES: rules,
                },
                file_handle,
                indent=json_indent,
                sort_keys=is_json_sort_keys,
            )

        if len(anti_patterns) > 0:
            dcr_core.core_utils.progress_msg(is_verbose, f"{len(anti_patterns):3d} bulleted list line type anti-pattern(s) exported")
        if len(rules) > 0:
            dcr_core.core_utils.progress_msg(is_verbose, f"{len(rules):3d} bulleted list line type rule(s)         exported")

    # -----------------------------------------------------------------------------
    # Export the default numbered list line type rules.
    # -----------------------------------------------------------------------------
    @staticmethod
    def export_rule_file_list_number(
        is_verbose: bool,
        file_name: str,
        file_encoding: str,
        json_indent: str,
        is_json_sort_keys: bool,
        environment_variant: str,
    ) -> None:
        """Export the default numbered list line type rules.

        Args:
            is_verbose (bool):
                    If true, processing results are reported.
            file_name (str, optional):
                    File name of the output file.
            file_encoding (str):
                    The encoding of the output file.
            json_indent (str):
                    Indent level for pretty-printing the JSON output.
            is_json_sort_keys (bool):
                    If true, the output of the JSON dictionaries will be sorted by key.
            environment_variant (str):
                    Environment variant: dev, prod or test.
        """
        anti_patterns = []

        for name, regexp in NLPCore.get_lt_anti_patterns_default_list_number(environment_variant):
            anti_patterns.append(
                {
                    NLPCore.JSON_NAME_NAME: name,
                    NLPCore.JSON_NAME_REGEXP: regexp,
                }
            )

        rules = []

        for name, regexp, function_is_asc, start_values in NLPCore.get_lt_rules_default_list_number():
            rules.append(
                {
                    NLPCore.JSON_NAME_NAME: name,
                    NLPCore.JSON_NAME_REGEXP: regexp,
                    NLPCore.JSON_NAME_FUNCTION_IS_ASC: function_is_asc.__qualname__[15:],
                    NLPCore.JSON_NAME_START_VALUES: start_values,
                }
            )

        with open(file_name, "w", encoding=file_encoding) as file_handle:
            # {
            #     "lineTypeListAntiPatterns": [
            #       (name, regexp),
            #     ]
            #     "lineTypeListRules": [
            #       {
            #          "name": "xxx",
            #          "regexp": "xxx",
            #          "functionIsAsc": "xxx",
            #          "startValues": ["xxx"]
            #       },
            #     ]
            # }
            json.dump(
                {
                    NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS: anti_patterns,
                    NLPCore.JSON_NAME_LINE_TYPE_RULES: rules,
                },
                file_handle,
                indent=json_indent,
                sort_keys=is_json_sort_keys,
            )

        if len(anti_patterns) > 0:
            dcr_core.core_utils.progress_msg(is_verbose, f"{len(anti_patterns):3d} numbered list line type anti-pattern(s) exported")
        if len(rules) > 0:
            dcr_core.core_utils.progress_msg(is_verbose, f"{len(rules):3d} numbered list line type rule(s)         exported")

    # -----------------------------------------------------------------------------
    # Get the default heading line type anti-patterns.
    # -----------------------------------------------------------------------------
    @staticmethod
    def get_lt_anti_patterns_default_heading() -> list[
        tuple[
            str,
            str,
        ]
    ]:
        """Get the default heading line type anti-patterns.

        Returns:
            list[tuple[str, str,]]:
                The heading line type anti-patterns.
        """
        return NLPCore._get_lt_anti_patterns_default_heading()

    # -----------------------------------------------------------------------------
    # Get the default bulleted list line type anti-patterns.
    # -----------------------------------------------------------------------------
    @staticmethod
    def get_lt_anti_patterns_default_list_bullet(
        environment_variant: str,
    ) -> list[tuple[str, str]]:
        """Get the default bulleted list line type anti-patterns.

        Args:
            environment_variant (str):
                    Environment variant: dev, prod or test.

        Returns:
            list[tuple[str, str]]:
                The bulleted list line type anti-patterns.
        """
        return NLPCore._get_lt_anti_patterns_default_list_bullet(environment_variant)

    # -----------------------------------------------------------------------------
    # Get the default numbered list line type anti-patterns.
    # -----------------------------------------------------------------------------
    @staticmethod
    def get_lt_anti_patterns_default_list_number(environment_variant: str) -> list[tuple[str, str]]:
        """Get the default numbered list line type anti-patterns.

        Args:
            environment_variant (str):
                    Environment variant: dev, prod or test.

        Returns:
            list[tuple[str, str]]:
                The numbered list line type anti-patterns.
        """
        return NLPCore._get_lt_anti_patterns_default_list_number(environment_variant)

    # -----------------------------------------------------------------------------
    # Get the default heading line type rules.
    # -----------------------------------------------------------------------------
    @staticmethod
    def get_lt_rules_default_heading() -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
        """Get the default heading line type rules.

        Returns:
            list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
                The heading line type rules.
        """
        return NLPCore._get_lt_rules_default_heading_list_number()

    # -----------------------------------------------------------------------------
    # Get the default bulleted list line type rules.
    # -----------------------------------------------------------------------------
    @staticmethod
    def get_lt_rules_default_list_bullet() -> dict[str, int]:
        """Get the default bulleted list line type rules.

        Returns:
            dict[str, int]:
                The bulleted list line type rules.
        """
        return NLPCore._get_lt_rules_default_list_bullet()

    # -----------------------------------------------------------------------------
    # Get the default numbered list line type rules.
    # -----------------------------------------------------------------------------
    @staticmethod
    def get_lt_rules_default_list_number() -> list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]:
        """Get the default numbered list line type rules.

        Returns:
            list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
                The numbered list line type rules.
        """
        rules: list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]] = []

        for (
            rule_name,
            _,
            regexp_str,
            function_is_asc,
            start_values,
        ) in NLPCore._get_lt_rules_default_heading_list_number():
            rules.append((rule_name, regexp_str, function_is_asc, start_values))

        return rules

    # -----------------------------------------------------------------------------
    # Ignore the comparison.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_ignore(cls, _predecessor: str, _successor: str) -> bool:
        """Ignore the comparison.

        Returns:
            bool: True.
        """
        return True

    # -----------------------------------------------------------------------------
    # Compare two lowercase letters on difference ascending 1.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_lowercase_letters(cls, predecessor: str, successor: str) -> bool:
        """Compare two lowercase_letters on ascending.

        Args:
            predecessor (str):
                    The previous string.
            successor (str):
                    The current string.

        Returns:
            bool:   True, if the successor - predecessor is equal to 1, False else.
        """
        if (predecessor_ints := re.findall(r"[a-z]", predecessor.lower())) and (successor_ints := re.findall(r"[a-z]", successor.lower())):
            if ord(successor_ints[0]) - ord(predecessor_ints[0]) == 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two lowercase letters on difference ascending 1 - only first token.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_lowercase_letters_token(cls, predecessor: str, successor: str) -> bool:
        """Compare two lowercase_letters on ascending - only first token.

        Args:
            predecessor (str):
                    The previous string.
            successor (str):
                    The current string.

        Returns:
            bool:   True, if the successor - predecessor is equal to 1, False else.
        """
        return cls.is_asc_lowercase_letters(predecessor.split()[0], successor.split()[0])

    # -----------------------------------------------------------------------------
    # Compare two roman numerals on ascending.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_romans(cls, predecessor: str, successor: str) -> bool:
        """Compare two roman numerals on ascending.

        Args:
            predecessor (str):
                    The previous roman numeral.
            successor (str):
                    The current roman numeral.

        Returns:
            bool:
            False, if the predecessor is greater than the current value, True else.
        """
        # TBD depending on different regexp patterns
        # if predecessor[0] == "(":
        #     predecessor_net = predecessor[1:-1]
        #     successor_net = successor[1:-1]
        # else:
        #     predecessor_net = predecessor
        #     successor_net = successor

        if predecessor[0:1] == "(":
            predecessor_net = predecessor[1:]
        else:
            predecessor_net = predecessor
        if predecessor_net[-1] in {")", "."}:
            predecessor_net = predecessor_net[:-1]

        if successor[0:1] == "(":
            successor_net = successor[1:]
        else:
            successor_net = successor
        if successor_net[-1] in {")", "."}:
            successor_net = successor_net[:-1]

        if NLPCore._convert_roman_2_int(successor_net.lower()) - NLPCore._convert_roman_2_int(predecessor_net.lower()) == 1:
            return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two roman numerals on ascending - only first token.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_romans_token(cls, predecessor: str, successor: str) -> bool:
        """Compare two roman numerals on ascending - only first token.

        Args:
            predecessor (str):
                    The previous roman numeral.
            successor (str):
                    The current roman numeral.

        Returns:
            bool:   False, if the predecessor is greater than the current value, True else.
        """
        # TBD depending on different regexp patterns
        # if predecessor[0] == "(":
        #     predecessor_net = predecessor[1:-1]
        #     successor_net = successor[1:-1]
        # else:
        #     predecessor_net = predecessor
        #     successor_net = successor
        return cls.is_asc_romans(predecessor.split()[0], successor.split()[0])

    # -----------------------------------------------------------------------------
    # Compare two strings on ascending.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_strings(cls, predecessor: str, successor: str) -> bool:
        """Compare two strings on ascending.

        Args:
            predecessor (str):
                    The previous string.
            successor (str):
                    The current string.

        Returns:
            bool:   False, if the predecessor is greater than the current value, True else.
        """
        if predecessor > successor:
            return False

        return True

    # -----------------------------------------------------------------------------
    # Compare two string floats on ascending.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_string_floats(cls, predecessor: str, successor: str) -> bool:
        """Compare two string float numbers on ascending.

        Args:
            predecessor (str):
                    The previous string float number.
            successor (str):
                    The current string float number.

        Returns:
            bool:   False, if the predecessor is greater than the current value, True else.
        """
        if (predecessor_floats := re.findall(r"\d+\.\d+", predecessor)) and (successor_floats := re.findall(r"\d+\.\d+", successor)):
            if 0 < float(successor_floats[0]) - float(predecessor_floats[0]) <= 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two string floats on ascending - only first token.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_string_floats_token(cls, predecessor: str, successor: str) -> bool:
        """Compare two string float numbers on ascending - only first token.

        Args:
            predecessor (str):
                    The previous string float number.
            successor (str):
                    The current string float number.

        Returns:
            bool:   False, if the predecessor is greater than the current value, True else.
        """
        return cls.is_asc_string_floats(predecessor.split()[0], successor.split()[0])

    # -----------------------------------------------------------------------------
    # Compare two string integers on difference ascending 1.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_string_integers(cls, predecessor: str, successor: str) -> bool:
        """Compare two string integers on ascending.

        Args:
            predecessor (str):
                    The previous string integer.
            successor (str):
                    The current string integer.

        Returns:
            bool:   True, if the successor - predecessor is equal to 1, False else.
        """
        if (predecessor_ints := re.findall(r"\d+", predecessor)) and (successor_ints := re.findall(r"\d+", successor)):
            if int(successor_ints[0]) - int(predecessor_ints[0]) == 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two string integers on difference ascending 1 - only first token.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_string_integers_token(cls, predecessor: str, successor: str) -> bool:
        """Compare two string integers on ascending - only first token.

        Args:
            predecessor (str):
                    The previous string integer.
            successor (str):
                    The current string integer.

        Returns:
            bool:   True, if the successor - predecessor is equal to 1, False else.
        """
        return cls.is_asc_string_integers(predecessor.split()[0], successor.split()[0])

    # -----------------------------------------------------------------------------
    # Compare two uppercase letters on difference ascending 1.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_uppercase_letters(cls, predecessor: str, successor: str) -> bool:
        """Compare two uppercase_letters on ascending.

        Args:
            predecessor (str):
                    The previous string.
            successor (str):
                    The current string.

        Returns:
            bool:   True, if the successor - predecessor is equal to 1, False else.
        """
        if (predecessor_ints := re.findall(r"[A-Z]", predecessor.upper())) and (successor_ints := re.findall(r"[A-Z]", successor.upper())):
            if ord(successor_ints[0]) - ord(predecessor_ints[0]) == 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two uppercase letters on difference ascending 1 - only first token.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_uppercase_letters_token(cls, predecessor: str, successor: str) -> bool:
        """Compare two uppercase_letters on ascending - only first token.

        Args:
            predecessor (str):
                    The previous string.
            successor (str):
                    The current string.

        Returns:
            bool:   True, if the successor - predecessor is equal to 1, False else.
        """
        return cls.is_asc_uppercase_letters(predecessor.split()[0], successor.split()[0])
