import dcr_core.PDFlib.TET

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_51_901 = (
    "51.901 Issue (tet): Opening document '{full_name}' - "
    + "error no: '{error_no}' - api: '{api_name}' - error: '{error}'."
)

RETURN_OK = ("ok", "")


# -----------------------------------------------------------------------------
# Processing a file with PDFlib TET.
# -----------------------------------------------------------------------------
def process_pdflib(file_name_in: str, file_name_out: str, document_opt_list: str, page_opt_list: str) -> tuple[str, str]:
    """Processing a PDF file with PDFlib TET.

    The data from a PDF file is made available in XML files
    with the help of PDFlib TET. The granularity of the XML
    files can be word, line or paragraph depending on the
    document and page options selected.

    Args:
        file_name_in (str):
                Directory name and file name of the input file.
        file_name_out (str):
                Directory name and file name of the output file.
        document_opt_list (str):
                Document level options:
                    word: engines={noannotation noimage text notextcolor novector}
                    line: engines={noannotation noimage text notextcolor novector}
                    page: engines={noannotation noimage text notextcolor novector} lineseparator=U+0020
        page_opt_list (str):
                Page level options:
                    word: granularity=word tetml={elements={line}}
                    line: granularity=line
                    page: granularity=page

    Returns:
        tuple[str, str]:
                ("ok", "") if the processing has been completed successfully,
                           otherwise a corresponding error code and error message.
    """
    tet = dcr_core.PDFlib.TET.TET()

    doc_opt_list = f"tetml={{filename={{{file_name_out}}}}} {document_opt_list}"

    if (file_curr := tet.open_document(file_name_in, doc_opt_list)) == -1:
        error_msg = (
            ERROR_51_901.replace("{full_name}", file_name_in)
            .replace("{error_no}", str(tet.get_errnum()))
            .replace("{api_name}", tet.get_apiname() + "()")
            .replace("{error}", tet.get_errmsg())
        )
        return error_msg[:6], error_msg

    # get number of pages in the document */
    no_pages = tet.pcos_get_number(file_curr, "length:pages")

    # loop over pages in the document */
    for page_no in range(1, int(no_pages) + 1):
        tet.process_page(file_curr, page_no, page_opt_list)

    # This could be combined with the last page-related call
    tet.process_page(file_curr, 0, "tetml={trailer}")

    tet.close_document(file_curr)

    tet.delete()

    return RETURN_OK
