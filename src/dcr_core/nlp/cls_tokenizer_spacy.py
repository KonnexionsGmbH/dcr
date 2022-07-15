"""Module nlp.cls_line_type: Determine footer and header lines."""
from __future__ import annotations

import json

import spacy
import spacy.tokens

import dcr_core.cfg.glob
import dcr_core.nlp.cls_nlp_core
import dcr_core.utils


# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-statements
class TokenizerSpacy:
    """Determine footer and header lines.

    Returns:
        _type_: TokenizeSpacy instance.
    """

    TokenToken = dict[str, bool | float | int | str]
    TokenTokens = list[TokenToken]

    TokenSent = dict[str, float | int | None | str | TokenTokens]
    TokenSents = list[TokenSent]

    TokenPara = dict[str, int | TokenSents]
    TokenParas = list[TokenPara]

    TokenPage = dict[str, int | TokenParas]
    TokenPages = list[TokenPage]

    TokenDocument = dict[str, int | TokenPages | str]

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        self._document_file_name: str = ""
        self._document_id: int = 0
        self._document_no_lines_footer: int = 0
        self._document_no_lines_header: int = 0
        self._document_no_lines_toc: int = 0
        self._file_encoding: str = ""
        self._full_name = ""
        self._is_json_sort_keys: bool = False
        self._is_spacy_ignore_bracket: bool = False
        self._is_spacy_ignore_left_punct: bool = False
        self._is_spacy_ignore_line_type_footer: bool = False
        self._is_spacy_ignore_line_type_header: bool = False
        self._is_spacy_ignore_line_type_heading: bool = False
        self._is_spacy_ignore_line_type_list_bullet: bool = False
        self._is_spacy_ignore_line_type_list_number: bool = False
        self._is_spacy_ignore_line_type_table: bool = False
        self._is_spacy_ignore_line_type_toc: bool = False
        self._is_spacy_ignore_punct: bool = False
        self._is_spacy_ignore_quote: bool = False
        self._is_spacy_ignore_right_punct: bool = False
        self._is_spacy_ignore_space: bool = False
        self._is_spacy_ignore_stop: bool = False
        self._is_spacy_tkn_attr_cluster: bool = False
        self._is_spacy_tkn_attr_dep_: bool = False
        self._is_spacy_tkn_attr_doc: bool = False
        self._is_spacy_tkn_attr_ent_iob_: bool = False
        self._is_spacy_tkn_attr_ent_kb_id_: bool = False
        self._is_spacy_tkn_attr_ent_type_: bool = False
        self._is_spacy_tkn_attr_head: bool = False
        self._is_spacy_tkn_attr_i: bool = False
        self._is_spacy_tkn_attr_idx: bool = False
        self._is_spacy_tkn_attr_is_alpha: bool = False
        self._is_spacy_tkn_attr_is_ascii: bool = False
        self._is_spacy_tkn_attr_is_bracket: bool = False
        self._is_spacy_tkn_attr_is_currency: bool = False
        self._is_spacy_tkn_attr_is_digit: bool = False
        self._is_spacy_tkn_attr_is_left_punct: bool = False
        self._is_spacy_tkn_attr_is_lower: bool = False
        self._is_spacy_tkn_attr_is_oov: bool = False
        self._is_spacy_tkn_attr_is_punct: bool = False
        self._is_spacy_tkn_attr_is_quote: bool = False
        self._is_spacy_tkn_attr_is_right_punct: bool = False
        self._is_spacy_tkn_attr_is_sent_end: bool = False
        self._is_spacy_tkn_attr_is_sent_start: bool = False
        self._is_spacy_tkn_attr_is_space: bool = False
        self._is_spacy_tkn_attr_is_stop: bool = False
        self._is_spacy_tkn_attr_is_title: bool = False
        self._is_spacy_tkn_attr_is_upper: bool = False
        self._is_spacy_tkn_attr_lang_: bool = False
        self._is_spacy_tkn_attr_left_edge: bool = False
        self._is_spacy_tkn_attr_lemma_: bool = False
        self._is_spacy_tkn_attr_lex: bool = False
        self._is_spacy_tkn_attr_lex_id: bool = False
        self._is_spacy_tkn_attr_like_email: bool = False
        self._is_spacy_tkn_attr_like_num: bool = False
        self._is_spacy_tkn_attr_like_url: bool = False
        self._is_spacy_tkn_attr_lower_: bool = False
        self._is_spacy_tkn_attr_morph: bool = False
        self._is_spacy_tkn_attr_norm_: bool = False
        self._is_spacy_tkn_attr_orth_: bool = False
        self._is_spacy_tkn_attr_pos_: bool = False
        self._is_spacy_tkn_attr_prefix_: bool = False
        self._is_spacy_tkn_attr_prob: bool = False
        self._is_spacy_tkn_attr_rank: bool = False
        self._is_spacy_tkn_attr_right_edge: bool = False
        self._is_spacy_tkn_attr_sent: bool = False
        self._is_spacy_tkn_attr_sentiment: bool = False
        self._is_spacy_tkn_attr_shape_: bool = False
        self._is_spacy_tkn_attr_suffix_: bool = False
        self._is_spacy_tkn_attr_tag_: bool = False
        self._is_spacy_tkn_attr_tensor: bool = False
        self._is_spacy_tkn_attr_text: bool = False
        self._is_spacy_tkn_attr_text_with_ws: bool = False
        self._is_spacy_tkn_attr_vocab: bool = False
        self._is_spacy_tkn_attr_whitespace_: bool = False
        self._is_tokenize_2_jsonfile: bool = False
        self._json_indent = ""
        self._pipeline_name = dcr_core.nlp.cls_nlp_core.NLPCore.CODE_SPACY_DEFAULT
        self._nlp: spacy.Language = spacy.load(self._pipeline_name)

        self._column_no: int = 0
        self._column_span: int = 0
        self._coord_llx = 0.0
        self._coord_urx = 0.0

        self._line_type = ""

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

        self._token_paras: TokenizerSpacy.TokenParas = []
        self._token_sents: TokenizerSpacy.TokenSents = []
        self._token_tokens: TokenizerSpacy.TokenTokens = []

        self.token_pages: TokenizerSpacy.TokenPages = []

        self._exist = True

    # -----------------------------------------------------------------------------
    # Finish current document.
    # -----------------------------------------------------------------------------
    # {
    #     "documentId": 99,
    #     "documentFileName": "xxx",
    #     "noLinesFooter": 99,
    #     "noLinesHeader": 99,
    #     "noLinesInDocument": 99,
    #     "noLinesToc": 99,
    #     "noListsBulletInDocument": 99,
    #     "noListsNumberInDocument": 99,
    #     "noPagesInDocument": 99,
    #     "noParagraphsInDocument": 99,
    #     "noSentencesInDocument": 99,
    #     "noTablesInDocument": 99,
    #     "noTokensInDocument": 99,
    #     "pages": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _finish_document(self) -> None:
        """Finish current ent."""
        dcr_core.utils.check_exists_object(
            is_text_parser=True,
        )

        json_data = {
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: self._document_id,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: self._document_file_name,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_FOOTER: self._document_no_lines_footer,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADER: self._document_no_lines_header,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_DOC: self._no_lines_in_doc,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC: self._document_no_lines_toc,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET_IN_DOC: dcr_core.cfg.glob.text_parser.parse_result_line_document[
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET_IN_DOC
            ],
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER_IN_DOC: dcr_core.cfg.glob.text_parser.parse_result_line_document[
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER_IN_DOC
            ],
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_PAGES_IN_DOC: self._no_pages_in_doc,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_DOC: self._no_paras_in_doc,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_SENTS_IN_DOC: self._no_sents_in_doc,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TABLES_IN_DOC: dcr_core.cfg.glob.text_parser.parse_result_line_document[
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TABLES_IN_DOC
            ],
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_DOC: self._no_tokens_in_doc,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGES: self.token_pages,
        }

        if self._is_tokenize_2_jsonfile:
            with open(self._full_name, "w", encoding=self._file_encoding) as file_handle:
                json.dump(
                    json_data,
                    file_handle,
                    indent=self._json_indent,
                    sort_keys=self._is_json_sort_keys,
                )

    # -----------------------------------------------------------------------------
    # Finish current page.
    # -----------------------------------------------------------------------------
    # {
    #     "pageNo": 99,
    #     "noLinesInPage": 99,
    #     "noParagraphsInPage": 99,
    #     "noSentencesInPage": 99,
    #     "noTokensInPage": 99,
    #     "paragraphs": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _finish_page(self) -> None:
        """Finish current page."""
        self._no_pages_in_doc += 1

        self.token_pages.append(
            {
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: self._page_no,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PAGE: self._no_lines_in_page,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_PAGE: self._no_paras_in_page,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_SENTS_IN_PAGE: self._no_sents_in_page,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_PAGE: self._no_tokens_in_page,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARAS: self._token_paras,
            }
        )

    # -----------------------------------------------------------------------------
    # Finish current paragraph.
    # -----------------------------------------------------------------------------
    # {
    #     "paragraphNo": 99,
    #     "noLinesInParagraph": 99,
    #     "noSentencesInParagraph": 99,
    #     "noTokensInParagraph": 99,
    #     "sentences": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _finish_para(self) -> None:
        """Finish current paragraph."""
        self._para_text = " ".join(self._para_lines)

        self._no_paras_in_doc += 1
        self._no_paras_in_page += 1

        self._process_sents()

        self._token_paras.append(
            {
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: self._para_no_prev,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PARA: self._no_lines_in_para,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_SENTS_IN_PARA: self._sent_no,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_PARA: self._no_tokens_in_para,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_SENTS: self._token_sents,
            }
        )

    # -----------------------------------------------------------------------------
    # Finish current sentence.
    # -----------------------------------------------------------------------------
    # {
    #     "sentenceNo": 99,
    #     "columnNo": 99,
    #     "coordLLX": 99.99,
    #     "coordURX": 99.99,
    #     "lineType": "xxx",
    #     "noTokensInSentence": 99,
    #     "rowNo": 99,
    #     "text": "xxx",
    #     "tokens": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _finish_sent(self) -> None:
        """Finish current sentence."""
        self._no_sents_in_doc += 1
        self._no_sents_in_page += 1

        self._sent_no += 1

        if self._line_type[:2] == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_HEADING and self._sent_no > 1:
            line_type = dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_BODY
        else:
            line_type = self._line_type

        if self._column_no > 0:
            if self._column_span > 0:
                self._token_sents.append(
                    {
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_SENT_NO: self._sent_no,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO: self._column_no,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN: self._column_span,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX: self._coord_llx,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX: self._coord_urx,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: line_type,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT: self._no_tokens_in_sent,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO: self._row_no,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._sentence,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKENS: self._token_tokens,
                    }
                )
            else:
                self._token_sents.append(
                    {
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_SENT_NO: self._sent_no,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO: self._column_no,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX: self._coord_llx,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX: self._coord_urx,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: line_type,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT: self._no_tokens_in_sent,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO: self._row_no,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._sentence,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKENS: self._token_tokens,
                    }
                )
        else:
            self._token_sents.append(
                {
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_SENT_NO: self._sent_no,
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX: self._coord_llx,
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX: self._coord_urx,
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: line_type,
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TOKENS_IN_SENT: self._no_tokens_in_sent,
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._sentence,
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKENS: self._token_tokens,
                }
            )

    # -----------------------------------------------------------------------------
    # Determine the requested token attributes.
    # -----------------------------------------------------------------------------
    def _get_token_attributes(self, token: spacy.tokens.Token) -> TokenToken:  # type: ignore # noqa: C901
        """Determine the requested token attributes.

        Args:
            token (spacy.tokens.Token):
                spaCy tokens.

        Returns:
            Token:
                Requested token attributes.
        """
        token_attr: dict[str, bool | float | int | str] = {}

        if (
            token.is_bracket  # pylint: disable=too-many-boolean-expressions
            and self._is_spacy_ignore_bracket
            or token.is_left_punct
            and self._is_spacy_ignore_left_punct
            or token.is_punct
            and self._is_spacy_ignore_punct
            or token.is_quote
            and self._is_spacy_ignore_quote
            or token.is_right_punct
            and self._is_spacy_ignore_right_punct
            or token.is_space
            and self._is_spacy_ignore_space
            or token.is_stop
            and self._is_spacy_ignore_stop
        ):
            return token_attr

        if self._is_spacy_tkn_attr_cluster:
            if token.cluster != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_CLUSTER] = token.cluster

        if self._is_spacy_tkn_attr_dep_:
            if token.dep_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_DEP_] = token.dep_

        if self._is_spacy_tkn_attr_doc:
            if token.doc is not None:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_DOC] = token.doc.text

        if self._is_spacy_tkn_attr_ent_iob_:
            if token.ent_iob_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ENT_IOB_] = token.ent_iob_

        if self._is_spacy_tkn_attr_ent_kb_id_:
            # not testable
            if token.ent_kb_id_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ENT_KB_ID_] = token.ent_kb_id_

        if self._is_spacy_tkn_attr_ent_type_:
            if token.ent_type_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ENT_TYPE_] = token.ent_type_

        if self._is_spacy_tkn_attr_head:
            if token.head is not None:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_HEAD] = token.head.i

        if self._is_spacy_tkn_attr_i:
            token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_I] = token.i

        if self._is_spacy_tkn_attr_idx:
            if token.idx != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IDX] = token.idx

        if self._is_spacy_tkn_attr_is_alpha:
            if token.is_alpha:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_ALPHA] = token.is_alpha

        if self._is_spacy_tkn_attr_is_ascii:
            if token.is_ascii:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_ASCII] = token.is_ascii

        if self._is_spacy_tkn_attr_is_bracket:
            if token.is_bracket:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_BRACKET] = token.is_bracket

        if self._is_spacy_tkn_attr_is_currency:
            if token.is_currency:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_CURRENCY] = token.is_currency

        if self._is_spacy_tkn_attr_is_digit:
            if token.is_digit:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_DIGIT] = token.is_digit

        if self._is_spacy_tkn_attr_is_left_punct:
            if token.is_left_punct:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_LEFT_PUNCT] = token.is_left_punct

        if self._is_spacy_tkn_attr_is_lower:
            if token.is_lower:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_LOWER] = token.is_lower

        if self._is_spacy_tkn_attr_is_oov:
            if token.is_oov:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_OOV] = token.is_oov

        if self._is_spacy_tkn_attr_is_punct:
            if token.is_punct:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_PUNCT] = token.is_punct

        if self._is_spacy_tkn_attr_is_quote:
            if token.is_quote:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_QUOTE] = token.is_quote

        if self._is_spacy_tkn_attr_is_right_punct:
            if token.is_right_punct:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_RIGHT_PUNCT] = token.is_right_punct

        if self._is_spacy_tkn_attr_is_sent_end:
            if token.is_sent_end:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_SENT_END] = token.is_sent_end

        if self._is_spacy_tkn_attr_is_sent_start:
            if token.is_sent_start:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_SENT_START] = token.is_sent_start

        if self._is_spacy_tkn_attr_is_space:
            if token.is_space:
                # not testable
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_SPACE] = token.is_space

        if self._is_spacy_tkn_attr_is_stop:
            if token.is_stop:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_STOP] = token.is_stop

        if self._is_spacy_tkn_attr_is_title:
            if token.is_title:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_TITLE] = token.is_title

        if self._is_spacy_tkn_attr_is_upper:
            if token.is_upper:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_IS_UPPER] = token.is_upper

        if self._is_spacy_tkn_attr_lang_:
            if token.lang_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LANG_] = token.lang_

        if self._is_spacy_tkn_attr_left_edge:
            if token.left_edge.text is not None:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEFT_EDGE] = token.left_edge.i

        if self._is_spacy_tkn_attr_lemma_:
            if token.lemma_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEMMA_] = token.lemma_

        if self._is_spacy_tkn_attr_lex:
            if token.lex is not None:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEX] = token.lex.text

        if self._is_spacy_tkn_attr_lex_id:
            if token.lex_id != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LEX_ID] = token.lex_id

        if self._is_spacy_tkn_attr_like_email:
            if token.like_email:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LIKE_EMAIL] = token.like_email

        if self._is_spacy_tkn_attr_like_num:
            if token.like_num:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LIKE_NUM] = token.like_num

        if self._is_spacy_tkn_attr_like_url:
            if token.like_url:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LIKE_URL] = token.like_url

        if self._is_spacy_tkn_attr_lower_:
            if token.lower_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_LOWER_] = token.lower_

        if self._is_spacy_tkn_attr_morph:
            if token.morph is not None:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_MORPH] = str(token.morph)

        if self._is_spacy_tkn_attr_norm_:
            if token.norm_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_NORM_] = token.norm_

        if self._is_spacy_tkn_attr_orth_:
            if token.orth_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_ORTH_] = token.orth_

        if self._is_spacy_tkn_attr_pos_:
            if token.pos_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_POS_] = token.pos_

        if self._is_spacy_tkn_attr_prefix_:
            if token.prefix_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_PREFIX_] = token.prefix_

        if self._is_spacy_tkn_attr_prob:
            if token.prob != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_PROB] = token.prob

        if self._is_spacy_tkn_attr_rank:
            if token.rank != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_RANK] = token.rank

        if self._is_spacy_tkn_attr_right_edge:
            if token.right_edge is not None:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_RIGHT_EDGE] = token.right_edge.i

        if self._is_spacy_tkn_attr_sent:
            if token.sent is not None:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SENT] = token.sent.text

        if self._is_spacy_tkn_attr_sentiment:
            if token.sentiment != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SENTIMENT] = token.sentiment

        if self._is_spacy_tkn_attr_shape_:
            if token.shape_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SHAPE_] = token.shape_

        if self._is_spacy_tkn_attr_suffix_:
            if token.suffix_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_SUFFIX_] = token.suffix_

        if self._is_spacy_tkn_attr_tag_:
            if token.tag_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TAG_] = token.tag_

        if self._is_spacy_tkn_attr_tensor:
            try:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TENSOR] = str(token.tensor)
            except IndexError:
                pass

        if self._is_spacy_tkn_attr_text:
            if token.text != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TEXT] = token.text

        if self._is_spacy_tkn_attr_text_with_ws:
            if token.text_with_ws != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_TEXT_WITH_WS] = token.text_with_ws

        if self._is_spacy_tkn_attr_vocab:
            if token.vocab is not None:
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_RANK] = str(token.vocab)

        if self._is_spacy_tkn_attr_whitespace_:
            if token.whitespace_ != "":
                token_attr[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOKEN_WHITESPACE_] = token.whitespace_

        return token_attr

    # -----------------------------------------------------------------------------
    # Initialise a new document.
    # -----------------------------------------------------------------------------
    def _init_document(self) -> None:
        """Initialize a new document."""
        self._no_lines_in_doc = 0
        self._no_pages_in_doc = 0
        self._no_paras_in_doc = 0
        self._no_sents_in_doc = 0
        self._no_tokens_in_doc = 0

        self.token_pages = []

    # -----------------------------------------------------------------------------
    # Initialise a new page.
    # -----------------------------------------------------------------------------
    def _init_page(self) -> None:
        """Initialize a new page."""
        self._no_lines_in_page = 0
        self._no_paras_in_page = 0
        self._no_sents_in_page = 0
        self._no_tokens_in_page = 0

        self._token_paras = []

    # -----------------------------------------------------------------------------
    # Initialise a new paragraph.
    # -----------------------------------------------------------------------------
    def _init_para(self) -> None:
        """Initialize a new paragraph."""
        dcr_core.utils.check_exists_object(
            is_text_parser=True,
        )

        if dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO in dcr_core.cfg.glob.text_parser.parse_result_line_line:
            self._column_no = dcr_core.cfg.glob.text_parser.parse_result_line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO]
            self._row_no = dcr_core.cfg.glob.text_parser.parse_result_line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO]
            if dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN in dcr_core.cfg.glob.text_parser.parse_result_line_line:
                self._column_span = dcr_core.cfg.glob.text_parser.parse_result_line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN]
            else:
                self._column_span = 0
        else:
            self._column_no = 0
            self._column_span = 0
            self._row_no = 0

        self._coord_llx = dcr_core.cfg.glob.text_parser.parse_result_line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX]
        self._coord_urx = dcr_core.cfg.glob.text_parser.parse_result_line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX]

        self._no_lines_in_para = 0
        self._no_tokens_in_para = 0

        self._para_lines = []

        self._token_sents = []

        self._para_no_prev = self._para_no

    # -----------------------------------------------------------------------------
    # Initialise a new sentence.
    # -----------------------------------------------------------------------------
    def _init_sent(self) -> None:
        """Initialize a new sentence."""
        self._no_tokens_in_sent = 0

        self._token_tokens = []

    # -----------------------------------------------------------------------------
    # Process a whole new page.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process a whole new page."""
        dcr_core.utils.check_exists_object(
            is_text_parser=True,
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
        for dcr_core.cfg.glob.text_parser.parse_result_line_line in dcr_core.cfg.glob.text_parser.parse_result_line_page[
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES
        ]:
            line_type = dcr_core.cfg.glob.text_parser.parse_result_line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]

            if (
                line_type == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_FOOTER  # pylint: disable=too-many-boolean-expressions
                and self._is_spacy_ignore_line_type_footer
                or line_type == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_HEADER
                and self._is_spacy_ignore_line_type_header
                or line_type == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_HEADING
                and self._is_spacy_ignore_line_type_heading
                or line_type == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_LIST_BULLET
                and self._is_spacy_ignore_line_type_list_bullet
                or line_type == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_LIST_NUMBER
                and self._is_spacy_ignore_line_type_list_number
                or line_type == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_TABLE
                and self._is_spacy_ignore_line_type_table
                or line_type == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_TOC
                and self._is_spacy_ignore_line_type_toc
            ):
                continue

            self._para_no = dcr_core.cfg.glob.text_parser.parse_result_line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]

            if self._para_no_prev == 0:
                self._init_para()
            elif self._para_no != self._para_no_prev:
                self._finish_para()
                self._init_para()

            self._process_para()

        if self._para_no_prev > 0:
            self._finish_para()

    # -----------------------------------------------------------------------------
    # Process a whole new paragraph.
    # -----------------------------------------------------------------------------
    def _process_para(self) -> None:
        """Process a whole new paragraph."""
        dcr_core.utils.check_exists_object(
            is_text_parser=True,
        )

        self._no_lines_in_doc += 1
        self._no_lines_in_page += 1
        self._no_lines_in_para += 1

        if not self._para_lines:
            self._line_type = dcr_core.cfg.glob.text_parser.parse_result_line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]

        self._para_lines.append(dcr_core.cfg.glob.text_parser.parse_result_line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

    # -----------------------------------------------------------------------------
    # Process all sentences of a paragraph.
    # -----------------------------------------------------------------------------
    def _process_sents(self) -> None:
        """Process all sentences of a paragraph."""
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
    # {
    #     "tknI": 99,
    #     "tknIsOov": boolean,
    #     "tknIsTitle": boolean,
    #     "tknLemma_": "xxx",
    #     "tknNorm_": "xxx",
    #     "tknPos_": "xxx",
    #     "tknTag_": "xxx",
    #     "tknText": "xxx",
    #     "tknWhitespace_": "xxx"
    # }
    # -----------------------------------------------------------------------------
    def _process_tokens(self) -> None:
        """Process all tokens of a sentence."""
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
    def process_document(  # pylint: disable=too-many-arguments, too-many-locals
        self,
        document_file_name: str,
        document_id: int,
        document_no_lines_footer: int,
        document_no_lines_header: int,
        document_no_lines_toc: int,
        file_encoding: str,
        full_name: str,
        is_json_sort_keys: bool,
        is_spacy_ignore_bracket: bool,
        is_spacy_ignore_left_punct: bool,
        is_spacy_ignore_line_type_footer: bool,
        is_spacy_ignore_line_type_header: bool,
        is_spacy_ignore_line_type_heading: bool,
        is_spacy_ignore_line_type_list_bullet: bool,
        is_spacy_ignore_line_type_list_number: bool,
        is_spacy_ignore_line_type_table: bool,
        is_spacy_ignore_line_type_toc: bool,
        is_spacy_ignore_punct: bool,
        is_spacy_ignore_quote: bool,
        is_spacy_ignore_right_punct: bool,
        is_spacy_ignore_space: bool,
        is_spacy_ignore_stop: bool,
        is_spacy_tkn_attr_cluster: bool,
        is_spacy_tkn_attr_dep_: bool,
        is_spacy_tkn_attr_doc: bool,
        is_spacy_tkn_attr_ent_iob_: bool,
        is_spacy_tkn_attr_ent_kb_id_: bool,
        is_spacy_tkn_attr_ent_type_: bool,
        is_spacy_tkn_attr_head: bool,
        is_spacy_tkn_attr_i: bool,
        is_spacy_tkn_attr_idx: bool,
        is_spacy_tkn_attr_is_alpha: bool,
        is_spacy_tkn_attr_is_ascii: bool,
        is_spacy_tkn_attr_is_bracket: bool,
        is_spacy_tkn_attr_is_currency: bool,
        is_spacy_tkn_attr_is_digit: bool,
        is_spacy_tkn_attr_is_left_punct: bool,
        is_spacy_tkn_attr_is_lower: bool,
        is_spacy_tkn_attr_is_oov: bool,
        is_spacy_tkn_attr_is_punct: bool,
        is_spacy_tkn_attr_is_quote: bool,
        is_spacy_tkn_attr_is_right_punct: bool,
        is_spacy_tkn_attr_is_sent_end: bool,
        is_spacy_tkn_attr_is_sent_start: bool,
        is_spacy_tkn_attr_is_space: bool,
        is_spacy_tkn_attr_is_stop: bool,
        is_spacy_tkn_attr_is_title: bool,
        is_spacy_tkn_attr_is_upper: bool,
        is_spacy_tkn_attr_lang_: bool,
        is_spacy_tkn_attr_left_edge: bool,
        is_spacy_tkn_attr_lemma_: bool,
        is_spacy_tkn_attr_lex: bool,
        is_spacy_tkn_attr_lex_id: bool,
        is_spacy_tkn_attr_like_email: bool,
        is_spacy_tkn_attr_like_num: bool,
        is_spacy_tkn_attr_like_url: bool,
        is_spacy_tkn_attr_lower_: bool,
        is_spacy_tkn_attr_morph: bool,
        is_spacy_tkn_attr_norm_: bool,
        is_spacy_tkn_attr_orth_: bool,
        is_spacy_tkn_attr_pos_: bool,
        is_spacy_tkn_attr_prefix_: bool,
        is_spacy_tkn_attr_prob: bool,
        is_spacy_tkn_attr_rank: bool,
        is_spacy_tkn_attr_right_edge: bool,
        is_spacy_tkn_attr_sent: bool,
        is_spacy_tkn_attr_sentiment: bool,
        is_spacy_tkn_attr_shape_: bool,
        is_spacy_tkn_attr_suffix_: bool,
        is_spacy_tkn_attr_tag_: bool,
        is_spacy_tkn_attr_tensor: bool,
        is_spacy_tkn_attr_text: bool,
        is_spacy_tkn_attr_text_with_ws: bool,
        is_spacy_tkn_attr_vocab: bool,
        is_spacy_tkn_attr_whitespace_: bool,
        is_tokenize_2_jsonfile: bool,
        json_indent: str,
        pipeline_name: str,
    ) -> None:
        """Process a whole new document.

        Args:
            document_file_name (str): _description_
            document_id (int): _description_
            document_no_lines_footer (int): _description_
            document_no_lines_header (int): _description_
            document_no_lines_toc (int): _description_
            file_encoding (str): _description_
            full_name (str):
                    Output file name.
            is_json_sort_keys (bool): _description_
            is_spacy_ignore_bracket (bool): _description_
            is_spacy_ignore_left_punct (bool): _description_
            is_spacy_ignore_line_type_footer (bool): _description_
            is_spacy_ignore_line_type_header (bool): _description_
            is_spacy_ignore_line_type_heading (bool): _description_
            is_spacy_ignore_line_type_list_bullet (bool): _description_
            is_spacy_ignore_line_type_list_number (bool): _description_
            is_spacy_ignore_line_type_table (bool): _description_
            is_spacy_ignore_line_type_toc (bool): _description_
            is_spacy_ignore_punct (bool): _description_
            is_spacy_ignore_quote (bool): _description_
            is_spacy_ignore_right_punct (bool): _description_
            is_spacy_ignore_space (bool): _description_
            is_spacy_ignore_stop (bool): _description_
            is_spacy_tkn_attr_cluster (bool): _description_
            is_spacy_tkn_attr_dep_ (bool): _description_
            is_spacy_tkn_attr_doc (bool): _description_
            is_spacy_tkn_attr_ent_iob_ (bool): _description_
            is_spacy_tkn_attr_ent_kb_id_ (bool): _description_
            is_spacy_tkn_attr_ent_type_ (bool): _description_
            is_spacy_tkn_attr_head (bool): _description_
            is_spacy_tkn_attr_i (bool): _description_
            is_spacy_tkn_attr_idx (bool): _description_
            is_spacy_tkn_attr_is_alpha (bool): _description_
            is_spacy_tkn_attr_is_ascii (bool): _description_
            is_spacy_tkn_attr_is_bracket (bool): _description_
            is_spacy_tkn_attr_is_currency (bool): _description_
            is_spacy_tkn_attr_is_digit (bool): _description_
            is_spacy_tkn_attr_is_left_punct (bool): _description_
            is_spacy_tkn_attr_is_lower (bool): _description_
            is_spacy_tkn_attr_is_oov (bool): _description_
            is_spacy_tkn_attr_is_punct (bool): _description_
            is_spacy_tkn_attr_is_quote (bool): _description_
            is_spacy_tkn_attr_is_right_punct (bool): _description_
            is_spacy_tkn_attr_is_sent_end (bool): _description_
            is_spacy_tkn_attr_is_sent_start (bool): _description_
            is_spacy_tkn_attr_is_space (bool): _description_
            is_spacy_tkn_attr_is_stop (bool): _description_
            is_spacy_tkn_attr_is_title (bool): _description_
            is_spacy_tkn_attr_is_upper (bool): _description_
            is_spacy_tkn_attr_lang_ (bool): _description_
            is_spacy_tkn_attr_left_edge (bool): _description_
            is_spacy_tkn_attr_lemma_ (bool): _description_
            is_spacy_tkn_attr_lex (bool): _description_
            is_spacy_tkn_attr_lex_id (bool): _description_
            is_spacy_tkn_attr_like_email (bool): _description_
            is_spacy_tkn_attr_like_num (bool): _description_
            is_spacy_tkn_attr_like_url (bool): _description_
            is_spacy_tkn_attr_lower_ (bool): _description_
            is_spacy_tkn_attr_morph (bool): _description_
            is_spacy_tkn_attr_norm_ (bool): _description_
            is_spacy_tkn_attr_orth_ (bool): _description_
            is_spacy_tkn_attr_pos_ (bool): _description_
            is_spacy_tkn_attr_prefix_ (bool): _description_
            is_spacy_tkn_attr_prob (bool): _description_
            is_spacy_tkn_attr_rank (bool): _description_
            is_spacy_tkn_attr_right_edge (bool): _description_
            is_spacy_tkn_attr_sent (bool): _description_
            is_spacy_tkn_attr_sentiment (bool): _description_
            is_spacy_tkn_attr_shape_ (bool): _description_
            is_spacy_tkn_attr_suffix_ (bool): _description_
            is_spacy_tkn_attr_tag_ (bool): _description_
            is_spacy_tkn_attr_tensor (bool): _description_
            is_spacy_tkn_attr_text (bool): _description_
            is_spacy_tkn_attr_text_with_ws (bool): _description_
            is_spacy_tkn_attr_vocab (bool): _description_
            is_spacy_tkn_attr_whitespace_ (bool): _description_
            is_tokenize_2_jsonfile (bool): _description_
            json_indent (str): _description_
            pipeline_name (str):
                    Spacy pipeline name.
        """
        dcr_core.utils.check_exists_object(
            is_text_parser=True,
        )

        self._document_file_name = document_file_name
        self._document_id = document_id
        self._document_no_lines_footer = document_no_lines_footer
        self._document_no_lines_header = document_no_lines_header
        self._document_no_lines_toc = document_no_lines_toc
        self._file_encoding = file_encoding
        self._full_name = full_name
        self._is_json_sort_keys = is_json_sort_keys
        self._is_spacy_ignore_bracket = is_spacy_ignore_bracket
        self._is_spacy_ignore_left_punct = is_spacy_ignore_left_punct
        self._is_spacy_ignore_line_type_footer = is_spacy_ignore_line_type_footer
        self._is_spacy_ignore_line_type_header = is_spacy_ignore_line_type_header
        self._is_spacy_ignore_line_type_heading = is_spacy_ignore_line_type_heading
        self._is_spacy_ignore_line_type_list_bullet = is_spacy_ignore_line_type_list_bullet
        self._is_spacy_ignore_line_type_list_number = is_spacy_ignore_line_type_list_number
        self._is_spacy_ignore_line_type_table = is_spacy_ignore_line_type_table
        self._is_spacy_ignore_line_type_toc = is_spacy_ignore_line_type_toc
        self._is_spacy_ignore_punct = is_spacy_ignore_punct
        self._is_spacy_ignore_quote = is_spacy_ignore_quote
        self._is_spacy_ignore_right_punct = is_spacy_ignore_right_punct
        self._is_spacy_ignore_space = is_spacy_ignore_space
        self._is_spacy_ignore_stop = is_spacy_ignore_stop
        self._is_spacy_tkn_attr_cluster = is_spacy_tkn_attr_cluster
        self._is_spacy_tkn_attr_dep_ = is_spacy_tkn_attr_dep_
        self._is_spacy_tkn_attr_doc = is_spacy_tkn_attr_doc
        self._is_spacy_tkn_attr_ent_iob_ = is_spacy_tkn_attr_ent_iob_
        self._is_spacy_tkn_attr_ent_kb_id_ = is_spacy_tkn_attr_ent_kb_id_
        self._is_spacy_tkn_attr_ent_type_ = is_spacy_tkn_attr_ent_type_
        self._is_spacy_tkn_attr_head = is_spacy_tkn_attr_head
        self._is_spacy_tkn_attr_i = is_spacy_tkn_attr_i
        self._is_spacy_tkn_attr_idx = is_spacy_tkn_attr_idx
        self._is_spacy_tkn_attr_is_alpha = is_spacy_tkn_attr_is_alpha
        self._is_spacy_tkn_attr_is_ascii = is_spacy_tkn_attr_is_ascii
        self._is_spacy_tkn_attr_is_bracket = is_spacy_tkn_attr_is_bracket
        self._is_spacy_tkn_attr_is_currency = is_spacy_tkn_attr_is_currency
        self._is_spacy_tkn_attr_is_digit = is_spacy_tkn_attr_is_digit
        self._is_spacy_tkn_attr_is_left_punct = is_spacy_tkn_attr_is_left_punct
        self._is_spacy_tkn_attr_is_lower = is_spacy_tkn_attr_is_lower
        self._is_spacy_tkn_attr_is_oov = is_spacy_tkn_attr_is_oov
        self._is_spacy_tkn_attr_is_punct = is_spacy_tkn_attr_is_punct
        self._is_spacy_tkn_attr_is_quote = is_spacy_tkn_attr_is_quote
        self._is_spacy_tkn_attr_is_right_punct = is_spacy_tkn_attr_is_right_punct
        self._is_spacy_tkn_attr_is_sent_end = is_spacy_tkn_attr_is_sent_end
        self._is_spacy_tkn_attr_is_sent_start = is_spacy_tkn_attr_is_sent_start
        self._is_spacy_tkn_attr_is_space = is_spacy_tkn_attr_is_space
        self._is_spacy_tkn_attr_is_stop = is_spacy_tkn_attr_is_stop
        self._is_spacy_tkn_attr_is_title = is_spacy_tkn_attr_is_title
        self._is_spacy_tkn_attr_is_upper = is_spacy_tkn_attr_is_upper
        self._is_spacy_tkn_attr_lang_ = is_spacy_tkn_attr_lang_
        self._is_spacy_tkn_attr_left_edge = is_spacy_tkn_attr_left_edge
        self._is_spacy_tkn_attr_lemma_ = is_spacy_tkn_attr_lemma_
        self._is_spacy_tkn_attr_lex = is_spacy_tkn_attr_lex
        self._is_spacy_tkn_attr_lex_id = is_spacy_tkn_attr_lex_id
        self._is_spacy_tkn_attr_like_email = is_spacy_tkn_attr_like_email
        self._is_spacy_tkn_attr_like_num = is_spacy_tkn_attr_like_num
        self._is_spacy_tkn_attr_like_url = is_spacy_tkn_attr_like_url
        self._is_spacy_tkn_attr_lower_ = is_spacy_tkn_attr_lower_
        self._is_spacy_tkn_attr_morph = is_spacy_tkn_attr_morph
        self._is_spacy_tkn_attr_norm_ = is_spacy_tkn_attr_norm_
        self._is_spacy_tkn_attr_orth_ = is_spacy_tkn_attr_orth_
        self._is_spacy_tkn_attr_pos_ = is_spacy_tkn_attr_pos_
        self._is_spacy_tkn_attr_prefix_ = is_spacy_tkn_attr_prefix_
        self._is_spacy_tkn_attr_prob = is_spacy_tkn_attr_prob
        self._is_spacy_tkn_attr_rank = is_spacy_tkn_attr_rank
        self._is_spacy_tkn_attr_right_edge = is_spacy_tkn_attr_right_edge
        self._is_spacy_tkn_attr_sent = is_spacy_tkn_attr_sent
        self._is_spacy_tkn_attr_sentiment = is_spacy_tkn_attr_sentiment
        self._is_spacy_tkn_attr_shape_ = is_spacy_tkn_attr_shape_
        self._is_spacy_tkn_attr_suffix_ = is_spacy_tkn_attr_suffix_
        self._is_spacy_tkn_attr_tag_ = is_spacy_tkn_attr_tag_
        self._is_spacy_tkn_attr_tensor = is_spacy_tkn_attr_tensor
        self._is_spacy_tkn_attr_text = is_spacy_tkn_attr_text
        self._is_spacy_tkn_attr_text_with_ws = is_spacy_tkn_attr_text_with_ws
        self._is_spacy_tkn_attr_vocab = is_spacy_tkn_attr_vocab
        self._is_spacy_tkn_attr_whitespace_ = is_spacy_tkn_attr_whitespace_
        self._is_tokenize_2_jsonfile = is_tokenize_2_jsonfile
        self._json_indent = json_indent

        if pipeline_name != self._pipeline_name:
            self._nlp = spacy.load(pipeline_name)
            self._pipeline_name = pipeline_name

        self._processing_ok = False

        self._init_document()

        # {
        #   "pageNo": 99,
        #   "noParagraphsInPage": 99,
        #   "noLinesInPage": 99,
        #   "lines": [...]
        # }
        for dcr_core.cfg.glob.text_parser.parse_result_line_page in dcr_core.cfg.glob.text_parser.parse_result_line_document[
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGES
        ]:
            self._page_no = dcr_core.cfg.glob.text_parser.parse_result_line_page[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]

            self._init_page()
            self._process_page()
            self._finish_page()

        self._finish_document()

        self._processing_ok = True

    # -----------------------------------------------------------------------------
    # Check the processing result.
    # -----------------------------------------------------------------------------
    def processing_ok(self) -> bool:
        """Check the processing result.

        Returns:
            bool:   True if processing has been completed without errors.
        """
        return self._processing_ok
