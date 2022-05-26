"""Module nlp.cls_line_type: Determine footer and header lines."""
from __future__ import annotations

from typing import Dict
from typing import List
from typing import Tuple

import cfg.glob
import db.cls_document
import jellyfish
import nlp.cls_text_parser
import utils

# -----------------------------------------------------------------------------
# Global type aliases.
# -----------------------------------------------------------------------------
# line index, line text
LineDataCell = Tuple[int, str]
LineDataRow = Tuple[LineDataCell, LineDataCell]
LineData = List[LineDataRow]

# line index current page, line index previous page, Levenshtein distance
LSDDataCell = Tuple[int, int, int]
LSDDataRow = List[LSDDataCell]
LSDData = List[LSDDataRow]

# page_index, line index
ResultKey = Tuple[int, int]
ResultData = Dict[ResultKey, str]


# pylint: disable=R0902
# pylint: disable=R0903


class LineType:
    """Determine footer and header lines.

    Returns:
        _type_: LineType instance.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    _JSON_NAME_LINE_INDEX_PAGE: str = "lineIndexPage"
    _JSON_NAME_LINE_TEXT: str = "lineText"

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

        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type(
            f"LineType: Start create instance                ={cfg.glob.action_curr.action_file_name}"
        )

        self._line_data_max: int = cfg.glob.setup.line_header_max_lines + cfg.glob.setup.line_footer_max_lines
        self._page_ind: int = -1
        self._page_max: int = cfg.glob.action_curr.action_no_pdf_pages

        self._line_data: LineData = [((-1, ""), (-1, "")) for _ in range(self._line_data_max)]
        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")

        self._lsd_data: LSDData = [[(-1, -1, -1) for _ in range(self._page_max)] for _ in range(self._line_data_max)]
        utils.progress_msg_line_type(f"LineType: Value of lsd_data                    ={self._lsd_data}")

        self._result_data: ResultData = {}

        self._exist = True

        utils.progress_msg_line_type(
            f"LineType: End   create instance                ={cfg.glob.action_curr.action_file_name}"
        )
        # old ............

        # [ ( (line_ind_curr, line_text_curr), (line_ind_prev, line_text_prev) ) ]
        self._line_text_footer: List[Tuple[Tuple[int, str], Tuple[int, str]]] = []
        self._line_text_header: List[Tuple[Tuple[int, str], Tuple[int, str]]] = []

        # [ [ (line_ind, line_ind, distance) ] ]_page_no
        self._line_1_lines_distance_footer: List[List[Tuple[int, int, int]]] = []
        self._line_1_lines_distance_header: List[List[Tuple[int, int, int]]] = []

        # [ (page_no, line_ind, line_type) ]
        self._page_line_type: List[Tuple[int, int, str]] = []

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Calculate the Levenshtein distances.
    # -----------------------------------------------------------------------------
    def _calc_levenshtein(self) -> None:
        """Calculate the Levenshtein distances."""

        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type("LineType: Start Levenshtein distance")
        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")

        for ind in range(self._line_data_max):
            ((curr_line_ind, curr_line), (prev_line_ind, prev_line)) = self._line_data[ind]
            if curr_line_ind != -1:
                if prev_line_ind != -1:
                    distance = jellyfish.levenshtein_distance(
                        prev_line,
                        curr_line,
                    )

                    lsd_row = self._lsd_data[ind]
                    lsd_row[self._page_ind] = (curr_line_ind, prev_line_ind, distance)
                    self._lsd_data[ind] = lsd_row

        utils.progress_msg_line_type(f"LineType: Value of lsd_data                    ={self._lsd_data}")
        utils.progress_msg_line_type("LineType: End   Levenshtein distance")

    # -----------------------------------------------------------------------------
    # Determine the special line candidates.
    # -----------------------------------------------------------------------------
    def _determine_special_line_candidate(self, distance_max: int, line_ind: int) -> bool:
        """Determine the special line candidates.

        Args:
            distance_max (int): Distance maximum..
            line_ind (int): Line index.

        Returns:
            bool: True if a special line candidate.
        """
        is_empty_line = True
        is_special_line = True

        for page_ind in range(self._page_max):
            (_, _, distance) = self._lsd_data[line_ind][page_ind]

            # no line existing
            if distance == -1:
                if page_ind <= 1 or page_ind == self._page_max - 1:
                    continue

                is_special_line = False
                break

            is_empty_line = False

            # processing a header line
            if distance <= distance_max:
                continue

            if page_ind == 1 or page_ind >= self._page_max - 1:
                if self._page_max > 2:
                    continue

            is_special_line = False
            break

        if is_empty_line:
            return False

        return is_special_line

    # -----------------------------------------------------------------------------
    # Store the footers of the current page.
    # -----------------------------------------------------------------------------
    def _store_line_data_footer(self) -> None:
        """Store the footers of the current page."""
        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type("LineType: Start store footers")
        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")

        if len(cfg.glob.text_parser.parse_result_line_1_lines) == 0:
            return

        line_1_lines_ind = len(cfg.glob.text_parser.parse_result_line_1_lines) - 1

        for ind in range(self._line_data_max - 1, cfg.glob.setup.line_header_max_lines - 1, -1):
            (_, prev) = self._line_data[ind]

            page_line: Dict[str, int | str] = cfg.glob.text_parser.parse_result_line_1_lines[line_1_lines_ind]

            self._line_data[ind] = (  # type: ignore
                (
                    page_line[LineType._JSON_NAME_LINE_INDEX_PAGE],
                    page_line[LineType._JSON_NAME_LINE_TEXT],
                ),
                prev,
            )

            if line_1_lines_ind == 0:
                break

            line_1_lines_ind -= 1

        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")
        utils.progress_msg_line_type("LineType: End   store footers")

    # -----------------------------------------------------------------------------
    # Store the headers of the current page.
    # -----------------------------------------------------------------------------
    def _store_line_data_header(self) -> None:
        """Store the headers of the current page."""
        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type("LineType: Start store headers")
        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")

        if len(cfg.glob.text_parser.parse_result_line_1_lines) == 0:
            return

        line_1_lines_max = len(cfg.glob.text_parser.parse_result_line_1_lines)

        for ind in range(cfg.glob.setup.line_header_max_lines):
            if ind >= line_1_lines_max:
                break

            (_, prev) = self._line_data[ind]

            page_line: Dict[str, int | str] = cfg.glob.text_parser.parse_result_line_1_lines[ind]

            self._line_data[ind] = (  # type: ignore
                (
                    page_line[LineType._JSON_NAME_LINE_INDEX_PAGE],
                    page_line[LineType._JSON_NAME_LINE_TEXT],
                ),
                prev,
            )

        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")
        utils.progress_msg_line_type("LineType: End   store headers")

    # -----------------------------------------------------------------------------
    # Store the found line types in parser result.
    # -----------------------------------------------------------------------------
    def _store_results(self) -> None:
        """Store the found line types in parser result."""
        for page in cfg.glob.text_parser.parse_result_line_3_pages:
            page_no = page[nlp.cls_text_parser.TextParser.JSON_NAME_PAGE_NO]
            lines = page[nlp.cls_text_parser.TextParser.JSON_NAME_LINES]

            for line in lines:
                line_index_page = line[nlp.cls_text_parser.TextParser.JSON_NAME_LINE_INDEX_PAGE]
                if (page_no, line_index_page) in self._result_data:
                    line[nlp.cls_text_parser.TextParser.JSON_NAME_LINE_TYPE] = self._result_data[(page_no, line_index_page)]

    # -----------------------------------------------------------------------------
    # Swap the current and previous data.
    # -----------------------------------------------------------------------------
    def _swap_current_previous(self) -> None:
        """Swap the current and previous data."""
        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type("LineType: Start swap current & previous")
        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")

        for ind in range(self._line_data_max):
            (curr, _) = self._line_data[ind]
            self._line_data[ind] = ((-1, ""), curr)

        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")
        utils.progress_msg_line_type("LineType: End   swap current & previous")

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
        if cfg.glob.setup.line_footer_max_lines == 0 and cfg.glob.setup.line_header_max_lines == 0:
            return

        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type(
            f"LineType: Start document                       ={cfg.glob.action_curr.action_file_name}"
        )
        utils.progress_msg_line_type(f"LineType: Value of lsd_data                    ={self._lsd_data}")

        for line_ind in range(self._line_data_max):
            if line_ind < cfg.glob.setup.line_header_max_lines:
                distance_max = cfg.glob.setup.line_header_max_distance
                line_type = db.cls_document.Document.DOCUMENT_LINE_TYPE_HEADER
            else:
                distance_max = cfg.glob.setup.line_footer_max_distance
                line_type = db.cls_document.Document.DOCUMENT_LINE_TYPE_FOOTER

            if self._determine_special_line_candidate(distance_max, line_ind):
                for page_ind in range(self._page_max):
                    (line_no_curr, line_no_prev, distance) = self._lsd_data[line_ind][page_ind]
                    if 0 <= distance <= distance_max:
                        self._result_data[(page_ind, line_no_prev)] = line_type
                        self._result_data[(page_ind + 1, line_no_curr)] = line_type

        if len(self._result_data) > 0:
            utils.progress_msg_line_type(f"LineType: Value of result_data                 ={self._result_data}")
            self._store_results()

        utils.progress_msg_line_type(
            f"LineType: End document                         ={cfg.glob.action_curr.action_file_name}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def process_page(self) -> None:
        """Process the page-related data."""
        if cfg.glob.setup.line_footer_max_lines == 0 and cfg.glob.setup.line_header_max_lines == 0:
            return

        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._page_ind += 1

        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type(f"LineType: Start page                           ={self._page_ind + 1}")

        if cfg.glob.setup.line_header_max_lines > 0:
            self._store_line_data_header()

        if cfg.glob.setup.line_footer_max_lines > 0:
            self._store_line_data_footer()

        if self._page_ind > 0:
            self._calc_levenshtein()

        self._swap_current_previous()

        utils.progress_msg_line_type(f"LineType: End   page                           ={self._page_ind + 1}")

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
