"""Module nlp.cls_line_type_headers_footers: Determine footer and header
lines."""
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


# pylint: disable=too-many-instance-attributes
class LineTypeHeaderFooters:
    """Determine footer and header lines.

    Returns:
        _type_: LineTypeHeaderFooters instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise the instance."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.check_exists_object(
            is_action_curr=True,
            is_setup=True,
            is_text_parser=True,
        )

        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters")
        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Start create instance                ={cfg.glob.action_curr.action_file_name}"
        )

        self._is_irregular_footer = True
        self._is_irregular_header = True

        self._line_data_max = cfg.glob.setup.lt_header_max_lines + cfg.glob.setup.lt_footer_max_lines
        self._page_ind = -1
        self._page_max = cfg.glob.action_curr.action_no_pdf_pages

        self._line_data: LineData = [((-1, ""), (-1, "")) for _ in range(self._line_data_max)]
        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}"
        )

        self._lsd_data: LSDData = [[(-1, -1, -1) for _ in range(self._page_max)] for _ in range(self._line_data_max)]
        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of lsd_data                    ={self._lsd_data}"
        )

        self._result_data: ResultData = {}

        self._irregular_footer_cand: tuple[int, int] = ()  # type: ignore
        self._irregular_footer_cand_fp: list[tuple[int, int]] = []
        self._irregular_footer_cands: list[tuple[int, int]] = []

        self._irregular_header_cand: tuple[int, int] = ()  # type: ignore
        self._irregular_header_cand_fp: list[tuple[int, int]] = []
        self._irregular_header_cands: list[tuple[int, int]] = []

        self._no_irregular_footer = 0
        self._no_irregular_header = 0

        self.no_lines_footer = 0
        self.no_lines_header = 0

        self._exist = True

        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: End   create instance                ={cfg.glob.action_curr.action_file_name}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Calculate the Levenshtein distances.
    # -----------------------------------------------------------------------------
    def _calc_levenshtein(self) -> None:
        """Calculate the Levenshtein distances."""

        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters")
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters: Start Levenshtein distance")
        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}"
        )

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

        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of lsd_data                    ={self._lsd_data}"
        )
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters: End   Levenshtein distance")

    # -----------------------------------------------------------------------------
    # Try to determine an ascending page number in the footers.
    # -----------------------------------------------------------------------------
    def _check_irregular_footer(self, line_ind: int, text: str) -> None:
        """Try to determine an ascending page number in the footers.

        Args:
            line_ind (int): Line index in page.
            text (str): Line text.
        """
        try:
            page_no_cand = int(text.split()[-1])

            if self._page_ind == 0:
                self._irregular_footer_cand_fp.append((line_ind, page_no_cand))
                return

            if self._page_ind == 1:
                for line, page_no_prev in self._irregular_footer_cand_fp:
                    if page_no_cand == int(page_no_prev) + 1:
                        self._irregular_footer_cands.append((line, page_no_prev))
                        self._irregular_footer_cand = (line_ind, page_no_cand)
                        return
                return

            if page_no_cand == self._irregular_footer_cands[-1][1] + 1:
                self._irregular_footer_cand = (line_ind, page_no_cand)
        except ValueError:
            return

    # -----------------------------------------------------------------------------
    # Try to determine an ascending page number in the headers.
    # -----------------------------------------------------------------------------
    def _check_irregular_header(self, line_ind: int, text: str) -> None:
        """Try to determine an ascending page number in the headers.

        Args:
            line_ind (int): Line index in page.
            text (str): Line text.
        """
        try:
            page_no_cand = int(text.split()[-1])

            if self._page_ind == 0:
                self._irregular_header_cand_fp.append((line_ind, page_no_cand))
                return

            if self._page_ind == 1:
                for line, page_no_prev in self._irregular_header_cand_fp:
                    if page_no_cand == int(page_no_prev) + 1:
                        self._irregular_header_cands.append((line, page_no_prev))
                        self._irregular_header_cand = (line_ind, page_no_cand)
                        return
                return

            if page_no_cand == self._irregular_header_cands[-1][1] + 1:
                self._irregular_header_cand = (line_ind, page_no_cand)
        except ValueError:
            return

    # -----------------------------------------------------------------------------
    # Determine the candidates.
    # -----------------------------------------------------------------------------
    def _determine_candidate(self, distance_max: int, line_ind: int) -> bool:
        """Determine the candidates.

        Args:
            distance_max (int):
                    Distance maximum.
            line_ind (int):
                    Line index.

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
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def _process_page(self) -> None:  # noqa: C901
        """Process the page-related data."""
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self._page_ind += 1

        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters")
        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Start page                           ={self._page_ind + 1}"
        )

        if self._is_irregular_footer:
            self._irregular_footer_cand = ()  # type: ignore

        if self._is_irregular_header:
            self._irregular_header_cand = ()  # type: ignore

        if cfg.glob.setup.lt_header_max_lines > 0:
            self._store_line_data_header()

        if cfg.glob.setup.lt_footer_max_lines > 0:
            self._store_line_data_footer()

        if self._is_irregular_footer:
            if self._page_ind == 0:
                if not self._irregular_footer_cand_fp:
                    self._is_irregular_footer = False
            elif self._irregular_footer_cand:
                self._irregular_footer_cands.append(self._irregular_footer_cand)
            else:
                self._is_irregular_footer = False

        if self._is_irregular_header:
            if self._page_ind == 0:
                if not self._irregular_header_cand_fp:
                    self._is_irregular_header = False
            elif self._irregular_header_cand:
                self._irregular_header_cands.append(self._irregular_header_cand)
            else:
                self._is_irregular_header = False

        if self._page_ind > 0:
            self._calc_levenshtein()

        self._swap_current_previous()

        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: End   page                           ={self._page_ind + 1}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Store the irregular footers and headers.
    # -----------------------------------------------------------------------------
    def _store_irregulars(self) -> None:
        """Store the irregular footers and headers."""
        if self._is_irregular_footer:
            self._no_irregular_footer = 1
            utils.progress_msg_line_type_headers_footers(
                f"LineTypeHeaderFooters: Value of irregular footers           ={self._irregular_footer_cands}"
            )

        if self._is_irregular_header:
            self._no_irregular_header = 1
            utils.progress_msg_line_type_headers_footers(
                f"LineTypeHeaderFooters: Value of irregular headers           ={self._irregular_header_cands}"
            )

        for page_ind, page in enumerate(cfg.glob.text_parser.parse_result_line_pages):
            lines = page[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]

            is_changed = False

            if self._is_irregular_footer and self._irregular_footer_cands:
                if (
                    lines[self._irregular_footer_cands[page_ind][0]][nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]
                    == db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY
                ):
                    lines[self._irregular_footer_cands[page_ind][0]][
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE
                    ] = db.cls_document.Document.DOCUMENT_LINE_TYPE_FOOTER
                    is_changed = True
                else:
                    self._no_irregular_footer = 0

            if self._is_irregular_header and self._irregular_header_cands:
                if (
                    lines[self._irregular_header_cands[page_ind][0]][nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE]
                    == db.cls_document.Document.DOCUMENT_LINE_TYPE_BODY
                ):
                    lines[self._irregular_header_cands[page_ind][0]][
                        nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE
                    ] = db.cls_document.Document.DOCUMENT_LINE_TYPE_HEADER
                    is_changed = True
                else:
                    self._no_irregular_header = 0

            if is_changed:
                cfg.glob.text_parser.parse_result_line_pages[page_ind] = page

        if self._no_irregular_footer != 0 or self._no_irregular_header != 0:
            cfg.glob.document.document_no_lines_footer = self._no_irregular_footer
            cfg.glob.document.document_no_lines_header = self._no_irregular_header
            cfg.glob.document.persist_2_db()  # type: ignore

    # -----------------------------------------------------------------------------
    # Store the footers of the current page.
    # -----------------------------------------------------------------------------
    def _store_line_data_footer(self) -> None:
        """Store the footers of the current page."""
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters")
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters: Start store footers")
        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}"
        )

        if len(cfg.glob.text_parser.parse_result_line_lines) == 0:
            return

        line_lines_ind = len(cfg.glob.text_parser.parse_result_line_lines) - 1

        for ind in range(self._line_data_max - 1, cfg.glob.setup.lt_header_max_lines - 1, -1):
            (_, prev) = self._line_data[ind]

            page_line: dict[str, int | str] = cfg.glob.text_parser.parse_result_line_lines[line_lines_ind]

            text = str(page_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

            if self._is_irregular_footer:
                self._check_irregular_footer(line_lines_ind, text)

            self._line_data[ind] = (
                (
                    int(page_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]) - 1,
                    text,
                ),
                prev,
            )

            if line_lines_ind == 0:
                break

            line_lines_ind -= 1

        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}"
        )
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters: End   store footers")

    # -----------------------------------------------------------------------------
    # Store the headers of the current page.
    # -----------------------------------------------------------------------------
    def _store_line_data_header(self) -> None:
        """Store the headers of the current page."""
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters")
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters: Start store headers")
        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}"
        )

        if len(cfg.glob.text_parser.parse_result_line_lines) == 0:
            return

        line_lines_max = len(cfg.glob.text_parser.parse_result_line_lines)

        for ind in range(cfg.glob.setup.lt_header_max_lines):
            if ind >= line_lines_max:
                break

            (_, prev) = self._line_data[ind]

            page_line: dict[str, int | str] = cfg.glob.text_parser.parse_result_line_lines[ind]

            text = str(page_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT])

            if self._is_irregular_header:
                self._check_irregular_header(ind, text)

            self._line_data[ind] = (
                (
                    int(page_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]) - 1,
                    text,
                ),
                prev,
            )

        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}"
        )
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters: End   store headers")

    # -----------------------------------------------------------------------------
    # Store the found line types in parser result.
    # -----------------------------------------------------------------------------
    def _store_results(self) -> None:
        """Store the found line types in parser result."""
        utils.check_exists_object(
            is_document=True,
        )

        self.no_lines_footer = 0
        self.no_lines_header = 0

        for page in cfg.glob.text_parser.parse_result_line_pages:
            page_no = page[nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]

            for line_line in page[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]:
                line_index_page = int(line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO_PAGE]) - 1
                if (page_no, line_index_page) in self._result_data:
                    line_line[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = self._result_data[(page_no, line_index_page)]
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

        if self.no_lines_footer != 0 or self.no_lines_header != 0:
            cfg.glob.document.document_no_lines_footer = self.no_lines_footer
            cfg.glob.document.document_no_lines_header = self.no_lines_header
            cfg.glob.document.persist_2_db()  # type: ignore

    # -----------------------------------------------------------------------------
    # Swap the current and previous data.
    # -----------------------------------------------------------------------------
    def _swap_current_previous(self) -> None:
        """Swap the current and previous data."""
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters")
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters: Start swap current & previous")
        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}"
        )

        for ind in range(self._line_data_max):
            (curr, _) = self._line_data[ind]
            self._line_data[ind] = ((-1, ""), curr)

        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of line_data                   ={self._line_data}"
        )
        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters: End   swap current & previous")

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
        if cfg.glob.setup.lt_footer_max_lines == 0 and cfg.glob.setup.lt_header_max_lines == 0:
            return

        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        utils.progress_msg_line_type_headers_footers("LineTypeHeaderFooters")
        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Start document                       ={cfg.glob.action_curr.action_file_name}"
        )
        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: Value of lsd_data                    ={self._lsd_data}"
        )

        for page in cfg.glob.text_parser.parse_result_line_pages:
            cfg.glob.text_parser.parse_result_line_lines = page[nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page()

        for line_ind in range(self._line_data_max):
            if line_ind < cfg.glob.setup.lt_header_max_lines:
                distance_max = cfg.glob.setup.lt_header_max_distance
                line_type = db.cls_document.Document.DOCUMENT_LINE_TYPE_HEADER
            else:
                distance_max = cfg.glob.setup.lt_footer_max_distance
                line_type = db.cls_document.Document.DOCUMENT_LINE_TYPE_FOOTER

            if self._determine_candidate(distance_max, line_ind):
                for page_ind in range(self._page_max):
                    (line_no_curr, line_no_prev, distance) = self._lsd_data[line_ind][page_ind]
                    if 0 <= distance <= distance_max:
                        self._result_data[(page_ind, line_no_prev)] = line_type
                        self._result_data[(page_ind + 1, line_no_curr)] = line_type

        if len(self._result_data) > 0:
            utils.progress_msg_line_type_headers_footers(
                f"LineTypeHeaderFooters: Value of result_data                 ={self._result_data}"
            )
            self._store_results()

        if self._is_irregular_footer or self._is_irregular_header:
            self._store_irregulars()
            self.no_lines_footer += self._no_irregular_footer
            self.no_lines_header += self._no_irregular_header

        utils.progress_msg_line_type_headers_footers(
            f"LineTypeHeaderFooters: End document                         ={cfg.glob.action_curr.action_file_name}"
        )

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)
