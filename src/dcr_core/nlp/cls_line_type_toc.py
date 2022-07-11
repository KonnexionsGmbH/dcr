"""Module nlp.cls_line_type_toc: Determine table of content lines."""
from __future__ import annotations

import datetime

import dcr_core.nlp.cls_nlp_core


# pylint: disable=too-many-instance-attributes
class LineTypeToc:
    """Determine table of content lines.

    Returns:
        _type_: LineTypeToc instance.
    """

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(
        self,
        lt_toc_last_page: int,
        lt_toc_min_entries: int,
        action_file_name: str = "",
        is_verbose_lt_toc: bool = False,
    ) -> None:
        """Initialise the instance."""
        self._action_file_name = action_file_name
        self._is_verbose_lt_toc = is_verbose_lt_toc
        self._lt_toc_last_page = lt_toc_last_page
        self._lt_toc_min_entries = lt_toc_min_entries

        self._progress_msg("LineTypeToc")
        self._progress_msg(f"LineTypeToc: Start create instance                ={self._action_file_name}")

        self._is_toc_existing = False

        self._page_no = 0

        self._parse_result_line_lines: dcr_core.nlp.cls_nlp_core.NLPCore.LineLines = []

        self._strategy = ""

        # page_no_toc, page_no, paragraph_no, row_no
        self._toc_candidates: list[list[int]] = []

        self.no_lines_toc = 0

        self.parse_result_line_pages: dcr_core.nlp.cls_nlp_core.NLPCore.LinePages = []
        self._parse_result_no_pages_in_doc = 0

        self._exist = True

        self._progress_msg(f"LineTypeToc: End   create instance                ={self._action_file_name}")

    # -----------------------------------------------------------------------------
    # Check a TOC candidate.
    # -----------------------------------------------------------------------------
    def _check_toc_candidate(self) -> None:
        if not self._toc_candidates:
            return

        self._progress_msg(f"LineTypeToc: Start check TOC candidate            ={len(self._toc_candidates)}")

        row_no = 0
        page_no_max = self._parse_result_no_pages_in_doc
        page_no_toc_last = -1

        for [page_no_toc, _, _, _] in self._toc_candidates:
            row_no += 1

            if page_no_toc == -1:
                if row_no != 1:
                    self._init_toc_candidate()
                    self._progress_msg(f"LineTypeToc: End   check TOC candidate (!=)       ={self._is_toc_existing}: {page_no_toc}")
                    return

                continue

            if page_no_toc < page_no_toc_last or page_no_toc > page_no_max:
                self._init_toc_candidate()
                self._progress_msg(f"LineTypeToc: End   check TOC candidate (<>)       ={self._is_toc_existing}: {page_no_toc}")
                return

            page_no_toc_last = page_no_toc

        self._is_toc_existing = True

        self._progress_msg(f"LineTypeToc: End   check TOC candidate            ={self._is_toc_existing}")

    # -----------------------------------------------------------------------------
    # Initialise the TOC candidate variables.
    # -----------------------------------------------------------------------------
    def _init_toc_candidate(self) -> None:
        self._toc_candidates = []

    # -----------------------------------------------------------------------------
    # Process the page-related data - line version.
    # -----------------------------------------------------------------------------
    def _process_page_lines(self) -> None:
        """Process the page-related data - line version."""
        if self._is_toc_existing or self._page_no >= self._lt_toc_last_page:
            return

        self._page_no += 1

        self._progress_msg("LineTypeToc")
        self._progress_msg(f"LineTypeToc: Start page (lines)                   ={self._page_no}")

        for line_line in self._parse_result_line_lines:
            if line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                if (text := line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT]) != "":
                    line_tokens = text.split()
                    try:
                        self._process_toc_candidate_line_line(line_line, int(line_tokens[-1]))
                    except ValueError:
                        self._check_toc_candidate()

                    if self._is_toc_existing:
                        break

        self._progress_msg(f"LineTypeToc: End   page (lines)                   ={self._page_no}")

    # -----------------------------------------------------------------------------
    # Process the page-related data - table version.
    # -----------------------------------------------------------------------------
    def _process_page_table(self) -> None:
        """Process the page-related data - table version."""
        if self._is_toc_existing or self._page_no >= self._lt_toc_last_page:
            return

        self._page_no += 1

        self._progress_msg("LineTypeToc")
        self._progress_msg(f"LineTypeToc: Start page (table)                   ={self._page_no}")

        for line_line in self._parse_result_line_lines:
            if line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                if dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO in line_line:
                    self._process_toc_candidate_table_line(line_line)
                else:
                    self._check_toc_candidate()

                if self._is_toc_existing:
                    break

        self._progress_msg(f"LineTypeToc: End   page (table)                   ={self._page_no}")

    # -----------------------------------------------------------------------------
    # Add a TOC line candidate element.
    # -----------------------------------------------------------------------------
    def _process_toc_candidate_line_line(self, line_line: dcr_core.nlp.cls_nlp_core.NLPCore.LineLine, page_no_toc: int) -> None:
        """Add a TOC line candidate element.

        Args:
            line_line (dcr_core.nlp.cls_nlp_core.NLPCore.LineLine):
                    Document line.
            page_no_toc (int):
                    Page number in the table of contents.
        """
        line_no = line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO]

        para_no = line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]

        self._toc_candidates.append([page_no_toc, self._page_no, para_no, line_no])

    # -----------------------------------------------------------------------------
    # Add a TOC table candidate element.
    # -----------------------------------------------------------------------------
    def _process_toc_candidate_table_line(self, line_line: dcr_core.nlp.cls_nlp_core.NLPCore.LineLine) -> None:
        """Add a TOC table candidate element.

        Args:
            line_line (dcr_core.nlp.cls_nlp_core.NLPCore.LineLine):
                    Document line.
        """
        row_no = line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO]

        para_no = line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]

        if not self._toc_candidates or self._page_no != self._toc_candidates[-1][1] or row_no != self._toc_candidates[-1][3]:
            self._toc_candidates.append([-1, self._page_no, para_no, row_no])

        try:
            self._toc_candidates[-1][0] = int(line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_TEXT])
            self._toc_candidates[-1][2] = para_no
        except ValueError:
            self._toc_candidates[-1][0] = -1

    # -----------------------------------------------------------------------------
    # Create a toc line_type progress message.
    # -----------------------------------------------------------------------------
    def _progress_msg(self, msg: str) -> None:
        """Create a progress message.

        Args:
            msg (str): Progress message.
        """
        if self._is_verbose_lt_toc:
            final_msg = dcr_core.nlp.cls_nlp_core.NLPCore.LOGGER_PROGRESS_UPDATE + str(datetime.datetime.now()) + " : " + msg + "."

            print(final_msg)

    # -----------------------------------------------------------------------------
    # Store the found TOC entries in parser result.
    # -----------------------------------------------------------------------------
    def _store_results(self) -> None:  # noqa: C901
        """Store the found TOC entries in parser result."""
        self._progress_msg("LineTypeToc: Start store result")

        self.no_lines_toc = len(self._toc_candidates)

        if len(self._toc_candidates) < self._lt_toc_min_entries:
            self._progress_msg(f"LineTypeToc: End   store result (min. entries)    ={self.no_lines_toc}")
            self.no_lines_toc = 0
            return

        page_no_from = self._toc_candidates[0][1]
        page_no_till = self._toc_candidates[-1][1]
        para_no_from = self._toc_candidates[0][2]
        para_no_till = self._toc_candidates[-1][2]

        for page in self.parse_result_line_pages:
            page_no = page[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]

            if page_no < page_no_from:
                continue
            if page_no > page_no_till:
                break

            for line_line in page[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]:
                para_no = line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]

                if page_no == page_no_from and para_no < para_no_from:
                    continue
                if page_no == page_no_till and para_no > para_no_till:
                    break

                if self._strategy == dcr_core.nlp.cls_nlp_core.NLPCore.SEARCH_STRATEGY_LINES:
                    for [_, cand_page_no, cand_para_no, cand_line_no] in self._toc_candidates:
                        if (
                            page_no == cand_page_no
                            and para_no == cand_para_no
                            and line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO] == cand_line_no
                        ):
                            line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_TOC
                elif self._strategy == dcr_core.nlp.cls_nlp_core.NLPCore.SEARCH_STRATEGY_TABLE:
                    if dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO in line_line:
                        if line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                            line_line[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = dcr_core.nlp.cls_nlp_core.NLPCore.LINE_TYPE_TOC

        self._progress_msg(f"LineTypeToc: End   store result                   ={self.no_lines_toc}")

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
    def process_document(
        self,
        parse_result_line_pages: dcr_core.nlp.cls_nlp_core.NLPCore.LinePages,
    ) -> None:
        """Process the document related data."""
        if self._lt_toc_last_page == 0:
            return

        self.parse_result_line_pages = parse_result_line_pages

        self._parse_result_no_pages_in_doc = len(parse_result_line_pages)

        self._progress_msg("LineTypeToc")
        self._progress_msg(f"LineTypeToc: Start document                       ={self._action_file_name}")

        # -------------------------------------------------------------------------
        # Examine the table version.
        # -------------------------------------------------------------------------
        self._strategy = dcr_core.nlp.cls_nlp_core.NLPCore.SEARCH_STRATEGY_TABLE

        for page in self.parse_result_line_pages:
            self._parse_result_line_lines = page[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page_table()

        if not self._is_toc_existing:
            self._check_toc_candidate()

        # -------------------------------------------------------------------------
        # Examine the lines version.
        # -------------------------------------------------------------------------
        if not self._is_toc_existing:
            self._strategy = dcr_core.nlp.cls_nlp_core.NLPCore.SEARCH_STRATEGY_LINES
            self._page_no = 0
            self._init_toc_candidate()
            for page in self.parse_result_line_pages:
                self._parse_result_line_lines = page[dcr_core.nlp.cls_nlp_core.NLPCore.JSON_NAME_LINES]
                self._process_page_lines()

            if not self._is_toc_existing:
                self._check_toc_candidate()

        # -------------------------------------------------------------------------
        # Store the results.
        # -------------------------------------------------------------------------
        if self._is_toc_existing:
            self._store_results()

        self._progress_msg(f"LineTypeToc: End   document                       ={self._action_file_name}")
