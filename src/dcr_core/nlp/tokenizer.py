import dcr_core.cfg.glob
import dcr_core.nlp.cls_nlp_core
import dcr_core.nlp.cls_text_parser
import dcr_core.PDFlib.TET

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_71_901 = "71.901 Issue (tkn): Tokenizing the file '{full_name}' failed - " + "error type: '{error_type}' - error: '{error}'."


# -----------------------------------------------------------------------------
# Tokenizing the text from the PDF document.
# -----------------------------------------------------------------------------
def process(
    full_name_in: str,
    full_name_out: str,
    pipeline_name: str,
    document_id: int = -1,
    file_name_orig: str = dcr_core.cfg.glob.INFORMATION_NOT_YET_AVAILABLE,
    no_lines_footer: int = -1,
    no_lines_header: int = -1,
    no_lines_toc: int = -1,
) -> tuple[str, str]:
    """Tokenizing the text from the PDF document.

    The line-oriented text is broken down into qualified
    tokens with the means of SpaCy.

    Args:
        full_name_in (str):
                The directory name and file name of the input file.
        full_name_out (str):
                The directory name and file name of the output file.
        pipeline_name (str):
                The loaded SpaCy pipeline.
        document_id (int, optional):
                The identification number of the document.
                Defaults to -1.
        file_name_orig (str, optional):
                The file name of the originating document.
                Defaults to dcr_core.cfg.glob.INFORMATION_NOT_YET_AVAILABLE.
        no_lines_footer (int, optional):
                Total number of footer lines.
                Defaults to -1.
        no_lines_header (int, optional):
                Total number of header lines.
                Defaults to -1.
        no_lines_toc (int, optional):
                Total number of TOC lines.
                Defaults to -1.

    Returns:
        tuple[str, str]:
                ("ok", "") if the processing has been completed successfully,
                           otherwise a corresponding error code and error message.
    """
    try:
        dcr_core.cfg.glob.text_parser = dcr_core.nlp.cls_text_parser.TextParser.from_files(
            file_encoding=dcr_core.cfg.glob.FILE_ENCODING_DEFAULT, full_name_line=full_name_in
        )

        dcr_core.cfg.glob.tokenizer_spacy.process_document(
            document_id=document_id,
            file_name_next=full_name_out,
            file_name_orig=file_name_orig,
            no_lines_footer=no_lines_footer,
            no_lines_header=no_lines_header,
            no_lines_toc=no_lines_toc,
            pipeline_name=pipeline_name,
        )

    except FileNotFoundError as err:
        error_msg = ERROR_71_901.replace("{full_name}", full_name_in).replace("{error_type}", str(type(err))).replace("{error}", str(err))
        return error_msg[:6], error_msg

    return dcr_core.cfg.glob.RETURN_OK
