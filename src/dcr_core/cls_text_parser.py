from __future__ import annotations

import collections.abc
import datetime
import json

import dcr_core.cls_line_type_headers_footers
import dcr_core.cls_line_type_heading
import dcr_core.cls_line_type_list_bullet
import dcr_core.cls_line_type_list_number
import dcr_core.cls_line_type_table
import dcr_core.cls_line_type_toc
import dcr_core.cls_nlp_core
import dcr_core.core_glob
import dcr_core.core_utils


# pylint: disable=too-many-instance-attributes
class TextParser:
    """Extract text and metadata from PDFlib TET.

    Returns:
        _type_: TextParser instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        dcr_core.core_utils.check_exists_object(
            is_setup=True,
        )

        self._directory_name: str = ""
        self._document_id: int = 0
        self._environment_variant: str = ""
        self._file_name_curr: str = ""
        self._file_name_orig: str = ""
        self._full_name: str = ""
        self._no_pdf_pages: int = 0

        self._parse_result_author = ""

        self._parse_result_creation_date = ""

        self._parse_result_line_document: dcr_core.cls_nlp_core.NLPCore.ParserLineDocument = {}
        self._parse_result_line_index_page = 0
        self._parse_result_line_index_para = 0
        self._parse_result_line_llx = 0.00
        self._parse_result_line_urx = 0.00

        self._parse_result_mod_date = ""

        self._parse_result_no_lines_in_doc = 0
        self._parse_result_no_lines_in_page = 0
        self._parse_result_no_lines_in_para = 0
        self._parse_result_no_paras_in_doc = 0
        self._parse_result_no_paras_in_page = 0
        self._parse_result_no_words_in_doc = 0
        self._parse_result_no_words_in_line = 0
        self._parse_result_no_words_in_page = 0
        self._parse_result_no_words_in_para = 0

        self._parse_result_page_pages: dcr_core.cls_nlp_core.NLPCore.ParserPagePages = []
        self._parse_result_page_paras: dcr_core.cls_nlp_core.NLPCore.ParserPageParas = []

        self._parse_result_table = False
        self._parse_result_table_cell = 0
        self._parse_result_table_cell_is_empty = True
        self._parse_result_table_col_span = 0
        self._parse_result_table_col_span_prev = 1
        self._parse_result_table_row = 0
        self._parse_result_text = ""

        self._parse_result_word_index_line = 0
        self._parse_result_word_index_page = 0
        self._parse_result_word_index_para = 0
        self._parse_result_word_lines: dcr_core.cls_nlp_core.NLPCore.ParserWordLines = []
        self._parse_result_word_pages: dcr_core.cls_nlp_core.NLPCore.ParserWordPages = []
        self._parse_result_word_paras: dcr_core.cls_nlp_core.NLPCore.ParserWordParas = []
        self._parse_result_word_words: dcr_core.cls_nlp_core.NLPCore.ParserWordWords = []

        self.parse_result_line_lines: dcr_core.cls_nlp_core.NLPCore.ParserLineLines = []
        self.parse_result_line_pages: dcr_core.cls_nlp_core.NLPCore.ParserLinePages = []

        self.parse_result_no_pages_in_doc = 0

        self.parse_result_titles: list[str] = []

        self._exist = True

    # -----------------------------------------------------------------------------
    # Create the data structure line: document.
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
    #     "noTablesInDocument": 99,
    #     "pages": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _create_line_document(self) -> None:
        with open(self._full_name, "w", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(
                {
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: self._document_id,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: self._file_name_orig,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_FOOTER: dcr_core.core_glob.line_type_headers_footers.no_lines_footer,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_HEADER: dcr_core.core_glob.line_type_headers_footers.no_lines_header,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_DOC: self._parse_result_no_lines_in_doc,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_TOC: dcr_core.core_glob.line_type_toc.no_lines_toc,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET_IN_DOC: dcr_core.core_glob.line_type_list_bullet.no_lists,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER_IN_DOC: dcr_core.core_glob.line_type_list_number.no_lists,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_PAGES_IN_DOC: self.parse_result_no_pages_in_doc,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_DOC: self._parse_result_no_paras_in_doc,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_TABLES_IN_DOC: dcr_core.core_glob.line_type_table.no_tables,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_TITLES_IN_DOC: len(self.parse_result_titles),
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TITLES: self.parse_result_titles,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGES: self.parse_result_line_pages,
                },
                file_handle,
                indent=dcr_core.core_glob.setup.json_indent,
                sort_keys=dcr_core.core_glob.setup.is_json_sort_keys,
            )

    # -----------------------------------------------------------------------------
    # Create the data structure line: lines.
    # -----------------------------------------------------------------------------
    # {
    #     "coordLLX": 99.9,
    #     "coordURX": 99.9,
    #     "lineNo": 99,
    #     "lineNoPage": 99,
    #     "lineType": "xxx",
    #     "paragraphNo": 99,
    #     "text": "xxx"
    # }
    # -----------------------------------------------------------------------------
    def _create_line_lines(self) -> None:
        self._debug_xml_element_text_line()

        new_entry = {
            dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX: self._parse_result_line_llx,
            dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX: self._parse_result_line_urx,
            dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO: self._parse_result_no_lines_in_para,
            dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE: self._parse_result_line_index_page + 1,
            dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_BODY,
            dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: self._parse_result_no_paras_in_page,
            dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._parse_result_text,
        }

        if self._parse_result_table:
            new_entry[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO] = self._parse_result_table_cell
            new_entry[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO] = self._parse_result_table_row
            if self._parse_result_table_col_span:
                new_entry[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN] = int(self._parse_result_table_col_span)

        self.parse_result_line_lines.append(new_entry)

    # -----------------------------------------------------------------------------
    # Create the data structure line: pages.
    # -----------------------------------------------------------------------------
    # {
    #     "pageNo": 99,
    #     "noLinesInPage": 99,
    #     "noParagraphsInPage": 99,
    #     "lines": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _create_line_pages(self) -> None:
        self.parse_result_line_pages.append(
            {
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: self.parse_result_no_pages_in_doc,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PAGE: self._parse_result_no_lines_in_page,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_PAGE: self._parse_result_no_paras_in_page,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES: self.parse_result_line_lines,
            }
        )

    # -----------------------------------------------------------------------------
    # Create the data structure page: document.
    # -----------------------------------------------------------------------------
    # {
    #     "documentId": 99,
    #     "documentFileName": "xxx",
    #     "noPagesInDocument": 99,
    #     "noParagraphsInDocument": 99,
    #     "pages": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _create_page_document(self) -> None:
        with open(self._full_name, "w", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(
                {
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: self._document_id,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: self._file_name_orig,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_PAGES_IN_DOC: self.parse_result_no_pages_in_doc,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_DOC: self._parse_result_no_paras_in_doc,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGES: self._parse_result_page_pages,
                },
                file_handle,
                indent=dcr_core.core_glob.setup.json_indent,
                sort_keys=dcr_core.core_glob.setup.is_json_sort_keys,
            )

    # -----------------------------------------------------------------------------
    # Create the data structure page: pages.
    # -----------------------------------------------------------------------------
    # {
    #     "pageNo": 99,
    #     "noParagraphsInPage": 99,
    #     "paragraphs": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _create_page_pages(self) -> None:
        self._parse_result_page_pages.append(
            {
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: self.parse_result_no_pages_in_doc,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_PAGE: self._parse_result_no_paras_in_page,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARAS: self._parse_result_page_paras,
            }
        )

    # -----------------------------------------------------------------------------
    # Create the data structure page: paras.
    # -----------------------------------------------------------------------------
    # {
    #     "paragraphNo": 99,
    #     "text": "xxx"
    # }
    # -----------------------------------------------------------------------------
    def _create_page_paras(self) -> None:
        self._debug_xml_element_text_page()

        self._parse_result_page_paras.append(
            {
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: self._parse_result_no_paras_in_page,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._parse_result_text,
            }
        )

    # -----------------------------------------------------------------------------
    # Create the data structure word: document.
    # -----------------------------------------------------------------------------
    # {
    #     "documentId": 99,
    #     "documentFileName": "xxx",
    #     "noLinesInDocument": 99,
    #     "noPagesInDocument": 99,
    #     "noParagraphsInDocument": 99,
    #     "noWordsInDocument": 99,
    #     "pages": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _create_word_document(self) -> None:
        with open(self._full_name, "w", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(
                {
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: self._document_id,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: self._file_name_orig,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_DOC: self._parse_result_no_lines_in_doc,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_PAGES_IN_DOC: self.parse_result_no_pages_in_doc,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_DOC: self._parse_result_no_paras_in_doc,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_WORDS_IN_DOC: self._parse_result_no_words_in_doc,
                    dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGES: self._parse_result_word_pages,
                },
                file_handle,
                indent=dcr_core.core_glob.setup.json_indent,
                sort_keys=dcr_core.core_glob.setup.is_json_sort_keys,
            )

    # -----------------------------------------------------------------------------
    # Create the data structure word: lines.
    # -----------------------------------------------------------------------------
    # {
    #     "lineNo": 99,
    #     "noWordsInLine": 99,
    #     "words": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _create_word_lines(self) -> None:
        self._parse_result_word_lines.append(
            {
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO: self._parse_result_no_lines_in_para,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_WORDS_IN_LINE: self._parse_result_no_words_in_line,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_WORDS: self._parse_result_word_words,
            }
        )

    # -----------------------------------------------------------------------------
    # Create the data structure word: pages.
    # -----------------------------------------------------------------------------
    # {
    #     "pageNo": 99,
    #     "noLinesInPage": 99,
    #     "noParagraphsInPage": 99,
    #     "noWordsInPage": 99,
    #     "paragraphs": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _create_word_pages(self) -> None:
        self._parse_result_word_pages.append(
            {
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: self.parse_result_no_pages_in_doc,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PAGE: self._parse_result_no_lines_in_page,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_PARAS_IN_PAGE: self._parse_result_no_paras_in_page,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_WORDS_IN_PAGE: self._parse_result_no_words_in_page,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARAS: self._parse_result_word_paras,
            }
        )

    # -----------------------------------------------------------------------------
    # Create the data structure word: paras.
    # -----------------------------------------------------------------------------
    # {
    #     "paragraphNo": 99,
    #     "noLinesInParagraph": 99,
    #     "noWordsInParagraph": 99,
    #     "lines": [
    #     ]
    # }
    # -----------------------------------------------------------------------------
    def _create_word_paras(self) -> None:
        self._parse_result_word_paras.append(
            {
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: self._parse_result_no_paras_in_page,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LINES_IN_PARA: self._parse_result_no_lines_in_para,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_WORDS_IN_PARA: self._parse_result_no_words_in_para,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES: self._parse_result_word_lines,
            }
        )

    # -----------------------------------------------------------------------------
    # Create the data structure word: words.
    # -----------------------------------------------------------------------------
    # {
    #     "wordNo": 99,
    #     "text": "xxx"
    # }
    # -----------------------------------------------------------------------------
    def _create_word_words(self) -> None:
        self._debug_xml_element_text_word()

        self._parse_result_word_words.append(
            {
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_WORD_NO: self._parse_result_no_words_in_line,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT: self._parse_result_text,
            }
        )

    # -----------------------------------------------------------------------------
    # Debug an XML element detailed.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _debug_xml_element_all(event: str, parent_tag: str, attrib: dict[str, str], text: collections.abc.Iterable[str | None]) -> None:
        """Debug an XML element detailed.

        Args:
            event (str):
                    Event: 'start' or 'end'.
            parent_tag (str):
                    Parent tag.
            attrib (dict[str,str]):
                    Attributes.
            text (collections.abc.Iterable[str|None]):
                    XML element.
        """
        if dcr_core.core_glob.setup.verbose_parser == "all":
            print(f"{event} tag   ={parent_tag}")

            if attrib != {}:
                print(f"      attrib={attrib}")

            if text is not None and str(text).strip() > "":
                print(f"      text  ='{text}'")

    # -----------------------------------------------------------------------------
    # Debug an XML element only 'text' - variant line.
    # -----------------------------------------------------------------------------
    def _debug_xml_element_text_line(self) -> None:
        """Debug an XML element only 'text - variant line."""
        if dcr_core.core_glob.setup.verbose_parser == "text":
            print(
                f"pages_i_doc={self.parse_result_no_pages_in_doc:2d} "
                f"paras_i_page={self._parse_result_no_paras_in_page:2d} "
                f"lines_i_page={self._parse_result_no_lines_in_page:2d} "
                f"lines_i_para={self._parse_result_no_lines_in_para:2d} "
                f"text='{self._parse_result_text}'"
            )

    # -----------------------------------------------------------------------------
    # Debug an XML element only 'text' - variant page.
    # -----------------------------------------------------------------------------
    def _debug_xml_element_text_page(self) -> None:
        """Debug an XML element only 'text - variant page."""
        if dcr_core.core_glob.setup.verbose_parser == "text":
            print(
                f"pages_i_doc={self.parse_result_no_pages_in_doc:2d} "
                f"paras_i_page={self._parse_result_no_paras_in_page:2d} "
                f"lines_i_page={self._parse_result_no_lines_in_page:2d} "
                f"lines_i_para={self._parse_result_no_lines_in_para:2d} "
                f"text='{self._parse_result_text}'"
            )

    # -----------------------------------------------------------------------------
    # Debug an XML element only 'text' - variant word.
    # -----------------------------------------------------------------------------
    def _debug_xml_element_text_word(self) -> None:
        """Debug an XML element only 'text - variant word."""
        if dcr_core.core_glob.setup.verbose_parser == "text":
            print(
                f"pages_i_doc={self.parse_result_no_pages_in_doc:2d} "
                f"paras_i_page={self._parse_result_no_paras_in_page:2d} "
                f"lines_i_page={self._parse_result_no_lines_in_page:2d} "
                f"lines_i_para={self._parse_result_no_lines_in_para:2d} "
                f"words_i_page={self._parse_result_no_words_in_page:2d} "
                f"words_i_para={self._parse_result_no_words_in_para:2d} "
                f"words_i_line={self._parse_result_no_words_in_line:2d} "
                f"text='{self._parse_result_text}'"
            )

    # -----------------------------------------------------------------------------
    # Processing tag Bookmark.
    # -----------------------------------------------------------------------------
    def _parse_tag_bookmark(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Bookmark'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_ACTION:
                    pass
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_BOOKMARK:
                    self._parse_tag_bookmark(child_tag, child)
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_TITLE:
                    self._parse_tag_title(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Bookmarks.
    # -----------------------------------------------------------------------------
    def _parse_tag_bookmarks(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Bookmarks'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_BOOKMARK:
                    self._parse_tag_bookmark(child_tag, child)
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Box.
    # -----------------------------------------------------------------------------
    def _parse_tag_box(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Box'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_LINE:
                    self._parse_tag_line(child_tag, child)
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Cell.
    # -----------------------------------------------------------------------------
    def _parse_tag_cell(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Cell'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_table_cell_is_empty = True

        self._parse_result_table_cell += self._parse_result_table_col_span_prev

        self._parse_result_table_col_span = parent.attrib.get(dcr_core.cls_nlp_core.NLPCore.PARSE_ATTR_COL_SPAN)

        if self._parse_result_table_col_span:
            self._parse_result_table_col_span_prev = int(self._parse_result_table_col_span)
        else:
            self._parse_result_table_col_span_prev = 1

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_PARA:
                    self._parse_result_table_cell_is_empty = False
                    self._parse_tag_para(child_tag, child)

        if self._parse_result_table_cell_is_empty:
            self._parse_result_line_llx = float(parent.attrib.get(dcr_core.cls_nlp_core.NLPCore.PARSE_ATTR_LLX))
            self._parse_result_line_urx = float(parent.attrib.get(dcr_core.cls_nlp_core.NLPCore.PARSE_ATTR_URX))
            new_entry = {
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO: self._parse_result_table_cell,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX: self._parse_result_line_llx,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX: self._parse_result_line_urx,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO: self._parse_result_no_lines_in_para,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE: self._parse_result_line_index_page + 1,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE: dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_BODY,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: self._parse_result_no_paras_in_page,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO: self._parse_result_table_row,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT: "",
            }

            if self._parse_result_table_col_span:
                # not testable
                new_entry[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN] = int(self._parse_result_table_col_span)

            self.parse_result_line_lines.append(new_entry)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag 'Content'.
    # -----------------------------------------------------------------------------
    def _parse_tag_content(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Content'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_PARA:
                    self._parse_tag_para(child_tag, child)
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_TABLE:
                    self._parse_tag_table(child_tag, child)
                # not testable
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_PLACED_IMAGE:
                    pass

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag 'DocInfo'.
    # -----------------------------------------------------------------------------
    def _parse_tag_doc_info(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'DocInfo'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_AUTHOR:
                    self._parse_result_author = child.text
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_CREATION_DATE:
                    self._parse_result_creation_date = child.text
                case (
                    dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_CREATOR
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_PRODUCER
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_CUSTOM
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_TITLE
                ):
                    pass
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_MOD_DATE:
                    self._parse_result_mod_date = datetime.datetime.strptime(child.text, "%Y-%m-%dT%H:%M:%S%z")

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Line.
    # -----------------------------------------------------------------------------
    def _parse_tag_line(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Line'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_line_llx = float(parent.attrib.get(dcr_core.cls_nlp_core.NLPCore.PARSE_ATTR_LLX))
        self._parse_result_line_urx = float(parent.attrib.get(dcr_core.cls_nlp_core.NLPCore.PARSE_ATTR_URX))

        self._parse_result_no_lines_in_para += 1
        self._parse_result_no_words_in_line = 0

        if dcr_core.core_glob.setup.is_parsing_word:
            self._parse_result_word_words = []

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_WORD:
                    self._parse_tag_word(child_tag, child)

        if dcr_core.core_glob.setup.is_parsing_line:
            self._create_line_lines()
            self._parse_result_line_index_page += 1
            self._parse_result_line_index_para += 1
        elif dcr_core.core_glob.setup.is_parsing_word:
            self._create_word_lines()

        self._parse_result_no_words_in_para += self._parse_result_no_words_in_line

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag 'Page'.
    # -----------------------------------------------------------------------------
    # noinspection PyArgumentList
    def _parse_tag_page(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Page'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self.parse_result_no_pages_in_doc += 1

        self._parse_result_no_paras_in_page = 0
        self._parse_result_no_lines_in_page = 0
        self._parse_result_no_words_in_page = 0

        if dcr_core.core_glob.setup.is_parsing_line:
            self._parse_result_line_index_page = 0
            self.parse_result_line_lines = []
        elif dcr_core.core_glob.setup.is_parsing_page:
            self._parse_result_page_paras = []
        elif dcr_core.core_glob.setup.is_parsing_word:
            self._parse_result_word_paras = []

        # Process the page related tags.
        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case (
                    dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_ACTION
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_ANNOTATIONS
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_EXCEPTION
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FIELDS
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_OPTIONS
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_OUTPUT_INTENTS
                ):
                    pass
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_CONTENT:
                    self._parse_tag_content(child_tag, child)

        if dcr_core.core_glob.setup.is_parsing_line:
            self._create_line_pages()
        elif dcr_core.core_glob.setup.is_parsing_page:
            self._create_page_pages()
        elif dcr_core.core_glob.setup.is_parsing_word:
            self._create_word_pages()

        self._parse_result_no_words_in_doc += self._parse_result_no_words_in_page
        self._parse_result_no_lines_in_doc += self._parse_result_no_lines_in_page
        self._parse_result_no_paras_in_doc += self._parse_result_no_paras_in_page

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag 'Pages'.
    # -----------------------------------------------------------------------------
    # noinspection PyArgumentList
    def _parse_tag_pages(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:  # noqa: C901
        """Processing tag 'Pages'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_no_paras_in_doc = 0
        self.parse_result_no_pages_in_doc = 0

        if dcr_core.core_glob.setup.is_parsing_line:
            self._parse_result_no_lines_in_doc = 0
            self.parse_result_line_pages = []
            dcr_core.core_glob.line_type_headers_footers = dcr_core.cls_line_type_headers_footers.LineTypeHeaderFooters(
                file_name_curr=self._file_name_curr,
            )
            dcr_core.core_glob.line_type_toc = dcr_core.cls_line_type_toc.LineTypeToc(
                file_name_curr=self._file_name_curr,
            )
            dcr_core.core_glob.line_type_table = dcr_core.cls_line_type_table.LineTypeTable(
                file_name_curr=self._file_name_curr,
            )
            dcr_core.core_glob.line_type_list_bullet = dcr_core.cls_line_type_list_bullet.LineTypeListBullet(
                file_name_curr=self._file_name_curr,
            )
            dcr_core.core_glob.line_type_list_number = dcr_core.cls_line_type_list_number.LineTypeListNumber(
                file_name_curr=self._file_name_curr,
            )
            dcr_core.core_glob.line_type_heading = dcr_core.cls_line_type_heading.LineTypeHeading(
                file_name_curr=self._file_name_curr,
            )
        elif dcr_core.core_glob.setup.is_parsing_page:
            self._parse_result_page_pages = []
        elif dcr_core.core_glob.setup.is_parsing_word:
            self._parse_result_no_words_in_doc = 0
            self._parse_result_no_lines_in_doc = 0
            self._parse_result_word_pages = []

        # Process the tags of all document pages.
        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_GRAPHICS | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_RESOURCES:
                    pass
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_PAGE:
                    self._parse_tag_page(child_tag, child)

        if dcr_core.core_glob.setup.is_parsing_line:
            dcr_core.core_glob.line_type_headers_footers.process_document(
                file_name_curr=self._file_name_curr,
                no_pdf_pages=self._no_pdf_pages,
                parser_line_pages_json=self.parse_result_line_pages,
            )
            dcr_core.core_glob.line_type_toc.process_document(
                file_name_curr=self._file_name_curr,
                parser_line_pages_json=self.parse_result_line_pages,
            )
            dcr_core.core_glob.line_type_table.process_document(
                file_name_curr=self._file_name_curr,
                directory_name=self._directory_name,
                document_id=self._document_id,
                file_name_orig=self._file_name_orig,
                parser_line_pages_json=self.parse_result_line_pages,
            )
            dcr_core.core_glob.line_type_list_bullet.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                environment_variant=self._environment_variant,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
                parser_line_pages_json=self.parse_result_line_pages,
            )
            dcr_core.core_glob.line_type_list_number.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                environment_variant=self._environment_variant,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
                parser_line_pages_json=self.parse_result_line_pages,
            )
            dcr_core.core_glob.line_type_heading.process_document(
                directory_name=self._directory_name,
                document_id=self._document_id,
                file_name_curr=self._file_name_curr,
                file_name_orig=self._file_name_orig,
                parser_line_pages_json=self.parse_result_line_pages,
            )
            self._create_line_document()
        elif dcr_core.core_glob.setup.is_parsing_page:
            self._create_page_document()
        elif dcr_core.core_glob.setup.is_parsing_word:
            self._create_word_document()

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Para.
    # -----------------------------------------------------------------------------
    def _parse_tag_para(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Para'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_no_paras_in_page += 1

        self._parse_result_no_lines_in_para = 0
        self._parse_result_no_words_in_para = 0

        if dcr_core.core_glob.setup.is_parsing_line:
            self._parse_result_line_index_para = 0
        elif dcr_core.core_glob.setup.is_parsing_word:
            self._parse_result_word_lines = []

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_BOX:
                    self._parse_tag_box(child_tag, child)

        if dcr_core.core_glob.setup.is_parsing_page:
            self._create_page_paras()
        elif dcr_core.core_glob.setup.is_parsing_word:
            self._create_word_paras()

        self._parse_result_no_lines_in_page += self._parse_result_no_lines_in_para
        self._parse_result_no_words_in_page += self._parse_result_no_words_in_para

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Row.
    # -----------------------------------------------------------------------------
    def _parse_tag_row(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Row'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_table_row += 1
        self._parse_result_table_cell = 0
        self._parse_result_table_col_span_prev = 1

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_CELL:
                    self._parse_tag_cell(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Table.
    # -----------------------------------------------------------------------------
    def _parse_tag_table(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Table'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_table = True
        self._parse_result_table_row = 0

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_ROW:
                    self._parse_tag_row(child_tag, child)

        self._parse_result_table = False

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Text.
    # -----------------------------------------------------------------------------
    def _parse_tag_text(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Text'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_text = parent.text

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Title.
    # -----------------------------------------------------------------------------
    def _parse_tag_title(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Title'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self.parse_result_titles.append(parent.text)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Word.
    # -----------------------------------------------------------------------------
    def _parse_tag_word(self, parent_tag: str, parent: collections.abc.Iterable[str]) -> None:
        """Processing tag 'Word'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_no_words_in_line += 1

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_BOX:
                    self._parse_tag_box(child_tag, child)
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_TEXT:
                    self._parse_tag_text(child_tag, child)

        self._create_word_words()

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

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
    # Initialise from the JSON files.
    # -----------------------------------------------------------------------------
    @classmethod
    def from_files(cls, file_encoding: str, full_name_line: str = "", full_name_page: str = "", full_name_word: str = "") -> TextParser:
        """Initialise from JSON files.

        Args:
            file_encoding (str):
                    The encoding of the output file.
            full_name_line (str):
                    Name of the file with the line-related JSON data.
            full_name_page (str):
                    Name of the file with the page-related JSON data.
            full_name_word (str):
                    Name of the file with the word-related JSON data.

        Returns:
            TextParser:
                    The object instance matching the specified database row.
        """
        instance = cls()

        if full_name_line != "":
            with open(full_name_line, "r", encoding=file_encoding) as file_handle:
                instance.parse_result_line_document = json.load(file_handle)

        if full_name_page != "":
            with open(full_name_page, "r", encoding=file_encoding) as file_handle:
                instance._parse_result_page_document = json.load(file_handle)

        if full_name_word != "":
            with open(full_name_word, "r", encoding=file_encoding) as file_handle:
                instance._parse_result_word_document = json.load(file_handle)

        return instance

    # -----------------------------------------------------------------------------
    # Processing tag 'Document'.
    # -----------------------------------------------------------------------------
    def parse_tag_document(
        self,
        directory_name: str,
        document_id: int,
        environment_variant: str,
        file_name_curr: str,
        file_name_next: str,
        file_name_orig: str,
        no_pdf_pages: int,
        parent: collections.abc.Iterable[str],
        parent_tag: str,
    ) -> None:
        """Processing tag 'Document'.

        Args:
            directory_name (str):
                    Directory name of the output file.
            document_id (int):
                    Identification of the document.
            environment_variant (str):
                    Environment variant: dev, prod or test.
            file_name_curr (str):
                    File name of the current file.
            file_name_next (str):
                    File name of the output file.
            file_name_orig (in):
                    File name of the document file.
            no_pdf_pages (int):
                    Number ODF pages.
            parent (collections.abc.Iterable[str]):
                    Parent data structure.
            parent_tag (str):
                    Parent tag.
        """
        dcr_core.core_utils.check_exists_object(
            is_setup=True,
        )

        self._directory_name = directory_name
        self._document_id = document_id
        self._environment_variant = environment_variant
        self._file_name_curr = file_name_curr
        self._file_name_orig = file_name_orig
        self._full_name = file_name_next
        self._no_pdf_pages = no_pdf_pages

        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case (
                    dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_ACTION
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_ATTACHMENTS
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_DESTINATIONS
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_ENCRYPTION
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_EXCEPTION
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_JAVA_SCRIPTS
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_METADATA
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_OPTIONS
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_OUTPUT_INTENTS
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_SIGNATURE_FIELDS
                    | dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_XFA
                ):
                    pass
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_BOOKMARKS:
                    self._parse_tag_bookmarks(child_tag, child)
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_DOCUMENT_INFO:
                    self._parse_tag_doc_info(child_tag, child)
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_PAGES:
                    self._parse_tag_pages(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)
