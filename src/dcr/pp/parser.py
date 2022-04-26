"""Module pp.parser: Store the document structure from the parser result."""
import datetime
import os
import time
import typing

import db.cfg
import db.orm.dml
import defusedxml.ElementTree
import libs.cfg
import libs.utils


# -----------------------------------------------------------------------------
# Debug an XML element detailed.
# -----------------------------------------------------------------------------
def debug_xml_element_all(
    event: str, parent_tag: str, attrib: typing.Dict[str, str], text: typing.Iterable[str | None]
) -> None:
    """Debug an XML element detailed.

    Args:
        event (str): Event: 'start' or 'end'.
        parent_tag (str): Parent tag.
        attrib (Dict[str,str]): Attributes.
        text (Iterable[str|None]): XML element.
    """
    if libs.cfg.config.verbose_parser == "all":
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
    if libs.cfg.config.verbose_parser == "text":
        print(
            f"page_i_doc={libs.cfg.parse_result_page_index_doc:2d} "
            f"para_i_page={libs.cfg.parse_result_para_index_page:2d} "
            f"line_i_page={libs.cfg.parse_result_line_index_page:2d} "
            f"line_i_para={libs.cfg.parse_result_line_index_para:2d} "
            f"text='{libs.cfg.parse_result_text}'"
        )


# -----------------------------------------------------------------------------
# Debug an XML element only 'text' - variant word.
# -----------------------------------------------------------------------------
def debug_xml_element_text_word() -> None:
    """Debug an XML element only 'text - variant word."""
    if libs.cfg.config.verbose_parser == "text":
        print(
            f"page_i_doc={libs.cfg.parse_result_page_index_doc:2d} "
            f"para_i_page={libs.cfg.parse_result_para_index_page:2d} "
            f"line_i_page={libs.cfg.parse_result_line_index_page:2d} "
            f"line_i_para={libs.cfg.parse_result_line_index_para:2d} "
            f"word_i_page={libs.cfg.parse_result_word_index_page:2d} "
            f"word_i_para={libs.cfg.parse_result_word_index_para:2d} "
            f"word_i_line={libs.cfg.parse_result_word_index_line:2d} "
            f"text='{libs.cfg.parse_result_text}'"
        )


# -----------------------------------------------------------------------------
# Initialize the parse result variables of a document.
# -----------------------------------------------------------------------------
def init_parse_result_document() -> None:
    """Initialize the parse result variables of a document."""
    libs.cfg.parse_result_no_pages_in_doc = 0
    libs.cfg.parse_result_page_index_doc = 0


# -----------------------------------------------------------------------------
# Initialize the parse result variables of a line.
# -----------------------------------------------------------------------------
def init_parse_result_line() -> None:
    """Initialize the parse result variables of a line."""
    libs.cfg.parse_result_no_words_in_line = 0
    libs.cfg.parse_result_word_index_line = 0


# -----------------------------------------------------------------------------
# Initialize the parse result variables of a page.
# -----------------------------------------------------------------------------
def init_parse_result_page() -> None:
    """Initialize the parse result variables of a page."""
    libs.cfg.parse_result_line_index_page = 0
    libs.cfg.parse_result_no_lines_in_page = 0
    libs.cfg.parse_result_no_paras_in_page = 0
    libs.cfg.parse_result_no_words_in_page = 0
    libs.cfg.parse_result_page_lines = {
        db.cfg.JSON_NAME_NO_LINES_IN_PAGE: None,
        db.cfg.JSON_NAME_NO_PARAS_IN_PAGE: None,
        db.cfg.JSON_NAME_PAGE_LINES: [],
    }
    libs.cfg.parse_result_page_words = {
        db.cfg.JSON_NAME_NO_LINES_IN_PAGE: None,
        db.cfg.JSON_NAME_NO_PARAS_IN_PAGE: None,
        db.cfg.JSON_NAME_NO_WORDS_IN_PAGE: None,
        db.cfg.JSON_NAME_PAGE_WORDS: [],
    }
    libs.cfg.parse_result_para_index_page = 0
    libs.cfg.parse_result_word_index_page = 0


# -----------------------------------------------------------------------------
# Initialize the parse result variables of a para.
# -----------------------------------------------------------------------------
def init_parse_result_para() -> None:
    """Initialize the parse result variables mof a para."""
    libs.cfg.parse_result_line_index_para = 0
    libs.cfg.parse_result_no_lines_in_para = 0
    libs.cfg.parse_result_no_words_in_para = 0
    libs.cfg.parse_result_word_index_para = 0


