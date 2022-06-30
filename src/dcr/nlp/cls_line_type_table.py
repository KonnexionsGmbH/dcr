"""Module nlp.cls_line_type_table: Determine tables."""
from __future__ import annotations

import json

import cfg.glob
import db.cls_document
import nlp.cls_nlp_core
import nlp.cls_text_parser
import utils

# -----------------------------------------------------------------------------
# Global type aliases.
# -----------------------------------------------------------------------------
# {
#    "columnNo": 99,
#    "columnSpan": 99,
#    "coordLLX": 99.99,
#    "coordURX": 99.99,
#    "lineIndexPage": 99,
#    "lineIndexParagraph": 99,
#    "lineNo": 99,
#    "paragraphNo": 99,
#    "text": "..."
# },
Column = dict[str, float | int | object | str]
Columns = list[Column]

# {
#    "firstColumnLLX": 99.99,
#    "lastColumnURX": 99.99,
#    "noColumns": 99,
#    "rowNo": 99,
#    "columns": []
# },
Row = dict[str, Columns | float | int | str]
Rows = list[Row]

# {
#    "firstRowURX": 99.99,
#    "firstRowLLX": 99.99,
#    "noColumns": 99,
#    "noRows": 99,
#    "pageNoFrom": 99,
#    "pageNoTill": 99,
#    "rows": []
# },
Table = dict[str, float | int | Rows]
Tables = list[Table]


