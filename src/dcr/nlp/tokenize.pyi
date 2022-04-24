"""Library Stub."""
from typing import Dict
from typing import List

from spacy import Language
from sqlalchemy import Table

def get_text_from_page_lines(page_data: Dict[str, str | List[Dict[str, int | str]]]) -> str: ...
def tokenize() -> None: ...
def tokenize_document(nlp: Language, dbt_content: Table) -> None: ...
