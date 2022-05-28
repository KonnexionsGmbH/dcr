"""Module db.cls_vdb_core: Managing the database."""
from __future__ import annotations

from typing import ClassVar

import cfg.glob


# pylint: disable=R0903
class DBCore:
    """Managing the database.

    Returns:
        _type_: Version instance.
    """

    # -----------------------------------------------------------------------------
    # Class variables.
    # -----------------------------------------------------------------------------
    DB_DIALECT_POSTGRESQL: ClassVar[str] = "postgresql"

    DBC_ACTION_CODE: ClassVar[str] = "action_code"
    DBC_ACTION_CODE_LAST: ClassVar[str] = "action_code_last"
    DBC_ACTION_TEXT: ClassVar[str] = "action_text"
    DBC_ACTION_TEXT_LAST: ClassVar[str] = "action_text_last"
    DBC_ACTIVE: ClassVar[str] = "active"
    DBC_CODE_ISO_639_3: ClassVar[str] = "code_iso_639_3"
    DBC_CODE_ISO_639_3_DEFAULT: ClassVar[str] = "eng"
    DBC_CODE_PANDOC: ClassVar[str] = "code_pandoc"
    DBC_CODE_PANDOC_DEFAULT: ClassVar[str] = "en"
    DBC_CODE_SPACY: ClassVar[str] = "code_spacy"
    DBC_CODE_SPACY_DEFAULT: ClassVar[str] = "en_core_web_trf"
    DBC_CODE_TESSERACT: ClassVar[str] = "code_tesseract"
    DBC_CODE_TESSERACT_DEFAULT: ClassVar[str] = "eng"
    DBC_CREATED_AT: ClassVar[str] = "created_at"
    DBC_DIRECTORY_NAME: ClassVar[str] = "directory_name"
    DBC_DIRECTORY_NAME_INBOX: ClassVar[str] = "directory_name_inbox"
    DBC_DIRECTORY_TYPE: ClassVar[str] = "directory_type"
    DBC_DURATION_NS: ClassVar[str] = "duration_ns"
    DBC_ERROR_CODE: ClassVar[str] = "error_code"
    DBC_ERROR_CODE_LAST: ClassVar[str] = "error_code_last"
    DBC_ERROR_MSG: ClassVar[str] = "error_msg"
    DBC_ERROR_MSG_LAST: ClassVar[str] = "error_msg_last"
    DBC_ERROR_NO: ClassVar[str] = "error_no"
    DBC_FILE_NAME: ClassVar[str] = "file_name"
    DBC_FILE_SIZE_BYTES: ClassVar[str] = "file_size_bytes"
    DBC_ID: ClassVar[str] = "id"
    DBC_ID_DOCUMENT: ClassVar[str] = "id_document"
    DBC_ID_LANGUAGE: ClassVar[str] = "id_language"
    DBC_ID_PARENT: ClassVar[str] = "id_parent"
    DBC_ID_RUN: ClassVar[str] = "id_run"
    DBC_ID_RUN_LAST: ClassVar[str] = "id_run_last"
    DBC_ISO_LANGUAGE_NAME: ClassVar[str] = "iso_language_name"
    DBC_ISO_LANGUAGE_NAME_DEFAULT: ClassVar[str] = "English"
    DBC_MODIFIED_AT: ClassVar[str] = "modified_at"
    DBC_NO_CHILDREN: ClassVar[str] = "no_children"
    DBC_NO_PDF_PAGES: ClassVar[str] = "no_pdf_pages"
    DBC_PAGE_DATA: ClassVar[str] = "page_data"
    DBC_PAGE_NO: ClassVar[str] = "page_no"
    DBC_SHA256: ClassVar[str] = "sha256"
    DBC_STATUS: ClassVar[str] = "status"
    DBC_TOTAL_ERRONEOUS: ClassVar[str] = "total_erroneous"
    DBC_TOTAL_PROCESSED_OK: ClassVar[str] = "total_processed_ok"
    DBC_TOTAL_PROCESSED_TO_BE: ClassVar[str] = "total_processed_to_be"
    DBC_VERSION: ClassVar[str] = "version"

    DBT_ACTION: ClassVar[str] = "action"
    DBT_DOCUMENT: ClassVar[str] = "document"
    DBT_LANGUAGE: ClassVar[str] = "language"
    DBT_RUN: ClassVar[str] = "run"
    DBT_TOKEN: ClassVar[str] = "token"
    DBT_VERSION: ClassVar[str] = "version"

    # -----------------------------------------------------------------------------
    # Initialise the instance.
    # -----------------------------------------------------------------------------
    def __init__(
        self,
        is_admin: bool = False,
    ) -> None:
        """Initialise the instance.

        Args:
            is_admin (bool, optional):
                    Administrator access. Defaults to False.
        """
        cfg.glob.logger.debug(cfg.glob.LOGGER_START)

        self.is_admin = is_admin

        self._exist = True

        cfg.glob.logger.debug(cfg.glob.LOGGER_END)

    # -----------------------------------------------------------------------------
    # Check the object existence.
    # -----------------------------------------------------------------------------
    def exists(self) -> bool:
        """Check the object existence.

        Returns:
            bool:   Always true
        """
        return self._exist
