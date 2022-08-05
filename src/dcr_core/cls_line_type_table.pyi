import dcr_core.cls_nlp_core

class LineTypeTable:
    Column = dict[str, float | int | object | str]
    Columns = list[Column]

    Row = dict[str, Columns | float | int | str]
    Rows = list[Row]

    Table = dict[str, float | int | Rows]
    Tables = list[Table]

    def __init__(self) -> None:
        self._column_no: int = 0
        self._column_no_prev: int = 0
        self._columns: LineTypeTable.Columns = []
        self._exist: bool = False
        self._file_name_curr: str = ""
        self._first_column_llx: float = 0.0
        self._first_row_llx: float = 0.0
        self._first_row_urx: float = 0.0
        self._is_table_open: int = 0
        self._last_column_urx: int = 0
        self._no_columns_table: int = 0
        self._page_idx: int = 0
        self._page_no_from: int = 0
        self._page_no_till: int = 0
        self._parser_line_lines_json: dcr_core.cls_nlp_core.NLPCore.ParserLineLines = []
        self._row_no: int = 0
        self._row_no_prev: int = 0
        self._rows: LineTypeTable.Rows = []
        self._tables: LineTypeTable.Tables = []
        self.no_tables: int = 0
        ...
    def _finish_row(self) -> None: ...
    def _finish_table(self) -> None: ...
    def _process_line(self, line_line: dict[str, int | str]) -> str: ...
    def _process_page(self) -> None: ...
    def _reset_document(self) -> None: ...
    def _reset_row(self) -> None: ...
    def _reset_table(self) -> None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        directory_name: str,
        document_id: int,
        file_name_curr: str,
        file_name_orig: str,
        parser_line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None: ...
