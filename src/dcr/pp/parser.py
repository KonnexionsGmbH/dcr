"""Module pp.parser: Store the document structure from the parser result."""
import os
import time
from datetime import datetime
from typing import Dict
from typing import Iterable

import db.cfg
import db.orm.dml
import defusedxml.ElementTree
import libs.cfg
import libs.utils


# -----------------------------------------------------------------------------
# Debug an XML element detailed.
# -----------------------------------------------------------------------------
def debug_xml_element_all(
    event: str, parent_tag: str, attrib: Dict[str, str], text: Iterable[str | None]
) -> None:
    """Debug an XML element detailed.

    Args:
        event (str): Event: 'start' or 'end'.
        parent_tag (str): Parent tag.
        attrib (Dict[str,str]): Attributes.
        text (Iterable[str|None]): XML element.
    """
    if libs.cfg.verbose_parser == "all":
        print(f"{event} tag   ={parent_tag}")

        if attrib != {}:
            print(f"      attrib={attrib}")

        if text is not None and str(text).strip() > "":
            print(f"      text  ='{text}'")


# -----------------------------------------------------------------------------
# Debug an XML element only 'text'.
# -----------------------------------------------------------------------------
def debug_xml_element_text() -> None:
    """Debug an XML element only 'text."""
    if libs.cfg.verbose_parser == "text":
        print(
            f"page={libs.cfg.parse_result_no_page:2d} "
            f"paragraph={libs.cfg.parse_result_no_para:2d} "
            f"sentence={libs.cfg.parse_result_no_sentence:2d} "
            f"line={libs.cfg.parse_result_no_line:2d} "
            f"word sentence={libs.cfg.parse_result_no_word_sentence:3d} "
            f"word line={libs.cfg.parse_result_no_word_line:2d} "
            f"text='{libs.cfg.parse_result_text}'"
        )


# -----------------------------------------------------------------------------
# Initialize the parse result variables.
# -----------------------------------------------------------------------------
def init_parse_result() -> None:
    """Initialize the parse result variables."""
    libs.cfg.parse_result_author = None
    libs.cfg.parse_result_creation_date = None
    libs.cfg.parse_result_mod_date = None
    libs.cfg.parse_result_no_line = 0
    libs.cfg.parse_result_no_page = 0
    libs.cfg.parse_result_no_para = 0
    libs.cfg.parse_result_no_sentence = 0
    libs.cfg.parse_result_no_word_line = 0
    libs.cfg.parse_result_text = None


# -----------------------------------------------------------------------------
# Initialize the parse result variables regarding sentence.
# -----------------------------------------------------------------------------
def init_parse_result_sentence() -> None:
    """Initialize the parse result variables regarding sentence."""
    libs.cfg.parse_result_no_word_sentence = 0

    libs.cfg.parse_result_sentence = {
        db.cfg.JSON_NAME_NO_SENTENCE_IN_PARA: None,
        db.cfg.JSON_NAME_NO_WORDS: None,
        db.cfg.JSON_NAME_WORDS: [],
    }


# -----------------------------------------------------------------------------
# Store the parse result in the database table content.
# -----------------------------------------------------------------------------
def insert_content() -> None:
    """Store the parse result in the database table content."""
    if not libs.cfg.parse_result_sentence[db.cfg.JSON_NAME_WORDS]:
        return

    libs.cfg.parse_result_sentence[
        db.cfg.JSON_NAME_NO_WORDS
    ] = libs.cfg.parse_result_no_word_sentence

    if not libs.cfg.is_simulate_parser:
        db.orm.dml.insert_dbt_row(
            db.cfg.DBT_CONTENT_TETML_WORD,
            {
                db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id_base,
                db.cfg.DBC_LINE_IN_PARA_END: libs.cfg.parse_result_line_in_para_end,
                db.cfg.DBC_LINE_IN_PARA_START: libs.cfg.parse_result_line_in_para_start,
                db.cfg.DBC_PAGE_IN_DOC_END: libs.cfg.parse_result_page_in_doc_end,
                db.cfg.DBC_PAGE_IN_DOC_START: libs.cfg.parse_result_page_in_doc_start,
                db.cfg.DBC_PARA_IN_PAGE_END: libs.cfg.parse_result_para_in_page_end,
                db.cfg.DBC_PARA_IN_PAGE_START: libs.cfg.parse_result_para_in_page_start,
                db.cfg.DBC_SENTENCE: libs.cfg.parse_result_sentence,
            },
        )

    init_parse_result_sentence()

    libs.cfg.parse_result_no_sentence += 1

    libs.cfg.parse_result_sentence[
        db.cfg.JSON_NAME_NO_SENTENCE_IN_PARA
    ] = libs.cfg.parse_result_no_sentence


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
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_LINE:
                parse_tag_line(child_tag, child)

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
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_PARA:
                parse_tag_para(child_tag, child)
            case (libs.cfg.PARSE_TAG_PLACED_IMAGE | libs.cfg.PARSE_TAG_TABLE):
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
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_AUTHOR:
                libs.cfg.parse_result_author = child.text
            case libs.cfg.PARSE_TAG_CREATION_DATE:
                libs.cfg.parse_result_creation_date = datetime.strptime(
                    child.text, "%Y-%m-%dT%H:%M:%S%z"
                )
            case (
                libs.cfg.PARSE_TAG_CREATOR
                | libs.cfg.PARSE_TAG_PRODUCER
                | libs.cfg.PARSE_TAG_CUSTOM
                | libs.cfg.PARSE_TAG_TITLE
            ):
                pass
            case libs.cfg.PARSE_TAG_MOD_DATE:
                libs.cfg.parse_result_mod_date = datetime.strptime(
                    child.text, "%Y-%m-%dT%H:%M:%S%z"
                )

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
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case (
                libs.cfg.PARSE_TAG_ACTION
                | libs.cfg.PARSE_TAG_ATTACHMENTS
                | libs.cfg.PARSE_TAG_BOOKMARKS
                | libs.cfg.PARSE_TAG_DESTINATIONS
                | libs.cfg.PARSE_TAG_ENCRYPTION
                | libs.cfg.PARSE_TAG_EXCEPTION
                | libs.cfg.PARSE_TAG_JAVA_SCRIPTS
                | libs.cfg.PARSE_TAG_METADATA
                | libs.cfg.PARSE_TAG_OPTIONS
                | libs.cfg.PARSE_TAG_OUTPUT_INTENTS
                | libs.cfg.PARSE_TAG_SIGNATURE_FIELDS
                | libs.cfg.PARSE_TAG_XFA
            ):
                pass
            case libs.cfg.PARSE_TAG_DOC_INFO:
                parse_tag_doc_info(child_tag, child)
            case libs.cfg.PARSE_TAG_PAGES:
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

    libs.cfg.parse_result_no_line += 1
    libs.cfg.parse_result_no_word_line = 0

    libs.cfg.parse_result_line_in_para_start = libs.cfg.parse_result_no_line
    libs.cfg.parse_result_page_in_doc_start = libs.cfg.parse_result_no_page
    libs.cfg.parse_result_para_in_page_start = libs.cfg.parse_result_no_para

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_WORD:
                parse_tag_word(child_tag, child)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'Page'.
