"""Module nlp.cls_nlp_core: Managing the NLP processing."""
from __future__ import annotations

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

    JSON_NAME_DOC_FILE_NAME: ClassVar[str] = "documentFileName"
    JSON_NAME_DOC_ID: ClassVar[str] = "documentId"
    JSON_NAME_LINES: ClassVar[str] = "lines"
    JSON_NAME_LINE_INDEX_PAGE: ClassVar[str] = "lineIndexPage"
    JSON_NAME_LINE_INDEX_PARA: ClassVar[str] = "lineIndexParagraph"
    JSON_NAME_LINE_NO: ClassVar[str] = "lineNo"
    JSON_NAME_LINE_TYPE: ClassVar[str] = "lineType"
    JSON_NAME_NO_LINES_IN_DOC: ClassVar[str] = "noLinesInDocument"
    JSON_NAME_NO_LINES_IN_PAGE: ClassVar[str] = "noLinesInPage"
    JSON_NAME_NO_LINES_IN_PARA: ClassVar[str] = "noLinesInParagraph"
    JSON_NAME_NO_PAGES_IN_DOC: ClassVar[str] = "noPagesInDocument"
    JSON_NAME_NO_PARAS_IN_DOC: ClassVar[str] = "noParagraphsInDocument"
    JSON_NAME_NO_PARAS_IN_PAGE: ClassVar[str] = "noParagraphsInPage"
    JSON_NAME_NO_SENTS_IN_DOC: ClassVar[str] = "noSentencesInDocument"
    JSON_NAME_NO_SENTS_IN_PAGE: ClassVar[str] = "noSentencesInPage"
    JSON_NAME_NO_SENTS_IN_PARA: ClassVar[str] = "noSentencesInParagraph"
    JSON_NAME_NO_TOKENS_IN_DOC: ClassVar[str] = "noTokensInDocument"
    JSON_NAME_NO_TOKENS_IN_PAGE: ClassVar[str] = "noTokensInPage"
    JSON_NAME_NO_TOKENS_IN_PARA: ClassVar[str] = "noTokensInParagraph"
    JSON_NAME_NO_TOKENS_IN_SENT: ClassVar[str] = "noTokensInSentence"
    JSON_NAME_NO_WORDS_IN_DOC: ClassVar[str] = "noWordsInDocument"
    JSON_NAME_NO_WORDS_IN_LINE: ClassVar[str] = "noWordsInLine"
    JSON_NAME_NO_WORDS_IN_PAGE: ClassVar[str] = "noWordsInPage"
    JSON_NAME_NO_WORDS_IN_PARA: ClassVar[str] = "noWordsInParagraph"
    JSON_NAME_PAGES: ClassVar[str] = "pages"
    JSON_NAME_PAGE_NO: ClassVar[str] = "pageNo"
    JSON_NAME_PARAS: ClassVar[str] = "paragraphs"
    JSON_NAME_PARA_NO: ClassVar[str] = "paragraphNo"
    JSON_NAME_SENTS: ClassVar[str] = "sentences"
    JSON_NAME_SENT_NO: ClassVar[str] = "sentenceNo"
    JSON_NAME_TEXT: ClassVar[str] = "text"
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

    JSON_NAME_WORDS: ClassVar[str] = "words"
    JSON_NAME_WORD_NO: ClassVar[str] = "wordNo"

    PARSE_NAME_SPACE: ClassVar[str] = "{http://www.pdflib.com/XML/TET5/TET-5.0}"
    PARSE_TAG_ACTION: ClassVar[str] = "Action"
    PARSE_TAG_ANNOTATIONS: ClassVar[str] = "Annotations"
    PARSE_TAG_ATTACHMENTS: ClassVar[str] = "Attachments"
    PARSE_TAG_AUTHOR: ClassVar[str] = "Author"
    PARSE_TAG_BOOKMARKS: ClassVar[str] = "Bookmarks"
    PARSE_TAG_BOX: ClassVar[str] = "Box"
    PARSE_TAG_CELL: ClassVar[str] = "Cell"
    PARSE_TAG_CONTENT: ClassVar[str] = "Content"
    PARSE_TAG_CREATION: ClassVar[str] = "Creation"
    PARSE_TAG_CREATION_DATE: ClassVar[str] = "CreationDate"
    PARSE_TAG_CREATOR: ClassVar[str] = "Creator"
    PARSE_TAG_CUSTOM: ClassVar[str] = "Custom"
    PARSE_TAG_DESTINATIONS: ClassVar[str] = "Destinations"
    PARSE_TAG_DOCUMENT: ClassVar[str] = "Document"
    PARSE_TAG_DOCUMENT_INFO: ClassVar[str] = "DocInfo"
    PARSE_TAG_ENCRYPTION: ClassVar[str] = "Encryption"
    PARSE_TAG_EXCEPTION: ClassVar[str] = "Exception"
    PARSE_TAG_FIELDS: ClassVar[str] = "Fields"
    PARSE_TAG_FROM: ClassVar[int] = len(PARSE_NAME_SPACE)
    PARSE_TAG_GRAPHICS: ClassVar[str] = "Graphics"
    PARSE_TAG_JAVA_SCRIPTS: ClassVar[str] = "JavaScripts"
    PARSE_TAG_LINE: ClassVar[str] = "Line"
    PARSE_TAG_METADATA: ClassVar[str] = "Metadata"
    PARSE_TAG_MOD_DATE: ClassVar[str] = "ModDate"
    PARSE_TAG_OPTIONS: ClassVar[str] = "Options"
    PARSE_TAG_OUTPUT_INTENTS: ClassVar[str] = "OutputIntents"
    PARSE_TAG_PAGE: ClassVar[str] = "Page"
    PARSE_TAG_PAGES: ClassVar[str] = "Pages"
    PARSE_TAG_PARA: ClassVar[str] = "Para"
    PARSE_TAG_PLACED_IMAGE: ClassVar[str] = "PlacedImage"
    PARSE_TAG_PRODUCER: ClassVar[str] = "Producer"
    PARSE_TAG_RESOURCES: ClassVar[str] = "Resources"
    PARSE_TAG_ROW: ClassVar[str] = "Row"
    PARSE_TAG_SIGNATURE_FIELDS: ClassVar[str] = "SignatureFields"
    PARSE_TAG_TABLE: ClassVar[str] = "Table"
    PARSE_TAG_TEXT: ClassVar[str] = "Text"
    PARSE_TAG_TITLE: ClassVar[str] = "Title"
    PARSE_TAG_WORD: ClassVar[str] = "Word"
    PARSE_TAG_XFA: ClassVar[str] = "XFA"

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._exist = True

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Check the object existence.
    # -----------------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns:
            bool:   Always true
        """
        return self._exist