# -----------------------------------------------------------------------------
# Store the parse result in the database table content_tetml_line.
# -----------------------------------------------------------------------------
def insert_content_tetml_line() -> None:
    """Store the parse result in the database table content_tetml_line."""
    if not libs.cfg.config.is_simulate_parser:
        libs.cfg.parse_result_page_lines[
            db.cfg.JSON_NAME_NO_LINES_IN_PAGE
        ] = libs.cfg.parse_result_no_lines_in_page
        libs.cfg.parse_result_page_lines[
            db.cfg.JSON_NAME_NO_PARAS_IN_PAGE
        ] = libs.cfg.parse_result_no_paras_in_page

        db.orm.dml.insert_dbt_row(
            db.cfg.DBT_CONTENT_TETML_LINE,
            {
                db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id_base,
                db.cfg.DBC_PAGE_NO: libs.cfg.parse_result_no_pages_in_doc,
                db.cfg.DBC_PAGE_DATA: libs.cfg.parse_result_page_lines,
            },
        )


# -----------------------------------------------------------------------------
# Store the parse result in the database table content_tetml_word.
# -----------------------------------------------------------------------------
def insert_content_tetml_word() -> None:
    """Store the parse result in the database table content_tetml_word."""
    if not libs.cfg.config.is_simulate_parser:
        libs.cfg.parse_result_page_words[
            db.cfg.JSON_NAME_NO_LINES_IN_PAGE
        ] = libs.cfg.parse_result_no_lines_in_page
        libs.cfg.parse_result_page_words[
            db.cfg.JSON_NAME_NO_PARAS_IN_PAGE
        ] = libs.cfg.parse_result_no_paras_in_page
        libs.cfg.parse_result_page_words[
            db.cfg.JSON_NAME_NO_WORDS_IN_PAGE
        ] = libs.cfg.parse_result_no_words_in_page

        db.orm.dml.insert_dbt_row(
            db.cfg.DBT_CONTENT_TETML_WORD,
            {
                db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id_base,
                db.cfg.DBC_PAGE_NO: libs.cfg.parse_result_no_pages_in_doc,
                db.cfg.DBC_PAGE_DATA: libs.cfg.parse_result_page_words,
            },
        )


