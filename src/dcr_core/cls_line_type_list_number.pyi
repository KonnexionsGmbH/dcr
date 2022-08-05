import collections
import pathlib
import re

import dcr_core.cls_nlp_core

class LineTypeListNumber:
    Entry = dict[str, int | str]
    Entries = list[Entry]

    List = dict[str, Entries | float | int | object | str]
    Lists = list[List]

    RuleExtern = tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]
    RuleIntern = tuple[str, re.Pattern[str], collections.abc.Callable[[str, str], bool], list[str], str]

    def __init__(self) -> None:
        self._RULE_NAME_SIZE: int = 0
        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = []
        self._entries: list[list[int | str]] = []
        self._environment_variant: str = ""
        self._exist: bool = False
        self._line_lines_idx: int = 0
        self._lists: LineTypeListNumber.Lists = []
        self._llx_lower_limit: float = 0.0
        self._llx_upper_limit: float = 0.0
        self._no_entries: int = 0
        self._page_idx: int = 0
        self._page_idx_prev: int = 0
        self._para_no_prev: int = 0
        self._parser_line_lines_json: dcr_core.cls_nlp_core.NLPCore.ParserLineLines = []
        self._parser_line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages = []
        self._rule: LineTypeListNumber.RuleIntern = ()  # type: ignore
        self._rules: list[LineTypeListNumber.RuleExtern] = []
        self._rules_collection: list[LineTypeListNumber.RuleIntern] = []
        self.file_name_curr: str = ""
        self.no_lists: int = 0
        ...
    def _finish_list(self) -> None: ...
    def _init_anti_patterns(self) -> list[tuple[str, re.Pattern[str]]]: ...
    def _init_rules(self) -> list[LineTypeListNumber.RuleExtern]: ...
    @staticmethod
    def _load_anti_patterns_from_json(
        lt_list_number_rule_file: pathlib.Path,
    ) -> list[tuple[str, re.Pattern[str]]]: ...
    @staticmethod
    def _load_rules_from_json(
        lt_list_number_rule_file: pathlib.Path,
    ) -> list[LineTypeListNumber.RuleExtern]: ...
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
