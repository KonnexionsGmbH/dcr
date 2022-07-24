"""Library Stub."""
import dcr_core.cfg.glob

def process(
    full_name_in: str,
    full_name_out: str,
    no_pdf_pages: int,
    document_id: int = -1,
    file_name_orig: str = dcr_core.cfg.glob.INFORMATION_NOT_YET_AVAILABLE,
) -> tuple[str, str]: ...
