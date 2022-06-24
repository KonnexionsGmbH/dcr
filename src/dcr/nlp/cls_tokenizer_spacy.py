"""Module nlp.cls_line_type: Determine footer and header lines."""
from __future__ import annotations

import json

import cfg.glob
import db.cls_db_core
import db.cls_document
import db.cls_token
import nlp.cls_nlp_core
import spacy
import spacy.tokens
import utils

# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
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

TokenToken = dict[str, bool | float | int | str]
TokenTokens = list[TokenToken]

# {
# 	"sentenceNo": 99,
# 	"columnNo": 99,
# 	"columnSpan": 99,
# 	"lowerLeftX": 99.99,
# 	"noTokensInSentence": 99,
# 	"rowNo": 99,
#   "text" = "...",
# 	"tokens": [...]
# }
TokenSent = dict[str, float | int | None | str | TokenTokens]
TokenSents = list[TokenSent]

# {
# 	"paragraphNo": 99,
# 	"noSentencesInParagraph": 99,
# 	"noLinesInParagraph": 99,
# 	"noTokensInParagraph": 99,
# 	"sentences": [...]
# }
TokenPara = dict[str, int | TokenSents]
TokenParas = list[TokenPara]

# {
# 	"pageNo": 99,
# 	"noParagraphsInPage": 99,
# 	"noSentencesInPage": 99,
# 	"noTLinesInPage": 99,
# 	"noTokensInPage": 99,
# 	"paragraphs": [...]
# }
TokenPage = dict[str, int | TokenParas]
TokenPages = list[TokenPage]

# {
#     "documentId": 99,
#     "documentFileName": "...",
#     "noPagesInDocument": 99,
#     "noParagraphsInDocument": 99,
#     "noSentencesInDocument": 99,
#     "noLinesInDocument": 99,
#     "noTokensInDocument": 99,
#     "pages": [...]
# }
TokenDocument = dict[str, int | TokenPages | str]


