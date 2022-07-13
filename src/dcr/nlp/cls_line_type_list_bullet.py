"""Module nlp.cls_line_type_list_bullet: Determine bulleted lists."""
from __future__ import annotations

import json
import os
import pathlib
import re

import cfg.glob
import utils

import dcr_core.cfg.glob
import dcr_core.nlp.cls_nlp_core
import dcr_core.utils

# -----------------------------------------------------------------------------
# Global type aliases.
# -----------------------------------------------------------------------------
Entry = dict[str, int | str]
Entries = list[Entry]

List = dict[str, Entries | float | int | str]
Lists = list[List]


# pylint: disable=too-many-instance-attributes
class LineTypeListBullet:
    """Determine list of bulleted lines.

    Returns:
        _type_: LineTypeListBullet instance.
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

        dcr_core.utils.progress_msg(cfg.glob.setup.is_verbose_lt_list_bullet, "LineTypeListBullet")
        dcr_core.utils.progress_msg(
            cfg.glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: Start create instance                ={cfg.glob.action_curr.action_file_name}",
        )

        self._anti_patterns: list[tuple[str, re.Pattern[str]]] = self._init_anti_patterns()

        self._bullet = ""

        # page_idx, para_no, line_lines_idx_from, line_lines_idx_till
        self._entries: list[list[int]] = []

        self._line_lines_idx = -1

        self._lists: Lists = []

        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._no_entries = 0

        self._page_idx = -1
        self._page_idx_prev = -1

        self._para_no = 0
        self._para_no_prev = 0

        self._rules = self._init_rules()
        for key in self._rules:
            self._rules[key] = len(key)

        self.no_lists = 0

        self._exist = True

        dcr_core.utils.progress_msg(
            cfg.glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: End   create instance                ={cfg.glob.action_curr.action_file_name}",
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Finish a list.
    # -----------------------------------------------------------------------------
    def _finish_list(self) -> None:
        """Finish a list."""
        if self._no_entries == 0:
            return

        if self._no_entries < cfg.glob.setup.lt_list_bullet_min_entries:
            dcr_core.utils.progress_msg(
                cfg.glob.setup.is_verbose_lt_list_bullet,
                f"LineTypeListBullet: Not enough list entries    found only={self._no_entries} - "
                + f"bullet='{self._bullet}' - entries={self._entries}",
            )
            self._reset_list()
            return

        dcr_core.utils.progress_msg(
            cfg.glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: List entries                    found={self._no_entries} - " + f"bullet='{self._bullet}' - entries={self._entries}",
        )

        self.no_lists += 1

        entries: Entries = []

        for [page_idx, para_no, line_lines_idx_from, line_lines_idx_till] in self._entries:
            line_lines: dcr_core.nlp.cls_nlp_core.NLPCore.ParserLineLines = dcr_core.cfg.glob.text_parser.parse_result_line_pages[page_idx][
                dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES
            ]

            text = []

            for idx in range(line_lines_idx_from, line_lines_idx_till + 1):
                line_lines[idx][dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_LIST_BULLET

                if cfg.glob.setup.is_create_extra_file_list_bullet:
                    text.append(line_lines[idx][dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

            if cfg.glob.setup.is_create_extra_file_list_bullet:
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
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_FROM: line_lines_idx_from + 1,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE_TILL: line_lines_idx_till + 1,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO: page_idx + 1,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO: para_no,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT: " ".join(text),
                    }
                )

            dcr_core.cfg.glob.text_parser.parse_result_line_pages[page_idx][dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES] = line_lines

        if cfg.glob.setup.is_create_extra_file_list_bullet:
            # {
            #     "bullet": "xxx",
            #     "listNo": 99,
            #     "noEntries": 99,
            #     "pageNoFrom": 99,
            #     "pageNoTill": 99,
            #     "entries": []
            # },
            self._lists.append(
                {
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_BULLET: self._bullet.rstrip(),
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LIST_NO: self.no_lists,
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_ENTRIES: len(entries),
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_FROM: self._entries[0][0] + 1,
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_TILL: self._entries[-1][0] + 1,
                    dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ENTRIES: entries,
                }
            )

        self._reset_list()

        dcr_core.utils.progress_msg(
            cfg.glob.setup.is_verbose_lt_list_bullet, f"LineTypeListBullet: End   list                    on page={self._page_idx+1}"
        )

    # -----------------------------------------------------------------------------
    # Initialise the bulleted list anti-patterns.
    # -----------------------------------------------------------------------------
    # 1: name:  pattern name
    # 2: regexp regular expression
    # -----------------------------------------------------------------------------
    def _init_anti_patterns(self) -> list[tuple[str, re.Pattern[str]]]:
        """Initialise the bulleted list anti-patterns.

        Returns:
            list[tuple[str, re.Pattern[str]]]:
                The valid bulleted list anti-patterns.
        """
        if cfg.glob.setup.lt_list_bullet_rule_file and cfg.glob.setup.lt_list_bullet_rule_file.lower() != "none":
            lt_list_bullet_rule_file_path = dcr_core.utils.get_os_independent_name(cfg.glob.setup.lt_list_bullet_rule_file)
            if os.path.isfile(lt_list_bullet_rule_file_path):
                return self._load_anti_patterns_from_json(pathlib.Path(lt_list_bullet_rule_file_path))

            dcr_core.utils.terminate_fatal(
                f"File with bulleted list anti-patterns is missing - " f"file name '{cfg.glob.setup.lt_list_bullet_rule_file}'"
            )

        anti_patterns = []

        for name, regexp in dcr_core.nlp.cls_nlp_core.NLPCore.get_lt_anti_patterns_default_list_bullet(
            environment_variant=cfg.glob.setup.environment_variant
        ):
            anti_patterns.append((name, re.compile(regexp)))

        return anti_patterns

    # -----------------------------------------------------------------------------
    # Initialise the valid bullets.
    # -----------------------------------------------------------------------------
    # 1: bullet character(s)
    # -----------------------------------------------------------------------------
    def _init_rules(self) -> dict[str, int]:
        """Initialise the valid bullets.

        Returns:
            dict[str, int]:
                    All valid bullets.
        """
        if cfg.glob.setup.lt_list_bullet_rule_file and cfg.glob.setup.lt_list_bullet_rule_file.lower() != "none":
            lt_list_bullet_rule_file_path = dcr_core.utils.get_os_independent_name(cfg.glob.setup.lt_list_bullet_rule_file)

            if os.path.isfile(lt_list_bullet_rule_file_path):
                return self._load_rules_from_json(pathlib.Path(lt_list_bullet_rule_file_path))

            dcr_core.utils.terminate_fatal(f"File with valid bullets is missing - " f"file name '{cfg.glob.setup.lt_list_bullet_rule_file}'")

        return dcr_core.nlp.cls_nlp_core.NLPCore.get_lt_rules_default_list_bullet()

    # -----------------------------------------------------------------------------
    # Load the valid bulleted list anti-patterns from a JSON file.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _load_anti_patterns_from_json(
        lt_list_bullet_rule_file: pathlib.Path,
    ) -> list[tuple[str, re.Pattern[str]]]:
        """Load the valid bulleted list anti-patterns from a JSON file.

        Args:
            lt_list_bullet_rule_file (Path):
                    JSON file.

        Returns:
            list[tuple[str, re.Pattern[str]]]:
                    The valid bulleted list anti-patterns from the JSON file,
        """
        anti_patterns = []

        with open(lt_list_bullet_rule_file, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for rule in json_data[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE_ANTI_PATTERNS]:
                anti_patterns.append(
                    (
                        rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NAME],
                        re.compile(rule[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_REGEXP]),
                    )
                )

        utils.progress_msg("The bulleted list anti-patterns were successfully loaded " + f"from the file {cfg.glob.setup.lt_list_bullet_rule_file}")

        return anti_patterns

    # -----------------------------------------------------------------------------
    # Load the valid bullets from a JSON file.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _load_rules_from_json(
        lt_list_bullet_rule_file: pathlib.Path,
    ) -> dict[str, int]:
        """Load the valid bullets from a JSON file.

        Args:
            lt_list_bullet_rule_file (Path):
                    JSON file name including directory path.

        Returns:
            dict[str, int]:
                The valid bullets from the JSON file,
        """
        list_bullet_rules = {}

        with open(lt_list_bullet_rule_file, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for bullet in json_data[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE_RULES]:
                list_bullet_rules[bullet] = 0

        utils.progress_msg(f"The list_bullet rules were successfully loaded from the file {cfg.glob.setup.lt_list_bullet_rule_file}")

        return list_bullet_rules

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
                dcr_core.utils.progress_msg(
                    cfg.glob.setup.is_verbose_lt_list_bullet, f"LineTypeListBullet: Anti pattern                         ={rule_name} - text={text}"
                )
                return

        para_no = int(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO])

        bullet = ""

        for key, value in self._rules.items():
            if text[0:value] == key:
                bullet = key
                break

        if not bullet:
            if self._page_idx == self._page_idx_prev and para_no == self._para_no_prev:
                # Paragraph already in progress.
                self._entries[-1][-1] = self._line_lines_idx
                return

            self._finish_list()
            return

        if (
            bullet != self._bullet
            or self._llx_upper_limit <= float(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX]) <= self._llx_lower_limit
        ):
            self._finish_list()

        self._bullet = bullet

        if not self._entries:
            # New bulleted paragraph.
            self._line_lines_idx_from = self._line_lines_idx
            self._line_lines_idx_till = self._line_lines_idx
            self._llx_lower_limit = round(
                (coord_llx := float(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX]))
                * (100 - cfg.glob.setup.lt_list_bullet_tolerance_llx)
                / 100,
                2,
            )
            self._llx_upper_limit = round(coord_llx * (100 + cfg.glob.setup.lt_list_bullet_tolerance_llx) / 100, 2)

        self._entries.append([self._page_idx, para_no, self._line_lines_idx, self._line_lines_idx])

        self._no_entries += 1

        self._para_no_prev = para_no

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        dcr_core.utils.progress_msg(
            cfg.glob.setup.is_verbose_lt_list_bullet, f"LineTypeListBullet: Start page                           ={self._page_idx + 1}"
        )

        self._max_line_line = len(dcr_core.cfg.glob.text_parser.parse_result_line_lines)

        for line_lines_idx, line_line in enumerate(dcr_core.cfg.glob.text_parser.parse_result_line_lines):
            self._line_lines_idx = line_lines_idx

            if line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                self._process_line(line_line)
                self._page_idx_prev = self._page_idx

        dcr_core.utils.progress_msg(
            cfg.glob.setup.is_verbose_lt_list_bullet, f"LineTypeListBullet: End   page                           ={self._page_idx + 1}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Reset the document memory.
    # -----------------------------------------------------------------------------
    def _reset_document(self) -> None:
        """Reset the document memory."""
        dcr_core.utils.progress_msg(cfg.glob.setup.is_verbose_lt_list_bullet, "LineTypeListBullet: Reset the document memory")

        self.no_lists = 0

        if cfg.glob.setup.is_create_extra_file_list_bullet:
            self._lists = []

        self._reset_list()

    # -----------------------------------------------------------------------------
    # Reset the list memory.
    # -----------------------------------------------------------------------------
    def _reset_list(self) -> None:
        """Reset the list memory."""
        self._bullet = ""

        self._entries = []

        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._no_entries = 0

        self._page_idx_prev = -1
        self._para_no_prev = 0

        dcr_core.utils.progress_msg(cfg.glob.setup.is_verbose_lt_list_bullet, "LineTypeListBullet: Reset the list memory")

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

        dcr_core.utils.progress_msg(cfg.glob.setup.is_verbose_lt_list_bullet, "LineTypeListBullet")
        dcr_core.utils.progress_msg(
            cfg.glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: Start document                       ={cfg.glob.action_curr.action_file_name}",
        )

        self._reset_document()

        for page_idx, page in enumerate(dcr_core.cfg.glob.text_parser.parse_result_line_pages):
            self._page_idx = page_idx
            dcr_core.cfg.glob.text_parser.parse_result_line_lines = page[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        self._finish_list()

        if cfg.glob.setup.is_create_extra_file_list_bullet and self._lists:
            full_name_toc = dcr_core.utils.get_full_name(
                cfg.glob.action_curr.action_directory_name,
                cfg.glob.action_curr.get_stem_name() + "_list_bullet." + dcr_core.cfg.glob.FILE_TYPE_JSON,  # type: ignore
            )
            with open(full_name_toc, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                # {
                #     "documentId": 99,
                #     "documentFileName": "xxx",
                #     "noListsBulletInDocument": 99,
                #     "listsBullet": [
                #     ]
                # }
                json.dump(
                    {
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: cfg.glob.document.document_id,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: cfg.glob.document.document_file_name,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET_IN_DOC: self.no_lists,
                        dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LISTS_BULLET: self._lists,
                    },
                    file_handle,
                    indent=cfg.glob.setup.json_indent,
                    sort_keys=cfg.glob.setup.is_json_sort_keys,
                )

        dcr_core.utils.progress_msg(
            cfg.glob.setup.is_verbose_lt_list_bullet,
            f"LineTypeListBullet: End   document                       ={cfg.glob.action_curr.action_file_name}",
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
