"""Library Stub."""

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
LINE_TET_DOCUMENT_OPT_LIST: str
LINE_TET_PAGE_OPT_LIST: str

PAGE_TET_DOCUMENT_OPT_LIST: str
PAGE_TET_PAGE_OPT_LIST: str

WORD_TET_DOCUMENT_OPT_LIST: str
WORD_TET_PAGE_OPT_LIST: str

# -----------------------------------------------------------------------------
# Functions.
# -----------------------------------------------------------------------------
def create_child_document() -> None: ...
def extract_text_from_pdf() -> None: ...
def extract_text_from_pdf_file_line() -> None: ...
def extract_text_from_pdf_file_page() -> None: ...
def extract_text_from_pdf_file_word() -> None: ...
