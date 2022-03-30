"""Library Stub."""
from typing import Iterable

def init_parse_result() -> None: ...
def parse_tag_doc_info(parent_tag: str, parent: Iterable[str]) -> None: ...
def parse_tag_document(parent_tag: str, parent: Iterable[str]) -> None: ...
def parse_tag_pages(parent_tag: str, parent: Iterable[str]) -> None: ...
def parse_tetml() -> None: ...
def parse_tetml_file() -> None: ...