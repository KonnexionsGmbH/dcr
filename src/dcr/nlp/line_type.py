"""Module setup.config: Managing the application configuration parameters."""
# import collections
from typing import Dict
from typing import List
from typing import Tuple

import db.cfg
import db.driver
import db.orm.dml
import jellyfish
import libs.cfg
import libs.utils
import sqlalchemy


# pylint: disable=R0903
class LineType:
    """Managing the application configuration parameters.

    Returns:
        _type_: Application configuration parameters.
    """

    # -----------------------------------------------------------------------------
    # Initialise and load the application configuration parameters.
    # -----------------------------------------------------------------------------
    def __init__(self) -> None:
        """Initialise and load the application configuration parameters."""
        libs.cfg.logger.debug(libs.cfg.LOGGER_START)

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

        libs.cfg.logger.debug(libs.cfg.LOGGER_END)

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
            List[Tuple[int, int, int]]: _description_
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

        libs.utils.progress_msg_line_type(f"LineType: Value of page_lines_distance       ={page_lines_distance}")
        return page_lines_distance

    # -----------------------------------------------------------------------------
    # Determine the footer lines.
    # -----------------------------------------------------------------------------
    def determine_footer_lines(self, page_ind_max: int) -> None:
        """Determine the footer lines.

        Args:
            page_ind_max (_type_): Highest page index.
        """
        for line in range(libs.cfg.config.line_footer_max_lines):
            distance_rest = 0
            for page in range(1, page_ind_max):
                (_, _, distance) = self._page_lines_distance_footer[page][line]
                if distance > libs.cfg.config.line_footer_max_distance:
                    distance_rest = distance
                    break

            if distance_rest > libs.cfg.config.line_footer_max_distance:
                continue

            (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_footer[0][line]
            if distance <= libs.cfg.config.line_footer_max_distance:
                self._page_line_type.append((1, line_ind_prev, db.cfg.DOCUMENT_LINE_TYPE_FOOTER))

            for page in range(1, page_ind_max):
                (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_footer[page][line]
                self._page_line_type.append((page + 1, line_ind_prev, db.cfg.DOCUMENT_LINE_TYPE_FOOTER))

            (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_footer[page_ind_max][line]
            if distance <= libs.cfg.config.line_footer_max_distance:
                self._page_line_type.append((page_ind_max + 1, line_ind_curr, db.cfg.DOCUMENT_LINE_TYPE_FOOTER))

    # -----------------------------------------------------------------------------
    # Determine the header lines.
    # -----------------------------------------------------------------------------
    def determine_header_lines(self, page_ind_max: int) -> None:
        """Determine the header lines.

        Args:
            page_ind_max (_type_): Highest page index.
        """
        for line in range(libs.cfg.config.line_header_max_lines):
            distance_rest = 0
            for page in range(1, page_ind_max):
                (_, _, distance) = self._page_lines_distance_header[page][line]
                if distance > libs.cfg.config.line_header_max_distance:
                    distance_rest = distance
                    break

            if distance_rest > libs.cfg.config.line_header_max_distance:
                continue

            (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_header[0][line]
            if distance <= libs.cfg.config.line_header_max_distance:
                self._page_line_type.append((1, line_ind_prev, db.cfg.DOCUMENT_LINE_TYPE_HEADER))

            for page in range(1, page_ind_max):
                (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_header[page][line]
                self._page_line_type.append((page + 1, line_ind_prev, db.cfg.DOCUMENT_LINE_TYPE_HEADER))

            (line_ind_prev, line_ind_curr, distance) = self._page_lines_distance_header[page_ind_max][line]
            if distance <= libs.cfg.config.line_header_max_distance:
                self._page_line_type.append((page_ind_max + 1, line_ind_curr, db.cfg.DOCUMENT_LINE_TYPE_HEADER))

    # -----------------------------------------------------------------------------
    # Process the document related data.
    # -----------------------------------------------------------------------------
    def process_document(self, document_id: sqlalchemy.Integer) -> None:
        """Process the document related data.

        Args:
            document_id (sqlalchemy.Integer): Document identification.
        """
        libs.cfg.logger.debug(libs.cfg.LOGGER_START)

        libs.utils.progress_msg_line_type(
            f"LineType: Value of page_lines_distance_header={self._page_lines_distance_header}"
        )
        libs.utils.progress_msg_line_type(
            f"LineType: Value of page_lines_distance_footer={self._page_lines_distance_footer}"
        )

        page_ind_max = len(self._page_lines_distance_header)

        if page_ind_max == 0:
            return

        page_ind_max -= 1

        if libs.cfg.config.line_header_max_lines > 0:
            self.determine_header_lines(page_ind_max)

        if libs.cfg.config.line_footer_max_lines > 0:
            self.determine_footer_lines(page_ind_max)

        if len(self._page_line_type) == 0:
            return

        self.update_content_tetml_line(document_id)

        libs.cfg.logger.debug(libs.cfg.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Process the page-related data.
    # -----------------------------------------------------------------------------
    def process_page(self, page_no: int, page_lines: List[Dict[str, int | str]]) -> None:
        """Process the page-related data.

        Args:
            page_no (int):
                    The number of the current page.
            page_lines (List[Dict[str, int  |  str]]):
                    The lines of the current page.
        """
        libs.cfg.logger.debug(libs.cfg.LOGGER_START)

        if libs.cfg.config.line_header_max_lines > 0:
            self._save_lines_header_curr(
                page_lines,
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

        if libs.cfg.config.line_footer_max_lines > 0:
            self._save_lines_footer_curr(
                page_lines,
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

        libs.cfg.logger.debug(libs.cfg.LOGGER_END)

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
        count = len(page_lines) - libs.cfg.config.line_footer_max_lines

        self._line_text_footer_curr = []

        for _ in range(libs.cfg.config.line_footer_max_lines):
            if count < 0:
                self._line_text_footer_curr.append((-1, libs.cfg.INFORMATION_NOT_YET_AVAILABLE))
            else:
                page_line: Dict[str, int | str] = page_lines[count]
                self._line_text_footer_curr.append(
                    (
                        page_line[db.cfg.JSON_NAME_LINE_INDEX_PAGE],
                        page_line[db.cfg.JSON_NAME_LINE_TEXT],
                    )  # type: ignore
                )
            count += 1

        libs.utils.progress_msg_line_type(
            f"LineType: Value of line_text_footer_prev     ={self._line_text_footer_prev}"
        )
        libs.utils.progress_msg_line_type(
            f"LineType: Value of line_text_footer_curr     ={self._line_text_footer_curr}"
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
    def _save_lines_header_curr(self, page_lines: List[Dict[str, int | str]]) -> None:
        """Save the headers of the current page.

        Args:
            page_lines (List[Dict[str, int | str]]):
                    All lines of the current page.
        """
        page_lines_max = len(page_lines)

        self._line_text_header_curr = []

        for ind in range(libs.cfg.config.line_header_max_lines):
            if ind < page_lines_max:
                page_line: Dict[str, int | str] = page_lines[ind]
                self._line_text_header_curr.append(
                    (
                        page_line[db.cfg.JSON_NAME_LINE_INDEX_PAGE],
                        page_line[db.cfg.JSON_NAME_LINE_TEXT],
                    )  # type: ignore
                )
            else:
                self._line_text_header_curr.append((-1, libs.cfg.INFORMATION_NOT_YET_AVAILABLE))

        libs.utils.progress_msg_line_type(
            f"LineType: Value of line_text_header_prev     ={self._line_text_header_prev}"
        )
        libs.utils.progress_msg_line_type(
            f"LineType: Value of line_text_header_curr     ={self._line_text_header_curr}"
        )

    # -----------------------------------------------------------------------------
    # Update the database table 'content_tetml_line'.
    # -----------------------------------------------------------------------------
    # Example : [ (page_no, line_ind, line_type) ]:
    #
    # page_line_type = [(1, 0, 'h'),
    #                  (1, 1, 'h'),
    #                  (1, 2, 'h'),
    #                  (1, 8, 'f'),
    #                  (1, 9, 'f'),
    #                  (1, 10, 'f'),
    #                  (2, 0, 'h'),
    #                  (2, 1, 'h'),
    #                  (2, 2, 'h'),
    #                  (2, 8, 'f'),
    #                  (2, 9, 'f'),
    #                  (2, 10, 'f')].
    # -----------------------------------------------------------------------------
    def update_content_tetml_line(self, document_id: sqlalchemy.Integer) -> None:
        """Update the database table 'content_tetml_line'.

        Args:
            document_id (sqlalchemy.Integer): Document identification.
        """
        libs.utils.progress_msg_line_type(f"LineType: Value of page_line_type raw        ={self._page_line_type}")

        self._page_line_type.sort()

        libs.utils.progress_msg_line_type(f"LineType: Value of page_line_type sorted     ={self._page_line_type}")

        dbt_content_tetml: sqlalchemy.Table = db.orm.dml.dml_prepare(db.cfg.DBT_CONTENT_TETML_LINE)

        with db.cfg.db_orm_engine.connect() as conn:
            rows = db.orm.dml.select_content_tetml(conn, dbt_content_tetml, document_id)
            for row in rows:
                content_page_no = row[0]

                libs.cfg.parse_result_page_lines = row[1]
                print(f"wwe parse_result_page_lines={libs.cfg.parse_result_page_lines}")
                content_page_lines = libs.cfg.parse_result_page_lines[db.cfg.JSON_NAME_PAGE_LINES]
                print(f"wwe content_page_lines     ={content_page_lines}")

                is_changed = False

                for (page_no, line_ind, line_type) in self._page_line_type:
                    if page_no < content_page_no:
                        continue
                    if page_no > content_page_no:
                        break

                    xxx = content_page_lines[line_ind]
                    line_type_curr = xxx[db.cfg.JSON_NAME_LINE_TYPE]

                    if (
                        line_type_curr == db.cfg.DOCUMENT_LINE_TYPE_FOOTER
                        and libs.cfg.config.is_line_footer_preferred
                        or line_type_curr == db.cfg.DOCUMENT_LINE_TYPE_HEADER
                        and not libs.cfg.config.is_line_footer_preferred
                    ):
                        continue

                    content_page_lines[line_ind][db.cfg.JSON_NAME_LINE_TYPE] = line_type

                    is_changed = True

                if is_changed:
                    libs.cfg.parse_result_page_lines[db.cfg.JSON_NAME_PAGE_LINES] = content_page_lines
                    db.orm.dml.update_dbt_id(
                        db.cfg.DBT_CONTENT_TETML_LINE,
                        document_id,
                        {
                            db.cfg.DBC_PAGE_DATA: libs.cfg.parse_result_page_lines,
                        },
                    )
                    libs.utils.progress_msg_line_type(
                        f"LineType: Successful update of page          ={libs.cfg.parse_result_no_pages_in_doc}"
                    )

                # wwe ? print(xxx)
