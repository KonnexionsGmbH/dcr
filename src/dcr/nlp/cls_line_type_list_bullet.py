"""Module nlp.cls_line_type_list_bullet: Determine bulleted lists."""
from __future__ import annotations

import json
import os
import pathlib

import cfg.glob
import db.cls_document
import nlp.cls_nlp_core
import nlp.cls_text_parser
import utils

# -----------------------------------------------------------------------------
# Global type aliases.
# -----------------------------------------------------------------------------
# {
#    "bullet": "xxx",
#    "firstEntryLLX": 99.99,
#    "noEntries": 99,
#    "pageNoFrom": 99,
#    "pageNoTill": 99,
#    "entries": []
# },
List = dict[str, float | int | list[str] | str]
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
            is_text_parser=True,
        )

        utils.progress_msg_line_type_list_bullet("LineTypeListBullet")
        utils.progress_msg_line_type_list_bullet(
            f"LineTypeListBullet: Start create instance                ={cfg.glob.action_curr.action_file_name}"
        )

        self._bullet = ""
        self._bullet_rules = self._init_list_bullet_rules()

        for key in self._bullet_rules:
            self._bullet_rules[key] = len(key)

        # page_idx, para_no, line_lines_idx
        self._entries: list[
            tuple[
                int,
                int,
                int,
            ]
        ] = []

        self._line_lines_idx = -1

        self._lists: list[dict[str, str]]

        self._llx_lower_limit = 0.0
        self._llx_upper_limit = 0.0

        self._no_entries = 0

        self._page_idx = -1
        self._page_idx_prev = -1

        self._para_no = 0
        self._para_no_prev = 0

        self._exist = True

        utils.progress_msg_line_type_list_bullet(
            f"LineTypeListBullet: End   create instance                ={cfg.glob.action_curr.action_file_name}"
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
            utils.progress_msg_line_type_list_bullet(
                f"LineTypeListBullet: Not enough list entries    found only={self._no_entries} - bullet='{self._bullet}' - entries={self._entries}"
            )
            self._reset_list()
            return

        utils.progress_msg_line_type_list_bullet(
                f"LineTypeListBullet: List entries                    found={self._no_entries} - bullet='{self._bullet}' - entries={self._entries}"
        )

        if not cfg.glob.setup.is_create_extra_file_list_bullet:
            self._reset_list()
            return

        self._page_no_till = self._page_idx + 1

        # self._lists.append(
        #     {
        #         nlp.cls_nlp_core.NLPCore.JSON_NAME_BULLET: self._bullet_prev,
        #         nlp.cls_nlp_core.NLPCore.JSON_NAME_FIRST_ENTRY_LLX: self._first_entry_llx,
        #         nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_ENTRIES: len(self._entries),
        #         nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_FROM: self._page_no_from,
        #         nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO_TILL: self._page_no_till,
        #         nlp.cls_nlp_core.NLPCore.JSON_NAME_LIST_NO: len(self._lists) + 1,
        #         nlp.cls_nlp_core.NLPCore.JSON_NAME_ENTRIES: self._entries,
        #     }
        # )

        self._reset_list()

        utils.progress_msg_line_type_list_bullet(
            f"LineTypeListBullet: End   list                    on page={self._page_idx+1}"
        )

    # -----------------------------------------------------------------------------
    # Initialise the bullet rules.
    # -----------------------------------------------------------------------------
    # 1: bullet character(s)
    # -----------------------------------------------------------------------------
    def _init_list_bullet_rules(self) -> dict[str, int]:
        if cfg.glob.setup.lt_list_bullet_rule_file and cfg.glob.setup.lt_list_bullet_rule_file.lower() != "none":
            lt_list_bullet_rule_file_path = utils.get_os_independent_name(cfg.glob.setup.lt_list_bullet_rule_file)
            if os.path.isfile(lt_list_bullet_rule_file_path):
                return self._load_list_bullet_rules_from_json(pathlib.Path(lt_list_bullet_rule_file_path))

            utils.terminate_fatal(
                f"File with bulleted list rule file is missing - " f"file name '{cfg.glob.setup.lt_list_bullet_rule_file}'"
            )

        return {
            "- ": 0,
            ". ": 0,
            "\ufffd ": 0,
            "o ": 0,
            "° ": 0,
            "• ": 0,
            "‣ ": 0,
        }

    # -----------------------------------------------------------------------------
    # Load bulleted list rules from a JSON file.
    # -----------------------------------------------------------------------------
    @staticmethod
    def _load_list_bullet_rules_from_json(
        lt_list_bullet_rule_file: pathlib.Path,
    ) -> dict[str, int]:
        """Load bulleted list rules from a JSON file.

        Args:
            lt_list_bullet_rule_file (Path): JSON file.
        """
        list_bullet_rules = {}

        with open(lt_list_bullet_rule_file, "r", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
            json_data = json.load(file_handle)

            for bullet in json_data[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE_LIST_BULLET_RULES]:
                list_bullet_rules[bullet] = 0

        utils.progress_msg(
            f"The list_bullet rules were successfully loaded from the file {cfg.glob.setup.lt_list_bullet_rule_file}"
        )

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
        para_no = int(line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO])
        text = str(line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

        bullet = ""

        for key, value in self._bullet_rules.items():
            if text[0:value] == key:
                bullet = key
                break

        if not bullet:
            if self._page_idx == self._page_idx_prev and para_no == self._para_no_prev:
                # Paragraph already in progress.
                return

            self._finish_list()
            return

        if (
            bullet != self._bullet
            or self._llx_upper_limit
            <= float(line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX])
            <= self._llx_lower_limit
        ):
            self._finish_list()

        self._bullet = bullet

        if not self._entries:
            # New bulleted paragraph.
            self._line_lines_idx_from = self._line_lines_idx
            self._line_lines_idx_till = self._line_lines_idx
            self._llx_lower_limit = round(
                coord_llx := float(line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_COORD_LLX])
                * (100 - cfg.glob.setup.lt_list_bullet_tolerance_llx)
                / 100,
                2,
            )
            self._llx_upper_limit = round(coord_llx * (100 + cfg.glob.setup.lt_list_bullet_tolerance_llx) / 100, 2)

        self._entries.append((self._page_idx, para_no, self._line_lines_idx))

        self._no_entries += 1

        self._page_idx_prev = self._page_idx
        self._para_no_prev = para_no

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:
        """Process the page-related data."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.progress_msg_line_type_list_bullet(
            f"LineTypeListBullet: Start page                           ={self._page_idx + 1}"
        )

        self._max_line_line = len(cfg.glob.text_parser.parse_result_line_lines)

        for line_lines_idx, line_line in enumerate(cfg.glob.text_parser.parse_result_line_lines):
            self._line_lines_idx = line_lines_idx
            if line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY:
                self._process_line(line_line)

        utils.progress_msg_line_type_list_bullet(
            f"LineTypeListBullet: End   page                           ={self._page_idx + 1}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Reset the document memory.
    # -----------------------------------------------------------------------------
    def _reset_document(self) -> None:
        """Reset the document memory."""
        self._max_page = cfg.glob.text_parser.parse_result_no_pages_in_doc

        self._lists = []

        utils.progress_msg_line_type_list_bullet("LineTypeListBullet: Reset the document memory")

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

        utils.progress_msg_line_type_list_bullet("LineTypeListBullet: Reset the list memory")

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

        utils.progress_msg_line_type_list_bullet("LineTypeListBullet")
        utils.progress_msg_line_type_list_bullet(
            f"LineTypeListBullet: Start document                       ={cfg.glob.action_curr.action_file_name}"
        )

        self._reset_document()

        for page_idx, page in enumerate(cfg.glob.text_parser.parse_result_line_pages):
            self._page_idx = page_idx
            cfg.glob.text_parser.parse_result_line_lines = page[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        self._finish_list()

        if cfg.glob.setup.is_create_extra_file_list_bullet and self._lists:
            full_name_toc = utils.get_full_name(
                cfg.glob.action_curr.action_directory_name,
                cfg.glob.action_curr.get_stem_name()  # type: ignore
                + "_list_bullet."
                + db.cls_document.Document.DOCUMENT_FILE_TYPE_JSON,
            )
            with open(full_name_toc, "w", encoding=cfg.glob.FILE_ENCODING_DEFAULT) as file_handle:
                json.dump(
                    {
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_ID: cfg.glob.document.document_id,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_DOC_FILE_NAME: cfg.glob.document.document_file_name,
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_NO_LISTS_BULLET_IN_DOC: len(self._lists),
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_LISTS_BULLET: self._lists,
                    },
                    file_handle,
                    indent=cfg.glob.setup.json_indent,
                    sort_keys=cfg.glob.setup.is_json_sort_keys,
                )

        utils.progress_msg_line_type_list_bullet(
            f"LineTypeListBullet: End   document                       ={cfg.glob.action_curr.action_file_name}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
