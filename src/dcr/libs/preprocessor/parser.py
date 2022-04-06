"""Module libs.preprocessor.parser: Store the document structure from the
parser result."""
import json
import os
import time
from datetime import datetime
from typing import Dict
from typing import Iterable

import defusedxml.ElementTree
import libs.cfg
import libs.db.cfg
import libs.db.orm.dml
import libs.utils


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
            f"font='{libs.cfg.parse_result_font_id}' "
            f"size='{libs.cfg.parse_result_font_size}' "
            f"text='{libs.cfg.parse_result_text}'"
        )


# -----------------------------------------------------------------------------
# Initialize the parse result variables.
# -----------------------------------------------------------------------------
def init_parse_result() -> None:
    """Initialize the parse result variables."""
    libs.cfg.parse_result_author = None
    libs.cfg.parse_result_creation_date = None
    libs.cfg.parse_result_font_id = None
    libs.cfg.parse_result_font_size = None
    libs.cfg.parse_result_fonts = []
    libs.cfg.parse_result_fonts_no_words = {}
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
        libs.db.cfg.JSON_NAME_NO_SENTENCE_IN_PARA: None,
        libs.db.cfg.JSON_NAME_NO_WORDS: None,
        libs.db.cfg.JSON_NAME_WORDS: [],
    }


