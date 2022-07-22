import os

import pdf2image
from pdf2image.exceptions import PDFPageCountError

import dcr_core.cfg.cls_setup
import dcr_core.cfg.glob
import dcr_core.utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------
ERROR_21_901 = "21.901 Issue (p_2_i): Processing file '{full_name}' with pdf2image failed - " + "error type: '{error_type}' - error: '{error}'."


# -----------------------------------------------------------------------------
# Converting a scanned PDF file to a set of image files.
# -----------------------------------------------------------------------------
def process(
    full_name_in: str,
) -> tuple[str, str, list[tuple[str, str]]]:
    """Converting a scanned PDF file to a set of image files.

    The following file formats are converted into
    PDF format here with the help of Pandoc:

    - tokens with the means of SpaCy.

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
                dcr_core.utils.get_full_name(
                    directory_name,
                    stem_name
                    + "_*."
                    + (
                        dcr_core.cfg.glob.FILE_TYPE_PNG
                        if dcr_core.cfg.glob.setup.pdf2image_type == dcr_core.cfg.cls_setup.Setup.PDF2IMAGE_TYPE_PNG
                        else dcr_core.cfg.glob.FILE_TYPE_JPEG
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
                    dcr_core.cfg.glob.FILE_TYPE_PNG
                    if dcr_core.cfg.glob.setup.pdf2image_type == dcr_core.cfg.cls_setup.Setup.PDF2IMAGE_TYPE_PNG
                    else dcr_core.cfg.glob.FILE_TYPE_JPEG
                )
            )

            full_name_next = dcr_core.utils.get_full_name(
                directory_name,
                file_name_next,
            )

            img.save(
                full_name_next,
                dcr_core.cfg.glob.setup.pdf2image_type,
            )

            children.append((file_name_next, full_name_next))
    except PDFPageCountError as err:
        error_msg = ERROR_21_901.replace("{full_name}", full_name_in).replace("{error_type}", str(type(err))).replace("{error}", str(err))
        return error_msg[:6], error_msg, []

    return dcr_core.cfg.glob.RETURN_OK[0], dcr_core.cfg.glob.RETURN_OK[1], children
