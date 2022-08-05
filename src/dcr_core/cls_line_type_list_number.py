from __future__ import annotations

import collections
import json
import os
import pathlib
import re

import dcr_core.cls_nlp_core
import dcr_core.core_glob
import dcr_core.core_utils


# pylint: disable=too-many-instance-attributes
class LineTypeListNumber:
    """Determine list of numbered lines.

    Returns:
        _type_: LineTypeListNumber instance.
    """

    Entry = dict[str, int | str]
    Entries = list[Entry]

    List = dict[str, Entries | float | int | object | str]
    Lists = list[List]

    RuleExtern = tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]
    RuleIntern = tuple[str, re.Pattern[str], collections.abc.Callable[[str, str], bool], list[str], str]

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(
        self,
        file_name_curr: str,
    ) -> None:
        """Initialise the instance.

        Args:
            file_name_curr (str):
                    File name of the file to be processed.
        """
        dcr_core.core_utils.check_exists_object(
            is_line_type_headers_footers=True,
            is_line_type_list_bullet=True,
            is_line_type_table=True,
            is_line_type_toc=True,
            is_setup=True,
            is_text_parser=True,
        )

        self.file_name_curr = file_name_curr
        self._environment_variant = ""

        dcr_core.core_utils.check_exists_object(
            is_text_parser=True,
        )

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_list_number, "LineTypeListNumber")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: Start create instance                ={self.file_name_curr}",
        )

        self._RULE_NAME_SIZE: int = 20

        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = self._init_anti_patterns()

        # page_idx, para_no, line_lines_idx_from, line_lines_idx_till, target_value
        self._entries: list[list[int | str]] = []

        self._line_lines_idx = -1

        self._lists: LineTypeListNumber.Lists = []

        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._no_entries = 0

        self._page_idx = -1
        self._page_idx_prev = -1

        self._para_no = 0
        self._para_no_prev = 0

        self._parser_line_lines_json: dcr_core.cls_nlp_core.NLPCore.ParserLineLines = []
        self._parser_line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages = []

        self._rule: LineTypeListNumber.RuleIntern = ()  # type: ignore

        self._rules: list[LineTypeListNumber.RuleExtern] = self._init_rules()

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
        self._rules_collection: list[LineTypeListNumber.RuleIntern] = []

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

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: End   create instance                ={self.file_name_curr}",
        )

    # -----------------------------------------------------------------------------
    # Finish a list.
    # -----------------------------------------------------------------------------
    def _finish_list(self) -> None:
        """Finish a list."""
        if self._no_entries == 0:
            return

        if self._no_entries < dcr_core.core_glob.setup.lt_list_number_min_entries:
            dcr_core.core_utils.progress_msg(
                dcr_core.core_glob.setup.is_verbose_lt_list_number,
                f"LineTypeListNumber: Not enough list entries    found only={self._no_entries} - "
                + f"number='{self._rule[0]}' - entries={self._entries}",
            )
            self._reset_list()
            return

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: List entries                    found={self._no_entries} - "
            + f"number='{self._rule[0]}' - entries={self._entries}",
        )

        self.no_lists += 1

        entries: LineTypeListNumber.Entries = []

        for [page_idx, para_no, line_lines_idx_from, line_lines_idx_till, _] in self._entries:
            line_lines: dcr_core.cls_nlp_core.NLPCore.ParserLineLines = self._parser_line_pages_json[page_idx][
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES
            ]

            text = []

            for idx in range(int(line_lines_idx_from), int(line_lines_idx_till) + 1):
                line_lines[idx][dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_LIST_NUMBER

                if dcr_core.core_glob.setup.is_create_extra_file_list_number:
                    text.append(line_lines[idx][dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

            if dcr_core.core_glob.setup.is_create_extra_file_list_number:
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
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_ENTRY_NO: len(entries) + 1,
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_FROM: int(line_lines_idx_from) + 1,
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_TILL: int(line_lines_idx_till) + 1,
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: int(page_idx) + 1,
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: para_no,
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT: " ".join(text),
                    }
                )

            self._parser_line_pages_json[page_idx][dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES] = line_lines

        if dcr_core.core_glob.setup.is_create_extra_file_list_number:
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
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NUMBER: self._rule[0].rstrip(),
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LIST_NO: self.no_lists,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_ENTRIES: len(entries),
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_FROM: int(self._entries[0][0]) + 1,
                dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_TILL: int(self._entries[-1][0]) + 1,
            }

            if dcr_core.core_glob.setup.is_lt_list_number_file_incl_regexp:
                entry[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_REGEXP] = self._rule[-1]

            entry[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_ENTRIES] = entries

            self._lists.append(entry)

        self._reset_list()

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: End   list                    on page={self._page_idx+1}",
        )

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
        if dcr_core.core_glob.setup.lt_list_number_rule_file and dcr_core.core_glob.setup.lt_list_number_rule_file.lower() != "none":
            lt_list_number_rule_file_path = dcr_core.core_utils.get_os_independent_name(dcr_core.core_glob.setup.lt_list_number_rule_file)
            if os.path.isfile(lt_list_number_rule_file_path):
                return self._load_anti_patterns_from_json(pathlib.Path(lt_list_number_rule_file_path))

            dcr_core.core_utils.terminate_fatal(
                f"File with numbered list anti-patterns is missing - " f"file name '{dcr_core.core_glob.setup.lt_list_number_rule_file}'"
            )

        anti_patterns = []

        for name, regexp in dcr_core.cls_nlp_core.NLPCore.get_lt_anti_patterns_default_list_number(
            environment_variant=self._environment_variant
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
    def _init_rules(self) -> list[LineTypeListNumber.RuleExtern]:
        """Initialise the numbered list rules.

        Returns:
            list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]:
                    The valid numbered list rules.
        """
        if dcr_core.core_glob.setup.lt_list_number_rule_file and dcr_core.core_glob.setup.lt_list_number_rule_file.lower() != "none":
            lt_list_number_rule_file_path = dcr_core.core_utils.get_os_independent_name(dcr_core.core_glob.setup.lt_list_number_rule_file)
            if os.path.isfile(lt_list_number_rule_file_path):
                return self._load_rules_from_json(pathlib.Path(lt_list_number_rule_file_path))

            dcr_core.core_utils.terminate_fatal(
                f"File with numbered list rules is missing - " f"file name '{dcr_core.core_glob.setup.lt_list_number_rule_file}'"
            )

        return dcr_core.cls_nlp_core.NLPCore.get_lt_rules_default_list_number()

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

        with open(lt_list_number_rule_file, "r", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS]:
                anti_patterns.append(
                    (
                        rule[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NAME],
                        re.compile(rule[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_REGEXP]),
                    )
                )

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number,
            "The numbered list anti-patterns were successfully loaded "
            + f"from the file {dcr_core.core_glob.setup.lt_list_number_rule_file}",
        )

        return anti_patterns

    # -----------------------------------------------------------------------------
    # Load numbered list rules from a JSON file.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _load_rules_from_json(
        lt_list_number_rule_file: pathlib.Path,
    ) -> list[LineTypeListNumber.RuleExtern]:
        """Load numbered list rules from a JSON file.

        Args:
            lt_list_number_rule_file (Path):
                    JSON file.

        Returns:
            list[tuple[str, str, collections.abc.Callable[[str, str], bool], list[str]]]:
                The valid numbered list rules from the JSON file,
        """
        rules: list[LineTypeListNumber.RuleExtern] = []

        with open(lt_list_number_rule_file, "r", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE_RULES]:
                rules.append(
                    (
                        rule[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NAME],
                        rule[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_REGEXP],
                        getattr(
                            dcr_core.cls_nlp_core.NLPCore,
                            "is_asc_" + rule[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_FUNCTION_IS_ASC],
                        ),
                        rule[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_START_VALUES],
                    )
                )

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number,
            "The list_number rules were successfully loaded from the " + f"file {dcr_core.core_glob.setup.lt_list_number_rule_file}",
        )

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
        text = str(line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

        for (rule_name, pattern) in self._anti_patterns:
            if pattern.match(text):
                dcr_core.core_utils.progress_msg(
                    dcr_core.core_glob.setup.is_verbose_lt_list_number,
                    f"LineTypeListNumber: Anti pattern                         ={rule_name} - text={text}",
                )
                return

        para_no = int(line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO])
        target_value = text.split()[0]

        if self._rule:
            if self._rule[1].match(target_value):
                if self._llx_lower_limit <= float(
                    line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX]
                ) <= self._llx_upper_limit and self._rule[2](str(self._entries[-1][4]), target_value):
                    self._entries.append([self._page_idx, para_no, self._line_lines_idx, self._line_lines_idx, target_value])
                    self._no_entries += 1
                    self._para_no_prev = para_no
                    return

                self._finish_list()

        rule: LineTypeListNumber.RuleIntern = ()  # type: ignore

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
                (coord_llx := float(line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX]))
                * (100 - dcr_core.core_glob.setup.lt_list_number_tolerance_llx)
                / 100,
                2,
            )
            self._llx_upper_limit = round(coord_llx * (100 + dcr_core.core_glob.setup.lt_list_number_tolerance_llx) / 100, 2)

        self._entries.append([self._page_idx, para_no, self._line_lines_idx, self._line_lines_idx, target_value])

        self._no_entries += 1

        self._para_no_prev = para_no

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: Start page                           ={self._page_idx + 1}",
        )

        self._max_line_line = len(self._parser_line_lines_json)

        for line_lines_idx, line_line in enumerate(self._parser_line_lines_json):
            self._line_lines_idx = line_lines_idx

            if line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                self._process_line(line_line)
                self._page_idx_prev = self._page_idx

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: End   page                           ={self._page_idx + 1}",
        )

    # -----------------------------------------------------------------------------
    # Reset the document memory.
    # -----------------------------------------------------------------------------
    def _reset_document(self) -> None:
        """Reset the document memory."""
        self._max_page = dcr_core.core_glob.text_parser.parse_result_no_pages_in_doc

        self._lists = []

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number, "LineTypeListNumber: Reset the document memory"
        )

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

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_list_number, "LineTypeListNumber: Reset the list memory")

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
    def process_document(
        self,
        directory_name: str,
        document_id: int,
        environment_variant: str,
        file_name_curr: str,
        file_name_orig: str,
        parser_line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None:
        """Process the document related data.

        Args:
            directory_name (str):
                    Directory name of the output file.
            document_id (int):
                    Identification of the document.
            environment_variant (str):
                    Environment variant: dev, prod or test.
            file_name_curr (str):
                    File name of the file to be processed.
            file_name_orig (in):
                    File name of the document file.
            parser_line_pages_json (dcr_core.cls_nlp_core.NLPCore.LinePages):
                    The document pages formatted in the parser.
        """
        dcr_core.core_utils.check_exists_object(
            is_line_type_headers_footers=True,
            is_line_type_list_bullet=True,
            is_line_type_table=True,
            is_line_type_toc=True,
            is_setup=True,
            is_text_parser=True,
        )

        self.file_name_curr = file_name_curr
        self._environment_variant = environment_variant
        self._parser_line_pages_json = parser_line_pages_json

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_list_number, "LineTypeListNumber")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: Start document                       ={self.file_name_curr}",
        )

        self._reset_document()

        for page_idx, page_json in enumerate(parser_line_pages_json):
            self._page_idx = page_idx
            self._parser_line_lines_json = page_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        self._finish_list()

        if dcr_core.core_glob.setup.is_create_extra_file_list_number and self._lists:
            full_name = dcr_core.core_utils.get_full_name(
                directory_name,
                dcr_core.core_utils.get_stem_name(str(file_name_curr)) + "_list_number." + dcr_core.core_glob.FILE_TYPE_JSON,
            )
            with open(full_name, "w", encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    {
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: document_id,
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: file_name_orig,
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_NUMBER_IN_DOC: self.no_lists,
                        dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LISTS_NUMBER: self._lists,
                    },
                    file_handle,
                    indent=dcr_core.core_glob.setup.json_indent,
                    sort_keys=dcr_core.core_glob.setup.is_json_sort_keys,
                )

        if self.no_lists > 0:
            dcr_core.core_utils.progress_msg(
                dcr_core.core_glob.setup.is_verbose_lt_list_number,
                f"LineTypeListNumber:                 number numbered lists={self.no_lists}",
            )

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_list_number,
            f"LineTypeListNumber: End   document                       ={self.file_name_curr}",
        )