# pylint: disable=too-many-instance-attributes
class LineTypeTable:
    """Determine table of content lines.

    Returns:
        _type_: LineTypeTable instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.check_exists_object(
            is_action_curr=True,
            is_document=True,
            is_setup=True,
            is_text_parser=True,
        )

        utils.progress_msg_line_type_table("LineTypeTable")
        utils.progress_msg_line_type_table(
            f"LineTypeTable: Start create instance                ={cfg.glob.action_curr.action_file_name}"
        )

        self._column_no = 0
        self._column_no_prev = 0
        self._columns: Columns = []

        self._first_column_llx = 0.0
        self._first_row_llx = 0.0
        self._first_row_urx = 0.0

        self._is_table_open = False

        self._last_column_urx = 0.0

        self._max_page = 0

        self._no_columns_table = 0
        self._no_rows = 0

        self._page_idx = 0
        self._page_no_from = 0
        self._page_no_till = 0

        self._row_no = 0
        self._row_no_prev = 0
        self._rows: Rows = []

        self.tables: Tables = []

        self._exist = True

        utils.progress_msg_line_type_table(
            f"LineTypeTable: End   create instance                ={cfg.glob.action_curr.action_file_name}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finish a row.
    # -----------------------------------------------------------------------------
    def _finish_row(self) -> None:
        """Finish a row."""
        if (no_columns := len(self._columns)) == 0:
            return

        self._no_columns_table += no_columns
        row_no = len(self._rows) + 1

        self._rows.append(
            {
                nlp.cls_nlp_core.NLPCore.JSON_NAME_FIRST_COLUMN_LLX: self._first_column_llx,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_LAST_COLUMN_URX: self._last_column_urx,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_COLUMNS: no_columns,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO: row_no,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMNS: self._columns,
            }
        )

        self._reset_row()

        utils.progress_msg_line_type_table(f"LineTypeTable: End   row                            ={row_no}")

    # -----------------------------------------------------------------------------
    # Finish a table.
    # -----------------------------------------------------------------------------
    def _finish_table(self) -> None:
        """Finish a table."""
        if not (self._is_table_open and cfg.glob.setup.is_create_extra_file_table):
            return

        self._finish_row()

        self._page_no_till = self._page_idx + 1

        self.tables.append(
            {
                nlp.cls_nlp_core.NLPCore.JSON_NAME_FIRST_ROW_LLX: self._first_row_llx,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_FIRST_ROW_URX: self._first_row_urx,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_COLUMNS: self._no_columns_table,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_ROWS: len(self._rows),
                nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_FROM: self._page_no_from,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_TILL: self._page_no_till,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_TABLE_NO: len(self.tables) + 1,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_ROWS: self._rows,
            }
        )

        self._reset_table()

        utils.progress_msg_line_type_table(f"LineTypeTable: End   table                   on page={self._page_idx+1}")

    # -----------------------------------------------------------------------------
    # Process the line-related data.
    # -----------------------------------------------------------------------------
    def _process_line(self, line_line: dict[str, str]) -> str:  # noqa: C901
        """Process the line-related data.

        Args:
            line_line (dict[str, str]): The line to be processed.

        Returns:
            str: The new or the old line type.
        """
        if nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO not in line_line:
            return db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY

        if not cfg.glob.setup.is_create_extra_file_table:
            return db.cls_document.Document.DOCUMENT_LINE_TYPE_TABLE

        self._column_no = int(line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO])
        self._row_no = int(line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO])

        if not self._is_table_open:
            self._reset_table()
        elif self._row_no < self._row_no_prev:
            self._finish_table()
        elif self._row_no != self._row_no_prev:
            self._finish_row()

        text = line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT]

        if text == "" and not cfg.glob.setup.is_lt_table_file_incl_empty_columns:
            return db.cls_document.Document.DOCUMENT_LINE_TYPE_TABLE

        coord_llx = float(line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX])
        coord_urx = float(line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX])

        if self._page_no_from == 0:
            self._page_no_from = self._page_idx + 1

        if self._row_no == 1:
            if self._column_no_prev == 0:
                self._first_row_llx = coord_llx
            self._first_row_urx = coord_urx

        if self._column_no_prev == 0:
            self._first_column_llx = coord_llx
        self._last_column_urx = coord_urx

        new_entry = {
            nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO: line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO],
            nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX: coord_llx,
            nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX: coord_urx,
            nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_INDEX_PAGE: line_line[
                nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_INDEX_PAGE
            ],
            nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_INDEX_PARA: line_line[
                nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_INDEX_PARA
            ],
            nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO: line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO],
            nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO],
            nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT: text,
        }

        if nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN in line_line:
            new_entry[nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN] = line_line[
                nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN
            ]

        self._columns.append(new_entry)

        self._is_table_open = True
        self._column_no_prev = self._column_no
        self._row_no_prev = self._row_no

        return db.cls_document.Document.DOCUMENT_LINE_TYPE_TABLE

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._max_line_line = len(cfg.glob.text_parser.parse_result_line_lines)

        for line_lines_idx, line_line in enumerate(cfg.glob.text_parser.parse_result_line_lines):
            if line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] != db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY:
                continue

            if self._process_line(line_line) == db.cls_document.Document.DOCUMENT_LINE_TYPE_TABLE:
                line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = db.cls_document.Document.DOCUMENT_LINE_TYPE_TABLE
                cfg.glob.text_parser.parse_result_line_lines[line_lines_idx] = line_line
            else:
                self._finish_table()

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Reset the document memory.
    # -----------------------------------------------------------------------------
    def _reset_document(self) -> None:
        """Reset the document memory."""
        self._max_page = cfg.glob.text_parser.parse_result_no_pages_in_doc

        self.tables = []

        utils.progress_msg_line_type_table("LineTypeTable: Reset the document memory")

        self._reset_table()

    # -----------------------------------------------------------------------------
    # Reset the row memory.
    # -----------------------------------------------------------------------------
    def _reset_row(self) -> None:
        """Reset the row memory."""
        self._column_no_prev = 0
        self._columns = []

        self._first_column_llx = 0.0
        self._last_column_urx = 0.0

        utils.progress_msg_line_type_table("LineTypeTable: Reset the row memory")

    # -----------------------------------------------------------------------------
    # Reset the table memory.
    # -----------------------------------------------------------------------------
    def _reset_table(self) -> None:
        """Reset the table memory."""
        self._first_row_llx = 0.0
        self._first_row_urx = 0.0

        self._is_table_open = False

        self._no_columns_table = 0

        self._page_no_from = 0
        self._page_no_till = 0

        self._row_no_prev = 0
        self._rows = []

        utils.progress_msg_line_type_table("LineTypeTable: Reset the table memory")

        self._reset_row()

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
    # Process the document related data.
    # -----------------------------------------------------------------------------
    def process_document(self) -> None:
        """Process the document related data."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.progress_msg_line_type_table("LineTypeTable")
        utils.progress_msg_line_type_table(
            f"LineTypeTable: Start document                       ={cfg.glob.action_curr.action_file_name}"
        )

        self._reset_document()

        for page_idx, page in enumerate(cfg.glob.text_parser.parse_result_line_pages):
            self._page_idx = page_idx
            cfg.glob.text_parser.parse_result_line_lines = page[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        if cfg.glob.setup.is_create_extra_file_table and self.tables:
            full_name_toc = utils.get_full_name(
                cfg.glob.action_curr.action_directory_name,
                cfg.glob.action_curr.get_stem_name()  # type: ignore
                + "_table."
                + db.cls_document.Document.DOCUMENT_FILE_TYPE_JSON,
            )
            with open(full_name_toc, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    {
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: cfg.glob.document.document_id,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: cfg.glob.document.document_file_name,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TABLES_IN_DOC: len(self.tables),
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_TABLES: self.tables,
                    },
                    file_handle,
                    indent=cfg.glob.setup.json_indent,
                    sort_keys=cfg.glob.setup.is_json_sort_keys,
                )

        utils.progress_msg_line_type_table(
            f"LineTypeTable: End   document                       ={cfg.glob.action_curr.action_file_name}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)