class TokenizerSpacy:
    """Determine footer and header lines.

    Returns:
        _type_: TokenizeSpacy instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        try:
            cfg.glob.setup.exists()  # type: ignore
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'Setup' does not yet exist.",
            )

        self._column_no: int = 0
        self._column_span: int = 0

        self._full_name = ""

        self._line_type = ""
        self._lower_left_x = 0.0

        self._no_lines_in_doc = 0
        self._no_lines_in_page = 0
        self._no_lines_in_para = 0
        self._no_pages_in_doc = 0
        self._no_paras_in_doc = 0
        self._no_paras_in_page = 0
        self._no_sents_in_doc = 0
        self._no_sents_in_page = 0
        self._no_tokens_in_doc = 0
        self._no_tokens_in_page = 0
        self._no_tokens_in_para = 0
        self._no_tokens_in_sent = 0

        self._page_no = 0
        self._para_lines: list[str] = []
        self._para_no = 0
        self._para_no_prev = 0
        self._para_text = ""
        self._processing_ok = False

        self._row_no: int = 0

        self._sent_no = 0
        self._sentence = ""

        self._token_pages: TokenPages = []
        self._token_paras: TokenParas = []
        self._token_sents: TokenSents = []
        self._token_tokens: TokenTokens = []

        self._pipeline_name = db.cls_db_core.DBCore.DBC_CODE_SPACY_DEFAULT
        self._nlp: spacy.Language = spacy.load(self._pipeline_name)

        self._exist = True

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finish current document.
    # -----------------------------------------------------------------------------
    def _finish_document(self) -> None:
        """Finish current ent."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        try:
            cfg.glob.document.exists()  # type: ignore
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'Document' does not yet exist.",
            )

        if cfg.glob.setup.is_tokenize_2_jsonfile:
            with open(self._full_name, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    {
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: cfg.glob.document.document_id,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: cfg.glob.document.document_file_name,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_FOOTER: cfg.glob.document.document_no_lines_footer,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADER: cfg.glob.document.document_no_lines_header,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_DOC: self._no_lines_in_doc,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC: cfg.glob.document.document_no_lines_toc,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_PAGES_IN_DOC: self._no_pages_in_doc,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_DOC: self._no_paras_in_doc,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_SENTS_IN_DOC: self._no_sents_in_doc,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_DOC: self._no_tokens_in_doc,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGES: self._token_pages,
                    },
                    file_handle,
                    indent=cfg.glob.setup.json_indent,
                    sort_keys=cfg.glob.setup.is_json_sort_keys,
                )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finish current page.
    # -----------------------------------------------------------------------------
    def _finish_page(self) -> None:
        """Finish current page."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._no_pages_in_doc += 1

        if cfg.glob.setup.is_tokenize_2_jsonfile:
            self._token_pages.append(
                {
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: self._page_no,
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PAGE: self._no_lines_in_page,
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_PAGE: self._no_paras_in_page,
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_SENTS_IN_PAGE: self._no_sents_in_page,
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_PAGE: self._no_tokens_in_page,
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_PARAS: self._token_paras,
                }
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finish current paragraph.
    # -----------------------------------------------------------------------------
    def _finish_para(self) -> None:
        """Finish current paragraph."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._para_text = " ".join(self._para_lines)

        self._no_paras_in_doc += 1
        self._no_paras_in_page += 1

        self._process_sents()

        if cfg.glob.setup.is_tokenize_2_jsonfile:
            self._token_paras.append(
                {
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: self._para_no_prev,
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PARA: self._no_lines_in_para,
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_SENTS_IN_PARA: self._sent_no,
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_PARA: self._no_tokens_in_para,
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_SENTS: self._token_sents,
                }
            )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finish current sentence.
    # -----------------------------------------------------------------------------
    def _finish_sent(self) -> None:
        """Finish current sentence."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        try:
            cfg.glob.document.exists()  # type: ignore
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'Document' does not yet exist.",
            )

        self._no_sents_in_doc += 1
        self._no_sents_in_page += 1

        self._sent_no += 1

        if self._line_type[:2] == db.cls_document.Document.DOCUMENT_LINE_TYPE_HEADING and self._sent_no > 1:
            line_type = db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY
        else:
            line_type = self._line_type

        if cfg.glob.setup.is_tokenize_2_database:
            db.cls_token.Token(
                id_document=cfg.glob.document.document_id,
                column_no=self._column_no,
                column_span=self._column_span,
                line_type=line_type,
                lower_left_x=self._lower_left_x,
                no_tokens_in_sent=self._no_tokens_in_sent,
                page_no=self._page_no,
                para_no=self._para_no_prev,
                row_no=self._row_no,
                sent_no=self._sent_no,
                text=self._sentence,
                tokens=self._token_tokens,  # type: ignore
            )

        if cfg.glob.setup.is_tokenize_2_jsonfile:
            if self._column_no > 0:
                if self._column_span > 0:
                    self._token_sents.append(
                        {
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_SENT_NO: self._sent_no,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO: self._column_no,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN: self._column_span,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: line_type,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_LOWER_LEFT_X: self._lower_left_x,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT: self._no_tokens_in_sent,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO: self._row_no,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._sentence,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKENS: self._token_tokens,
                        }
                    )
                else:
                    self._token_sents.append(
                        {
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_SENT_NO: self._sent_no,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO: self._column_no,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: line_type,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_LOWER_LEFT_X: self._lower_left_x,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT: self._no_tokens_in_sent,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO: self._row_no,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._sentence,
                            nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKENS: self._token_tokens,
                        }
                    )
            else:
                self._token_sents.append(
                    {
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_SENT_NO: self._sent_no,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: line_type,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_LOWER_LEFT_X: self._lower_left_x,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT: self._no_tokens_in_sent,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._sentence,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKENS: self._token_tokens,
                    }
                )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Determine the requested token attributes.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _get_token_attributes(token: spacy.tokens.Token) -> TokenToken:  # type: ignore # noqa: C901
        """Determine the requested token attributes.

        Args:
            token (spacy.tokens.Token):
                SpaCy tokens.

        Returns:
            Token:
                Requested token attributes.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        token_attr: dict[str, bool | float | int | str] = {}

        if (
            token.is_bracket  # pylint: disable=too-many-boolean-expressions
            and cfg.glob.setup.is_spacy_ignore_bracket
            or token.is_left_punct
            and cfg.glob.setup.is_spacy_ignore_left_punct
            or token.is_punct
            and cfg.glob.setup.is_spacy_ignore_punct
            or token.is_quote
            and cfg.glob.setup.is_spacy_ignore_quote
            or token.is_right_punct
            and cfg.glob.setup.is_spacy_ignore_right_punct
            or token.is_space
            and cfg.glob.setup.is_spacy_ignore_space
            or token.is_stop
            and cfg.glob.setup.is_spacy_ignore_stop
        ):
            return token_attr

        if cfg.glob.setup.is_spacy_tkn_attr_cluster:
            if token.cluster != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_CLUSTER] = token.cluster

        if cfg.glob.setup.is_spacy_tkn_attr_dep_:
            if token.dep_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_DEP_] = token.dep_

        if cfg.glob.setup.is_spacy_tkn_attr_doc:
            if token.doc is not None:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_DOC] = token.doc.text

        if cfg.glob.setup.is_spacy_tkn_attr_ent_iob_:
            if token.ent_iob_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ENT_IOB_] = token.ent_iob_

        if cfg.glob.setup.is_spacy_tkn_attr_ent_kb_id_:
            # not testable
            if token.ent_kb_id_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ENT_KB_ID_] = token.ent_kb_id_

        if cfg.glob.setup.is_spacy_tkn_attr_ent_type_:
            if token.ent_type_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ENT_TYPE_] = token.ent_type_

        if cfg.glob.setup.is_spacy_tkn_attr_head:
            if token.head is not None:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_HEAD] = token.head.i

        if cfg.glob.setup.is_spacy_tkn_attr_i:
            token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_I] = token.i

        if cfg.glob.setup.is_spacy_tkn_attr_idx:
            if token.idx != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IDX] = token.idx

        if cfg.glob.setup.is_spacy_tkn_attr_is_alpha:
            if token.is_alpha:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_ALPHA] = token.is_alpha

        if cfg.glob.setup.is_spacy_tkn_attr_is_ascii:
            if token.is_ascii:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_ASCII] = token.is_ascii

        if cfg.glob.setup.is_spacy_tkn_attr_is_bracket:
            if token.is_bracket:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_BRACKET] = token.is_bracket

        if cfg.glob.setup.is_spacy_tkn_attr_is_currency:
            if token.is_currency:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_CURRENCY] = token.is_currency

        if cfg.glob.setup.is_spacy_tkn_attr_is_digit:
            if token.is_digit:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_DIGIT] = token.is_digit

        if cfg.glob.setup.is_spacy_tkn_attr_is_left_punct:
            if token.is_left_punct:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_LEFT_PUNCT] = token.is_left_punct

        if cfg.glob.setup.is_spacy_tkn_attr_is_lower:
            if token.is_lower:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_LOWER] = token.is_lower

        if cfg.glob.setup.is_spacy_tkn_attr_is_oov:
            if token.is_oov:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_OOV] = token.is_oov

        if cfg.glob.setup.is_spacy_tkn_attr_is_punct:
            if token.is_punct:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_PUNCT] = token.is_punct

        if cfg.glob.setup.is_spacy_tkn_attr_is_quote:
            if token.is_quote:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_QUOTE] = token.is_quote

        if cfg.glob.setup.is_spacy_tkn_attr_is_right_punct:
            if token.is_right_punct:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_RIGHT_PUNCT] = token.is_right_punct

        if cfg.glob.setup.is_spacy_tkn_attr_is_sent_end:
            if token.is_sent_end:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_SENT_END] = token.is_sent_end

        if cfg.glob.setup.is_spacy_tkn_attr_is_sent_start:
            if token.is_sent_start:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_SENT_START] = token.is_sent_start

        if cfg.glob.setup.is_spacy_tkn_attr_is_space:
            if token.is_space:
                # not testable
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_SPACE] = token.is_space

        if cfg.glob.setup.is_spacy_tkn_attr_is_stop:
            if token.is_stop:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_STOP] = token.is_stop

        if cfg.glob.setup.is_spacy_tkn_attr_is_title:
            if token.is_title:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_TITLE] = token.is_title

        if cfg.glob.setup.is_spacy_tkn_attr_is_upper:
            if token.is_upper:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_UPPER] = token.is_upper

        if cfg.glob.setup.is_spacy_tkn_attr_lang_:
            if token.lang_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LANG_] = token.lang_

        if cfg.glob.setup.is_spacy_tkn_attr_left_edge:
            if token.left_edge.text is not None:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEFT_EDGE] = token.left_edge.i

        if cfg.glob.setup.is_spacy_tkn_attr_lemma_:
            if token.lemma_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEMMA_] = token.lemma_

        if cfg.glob.setup.is_spacy_tkn_attr_lex:
            if token.lex is not None:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEX] = token.lex.text

        if cfg.glob.setup.is_spacy_tkn_attr_lex_id:
            if token.lex_id != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEX_ID] = token.lex_id

        if cfg.glob.setup.is_spacy_tkn_attr_like_email:
            if token.like_email:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LIKE_EMAIL] = token.like_email

        if cfg.glob.setup.is_spacy_tkn_attr_like_num:
            if token.like_num:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LIKE_NUM] = token.like_num

        if cfg.glob.setup.is_spacy_tkn_attr_like_url:
            if token.like_url:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LIKE_URL] = token.like_url

        if cfg.glob.setup.is_spacy_tkn_attr_lower_:
            if token.lower_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LOWER_] = token.lower_

        if cfg.glob.setup.is_spacy_tkn_attr_morph:
            if token.morph is not None:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_MORPH] = str(token.morph)

        if cfg.glob.setup.is_spacy_tkn_attr_norm_:
            if token.norm_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_NORM_] = token.norm_

        if cfg.glob.setup.is_spacy_tkn_attr_orth_:
            if token.orth_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ORTH_] = token.orth_

        if cfg.glob.setup.is_spacy_tkn_attr_pos_:
            if token.pos_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_POS_] = token.pos_

        if cfg.glob.setup.is_spacy_tkn_attr_prefix_:
            if token.prefix_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_PREFIX_] = token.prefix_

        if cfg.glob.setup.is_spacy_tkn_attr_prob:
            if token.prob != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_PROB] = token.prob

        if cfg.glob.setup.is_spacy_tkn_attr_rank:
            if token.rank != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_RANK] = token.rank

        if cfg.glob.setup.is_spacy_tkn_attr_right_edge:
            if token.right_edge is not None:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_RIGHT_EDGE] = token.right_edge.i

        if cfg.glob.setup.is_spacy_tkn_attr_sent:
            if token.sent is not None:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SENT] = token.sent.text

        if cfg.glob.setup.is_spacy_tkn_attr_sentiment:
            if token.sentiment != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SENTIMENT] = token.sentiment

        if cfg.glob.setup.is_spacy_tkn_attr_shape_:
            if token.shape_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SHAPE_] = token.shape_

        if cfg.glob.setup.is_spacy_tkn_attr_suffix_:
            if token.suffix_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SUFFIX_] = token.suffix_

        if cfg.glob.setup.is_spacy_tkn_attr_tag_:
            if token.tag_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TAG_] = token.tag_

        if cfg.glob.setup.is_spacy_tkn_attr_tensor:
            try:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TENSOR] = str(token.tensor)
            except IndexError:
                pass

        if cfg.glob.setup.is_spacy_tkn_attr_text:
            if token.text != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TEXT] = token.text

        if cfg.glob.setup.is_spacy_tkn_attr_text_with_ws:
            if token.text_with_ws != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TEXT_WITH_WS] = token.text_with_ws

        if cfg.glob.setup.is_spacy_tkn_attr_vocab:
            if token.vocab is not None:
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_RANK] = str(token.vocab)

        if cfg.glob.setup.is_spacy_tkn_attr_whitespace_:
            if token.whitespace_ != "":
                token_attr[nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_WHITESPACE_] = token.whitespace_

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return token_attr

    # -----------------------------------------------------------------------------
    # Initialise a new document.
    # -----------------------------------------------------------------------------
    def _init_document(self) -> None:
        """Initialize a new document."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._no_lines_in_doc = 0
        self._no_pages_in_doc = 0
        self._no_paras_in_doc = 0
        self._no_sents_in_doc = 0
        self._no_tokens_in_doc = 0

        self._token_pages = []

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise a new page.
    # -----------------------------------------------------------------------------
    def _init_page(self) -> None:
        """Initialize a new page."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._no_lines_in_page = 0
        self._no_paras_in_page = 0
        self._no_sents_in_page = 0
        self._no_tokens_in_page = 0

        self._token_paras = []

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise a new paragraph.
    # -----------------------------------------------------------------------------
    def _init_para(self) -> None:
        """Initialize a new paragraph."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        try:
            cfg.glob.text_parser.exists()
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'TextParser' does not yet exist.",
            )

        if nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO in cfg.glob.text_parser.parse_result_line_line:
            self._column_no = cfg.glob.text_parser.parse_result_line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO]
            self._row_no = cfg.glob.text_parser.parse_result_line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO]
            if nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN in cfg.glob.text_parser.parse_result_line_line:
                self._column_span = cfg.glob.text_parser.parse_result_line_line[
                    nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN
                ]
            else:
                self._column_span = 0
        else:
            self._column_no = 0
            self._column_span = 0
            self._row_no = 0

        self._lower_left_x = cfg.glob.text_parser.parse_result_line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LOWER_LEFT_X]

        self._no_lines_in_para = 0
        self._no_tokens_in_para = 0

        self._para_lines = []

        self._token_sents = []

        self._para_no_prev = self._para_no

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Initialise a new sentence.
    # -----------------------------------------------------------------------------
    def _init_sent(self) -> None:
        """Initialize a new sentence."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._no_tokens_in_sent = 0

        self._token_tokens = []

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Process a whole new page.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process a whole new page."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        try:
            cfg.glob.text_parser.exists()
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'TextParser' does not yet exist.",
            )

        self._para_no_prev = 0

        # {
        #    "columnNo": 99,
        #    "columnSpan": 99,
        #    "lineNo": 99,
        #    "lineIndexPage": 99,
        #    "lineIndexParagraph": 99,
        #    "lineType": "b",
        #    "lowerLeftX": 99.99,
        #    "paragraphNo": 99,
        #    "rowNo": 99,
        #    "text": "..."
        # },
        for cfg.glob.text_parser.parse_result_line_line in cfg.glob.text_parser.parse_result_line_page[
            nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES
        ]:
            line_type = cfg.glob.text_parser.parse_result_line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]

            if (
                line_type == cfg.glob.document.DOCUMENT_LINE_TYPE_FOOTER  # pylint: disable=too-many-boolean-expressions
                and cfg.glob.setup.is_spacy_ignore_line_type_footer
                or line_type == cfg.glob.document.DOCUMENT_LINE_TYPE_HEADER
                and cfg.glob.setup.is_spacy_ignore_line_type_header
                or line_type == cfg.glob.document.DOCUMENT_LINE_TYPE_HEADING
                and cfg.glob.setup.is_spacy_ignore_line_type_heading
                or line_type == cfg.glob.document.DOCUMENT_LINE_TYPE_LIST_BULLETED
                and cfg.glob.setup.is_spacy_ignore_line_type_list_bulleted
                or line_type == cfg.glob.document.DOCUMENT_LINE_TYPE_LIST_NUMBERED
                and cfg.glob.setup.is_spacy_ignore_line_type_list_numbered
                or line_type == cfg.glob.document.DOCUMENT_LINE_TYPE_TABLE
                and cfg.glob.setup.is_spacy_ignore_line_type_table
                or line_type == cfg.glob.document.DOCUMENT_LINE_TYPE_TOC
                and cfg.glob.setup.is_spacy_ignore_line_type_toc
            ):
                continue

            self._para_no = cfg.glob.text_parser.parse_result_line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]

            if self._para_no_prev == 0:
                self._init_para()
            elif self._para_no != self._para_no_prev:
                self._finish_para()
                self._init_para()

            self._process_para()

        if self._para_no_prev > 0:
            self._finish_para()

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Process a whole new paragraph.
    # -----------------------------------------------------------------------------
    def _process_para(self) -> None:
        """Process a whole new paragraph."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        try:
            cfg.glob.text_parser.exists()
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'TextParser' does not yet exist.",
            )

        self._no_lines_in_doc += 1
        self._no_lines_in_page += 1
        self._no_lines_in_para += 1

        if not self._para_lines:
            self._line_type = cfg.glob.text_parser.parse_result_line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]

        self._para_lines.append(cfg.glob.text_parser.parse_result_line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Process all sentences of a paragraph.
    # -----------------------------------------------------------------------------
    def _process_sents(self) -> None:
        """Process all sentences of a paragraph."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._sent_no = 0

        paragraph = self._nlp(self._para_text)

        for sent in paragraph.sents:
            self._sentence = sent.text

            self._init_sent()

            self._process_tokens()

            self._finish_sent()

    # -----------------------------------------------------------------------------
    # Process all tokens of a sentence.
    # -----------------------------------------------------------------------------
    def _process_tokens(self) -> None:
        """Process all tokens of a sentence."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._token_no = 0

        sentence = self._nlp(self._sentence)

        for token in sentence:
            if (token_token := self._get_token_attributes(token)) != {}:
                self._no_tokens_in_doc += 1
                self._no_tokens_in_page += 1
                self._no_tokens_in_para += 1
                self._no_tokens_in_sent += 1
                self._token_tokens.append(token_token)

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
    # Process a whole new document.
    # -----------------------------------------------------------------------------
    def process_document(self, full_name: str, pipeline_name: str) -> None:
        """Process a whole new document.

        Args:
            full_name (str):
                    Output file name.
            pipeline_name (str):
                    Spacy pipeline name.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        try:
            cfg.glob.setup.exists()  # type: ignore
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'Setup' does not yet exist.",
            )

        try:
            cfg.glob.text_parser.exists()
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'TextParser' does not yet exist.",
            )

        self._processing_ok = False

        self._full_name = full_name

        if pipeline_name != self._pipeline_name:
            self._nlp = spacy.load(pipeline_name)
            self._pipeline_name = pipeline_name

        self._init_document()

        # {
        #   "pageNo": 99,
        #   "noParagraphsInPage": 99,
        #   "noLinesInPage": 99,
        #   "lines": [...]
        # }
        for cfg.glob.text_parser.parse_result_line_page in cfg.glob.text_parser.parse_result_line_document[
            nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGES
        ]:
            self._page_no = cfg.glob.text_parser.parse_result_line_page[nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]

            self._init_page()
            self._process_page()
            self._finish_page()

        self._finish_document()

        self._processing_ok = True

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Check the processing result.
    # -----------------------------------------------------------------------------
    def processing_ok(self) -> bool:
        """Check the processing result.

        Returns:
            bool:   True if processing has been completed without errors.
        """
        return self._processing_ok
