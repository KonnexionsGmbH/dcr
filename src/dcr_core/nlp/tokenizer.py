import dcr_core.cfg.glob
import dcr_core.nlp.cls_nlp_core
import dcr_core.nlp.cls_text_parser
import dcr_core.PDFlib.TET

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_71_901 = "71.901 Issue (tkn): Tokenizing the file '{full_name}' failed - " + "error type: '{error_type}' - error: '{error}'."


# -----------------------------------------------------------------------------
# Extracting the text from the PDF document.
# -----------------------------------------------------------------------------
def process(
    full_name_in: str,
    full_name_out: str,
    document_id: int,
    file_name_orig: str,
    no_lines_footer: int,
    no_lines_header: int,
    no_lines_toc: int,
    pipeline_name: str,
) -> tuple[str, str]:
    """Processing a PDF file with PDFlib TET.

    From the line-oriented XML output file of PDFlib TET,
    the text and relevant metadata are extracted with the
    help of an XML parser and stored in a JSON file.

    Args:
        full_name_in (str):
                The directory name and file name of the input file.
        full_name_out (str):
                The directory name and file name of the output file.
        document_id (int):
                The identification number of the document.
        file_name_orig (str):
                The file name of the originating document.
        no_lines_footer (int):
                Total number of PDF pages.
        no_lines_header (int):
                Total number of PDF pages.
        no_lines_toc (int):
                Total number of PDF pages.
        pipeline_name (str):
                The SpaCy pipeline to load.

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
