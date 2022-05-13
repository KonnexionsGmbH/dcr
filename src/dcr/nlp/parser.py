"""Module nlp.parser: Store the document structure from the parser result."""
import datetime
import json
import os
import pathlib
import time
from typing import Dict
from typing import Iterable

import cfg.glob
import db.cls_action
import db.cls_base
import db.cls_run
import db.dml
import defusedxml.ElementTree
import nlp.cls_line_type
import utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
TETML_TYPE_LINE: str = "line"
TETML_TYPE_WORD: str = "word"


# -----------------------------------------------------------------------------
# Debug an XML element detailed.
# -----------------------------------------------------------------------------
def debug_xml_element_all(event: str, parent_tag: str, attrib: Dict[str, str], text: Iterable[str | None]) -> None:
    """Debug an XML element detailed.

    Args:
        event (str): Event: 'start' or 'end'.
        parent_tag (str): Parent tag.
        attrib (Dict[str,str]): Attributes.
        text (Iterable[str|None]): XML element.
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
def debug_xml_element_text_line() -> None:
    """Debug an XML element only 'text - variant line."""
    if cfg.glob.setup.verbose_parser == "text":
        print(
            f"page_i_doc={cfg.glob.parse_result_page_index_doc:2d} "
            f"para_i_page={cfg.glob.parse_result_para_index_page:2d} "
            f"line_i_page={cfg.glob.parse_result_line_index_page:2d} "
            f"line_i_para={cfg.glob.parse_result_line_index_para:2d} "
            f"text='{cfg.glob.parse_result_text}'"
        )


# -----------------------------------------------------------------------------
# Debug an XML element only 'text' - variant word.
# -----------------------------------------------------------------------------
def debug_xml_element_text_word() -> None:
    """Debug an XML element only 'text - variant word."""
    if cfg.glob.setup.verbose_parser == "text":
        print(
            f"page_i_doc={cfg.glob.parse_result_page_index_doc:2d} "
            f"para_i_page={cfg.glob.parse_result_para_index_page:2d} "
            f"line_i_page={cfg.glob.parse_result_line_index_page:2d} "
            f"line_i_para={cfg.glob.parse_result_line_index_para:2d} "
            f"word_i_page={cfg.glob.parse_result_word_index_page:2d} "
            f"word_i_para={cfg.glob.parse_result_word_index_para:2d} "
            f"word_i_line={cfg.glob.parse_result_word_index_line:2d} "
            f"text='{cfg.glob.parse_result_text}'"
        )


