"""Library Stub."""
import dcr_core.cfg.glob

ERROR_71_901: str

def process(
    full_name_in: str,
    full_name_out: str,
    pipeline_name: str,
    document_id: int = -1,
    file_name_orig: str = dcr_core.cfg.glob.INFORMATION_NOT_YET_AVAILABLE,
    no_lines_footer: int = -1,
    no_lines_header: int = -1,
    no_lines_toc: int = -1,
) -> tuple[str, str]: ...
