"""Module nlp.cls_line_type: Determine footer and header lines."""
from __future__ import annotations

from typing import Dict
from typing import List
from typing import Tuple

import cfg.glob
import jellyfish
import utils


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

        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type(
            f"LineType: Start document                       ={cfg.glob.action_curr.action_file_name}"
        )

        # [ (line_ind, line_text) ]
        self._line_text_footer_curr: List[Tuple[int, str]] = []
        self._line_text_footer_prev: List[Tuple[int, str]] = []
        self._line_text_header_curr: List[Tuple[int, str]] = []
        self._line_text_header_prev: List[Tuple[int, str]] = []

        # [ [ (line_ind, line_ind, distance) ] ]_page_no
        self._line_1_lines_distance_footer: List[List[Tuple[int, int, int]]] = []
        self._line_1_lines_distance_header: List[List[Tuple[int, int, int]]] = []

        # [ (page_no, line_ind, line_type) ]
        self._page_line_type: List[Tuple[int, int, str]] = []

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Calculate the Levenshtein distances.
    # -----------------------------------------------------------------------------
    # Example : [ [ (line_ind, line_ind, distance) ] ]_page_no:
    #
    # line_1_lines_distance_header = [[(0, 0, 0), (1, 1, 0), (2, 2, 0)],
    #                                [(0, 0, 0), (1, 1, 0), (2, 2, 0)]]
    # line_1_lines_distance_footer = [[(8, 8, 0), (9, 9, 1), (10, 10, 0)],
    #                                [(8, 8, 0), (9, 9, 1), (10, 10, 0)]]
    # -----------------------------------------------------------------------------
    @staticmethod
    def _calc_levenshtein(
        line_text_prev: List[Tuple[int, str]],
        line_text_curr: List[Tuple[int, str]],
    ) -> List[Tuple[int, int, int]]:
        """Calculate the Levenshtein distances.

        Args:
            line_text_prev (List[Tuple[int, str]):
                    The potential footer or header lines of the previous page.
            line_text_curr (List[Tuple[int, str]):
                    The potential footer or header lines of the current page.

        Returns:
            List[Tuple[int, int, int]]:
                    List of tuples representing previous line no.,
                    current line no. and Levenshtein distance
        """
        no_lines = len(line_text_curr)

        line_1_lines_distance: List[Tuple[int, int, int]] = []

        for ind in range(no_lines):
            (curr_line_no, curr_line_text) = line_text_curr[ind]
            (prev_line_no, prev_line_text) = line_text_prev[ind]
            if curr_line_no == -1:
                line_1_lines_distance.append((prev_line_no, curr_line_no, -1))
            else:
                line_1_lines_distance.append(
                    (
                        prev_line_no,
                        curr_line_no,
                        jellyfish.levenshtein_distance(
                            prev_line_text,
                            curr_line_text,
                        ),
                    )
                )

        utils.progress_msg_line_type(f"LineType: Value of line_1_lines_distance       ={line_1_lines_distance}")

        return line_1_lines_distance

    # -----------------------------------------------------------------------------
    # Save the footers of the current page.
    # -----------------------------------------------------------------------------
    # Example : [ (line_ind, line_text) ]:
    #
    # line_text_footer_curr = [(8, 'Footer 2'),
    #                          (9, 'Footer 3 pg. 1'),
    #                          (10, 'Footer 4')]
    # -----------------------------------------------------------------------------
    def _save_lines_footer_curr(self) -> None:
        """Save the footers of the current page."""
        line_1_lines_max = len(cfg.glob.text_parser.parse_result_line_1_lines) - cfg.glob.setup.line_footer_max_lines

        self._line_text_footer_curr = []

        for _ in range(cfg.glob.setup.line_footer_max_lines):
            if line_1_lines_max < 0:
                self._line_text_footer_curr.append((-1, cfg.glob.INFORMATION_NOT_YET_AVAILABLE))
            else:
                line_1_line: Dict[str, int | str] = cfg.glob.text_parser.parse_result_line_1_lines[line_1_lines_max]
                self._line_text_footer_curr.append(
                    (
                        line_1_line[LineType._JSON_NAME_LINE_INDEX_PAGE],
                        line_1_line[LineType._JSON_NAME_LINE_TEXT],
                    )  # type: ignore
                )
            line_1_lines_max += 1

        if cfg.glob.text_parser.parse_result_no_pages_in_doc > 1:
            utils.progress_msg_line_type(
                f"LineType: Value of line_text_footer_prev       ={self._line_text_footer_prev}"
            )
            utils.progress_msg_line_type(
                f"LineType: Value of line_text_footer_curr       ={self._line_text_footer_curr}"
            )

    # -----------------------------------------------------------------------------
    # Save the headers of the current page.
    # -----------------------------------------------------------------------------
    # Example : [ (line_ind, line_text) ]:
    #
    # line_text_header_curr = [(0, 'Header 1'),
    #                          (1, 'Header 2'),
    #                          (2, 'Header 3')]
    # -----------------------------------------------------------------------------
    def _save_lines_header_curr(self) -> None:
        """Save the headers of the current page."""
        line_1_lines_max = len(cfg.glob.text_parser.parse_result_line_1_lines)

        self._line_text_header_curr = []

        for ind in range(cfg.glob.setup.line_header_max_lines):
            if ind < line_1_lines_max:
                page_line: Dict[str, int | str] = cfg.glob.text_parser.parse_result_line_1_lines[ind]
                self._line_text_header_curr.append(
                    (
                        page_line[LineType._JSON_NAME_LINE_INDEX_PAGE],
                        page_line[LineType._JSON_NAME_LINE_TEXT],
                    )  # type: ignore
                )
            else:
                self._line_text_header_curr.append((-1, cfg.glob.INFORMATION_NOT_YET_AVAILABLE))

        if cfg.glob.text_parser.parse_result_no_pages_in_doc > 1:
            utils.progress_msg_line_type(
                f"LineType: Value of line_text_header_prev       ={self._line_text_header_prev}"
            )
            utils.progress_msg_line_type(
                f"LineType: Value of line_text_header_curr       ={self._line_text_header_curr}"
            )

    # -----------------------------------------------------------------------------
    # Determine the footer lines.
    # -----------------------------------------------------------------------------
    def determine_footer_lines(self, page_ind_max: int) -> None:  # noqa: C901
        """Determine the footer lines.

        Args:
            page_ind_max (int): Highest page index.
        """
        if cfg.glob.text_parser.parse_result_no_pages_in_doc > 1:
            utils.progress_msg_line_type(
                f"LineType: Value of line_1_lines_distance_footer={self._line_1_lines_distance_footer}"
            )

        for line in range(cfg.glob.setup.line_footer_max_lines):
            distance_rest = 0
            for page in range(1, page_ind_max):
                (_, _, distance) = self._line_1_lines_distance_footer[page][line]
                if distance > cfg.glob.setup.line_footer_max_distance:
                    distance_rest = distance
                    if page > 0:
                        break

            if distance_rest > cfg.glob.setup.line_footer_max_distance:
                continue

            (line_ind_prev, line_ind_curr, distance) = self._line_1_lines_distance_footer[0][line]
            if distance <= cfg.glob.setup.line_footer_max_distance:
                self._page_line_type.append((1, line_ind_prev, cfg.glob.DOCUMENT_LINE_TYPE_FOOTER))

            if page_ind_max == 1:
                continue

            for page in range(1, page_ind_max + 1):
                (line_ind_prev, line_ind_curr, distance) = self._line_1_lines_distance_footer[page][line]
                self._page_line_type.append((page + 1, line_ind_prev, cfg.glob.DOCUMENT_LINE_TYPE_FOOTER))

            (line_ind_prev, line_ind_curr, distance) = self._line_1_lines_distance_footer[page_ind_max][line]
            if distance <= cfg.glob.setup.line_footer_max_distance:
                self._page_line_type.append((page_ind_max + 2, line_ind_curr, cfg.glob.DOCUMENT_LINE_TYPE_FOOTER))

    # -----------------------------------------------------------------------------
    # Determine the header lines.
    # -----------------------------------------------------------------------------
    def determine_header_lines(self, page_ind_max: int) -> None:  # noqa: C901
        """Determine the header lines.

        Args:
            page_ind_max (int): Highest page index.
        """
        if cfg.glob.text_parser.parse_result_no_pages_in_doc > 2:
            utils.progress_msg_line_type(
                f"LineType: Value of line_1_lines_distance_header={self._line_1_lines_distance_header}"
            )

        for line in range(cfg.glob.setup.line_header_max_lines):
            distance_rest = 0
            for page in range(1, page_ind_max):
                (_, _, distance) = self._line_1_lines_distance_header[page][line]
                if distance > cfg.glob.setup.line_header_max_distance:
                    distance_rest = distance
                    if page > 0:
                        break

            if distance_rest > cfg.glob.setup.line_header_max_distance:
                continue

            (line_ind_prev, line_ind_curr, distance) = self._line_1_lines_distance_header[0][line]
            if distance <= cfg.glob.setup.line_header_max_distance:
                self._page_line_type.append((1, line_ind_prev, cfg.glob.DOCUMENT_LINE_TYPE_HEADER))

            if page_ind_max == 1:
                continue

            for page in range(1, page_ind_max + 1):
                (line_ind_prev, line_ind_curr, distance) = self._line_1_lines_distance_header[page][line]
                self._page_line_type.append((page + 1, line_ind_prev, cfg.glob.DOCUMENT_LINE_TYPE_HEADER))

            (line_ind_prev, line_ind_curr, distance) = self._line_1_lines_distance_header[page_ind_max][line]
            if distance <= cfg.glob.setup.line_header_max_distance:
                self._page_line_type.append((page_ind_max + 2, line_ind_curr, cfg.glob.DOCUMENT_LINE_TYPE_HEADER))

    # -----------------------------------------------------------------------------
    # Process the document related data.
    # -----------------------------------------------------------------------------
    def process_document(self) -> None:
        """Process the document related data."""
        if cfg.glob.setup.line_footer_max_lines == 0 and cfg.glob.setup.line_header_max_lines == 0:
            return

        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.progress_msg_line_type("LineType")

        page_ind_max = len(self._line_1_lines_distance_header)

        if page_ind_max == 0:
            return

        page_ind_max -= 1

        if cfg.glob.setup.line_header_max_lines > 0:
            self.determine_header_lines(page_ind_max)

        if cfg.glob.setup.line_footer_max_lines > 0:
            self.determine_footer_lines(page_ind_max)

        utils.progress_msg_line_type(f"LineType: Value of page_line_type              ={self._page_line_type}")

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

        utils.progress_msg_line_type(
            f"LineType: Start page                           ={cfg.glob.text_parser.parse_result_no_pages_in_doc}"
        )

        if cfg.glob.setup.line_header_max_lines > 0:
            self._save_lines_header_curr()
            if cfg.glob.text_parser.parse_result_no_pages_in_doc > 1:
                self._line_1_lines_distance_header.append(
                    self._calc_levenshtein(
                        self._line_text_header_prev,
                        self._line_text_header_curr,
                    )
                )
            # Swap the page-related headers.
            self._line_text_header_prev = self._line_text_header_curr
            self._line_text_header_curr = []

        if cfg.glob.setup.line_footer_max_lines > 0:
            self._save_lines_footer_curr()
            if cfg.glob.text_parser.parse_result_no_pages_in_doc > 1:
                self._line_1_lines_distance_footer.append(
                    self._calc_levenshtein(
                        self._line_text_footer_prev,
                        self._line_text_footer_curr,
                    )
                )
            # Swap the page-related footers.
            self._line_text_footer_prev = self._line_text_footer_curr
            self._line_text_footer_curr = []

        utils.progress_msg_line_type(
            f"LineType: End   page                           ={cfg.glob.text_parser.parse_result_no_pages_in_doc}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
