from typing import ClassVar

import sqlalchemy.orm

class Language:
    LANGUAGES_PANDOC: ClassVar[dict[int, str]]
    LANGUAGES_SPACY: ClassVar[dict[int, str]]
    LANGUAGES_TESSERACT: ClassVar[dict[int, str]]
    language_active: str
    language_code_iso_639_3: str
    language_code_pandoc: str
    language_code_spacy: str
    language_code_tesseract: str
    language_directory_name_inbox: str
    language_id: str
    language_iso_language_name: str
    total_erroneous: int
    total_processed: int
    total_processed_to_be: int
    total_processed_pandoc: int
    total_processed_pdf2image: int
    total_processed_pdflib: int
    total_processed_tesseract: int
    def __init__(
        self,
        code_iso_639_3: str,
        code_pandoc: str,
        code_spacy: str,
        code_tesseract: str,
        iso_language_name: str,
        _row_id: int = ...,
        active: bool = ...,
        directory_name_inbox: str = ...,
    ) -> None: ...
    @classmethod
    def create_dbt(cls) -> None: ...
    def exists(self) -> bool: ...
    @classmethod
    def from_id(cls, id_language: int) -> Language: ...
    @classmethod
    def from_row(cls, row: sqlalchemy.engine.Row) -> Language: ...
    def get_columns_in_tuple(self) -> tuple[int, bool, str, str, str, str, str, str]: ...
    @classmethod
    def load_data_from_dbt_language(cls) -> None: ...
    def persist_2_db(self) -> None: ...
    @classmethod
    def select_active_languages(cls, conn: sqlalchemy.engine.Connection) -> sqlalchemy.engine.CursorResult: ...
