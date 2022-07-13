"""Module nlp.cls_line_type_heading: Determine headings."""
from __future__ import annotations

import collections
import decimal
import json
import math
import os
import pathlib
import re

import dcr_core.cfg.glob
import dcr_core.nlp.cls_nlp_core
import dcr_core.utils

# -----------------------------------------------------------------------------
# Global type aliases.
# -----------------------------------------------------------------------------


# pylint: disable=too-many-instance-attributes
class LineTypeHeading:
    """Determine table of content lines.

    Returns:
        _type_: LineTypeHeading instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(
        self,
        action_file_name: str,
        is_verbose_lt: bool = False,
    ) -> None:
        """Initialise the instance.

        Args:
            action_file_name (str):
                    File name of the file to be processed.
            is_verbose_lt (bool, optional):
                    If true, processing results are reported. Defaults to False.
        """
        self._action_file_name = action_file_name
        self._file_encoding = ""
        self._is_create_extra_file_heading = False
        self._is_lt_heading_file_incl_regexp = False
        self._is_verbose_lt = is_verbose_lt
        self._lt_heading_file_incl_no_ctx = 0
        self._lt_heading_max_level = 0
        self._lt_heading_min_pages = 0
        self._lt_heading_rule_file = ""
        self._lt_heading_tolerance_llx = 0.0

        dcr_core.utils.check_exists_object(
            is_text_parser=True,
        )

        dcr_core.utils.progress_msg(self._is_verbose_lt, "LineTypeHeading")
        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeHeading: Start create instance                ={self._action_file_name}")

        self._RULE_NAME_SIZE: int = 20

        # -----------------------------------------------------------------------------
        # Anti-patterns.
        # -----------------------------------------------------------------------------
        # 1: name:  pattern name
        # 2: regexp_compiled:
        #           compiled regular expression
        # -----------------------------------------------------------------------------
        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = self._init_anti_patterns()

        self._lt_heading_max_level_curr = 0

        self._line_lines_idx = 0

        self._level_prev = 0

        self._max_line_line = 0
        self._max_page = 0

        self._page_idx = 0

        self._parser_line_lines_json: dcr_core.nlp.cls_nlp_core.NLPCore.ParserLineLines = []

        self._rules: list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]] = self._init_rules()

        # -----------------------------------------------------------------------------
        # Heading rules collection.
        # -----------------------------------------------------------------------------
        # 1: rule_name
        # 2: is_first_token:
        #           True:  apply rule to first token (split)
        #           False: apply rule to beginning of line
        # 3: regexp_compiled:
        #           compiled regular expression
        # 4: function_is_asc:
        #           compares predecessor and successor
        # 5: start_values:
        #           list of strings
        # 6: regexp_str:
        #           regular expression
        # -----------------------------------------------------------------------------
        self._rules_collection: list[tuple[str, bool, re.Pattern[str], collections.abc.Callable[[str, str], bool], list[str], str]] = []

        for (rule_name, is_first_token, regexp_str, function_is_asc, start_values) in self._rules:
            self._rules_collection.append(
                (
                    rule_name.ljust(self._RULE_NAME_SIZE),
                    is_first_token,
                    re.compile(regexp_str),
                    function_is_asc,
                    start_values,
                    regexp_str,
                )
            )

        # -----------------------------------------------------------------------------
        # Rules hierarchy for determining the headings.
        # -----------------------------------------------------------------------------
        # 1: rule_name
        # 2: is_first_token:
        #           True:  apply rule to first token (split)
        #           False: apply rule to beginning of line
        # 3: regexp_compiled:
        #           compiled regular expression
        # 4: function_is_asc:
        #           compares predecessor and successor
        # 5: start_values:
        #           list of strings
        # 6: level:
        #           hierarchical level of the current heading
        # 7: coord_llx:
        #           lower left x-coordinate of the beginning of the possible heading
        # 8: predecessor:
        #           predecessor value
        # 9: regexp_str:
        #           regular expression
        # -----------------------------------------------------------------------------
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

        # [
        #     {
        #         "headingLevel": 99,
        #         "headingText": "xxx",
        #         "pageNo": 99,
        #         "headingCtxLine99": "xxx",
        #         "regexp": "xxx"
        #     },
        # ]
        self._toc: list[dict[str, int | object | str]] = []

        self._exist = True

        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeHeading: End   create instance                ={self._action_file_name}")

    # -----------------------------------------------------------------------------
    # Check whether a valid start value is present.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _check_valid_start_value(target_value: str, is_first_token: bool, start_values: list[str]) -> bool:  # noqa: C901
        """Check whether a valid start value is present.

        Args:
            target_value (str):
                    Value to be checked.
            is_first_token (bool):
                    Restrict the check to the first token.
            start_values (list[str]):
                    Valid start values.

        Returns:
            bool:   True if a valid start value is present, false else.
        """
        if is_first_token:
            try:
                float(target_value)
                target_value_decimal = decimal.Decimal(target_value)
                target_fraction = target_value_decimal - math.floor(target_value_decimal)

                for start_value in start_values:
                    try:
                        start_value_decimal = decimal.Decimal(start_value)
                        start_fraction = start_value_decimal - math.floor(start_value_decimal)

                        if target_fraction == start_fraction:
                            return True
                    except ValueError:
                        pass

                return False
            except ValueError:
                if target_value in start_values:
                    return True
                return False

        for start_value in start_values:
            start_value_len = len(start_value)

            if len(target_value) < start_value_len:
                continue

            if start_value == target_value[0:start_value_len]:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Create a table of content entry.
    # -----------------------------------------------------------------------------
    #     {
    #         "headingLevel": 99,
    #         "headingText": "xxx",
    #         "pageNo": 99,
    #         "headingCtxLine9": "xxx",
    #         "regexp": "xxxx"
    #     }
    # -----------------------------------------------------------------------------
    def _create_toc_entry(self, level: int, text: str) -> None:

        """Create a table of content entry.

        Args:
            level (int): Heading level.
            text: Heading text.
        """
        if not self._is_create_extra_file_heading:
            return

        toc_entry = {
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_HEADING_LEVEL: level,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_HEADING_TEXT: text,
            dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: self._page_idx + 1,
        }

        if self._lt_heading_file_incl_no_ctx > 0:
            page_idx = self._page_idx
            line_lines: dcr_core.nlp.cls_nlp_core.NLPCore.ParserLineLines = dcr_core.cfg.glob.text_parser.parse_result_line_lines
            line_lines_idx = self._line_lines_idx + 1

            for idx in range(self._lt_heading_file_incl_no_ctx):
                (line, new_page_idx, new_line_lines, new_line_lines_idx) = self._get_next_body_line(page_idx, line_lines, line_lines_idx)

                toc_entry[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_HEADING_CTX_LINE + str(idx + 1)] = line

                line_lines = new_line_lines
                line_lines_idx = new_line_lines_idx

                page_idx = new_page_idx

        if self._is_lt_heading_file_incl_regexp:
            toc_entry[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_REGEXP] = self._rules_hierarchy[level - 1][8]

        self._toc.append(toc_entry)

    # -----------------------------------------------------------------------------
    # Get the next body line.
    # -----------------------------------------------------------------------------
    def _get_next_body_line(
        self, page_idx: int, line_lines: dcr_core.nlp.cls_nlp_core.NLPCore.ParserLineLines, line_lines_idx: int
    ) -> tuple[str, int, dcr_core.nlp.cls_nlp_core.NLPCore.ParserLineLines, int]:
        """Get the next body line.

        Args:
            page_idx (int):
                    Start with this page number.
            line_lines (LineLines):
                    The lines of the start page.
            line_lines_idx (int):
                    Start with this line number.

        Returns:
            tuple[str, int, LineLines, int]:
                    found line or empty, last page searched, lines of this page, last checked line.
        """
        for idx in range(line_lines_idx + 1, len(line_lines)):
            line_line: dcr_core.nlp.cls_nlp_core.NLPCore.ParserLineLine = line_lines[idx]

            if line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] != dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                continue

            return line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT], page_idx, line_lines, idx

        if (page_idx + 1) < self._max_page:
            page_idx_local = page_idx + 1

            line_lines_local: dcr_core.nlp.cls_nlp_core.NLPCore.ParserLineLines = dcr_core.cfg.glob.text_parser.parse_result_line_pages[
                page_idx_local
            ][dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]

            for idx, line_line in enumerate(line_lines_local):
                if line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] != dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                    continue

                return (
                    line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT],
                    page_idx_local,
                    line_lines_local,
                    idx + 1,
                )

        # not testable
        return "", page_idx, line_lines, line_lines_idx

    # -----------------------------------------------------------------------------
    # Initialise the heading anti-patterns.
    # -----------------------------------------------------------------------------
    # 1: name:  pattern name
    # 2: regexp regular expression
    # -----------------------------------------------------------------------------
    def _init_anti_patterns(self) -> list[tuple[str, re.Pattern[str]]]:
        """Initialise the heading anti-patterns.

        Returns:
            list[tuple[str, re.Pattern[str]]]:
                The valid heading anti-patterns.
        """
        if self._lt_heading_rule_file and self._lt_heading_rule_file.lower() != "none":
            lt_heading_rule_file_path = dcr_core.utils.get_os_independent_name(self._lt_heading_rule_file)
            if os.path.isfile(lt_heading_rule_file_path):
                return self._load_anti_patterns_from_json(pathlib.Path(lt_heading_rule_file_path))

            dcr_core.utils.terminate_fatal(f"File with heading anti-patterns is missing - " f"file name '{self._lt_heading_rule_file}'")

        anti_patterns = []

        for name, regexp in dcr_core.nlp.cls_nlp_core.NLPCore.get_lt_anti_patterns_default_heading():
            anti_patterns.append((name, re.compile(regexp)))

        return anti_patterns

    # -----------------------------------------------------------------------------
    # Initialise the heading rules.
    # -----------------------------------------------------------------------------
    # 1: rule_name
    # 2: is_first_token:
    #           True:  apply rule to first token (split)
    #           False: apply rule to beginning of line
    # 3: regexp_str:
    #           regular expression
    # 4: function_is_asc:
    #           compares predecessor and successor
    # 5: start_values:
    #           list of strings
    # -----------------------------------------------------------------------------
    def _init_rules(self) -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
        """Initialise the heading rules.

        Returns:
            list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
                The valid heading rules.
        """
        if self._lt_heading_rule_file and self._lt_heading_rule_file.lower() != "none":
            lt_heading_rule_file_path = dcr_core.utils.get_os_independent_name(self._lt_heading_rule_file)
            if os.path.isfile(lt_heading_rule_file_path):
                return self._load_rules_from_json(pathlib.Path(lt_heading_rule_file_path))

            dcr_core.utils.terminate_fatal(f"File with heading rules is missing - " f"file name '{self._lt_heading_rule_file}'")

        return dcr_core.nlp.cls_nlp_core.NLPCore.get_lt_rules_default_heading()

    # -----------------------------------------------------------------------------
    # Load the valid heading anti-patterns from a JSON file.
    # -----------------------------------------------------------------------------
    def _load_anti_patterns_from_json(
        self,
        lt_heading_rule_file: pathlib.Path,
    ) -> list[tuple[str, re.Pattern[str]]]:
        """Load the valid heading anti-patterns from a JSON file.

        Args:
            lt_heading_rule_file (Path):
                    JSON file.

        Returns:
            list[tuple[str, re.Pattern[str]]]:
                    The valid heading anti-patterns from the JSON file,
        """
        anti_patterns = []

        with open(lt_heading_rule_file, "r", encoding=self._file_encoding) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS]:
                anti_patterns.append(
                    (
                        rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NAME],
                        re.compile(rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_REGEXP]),
                    )
                )

        dcr_core.utils.progress_msg(
            self._is_verbose_lt, f"The heading anti-patterns were successfully loaded from the file {self._lt_heading_rule_file}"
        )

        return anti_patterns

    # -----------------------------------------------------------------------------
    # Load the valid heading rules from a JSON file.
    # -----------------------------------------------------------------------------
    def _load_rules_from_json(
        self,
        lt_heading_rule_file: pathlib.Path,
    ) -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
        """Load the valid heading rules from a JSON file.

        Args:
            lt_heading_rule_file (Path):
                    JSON file.

        Returns:
            list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
                The valid heading rules from the JSON file,
        """
        rules = []

        with open(lt_heading_rule_file, "r", encoding=self._file_encoding) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE_RULES]:
                rules.append(
                    (
                        rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NAME],
                        rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_IS_FIRST_TOKEN],
                        rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_REGEXP],
                        getattr(
                            dcr_core.nlp.cls_nlp_core.NLPCore,
                            "is_asc_" + rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_FUNCTION_IS_ASC],
                        ),
                        rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_START_VALUES],
                    )
                )

        dcr_core.utils.progress_msg(self._is_verbose_lt, f"The heading rules were successfully loaded from the file {self._lt_heading_rule_file}")

        return rules

    # -----------------------------------------------------------------------------
    # Process the line-related data.
    # -----------------------------------------------------------------------------
    def _process_line(self, line_line: dict[str, str], text: str, first_token: str) -> int:  # noqa: C901
        """Process the line-related data.

        Args:
            line_line (dict[str, str]):
                    The line to be processed.
            text (str):
                    The text of the line.
            first_token (str):
                    The first token of the text.

        Returns:
            int: The heading level or zero.
        """
        for (rule_name, pattern) in self._anti_patterns:
            if pattern.match(text):
                dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeHeading: Anti pattern                         ={rule_name} - text={text}")
                return 0

        coord_llx_curr = line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX]

        for ph_idx in reversed(range(ph_size := len(self._rules_hierarchy))):
            (
                rule_name,
                is_first_token,
                regexp_compiled,
                function_is_asc,
                start_values,
                level,
                coord_llx,
                predecessor,
                regexp_str,
            ) = self._rules_hierarchy[ph_idx]

            target_value = first_token if is_first_token else text

            if regexp_compiled.match(target_value):
                if not function_is_asc(predecessor, target_value):
                    if self._check_valid_start_value(target_value, is_first_token, start_values):
                        break
                    continue

                coord_llx_curr_float = float(coord_llx_curr)
                coord_llx_float = float(coord_llx)
                if (
                    coord_llx_curr_float < coord_llx_float * (100 - self._lt_heading_tolerance_llx) / 100
                    or coord_llx_curr_float > coord_llx_float * (100 + self._lt_heading_tolerance_llx) / 100
                ):
                    return 0

                self._rules_hierarchy[ph_idx] = (
                    rule_name,
                    is_first_token,
                    regexp_compiled,
                    function_is_asc,
                    start_values,
                    level,
                    coord_llx,
                    target_value,
                    regexp_str,
                )

                self._level_prev = level

                self._create_toc_entry(level, text)

                dcr_core.utils.progress_msg(
                    self._is_verbose_lt,
                    f"LineTypeHeading: Match                                ={rule_name} " + f"- level={level} - heading={text}",
                )

                # Delete levels that are no longer needed
                if ph_size > level:
                    for i in range(ph_size - 1, level - 1, -1):
                        del self._rules_hierarchy[i]

                return level

        for (
            rule_name,
            is_first_token,
            regexp_compiled,
            function_is_asc,
            start_values,
            regexp_str,
        ) in self._rules_collection:
            target_value = first_token if is_first_token else text
            if regexp_compiled.match(target_value):
                if not self._check_valid_start_value(target_value, is_first_token, start_values):
                    continue

                level = self._level_prev + 1

                self._rules_hierarchy.append(
                    (
                        rule_name,
                        is_first_token,
                        regexp_compiled,
                        function_is_asc,
                        start_values,
                        level,
                        coord_llx_curr,
                        target_value,
                        regexp_str,
                    )
                )

                self._level_prev = level

                self._create_toc_entry(level, text)

                dcr_core.utils.progress_msg(
                    self._is_verbose_lt,
                    f"LineTypeHeading: Match new level                      ={rule_name} " + f"- level={level} - heading={text}",
                )

                return level

        return 0

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        dcr_core.utils.progress_msg(self._is_verbose_lt, "LineTypeHeading")
        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeHeading: Start page (lines)                   ={self._page_idx+1}")

        self._max_line_line = len(dcr_core.cfg.glob.text_parser.parse_result_line_lines)

        # wwe max_line_line_idx = self._max_line_line - 1

        for line_lines_idx, line_line in enumerate(dcr_core.cfg.glob.text_parser.parse_result_line_lines):
            self._line_lines_idx = line_lines_idx
            if line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] != dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                continue

            if (text := line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT]) == "":
                # not testable
                continue

            if (first_token := text.split()[0]) == text:
                continue

            # wwe
            # if not (
            #     dcr_core.cfg.glob.text_parser.parse_result_titles
            #     and line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT] in cfg.glob.text_parser.parse_result_titles
            # ):
            #     # Headings are limited to single-line paragraphs.
            #     if self._line_lines_idx > 0:
            #         if (
            #             line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]
            #             == cfg.glob.text_parser.parse_result_line_lines[self._line_lines_idx - 1][
            #                 nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO
            #             ]
            #         ):
            #             continue
            #     if self._line_lines_idx < max_line_line_idx:
            #         if (
            #             line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]
            #             == cfg.glob.text_parser.parse_result_line_lines[self._line_lines_idx + 1][
            #                 nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO
            #             ]
            #         ):
            #             continue

            if (level := self._process_line(line_line, text, first_token)) > 0:
                line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = (
                    dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_HEADER + "_" + str(level)
                )
                dcr_core.cfg.glob.text_parser.parse_result_line_lines[self._line_lines_idx] = line_line

        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeHeading: End   page (lines)                   ={self._page_idx+1}")

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
        is_create_extra_file_heading: bool,
        is_json_sort_keys: bool,
        is_lt_heading_file_incl_regexp: bool,
        json_indent: str,
        lt_heading_file_incl_no_ctx: int,
        lt_heading_max_level: int,
        lt_heading_min_pages: int,
        lt_heading_rule_file: str,
        lt_heading_tolerance_llx: float,
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
            is_create_extra_file_heading (bool):
                    Create a separate JSON file with the table of contents.
            is_json_sort_keys (bool):
                    If true, the output of the JSON dictionaries will be sorted by key.
            is_lt_heading_file_incl_regexp (bool):
                    If it is set to true, the regular expression
                    for the heading is included in the JSON file.
            json_indent (str):
                    Indent level for pretty-printing the JSON output.
            lt_heading_file_incl_no_ctx (int):
                    The number of lines following the heading to be included as context
                     into the JSON file.
            lt_heading_max_level (int):
                    Maximum level of the heading structure.
            lt_heading_min_pages (int):
                    Minimum number of pages to determine the headings.
            lt_heading_rule_file (str):
                    File with rules to determine the headings.
            lt_heading_tolerance_llx (float):
                    Tolerance of vertical indentation in percent.
            parser_line_pages_json (dcr_core.nlp.cls_nlp_core.NLPCore.LinePages):
                    The document pages formatted in the parser.
        """
        if lt_heading_max_level == 0 or len(dcr_core.cfg.glob.text_parser.parse_result_line_pages) < lt_heading_min_pages:
            return

        self._action_file_name = action_file_name
        self._file_encoding = file_encoding
        self._is_create_extra_file_heading = is_create_extra_file_heading
        self._is_lt_heading_file_incl_regexp = is_lt_heading_file_incl_regexp
        self._lt_heading_file_incl_no_ctx = lt_heading_file_incl_no_ctx
        self._lt_heading_max_level = lt_heading_max_level
        self._lt_heading_min_pages = lt_heading_min_pages
        self._lt_heading_rule_file = lt_heading_rule_file
        self._lt_heading_tolerance_llx = lt_heading_tolerance_llx

        dcr_core.utils.progress_msg(self._is_verbose_lt, "LineTypeHeading")
        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeHeading: Start document                       ={self._action_file_name}")

        self._max_page = dcr_core.cfg.glob.text_parser.parse_result_no_pages_in_doc

        for page_idx, page_json in enumerate(parser_line_pages_json):
            self._page_idx = page_idx
            self._parser_line_lines_json = page_json[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        if self._is_create_extra_file_heading and self._toc:
            full_name = dcr_core.utils.get_full_name(
                directory_name,
                dcr_core.utils.get_stem_name(str(file_name)) + "_heading." + dcr_core.cfg.glob.FILE_TYPE_JSON,
            )
            with open(full_name, "w", encoding=self._file_encoding) as file_handle:
                # {
                #     "documentId": 99,
                #     "documentFileName": "xxx",
                #     "toc": [
                #     ]
                # }
                json.dump(
                    {
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: document_document_id,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: document_file_name,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TOC: self._toc,
                    },
                    file_handle,
                    indent=json_indent,
                    sort_keys=is_json_sort_keys,
                )

        dcr_core.utils.progress_msg(self._is_verbose_lt, f"LineTypeHeading: End   document                       ={self._action_file_name}")
