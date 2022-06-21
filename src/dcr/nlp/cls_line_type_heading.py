"""Module nlp.cls_line_type_heading: Determine headings."""
from __future__ import annotations

import collections
import json
import re

import cfg.glob
import db.cls_document
import nlp.cls_nlp_core
import nlp.cls_text_parser
import utils


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

        self._PATTERN_NAME_SIZE: int = 20

        # -----------------------------------------------------------------------------
        # Anti-patterns.
        # -----------------------------------------------------------------------------
        # 1: name:  pattern name
        # 2: regexp_compiled:
        #           compiled regular expression
        # -----------------------------------------------------------------------------
        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = [
            ("A A".ljust(self._PATTERN_NAME_SIZE), re.compile(r"^[A-Z] [A-Z]")),
        ]

        self._heading_max_level_curr = 0

        self._idx_line_line = 0

        self._level_prev = 0

        self._max_line_line = 0

        self._page_no = 0

        # -----------------------------------------------------------------------------
        # Basic patterns.
        # -----------------------------------------------------------------------------
        # 1: pattern_name
        # 2: is_first_token:
        #           True:  apply pattern to first token (split)
        #           False: apply pattern to beginning of line
        # 3: regexp_str:
        #           regular expression
        # 4: function_is_asc:
        #           compares predecessor and successor
        # 5: start_values:
        #           list of strings
        # -----------------------------------------------------------------------------
        self._pattern_basis: list[tuple[str, bool, str, collections.abc.Callable[[str, str], bool], list[str]]] = [
            (
                "(a)",
                True,
                r"\([a-z]\)$",
                self._is_asc_lowercase_letters,
                ["(a)"],
            ),
            (
                "(A)",
                True,
                r"\([A-Z]\)$",
                self._is_asc_uppercase_letters,
                ["(A)"],
            ),
            (
                "Article 999:",
                False,
                r"Article \d+:?",
                self._is_asc_string_integers,
                [],
            ),
            (
                "ARTICLE 999 -",
                False,
                r"ARTICLE \d+ -",
                self._is_asc_string_integers,
                [],
            ),
            (
                "ARTICLE XXX-YYY:",
                False,
                r"ARTICLE [A-Z]+(-[A-Z]+)?:",
                self._is_asc_ignore,
                [],
            ),
            (
                "EXHIBIT A",
                False,
                r"EXHIBIT [A-Z]$",
                self._is_asc_strings,
                [],
            ),
            (
                'EXHIBIT "A"        ',
                False,
                r"EXHIBIT \u201c[A-Z]\u201d$",
                self._is_asc_strings,
                [],
            ),
            (
                "Riders-9",
                True,
                r"Riders-\d$",
                self._is_asc_string_integers,
                [],
            ),
            (
                "999.",
                True,
                r"\d+\.$",
                self._is_asc_string_integers,
                ["1."],
            ),
            (
                "(999)",
                True,
                r"\(\d+\)$",
                self._is_asc_string_integers,
                ["(1)"],
            ),
            (
                "Section 999.999.",
                False,
                r"Section \d+\.\d+\.",
                self._is_asc_string_floats,
                [],
            ),
            (
                "999.999",
                True,
                r"\d+\.\d+\.?$",
                self._is_asc_string_floats,
                [],
            ),
            (
                "a.",
                True,
                r"[a-z]\.$",
                self._is_asc_lowercase_letters,
                ["a", "a."],
            ),
            (
                "A.",
                True,
                r"[A-Z]\.$",
                self._is_asc_uppercase_letters,
                ["A", "A."],
            ),
            (
                "(rom)",
                True,
                r"\(m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$",
                self._is_asc_romans,
                ["(i)"],
            ),
            (
                "(ROM)",
                True,
                r"\(M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$",
                self._is_asc_romans,
                ["(I)"],
            ),
        ]

        # -----------------------------------------------------------------------------
        # Pattern collection.
        # -----------------------------------------------------------------------------
        # 1: pattern_name
        # 2: is_first_token:
        #           True:  apply pattern to first token (split)
        #           False: apply pattern to beginning of line
        # 3: regexp_compiled_match:
        #           compiled regular expression for matching
        # 4: regexp_compiled_display:
        #           compiled regular expression for showing the match
        # 5: function_is_asc:
        #           compares predecessor and successor
        # 6: start_values:
        #           list of strings
        # -----------------------------------------------------------------------------
        self._pattern_collection: list[
            tuple[str, bool, re.Pattern[str], re.Pattern[str], collections.abc.Callable[[str, str], bool], list[str]]
        ] = []

        for (pattern_name, is_first_token, regexp_str, function_is_asc, start_values) in self._pattern_basis:
            self._pattern_collection.append(
                (
                    pattern_name.ljust(self._PATTERN_NAME_SIZE),
                    is_first_token,
                    re.compile(regexp_str),
                    re.compile(regexp_str + " [^.]+"),
                    function_is_asc,
                    start_values,
                )
            )

        # -----------------------------------------------------------------------------
        # Hierarchy of patterns for determining the headings.
        # -----------------------------------------------------------------------------
        # 1: pattern_name
        # 2: is_first_token:
        #           True:  apply pattern to first token (split)
        #           False: apply pattern to beginning of line
        # 3: regexp_compiled_match:
        #           compiled regular expression for matching
        # 4: regexp_compiled_display:
        #           compiled regular expression for showing the match
        # 5: function_is_asc:
        #           compares predecessor and successor
        # 6: start_values:
        #           list of strings
        # 7: level:
        #           hierarchical level of the current heading
        # 8: lower_left_x:
        #           lower left x-coordinate of the beginning of the possible heading
        # 9: predecessor:
        #           predecessor value
        # -----------------------------------------------------------------------------
        self._pattern_hierarchy: list[
            tuple[
                str,
                bool,
                re.Pattern[str],
                re.Pattern[str],
                collections.abc.Callable[[str, str], bool],
                list[str],
                int,
                str,
                str,
            ]
        ] = []

        self._toc: list[dict[str, int | str]] = []

        self._exist = True

        utils.progress_msg_line_type_heading(
            f"LineTypeHeading: End   create instance                ={cfg.glob.action_curr.action_file_name}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Convert a roman numeral to integer.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _convert_roman_2_int(roman: str) -> int:
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
    # pylint: disable=missing-param-doc
    def _create_toc_entry(self, level: int, pattern_display: re.Match[str] | None, pattern_matched: re.Match[str]) -> str:

        """Create a table of content entry.

        Args:
            level (int): Heading level.
            pattern_display (re.Match[str] | None): Hits for display.
            pattern_matched (re.Match[str] | None): Hits from search.

        Returns:
            str: The heading text.
        """
        if not cfg.glob.setup.is_heading_create_toc:
            return ""

        if pattern_display is None:
            heading = pattern_matched.group(0)
            if self._idx_line_line < self._max_line_line:
                heading = (
                    heading
                    + ("" if heading[-1] == " " else " ")
                    + cfg.glob.text_parser.parse_result_line_lines[self._idx_line_line + 1][
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT
                    ]
                )
        else:
            heading = pattern_display.group(0)

        self._toc.append(
            {
                nlp.cls_nlp_core.NLPCore.JSON_NAME_HEADING_LEVEL: level,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_HEADING_TEXT: heading,
                nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: self._page_no,
            }
        )

        return heading

    # -----------------------------------------------------------------------------
    # Ignore the comparison.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _is_asc_ignore(_predecessor: str, _successor: str) -> bool:
        """Ignore the comparison.

        Returns:
            bool: True.
        """
        return True

    # -----------------------------------------------------------------------------
    # Compare two lowercase letters on difference ascending 1.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _is_asc_lowercase_letters(predecessor: str, successor: str) -> bool:
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
    def _is_asc_romans(self, predecessor: str, successor: str) -> bool:
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

        predecessor_net = predecessor[1:-1]
        successor_net = successor[1:-1]

        if self._convert_roman_2_int(successor_net.lower()) - self._convert_roman_2_int(predecessor_net.lower()) == 1:
            return True

        return False

    # -----------------------------------------------------------------------------
    # Compare two strings on ascending.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _is_asc_strings(predecessor: str, successor: str) -> bool:
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
    @staticmethod
    def _is_asc_string_floats(predecessor: str, successor: str) -> bool:
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
    @staticmethod
    def _is_asc_string_integers(predecessor: str, successor: str) -> bool:
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
    @staticmethod
    def _is_asc_uppercase_letters(predecessor: str, successor: str) -> bool:
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

        for (pattern_name, pattern) in self._anti_patterns:
            if pattern.match(text):
                utils.progress_msg_line_type_heading(
                    f"LineTypeHeading: Anti pattern                         ={pattern_name} - text={text}"
                )
                return 0

        first_token = text.split()[0]
        lower_left_x_curr = line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LOWER_LEFT_X]

        for ph_idx in reversed(range(ph_size := len(self._pattern_hierarchy))):
            (
                pattern_name,
                is_first_token,
                regexp_compiled_match,
                regexp_compiled_display,
                function_is_asc,
                start_values,
                level,
                lower_left_x,
                predecessor,
            ) = self._pattern_hierarchy[ph_idx]

            target_value = first_token if is_first_token else text

            if pattern_matched := regexp_compiled_match.match(target_value):
                lower_left_x_curr_float = float(lower_left_x_curr)
                lower_left_x_float = float(lower_left_x)
                if (
                    lower_left_x_curr_float < lower_left_x_float * (100 - cfg.glob.setup.heading_tolerance_x) / 100
                    or lower_left_x_curr_float > lower_left_x_float * (100 + cfg.glob.setup.heading_tolerance_x) / 100
                ):
                    return 0

                if function_is_asc(predecessor, target_value):
                    self._pattern_hierarchy[ph_idx] = (
                        pattern_name,
                        is_first_token,
                        regexp_compiled_match,
                        regexp_compiled_display,
                        function_is_asc,
                        start_values,
                        level,
                        lower_left_x,
                        target_value,
                    )

                    self._level_prev = level

                    heading = self._create_toc_entry(level, regexp_compiled_display.match(text), pattern_matched)

                    utils.progress_msg_line_type_heading(
                        f"LineTypeHeading: Match                                ={pattern_name} "
                        + f"- level={level} - heading={heading}"
                    )

                    # Delete levels that are no longer needed
                    if ph_size > level:
                        for i in range(ph_size - 1, level - 1, -1):
                            del self._pattern_hierarchy[i]

                    return level

                return 0

        for (
            pattern_name,
            is_first_token,
            regexp_compiled_match,
            regexp_compiled_display,
            function_is_asc,
            start_values,
        ) in self._pattern_collection:
            target_value = first_token if is_first_token else text
            if pattern_matched := regexp_compiled_match.match(target_value):
                if is_first_token and start_values:
                    if first_token not in start_values:
                        continue

                if (level := self._level_prev + 1) > cfg.glob.setup.heading_max_level:
                    return 0

                self._pattern_hierarchy.append(
                    (
                        pattern_name,
                        is_first_token,
                        regexp_compiled_match,
                        regexp_compiled_display,
                        function_is_asc,
                        start_values,
                        level,
                        lower_left_x_curr,
                        target_value,
                    )
                )

                self._level_prev = level

                heading = self._create_toc_entry(level, regexp_compiled_display.match(text), pattern_matched)

                utils.progress_msg_line_type_heading(
                    f"LineTypeHeading: Match new level                      ={pattern_name} "
                    + f"- level={level} - heading={heading}"
                )

                return level

        return 0

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._page_no += 1

        utils.progress_msg_line_type_heading("LineTypeHeading")
        utils.progress_msg_line_type_heading(f"LineTypeHeading: Start page (lines)                   ={self._page_no}")

        self._max_line_line = len(cfg.glob.text_parser.parse_result_line_lines)

        for idx, line_line in enumerate(cfg.glob.text_parser.parse_result_line_lines):
            self._idx_line_line = idx
            if line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] != db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY:
                continue

            if nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO in line_line:
                utils.progress_msg_line_type_heading(f"LineTypeHeading: Table row                            ={idx}")
                line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = db.cls_document.Document.DOCUMENT_LINE_TYPE_TABLE
                cfg.glob.text_parser.parse_result_line_lines[idx] = line_line
                continue

            if (level := self._process_line(line_line)) > 0:
                line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = (
                    db.cls_document.Document.DOCUMENT_LINE_TYPE_HEADER + "_" + str(level)
                )
                cfg.glob.text_parser.parse_result_line_lines[idx] = line_line

        utils.progress_msg_line_type_heading(f"LineTypeHeading: End   page (lines)                   ={self._page_no}")

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

        for page in cfg.glob.text_parser.parse_result_line_pages:
            cfg.glob.text_parser.parse_result_line_lines = page[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        if cfg.glob.setup.is_heading_create_toc and self._toc:
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