# -----------------------------------------------------------------------------
# Processing tag Box.
# -----------------------------------------------------------------------------
def parse_tag_box(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Box'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_LINE:
                parse_tag_line(child_tag, child)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag Cell.
# -----------------------------------------------------------------------------
def parse_tag_cell(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Cell'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_PARA:
                parse_tag_para(child_tag, child)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'Content'.
# -----------------------------------------------------------------------------
def parse_tag_content(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Content'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_PARA:
                parse_tag_para(child_tag, child)
            case cfg.glob.PARSE_TAG_TABLE:
                parse_tag_table(child_tag, child)
            # not testable
            case cfg.glob.PARSE_TAG_PLACED_IMAGE:
                pass

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'DocInfo'.
# -----------------------------------------------------------------------------
def parse_tag_doc_info(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'DocInfo'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_AUTHOR:
                cfg.glob.parse_result_author = child.text
            case cfg.glob.PARSE_TAG_CREATION_DATE:
                cfg.glob.parse_result_creation_date = child.text
            case (
                cfg.glob.PARSE_TAG_CREATOR
                | cfg.glob.PARSE_TAG_PRODUCER
                | cfg.glob.PARSE_TAG_CUSTOM
                | cfg.glob.PARSE_TAG_TITLE
            ):
                pass
            case cfg.glob.PARSE_TAG_MOD_DATE:
                cfg.glob.parse_result_mod_date = datetime.datetime.strptime(child.text, "%Y-%m-%dT%H:%M:%S%z")

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'Document'.
# -----------------------------------------------------------------------------
def parse_tag_document(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Document'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case (
                cfg.glob.PARSE_TAG_ACTION
                | cfg.glob.PARSE_TAG_ATTACHMENTS
                | cfg.glob.PARSE_TAG_BOOKMARKS
                | cfg.glob.PARSE_TAG_DESTINATIONS
                | cfg.glob.PARSE_TAG_ENCRYPTION
                | cfg.glob.PARSE_TAG_EXCEPTION
                | cfg.glob.PARSE_TAG_JAVA_SCRIPTS
                | cfg.glob.PARSE_TAG_METADATA
                | cfg.glob.PARSE_TAG_OPTIONS
                | cfg.glob.PARSE_TAG_OUTPUT_INTENTS
                | cfg.glob.PARSE_TAG_SIGNATURE_FIELDS
                | cfg.glob.PARSE_TAG_XFA
            ):
                pass
            case cfg.glob.PARSE_TAG_DOC_INFO:
                parse_tag_doc_info(child_tag, child)
            case cfg.glob.PARSE_TAG_PAGES:
                parse_tag_pages(child_tag, child)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag Line.
# -----------------------------------------------------------------------------
def parse_tag_line(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Line'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    # Initialize the parse result variables of a line.
    cfg.glob.parse_result_no_words_in_line = 0
    cfg.glob.parse_result_word_index_line = 0

    cfg.glob.parse_result_no_lines_in_page += 1
    cfg.glob.parse_result_no_lines_in_para += 1

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_TEXT:
                parse_tag_text(child_tag, child)
            case cfg.glob.PARSE_TAG_WORD:
                parse_tag_word(child_tag, child)

    debug_xml_element_text_line()

    if cfg.glob.setup.is_parsing_line:
        cfg.glob.parse_result_line_1_lines.append(
            {
                cfg.glob.JSON_NAME_LINE_INDEX_PAGE: cfg.glob.parse_result_line_index_page,
                cfg.glob.JSON_NAME_PARA_INDEX_PAGE: cfg.glob.parse_result_para_index_page,
                cfg.glob.JSON_NAME_LINE_INDEX_PARA: cfg.glob.parse_result_line_index_para,
                cfg.glob.JSON_NAME_LINE_TEXT: cfg.glob.parse_result_text,
                cfg.glob.JSON_NAME_LINE_TYPE: cfg.glob.DOCUMENT_LINE_TYPE_BODY,
            }
        )

    cfg.glob.parse_result_line_index_page += 1
    cfg.glob.parse_result_line_index_para += 1

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'Page'.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def parse_tag_page(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Page'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    # Initialize the parse result variables of a page.
    if cfg.glob.setup.is_parsing_line:
        cfg.glob.parse_result_line_1_lines = []
    elif cfg.glob.setup.is_parsing_word:
        cfg.glob.parse_result_word_1_words = []

    cfg.glob.parse_result_line_index_page = 0
    cfg.glob.parse_result_no_lines_in_page = 0
    cfg.glob.parse_result_no_pages_in_doc += 1  # relative 1
    cfg.glob.parse_result_no_paras_in_page = 0
    cfg.glob.parse_result_no_words_in_page = 0
    cfg.glob.parse_result_page_index_doc += 1  # relative 0
    cfg.glob.parse_result_para_index_page = 0
    cfg.glob.parse_result_word_index_page = 0

    if cfg.glob.setup.line_footer_max_lines > 0 or cfg.glob.setup.line_header_max_lines > 0:
        utils.progress_msg_line_type(
            f"LineType: Start page                         ={cfg.glob.parse_result_no_pages_in_doc}"
        )

    # Process the page related tags.
    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case (
                cfg.glob.PARSE_TAG_ACTION
                | cfg.glob.PARSE_TAG_ANNOTATIONS
                | cfg.glob.PARSE_TAG_EXCEPTION
                | cfg.glob.PARSE_TAG_FIELDS
                | cfg.glob.PARSE_TAG_OPTIONS
                | cfg.glob.PARSE_TAG_OUTPUT_INTENTS
            ):
                pass
            case cfg.glob.PARSE_TAG_CONTENT:
                parse_tag_content(child_tag, child)

    # Process the page related variables.
    if cfg.glob.setup.is_parsing_line:
        if cfg.glob.setup.line_footer_max_lines > 0 or cfg.glob.setup.line_header_max_lines > 0:
            cfg.glob.line_type.process_page(
                page_no=cfg.glob.parse_result_no_pages_in_doc, line_lines=cfg.glob.parse_result_line_1_lines
            )
        cfg.glob.parse_result_line_3_pages.append(
            {
                cfg.glob.JSON_NAME_PAGE_NO: cfg.glob.parse_result_no_pages_in_doc,
                cfg.glob.JSON_NAME_NO_LINES_IN_PAGE: cfg.glob.parse_result_no_lines_in_page,
                cfg.glob.JSON_NAME_NO_PARAS_IN_PAGE: cfg.glob.parse_result_no_paras_in_page,
                cfg.glob.JSON_NAME_LINES: cfg.glob.parse_result_line_1_lines,
            }
        )
    elif cfg.glob.setup.is_parsing_word:
        cfg.glob.parse_result_word_3_pages.append(
            {
                cfg.glob.JSON_NAME_PAGE_NO: cfg.glob.parse_result_no_pages_in_doc,
                cfg.glob.JSON_NAME_LINES: cfg.glob.parse_result_word_1_words,
            }
        )

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'Pages'.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def parse_tag_pages(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Pages'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    # Initialize the parse result variables of a document.
    if cfg.glob.setup.is_parsing_line:
        cfg.glob.parse_result_line_3_pages = []
    elif cfg.glob.setup.is_parsing_word:
        cfg.glob.parse_result_word_3_pages = []

    cfg.glob.parse_result_no_pages_in_doc = 0
    cfg.glob.parse_result_page_index_doc = -1

    cfg.glob.parse_result_no_words_in_line = 0
    cfg.glob.parse_result_word_index_line = 0

    if cfg.glob.setup.line_footer_max_lines > 0 or cfg.glob.setup.line_header_max_lines > 0:
        if cfg.glob.setup.is_parsing_line:
            cfg.glob.line_type = nlp.cls_line_type.LineType()

        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type(
            f"LineType: Start document                     ={cfg.glob.action_curr.action_file_name}"
        )

    # Process the tags of all document pages.
    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_GRAPHICS | cfg.glob.PARSE_TAG_RESOURCES:
                pass
            case cfg.glob.PARSE_TAG_PAGE:
                parse_tag_page(child_tag, child)

    if cfg.glob.setup.line_footer_max_lines > 0 or cfg.glob.setup.line_header_max_lines > 0:
        # Process the document related variables.
        utils.progress_msg_line_type(
            f"LineType: End document                       ={cfg.glob.action_curr.action_file_name}"
        )

    if cfg.glob.setup.is_parsing_line:
        if cfg.glob.setup.line_footer_max_lines > 0 or cfg.glob.setup.line_header_max_lines > 0:
            cfg.glob.line_type.process_document(cfg.glob.parse_result_line_3_pages)
        cfg.glob.parse_result_line_4_document = {
            cfg.glob.JSON_NAME_BASE_ID: cfg.glob.base.base_id,
            cfg.glob.JSON_NAME_BASE_FILE_NAME: cfg.glob.base.base_file_name,
            cfg.glob.JSON_NAME_NO_PAGES_IN_DOC: cfg.glob.parse_result_no_pages_in_doc,
            cfg.glob.JSON_NAME_PAGES: cfg.glob.parse_result_line_3_pages,
        }
        with open(cfg.glob.action_next.get_full_name(), "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(cfg.glob.parse_result_line_4_document, file_handle)
    elif cfg.glob.setup.is_parsing_word:
        cfg.glob.parse_result_word_4_document = {
            cfg.glob.JSON_NAME_BASE_ID: cfg.glob.base.base_id,
            cfg.glob.JSON_NAME_BASE_FILE_NAME: cfg.glob.base.base_file_name,
            cfg.glob.JSON_NAME_NO_PAGES_IN_DOC: cfg.glob.parse_result_no_pages_in_doc,
            cfg.glob.JSON_NAME_PAGES: cfg.glob.parse_result_word_3_pages,
        }
        with open(cfg.glob.action_next.get_full_name(), "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
            json.dump(cfg.glob.parse_result_word_4_document, file_handle)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag Para.
# -----------------------------------------------------------------------------
def parse_tag_para(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Para'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    # Initialize the parse result variables of a paragraph.
    cfg.glob.parse_result_line_index_para = 0
    cfg.glob.parse_result_no_lines_in_para = 0
    cfg.glob.parse_result_no_words_in_para = 0
    cfg.glob.parse_result_word_index_para = 0

    cfg.glob.parse_result_no_paras_in_page += 1

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_BOX:
                parse_tag_box(child_tag, child)

    cfg.glob.parse_result_para_index_page += 1

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag Row.
# -----------------------------------------------------------------------------
def parse_tag_row(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Row'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_CELL:
                parse_tag_cell(child_tag, child)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag Table.
# -----------------------------------------------------------------------------
def parse_tag_table(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Table'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_ROW:
                parse_tag_row(child_tag, child)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag Text.
# -----------------------------------------------------------------------------
def parse_tag_text(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Text'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    cfg.glob.parse_result_text = parent.text

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag Word.
# -----------------------------------------------------------------------------
def parse_tag_word(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Word'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_BOX:
                parse_tag_box(child_tag, child)
            case cfg.glob.PARSE_TAG_TEXT:
                parse_tag_text(child_tag, child)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    cfg.glob.parse_result_no_words_in_line += 1
    cfg.glob.parse_result_no_words_in_page += 1
    cfg.glob.parse_result_no_words_in_para += 1

    debug_xml_element_text_word()

    if cfg.glob.setup.is_parsing_word:
        cfg.glob.parse_result_word_1_words.append(
            {
                cfg.glob.JSON_NAME_LINE_INDEX_PAGE: cfg.glob.parse_result_line_index_page,
                cfg.glob.JSON_NAME_WORD_INDEX_LINE: cfg.glob.parse_result_word_index_line,
                cfg.glob.JSON_NAME_WORD_TEXT: cfg.glob.parse_result_text,
            }
        )

    cfg.glob.parse_result_word_index_line += 1
    cfg.glob.parse_result_word_index_page += 1
    cfg.glob.parse_result_word_index_para += 1


# -----------------------------------------------------------------------------
# Parse the TETML files (step: s_p_j).
# -----------------------------------------------------------------------------
def parse_tetml() -> None:
    """Parse the TETML files.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    with cfg.glob.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(
            conn=conn, action_code=db.cls_run.Run.ACTION_CODE_PARSER_LINE
        )

        for row in rows:
            # ------------------------------------------------------------------
            # Processing a single document
            # ------------------------------------------------------------------
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_row(row)

            if cfg.glob.action_curr.action_status == cfg.glob.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                cfg.glob.run.total_status_ready += 1

            cfg.glob.base = db.cls_base.Base.from_id(id_base=cfg.glob.action_curr.action_id_base)

            parse_tetml_file(tetml_type=TETML_TYPE_LINE)

        conn.close()

    with cfg.glob.db_orm_engine.begin() as conn:
        rows = db.cls_action.Action.select_action_by_action_code(
            conn=conn, action_code=db.cls_run.Run.ACTION_CODE_PARSER_WORD
        )

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            cfg.glob.run.run_total_processed_to_be += 1

            cfg.glob.action_curr = db.cls_action.Action.from_row(row)

            if cfg.glob.action_curr.action_status == cfg.glob.DOCUMENT_STATUS_ERROR:
                cfg.glob.run.total_status_error += 1
            else:
                cfg.glob.run.total_status_ready += 1

            cfg.glob.base = db.cls_base.Base.from_id(id_base=cfg.glob.action_curr.action_id_base)

            parse_tetml_file(tetml_type=TETML_TYPE_WORD)

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Parse the TETML file (step: s_p_j).
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def parse_tetml_file(tetml_type: str) -> None:
    """Parse the TETML file.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    full_name_curr = cfg.glob.action_curr.get_full_name()

    file_name_next = cfg.glob.action_curr.get_stem_name() + "." + cfg.glob.DOCUMENT_FILE_TYPE_JSON
    full_name_next = utils.get_full_name(
        cfg.glob.action_curr.action_directory_name,
        file_name_next,
    )

    if tetml_type == TETML_TYPE_LINE:
        cfg.glob.setup.is_parsing_line = True
        cfg.glob.setup.is_parsing_word = False
    else:
        cfg.glob.setup.is_parsing_line = False
        cfg.glob.setup.is_parsing_word = True

    # Create the Element tree object
    tree = defusedxml.ElementTree.parse(full_name_curr)

    # Get the root Element
    root = tree.getroot()

    cfg.glob.action_next = db.cls_action.Action(
        action_code=db.cls_run.Run.ACTION_CODE_TOKENIZE,
        directory_name=cfg.glob.action_curr.action_directory_name,
        directory_type=cfg.glob.action_curr.action_directory_type,
        file_name=file_name_next,
        file_size_bytes=-1,
        id_base=cfg.glob.action_curr.action_id_base,
        id_parent=cfg.glob.action_curr.action_id,
        id_run_last=cfg.glob.run.run_id,
        no_pdf_pages=-1,
    )

    for child in root:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_DOCUMENT:
                parse_tag_document(child_tag, child)
            case cfg.glob.PARSE_TAG_CREATION:
                pass

    cfg.glob.action_next.action_file_size_bytes = (os.path.getsize(pathlib.Path(full_name_next)),)
    cfg.glob.action_next.action_no_pdf_pages = utils.get_pdf_pages_no(str(pathlib.Path(full_name_next)))

    cfg.glob.action_next.persist_2_db()

    utils.delete_auxiliary_file(full_name_curr)

    cfg.glob.action_curr.finalise()

    cfg.glob.run.run_total_processed_ok += 1

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