# -----------------------------------------------------------------------------
# Store the parse result in the database table content.
# -----------------------------------------------------------------------------
def insert_content() -> None:
    """Store the parse result in the database table content."""
    if not libs.cfg.parse_result_sentence[libs.db.cfg.JSON_NAME_WORDS]:
        return

    libs.cfg.parse_result_sentence[libs.db.cfg.JSON_NAME_NO_WORDS] = libs.cfg.parse_result_no_word_sentence

    if not libs.cfg.is_simulate_parser:
        libs.db.orm.dml.insert_dbt_row(
            libs.db.cfg.DBT_CONTENT,
            {
                libs.db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id_base,
                libs.db.cfg.DBC_LINE_IN_PARA_END: libs.cfg.parse_result_line_in_para_end,
                libs.db.cfg.DBC_LINE_IN_PARA_START: libs.cfg.parse_result_line_in_para_start,
                libs.db.cfg.DBC_PAGE_IN_DOCUMENT_END: libs.cfg.parse_result_page_in_document_end,
                libs.db.cfg.DBC_PAGE_IN_DOCUMENT_START: libs.cfg.parse_result_page_in_document_start,
                libs.db.cfg.DBC_PARA_IN_PAGE_END: libs.cfg.parse_result_para_in_page_end,
                libs.db.cfg.DBC_PARA_IN_PAGE_START: libs.cfg.parse_result_para_in_page_start,
                libs.db.cfg.DBC_SENTENCE: json.dumps(libs.cfg.parse_result_sentence),
            },
        )

    init_parse_result_sentence()

    libs.cfg.parse_result_no_sentence += 1

    libs.cfg.parse_result_sentence[libs.db.cfg.JSON_NAME_NO_SENTENCE_IN_PARA] = libs.cfg.parse_result_no_sentence


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
            case (libs.cfg.PARSE_TAG_A | libs.cfg.PARSE_TAG_PLACED_IMAGE | libs.cfg.PARSE_TAG_TABLE):
                pass
            case libs.cfg.PARSE_TAG_GLYPH:
                parse_tag_glyph(child_tag, child)
            case libs.cfg.PARSE_TAG_LINE:
                parse_tag_line(child_tag, child)
            # not testable
            # case libs.cfg.PARSE_TAG_PARA:
            #     parse_tag_para(child_tag, child)
            # case libs.cfg.PARSE_TAG_TEXT:
            #     parse_tag_text(child_tag, child)
            # case libs.cfg.PARSE_TAG_WORD:
            #     parse_tag_word(child_tag, child)

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
                libs.cfg.parse_result_creation_date = datetime.strptime(child.text, "%Y-%m-%dT%H:%M:%S%z")
            case (
                libs.cfg.PARSE_TAG_CREATOR
                | libs.cfg.PARSE_TAG_PRODUCER
                | libs.cfg.PARSE_TAG_CUSTOM
                | libs.cfg.PARSE_TAG_TITLE
            ):
                pass
            case libs.cfg.PARSE_TAG_MOD_DATE:
                libs.cfg.parse_result_mod_date = datetime.strptime(child.text, "%Y-%m-%dT%H:%M:%S%z")

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
# Processing tag 'Font'.
# -----------------------------------------------------------------------------
def parse_tag_font(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Font'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    libs.cfg.parse_result_fonts.append(
        {
            libs.db.cfg.JSON_NAME_ID: parent.attrib[libs.cfg.PARSE_ATTRIB_ID],
            libs.db.cfg.JSON_NAME_ITALIC_ANGLE: parent.attrib[libs.cfg.PARSE_ATTRIB_ITALIC_ANGLE],
            libs.db.cfg.JSON_NAME_NAME: parent.attrib[libs.cfg.PARSE_ATTRIB_NAME],
            libs.db.cfg.JSON_NAME_NO_WORDS: libs.cfg.parse_result_fonts_no_words[
                parent.attrib[libs.cfg.PARSE_ATTRIB_ID]
            ],
            libs.db.cfg.JSON_NAME_WEIGHT: parent.attrib[libs.cfg.PARSE_ATTRIB_WEIGHT],
        }
    )

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'Fonts'.
# -----------------------------------------------------------------------------
def parse_tag_fonts(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Fonts'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_FONT:
                parse_tag_font(child_tag, child)

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag Glyph.
# -----------------------------------------------------------------------------
def parse_tag_glyph(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Glyph'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    if libs.cfg.parse_result_font_id is None:
        libs.cfg.parse_result_font_id = parent.attrib[libs.cfg.PARSE_ATTRIB_FONT]
        libs.cfg.parse_result_font_size = parent.attrib[libs.cfg.PARSE_ATTRIB_SIZE]

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
    libs.cfg.parse_result_page_in_document_start = libs.cfg.parse_result_no_page
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
                parse_tag_resources(child_tag, child)
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

    libs.cfg.parse_result_sentence[libs.db.cfg.JSON_NAME_NO_SENTENCE_IN_PARA] = libs.cfg.parse_result_no_sentence
    libs.cfg.parse_result_sentence[libs.db.cfg.JSON_NAME_WORDS] = []

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_A:
                pass
            case libs.cfg.PARSE_TAG_BOX:
                parse_tag_box(child_tag, child)
            # not testable
            # case libs.cfg.PARSE_TAG_PARA:
            #     parse_tag_para(child_tag, child)

    insert_content()

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag Resources.
# -----------------------------------------------------------------------------
def parse_tag_resources(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Resources'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case (libs.cfg.PARSE_TAG_COLOR_SPACES | libs.cfg.PARSE_TAG_IMAGES | libs.cfg.PARSE_TAG_PATTERNX):
                pass
            case libs.cfg.PARSE_TAG_FONTS:
                parse_tag_fonts(child_tag, child)

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

    word_list = libs.cfg.parse_result_sentence[libs.db.cfg.JSON_NAME_WORDS]
    word_list.append(
        {
            libs.db.cfg.JSON_NAME_FONT_ID: libs.cfg.parse_result_font_id,
            libs.db.cfg.JSON_NAME_FONT_SIZE: libs.cfg.parse_result_font_size,
            libs.db.cfg.JSON_NAME_NO_WORD_LINE: libs.cfg.parse_result_no_word_line,
            libs.db.cfg.JSON_NAME_NO_WORD_SENTENCE: libs.cfg.parse_result_no_word_sentence,
            libs.db.cfg.JSON_NAME_WORD_PARSED: libs.cfg.parse_result_text,
        }
    )
    libs.cfg.parse_result_sentence[libs.db.cfg.JSON_NAME_WORDS] = word_list

    if libs.cfg.parse_result_font_id in libs.cfg.parse_result_fonts_no_words:
        libs.cfg.parse_result_fonts_no_words[libs.cfg.parse_result_font_id] = (
            libs.cfg.parse_result_fonts_no_words[libs.cfg.parse_result_font_id] + 1
        )
    else:
        libs.cfg.parse_result_fonts_no_words[libs.cfg.parse_result_font_id] = 1

    libs.cfg.parse_result_line_in_para_end = libs.cfg.parse_result_no_line
    libs.cfg.parse_result_page_in_document_end = libs.cfg.parse_result_no_page
    libs.cfg.parse_result_para_in_page_end = libs.cfg.parse_result_no_para

    if libs.cfg.parse_result_text == ".":
        insert_content()

    libs.cfg.parse_result_font_id = None
    libs.cfg.parse_result_font_size = None
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

    with libs.db.cfg.db_orm_engine.connect() as conn:
        rows = libs.utils.select_document(conn, dbt, libs.db.cfg.DOCUMENT_STEP_PARSER)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            parse_tetml_file()

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

    # Text and metadata from Document successfully extracted to xml format
    if not libs.cfg.is_simulate_parser:
        libs.utils.finalize_file_processing()

    # Update the font information in the database table.
    libs.db.orm.dml.update_dbt_id(
        libs.db.cfg.DBT_DOCUMENT,
        libs.cfg.document_id_base,
        {
            libs.db.cfg.DBC_FONTS: json.dumps(libs.cfg.parse_result_fonts),
        },
    )

    libs.db.orm.dml.insert_journal_statistics(libs.cfg.document_id)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
