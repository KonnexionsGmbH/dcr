"""Module nlp.cls_line_type_heading: Determine headings."""
from __future__ import annotations

import collections
import json
import os
import pathlib
import re

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
#    "lineNo": 99,
#    "lineIndexPage": 99,
#    "lineIndexParagraph": 99,
#    "lineType": "...",
#    "lowerLeftX": 99.99,
#    "paragraphNo": 99,
#    "rowNo": 99,
#    "text": "..."
# },
LineLine = dict[str, int | str]
LineLines = list[LineLine]


# pylint: disable=too-many-instance-attributes
class LineTypeHeading:
    """Determine table of content lines.

    Returns:
        _type_: LineTypeHeading instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        try:
            cfg.glob.action_curr.exists()  # type: ignore
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'Action (action_curr)' does not yet exist.",
            )

        try:
            cfg.glob.document.exists()  # type: ignore
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'Document' does not yet exist.",
            )

        try:
            cfg.glob.setup.exists()  # type: ignore
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'Setup' does not yet exist.",
            )

        try:
            cfg.glob.text_parser.exists()
        except AttributeError:
            utils.terminate_fatal(
                "The required instance of the class 'TextParser' does not yet exist.",
            )

        utils.progress_msg_line_type_heading("LineTypeHeading")
        utils.progress_msg_line_type_heading(
            f"LineTypeHeading: Start create instance                ={cfg.glob.action_curr.action_file_name}"
        )

        self._RULE_NAME_SIZE: int = 20

        # -----------------------------------------------------------------------------
        # Anti-patterns.
        # -----------------------------------------------------------------------------
        # 1: name:  pattern name
        # 2: regexp_compiled:
        #           compiled regular expression
        # -----------------------------------------------------------------------------
        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = [
            ("A A".ljust(self._RULE_NAME_SIZE), re.compile(r"^[A-Z] [A-Z]")),
        ]

        self._heading_max_level_curr = 0

        self._heading_rules: list[
            tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]
        ] = self._init_heading_rules()

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
        self._heading_rules_collection: list[
            tuple[str, bool, re.Pattern[str], collections.abc.Callable[[str, str], bool], list[str], str]
        ] = []

        for (rule_name, is_first_token, regexp_str, function_is_asc, start_values) in self._heading_rules:
            self._heading_rules_collection.append(
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
        # Heading rules hierarchy for determining the headings.
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
        self._heading_rules_hierarchy: list[
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

        self._line_lines_idx = 0

        self._level_prev = 0

        self._max_line_line = 0
        self._max_page = 0

        self._page_idx = 0

        self._toc: list[dict[str, int | object | str]] = []

        self._exist = True

        utils.progress_msg_line_type_heading(
            f"LineTypeHeading: End   create instance                ={cfg.glob.action_curr.action_file_name}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Convert a roman numeral to integer.
    # -----------------------------------------------------------------------------
    @classmethod
    def _convert_roman_2_int(cls, roman: str) -> int:
        """Convert a roman numeral to integer.

        Args:
            roman (str): The roman numeral.

        Returns:
            int: The corresponding integer.
        """
        tallies = {
            "i": 1,
            "v": 5,
            "x": 10,
            "l": 50,
            "c": 100,
            "d": 500,
            "m": 1000,
            # specify more numerals if you wish
        }

        integer: int = 0

        for i in range(len(roman) - 1):
            left = roman[i]
            right = roman[i + 1]
            if tallies[left] < tallies[right]:
                integer -= tallies[left]
            else:
                integer += tallies[left]

        integer += tallies[roman[-1]]

        return integer

    # -----------------------------------------------------------------------------
    # Create a table of content entry.
    # -----------------------------------------------------------------------------
    def _create_toc_entry(self, level: int, text: str) -> None:

        """Create a table of content entry.

        Args:
            level (int): Heading level.
            text: Heading text.
        """
        if not cfg.glob.setup.is_create_extra_file_toc:
            return

        toc_entry = {
            nlp.cls_nlp_core.NLPCore.JSON_NAME_HEADING_LEVEL: level,
            nlp.cls_nlp_core.NLPCore.JSON_NAME_HEADING_TEXT: text,
            nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: self._page_idx + 1,
        }

        if cfg.glob.setup.heading_toc_incl_no_ctx > 0:
            page_idx = self._page_idx
            line_lines: LineLines = cfg.glob.text_parser.parse_result_line_lines
            line_lines_idx = self._line_lines_idx + 1

            for idx in range(cfg.glob.setup.heading_toc_incl_no_ctx):
                (line, new_page_idx, new_line_lines, new_line_lines_idx) = self._get_next_body_line(
                    page_idx, line_lines, line_lines_idx
                )

                if line == "":
                    break

                toc_entry[nlp.cls_nlp_core.NLPCore.JSON_NAME_HEADING_CTX_LINE + str(idx + 1)] = line

                page_idx = new_page_idx
                line_lines = new_line_lines
                line_lines_idx = new_line_lines_idx

        if cfg.glob.setup.is_heading_toc_incl_regexp:
            toc_entry[nlp.cls_nlp_core.NLPCore.JSON_NAME_REGEXP] = self._heading_rules_hierarchy[level - 1][8]

        self._toc.append(toc_entry)

    # -----------------------------------------------------------------------------
    # Initialise the heading rules.
    # -----------------------------------------------------------------------------
    def _get_next_body_line(
        self, page_idx: int, line_lines: LineLines, line_lines_idx: int
    ) -> tuple[str, int, LineLines, int]:
        for idx in range(line_lines_idx + 1, len(line_lines)):
            line_line: LineLine = line_lines[idx]

            if line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] != db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY:
                continue

            return line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT], page_idx, line_lines, idx  # type: ignore

        if (page_idx_local := page_idx + 1) == self._max_page:
            return "", page_idx, line_lines, line_lines_idx

        line_lines_local: LineLines = cfg.glob.text_parser.parse_result_line_pages[page_idx_local][
            nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES
        ]

        for idx, line_line in enumerate(line_lines_local):
            if line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] != db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY:
                continue

            return (
                line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT],
                page_idx_local,
                line_lines_local,
                idx + 1,
            )  # type: ignore

        return "", page_idx, line_lines, line_lines_idx

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
    def _init_heading_rules(self) -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
        if cfg.glob.setup.heading_rule_file and cfg.glob.setup.heading_rule_file.lower() != "none":
            heading_rule_file_path = utils.get_os_independent_name(cfg.glob.setup.heading_rule_file)
            if os.path.isfile(heading_rule_file_path):
                return self._load_heading_rules_from_json(pathlib.Path(heading_rule_file_path))

            utils.terminate_fatal(
                f"File with heading rule file is missing - " f"file name '{cfg.glob.setup.heading_rule_file}'"
            )

        return [
            (
                "(999)",
                True,
                r"\(\d+\)$",
                self._is_asc_string_integers,
                ["(1)"],
            ),
            (
                "(A)",
                True,
                r"\([A-Z]\)$",
                self._is_asc_uppercase_letters,
                ["(A)"],
            ),
            (
                "(ROM)",
                True,
                r"\(M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$",
                self._is_asc_romans,
                ["(I)"],
            ),
            (
                "(a)",
                True,
                r"\([a-z]\)$",
                self._is_asc_lowercase_letters,
                ["(a)"],
            ),
            (
                "(rom)",
                True,
                r"\(m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$",
                self._is_asc_romans,
                ["(i)"],
            ),
            (
                "999)",
                True,
                r"\d+\)$",
                self._is_asc_string_integers,
                ["1)"],
            ),
            (
                "999.",
                True,
                r"\d+\.$",
                self._is_asc_string_integers,
                ["1."],
            ),
            (
                "999.999",
                True,
                r"\d+\.\d+\.?$",
                self._is_asc_string_floats,
                [],
            ),
            (
                "A)",
                True,
                r"[A-Z]\)$",
                self._is_asc_uppercase_letters,
                ["A)"],
            ),
            (
                "A.",
                True,
                r"[A-Z]\.$",
                self._is_asc_uppercase_letters,
                ["A."],
            ),
            (
                "ROM)",
                True,
                r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$",
                self._is_asc_romans,
                ["I)"],
            ),
            (
                "ROM.",
                True,
                r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.$",
                self._is_asc_romans,
                ["I."],
            ),
            (
                "a)",
                True,
                r"[a-z]\)$",
                self._is_asc_lowercase_letters,
                ["a)"],
            ),
            (
                "a.",
                True,
                r"[a-z]\.$",
                self._is_asc_lowercase_letters,
                ["a."],
            ),
            (
                "rom)",
                True,
                r"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$",
                self._is_asc_romans,
                ["i)"],
            ),
            (
                "rom.",
                True,
                r"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\.$",
                self._is_asc_romans,
                ["i."],
            ),
        ]

    # -----------------------------------------------------------------------------
    # Ignore the comparison.
    # -----------------------------------------------------------------------------
    @classmethod
    def _is_asc_ignore(cls, _predecessor: str, _successor: str) -> bool:
        """Ignore the comparison.

        Returns:
            bool: True.
        """
        return True

    # -----------------------------------------------------------------------------
    # Compare two lowercase letters on difference ascending 1.
    # -----------------------------------------------------------------------------
    @classmethod
    def _is_asc_lowercase_letters(cls, predecessor: str, successor: str) -> bool:
        """Compare two lowercase_letters on ascending.

        Args:
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: True, if the successor - predecessor is equal to 1, False else.
        """
        if (predecessor_ints := re.findall(r"[a-z]", predecessor.lower())) and (
            successor_ints := re.findall(r"[a-z]", successor.lower())
        ):
            if ord(successor_ints[0]) - ord(predecessor_ints[0]) == 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two roman numerals on ascending.
    # -----------------------------------------------------------------------------
    @classmethod
    def _is_asc_romans(cls, predecessor: str, successor: str) -> bool:
        """Compare two roman numerals on ascending.

        Args:
            predecessor (str): The previous roman numeral.
            successor (str): The current roman numeral.

        Returns:
            bool: False, if the predecessor is greater than the current value, True else.
        """
        # TBD depending on different regexp patterns
        # if predecessor[0] == "(":
        #     predecessor_net = predecessor[1:-1]
        #     successor_net = successor[1:-1]
        # else:
        #     predecessor_net = predecessor
        #     successor_net = successor

        if predecessor[0:1] == "(":
            predecessor_net = predecessor[1:]
        else:
            predecessor_net = predecessor
        if predecessor_net[-1] in {")", "."}:
            predecessor_net = predecessor_net[:-1]

        if successor[0:1] == "(":
            successor_net = successor[1:]
        else:
            successor_net = successor
        if successor_net[-1] in {")", "."}:
            successor_net = successor_net[:-1]

        if (
            LineTypeHeading._convert_roman_2_int(successor_net.lower())
            - LineTypeHeading._convert_roman_2_int(predecessor_net.lower())
            == 1
        ):
            return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two strings on ascending.
    # -----------------------------------------------------------------------------
    @classmethod
    def _is_asc_strings(cls, predecessor: str, successor: str) -> bool:
        """Compare two strings on ascending.

        Args:
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: False, if the predecessor is greater than the current value, True else.
        """
        if predecessor > successor:
            return False

        return True

    # -----------------------------------------------------------------------------
    # Compare two string floats on ascending.
    # -----------------------------------------------------------------------------
    @classmethod
    def _is_asc_string_floats(cls, predecessor: str, successor: str) -> bool:
        """Compare two string float numbers on ascending.

        Args:
            predecessor (str): The previous string float number.
            successor (str): The current string float number.

        Returns:
            bool: False, if the predecessor is greater than the current value, True else.
        """
        if (predecessor_floats := re.findall(r"\d+\.\d+", predecessor)) and (
            successor_floats := re.findall(r"\d+\.\d+", successor)
        ):
            if 0 < float(successor_floats[0]) - float(predecessor_floats[0]) <= 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two string integers on difference ascending 1.
    # -----------------------------------------------------------------------------
    @classmethod
    def _is_asc_string_integers(cls, predecessor: str, successor: str) -> bool:
        """Compare two string integers on ascending.

        Args:
            predecessor (str): The previous string integer.
            successor (str): The current string integer.

        Returns:
            bool: True, if the successor - predecessor is equal to 1, False else.
        """
        if (predecessor_ints := re.findall(r"\d+", predecessor)) and (successor_ints := re.findall(r"\d+", successor)):
            if int(successor_ints[0]) - int(predecessor_ints[0]) == 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two uppercase letters on difference ascending 1.
    # -----------------------------------------------------------------------------
    @classmethod
    def _is_asc_uppercase_letters(cls, predecessor: str, successor: str) -> bool:
        """Compare two uppercase_letters on ascending.

        Args:
            predecessor (str): The previous string.
            successor (str): The current string.

        Returns:
            bool: True, if the successor - predecessor is equal to 1, False else.
        """
        if (predecessor_ints := re.findall(r"[A-Z]", predecessor.upper())) and (
            successor_ints := re.findall(r"[A-Z]", successor.upper())
        ):
            if ord(successor_ints[0]) - ord(predecessor_ints[0]) == 1:
                return True

        return False

    # -----------------------------------------------------------------------------
    # Load heading rules from a JSON file.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _load_heading_rules_from_json(
        heading_rule_file: pathlib.Path,
    ) -> list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]]:
        """Load heading rules from a JSON file.

        Args:
            heading_rule_file (Path): JSON file.
        """
        heading_rules = []

        with open(heading_rule_file, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for heading_rule in json_data[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE_HEADING_RULES]:
                heading_rules.append(
                    (
                        heading_rule[nlp.cls_nlp_core.NLPCore.JSON_NAME_NAME],
                        heading_rule[nlp.cls_nlp_core.NLPCore.JSON_NAME_IS_FIRST_TOKEN],
                        heading_rule[nlp.cls_nlp_core.NLPCore.JSON_NAME_REGEXP],
                        getattr(
                            LineTypeHeading, "_is_asc_" + heading_rule[nlp.cls_nlp_core.NLPCore.JSON_NAME_FUNCTION_IS_ASC]
                        ),
                        heading_rule[nlp.cls_nlp_core.NLPCore.JSON_NAME_START_VALUES],
                    )
                )

        utils.progress_msg(f"The heading rules were successfully loaded from the file {cfg.glob.setup.heading_rule_file}")

        return heading_rules

    # -----------------------------------------------------------------------------
    # Process the line-related data.
    # -----------------------------------------------------------------------------
    def _process_line(self, line_line: dict[str, str]) -> int:  # noqa: C901
        """Process the line-related data.

        Args:
            line_line (dict[str, str]): The line to be processed.

        Returns:
            int: The heading level or zero.
        """
        text = line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT]

        for (rule_name, pattern) in self._anti_patterns:
            if pattern.match(text):
                utils.progress_msg_line_type_heading(
                    f"LineTypeHeading: Anti pattern                         ={rule_name} - text={text}"
                )
                return 0

        first_token = text.split()[0]
        coord_llx_curr = line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX]

        for ph_idx in reversed(range(ph_size := len(self._heading_rules_hierarchy))):
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
            ) = self._heading_rules_hierarchy[ph_idx]

            target_value = first_token if is_first_token else text

            if regexp_compiled.match(target_value):
                coord_llx_curr_float = float(coord_llx_curr)
                coord_llx_float = float(coord_llx)
                if (
                    coord_llx_curr_float < coord_llx_float * (100 - cfg.glob.setup.heading_tolerance_x) / 100
                    or coord_llx_curr_float > coord_llx_float * (100 + cfg.glob.setup.heading_tolerance_x) / 100
                ):
                    return 0

                if function_is_asc(predecessor, target_value):
                    self._heading_rules_hierarchy[ph_idx] = (
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

                    utils.progress_msg_line_type_heading(
                        f"LineTypeHeading: Match                                ={rule_name} "
                        + f"- level={level} - heading={text}"
                    )

                    # Delete levels that are no longer needed
                    if ph_size > level:
                        for i in range(ph_size - 1, level - 1, -1):
                            del self._heading_rules_hierarchy[i]

                    return level

                return 0

        for (
            rule_name,
            is_first_token,
            regexp_compiled,
            function_is_asc,
            start_values,
            regexp_str,
        ) in self._heading_rules_collection:
            target_value = first_token if is_first_token else text
            if regexp_compiled.match(target_value):
                if is_first_token and start_values:
                    if first_token not in start_values:
                        continue

                if (level := self._level_prev + 1) > cfg.glob.setup.heading_max_level:
                    return 0

                self._heading_rules_hierarchy.append(
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

                utils.progress_msg_line_type_heading(
                    f"LineTypeHeading: Match new level                      ={rule_name} "
                    + f"- level={level} - heading={text}"
                )

                return level

        return 0

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.progress_msg_line_type_heading("LineTypeHeading")
        utils.progress_msg_line_type_heading(f"LineTypeHeading: Start page (lines)                   ={self._page_idx+1}")

        self._max_line_line = len(cfg.glob.text_parser.parse_result_line_lines)

        for line_lines_idx, line_line in enumerate(cfg.glob.text_parser.parse_result_line_lines):
            self._line_lines_idx = line_lines_idx
            if line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] != db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY:
                continue

            if (level := self._process_line(line_line)) > 0:
                line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = (
                    db.cls_document.Document.DOCUMENT_LINE_TYPE_HEADER + "_" + str(level)
                )
                cfg.glob.text_parser.parse_result_line_lines[line_lines_idx] = line_line

        utils.progress_msg_line_type_heading(f"LineTypeHeading: End   page (lines)                   ={self._page_idx+1}")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

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
        if (
            cfg.glob.setup.heading_max_level == 0
            or len(cfg.glob.text_parser.parse_result_line_pages) < cfg.glob.setup.heading_min_pages
        ):
            return

        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.progress_msg_line_type_heading("LineTypeHeading")
        utils.progress_msg_line_type_heading(
            f"LineTypeHeading: Start document                       ={cfg.glob.action_curr.action_file_name}"
        )

        self._max_page = cfg.glob.text_parser.parse_result_no_pages_in_doc

        for page_idx, page in enumerate(cfg.glob.text_parser.parse_result_line_pages):
            self._page_idx = page_idx
            cfg.glob.text_parser.parse_result_line_lines = page[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        if cfg.glob.setup.is_create_extra_file_toc and self._toc:
            full_name_toc = utils.get_full_name(
                cfg.glob.action_curr.action_directory_name,
                cfg.glob.action_curr.get_stem_name()  # type: ignore
                + "_toc."
                + db.cls_document.Document.DOCUMENT_FILE_TYPE_JSON,
            )
            with open(full_name_toc, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    {
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: cfg.glob.document.document_id,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: cfg.glob.document.document_file_name,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_TOC: self._toc,
                    },
                    file_handle,
                    indent=cfg.glob.setup.json_indent,
                    sort_keys=cfg.glob.setup.is_json_sort_keys,
                )

        utils.progress_msg_line_type_heading(
            f"LineTypeHeading: End   document                       ={cfg.glob.action_curr.action_file_name}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
