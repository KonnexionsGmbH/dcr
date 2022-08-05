import collections
import pathlib
import re

import dcr_core.cls_nlp_core

class LineTypeHeading:
    def __init__(self) -> None:
        self._RULE_NAME_SIZE: int = 0
        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = []
        self._exist: bool = False
        self._level_prev = None
        self._line_lines_idx: int = 0
        self._max_page: int = 0
        self._page_idx: int = 0
        self._rules: list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]] = []
        self._rules_collection: list[tuple[str, bool, re.Pattern[str], collections.abc.Callable[[str, str], bool], list[str], str]] = []
        self._rules_hierarchy: list[
            tuple[
                str,
                bool,
                re.Pattern[str],
                collections.abc.Callable[[str, str], bool],
                list[str],
                int,
                str,
                str,
                str,
            ]
        ] = []
        self._toc: list[dict[str, int | object | str]] = []
        self.file_name_curr: str = ""
        ...
    @staticmethod
    def _check_valid_start_value(target_value: str, is_first_token: bool, start_values: list[str]) -> bool: ...
    def _create_toc_entry(self, level: int, text: str) -> None: ...
    def _get_next_body_line(
        self, page_idx: int, line_lines: dcr_core.cls_nlp_core.NLPCore.ParserLineLines, line_lines_idx: int
    ) -> tuple[str, int, dcr_core.cls_nlp_core.NLPCore.ParserLineLines, int]: ...
    def _init_anti_patterns(self) -> list[tuple[str, re.Pattern[str]]]: ...
    def _init_rules(self) -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]: ...
    @staticmethod
    def _load_anti_patterns_from_json(
        lt_heading_rule_file: pathlib.Path,
    ) -> list[tuple[str, re.Pattern[str]]]: ...
    @staticmethod
    def _load_rules_from_json(
        lt_heading_rule_file: pathlib.Path,
    ) -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]: ...
    def _process_line(self, line_line: dict[str, str], text: str, first_token: str) -> int: ...
    def _process_page(self) -> None: ...
    def exists(self) -> bool: ...
    def process_document(
        self,
        directory_name: str,
        document_id: int,
        file_name_curr: str,
        file_name_orig: str,
        parser_line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None: ...
