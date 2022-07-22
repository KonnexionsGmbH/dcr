import pypandoc

import dcr_core.cfg.glob

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_31_902 = (
    "31.902 Issue (n_2_p): The file '{full_name}' cannot be converted to an "
    + "'pdf' document - "
    + "error type: '{error_type}' - error: '{error_msg}'."
)

PANDOC_PDF_ENGINE_LULATEX = "lulatex"
PANDOC_PDF_ENGINE_XELATEX = "xelatex"


# -----------------------------------------------------------------------------
# Converting a Non-PDF file to a PDF file.
# -----------------------------------------------------------------------------
def process(
    full_name_in: str,
    full_name_out: str,
    language_pandoc: str,
) -> tuple[str, str]:
    """Converting a Non-PDF file to a PDF file.

    The following file formats are converted into
    PDF format here with the help of Pandoc:

    - csv  comma-separated values
    - docx Office Open XML
    - epub e-book file format
    - html HyperText Markup Language
    - odt  Open Document Format for Office Applications
    - rst  reStructuredText (RST
    - rtf  Rich Text Format

    Args:
        full_name_in (str):
                The directory name and file name of the input file.
        full_name_out (str):
                The directory name and file name of the output file.
        language_pandoc (str):
                The Pandoc name of the document language.

    Returns:
        tuple[str, str]:
                ("ok", "") if the processing has been completed successfully,
                           otherwise a corresponding error code and error message.
    """
    # Convert the document
    extra_args = [
        f"--pdf-engine={PANDOC_PDF_ENGINE_XELATEX}",
        "-V",
        f"lang:{language_pandoc}",
    ]

    try:
        pypandoc.convert_file(
            full_name_in,
            dcr_core.cfg.glob.FILE_TYPE_PDF,
            extra_args=extra_args,
            outputfile=full_name_out,
        )

    except (FileNotFoundError, RuntimeError) as err:
        error_msg = ERROR_31_902.replace("{full_name}", full_name_in).replace("{error_type}", str(type(err))).replace("{error}", str(err))
        return error_msg[:6], error_msg

    return dcr_core.cfg.glob.RETURN_OK
