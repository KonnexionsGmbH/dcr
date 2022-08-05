import pathlib
import re

import dcr_core.cls_nlp_core

class LineTypeListBullet:
    Entry = dict[str, int | str]
    Entries = list[Entry]

    List = dict[str, Entries | float | int | str]
    Lists = list[List]

    def __init__(self) -> None:
        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = []
        self._bullet: str = ""
        self._entries: list[list[int]] = []
        self._environment_variant: str = ""
        self._exist: bool = False
        self._file_name_curr: str = ""
        self._line_lines_idx: int = 0
        self._lists: LineTypeListBullet.Lists = []
        self._llx_lower_limit: float = 0.0
        self._llx_upper_limit: float = 0.0
        self._no_entries: int = 0
        self._page_idx: int = 0
        self._page_idx_prev: int = 0
        self._para_no_prev: int = 0
        self._parser_line_lines_json: dcr_core.cls_nlp_core.NLPCore.ParserLineLines = []
        self._rules: dict[str, int] = {}
        self.no_lists: int = 0
        ...
    def _finish_list(self) -> None: ...
    def _init_anti_patterns(self) -> list[tuple[str, re.Pattern[str]]]: ...
    def _init_rules(self) -> dict[str, int]: ...
    @staticmethod
    def _load_anti_patterns_from_json(
        lt_list_bullet_rule_file: pathlib.Path,
    ) -> list[tuple[str, re.Pattern[str]]]: ...
    @staticmethod
    def _load_rules_from_json(
        lt_list_bullet_rule_file: pathlib.Path,
    ) -> dict[str, int]: ...
    def _process_line(self, line_line: dict[str, float | int | str]) -> None: ...
    def _process_page(self) -> None: ...
    def _reset_document(self) -> None: ...
    def _reset_list(self) -> None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        directory_name: str,
        document_id: int,
        environment_variant: str,
        file_name_curr: str,
        file_name_orig: str,
        parser_line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None: ...
