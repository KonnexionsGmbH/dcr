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
        _type_: Instance object.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        # [ (line_ind, line_text) ]
        self._line_text_footer_curr: List[Tuple[int, str]] = []
        self._line_text_footer_prev: List[Tuple[int, str]] = []
        self._line_text_header_curr: List[Tuple[int, str]] = []
        self._line_text_header_prev: List[Tuple[int, str]] = []

        # [ [ (line_ind, line_ind, distance) ] ]_page_no
        self._page_lines_distance_footer: List[List[Tuple[int, int, int]]] = []
        self._page_lines_distance_header: List[List[Tuple[int, int, int]]] = []

        # [ (page_no, line_ind, line_type) ]
        self._page_line_type: List[Tuple[int, int, str]] = []

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Calculate the Levenshtein distances.
    # -----------------------------------------------------------------------------
    # Example : [ [ (line_ind, line_ind, distance) ] ]_page_no:
    #
    # page_lines_distance_header = [[(0, 0, 0), (1, 1, 0), (2, 2, 0)],
    #                               [(0, 0, 0), (1, 1, 0), (2, 2, 0)]]
    # page_lines_distance_footer = [[(8, 8, 0), (9, 9, 1), (10, 10, 0)],
    #                               [(8, 8, 0), (9, 9, 1), (10, 10, 0)]]
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

        page_lines_distance: List[Tuple[int, int, int]] = []

        for ind in range(no_lines):
            (curr_line_no, curr_line_text) = line_text_curr[ind]
            (prev_line_no, prev_line_text) = line_text_prev[ind]
            if curr_line_no == -1:
                page_lines_distance.append((prev_line_no, curr_line_no, -1))
            else:
                page_lines_distance.append(
                    (
                        prev_line_no,
                        curr_line_no,
                        jellyfish.levenshtein_distance(
                            prev_line_text,
                            curr_line_text,
                        ),
                    )
                )

        utils.progress_msg_line_type(f"LineType: Value of page_lines_distance       ={page_lines_distance}")

        return page_lines_distance

    # -----------------------------------------------------------------------------
    # Save the footers of the current page.
    # -----------------------------------------------------------------------------
    # Example : [ (line_ind, line_text) ]:
    #
    # line_text_footer_curr = [(8, 'Footer 2'),
    #                          (9, 'Footer 3 pg. 1'),
    #                          (10, 'Footer 4')]
    # -----------------------------------------------------------------------------
    def _save_lines_footer_curr(self, page_lines: List[Dict[str, int | str]]) -> None:
        """Save the footers of the current page.

        Args:
            page_lines (List[Dict[str, int | str]]):
                    All lines of the current page.
        """
        count = len(page_lines) - cfg.glob.setup.line_footer_max_lines

        self._line_text_footer_curr = []

        for _ in range(cfg.glob.setup.line_footer_max_lines):
            if count < 0:
                self._line_text_footer_curr.append((-1, cfg.glob.INFORMATION_NOT_YET_AVAILABLE))
            else:
                page_line: Dict[str, int | str] = page_lines[count]
                self._line_text_footer_curr.append(
                    (
                        page_line[cfg.glob.JSON_NAME_LINE_INDEX_PAGE],
                        page_line[cfg.glob.JSON_NAME_LINE_TEXT],
                    )  # type: ignore
                )
            count += 1

        utils.progress_msg_line_type(f"LineType: Value of line_text_footer_prev     ={self._line_text_footer_prev}")
        utils.progress_msg_line_type(f"LineType: Value of line_text_footer_curr     ={self._line_text_footer_curr}")

    # -----------------------------------------------------------------------------
    # Save the headers of the current page.
    # -----------------------------------------------------------------------------
    # Example : [ (line_ind, line_text) ]:
    #
    # line_text_header_curr = [(0, 'Header 1'),
    #                          (1, 'Header 2'),
    #                          (2, 'Header 3')]
    # -----------------------------------------------------------------------------
    def _save_lines_header_curr(self, page_lines: List[Dict[str, int | str]]) -> None:
        """Save the headers of the current page.

        Args:
            page_lines (List[Dict[str, int | str]]):
                    All lines of the current page.
        """
        page_lines_max = len(page_lines)

        self._line_text_header_curr = []

        for ind in range(cfg.glob.setup.line_header_max_lines):
            if ind < page_lines_max:
                page_line: Dict[str, int | str] = page_lines[ind]
                self._line_text_header_curr.append(
                    (
                        page_line[cfg.glob.JSON_NAME_LINE_INDEX_PAGE],
                        page_line[cfg.glob.JSON_NAME_LINE_TEXT],
                    )  # type: ignore
                )
            else:
                self._line_text_header_curr.append((-1, cfg.glob.INFORMATION_NOT_YET_AVAILABLE))

        utils.progress_msg_line_type(f"LineType: Value of line_text_header_prev     ={self._line_text_header_prev}")
        utils.progress_msg_line_type(f"LineType: Value of line_text_header_curr     ={self._line_text_header_curr}")

    # -----------------------------------------------------------------------------
    # Determine the footer lines.
    # -----------------------------------------------------------------------------
    def determine_footer_lines(self, page_ind_max: int) -> None:
        """Determine the footer lines.

        Args:
            page_ind_max (int): Highest page index.
        """
        utils.progress_msg_line_type(
            f"LineType: Value of page_lines_distance_footer={self._page_lines_distance_footer}"
        )

        for line in range(cfg.glob.setup.line_footer_max_lines):
            distance_rest = 0
            for page in range(1, page_ind_max):
                (_, _, distance) = self._page_lines_distance_footer[page][line]
                if distance > cfg.glob.setup.line_footer_max_distance:
                    distance_rest = distance
                    if page > 0:
                        break

            if distance_rest > cfg.glob.setup.line_footer_max_distance:
                continue

            (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_footer[0][line]
            if distance <= cfg.glob.setup.line_footer_max_distance:
                self._page_line_type.append((1, line_ind_prev, cfg.glob.DOCUMENT_LINE_TYPE_FOOTER))

            if page_ind_max == 1:
                continue

            for page in range(1, page_ind_max + 1):
                (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_footer[page][line]
                self._page_line_type.append((page + 1, line_ind_prev, cfg.glob.DOCUMENT_LINE_TYPE_FOOTER))

            (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_footer[page_ind_max][line]
            if distance <= cfg.glob.setup.line_footer_max_distance:
                self._page_line_type.append((page_ind_max + 2, line_ind_curr, cfg.glob.DOCUMENT_LINE_TYPE_FOOTER))

    # -----------------------------------------------------------------------------
    # Determine the header lines.
    # -----------------------------------------------------------------------------
    def determine_header_lines(self, page_ind_max: int) -> None:
        """Determine the header lines.

        Args:
            page_ind_max (int): Highest page index.
        """
        utils.progress_msg_line_type(
            f"LineType: Value of page_lines_distance_header={self._page_lines_distance_header}"
        )

        for line in range(cfg.glob.setup.line_header_max_lines):
            distance_rest = 0
            for page in range(1, page_ind_max):
                (_, _, distance) = self._page_lines_distance_header[page][line]
                if distance > cfg.glob.setup.line_header_max_distance:
                    distance_rest = distance
                    if page > 0:
                        break

            if distance_rest > cfg.glob.setup.line_header_max_distance:
                continue

            (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_header[0][line]
            if distance <= cfg.glob.setup.line_header_max_distance:
                self._page_line_type.append((1, line_ind_prev, cfg.glob.DOCUMENT_LINE_TYPE_HEADER))

            if page_ind_max == 1:
                continue

            for page in range(1, page_ind_max + 1):
                (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_header[page][line]
                self._page_line_type.append((page + 1, line_ind_prev, cfg.glob.DOCUMENT_LINE_TYPE_HEADER))

            (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_header[page_ind_max][line]
            if distance <= cfg.glob.setup.line_header_max_distance:
                self._page_line_type.append((page_ind_max + 2, line_ind_curr, cfg.glob.DOCUMENT_LINE_TYPE_HEADER))

    # -----------------------------------------------------------------------------
    # Process the document related data.
    # -----------------------------------------------------------------------------
    def process_document(self, line_pages: List[Dict[str, int | str | List[Dict[str, int | str]]]]) -> None:
        """Process the document related data.

        Args:
            line_pages (List[Dict[str, int  |  str  |  List[Dict[str, int  |  str]]]]):
                    All document pages.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        page_ind_max = len(self._page_lines_distance_header)

        if page_ind_max == 0:
            return

        page_ind_max -= 1

        if cfg.glob.setup.line_header_max_lines > 0:
            self.determine_header_lines(page_ind_max)

        if cfg.glob.setup.line_footer_max_lines > 0:
            self.determine_footer_lines(page_ind_max)

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def process_page(self, page_no: int, line_lines: List[Dict[str, int | str]]) -> None:
        """Process the page-related data.

        Args:
            page_no (int):
                    The number of the current page.
            line_lines (List[Dict[str, int  |  str]]):
                    The content of the current page._description_
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        if cfg.glob.setup.line_header_max_lines > 0:
            self._save_lines_header_curr(
                line_lines,
            )
            if page_no > 1:
                self._page_lines_distance_header.append(
                    self._calc_levenshtein(
                        self._line_text_header_prev,
                        self._line_text_header_curr,
                    )
                )
            # Swap the page-related headers.
            self._line_text_header_prev = self._line_text_header_curr
            self._line_text_header_curr = []

        if cfg.glob.setup.line_footer_max_lines > 0:
            self._save_lines_footer_curr(
                line_lines,
            )
            if page_no > 1:
                self._page_lines_distance_footer.append(
                    self._calc_levenshtein(
                        self._line_text_footer_prev,
                        self._line_text_footer_curr,
                    )
                )
            # Swap the page-related footers.
            self._line_text_footer_prev = self._line_text_footer_curr
            self._line_text_footer_curr = []

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
