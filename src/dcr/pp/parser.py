"""Module pp.parser: Store the document structure from the parser result."""
import datetime
import os
import time
import typing

import cfg.glob
import db.dml
import defusedxml.ElementTree
import nlp.line_type
import utils


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
# Initialize the parse result variables of a document.
# -----------------------------------------------------------------------------
def init_parse_result_document() -> None:
    """Initialize the parse result variables of a document."""
    cfg.glob.parse_result_no_pages_in_doc = 0
    cfg.glob.parse_result_page_index_doc = -1


# -----------------------------------------------------------------------------
# Initialize the parse result variables of a line.
# -----------------------------------------------------------------------------
def init_parse_result_line() -> None:
    """Initialize the parse result variables of a line."""
    cfg.glob.parse_result_no_words_in_line = 0
    cfg.glob.parse_result_word_index_line = 0


# -----------------------------------------------------------------------------
# Initialize the parse result variables of a page.
# -----------------------------------------------------------------------------
def init_parse_result_page() -> None:
    """Initialize the parse result variables of a page."""
    cfg.glob.parse_result_line_index_page = 0
    cfg.glob.parse_result_no_lines_in_page = 0
    cfg.glob.parse_result_no_paras_in_page = 0
    cfg.glob.parse_result_no_words_in_page = 0

    cfg.glob.parse_result_page_lines = {
        cfg.glob.JSON_NAME_NO_LINES_IN_PAGE: None,
        cfg.glob.JSON_NAME_NO_PARAS_IN_PAGE: None,
        cfg.glob.JSON_NAME_PAGE_LINES: [],
    }

    cfg.glob.parse_result_page_words = {
        cfg.glob.JSON_NAME_NO_LINES_IN_PAGE: None,
        cfg.glob.JSON_NAME_NO_PARAS_IN_PAGE: None,
        cfg.glob.JSON_NAME_NO_WORDS_IN_PAGE: None,
        cfg.glob.JSON_NAME_PAGE_WORDS: [],
    }
    cfg.glob.parse_result_para_index_page = 0
    cfg.glob.parse_result_word_index_page = 0


# -----------------------------------------------------------------------------
# Initialize the parse result variables of a para.
# -----------------------------------------------------------------------------
def init_parse_result_para() -> None:
    """Initialize the parse result variables mof a para."""
    cfg.glob.parse_result_line_index_para = 0
    cfg.glob.parse_result_no_lines_in_para = 0
    cfg.glob.parse_result_no_words_in_para = 0
    cfg.glob.parse_result_word_index_para = 0


# -----------------------------------------------------------------------------
# Store the parse result in the database table content_tetml_line.
# -----------------------------------------------------------------------------
def insert_content_tetml_line() -> None:
    """Store the parse result in the database table content_tetml_line."""
    if not cfg.glob.setup.is_simulate_parser:
        cfg.glob.parse_result_page_lines[cfg.glob.JSON_NAME_NO_LINES_IN_PAGE] = cfg.glob.parse_result_no_lines_in_page

        cfg.glob.parse_result_page_lines[cfg.glob.JSON_NAME_NO_PARAS_IN_PAGE] = cfg.glob.parse_result_no_paras_in_page

        db.dml.insert_dbt_row(
            cfg.glob.DBT_CONTENT_TETML_LINE,
            {
                cfg.glob.DBC_DOCUMENT_ID: cfg.glob.document_id_base,
                cfg.glob.DBC_PAGE_NO: cfg.glob.parse_result_no_pages_in_doc,
                cfg.glob.DBC_PAGE_DATA: cfg.glob.parse_result_page_lines,
            },
        )


