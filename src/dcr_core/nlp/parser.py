import os.path

import defusedxml
import defusedxml.ElementTree

import dcr_core.cfg.glob
import dcr_core.nlp.cls_nlp_core
import dcr_core.nlp.cls_text_parser
import dcr_core.PDFlib.TET

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_61_901 = "61.901 Issue (s_p_j): Parsing the file '{full_name}' failed - " + "error type: '{error_type}' - error: '{error}'."


# -----------------------------------------------------------------------------
# Extracting the text from the PDF document.
# -----------------------------------------------------------------------------
def process(full_name_in: str, full_name_out: str, file_name_orig: str, document_id: int, no_pdf_pages: int) -> tuple[str, str]:
    """Processing a PDF file with PDFlib TET.

    From the line-oriented XML output file of PDFlib TET,
    the text and relevant metadata are extracted with the
    help of an XML parser and stored in a JSON file.

    Args:
        full_name_in (str):
                The directory name and file name of the input file.
        full_name_out (str):
                The directory name and file name of the output file.
        file_name_orig (str):
                The file name of the originating document.
        document_id (int):
                The identification number of the document.
        no_pdf_pages (int):
                Total number of PDF pages.

    Returns:
        tuple[str, str]:
                ("ok", "") if the processing has been completed successfully,
                           otherwise a corresponding error code and error message.
    """
    try:
        # Create the Element tree object
        tree = defusedxml.ElementTree.parse(full_name_in)

        # Get the root Element
        root = tree.getroot()

        dcr_core.cfg.glob.text_parser = dcr_core.nlp.cls_text_parser.TextParser()

        for child in root:
            child_tag = child.tag[dcr_core.nlp.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.nlp.cls_nlp_core.NLPCore.PARSE_ELEM_DOCUMENT:
                    dcr_core.cfg.glob.text_parser.parse_tag_document(
                        directory_name=os.path.dirname(full_name_in),
                        document_id=document_id,
                        environment_variant=dcr_core.cfg.glob.setup.environment_variant,
                        file_name_curr=os.path.basename(full_name_in),
                        file_name_next=full_name_out,
                        file_name_orig=file_name_orig,
                        no_pdf_pages=no_pdf_pages,
                        parent=child,
                        parent_tag=child_tag,
                    )
                case dcr_core.nlp.cls_nlp_core.NLPCore.PARSE_ELEM_CREATION:
                    pass
    except FileNotFoundError as err:
        error_msg = ERROR_61_901.replace("{full_name}", full_name_in).replace("{error_type}", str(type(err))).replace("{error}", str(err))
        return error_msg[:6], error_msg

    return dcr_core.cfg.glob.RETURN_OK
