import dcr_core.cls_nlp_core
import dcr_core.core_glob
import dcr_core.core_utils


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
        file_name_curr: str,
    ) -> None:
        """_summary_

        Args:
            file_name_curr (str):
                    File name of the file to be processed.
        """
        dcr_core.core_utils.check_exists_object(
            is_line_type_headers_footers=True,
            is_setup=True,
            is_text_parser=True,
        )

        self._file_name_curr = file_name_curr

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_toc, "LineTypeToc")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start create instance                ={self._file_name_curr}",
        )

        self._is_toc_existing = False

        self._page_no = 0

        self._parser_line_lines_json: dcr_core.cls_nlp_core.NLPCore.ParserLineLines = []
        self._parser_no_pages_in_doc = 0

        self._strategy = ""

        # page_no_toc, page_no, paragraph_no, row_no
        self._toc_candidates: list[list[int]] = []

        self.no_lines_toc = 0

        self.parser_line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages = []

        self._exist = True

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: End   create instance                ={self._file_name_curr}",
        )

    # -----------------------------------------------------------------------------
    # Check a TOC candidate.
    # -----------------------------------------------------------------------------
    def _check_toc_candidate(self) -> None:
        if not self._toc_candidates:
            return

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start check TOC candidate            ={len(self._toc_candidates)}",
        )

        row_no = 0
        page_no_max = self._parser_no_pages_in_doc
        page_no_toc_last = -1

        for [page_no_toc, _, _, _] in self._toc_candidates:
            row_no += 1

            if page_no_toc == -1:
                if row_no != 1:
                    self._init_toc_candidate()
                    dcr_core.core_utils.progress_msg(
                        dcr_core.core_glob.setup.is_verbose_lt_toc,
                        "LineTypeToc: End   check TOC candidate (!=)       " + f"={self._is_toc_existing}: {page_no_toc}",
                    )
                    return

                continue

            if page_no_toc < page_no_toc_last or page_no_toc > page_no_max:
                self._init_toc_candidate()
                dcr_core.core_utils.progress_msg(
                    dcr_core.core_glob.setup.is_verbose_lt_toc,
                    "LineTypeToc: End   check TOC candidate (<>)       " + f"={self._is_toc_existing}: {page_no_toc}",
                )
                return

            page_no_toc_last = page_no_toc

        self._is_toc_existing = True

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            "LineTypeToc: End   check TOC candidate            " + f"={self._is_toc_existing}",
        )

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
        if self._is_toc_existing or self._page_no >= dcr_core.core_glob.setup.lt_toc_last_page:
            return

        self._page_no += 1

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_toc, "LineTypeToc")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start page (lines)                   ={self._page_no}",
        )

        for line_line in self._parser_line_lines_json:
            if line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                if (text := line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT]) != "":
                    line_tokens = text.split()
                    try:
                        self._process_toc_candidate_line_line(line_line, int(line_tokens[-1]))
                    except ValueError:
                        self._check_toc_candidate()
                        if self._is_toc_existing:
                            break

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: End   page (lines)                   ={self._page_no}",
        )

    # -----------------------------------------------------------------------------
    # Process the page-related data - table version.
    # -----------------------------------------------------------------------------
    def _process_page_table(self) -> None:
        """Process the page-related data - table version."""
        if self._is_toc_existing or self._page_no >= dcr_core.core_glob.setup.lt_toc_last_page:
            return

        self._page_no += 1

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_toc, "LineTypeToc")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start page (table)                   ={self._page_no}",
        )

        for line_line in self._parser_line_lines_json:
            if line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                if dcr_core.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO in line_line:
                    self._process_toc_candidate_table_line(line_line)
                else:
                    self._check_toc_candidate()
                    if self._is_toc_existing:
                        break

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: End   page (table)                   ={self._page_no}",
        )

    # -----------------------------------------------------------------------------
    # Add a TOC line candidate element.
    # -----------------------------------------------------------------------------
    def _process_toc_candidate_line_line(self, line_line: dcr_core.cls_nlp_core.NLPCore.ParserLineLine, page_no_toc: int) -> None:
        """Add a TOC line candidate element.

        Args:
            line_line (dcr_core.cls_nlp_core.NLPCore.LineLine):
                    Document line.
            page_no_toc (int):
                    Page number in the table of contents.
        """
        line_no = line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO]

        para_no = line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]

        self._toc_candidates.append([page_no_toc, self._page_no, para_no, line_no])

    # -----------------------------------------------------------------------------
    # Add a TOC table candidate element.
    # -----------------------------------------------------------------------------
    def _process_toc_candidate_table_line(self, line_line: dcr_core.cls_nlp_core.NLPCore.ParserLineLine) -> None:
        """Add a TOC table candidate element.

        Args:
            line_line (dcr_core.cls_nlp_core.NLPCore.LineLine):
                    Document line.
        """
        row_no = line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO]

        para_no = line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]

        if not self._toc_candidates or self._page_no != self._toc_candidates[-1][1] or row_no != self._toc_candidates[-1][3]:
            self._toc_candidates.append([-1, self._page_no, para_no, row_no])

        try:
            self._toc_candidates[-1][0] = int(line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_TEXT])
            self._toc_candidates[-1][2] = para_no
        except ValueError:
            self._toc_candidates[-1][0] = -1

    # -----------------------------------------------------------------------------
    # Store the found TOC entries in parser result.
    # -----------------------------------------------------------------------------
    def _store_results(self) -> None:  # noqa: C901
        """Store the found TOC entries in parser result."""
        self.no_lines_toc = len(self._toc_candidates)

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start store result                   ={self.no_lines_toc}",
        )

        if len(self._toc_candidates) < dcr_core.core_glob.setup.lt_toc_min_entries:
            dcr_core.core_utils.progress_msg(
                dcr_core.core_glob.setup.is_verbose_lt_toc,
                f"LineTypeToc: End   store result (min. entries)    ={self.no_lines_toc}",
            )
            self.no_lines_toc = 0
            return

        page_no_from = self._toc_candidates[0][1]
        page_no_till = self._toc_candidates[-1][1]
        para_no_from = self._toc_candidates[0][2]
        para_no_till = self._toc_candidates[-1][2]

        for page in self.parser_line_pages_json:
            page_no = page[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PAGE_NO]

            if page_no < page_no_from:
                continue
            if page_no > page_no_till:
                break

            for line_line in page[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES]:
                para_no = line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_PARA_NO]

                if page_no == page_no_from and para_no < para_no_from:
                    continue
                if page_no == page_no_till and para_no > para_no_till:
                    break

                if self._strategy == dcr_core.cls_nlp_core.NLPCore.SEARCH_STRATEGY_LINES:
                    for [_, cand_page_no, cand_para_no, cand_line_no] in self._toc_candidates:
                        if (
                            page_no == cand_page_no
                            and para_no == cand_para_no
                            and line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_NO] == cand_line_no
                        ):
                            line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_TOC
                elif self._strategy == dcr_core.cls_nlp_core.NLPCore.SEARCH_STRATEGY_TABLE:
                    if dcr_core.cls_nlp_core.NLPCore.JSON_NAME_ROW_NO in line_line:
                        if line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] == dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_BODY:
                            line_line[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINE_TYPE] = dcr_core.cls_nlp_core.NLPCore.LINE_TYPE_TOC

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: End   store result                   ={self.no_lines_toc}",
        )

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
        file_name_curr: str,
        parser_line_pages_json: dcr_core.cls_nlp_core.NLPCore.ParserLinePages,
    ) -> None:
        """_summary_

        Args:
            file_name_curr (str, optional):
                    File name of the file to be processed.
            parser_line_pages_json (dcr_core.cls_nlp_core.NLPCore.LinePages):
                    The document pages formatted in the parser.
        """
        dcr_core.core_utils.check_exists_object(
            is_line_type_headers_footers=True,
            is_setup=True,
            is_text_parser=True,
        )

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: lt_toc_last_page={dcr_core.core_glob.setup.lt_toc_last_page}",
        )

        if dcr_core.core_glob.setup.lt_toc_last_page == 0:
            return

        self._file_name_curr = file_name_curr
        self.parser_line_pages_json = parser_line_pages_json

        self._parser_no_pages_in_doc = len(self.parser_line_pages_json)

        dcr_core.core_utils.progress_msg(dcr_core.core_glob.setup.is_verbose_lt_toc, "LineTypeToc")
        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: Start document                       ={self._file_name_curr}",
        )

        # -------------------------------------------------------------------------
        # Examine the table version.
        # -------------------------------------------------------------------------
        self._strategy = dcr_core.cls_nlp_core.NLPCore.SEARCH_STRATEGY_TABLE

        for page_json in self.parser_line_pages_json:
            self._parser_line_lines_json = page_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES]
            self._process_page_table()

        if not self._is_toc_existing:
            self._check_toc_candidate()

        # -------------------------------------------------------------------------
        # Examine the lines version.
        # -------------------------------------------------------------------------
        if not self._is_toc_existing:
            self._strategy = dcr_core.cls_nlp_core.NLPCore.SEARCH_STRATEGY_LINES
            self._page_no = 0
            self._init_toc_candidate()
            for page_json in self.parser_line_pages_json:
                self._parser_line_lines_json = page_json[dcr_core.cls_nlp_core.NLPCore.JSON_NAME_LINES]
                self._process_page_lines()

            if not self._is_toc_existing:
                self._check_toc_candidate()

        # -------------------------------------------------------------------------
        # Store the results.
        # -------------------------------------------------------------------------
        if self._is_toc_existing:
            self._store_results()

        dcr_core.core_utils.progress_msg(
            dcr_core.core_glob.setup.is_verbose_lt_toc,
            f"LineTypeToc: End   document                       ={self._file_name_curr}",
        )
