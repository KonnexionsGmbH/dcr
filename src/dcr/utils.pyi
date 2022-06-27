"""Library Stub."""
import pathlib

def check_exists_object(
    is_action_curr: bool = False,
    is_action_next: bool = False,
    is_db_core: bool = False,
    is_document: bool = False,
    is_run: bool = False,
    is_setup: bool = False,
    is_text_parser: bool = False,
) -> None: ...
def compute_sha256(file: pathlib.Path) -> str: ...
def delete_auxiliary_file(full_name: pathlib.Path | str) -> None: ...
def get_file_type(file_name: pathlib.Path | str | None) -> str: ...
def get_full_name(directory_name: pathlib.Path | str | None, file_name: pathlib.Path | str | None) -> str: ...
def get_os_independent_name(name: pathlib.Path | str | None) -> str: ...
def get_path_name(name: pathlib.Path | str | None) -> pathlib.Path | str: ...
def get_pdf_pages_no(
    file_name: pathlib.Path | str,
) -> int: ...
def get_stem_name(file_name: pathlib.Path | str | None) -> str: ...
def progress_msg(msg: str) -> None: ...
def progress_msg_connected(database: str | None, user: str | None) -> None: ...
def progress_msg_core(msg: str) -> None: ...
def progress_msg_disconnected() -> None: ...
def progress_msg_empty_before(msg: str) -> None: ...
def progress_msg_line_type_headers_footers(msg: str) -> None: ...
def progress_msg_line_type_heading(msg: str) -> None: ...
def progress_msg_line_type_list(msg: str) -> None: ...
def progress_msg_line_type_table(msg: str) -> None: ...
def progress_msg_line_type_toc(msg: str) -> None: ...
def reset_statistics_total() -> None: ...
def show_statistics_language() -> None: ...
def show_statistics_total() -> None: ...
def terminate_fatal(error_msg: str) -> None: ...
def terminate_fatal_setup(error_msg: str) -> None: ...
