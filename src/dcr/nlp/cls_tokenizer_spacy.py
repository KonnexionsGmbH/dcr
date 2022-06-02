"""Module nlp.cls_line_type: Determine footer and header lines."""
from __future__ import annotations

from typing import ClassVar

import cfg.glob
import spacy
import spacy.tokens


# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# -----------------------------------------------------------------------------
# Global type aliases.
# -----------------------------------------------------------------------------
# {
#     "tknEntIob_": "O",
#     "tknI": 0,
#     "tknIsOov": true,
#     "tknIsSentStart": true,
#     "tknIsStop": true,
#     "tknIsTitle": true,
#     "tknLemma_": "this",
#     "tknNorm_": "this",
#     "tknPos_": "PRON",
#     "tknTag_": "DT",
#     "tknText": "This",
#     "tknWhitespace_": " "
# }
Token = dict[str, bool | float | int | str]
Tokens = list[Token]

# {
# 	"paraNo": 99,
# 	"noLinesInPara": 99,
# 	"noTokensInPara": 99,
# 	"tokens": [
TokensPara = dict[str, int | Tokens]
TokensParas = list[TokensPara]

# {
# 	"pageNo": 99,
# 	"noTLinesInPage": 99,
# 	"noParasInPage": 99,
# 	"noTokensInPage": 99,
# 	"paras": [
TokensPage = dict[str, int | TokensPara]
TokensPages = list[TokensPage]

# {
#     "documentId": 99,
#     "documentFileName": "case_2_docx_route_inbox_pandoc_pdflib.docx",
#     "noLinesInDoc": 99,
#     "noPagesInDoc": 99,
#     "noParasInDoc": 99,
#     "noTokensInDoc": 99,
#     "pages": [
TokensDocument = dict[str, int | TokensPages | str]