# -----------------------------------------------------------------------------
# Store the parse result in the database table content_tetml_word.
# -----------------------------------------------------------------------------
def insert_content_tetml_word() -> None:
    """Store the parse result in the database table content_tetml_word."""
    if not cfg.glob.setup.is_simulate_parser:
        cfg.glob.parse_result_page_words[cfg.glob.JSON_NAME_NO_LINES_IN_PAGE] = cfg.glob.parse_result_no_lines_in_page
        cfg.glob.parse_result_page_words[cfg.glob.JSON_NAME_NO_PARAS_IN_PAGE] = cfg.glob.parse_result_no_paras_in_page
        cfg.glob.parse_result_page_words[cfg.glob.JSON_NAME_NO_WORDS_IN_PAGE] = cfg.glob.parse_result_no_words_in_page

        db.dml.insert_dbt_row(
            cfg.glob.DBT_CONTENT_TETML_WORD,
            {
                cfg.glob.DBC_DOCUMENT_ID: cfg.glob.document_id_base,
                cfg.glob.DBC_PAGE_NO: cfg.glob.parse_result_no_pages_in_doc,
                cfg.glob.DBC_PAGE_DATA: cfg.glob.parse_result_page_words,
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
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_LINE:
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
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_PARA:
                parse_tag_para(child_tag, child)
            case (cfg.glob.PARSE_TAG_PLACED_IMAGE | cfg.glob.PARSE_TAG_TABLE):
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
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_AUTHOR:
                cfg.glob.parse_result_author = child.text
            case cfg.glob.PARSE_TAG_CREATION_DATE:
                cfg.glob.parse_result_creation_date = datetime.datetime.strptime(child.text, "%Y-%m-%dT%H:%M:%S%z")
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
def parse_tag_document(parent_tag: str, parent: typing.Iterable[str]) -> None:
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
def parse_tag_line(parent_tag: str, parent: typing.Iterable[str]) -> None:
    """Processing tag 'Line'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    debug_xml_element_all("Start", parent_tag, parent.attrib, parent.text)

    init_parse_result_line()

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
        page_lines = cfg.glob.parse_result_page_lines[cfg.glob.JSON_NAME_PAGE_LINES]
        page_lines.append(
            {
                cfg.glob.JSON_NAME_PARA_INDEX_PAGE: cfg.glob.parse_result_para_index_page,
                cfg.glob.JSON_NAME_LINE_INDEX_PAGE: cfg.glob.parse_result_line_index_page,
                cfg.glob.JSON_NAME_LINE_INDEX_PARA: cfg.glob.parse_result_line_index_para,
                cfg.glob.JSON_NAME_LINE_TEXT: cfg.glob.parse_result_text,
                cfg.glob.JSON_NAME_LINE_TYPE: cfg.glob.DOCUMENT_LINE_TYPE_BODY,
            }
        )
        cfg.glob.parse_result_page_lines[cfg.glob.JSON_NAME_PAGE_LINES] = page_lines

    cfg.glob.parse_result_line_index_page += 1
    cfg.glob.parse_result_line_index_para += 1

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

    # Initialize the page related variables.
    init_parse_result_page()

    cfg.glob.parse_result_no_pages_in_doc += 1  # relative 1
    cfg.glob.parse_result_page_index_doc += 1  # relative 0

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
    if not cfg.glob.setup.is_simulate_parser:
        if cfg.glob.setup.is_parsing_line:
            insert_content_tetml_line()
            if cfg.glob.setup.line_footer_max_lines > 0 or cfg.glob.setup.line_header_max_lines > 0:
                cfg.glob.line_type.process_page(
                    page_no=cfg.glob.parse_result_no_pages_in_doc,
                    page_lines=cfg.glob.parse_result_page_lines[cfg.glob.JSON_NAME_PAGE_LINES],
                )
        elif cfg.glob.setup.is_parsing_word:
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

    # Initialize the document related variables.
    init_parse_result_document()

    cfg.glob.parse_result_no_words_in_line = 0
    cfg.glob.parse_result_word_index_line = 0

    if cfg.glob.setup.is_parsing_line:
        cfg.glob.line_type = nlp.line_type.LineType()

    utils.progress_msg_line_type("LineType")
    utils.progress_msg_line_type(f"LineType: Start document                     ={cfg.glob.document_file_name}")

    # Process the tags of all document pages.
    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_GRAPHICS | cfg.glob.PARSE_TAG_RESOURCES:
                pass
            case cfg.glob.PARSE_TAG_PAGE:
                parse_tag_page(child_tag, child)

    # Process the document related variables.
    utils.progress_msg_line_type(f"LineType: End document                       ={cfg.glob.document_file_name}")
    if cfg.glob.setup.is_parsing_line:
        if cfg.glob.setup.line_footer_max_lines > 0 or cfg.glob.setup.line_header_max_lines > 0:
            cfg.glob.line_type.process_document(cfg.glob.document_id_base)

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

    cfg.glob.parse_result_no_paras_in_page += 1

    for child in parent:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_BOX:
                parse_tag_box(child_tag, child)

    cfg.glob.parse_result_para_index_page += 1

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

    cfg.glob.parse_result_text = parent.text

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
        page_words = cfg.glob.parse_result_page_words[cfg.glob.JSON_NAME_PAGE_WORDS]
        page_words.append(
            {
                cfg.glob.JSON_NAME_LINE_INDEX_PAGE: cfg.glob.parse_result_line_index_page,
                cfg.glob.JSON_NAME_WORD_INDEX_LINE: cfg.glob.parse_result_word_index_line,
                cfg.glob.JSON_NAME_WORD_TEXT: cfg.glob.parse_result_text,
            }
        )
        cfg.glob.parse_result_page_words[cfg.glob.JSON_NAME_PAGE_WORDS] = page_words

    cfg.glob.parse_result_word_index_line += 1
    cfg.glob.parse_result_word_index_page += 1
    cfg.glob.parse_result_word_index_para += 1


# -----------------------------------------------------------------------------
# Parse the TETML files (step: s_f_p).
# -----------------------------------------------------------------------------
def parse_tetml() -> None:
    """Parse the TETML files.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    dbt = db.dml.dml_prepare(cfg.glob.DBT_DOCUMENT)

    utils.reset_statistics_total()

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = db.dml.select_document(conn, dbt, cfg.glob.DOCUMENT_STEP_PARSER_LINE)

        for row in rows:
            # ------------------------------------------------------------------
            # Processing a single document
            # ------------------------------------------------------------------
            cfg.glob.start_time_document = time.perf_counter_ns()

            utils.start_document_processing(
                document=row,
            )

            parse_tetml_file_line()

            # Text and metadata from Document successfully extracted to xml format
            if not cfg.glob.setup.is_simulate_parser:
                duration_ns = utils.finalize_file_processing()

                if cfg.glob.setup.is_verbose:
                    utils.progress_msg(
                        f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                        f"Document: {cfg.glob.document_id:6d} "
                        f"[{db.dml.select_document_file_name_id(cfg.glob.document_id)}]"
                    )

        conn.close()

    with cfg.glob.db_orm_engine.connect() as conn:
        rows = db.dml.select_document(conn, dbt, cfg.glob.DOCUMENT_STEP_PARSER_WORD)

        for row in rows:
            cfg.glob.start_time_document = time.perf_counter_ns()

            utils.start_document_processing(
                document=row,
            )

            parse_tetml_file_word()

            # Text and metadata from Document successfully extracted to xml format
            if not cfg.glob.setup.is_simulate_parser:
                duration_ns = utils.finalize_file_processing()

                if cfg.glob.setup.is_verbose:
                    utils.progress_msg(
                        f"Duration: {round(duration_ns / 1000000000, 2):6.2f} s - "
                        f"Document: {cfg.glob.document_id:6d} "
                        f"[{db.dml.select_document_file_name_id(cfg.glob.document_id)}]"
                    )

        conn.close()

    utils.show_statistics_total()

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Parse the TETML file type line (step: s_f_p).
# -----------------------------------------------------------------------------
def parse_tetml_file_line() -> None:
    """Parse the TETML file type line.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    cfg.glob.document_current_step = cfg.glob.DOCUMENT_STEP_PARSER_LINE

    file_name = os.path.join(
        cfg.glob.document_directory_name,
        cfg.glob.document_file_name,
    )

    cfg.glob.setup.is_parsing_line = True
    cfg.glob.setup.is_parsing_word = False

    # Create the Element tree object
    tree = defusedxml.ElementTree.parse(file_name)

    # Get the root Element
    root = tree.getroot()

    for child in root:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_DOCUMENT:
                parse_tag_document(child_tag, child)
            case cfg.glob.PARSE_TAG_CREATION:
                pass

    if not cfg.glob.setup.is_simulate_parser:
        utils.delete_auxiliary_file(file_name)

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Parse the TETML file type word (step: s_f_p).
# -----------------------------------------------------------------------------
def parse_tetml_file_word() -> None:
    """Parse the TETML file type word.

    TBD
    """
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    cfg.glob.document_current_step = cfg.glob.DOCUMENT_STEP_PARSER_WORD

    file_name = os.path.join(
        cfg.glob.document_directory_name,
        cfg.glob.document_file_name,
    )

    cfg.glob.setup.is_parsing_line = False
    cfg.glob.setup.is_parsing_word = True

    # Create the Element tree object
    tree = defusedxml.ElementTree.parse(file_name)

    # Get the root Element
    root = tree.getroot()

    for child in root:
        child_tag = child.tag[cfg.glob.PARSE_TAG_FROM :]
        match child_tag:
            case cfg.glob.PARSE_TAG_DOCUMENT:
                parse_tag_document(child_tag, child)
            case cfg.glob.PARSE_TAG_CREATION:
                pass

    if not cfg.glob.setup.is_simulate_parser:
        utils.delete_auxiliary_file(file_name)

    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
