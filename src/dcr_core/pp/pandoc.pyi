"""Library Stub."""

ERROR_31_902: str

PANDOC_PDF_ENGINE_LULATEX: str
PANDOC_PDF_ENGINE_XELATEX: str

def process(
    full_name_in: str,
    full_name_out: str,
    language_pandoc: str,
) -> tuple[str, str]: ...
