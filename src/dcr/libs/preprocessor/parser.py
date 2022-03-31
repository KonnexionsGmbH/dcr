"""Module libs.preprocessor.parser: Store the document structure from the
parser result."""
import os
import time
from datetime import datetime
from typing import Iterable

import defusedxml.ElementTree
import libs.cfg
import libs.db.cfg
import libs.db.orm
import libs.utils


# -----------------------------------------------------------------------------
# Initialize the parse result variables.
# -----------------------------------------------------------------------------
def init_parse_result() -> None:
    """Initialize the parse result variables."""
    libs.cfg.parse_result_author = None
    libs.cfg.parse_result_creation_date = None
    libs.cfg.parse_result_mod_date = None
    libs.cfg.parse_result_page_in_document = 0


# -----------------------------------------------------------------------------
# Processing tag Box.
# -----------------------------------------------------------------------------
def parse_tag_box(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Box'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    libs.utils.debug_xml_element(parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_A:
                pass
            case libs.cfg.PARSE_TAG_LINE:
                parse_tag_line(child_tag, child)
            case _:
                libs.utils.report_document_error(
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                    error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag).replace(
                        "{parent_tag}", parent_tag
                    ),
                )


# -----------------------------------------------------------------------------
# Processing tag 'Content'.
# -----------------------------------------------------------------------------
def parse_tag_content(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Content'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    libs.utils.debug_xml_element(parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_PARA:
                parse_tag_para(child_tag, child)
            case libs.cfg.PARSE_TAG_PLACED_IMAGE | libs.cfg.PARSE_TAG_TABLE:
                pass
            case _:
                libs.utils.report_document_error(
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                    error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag).replace(
                        "{parent_tag}", parent_tag
                    ),
                )


