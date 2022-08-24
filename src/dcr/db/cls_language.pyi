# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
from typing import ClassVar

import sqlalchemy.orm

class Language:
    LANGUAGES_PANDOC: ClassVar[dict[int, str]]
    LANGUAGES_SPACY: ClassVar[dict[int, str]]
    LANGUAGES_TESSERACT: ClassVar[dict[int, str]]

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
    ) -> None:
        self._exist = None
        self.language_active = None
        self.language_code_iso_639_3 = None
        self.language_code_pandoc = None
        self.language_code_spacy = None
        self.language_code_tesseract = None
        self.language_directory_name_inbox = None
        self.language_id = None
        self.language_iso_language_name = None
        self.total_erroneous = None
        self.total_processed = None
        self.total_processed_pandoc = None
        self.total_processed_pdf2image = None
        self.total_processed_pdflib = None
        self.total_processed_tesseract = None
        self.total_processed_to_be = None
    def _get_columns(self) -> None: ...
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
