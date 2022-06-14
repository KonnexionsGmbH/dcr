"""Module nlp.cls_line_type: Determine footer and header lines."""
from __future__ import annotations

import cfg.glob
import db.cls_document
import jellyfish
import nlp.cls_nlp_core
import nlp.cls_text_parser
import utils

# -----------------------------------------------------------------------------
# Global type aliases.
# -----------------------------------------------------------------------------
# line index, line text
LineDataCell = tuple[int, str]
LineDataRow = tuple[LineDataCell, LineDataCell]
LineData = list[LineDataRow]

# line index current page, line index previous page, Levenshtein distance
LSDDataCell = tuple[int, int, int]
LSDDataRow = list[LSDDataCell]
LSDData = list[LSDDataRow]

# page_index, line index
ResultKey = tuple[int, int]
ResultData = dict[ResultKey, str]


class LineType:
    """Determine footer and header lines.

    Returns:
        _type_: LineType instance.
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

        self._line_data_max = cfg.glob.setup.line_header_max_lines + cfg.glob.setup.line_footer_max_lines
        self._page_ind = -1
        self._page_max = cfg.glob.action_curr.action_no_pdf_pages

        self._line_data: LineData = [((-1, ""), (-1, "")) for _ in range(self._line_data_max)]
        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")

        self._lsd_data: LSDData = [[(-1, -1, -1) for _ in range(self._page_max)] for _ in range(self._line_data_max)]
        utils.progress_msg_line_type(f"LineType: Value of lsd_data                    ={self._lsd_data}")

        self._result_data: ResultData = {}

        self._exist = True

        self.no_lines_footer = 0
        self.no_lines_header = 0
        self.no_lines_toc = 0

        utils.progress_msg_line_type(
            f"LineType: End   create instance                ={cfg.glob.action_curr.action_file_name}"
        )

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
    # Footers & Header: Determine the candidates.
    # -----------------------------------------------------------------------------
    def _determine_footers_header_candidate(self, distance_max: int, line_ind: int) -> bool:
        """Footers & Header: Determine the candidates.

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
    # Footers & Header: Store the footers of the current page.
    # -----------------------------------------------------------------------------
    def _store_line_data_footer(self) -> None:
        """Footers & Header: Store the footers of the current page."""
        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type("LineType: Start store footers")
        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")

        if len(cfg.glob.text_parser.parse_result_line_lines) == 0:
            return

        line_lines_ind = len(cfg.glob.text_parser.parse_result_line_lines) - 1

        for ind in range(self._line_data_max - 1, cfg.glob.setup.line_header_max_lines - 1, -1):
            (_, prev) = self._line_data[ind]

            page_line: dict[str, int | str] = cfg.glob.text_parser.parse_result_line_lines[line_lines_ind]

            self._line_data[ind] = (  # type: ignore
                (
                    page_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_INDEX_PAGE],
                    page_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT],
                ),
                prev,
            )

            if line_lines_ind == 0:
                break

            line_lines_ind -= 1

        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")
        utils.progress_msg_line_type("LineType: End   store footers")

    # -----------------------------------------------------------------------------
    # Footers & Header: Store the headers of the current page.
    # -----------------------------------------------------------------------------
    def _store_line_data_header(self) -> None:
        """Footers & Header: Store the headers of the current page."""
        utils.progress_msg_line_type("LineType")
        utils.progress_msg_line_type("LineType: Start store headers")
        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")

        if len(cfg.glob.text_parser.parse_result_line_lines) == 0:
            return

        line_lines_max = len(cfg.glob.text_parser.parse_result_line_lines)

        for ind in range(cfg.glob.setup.line_header_max_lines):
            if ind >= line_lines_max:
                break

            (_, prev) = self._line_data[ind]

            page_line: dict[str, int | str] = cfg.glob.text_parser.parse_result_line_lines[ind]

            self._line_data[ind] = (  # type: ignore
                (
                    page_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_INDEX_PAGE],
                    page_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT],
                ),
                prev,
            )

        utils.progress_msg_line_type(f"LineType: Value of line_data                   ={self._line_data}")
        utils.progress_msg_line_type("LineType: End   store headers")

    # -----------------------------------------------------------------------------
    # Footers & Header: Store the found line types in parser result.
    # -----------------------------------------------------------------------------
    def _store_results_footers_header(self) -> None:
        """Footers & Header: Store the found line types in parser result."""
        self.no_lines_footer = 0
        self.no_lines_header = 0

        for page in cfg.glob.text_parser.parse_result_line_pages:
            page_no = page[nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]
            lines = page[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]

            for line in lines:
                line_index_page = line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_INDEX_PAGE]
                if (page_no, line_index_page) in self._result_data:
                    line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = self._result_data[(page_no, line_index_page)]
                    if page_no == 2:
                        if (
                            self._result_data[(page_no, line_index_page)]
                            == db.cls_document.Document.DOCUMENT_LINE_TYPE_FOOTER
                        ):
                            self.no_lines_footer += 1
                        elif (
                            self._result_data[(page_no, line_index_page)]
                            == db.cls_document.Document.DOCUMENT_LINE_TYPE_HEADER
                        ):
                            self.no_lines_header += 1

    # -----------------------------------------------------------------------------
    # Footers & Header: Swap the current and previous data.
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
    # Footers & Header: Process the document related data.
    # -----------------------------------------------------------------------------
    def footers_header_process_document(self) -> None:
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

            if self._determine_footers_header_candidate(distance_max, line_ind):
                for page_ind in range(self._page_max):
                    (line_no_curr, line_no_prev, distance) = self._lsd_data[line_ind][page_ind]
                    if 0 <= distance <= distance_max:
                        self._result_data[(page_ind, line_no_prev)] = line_type
                        self._result_data[(page_ind + 1, line_no_curr)] = line_type

        if len(self._result_data) > 0:
            utils.progress_msg_line_type(f"LineType: Value of result_data                 ={self._result_data}")
            self._store_results_footers_header()

        utils.progress_msg_line_type(
            f"LineType: End document                         ={cfg.glob.action_curr.action_file_name}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Footers & Header: Process the page-related data.
    # -----------------------------------------------------------------------------
    def footers_header_process_page(self) -> None:
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
