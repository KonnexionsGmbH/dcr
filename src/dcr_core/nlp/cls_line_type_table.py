"""Module nlp.cls_line_type_table: Determine tables."""
from __future__ import annotations

import json

import dcr_core.cfg.glob
import dcr_core.nlp.cls_nlp_core
import dcr_core.utils


# pylint: disable=too-many-instance-attributes
class LineTypeTable:
    """Determine table of content lines.

    Returns:
        _type_: LineTypeTable instance.
    """

    Column = dict[str, float | int | object | str]
    Columns = list[Column]

    Row = dict[str, Columns | float | int | str]
    Rows = list[Row]

    Table = dict[str, float | int | Rows]
    Tables = list[Table]

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(
        self,
        action_file_name: str,
        is_verbose_lt: bool,
    ) -> None:
        """Initialise the instance.

        Args:
            action_file_name (str):
                    File name of the file to be processed.
            is_verbose_lt (bool):
                    If true, processing results are reported. Defaults to False.
        """
        dcr_core.utils.check_exists_object(
            is_text_parser=True,
        )

        self._action_file_name = action_file_name
        self._is_lt_table_file_incl_empty_columns = False
        self._is_verbose_lt = is_verbose_lt

        dcr_core.utils.progress_msg(self._is_verbose_lt, "LineTypeTable")
        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeTable: Start create instance                ={self._action_file_name}")

        self._column_no = 0
        self._column_no_prev = 0
        self._columns: LineTypeTable.Columns = []

        self._first_column_llx = 0.0
        self._first_row_llx = 0.0
        self._first_row_urx = 0.0

        self._is_table_open = False

        self._last_column_urx = 0.0

        self._no_columns_table = 0
        self._no_rows = 0

        self._page_idx = 0
        self._page_no_from = 0
        self._page_no_till = 0

        self._parser_line_lines_json: dcr_core.nlp.cls_nlp_core.NLPCore.ParserLineLines = []

        self._row_no = 0
        self._row_no_prev = 0
        self._rows: LineTypeTable.Rows = []

        self._tables: LineTypeTable.Tables = []

        self.no_tables = 0

        self._exist = True

        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeTable: End   create instance                ={self._action_file_name}")

    # -----------------------------------------------------------------------------
    # Finish a row.
    # -----------------------------------------------------------------------------
    def _finish_row(self) -> None:
        """Finish a row."""
        if (no_columns := len(self._columns)) == 0:
            return

        self._no_columns_table += no_columns
        row_no = len(self._rows) + 1

        # {
        #    "firstColumnLLX": 99.99,
        #    "lastColumnURX": 99.99,
        #    "noColumns": 99,
        #    "rowNo": 99,
        #    "columns": []
        # },
        self._rows.append(
            {
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_FIRST_COLUMN_LLX: self._first_column_llx,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LAST_COLUMN_URX: self._last_column_urx,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_COLUMNS: no_columns,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO: row_no,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMNS: self._columns,
            }
        )

        self._reset_row()

        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeTable: End   row                            ={row_no}")

    # -----------------------------------------------------------------------------
    # Finish a table.
    # -----------------------------------------------------------------------------
    def _finish_table(self) -> None:
        """Finish a table."""
        if not self._is_table_open:
            return

        self._finish_row()

        self.no_tables += 1
        self._page_no_till = self._page_idx + 1

        # {
        #    "firstRowLLX": 99.99,
        #    "firstRowURX": 99.99,
        #    "noColumns": 99,
        #    "noRows": 99,
        #    "pageNoFrom": 99,
        #    "pageNoTill": 99,
        #    "tableNo": 99,
        #    "rows": []
        # },
        self._tables.append(
            {
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_FIRST_ROW_LLX: self._first_row_llx,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_FIRST_ROW_URX: self._first_row_urx,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_COLUMNS: self._no_columns_table,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_ROWS: len(self._rows),
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_FROM: self._page_no_from,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_TILL: self._page_no_till,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TABLE_NO: self.no_tables,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROWS: self._rows,
            }
        )

        self._reset_table()

        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeTable: End   table                   on page={self._page_idx+1}")

    # -----------------------------------------------------------------------------
    # Process the line-related data.
    # -----------------------------------------------------------------------------
    def _process_line(self, line_line: dict[str, int | str]) -> str:  # noqa: C901
        """Process the line-related data.

        Args:
            line_line (dict[str, str]):
                    The line to be processed.

        Returns:
            str:    The new or the old line type.
        """
        if dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO not in line_line:
            return dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_BODY

        self._column_no = int(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO])
        self._row_no = int(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO])

        if not self._is_table_open:
            self._reset_table()
        elif self._row_no < self._row_no_prev:
            self._finish_table()
        elif self._row_no != self._row_no_prev:
            self._finish_row()

        text = line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT]

        if text == "" and not self._is_lt_table_file_incl_empty_columns:
            return dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_TABLE

        coord_llx = float(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX])
        coord_urx = float(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX])

        if self._page_no_from == 0:
            self._page_no_from = self._page_idx + 1

        if self._row_no == 1:
            if self._column_no_prev == 0:
                self._first_row_llx = coord_llx
            self._first_row_urx = coord_urx

        if self._column_no_prev == 0:
            self._first_column_llx = coord_llx
        self._last_column_urx = coord_urx

        # {
        #     "columnNo": 99,
        #     "coordLLX": 99.9,
        #     "coordURX": 99.9,
        #     "lineNo": 99,
        #     "lineNoPage": 99,
        #     "paragraphNo": 99,
        #     "text": "xxx"
        # }
        new_entry = {
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO: line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_NO],
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX: coord_llx,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_URX: coord_urx,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO: line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO],
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE: line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE],
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO],
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT: text,
        }

        if dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN in line_line:
            new_entry[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN] = line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COLUMN_SPAN]

        self._columns.append(new_entry)

        self._is_table_open = True
        self._column_no_prev = self._column_no
        self._row_no_prev = self._row_no

        return dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_TABLE

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        self._max_line_line = len(self._parser_line_lines_json)

        for line_lines_idx, line_line in enumerate(self._parser_line_lines_json):
            if line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] != dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                continue

            if self._process_line(line_line) == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_TABLE:
                line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_TABLE
                self._parser_line_lines_json[line_lines_idx] = line_line
            else:
                self._finish_table()

    # -----------------------------------------------------------------------------
    # Reset the document memory.
    # -----------------------------------------------------------------------------
    def _reset_document(self) -> None:
        """Reset the document memory."""
        self.no_tables = 0

        self._tables = []

        self.table_no = 0

        dcr_core.utils.progress_msg(self._is_verbose_lt, "LineTypeTable: Reset the document memory")

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

        dcr_core.utils.progress_msg(self._is_verbose_lt, "LineTypeTable: Reset the row memory")

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

        self.table_no = 0

        dcr_core.utils.progress_msg(self._is_verbose_lt, "LineTypeTable: Reset the table memory")

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
    def process_document(  # pylint: disable=too-many-arguments
        self,
        action_file_name: str,
        directory_name: str,
        document_document_id: int,
        document_file_name: str,
        file_encoding: str,
        file_name: str,
        is_create_extra_file_table: bool,
        is_json_sort_keys: bool,
        is_lt_table_file_incl_empty_columns: bool,
        json_indent: str,
        parser_line_pages_json: dcr_core.nlp.cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None:
        """Process the document related data.

        Args:
            action_file_name (str):
                    File name of the file to be processed.
            directory_name (str):
                    Directory name of the output file.
            document_document_id (int):
                    Identification of the document.
            document_file_name (in):
                    File name of the document file.
            file_encoding (str):
                    The encoding of the output file.
            file_name (str):
                    File name of the output file.
            is_create_extra_file_table (bool):
                    Create a separate JSON file with the tables.
            is_json_sort_keys (bool):
                    If true, the output of the JSON dictionaries will be sorted by key.
            is_lt_table_file_incl_empty_columns (bool):
                    If true, the empty cells are included in the separate JSON file with the tables.
            json_indent (str):
                    Indent level for pretty-printing the JSON output.
            parser_line_pages_json (dcr_core.nlp.cls_nlp_core.NLPCore.LinePages):
                    The document pages formatted in the parser.
        """
        self._action_file_name = action_file_name
        self._is_lt_table_file_incl_empty_columns = is_lt_table_file_incl_empty_columns

        dcr_core.utils.progress_msg(self._is_verbose_lt, "LineTypeTable")
        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeTable: Start document                       ={self._action_file_name}")

        self._reset_document()

        for page_idx, page_json in enumerate(parser_line_pages_json):
            self._page_idx = page_idx
            self._parser_line_lines_json = page_json[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        if is_create_extra_file_table and self._tables:
            full_name = dcr_core.utils.get_full_name(
                directory_name,
                dcr_core.utils.get_stem_name(str(file_name)) + "_table." + dcr_core.cfg.glob.FILE_TYPE_JSON,
            )
            with open(full_name, "w", encoding=file_encoding) as file_handle:
                # {
                #     "documentId": 99,
                #     "documentFileName": "xxx",
                #     "noTablesInDocument": 99,
                #     "tables": [
                #     ]
                # }
                json.dump(
                    {
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: document_document_id,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: document_file_name,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_TABLES_IN_DOC: self.no_tables,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TABLES: self._tables,
                    },
                    file_handle,
                    indent=json_indent,
                    sort_keys=is_json_sort_keys,
                )

        if self.no_tables > 0:
            dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeTable:                         number tables={self.no_tables}")

        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeTable: End   document                       ={self._action_file_name}")
