from typing import ClassVar

import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm
from sqlalchemy.engine import Connection

class Action:
    PDF2IMAGE_FILE_TYPE: ClassVar[str]
    action_id: int
    action_action_code: str
    action_action_text: str
    action_directory_name: str
    action_directory_type: str
    action_duration_ns: int
    action_error_code_last: str
    action_error_msg_last: str
    action_error_no: int
    action_file_name: str
    action_file_size_bytes: int
    action_id_document: int
    action_id_parent: int
    action_id_run_last: int
    action_no_children: int
    action_no_pdf_pages: int
    action_status: str
    def __init__(
        self,
        action_code: str,
        id_run_last: int,
        _row_id: int = ...,
        action_text: str = ...,
        directory_name: str = ...,
        directory_type: str = ...,
        duration_ns: int = ...,
        error_code_last: str = ...,
        error_msg_last: str = ...,
        error_no: int = ...,
        file_name: str = ...,
        file_size_bytes: int = ...,
        id_document: int = ...,
        id_parent: int = ...,
        no_children: int = ...,
        no_pdf_pages: int = ...,
        status: str = ...,
    ) -> None:
        self._exist = None
        ...
    def _get_columns(self) -> None: ...
    @classmethod
    def create_dbt(cls) -> None: ...
    def exists(self) -> bool: ...
    def finalise(self) -> None: ...
    def finalise_error(self, error_code: str, error_msg: str) -> None: ...
    @classmethod
    def from_id(cls, id_action: int) -> Action: ...
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Action: ...
    def get_columns_in_tuple(self, is_duration_ns: bool = ..., is_file_size_bytes: bool = ...) -> tuple[int | str, ...]: ...
    def get_file_type(self) -> str: ...
    def get_full_name(self) -> str: ...
    def get_stem_name(self) -> str: ...
    def persist_2_db(self) -> None: ...
    @classmethod
    def select_action_by_action_code(cls, conn: Connection, action_code: str) -> sqlalchemy.engine.CursorResult: ...
    @classmethod
    def select_action_by_action_code_id_document(
        cls, conn: Connection, action_code: str, id_document: int
    ) -> sqlalchemy.engine.CursorResult: ...
