import glob
import os.path

import defusedxml
import defusedxml.ElementTree
import pdf2image
import pypandoc
import PyPDF2
import pytesseract
from pdf2image.exceptions import PDFPageCountError

import dcr_core.cls_nlp_core
import dcr_core.cls_setup
import dcr_core.cls_text_parser
import dcr_core.core_glob
import dcr_core.core_utils
import PDFlib.TET

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_21_901 = (
    "21.901 Issue (p_2_i): Processing file '{full_name}' with pdf2image failed - " + "error type: '{error_type}' - error: '{error}'."
)
ERROR_31_902 = (
    "31.902 Issue (n_2_p): The file '{full_name}' cannot be converted to an "
    + "'pdf' document - "
    + "error type: '{error_type}' - error: '{error_msg}'."
)
ERROR_41_901 = (
    "41.901 Issue (ocr): Converting the file '{full_name}' with Tesseract OCR failed - " + "error type: '{error_type}' - error: '{error}'."
)
ERROR_51_901 = "51.901 Issue (tet): Opening document '{full_name}' - " + "error no: '{error_no}' - api: '{api_name}' - error: '{error}'."
ERROR_61_901 = "61.901 Issue (s_p_j): Parsing the file '{full_name}' failed - " + "error type: '{error_type}' - error: '{error}'."
ERROR_71_901 = "71.901 Issue (tkn): Tokenizing the file '{full_name}' failed - " + "error type: '{error_type}' - error: '{error}'."

PANDOC_PDF_ENGINE_LULATEX = "lulatex"
PANDOC_PDF_ENGINE_XELATEX = "xelatex"


# -----------------------------------------------------------------------------
# Converting a Non-PDF file to a PDF file.
# -----------------------------------------------------------------------------
def pandoc_process(
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
            dcr_core.core_glob.FILE_TYPE_PDF,
            extra_args=extra_args,
            outputfile=full_name_out,
        )

    except (FileNotFoundError, RuntimeError) as err:
        error_msg = ERROR_31_902.replace("{full_name}", full_name_in).replace("{error_type}", str(type(err))).replace("{error}", str(err))
        return error_msg[:6], error_msg

    return dcr_core.core_glob.RETURN_OK


