"""Module nlp.cls_line_type_list_number: Determine numbered lists."""
from __future__ import annotations

import collections
import json
import os
import pathlib
import re

import cfg.glob
import db.cls_document
import utils

import dcr_core.cfg.glob
import dcr_core.nlp.cls_nlp_core
import dcr_core.utils

# -----------------------------------------------------------------------------
# Global type aliases.
# -----------------------------------------------------------------------------
Entry = dict[str, int | str]
Entries = list[Entry]

List = dict[str, Entries | float | int | object | str]
Lists = list[List]

RuleExtern = tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]
RuleIntern = tuple[str, re.Pattern[str], collections.abc.Callable[[str, str], bool], list[str], str]


# pylint: disable=too-many-instance-attributes
class LineTypeListNumber:
    """Determine list of numbered lines.

    Returns:
        _type_: LineTypeListNumber instance.
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
        )

        dcr_core.utils.check_exists_object(
            is_text_parser=True,
        )

        utils.progress_msg_line_type_list_number("LineTypeListNumber")
        utils.progress_msg_line_type_list_number(f"LineTypeListNumber: Start create instance                ={cfg.glob.action_curr.action_file_name}")

        self._RULE_NAME_SIZE: int = 20

        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = self._init_anti_patterns()

        # page_idx, para_no, line_lines_idx_from, line_lines_idx_till, target_value
        self._entries: list[list[int | str]] = []

        self._line_lines_idx = -1

        self._lists: Lists = []

        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._no_entries = 0

        self._page_idx = -1
        self._page_idx_prev = -1

        self._para_no = 0
        self._para_no_prev = 0

        self._rule: RuleIntern = ()  # type: ignore

        self._rules: list[RuleExtern] = self._init_rules()

        # -----------------------------------------------------------------------------
        # Number rules collection.
        # -----------------------------------------------------------------------------
        # 1: rule_name
        # 2: regexp_compiled:
        #           compiled regular expression
        # 3: function_is_asc:
        #           compares predecessor and successor
        # 4: start_values:
        #           list of strings
        # 5: regexp_str:
        #           regular expression
        # -----------------------------------------------------------------------------
        self._rules_collection: list[RuleIntern] = []

        for (rule_name, regexp_str, function_is_asc, start_values) in self._rules:
            self._rules_collection.append(
                (
                    rule_name.ljust(self._RULE_NAME_SIZE),
                    re.compile(regexp_str),
                    function_is_asc,
                    start_values,
                    regexp_str,
                )
            )

        self.no_lists = 0

        self._exist = True

        utils.progress_msg_line_type_list_number(f"LineTypeListNumber: End   create instance                ={cfg.glob.action_curr.action_file_name}")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finish a list.
    # -----------------------------------------------------------------------------
    def _finish_list(self) -> None:
        """Finish a list."""
        if self._no_entries == 0:
            return

        if self._no_entries < cfg.glob.setup.lt_list_number_min_entries:
            utils.progress_msg_line_type_list_number(
                f"LineTypeListNumber: Not enough list entries    found only={self._no_entries} - "
                + f"number='{self._rule[0]}' - entries={self._entries}"
            )
            self._reset_list()
            return

        utils.progress_msg_line_type_list_number(
            f"LineTypeListNumber: List entries                    found={self._no_entries} - " + f"number='{self._rule[0]}' - entries={self._entries}"
        )

        self.no_lists += 1

        entries: Entries = []

        for [page_idx, para_no, line_lines_idx_from, line_lines_idx_till, _] in self._entries:
            line_lines: dcr_core.nlp.cls_nlp_core.NLPCore.LineLines = dcr_core.cfg.glob.text_parser.parse_result_line_pages[page_idx][
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES
            ]

            text = []

            for idx in range(int(line_lines_idx_from), int(line_lines_idx_till) + 1):
                line_lines[idx][dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = db.cls_document.Document.DOCUMENT_LINE_TYPE_LIST_NUMBER

                if cfg.glob.setup.is_create_extra_file_list_number:
                    text.append(line_lines[idx][dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

            if cfg.glob.setup.is_create_extra_file_list_number:
                # {
                #     "entryNo": 99,
                #     "lineNoPageFrom": 99,
                #     "lineNoPageTill": 99,
                #     "pageNo": 99,
                #     "paragraphNo": 99,
                #     "text": "xxx"
                # },
                entries.append(
                    {
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ENTRY_NO: len(entries) + 1,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_FROM: int(line_lines_idx_from) + 1,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_TILL: int(line_lines_idx_till) + 1,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: int(page_idx) + 1,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: para_no,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT: " ".join(text),
                    }
                )

            dcr_core.cfg.glob.text_parser.parse_result_line_pages[page_idx][dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES] = line_lines

        if cfg.glob.setup.is_create_extra_file_list_number:
            # {
            #     "number": "xxx",
            #     "listNo": 99,
            #     "noEntries": 99,
            #     "pageNoFrom": 99,
            #     "pageNoTill": 99,
            #     "regexp": "xxx",
            #     "entries": []
            # }
            entry = {
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NUMBER: self._rule[0].rstrip(),
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LIST_NO: self.no_lists,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_ENTRIES: len(entries),
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_FROM: int(self._entries[0][0]) + 1,
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_TILL: int(self._entries[-1][0]) + 1,
            }

            if cfg.glob.setup.is_lt_list_number_file_incl_regexp:
                entry[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_REGEXP] = self._rule[-1]

            entry[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ENTRIES] = entries

            self._lists.append(entry)

        self._reset_list()

        utils.progress_msg_line_type_list_number(f"LineTypeListNumber: End   list                    on page={self._page_idx+1}")

    # -----------------------------------------------------------------------------
    # Initialise the numbered list anti-patterns.
    # -----------------------------------------------------------------------------
    # 1: name:  pattern name
    # 2: regexp regular expression
    # -----------------------------------------------------------------------------
    def _init_anti_patterns(self) -> list[tuple[str, re.Pattern[str]]]:
        """Initialise the numbered list anti-patterns.

        Returns:
            list[tuple[str, re.Pattern[str]]]:
                The valid numbered list anti-patterns.
        """
        if cfg.glob.setup.lt_list_number_rule_file and cfg.glob.setup.lt_list_number_rule_file.lower() != "none":
            lt_list_number_rule_file_path = utils.get_os_independent_name(cfg.glob.setup.lt_list_number_rule_file)
            if os.path.isfile(lt_list_number_rule_file_path):
                return self._load_anti_patterns_from_json(pathlib.Path(lt_list_number_rule_file_path))

            dcr_core.utils.terminate_fatal(
                f"File with numbered list anti-patterns is missing - " f"file name '{cfg.glob.setup.lt_list_number_rule_file}'"
            )

        anti_patterns = []

        for name, regexp in dcr_core.nlp.cls_nlp_core.NLPCore.get_lt_anti_patterns_default_list_number(
            environment_variant=cfg.glob.setup.environment_variant
        ):
            anti_patterns.append((name, re.compile(regexp)))

        return anti_patterns

    # -----------------------------------------------------------------------------
    # Initialise the numbered list rules.
    # -----------------------------------------------------------------------------
    # 1: rule_name
    # 2: regexp_str:
    #           regular expression
    # 3: function_is_asc:
    #           compares predecessor and successor
    # 4: start_values:
    #           list of strings
    # -----------------------------------------------------------------------------
    def _init_rules(self) -> list[RuleExtern]:
        """Initialise the numbered list rules.

        Returns:
            list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]:
                    The valid numbered list rules.
        """
        if cfg.glob.setup.lt_list_number_rule_file and cfg.glob.setup.lt_list_number_rule_file.lower() != "none":
            lt_list_number_rule_file_path = utils.get_os_independent_name(cfg.glob.setup.lt_list_number_rule_file)
            if os.path.isfile(lt_list_number_rule_file_path):
                return self._load_rules_from_json(pathlib.Path(lt_list_number_rule_file_path))

            dcr_core.utils.terminate_fatal(f"File with numbered list rules is missing - " f"file name '{cfg.glob.setup.lt_list_number_rule_file}'")

        return dcr_core.nlp.cls_nlp_core.NLPCore.get_lt_rules_default_list_number()

    # -----------------------------------------------------------------------------
    # Load the valid numbered list anti-patterns from a JSON file.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _load_anti_patterns_from_json(
        lt_list_number_rule_file: pathlib.Path,
    ) -> list[tuple[str, re.Pattern[str]]]:
        """Load the valid numbered list anti-patterns from a JSON file.

        Args:
            lt_list_number_rule_file (Path):
                    JSON file.

        Returns:
            list[tuple[str, re.Pattern[str]]]:
                    The valid numbered list anti-patterns from the JSON file,
        """
        anti_patterns = []

        with open(lt_list_number_rule_file, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS]:
                anti_patterns.append(
                    (
                        rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NAME],
                        re.compile(rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_REGEXP]),
                    )
                )

        utils.progress_msg("The numbered list anti-patterns were successfully loaded " + f"from the file {cfg.glob.setup.lt_list_number_rule_file}")

        return anti_patterns

    # -----------------------------------------------------------------------------
    # Load numbered list rules from a JSON file.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _load_rules_from_json(
        lt_list_number_rule_file: pathlib.Path,
    ) -> list[RuleExtern]:
        """Load numbered list rules from a JSON file.

        Args:
            lt_list_number_rule_file (Path):
                    JSON file.

        Returns:
            list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]:
                The valid numbered list rules from the JSON file,
        """
        rules: list[RuleExtern] = []

        with open(lt_list_number_rule_file, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE_RULES]:
                rules.append(
                    (
                        rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NAME],
                        rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_REGEXP],
                        getattr(
                            dcr_core.nlp.cls_nlp_core.NLPCore,
                            "is_asc_" + rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_FUNCTION_IS_ASC],
                        ),
                        rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_START_VALUES],
                    )
                )

        utils.progress_msg(f"The list_number rules were successfully loaded from the file {cfg.glob.setup.lt_list_number_rule_file}")

        return rules

    # -----------------------------------------------------------------------------
    # Process the line-related data.
    # -----------------------------------------------------------------------------
    def _process_line(self, line_line: dict[str, float | int | str]) -> None:  # noqa: C901
        """Process the line-related data.

        Args:
            line_line (dict[str, str]):
                    The line to be processed.
        """
        text = str(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

        for (rule_name, pattern) in self._anti_patterns:
            if pattern.match(text):
                utils.progress_msg_line_type_list_number(f"LineTypeListNumber: Anti pattern                         ={rule_name} - text={text}")
                return

        para_no = int(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO])
        target_value = text.split()[0]

        if self._rule:
            if self._rule[1].match(target_value):
                if self._llx_lower_limit <= float(
                    line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX]
                ) <= self._llx_upper_limit and self._rule[2](str(self._entries[-1][4]), target_value):
                    self._entries.append([self._page_idx, para_no, self._line_lines_idx, self._line_lines_idx, target_value])
                    self._no_entries += 1
                    self._para_no_prev = para_no
                    return

                self._finish_list()

        rule: RuleIntern = ()  # type: ignore

        # rule_name, regexp_compiled, function_is_asc, start_values, regexp_str,
        for elem in self._rules_collection:
            if not elem[1].match(target_value):
                continue

            if elem[3]:
                if target_value not in elem[3]:
                    continue

            rule = elem
            break

        if rule:
            if self._rule:
                self._finish_list()
        else:
            if self._rule:
                if self._page_idx == self._page_idx_prev and para_no == self._para_no_prev:
                    # Paragraph already in progress.
                    self._entries[-1][-2] = self._line_lines_idx
                else:
                    self._finish_list()

            self._para_no_prev = para_no
            return

        self._rule = rule

        if not self._entries:
            # New numbered paragraph.
            self._line_lines_idx_from = self._line_lines_idx
            self._line_lines_idx_till = self._line_lines_idx
            self._llx_lower_limit = round(
                (coord_llx := float(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX]))
                * (100 - cfg.glob.setup.lt_list_number_tolerance_llx)
                / 100,
                2,
            )
            self._llx_upper_limit = round(coord_llx * (100 + cfg.glob.setup.lt_list_number_tolerance_llx) / 100, 2)

        self._entries.append([self._page_idx, para_no, self._line_lines_idx, self._line_lines_idx, target_value])

        self._no_entries += 1

        self._para_no_prev = para_no

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.progress_msg_line_type_list_number(f"LineTypeListNumber: Start page                           ={self._page_idx + 1}")

        self._max_line_line = len(dcr_core.cfg.glob.text_parser.parse_result_line_lines)

        for line_lines_idx, line_line in enumerate(dcr_core.cfg.glob.text_parser.parse_result_line_lines):
            self._line_lines_idx = line_lines_idx

            if line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY:
                self._process_line(line_line)
                self._page_idx_prev = self._page_idx

        utils.progress_msg_line_type_list_number(f"LineTypeListNumber: End   page                           ={self._page_idx + 1}")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Reset the document memory.
    # -----------------------------------------------------------------------------
    def _reset_document(self) -> None:
        """Reset the document memory."""
        self._max_page = dcr_core.cfg.glob.text_parser.parse_result_no_pages_in_doc

        self._lists = []

        utils.progress_msg_line_type_list_number("LineTypeListNumber: Reset the document memory")

        self._reset_list()

    # -----------------------------------------------------------------------------
    # Reset the list memory.
    # -----------------------------------------------------------------------------
    def _reset_list(self) -> None:
        """Reset the list memory."""
        self._rule = ()  # type: ignore

        self._entries = []

        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._no_entries = 0

        self._page_idx_prev = -1
        self._para_no_prev = 0

        self._predecessor = ""

        self._rule = ()  # type: ignore

        utils.progress_msg_line_type_list_number("LineTypeListNumber: Reset the list memory")

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

        utils.progress_msg_line_type_list_number("LineTypeListNumber")
        utils.progress_msg_line_type_list_number(f"LineTypeListNumber: Start document                       ={cfg.glob.action_curr.action_file_name}")

        self._reset_document()

        for page_idx, page in enumerate(dcr_core.cfg.glob.text_parser.parse_result_line_pages):
            self._page_idx = page_idx
            dcr_core.cfg.glob.text_parser.parse_result_line_lines = page[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        self._finish_list()

        if cfg.glob.setup.is_create_extra_file_list_number and self._lists:
            full_name_toc = utils.get_full_name(
                cfg.glob.action_curr.action_directory_name,
                cfg.glob.action_curr.get_stem_name() + "_list_number." + db.cls_document.Document.DOCUMENT_FILE_TYPE_JSON,  # type: ignore
            )
            with open(full_name_toc, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    {
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: cfg.glob.document.document_id,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: cfg.glob.document.document_file_name,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER_IN_DOC: self.no_lists,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LISTS_NUMBER: self._lists,
                    },
                    file_handle,
                    indent=cfg.glob.setup.json_indent,
                    sort_keys=cfg.glob.setup.is_json_sort_keys,
                )

        utils.progress_msg_line_type_list_number(f"LineTypeListNumber: End   document                       ={cfg.glob.action_curr.action_file_name}")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