# -----------------------------------------------------------------------------
def parse_tag_page(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Page'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    libs.cfg.parse_result_no_page = int(parent.attrib["number"])
    libs.cfg.parse_result_no_para = 0

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case (
                libs.cfg.PARSE_TAG_ACTION
                | libs.cfg.PARSE_TAG_ANNOTATIONS
                | libs.cfg.PARSE_TAG_EXCEPTION
                | libs.cfg.PARSE_TAG_FIELDS
                | libs.cfg.PARSE_TAG_OPTIONS
                | libs.cfg.PARSE_TAG_OUTPUT_INTENTS
            ):
                pass
            case libs.cfg.PARSE_TAG_CONTENT:
                parse_tag_content(child_tag, child)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'Pages'.
# -----------------------------------------------------------------------------
def parse_tag_pages(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Pages'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_GRAPHICS | libs.cfg.PARSE_TAG_RESOURCES:
                pass
            case libs.cfg.PARSE_TAG_PAGE:
                parse_tag_page(child_tag, child)

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

    libs.cfg.parse_result_no_line = 0
    libs.cfg.parse_result_no_para += 1
    libs.cfg.parse_result_no_sentence = 1
    libs.cfg.parse_result_no_word_sentence = 0

    libs.cfg.parse_result_sentence[
        db.cfg.JSON_NAME_NO_SENTENCE_IN_PARA
    ] = libs.cfg.parse_result_no_sentence
    libs.cfg.parse_result_sentence[db.cfg.JSON_NAME_WORDS] = []

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_BOX:
                parse_tag_box(child_tag, child)

    insert_content()

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

    libs.cfg.parse_result_text = parent.text

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
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_BOX:
                parse_tag_box(child_tag, child)
            case libs.cfg.PARSE_TAG_TEXT:
                parse_tag_text(child_tag, child)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)

    libs.cfg.parse_result_no_word_line += 1
    libs.cfg.parse_result_no_word_sentence += 1

    debug_xml_element_text()

    word_list = libs.cfg.parse_result_sentence[db.cfg.JSON_NAME_WORDS]
    word_list.append(
        {
            db.cfg.JSON_NAME_NO_WORD_LINE: libs.cfg.parse_result_no_word_line,
            db.cfg.JSON_NAME_NO_WORD_SENTENCE: libs.cfg.parse_result_no_word_sentence,
            db.cfg.JSON_NAME_WORD_PARSED: libs.cfg.parse_result_text,
        }
    )
    libs.cfg.parse_result_sentence[db.cfg.JSON_NAME_WORDS] = word_list

    libs.cfg.parse_result_line_in_para_end = libs.cfg.parse_result_no_line
    libs.cfg.parse_result_page_in_doc_end = libs.cfg.parse_result_no_page
    libs.cfg.parse_result_para_in_page_end = libs.cfg.parse_result_no_para

    if libs.cfg.parse_result_text == ".":
        insert_content()

    libs.cfg.parse_result_text = None


# -----------------------------------------------------------------------------
# Parse the TETML files (step: s_f_p).
# -----------------------------------------------------------------------------
def parse_tetml() -> None:
    """Parse the TETML files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = libs.utils.select_document_prepare()

    libs.utils.reset_statistics_total()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.orm.dml.select_document(conn, dbt, db.cfg.DOCUMENT_STEP_PARSER)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            parse_tetml_file()

            # Text and metadata from Document successfully extracted to xml format
            if not libs.cfg.is_simulate_parser:
                libs.utils.finalize_file_processing()

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Parse the TETML file (step: s_f_p).
# -----------------------------------------------------------------------------
def parse_tetml_file() -> None:
    """Parse a document.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    file_name = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    init_parse_result()
    init_parse_result_sentence()

    # Create the Element tree object
    tree = defusedxml.ElementTree.parse(file_name)

    # Get the root Element
    root = tree.getroot()

    for child in root:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_DOCUMENT:
                parse_tag_document(child_tag, child)
            case libs.cfg.PARSE_TAG_CREATION:
                pass

    if not libs.cfg.is_simulate_parser:
        libs.utils.delete_auxiliary_file(file_name)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