# -----------------------------------------------------------------------------
# Extracting the text from the PDF document.
# -----------------------------------------------------------------------------
def parser_process(
    full_name_in: str,
    full_name_out: str,
    no_pdf_pages: int,
    document_id: int = -1,
    file_name_orig: str = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE,
) -> tuple[str, str]:
    """Extracting the text from the PDF document.

    From the line-oriented XML output file of PDFlib TET,
    the text and relevant metadata are extracted with the
    help of an XML parser and stored in a JSON file.

    Args:
        full_name_in (str):
                The directory name and file name of the input file.
        full_name_out (str):
                The directory name and file name of the output file.
        no_pdf_pages (int):
                Total number of PDF pages.
        document_id (int, optional):
                The identification number of the document.
                Defaults to -1.
        file_name_orig (str, optional):
                The file name of the originating document.
                Defaults to dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE.

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

        dcr_core.core_glob.text_parser = dcr_core.cls_text_parser.TextParser()

        for child in root:
            child_tag = child.tag[dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_FROM :]
            match child_tag:
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_DOCUMENT:
                    dcr_core.core_glob.text_parser.parse_tag_document(
                        directory_name=os.path.dirname(full_name_in),
                        document_id=document_id,
                        environment_variant=dcr_core.core_glob.setup.environment_variant,
                        file_name_curr=os.path.basename(full_name_in),
                        file_name_next=full_name_out,
                        file_name_orig=file_name_orig,
                        no_pdf_pages=no_pdf_pages,
                        parent=child,
                        parent_tag=child_tag,
                    )
                case dcr_core.cls_nlp_core.NLPCore.PARSE_ELEM_CREATION:
                    pass
    except FileNotFoundError as err:
        error_msg = ERROR_61_901.replace("{full_name}", full_name_in).replace("{error_type}", str(type(err))).replace("{error}", str(err))
        return error_msg[:6], error_msg

    return dcr_core.core_glob.RETURN_OK


# -----------------------------------------------------------------------------
# Converting a scanned PDF file to a set of image files.
# -----------------------------------------------------------------------------
def pdf2image_process(
    full_name_in: str,
) -> tuple[str, str, list[tuple[str, str]]]:
    """Converting a scanned PDF file to a set of image files.

    To extract the text from a scanned PDF document, it must
    first be converted into one or more image files, depending
    on the number of pages. Then these image files are converted
    into a normal PDF document with the help of an OCR programme.
    The input file for this method must be a scanned PDF document,
    which is then converted into image files with the help of PDF2Image.

    Args:
        full_name_in (str):
                The directory name and file name of the input file.

    Returns:
        tuple[str, str, list[tuple[str,str]]]:
                ("ok", "", [...]) if the processing has been completed successfully,
                                  otherwise a corresponding error code and error message.
    """
    try:
        images = pdf2image.convert_from_path(full_name_in)

        children: list[tuple[str, str]] = []
        no_children = 0

        directory_name = os.path.dirname(full_name_in)
        stem_name = os.path.splitext(os.path.basename(full_name_in))[0]

        try:
            os.remove(
                dcr_core.core_utils.get_full_name(
                    directory_name,
                    stem_name
                    + "_*."
                    + (
                        dcr_core.core_glob.FILE_TYPE_PNG
                        if dcr_core.core_glob.setup.pdf2image_type == dcr_core.cls_setup.Setup.PDF2IMAGE_TYPE_PNG
                        else dcr_core.core_glob.FILE_TYPE_JPEG
                    ),
                )
            )
        except OSError:
            pass

        # Store the image pages
        for img in images:
            no_children += 1

            file_name_next = (
                stem_name
                + "_"
                + str(no_children)
                + "."
                + (
                    dcr_core.core_glob.FILE_TYPE_PNG
                    if dcr_core.core_glob.setup.pdf2image_type == dcr_core.cls_setup.Setup.PDF2IMAGE_TYPE_PNG
                    else dcr_core.core_glob.FILE_TYPE_JPEG
                )
            )

            full_name_next = dcr_core.core_utils.get_full_name(
                directory_name,
                file_name_next,
            )

            img.save(
                full_name_next,
                dcr_core.core_glob.setup.pdf2image_type,
            )

            children.append((file_name_next, full_name_next))
    except PDFPageCountError as err:
        error_msg = ERROR_21_901.replace("{full_name}", full_name_in).replace("{error_type}", str(type(err))).replace("{error}", str(err))
        return error_msg[:6], error_msg, []

    return dcr_core.core_glob.RETURN_OK[0], dcr_core.core_glob.RETURN_OK[1], children


# -----------------------------------------------------------------------------
# Processing a PDF file with PDFlib TET.
# -----------------------------------------------------------------------------
def pdflib_process(
    full_name_in: str,
    full_name_out: str,
    document_opt_list: str,
    page_opt_list: str,
) -> tuple[str, str]:
    """Processing a PDF file with PDFlib TET.

    The data from a PDF file is made available in XML files
    with the help of PDFlib TET. The granularity of the XML
    files can be word, line or paragraph depending on the
    document and page options selected.

    Args:
        full_name_in (str):
                Directory name and file name of the input file.
        full_name_out (str):
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
    tet = PDFlib.TET.TET()

    doc_opt_list = f"tetml={{filename={{{full_name_out}}}}} {document_opt_list}"

    if (file_curr := tet.open_document(full_name_in, doc_opt_list)) == -1:
        error_msg = (
            ERROR_51_901.replace("{full_name}", full_name_in)
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

    return dcr_core.core_glob.RETURN_OK


# -----------------------------------------------------------------------------
# Converting image files to PDF files via OCR.
# -----------------------------------------------------------------------------
def tesseract_process(
    full_name_in: str,
    full_name_out: str,
    language_tesseract: str,
) -> tuple[str, str, list[str]]:
    """Converting image files to PDF files via OCR.

    The documents of the following document types are converted
    to the pdf format using Tesseract OCR:

    - bmp  - bitmap image file
    - gif  - Graphics Interchange Format
    - jp2  - JPEG 2000
    - jpeg - Joint Photographic Experts Group
    - png  - Portable Network Graphics
    - pnm  - portable any-map format
    - tif  - Tag Image File Format
    - tiff - Tag Image File Format
    - webp - Image file format with lossless and lossy compression

    After processing with Tesseract OCR, the files split previously
    into multiple image files are combined into a single pdf document.

    Args:
        full_name_in (str):
                The directory name and file name of the input file.
        full_name_out (str):
                The directory name and file name of the output file.
        language_tesseract (str):
                The Tesseract name of the document language.

    Returns:
        tuple[str, str, list[str]]:
                ("ok", "", [...]) if the processing has been completed successfully,
                                  otherwise a corresponding error code and error message.
    """
    children: list[str] = []

    pdf_writer = PyPDF2.PdfWriter()

    for full_name in sorted(glob.glob(full_name_in)):
        try:
            pdf = pytesseract.image_to_pdf_or_hocr(
                extension="pdf",
                image=full_name,
                lang=language_tesseract,
                timeout=dcr_core.core_glob.setup.tesseract_timeout,
            )

            with open(full_name_out, "w+b") as file_handle:
                # pdf type is bytes by default
                file_handle.write(pdf)

            pdf_reader = PyPDF2.PdfReader(full_name_out)

            for page in pdf_reader.pages:
                # Add each page to the writer object
                pdf_writer.add_page(page)

            children.append(full_name)

        except RuntimeError as err:
            error_msg = (
                ERROR_41_901.replace("{full_name}", full_name_in).replace("{error_type}", str(type(err))).replace("{error}", str(err))
            )
            return error_msg[:6], error_msg, []

    # Write out the merged PDF
    with open(full_name_out, "wb") as file_handle:
        pdf_writer.write(file_handle)

    return dcr_core.core_glob.RETURN_OK[0], dcr_core.core_glob.RETURN_OK[1], children


# -----------------------------------------------------------------------------
# Tokenizing the text from the PDF document.
# -----------------------------------------------------------------------------
def tokenizer_process(
    full_name_in: str,
    full_name_out: str,
    pipeline_name: str,
    document_id: int = -1,
    file_name_orig: str = dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE,
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
                Defaults to dcr_core.core_glob.INFORMATION_NOT_YET_AVAILABLE.
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
        dcr_core.core_glob.text_parser = dcr_core.cls_text_parser.TextParser.from_files(
            file_encoding=dcr_core.core_glob.FILE_ENCODING_DEFAULT, full_name_line=full_name_in
        )

        dcr_core.core_glob.tokenizer_spacy.process_document(
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

    return dcr_core.core_glob.RETURN_OK
