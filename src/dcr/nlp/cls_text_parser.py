"""Module nlp.cls_text_parser: Extract text and metadata from PDFlib TET."""
from __future__ import annotations

import datetime
import json
from typing import Dict
from typing import Iterable
from typing import List

import cfg.glob
import nlp.cls_line_type
import utils

# pylint: disable=R0902
# pylint: disable=R0903


class TextParser:
    """Extract text and metadata from PDFlib TET.

    Returns:
        _type_: TextParser instance.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    JSON_NAME_DOCUMENT_FILE_NAME: str = "documentFileName"
    JSON_NAME_DOCUMENT_ID: str = "documentId"
    JSON_NAME_LINES: str = "lines"
    JSON_NAME_LINE_INDEX_PAGE: str = "lineIndexPage"
    JSON_NAME_LINE_TEXT: str = "lineText"
    JSON_NAME_LINE_TYPE: str = "lineType"
    JSON_NAME_NO_PAGES_IN_DOC: str = "noPagesInDoc"
    JSON_NAME_PAGES: str = "pages"
    JSON_NAME_PAGE_NO: str = "pageNo"

    _JSON_NAME_LINE_INDEX_PARA: str = "lineIndexPara"
    _JSON_NAME_NO_LINES_IN_PAGE: str = "noLinesInPage"
    _JSON_NAME_NO_PARAS_IN_PAGE: str = "noParasInPage"
    _JSON_NAME_PAGE_TEXT: str = "pageText"
    _JSON_NAME_PARA_INDEX_PAGE: str = "paraIndexPage"
    _JSON_NAME_WORDS: str = "words"
    _JSON_NAME_WORD_INDEX_LINE: str = "wordIndexLine"
    _JSON_NAME_WORD_TEXT: str = "wordText"

    _PARSE_NAME_SPACE: str = "{http://www.pdflib.com/XML/TET5/TET-5.0}"

    _PARSE_TAG_ACTION: str = "Action"
    _PARSE_TAG_ANNOTATIONS: str = "Annotations"
    _PARSE_TAG_ATTACHMENTS: str = "Attachments"
    _PARSE_TAG_AUTHOR: str = "Author"
    _PARSE_TAG_BOOKMARKS: str = "Bookmarks"
    _PARSE_TAG_BOX: str = "Box"
    _PARSE_TAG_CELL: str = "Cell"
    _PARSE_TAG_CONTENT: str = "Content"
    _PARSE_TAG_CREATION_DATE: str = "CreationDate"
    _PARSE_TAG_CREATOR: str = "Creator"
    _PARSE_TAG_CUSTOM: str = "Custom"
    _PARSE_TAG_DESTINATIONS: str = "Destinations"
    _PARSE_TAG_DOC_INFO: str = "DocInfo"
    _PARSE_TAG_ENCRYPTION: str = "Encryption"
    _PARSE_TAG_EXCEPTION: str = "Exception"
    _PARSE_TAG_FIELDS: str = "Fields"
    _PARSE_TAG_GRAPHICS: str = "Graphics"
    _PARSE_TAG_JAVA_SCRIPTS: str = "JavaScripts"
    _PARSE_TAG_LINE: str = "Line"
    _PARSE_TAG_METADATA: str = "Metadata"
    _PARSE_TAG_MOD_DATE: str = "ModDate"
    _PARSE_TAG_OPTIONS: str = "Options"
    _PARSE_TAG_OUTPUT_INTENTS: str = "OutputIntents"
    _PARSE_TAG_PAGE: str = "Page"
    _PARSE_TAG_PAGES: str = "Pages"
    _PARSE_TAG_PARA: str = "Para"
    _PARSE_TAG_PLACED_IMAGE: str = "PlacedImage"
    _PARSE_TAG_PRODUCER: str = "Producer"
    _PARSE_TAG_RESOURCES: str = "Resources"
    _PARSE_TAG_ROW: str = "Row"
    _PARSE_TAG_SIGNATURE_FIELDS: str = "SignatureFields"
    _PARSE_TAG_TABLE: str = "Table"
    _PARSE_TAG_TEXT: str = "Text"
    _PARSE_TAG_TITLE: str = "Title"
    _PARSE_TAG_WORD: str = "Word"
    _PARSE_TAG_XFA: str = "XFA"

    PARSE_TAG_CREATION: str = "Creation"
    PARSE_TAG_DOCUMENT: str = "Document"
    PARSE_TAG_FROM: int = len(_PARSE_NAME_SPACE)

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

        #   {
        #     "lineIndexPage": 0,
        #     "paraIndexPage": 0,
        #     "lineIndexPara": 0,
        #     "lineText": "Header 1",
        #     "lineType": "b"
        #   },
        self.parse_result_line_0_line: Dict[str, int | str]

        self.parse_result_line_1_lines: List[Dict[str, int | str]]

        #   {
        #     "pageNo": 1,
        #     "noLinesInPage": 5,
        #     "noParasInPage": 3,
        #     "lines": [
        #         {
        self.parse_result_line_2_page: Dict[str, int | str | List[Dict[str, int | str]]]

        self.parse_result_line_3_pages: List[Dict[str, int | str | List[Dict[str, int | str]]]]

        # {
        #   "documentId": 1,
        #   "documentFileName": "p_2_header_1_footer_1.pdf",
        #   "noPagesInDoc": 2,
        #   "pages": [
        #     {
        self.parse_result_line_4_document: Dict[str, int | str | List[Dict[str, int | str | List[Dict[str, int | str]]]]]

        self.parse_result_no_pages_in_doc: int

        self._parse_result_author: str = ""
        self._parse_result_creation_date: str = ""

        self._parse_result_line_index_page: int = 0
        self._parse_result_line_index_para: int = 0

        self._parse_result_mod_date: str = ""

        # -----------------------------------------------------------------------------
        # Internal variables.
        # -----------------------------------------------------------------------------
        self._parse_result_no_lines_in_page: int = 0
        self._parse_result_no_lines_in_para: int = 0
        # self.parse_result_no_pages_in_doc: int = 0
        self._parse_result_no_paras_in_page: int = 0
        self._parse_result_no_words_in_line: int = 0
        self._parse_result_no_words_in_page: int = 0
        self._parse_result_no_words_in_para: int = 0

        self._parse_result_page_0_paras: List[str] = []

        # {
        #     "pageNo": 1,
        #     "pageText": [
        #         "Header 1",
        #         "Seite 1 Zeile 1 This chapter uses Volto to change displaying ...",
        #         "Footer 1 pg. 1"
        #     ]
        # }
        # self._parse_result_page_1_page: Dict[str, int | str | List[str]]

        self._parse_result_page_2_pages: List[Dict[str, int | str | List[str]]] = []

        # {
        #   "documentId": 1,
        #   "documentFileName": "p_2_header_1_footer_1.pdf",
        #   "noPagesInDoc": 2,
        #   "pages": [
        #     {
        self._parse_result_page_3_document: Dict[str, int | str | List[Dict[str, int | str | List[str]]]] = {}

        self._parse_result_page_index_doc: int = 0
        self._parse_result_para_index_page: int = 0

        self._parse_result_text: str = ""

        # {"lineIndexPage": 0, "wordIndexLine": 0, "wordText": "Header"}
        # self._parse_result_word_0_word: Dict[str, int | str]

        self._parse_result_word_1_words: List[Dict[str, int | str]] = []

        # {
        #     "pageNo": 1,
        #     "words": [
        # self._parse_result_word_2_page: Dict[str, int | str | List[Dict[str, int | str]]]

        self._parse_result_word_3_pages: List[Dict[str, int | str | List[Dict[str, int | str]]]] = []

        # {
        #   "documentId": 1,
        #   "documentFileName": "p_2_header_1_footer_1.pdf",
        #   "noPagesInDoc": 2,
        #   "pages": [
        #     {
        self._parse_result_word_4_document: Dict[
            str, int | str | List[Dict[str, int | str | List[Dict[str, int | str]]]]
        ] = {}

        self._parse_result_word_index_line: int = 0
        self._parse_result_word_index_page: int = 0
        self._parse_result_word_index_para: int = 0

        self._exist = True

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Debug an XML element detailed.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _debug_xml_element_all(event: str, parent_tag: str, attrib: Dict[str, str], text: Iterable[str | None]) -> None:
        """Debug an XML element detailed.

        Args:
            event (str):
                    Event: 'start' or 'end'.
            parent_tag (str):
                    Parent tag.
            attrib (Dict[str,str]):
                    Attributes.
            text (Iterable[str|None]):
                    XML element.
        """
        if cfg.glob.setup.verbose_parser == "all":
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
        if cfg.glob.setup.verbose_parser == "text":
            print(
                f"page_i_doc={self._parse_result_page_index_doc:2d} "
                f"para_i_page={self._parse_result_para_index_page:2d} "
                f"line_i_page={self._parse_result_line_index_page:2d} "
                f"line_i_para={self._parse_result_line_index_para:2d} "
                f"text='{self._parse_result_text}'"
            )

    # -----------------------------------------------------------------------------
    # Debug an XML element only 'text' - variant page.
    # -----------------------------------------------------------------------------
    def _debug_xml_element_text_page(self) -> None:
        """Debug an XML element only 'text - variant page."""
        if cfg.glob.setup.verbose_parser == "text":
            print(
                f"page_i_doc={self._parse_result_page_index_doc:2d} "
                f"para_i_page={self._parse_result_para_index_page:2d} "
                f"line_i_page={self._parse_result_line_index_page:2d} "
                f"line_i_para={self._parse_result_line_index_para:2d} "
                f"text='{self._parse_result_text}'"
            )

    # -----------------------------------------------------------------------------
    # Debug an XML element only 'text' - variant word.
    # -----------------------------------------------------------------------------
    def _debug_xml_element_text_word(self) -> None:
        """Debug an XML element only 'text - variant word."""
        if cfg.glob.setup.verbose_parser == "text":
            print(
                f"page_i_doc={self._parse_result_page_index_doc:2d} "
                f"para_i_page={self._parse_result_para_index_page:2d} "
                f"line_i_page={self._parse_result_line_index_page:2d} "
                f"line_i_para={self._parse_result_line_index_para:2d} "
                f"word_i_page={self._parse_result_word_index_page:2d} "
                f"word_i_para={self._parse_result_word_index_para:2d} "
                f"word_i_line={self._parse_result_word_index_line:2d} "
                f"text='{self._parse_result_text}'"
            )

    # -----------------------------------------------------------------------------
    # Processing tag Box.
    # -----------------------------------------------------------------------------
    def _parse_tag_box(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Box'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case TextParser._PARSE_TAG_LINE:
                    self._parse_tag_line(child_tag, child)
                case TextParser._PARSE_TAG_TEXT:
                    self._parse_tag_text(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Cell.
    # -----------------------------------------------------------------------------
    def _parse_tag_cell(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Cell'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case TextParser._PARSE_TAG_PARA:
                    self._parse_tag_para(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag 'Content'.
    # -----------------------------------------------------------------------------
    def _parse_tag_content(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Content'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case TextParser._PARSE_TAG_PARA:
                    self._parse_tag_para(child_tag, child)
                case TextParser._PARSE_TAG_TABLE:
                    self._parse_tag_table(child_tag, child)
                # not testable
                case TextParser._PARSE_TAG_PLACED_IMAGE:
                    pass

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag 'DocInfo'.
    # -----------------------------------------------------------------------------
    def _parse_tag_doc_info(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'DocInfo'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case TextParser._PARSE_TAG_AUTHOR:
                    self._parse_result_author = child.text
                case TextParser._PARSE_TAG_CREATION_DATE:
                    self._parse_result_creation_date = child.text
                case (
                    TextParser._PARSE_TAG_CREATOR
                    | TextParser._PARSE_TAG_PRODUCER
                    | TextParser._PARSE_TAG_CUSTOM
                    | TextParser._PARSE_TAG_TITLE
                ):
                    pass
                case TextParser._PARSE_TAG_MOD_DATE:
                    self._parse_result_mod_date = datetime.datetime.strptime(child.text, "%Y-%m-%dT%H:%M:%S%z")

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Line.
    # -----------------------------------------------------------------------------
    def _parse_tag_line(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Line'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        # Initialize the parse result variables of a line.
        self._parse_result_no_words_in_line = 0
        self._parse_result_word_index_line = 0

        self._parse_result_no_lines_in_page += 1
        self._parse_result_no_lines_in_para += 1

        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case TextParser._PARSE_TAG_TEXT:
                    self._parse_tag_text(child_tag, child)
                case TextParser._PARSE_TAG_WORD:
                    self._parse_tag_word(child_tag, child)

        if cfg.glob.setup.is_parsing_line:
            self._debug_xml_element_text_line()
            self.parse_result_line_1_lines.append(
                {
                    TextParser.JSON_NAME_LINE_INDEX_PAGE: self._parse_result_line_index_page,
                    TextParser._JSON_NAME_PARA_INDEX_PAGE: self._parse_result_para_index_page,
                    TextParser._JSON_NAME_LINE_INDEX_PARA: self._parse_result_line_index_para,
                    TextParser.JSON_NAME_LINE_TEXT: self._parse_result_text,
                    TextParser.JSON_NAME_LINE_TYPE: cfg.glob.DOCUMENT_LINE_TYPE_BODY,
                }
            )

        self._parse_result_line_index_page += 1
        self._parse_result_line_index_para += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag 'Page'.
    # -----------------------------------------------------------------------------
    # noinspection PyArgumentList
    def _parse_tag_page(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Page'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        # Initialize the parse result variables of a page.
        if cfg.glob.setup.is_parsing_line:
            self.parse_result_line_1_lines = []
        elif cfg.glob.setup.is_parsing_page:
            self._parse_result_page_0_paras = []
        elif cfg.glob.setup.is_parsing_word:
            self._parse_result_word_1_words = []

        self._parse_result_line_index_page = 0
        self._parse_result_no_lines_in_page = 0
        self.parse_result_no_pages_in_doc += 1  # relative 1
        self._parse_result_no_paras_in_page = 0
        self._parse_result_no_words_in_page = 0
        self._parse_result_page_index_doc += 1  # relative 0
        self._parse_result_para_index_page = 0
        self._parse_result_word_index_page = 0

        # Process the page related tags.
        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case (
                    TextParser._PARSE_TAG_ACTION
                    | TextParser._PARSE_TAG_ANNOTATIONS
                    | TextParser._PARSE_TAG_EXCEPTION
                    | TextParser._PARSE_TAG_FIELDS
                    | TextParser._PARSE_TAG_OPTIONS
                    | TextParser._PARSE_TAG_OUTPUT_INTENTS
                ):
                    pass
                case TextParser._PARSE_TAG_CONTENT:
                    self._parse_tag_content(child_tag, child)

        # Process the page related variables.
        if cfg.glob.setup.is_parsing_line:
            cfg.glob.line_type.process_page()
            self.parse_result_line_3_pages.append(
                {
                    TextParser.JSON_NAME_PAGE_NO: self.parse_result_no_pages_in_doc,
                    TextParser._JSON_NAME_NO_LINES_IN_PAGE: self._parse_result_no_lines_in_page,
                    TextParser._JSON_NAME_NO_PARAS_IN_PAGE: self._parse_result_no_paras_in_page,
                    TextParser.JSON_NAME_LINES: self.parse_result_line_1_lines,
                }
            )
        elif cfg.glob.setup.is_parsing_page:
            self._parse_result_page_2_pages.append(
                {
                    TextParser.JSON_NAME_PAGE_NO: self.parse_result_no_pages_in_doc,
                    TextParser._JSON_NAME_PAGE_TEXT: self._parse_result_page_0_paras,
                }
            )
        elif cfg.glob.setup.is_parsing_word:
            self._parse_result_word_3_pages.append(
                {
                    TextParser.JSON_NAME_PAGE_NO: self.parse_result_no_pages_in_doc,
                    TextParser._JSON_NAME_WORDS: self._parse_result_word_1_words,
                }
            )

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag 'Pages'.
    # -----------------------------------------------------------------------------
    # noinspection PyArgumentList
    def _parse_tag_pages(self, parent_tag: str, parent: Iterable[str]) -> None:  # noqa: C901
        """Processing tag 'Pages'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        try:
            cfg.glob.action_next.exists()  # type: ignore
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'Action (action next)' does not yet exist.",
            )

        try:
            cfg.glob.document.exists()  # type: ignore
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'Document' does not yet exist.",
            )

        # Initialize the parse result variables of a document.
        if cfg.glob.setup.is_parsing_line:
            self.parse_result_line_3_pages = []
        elif cfg.glob.setup.is_parsing_page:
            self._parse_result_page_2_pages = []
        elif cfg.glob.setup.is_parsing_word:
            self._parse_result_word_3_pages = []

        self.parse_result_no_pages_in_doc = 0
        self._parse_result_page_index_doc = -1

        self._parse_result_no_words_in_line = 0
        self._parse_result_word_index_line = 0

        if cfg.glob.setup.is_parsing_line:
            cfg.glob.line_type = nlp.cls_line_type.LineType()

        # Process the tags of all document pages.
        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case TextParser._PARSE_TAG_GRAPHICS | TextParser._PARSE_TAG_RESOURCES:
                    pass
                case TextParser._PARSE_TAG_PAGE:
                    self._parse_tag_page(child_tag, child)

        if cfg.glob.setup.is_parsing_line:
            cfg.glob.line_type.process_document()
            self.parse_result_line_4_document = {
                TextParser.JSON_NAME_DOCUMENT_ID: cfg.glob.document.document_id,
                TextParser.JSON_NAME_DOCUMENT_FILE_NAME: cfg.glob.document.document_file_name,
                TextParser.JSON_NAME_NO_PAGES_IN_DOC: self.parse_result_no_pages_in_doc,
                TextParser.JSON_NAME_PAGES: self.parse_result_line_3_pages,
            }
            with open(cfg.glob.action_next.get_full_name(), "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(self.parse_result_line_4_document, file_handle)
        elif cfg.glob.setup.is_parsing_page:
            self._parse_result_page_3_document = {
                TextParser.JSON_NAME_DOCUMENT_ID: cfg.glob.document.document_id,
                TextParser.JSON_NAME_DOCUMENT_FILE_NAME: cfg.glob.document.document_file_name,
                TextParser.JSON_NAME_NO_PAGES_IN_DOC: self.parse_result_no_pages_in_doc,
                TextParser.JSON_NAME_PAGES: self._parse_result_page_2_pages,
            }
            with open(cfg.glob.action_next.get_full_name(), "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(self._parse_result_page_3_document, file_handle)
        elif cfg.glob.setup.is_parsing_word:
            self._parse_result_word_4_document = {
                TextParser.JSON_NAME_DOCUMENT_ID: cfg.glob.document.document_id,
                TextParser.JSON_NAME_DOCUMENT_FILE_NAME: cfg.glob.document.document_file_name,
                TextParser.JSON_NAME_NO_PAGES_IN_DOC: self.parse_result_no_pages_in_doc,
                TextParser.JSON_NAME_PAGES: self._parse_result_word_3_pages,
            }
            with open(cfg.glob.action_next.get_full_name(), "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(self._parse_result_word_4_document, file_handle)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Para.
    # -----------------------------------------------------------------------------
    def _parse_tag_para(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Para'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        # Initialize the parse result variables of a paragraph.
        self._parse_result_line_index_para = 0
        self._parse_result_no_lines_in_para = 0
        self._parse_result_no_words_in_para = 0
        self._parse_result_word_index_para = 0

        self._parse_result_no_paras_in_page += 1

        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case TextParser._PARSE_TAG_BOX:
                    self._parse_tag_box(child_tag, child)

        if cfg.glob.setup.is_parsing_page:
            self._debug_xml_element_text_page()
            self._parse_result_page_0_paras.append(self._parse_result_text)

        self._parse_result_para_index_page += 1

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Row.
    # -----------------------------------------------------------------------------
    def _parse_tag_row(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Row'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case TextParser._PARSE_TAG_CELL:
                    self._parse_tag_cell(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Table.
    # -----------------------------------------------------------------------------
    def _parse_tag_table(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Table'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case TextParser._PARSE_TAG_ROW:
                    self._parse_tag_row(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Text.
    # -----------------------------------------------------------------------------
    def _parse_tag_text(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Text'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        self._parse_result_text = parent.text

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    # -----------------------------------------------------------------------------
    # Processing tag Word.
    # -----------------------------------------------------------------------------
    def _parse_tag_word(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Word'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case TextParser._PARSE_TAG_BOX:
                    self._parse_tag_box(child_tag, child)
                case TextParser._PARSE_TAG_TEXT:
                    self._parse_tag_text(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

        self._parse_result_no_words_in_line += 1
        self._parse_result_no_words_in_page += 1
        self._parse_result_no_words_in_para += 1

        if cfg.glob.setup.is_parsing_word:
            self._debug_xml_element_text_word()
            self._parse_result_word_1_words.append(
                {
                    TextParser.JSON_NAME_LINE_INDEX_PAGE: self._parse_result_line_index_page,
                    TextParser._JSON_NAME_WORD_INDEX_LINE: self._parse_result_word_index_line,
                    TextParser._JSON_NAME_WORD_TEXT: self._parse_result_text,
                }
            )

        self._parse_result_word_index_line += 1
        self._parse_result_word_index_page += 1
        self._parse_result_word_index_para += 1

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
    def from_files(cls, full_name_line="", full_name_page="", full_name_word="") -> TextParser:
        """Initialise from JSON files.

        Args:
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
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        instance = cls()

        if full_name_line != "":
            with open(full_name_line, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                instance.parse_result_line_4_document = json.load(file_handle)

        if full_name_page != "":
            with open(full_name_page, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                instance._parse_result_page_3_document = json.load(file_handle)

        if full_name_word != "":
            with open(full_name_word, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                instance._parse_result_word_4_document = json.load(file_handle)

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

        return instance

    # -----------------------------------------------------------------------------
    # Processing tag 'Document'.
    # -----------------------------------------------------------------------------
    def parse_tag_document(self, parent_tag: str, parent: Iterable[str]) -> None:
        """Processing tag 'Document'.

        Args:
            parent_tag (str):
                    Parent tag.
            parent (Iterable[str):
                    Parent data structure.
        """
        self._debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

        for child in parent:
            child_tag = child.tag[TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case (
                    TextParser._PARSE_TAG_ACTION
                    | TextParser._PARSE_TAG_ATTACHMENTS
                    | TextParser._PARSE_TAG_BOOKMARKS
                    | TextParser._PARSE_TAG_DESTINATIONS
                    | TextParser._PARSE_TAG_ENCRYPTION
                    | TextParser._PARSE_TAG_EXCEPTION
                    | TextParser._PARSE_TAG_JAVA_SCRIPTS
                    | TextParser._PARSE_TAG_METADATA
                    | TextParser._PARSE_TAG_OPTIONS
                    | TextParser._PARSE_TAG_OUTPUT_INTENTS
                    | TextParser._PARSE_TAG_SIGNATURE_FIELDS
                    | TextParser._PARSE_TAG_XFA
                ):
                    pass
                case TextParser._PARSE_TAG_DOC_INFO:
                    self._parse_tag_doc_info(child_tag, child)
                case TextParser._PARSE_TAG_PAGES:
                    self._parse_tag_pages(child_tag, child)

        self._debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)
