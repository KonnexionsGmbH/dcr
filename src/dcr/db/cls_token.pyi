# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
import sqlalchemy.orm

class Token:
    def __init__(
        self,
        id_document: int,
        column_no: int,
        column_span: int,
        coord_llx: float,
        coord_urx: float,
        line_type: str,
        no_tokens_in_sent: int,
        page_no: int,
        para_no: int,
        row_no: int,
        sent_no: int,
        text: str,
        tokens: str,
        _row_id: int = ...,
    ) -> None:
        self._exist = None
        self.token_column_no = None
        self.token_column_span = None
        self.token_coord_llx = None
        self.token_coord_urx = None
        self.token_id = None
        self.token_id_document = None
        self.token_line_type = None
        self.token_no_tokens_in_sent = None
        self.token_page_no = None
        self.token_para_no = None
        self.token_row_no = None
        self.token_sent_no = None
        self.token_text = None
        self.token_tokens = None
    def _get_columns(self) -> None: ...
    @classmethod
    def create_dbt(cls) -> None: ...
    def exists(self) -> bool: ...
    def finalise(self) -> None: ...
    @classmethod
    def from_id(cls, id_token: int) -> Token: ...
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Token: ...
    def get_columns_in_tuple(self) -> tuple[int, int, int, int, float, float, str, int, int, int, int, int, str, str]: ...
    def persist_2_db(self) -> None: ...
