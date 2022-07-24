import glob

import PyPDF2
import pytesseract

import dcr_core.cfg.cls_setup
import dcr_core.cfg.glob
import dcr_core.utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_41_901 = "41.901 Issue (ocr): Converting the file '{full_name}' with Tesseract OCR failed - " + "error type: '{error_type}' - error: '{error}'."


# -----------------------------------------------------------------------------
# Converting image files to PDF files via OCR.
# -----------------------------------------------------------------------------
def process(
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
                timeout=dcr_core.cfg.glob.setup.tesseract_timeout,
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
            error_msg = ERROR_41_901.replace("{full_name}", full_name_in).replace("{error_type}", str(type(err))).replace("{error}", str(err))
            return error_msg[:6], error_msg, []

    # Write out the merged PDF
    with open(full_name_out, "wb") as file_handle:
        pdf_writer.write(file_handle)

    return dcr_core.cfg.glob.RETURN_OK[0], dcr_core.cfg.glob.RETURN_OK[1], children
