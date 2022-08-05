"""Library Stub."""
import dcr_core.core_glob

ERROR_21_901: str
ERROR_31_902: str
ERROR_41_901: str
ERROR_51_901: str
ERROR_61_901: str
ERROR_71_901: str

PANDOC_PDF_ENGINE_LULATEX: str
PANDOC_PDF_ENGINE_XELATEX: str

def pandoc_process(
    full_name_in: str,
    full_name_out: str,
    language_pandoc: str,
) -> tuple[str, str]: ...
def parser_process(
    full_name_in: str,
    full_name_out: str,
    no_pdf_pages: int,
    document_id: int = -1,
    file_name_orig: str = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE,
) -> tuple[str, str]: ...
def pdf2image_process(
    full_name_in: str,
) -> tuple[str, str, list[tuple[str, str]]]: ...
def pdflib_process(
    full_name_in: str,
    full_name_out: str,
    document_opt_list: str,
    page_opt_list: str,
) -> tuple[str, str]: ...
def tesseract_process(
    full_name_in: str,
    full_name_out: str,
    language_tesseract: str,
) -> tuple[str, str, list[str]]: ...
def tokenizer_process(
    full_name_in: str,
    full_name_out: str,
    pipeline_name: str,
    document_id: int = -1,
    file_name_orig: str = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE,
    no_lines_footer: int = -1,
    no_lines_header: int = -1,
    no_lines_toc: int = -1,
) -> tuple[str, str]: ...
