"""Module nlp.cls_nlp_core: Managing the NLP processing."""
from __future__ import annotations

import re
from typing import ClassVar

import cfg.glob

# -----------------------------------------------------------------------------
# Global type aliases.
# -----------------------------------------------------------------------------


class NLPCore:
    """Managing the NLP processing.

    Returns:
        _type_: LineType instance.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
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
    JSON_NAME_LINE_TYPE_HEADING_RULES: ClassVar[str] = "lineTypeHeadingRules"
    JSON_NAME_LINE_TYPE_LIST_BULLET_RULES: ClassVar[str] = "lineTypeListBulletRules"
    JSON_NAME_LINE_TYPE_LIST_NUMBER_RULES: ClassVar[str] = "lineTypeListNumberRules"
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

    PARSE_NAME_SPACE: ClassVar[str] = "{http://www.pdflib.com/XML/TET5/TET-5.0}"

    PARSE_ATTR_COL_SPAN: ClassVar[str] = "colSpan"
    PARSE_ATTR_LLX: ClassVar[str] = "llx"
    PARSE_ATTR_URX: ClassVar[str] = "urx"

    PARSE_ELEM_ACTION: ClassVar[str] = "Action"
    PARSE_ELEM_ANNOTATIONS: ClassVar[str] = "Annotations"
    PARSE_ELEM_ATTACHMENTS: ClassVar[str] = "Attachments"
    PARSE_ELEM_AUTHOR: ClassVar[str] = "Author"
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
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._exist = True

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Convert a roman numeral to integer.
    # -----------------------------------------------------------------------------
    @classmethod
    def _convert_roman_2_int(cls, roman: str) -> int:
        """Convert a roman numeral to integer.

        Args:
            roman (str): The roman numeral.

        Returns:
            int: The corresponding integer.
        """
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
    # Check the object existence.
    # -----------------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns:
            bool:   Always true
        """
        return self._exist

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
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: True, if the successor - predecessor is equal to 1, False else.
        """
        if (predecessor_ints := re.findall(r"[a-z]", predecessor.lower())) and (
            successor_ints := re.findall(r"[a-z]", successor.lower())
        ):
            if ord(successor_ints[0]) - ord(predecessor_ints[0]) == 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two roman numerals on ascending.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_romans(cls, predecessor: str, successor: str) -> bool:
        """Compare two roman numerals on ascending.

        Args:
            predecessor (str): The previous roman numeral.
            successor (str): The current roman numeral.

        Returns:
            bool: False, if the predecessor is greater than the current value, True else.
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
    # Compare two strings on ascending.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_strings(cls, predecessor: str, successor: str) -> bool:
        """Compare two strings on ascending.

        Args:
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: False, if the predecessor is greater than the current value, True else.
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
            predecessor (str): The previous string float number.
            successor (str): The current string float number.

        Returns:
            bool: False, if the predecessor is greater than the current value, True else.
        """
        if (predecessor_floats := re.findall(r"\d+\.\d+", predecessor)) and (
            successor_floats := re.findall(r"\d+\.\d+", successor)
        ):
            if 0 < float(successor_floats[0]) - float(predecessor_floats[0]) <= 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two string integers on difference ascending 1.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_string_integers(cls, predecessor: str, successor: str) -> bool:
        """Compare two string integers on ascending.

        Args:
            predecessor (str): The previous string integer.
            successor (str): The current string integer.

        Returns:
            bool: True, if the successor - predecessor is equal to 1, False else.
        """
        if (predecessor_ints := re.findall(r"\d+", predecessor)) and (successor_ints := re.findall(r"\d+", successor)):
            if int(successor_ints[0]) - int(predecessor_ints[0]) == 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two uppercase letters on difference ascending 1.
    # -----------------------------------------------------------------------------
    @classmethod
    def is_asc_uppercase_letters(cls, predecessor: str, successor: str) -> bool:
        """Compare two uppercase_letters on ascending.

        Args:
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: True, if the successor - predecessor is equal to 1, False else.
        """
        if (predecessor_ints := re.findall(r"[A-Z]", predecessor.upper())) and (
            successor_ints := re.findall(r"[A-Z]", successor.upper())
        ):
            if ord(successor_ints[0]) - ord(predecessor_ints[0]) == 1:
                return True

        return False