# -----------------------------------------------------------------------------
# Processing tag Box.
# -----------------------------------------------------------------------------
def parse_tag_box(parent_tag: str, parent: typing.Iterable[str]) -> None:
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
def parse_tag_content(parent_tag: str, parent: typing.Iterable[str]) -> None:
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
def parse_tag_doc_info(parent_tag: str, parent: typing.Iterable[str]) -> None:
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
                libs.cfg.parse_result_creation_date = datetime.datetime.strptime(
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
                libs.cfg.parse_result_mod_date = datetime.datetime.strptime(
                    child.text, "%Y-%m-%dT%H:%M:%S%z"
                )

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'Document'.
# -----------------------------------------------------------------------------
def parse_tag_document(parent_tag: str, parent: typing.Iterable[str]) -> None:
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
def parse_tag_line(parent_tag: str, parent: typing.Iterable[str]) -> None:
    """Processing tag 'Line'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    init_parse_result_line()

    libs.cfg.parse_result_no_lines_in_page += 1
    libs.cfg.parse_result_no_lines_in_para += 1

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_TEXT:
                parse_tag_text(child_tag, child)
            case libs.cfg.PARSE_TAG_WORD:
                parse_tag_word(child_tag, child)

    debug_xml_element_text_line()

    if libs.cfg.config.is_parsing_line:
        page_lines = libs.cfg.parse_result_page_lines[db.cfg.JSON_NAME_PAGE_LINES]
        page_lines.append(
            {
                db.cfg.JSON_NAME_PARA_INDEX_PAGE: libs.cfg.parse_result_para_index_page,
                db.cfg.JSON_NAME_LINE_INDEX_PAGE: libs.cfg.parse_result_line_index_page,
                db.cfg.JSON_NAME_LINE_INDEX_PARA: libs.cfg.parse_result_line_index_para,
                db.cfg.JSON_NAME_LINE_TEXT: libs.cfg.parse_result_text,
                db.cfg.JSON_NAME_LINE_TYPE: db.cfg.DOCUMENT_LINE_TYPE_BODY,
            }
        )
        libs.cfg.parse_result_page_lines[db.cfg.JSON_NAME_PAGE_LINES] = page_lines

    libs.cfg.parse_result_line_index_page += 1
    libs.cfg.parse_result_line_index_para += 1

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'Page'.
# -----------------------------------------------------------------------------
def parse_tag_page(parent_tag: str, parent: typing.Iterable[str]) -> None:
    """Processing tag 'Page'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    init_parse_result_page()

    libs.cfg.parse_result_no_pages_in_doc += 1

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

    libs.cfg.parse_result_page_index_doc += 1

    if not libs.cfg.config.is_simulate_parser:
        if libs.cfg.config.is_parsing_line:
            insert_content_tetml_line()
        elif libs.cfg.config.is_parsing_word:
            insert_content_tetml_word()

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag 'Pages'.
# -----------------------------------------------------------------------------
def parse_tag_pages(parent_tag: str, parent: typing.Iterable[str]) -> None:
    """Processing tag 'Pages'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    init_parse_result_document()

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
def parse_tag_para(parent_tag: str, parent: typing.Iterable[str]) -> None:
    """Processing tag 'Para'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    init_parse_result_para()

    libs.cfg.parse_result_no_paras_in_page += 1

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_BOX:
                parse_tag_box(child_tag, child)

    libs.cfg.parse_result_para_index_page += 1

    debug_xml_element_all("End  ", parent_tag, parent.attrib, parent.text)


# -----------------------------------------------------------------------------
# Processing tag Text.
# -----------------------------------------------------------------------------
def parse_tag_text(parent_tag: str, parent: typing.Iterable[str]) -> None:
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
def parse_tag_word(parent_tag: str, parent: typing.Iterable[str]) -> None:
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

    libs.cfg.parse_result_no_words_in_line += 1
    libs.cfg.parse_result_no_words_in_page += 1
    libs.cfg.parse_result_no_words_in_para += 1

    debug_xml_element_text_word()

    if libs.cfg.config.is_parsing_word:
        page_words = libs.cfg.parse_result_page_words[db.cfg.JSON_NAME_PAGE_WORDS]
        page_words.append(
            {
                db.cfg.JSON_NAME_LINE_INDEX_PAGE: libs.cfg.parse_result_line_index_page,
                db.cfg.JSON_NAME_WORD_INDEX_LINE: libs.cfg.parse_result_word_index_line,
                db.cfg.JSON_NAME_WORD_TEXT: libs.cfg.parse_result_text,
            }
        )
        libs.cfg.parse_result_page_words[db.cfg.JSON_NAME_PAGE_WORDS] = page_words

    libs.cfg.parse_result_word_index_line += 1
    libs.cfg.parse_result_word_index_page += 1
    libs.cfg.parse_result_word_index_para += 1


# -----------------------------------------------------------------------------
# Parse the TETML files (step: s_f_p).
# -----------------------------------------------------------------------------
def parse_tetml() -> None:
    """Parse the TETML files.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    dbt = db.orm.dml.dml_prepare(db.cfg.DBT_DOCUMENT)

    libs.utils.reset_statistics_total()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.orm.dml.select_document(conn, dbt, db.cfg.DOCUMENT_STEP_PARSER_LINE)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            parse_tetml_file_line()

            # Text and metadata from Document successfully extracted to xml format
            if not libs.cfg.config.is_simulate_parser:
                duration_ns = libs.utils.finalize_file_processing()

                if libs.cfg.config.is_verbose:
                    libs.utils.progress_msg(
                        f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                        f"Document: {libs.cfg.document_id:6d} "
                        f"[{db.orm.dml.select_document_file_name_id(libs.cfg.document_id)}]"
                    )

        conn.close()

    with db.cfg.db_orm_engine.connect() as conn:
        rows = db.orm.dml.select_document(conn, dbt, db.cfg.DOCUMENT_STEP_PARSER_WORD)

        for row in rows:
            libs.cfg.start_time_document = time.perf_counter_ns()

            libs.utils.start_document_processing(
                document=row,
            )

            parse_tetml_file_word()

            # Text and metadata from Document successfully extracted to xml format
            if not libs.cfg.config.is_simulate_parser:
                duration_ns = libs.utils.finalize_file_processing()

                if libs.cfg.config.is_verbose:
                    libs.utils.progress_msg(
                        f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                        f"Document: {libs.cfg.document_id:6d} "
                        f"[{db.orm.dml.select_document_file_name_id(libs.cfg.document_id)}]"
                    )

        conn.close()

    libs.utils.show_statistics_total()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Parse the TETML file type line (step: s_f_p).
# -----------------------------------------------------------------------------
def parse_tetml_file_line() -> None:
    """Parse the TETML file type line.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_PARSER_LINE

    file_name = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    libs.cfg.config.is_parsing_line = True
    libs.cfg.config.is_parsing_word = False

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

    if not libs.cfg.config.is_simulate_parser:
        libs.utils.delete_auxiliary_file(file_name)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)


# -----------------------------------------------------------------------------
# Parse the TETML file type word (step: s_f_p).
# -----------------------------------------------------------------------------
def parse_tetml_file_word() -> None:
    """Parse the TETML file type word.

    TBD
    """
    libs.cfg.logger.debug(libs.cfg.LOGGER_START)

    libs.cfg.document_current_step = db.cfg.DOCUMENT_STEP_PARSER_WORD

    file_name = os.path.join(
        libs.cfg.document_directory_name,
        libs.cfg.document_file_name,
    )

    libs.cfg.config.is_parsing_line = False
    libs.cfg.config.is_parsing_word = True

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

    if not libs.cfg.config.is_simulate_parser:
        libs.utils.delete_auxiliary_file(file_name)

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
