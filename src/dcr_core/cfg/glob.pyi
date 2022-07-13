"""Library Stub."""

import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy

import dcr_core.nlp.cls_line_type_headers_footers
import dcr_core.nlp.cls_line_type_heading
import dcr_core.nlp.cls_line_type_list_bullet
import dcr_core.nlp.cls_line_type_list_number
import dcr_core.nlp.cls_line_type_table
import dcr_core.nlp.cls_line_type_toc

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
FILE_TYPE_JPEG: str
FILE_TYPE_JPG: str
FILE_TYPE_JSON: str
FILE_TYPE_PANDOC: list[str]
FILE_TYPE_PDF: str
FILE_TYPE_PNG: str
FILE_TYPE_TESSERACT: list[str]
FILE_TYPE_TIF: str
FILE_TYPE_TIFF: str
FILE_TYPE_XML: str

INFORMATION_NOT_YET_AVAILABLE: str

LOGGER_FATAL_HEAD: str
LOGGER_FATAL_TAIL: str
LOGGER_PROGRESS_UPDATE: str

RETURN_OK: tuple[str, str]

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
line_type_headers_footers: type[dcr_core.nlp.cls_line_type_headers_footers.LineTypeHeaderFooters]
line_type_heading: type[dcr_core.nlp.cls_line_type_heading.LineTypeHeading]
line_type_list_bullet: type[dcr_core.nlp.cls_line_type_list_bullet.LineTypeListBullet]
line_type_list_number: type[dcr_core.nlp.cls_line_type_list_number.LineTypeListNumber]
line_type_table: type[dcr_core.nlp.cls_line_type_table.LineTypeTable]
line_type_toc: type[dcr_core.nlp.cls_line_type_toc.LineTypeToc]

text_parser: type[nlp.cls_text_parser.TextParser]

tokenizer_spacy: type[nlp.cls_tokenizer_spacy.TokenizerSpacy]
