import dcr_core.cls_line_type_headers_footers
import dcr_core.cls_line_type_heading
import dcr_core.cls_line_type_list_bullet
import dcr_core.cls_line_type_list_number
import dcr_core.cls_line_type_table
import dcr_core.cls_line_type_toc
import dcr_core.cls_setup
import dcr_core.cls_text_parser
import dcr_core.cls_tokenizer_spacy

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
FILE_ENCODING_DEFAULT = "utf-8"

FILE_TYPE_JPEG = "jpeg"
FILE_TYPE_JPG = "jpg"
FILE_TYPE_JSON = "json"
FILE_TYPE_PANDOC: list[str] = [
    "csv",
    "docx",
    "epub",
    "html",
    "odt",
    "rst",
    "rtf",
]
FILE_TYPE_PDF = "pdf"
FILE_TYPE_PNG = "png"
FILE_TYPE_TESSERACT: list[str] = [
    "bmp",
    "gif",
    "jp2",
    "jpeg",
    "jpg",
    "png",
    "pnm",
    "tif",
    "tiff",
    "webp",
]
FILE_TYPE_TIF = "tif"
FILE_TYPE_TIFF = "tiff"
FILE_TYPE_XML = "xml"

INFORMATION_NOT_YET_AVAILABLE = "n/a"

LOGGER_FATAL_HEAD = "FATAL ERROR: program abort =====> "
LOGGER_FATAL_TAIL = " <===== FATAL ERROR"
LOGGER_PROGRESS_UPDATE = "Progress update "

RETURN_OK = ("ok", "")

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
line_type_headers_footers: dcr_core.cls_line_type_headers_footers.LineTypeHeaderFooters
line_type_heading: dcr_core.cls_line_type_heading.LineTypeHeading
line_type_list_bullet: dcr_core.cls_line_type_list_bullet.LineTypeListBullet
line_type_list_number: dcr_core.cls_line_type_list_number.LineTypeListNumber
line_type_table: dcr_core.cls_line_type_table.LineTypeTable
line_type_toc: dcr_core.cls_line_type_toc.LineTypeToc

setup: dcr_core.cls_setup.Setup

text_parser: dcr_core.cls_text_parser.TextParser

tokenizer_spacy: dcr_core.cls_tokenizer_spacy.TokenizerSpacy
