"""Library stub."""

import pathlib
from typing import Callable

from libs import db

def check_and_create_directories() -> None: ...
def create_directory(directory_type: str, directory_name: str) -> None: ...
def prepare_pdf() -> None: ...
def prepare_pdf_for_teseract() -> None: ...
def process_inbox_accepted(
    action: str,
    function_name: str,
    module_name: str,
    status: str,
    target_file_name: str,
) -> None: ...
def process_inbox_rejected(
    update_document_status: Callable[[str, str, str, str], None],
) -> None: ...
def process_inbox_document_initial(file: pathlib.Path) -> None: ...
def process_inbox_files() -> None: ...
def process_inbox_pandoc() -> None: ...