class TokenizerSpacy:
    """Determine footer and header lines.

    Returns:
        _type_: TokenizeSpacy instance.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    JSON_NAME_NO_TOKENS_IN_PAGE: ClassVar[str] = "noTokensInPage"

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

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._token_0_token: Token = {}
        self._token_1_tokens: Tokens = []

        self._token_2_para: TokensPara = {}
        self._token_3_paras: TokensParas = []

        self._token_4_page: TokensPage = {}
        self._token_5_pages: TokensPages = []

        self._token_6_document: TokensDocument = {}

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

    # -----------------------------------------------------------------------------
    # Determine the requested token attributes.
    # -----------------------------------------------------------------------------
    @classmethod
    def get_token_attributes(  # type: ignore # noqa: C901
        cls, token: spacy.tokens.Token
    ) -> Token:
        """Determine the requested token attributes.

        Args:
            token (spacy.tokens.Token):
                SpaCy tokens.

        Returns:
            Token:
                Requested token attributes.
        """
        token_attr = {}

        if cfg.glob.setup.is_spacy_tkn_attr_cluster:
            if token.cluster != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_CLUSTER] = token.cluster

        if cfg.glob.setup.is_spacy_tkn_attr_dep_:
            if token.dep_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_DEP_] = token.dep_

        if cfg.glob.setup.is_spacy_tkn_attr_doc:
            if token.doc is not None:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_DOC] = token.doc.text

        if cfg.glob.setup.is_spacy_tkn_attr_ent_iob_:
            if token.ent_iob_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_ENT_IOB_] = token.ent_iob_

        if cfg.glob.setup.is_spacy_tkn_attr_ent_kb_id_:
            # not testable
            if token.ent_kb_id_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_ENT_KB_ID_] = token.ent_kb_id_

        if cfg.glob.setup.is_spacy_tkn_attr_ent_type_:
            if token.ent_type_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_ENT_TYPE_] = token.ent_type_

        if cfg.glob.setup.is_spacy_tkn_attr_head:
            if token.head is not None:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_HEAD] = token.head.i

        if cfg.glob.setup.is_spacy_tkn_attr_i:
            token_attr[TokenizerSpacy.JSON_NAME_TOKEN_I] = token.i

        if cfg.glob.setup.is_spacy_tkn_attr_idx:
            if token.idx != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IDX] = token.idx

        if cfg.glob.setup.is_spacy_tkn_attr_is_alpha:
            if token.is_alpha:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_ALPHA] = token.is_alpha

        if cfg.glob.setup.is_spacy_tkn_attr_is_ascii:
            if token.is_ascii:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_ASCII] = token.is_ascii

        if cfg.glob.setup.is_spacy_tkn_attr_is_bracket:
            if token.is_bracket:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_BRACKET] = token.is_bracket

        if cfg.glob.setup.is_spacy_tkn_attr_is_currency:
            if token.is_currency:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_CURRENCY] = token.is_currency

        if cfg.glob.setup.is_spacy_tkn_attr_is_digit:
            if token.is_digit:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_DIGIT] = token.is_digit

        if cfg.glob.setup.is_spacy_tkn_attr_is_left_punct:
            if token.is_left_punct:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_LEFT_PUNCT] = token.is_left_punct

        if cfg.glob.setup.is_spacy_tkn_attr_is_lower:
            if token.is_lower:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_LOWER] = token.is_lower

        if cfg.glob.setup.is_spacy_tkn_attr_is_oov:
            if token.is_oov:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_OOV] = token.is_oov

        if cfg.glob.setup.is_spacy_tkn_attr_is_punct:
            if token.is_punct:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_PUNCT] = token.is_punct

        if cfg.glob.setup.is_spacy_tkn_attr_is_quote:
            if token.is_quote:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_QUOTE] = token.is_quote

        if cfg.glob.setup.is_spacy_tkn_attr_is_right_punct:
            if token.is_right_punct:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_RIGHT_PUNCT] = token.is_right_punct

        if cfg.glob.setup.is_spacy_tkn_attr_is_sent_end:
            if token.is_sent_end:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_SENT_END] = token.is_sent_end

        if cfg.glob.setup.is_spacy_tkn_attr_is_sent_start:
            if token.is_sent_start:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_SENT_START] = token.is_sent_start

        if cfg.glob.setup.is_spacy_tkn_attr_is_space:
            if token.is_space:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_SPACE] = token.is_space

        if cfg.glob.setup.is_spacy_tkn_attr_is_stop:
            if token.is_stop:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_STOP] = token.is_stop

        if cfg.glob.setup.is_spacy_tkn_attr_is_title:
            if token.is_title:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_TITLE] = token.is_title

        if cfg.glob.setup.is_spacy_tkn_attr_is_upper:
            if token.is_upper:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_IS_UPPER] = token.is_upper

        if cfg.glob.setup.is_spacy_tkn_attr_lang_:
            if token.lang_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_LANG_] = token.lang_

        if cfg.glob.setup.is_spacy_tkn_attr_left_edge:
            if token.left_edge.text is not None:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_LEFT_EDGE] = token.left_edge.i

        if cfg.glob.setup.is_spacy_tkn_attr_lemma_:
            if token.lemma_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_LEMMA_] = token.lemma_

        if cfg.glob.setup.is_spacy_tkn_attr_lex:
            if token.lex is not None:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_LEX] = token.lex.text

        if cfg.glob.setup.is_spacy_tkn_attr_lex_id:
            if token.lex_id != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_LEX_ID] = token.lex_id

        if cfg.glob.setup.is_spacy_tkn_attr_like_email:
            if token.like_email:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_LIKE_EMAIL] = token.like_email

        if cfg.glob.setup.is_spacy_tkn_attr_like_num:
            if token.like_num:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_LIKE_NUM] = token.like_num

        if cfg.glob.setup.is_spacy_tkn_attr_like_url:
            if token.like_url:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_LIKE_URL] = token.like_url

        if cfg.glob.setup.is_spacy_tkn_attr_lower_:
            if token.lower_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_LOWER_] = token.lower_

        if cfg.glob.setup.is_spacy_tkn_attr_morph:
            if token.morph is not None:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_MORPH] = str(token.morph)

        if cfg.glob.setup.is_spacy_tkn_attr_norm_:
            if token.norm_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_NORM_] = token.norm_

        if cfg.glob.setup.is_spacy_tkn_attr_orth_:
            if token.orth_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_ORTH_] = token.orth_

        if cfg.glob.setup.is_spacy_tkn_attr_pos_:
            if token.pos_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_POS_] = token.pos_

        if cfg.glob.setup.is_spacy_tkn_attr_prefix_:
            if token.prefix_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_PREFIX_] = token.prefix_

        if cfg.glob.setup.is_spacy_tkn_attr_prob:
            if token.prob != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_PROB] = token.prob

        if cfg.glob.setup.is_spacy_tkn_attr_rank:
            if token.rank != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_RANK] = token.rank

        if cfg.glob.setup.is_spacy_tkn_attr_right_edge:
            if token.right_edge is not None:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_RIGHT_EDGE] = token.right_edge.i

        if cfg.glob.setup.is_spacy_tkn_attr_sent:
            if token.sent is not None:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_SENT] = token.sent.text

        if cfg.glob.setup.is_spacy_tkn_attr_sentiment:
            if token.sentiment != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_SENTIMENT] = token.sentiment

        if cfg.glob.setup.is_spacy_tkn_attr_shape_:
            if token.shape_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_SHAPE_] = token.shape_

        if cfg.glob.setup.is_spacy_tkn_attr_suffix_:
            if token.suffix_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_SUFFIX_] = token.suffix_

        if cfg.glob.setup.is_spacy_tkn_attr_tag_:
            if token.tag_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_TAG_] = token.tag_

        if cfg.glob.setup.is_spacy_tkn_attr_tensor:
            try:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_TENSOR] = str(token.tensor)
            except IndexError:
                pass

        if cfg.glob.setup.is_spacy_tkn_attr_text:
            if token.text != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_TEXT] = token.text

        if cfg.glob.setup.is_spacy_tkn_attr_text_with_ws:
            if token.text_with_ws != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_TEXT_WITH_WS] = token.text_with_ws

        if cfg.glob.setup.is_spacy_tkn_attr_vocab:
            if token.vocab is not None:
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_RANK] = str(token.vocab)

        if cfg.glob.setup.is_spacy_tkn_attr_whitespace_:
            if token.whitespace_ != "":
                token_attr[TokenizerSpacy.JSON_NAME_TOKEN_WHITESPACE_] = token.whitespace_

        return token_attr