# -----------------------------------------------------------------------------
# Processing tag 'DocInfo'.
# -----------------------------------------------------------------------------
def parse_tag_doc_info(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'DocInfo'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    libs.utils.debug_xml_element(parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_AUTHOR:
                libs.cfg.parse_result_author = child.text
            case libs.cfg.PARSE_TAG_CREATION_DATE:
                libs.cfg.parse_result_creation_date = datetime.strptime(
                    child.text, "%Y-%m-%dT%H:%M:%S%z"
                )
            case libs.cfg.PARSE_TAG_CREATOR | libs.cfg.PARSE_TAG_PRODUCER:
                pass
            case libs.cfg.PARSE_TAG_CUSTOM | libs.cfg.PARSE_TAG_TITLE:
                pass
            case libs.cfg.PARSE_TAG_MOD_DATE:
                libs.cfg.parse_result_mod_date = datetime.strptime(
                    child.text, "%Y-%m-%dT%H:%M:%S%z"
                )
            case _:
                libs.utils.report_document_error(
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                    error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag).replace(
                        "{parent_tag}", parent_tag
                    ),
                )


# -----------------------------------------------------------------------------
# Processing tag 'Document'.
# -----------------------------------------------------------------------------
def parse_tag_document(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Document'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    libs.utils.debug_xml_element(parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_BOOKMARKS | libs.cfg.PARSE_TAG_DESTINATIONS:
                pass
            case libs.cfg.PARSE_TAG_DOC_INFO:
                parse_tag_doc_info(child_tag, child)
            case libs.cfg.PARSE_TAG_METADATA | libs.cfg.PARSE_TAG_OPTIONS:
                pass
            case libs.cfg.PARSE_TAG_PAGES:
                parse_tag_pages(child_tag, child)
            case _:
                libs.utils.report_document_error(
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                    error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag).replace(
                        "{parent_tag}", parent_tag
                    ),
                )


# -----------------------------------------------------------------------------
# Processing tag Line.
# -----------------------------------------------------------------------------
def parse_tag_line(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Line'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    libs.utils.debug_xml_element(parent_tag, parent.attrib, parent.text)

    libs.cfg.parse_result_line_in_para += 1
    libs.cfg.parse_result_token_in_line = 0

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_A:
                pass
            case libs.cfg.PARSE_TAG_WORD:
                parse_tag_word(child_tag, child)
            case _:
                libs.utils.report_document_error(
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                    error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag).replace(
                        "{parent_tag}", parent_tag
                    ),
                )


# -----------------------------------------------------------------------------
# Processing tag 'Page'.
# -----------------------------------------------------------------------------
def parse_tag_page(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Page'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    libs.utils.debug_xml_element(parent_tag, parent.attrib, parent.text)

    libs.cfg.parse_result_page_in_document = int(parent.attrib["number"])
    libs.cfg.parse_result_para_in_page = 0

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_ANNOTATIONS:
                pass
            case libs.cfg.PARSE_TAG_CONTENT:
                parse_tag_content(child_tag, child)
            case libs.cfg.PARSE_TAG_OPTIONS:
                pass
            case _:
                libs.utils.report_document_error(
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                    error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag).replace(
                        "{parent_tag}", parent_tag
                    ),
                )


# -----------------------------------------------------------------------------
# Processing tag 'Pages'.
# -----------------------------------------------------------------------------
def parse_tag_pages(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Pages'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    libs.utils.debug_xml_element(parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_GRAPHICS | libs.cfg.PARSE_TAG_RESOURCES:
                pass
            case libs.cfg.PARSE_TAG_PAGE:
                parse_tag_page(child_tag, child)
            case _:
                libs.utils.report_document_error(
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                    error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag).replace(
                        "{parent_tag}", parent_tag
                    ),
                )


# -----------------------------------------------------------------------------
# Processing tag Para.
# -----------------------------------------------------------------------------
def parse_tag_para(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Para'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    libs.utils.debug_xml_element(parent_tag, parent.attrib, parent.text)

    libs.cfg.parse_result_line_in_para = 0
    libs.cfg.parse_result_para_in_page += 1
    libs.cfg.parse_result_sentence_in_para = 1
    libs.cfg.parse_result_token_in_sentence = 0

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_A:
                pass
            case libs.cfg.PARSE_TAG_BOX:
                parse_tag_box(child_tag, child)
            case _:
                libs.utils.report_document_error(
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                    error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag).replace(
                        "{parent_tag}", parent_tag
                    ),
                )


# -----------------------------------------------------------------------------
# Processing tag Text.
# -----------------------------------------------------------------------------
def parse_tag_text(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Text'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    libs.utils.debug_xml_element(parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case _:
                libs.utils.report_document_error(
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                    error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag).replace(
                        "{parent_tag}", parent_tag
                    ),
                )

    if parent.text is None:
        libs.utils.report_document_error(
            error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
            error=libs.db.cfg.ERROR_61_903.replace("{document_id}", str(libs.cfg.document_id_base))
            .replace("{page_no}", str(libs.cfg.parse_result_page_in_document))
            .replace("{para_no}", str(libs.cfg.parse_result_para_in_page))
            .replace("{line_no}", str(libs.cfg.parse_result_token_in_line)),
        )
    else:
        libs.cfg.parse_result_token_in_line += 1
        libs.cfg.parse_result_token_in_sentence += 1

        libs.cfg.logger.debug(
            "doc=%5d page=%2d para=%2d line=%2d tkn_lin=%2d sentence=%2d tkn_sen=%2d tkn='%s'",
            libs.cfg.document_id_base,
            libs.cfg.parse_result_page_in_document,
            libs.cfg.parse_result_para_in_page,
            libs.cfg.parse_result_line_in_para,
            libs.cfg.parse_result_token_in_line,
            libs.cfg.parse_result_sentence_in_para,
            libs.cfg.parse_result_token_in_sentence,
            parent.text,
        )

        libs.db.orm.insert_dbt_row(
            libs.db.cfg.DBT_CONTENT,
            {
                libs.db.cfg.DBC_DOCUMENT_ID: libs.cfg.document_id_base,
                libs.db.cfg.DBC_PAGE_IN_DOCUMENT: libs.cfg.parse_result_page_in_document,
                libs.db.cfg.DBC_PARA_IN_PAGE: libs.cfg.parse_result_para_in_page,
                libs.db.cfg.DBC_LINE_IN_PARA: libs.cfg.parse_result_line_in_para,
                libs.db.cfg.DBC_TOKEN_IN_LINE: libs.cfg.parse_result_token_in_line,
                libs.db.cfg.DBC_SENTENCE_IN_PARA: libs.cfg.parse_result_sentence_in_para,
                libs.db.cfg.DBC_TOKEN_IN_SENTENCE: libs.cfg.parse_result_token_in_sentence,
                libs.db.cfg.DBC_TOKEN_PARSED: parent.text,
            },
        )

        if parent.text == ".":
            libs.cfg.parse_result_sentence_in_para += 1
            libs.cfg.parse_result_token_in_sentence = 0


# -----------------------------------------------------------------------------
# Processing tag Word.
# -----------------------------------------------------------------------------
def parse_tag_word(parent_tag: str, parent: Iterable[str]) -> None:
    """Processing tag 'Word'.

    Args:
        parent_tag (str): Parent tag.
        parent (Iterable[str): Parent data structure.
    """
    libs.utils.debug_xml_element(parent_tag, parent.attrib, parent.text)

    for child in parent:
        child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
        match child_tag:
            case libs.cfg.PARSE_TAG_BOX:
                pass
            case libs.cfg.PARSE_TAG_TEXT:
                parse_tag_text(child_tag, child)
            case _:
                libs.utils.report_document_error(
                    error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                    error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag).replace(
                        "{parent_tag}", parent_tag
                    ),
                )


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
        rows = libs.utils.select_document(conn, dbt, libs.db.cfg.DOCUMENT_NEXT_STEP_PARSER)

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

    # Create the Element tree object
    tree = defusedxml.ElementTree.parse(file_name)

    # Get the root Element
    root = tree.getroot()

    parent_tag = root.tag[libs.cfg.PARSE_TAG_FROM :]

    libs.utils.debug_xml_element(parent_tag, root.attrib, root.text)

    if parent_tag != libs.cfg.PARSE_TAG_TET:
        libs.utils.report_document_error(
            error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
            error=libs.db.cfg.ERROR_61_902.replace(
                "{expected_tag}", libs.cfg.PARSE_TAG_TET
            ).replace("{found_tag}", parent_tag),
        )
    else:
        for child in root:
            child_tag = child.tag[libs.cfg.PARSE_TAG_FROM :]
            libs.utils.debug_xml_element(child_tag, child.attrib, child.text)
            match child_tag:
                case libs.cfg.PARSE_TAG_DOCUMENT:
                    parse_tag_document(child_tag, child)
                case libs.cfg.PARSE_TAG_CREATION:
                    pass
                case _:
                    libs.utils.report_document_error(
                        error_code=libs.db.cfg.DOCUMENT_ERROR_CODE_REJ_PARSER,
                        error=libs.db.cfg.ERROR_61_901.replace("{child_tag}", child_tag),
                    )

        libs.utils.delete_auxiliary_file(file_name)

        # Text and metadata from Document successfully extracted to xml format
        libs.utils.finalize_file_processing()

    libs.cfg.logger.debug(libs.cfg.LOGGER_END)
