"""Module cfg.glob: DCR Global Data."""

import nlp.cls_line_type_heading
import nlp.cls_line_type_list_bullet
import nlp.cls_line_type_list_number
import nlp.cls_line_type_table
import nlp.cls_text_parser
import nlp.cls_tokenizer_spacy

import dcr_core.nlp.cls_line_type_headers_footers
import dcr_core.nlp.cls_line_type_toc

# -----------------------------------------------------------------------------
# Global Constants.
# -----------------------------------------------------------------------------
INFORMATION_NOT_YET_AVAILABLE = "n/a"

LOGGER_FATAL_HEAD = "FATAL ERROR: program abort =====> "
LOGGER_FATAL_TAIL = " <===== FATAL ERROR"
LOGGER_PROGRESS_UPDATE = "Progress update "

RETURN_OK = ("ok", "")

# -----------------------------------------------------------------------------
# Global Variables.
# -----------------------------------------------------------------------------
line_type_headers_footers: type[dcr_core.nlp.cls_line_type_headers_footers.LineTypeHeaderFooters]
line_type_heading: type[nlp.cls_line_type_heading.LineTypeHeading]
line_type_list_bullet: type[nlp.cls_line_type_list_bullet.LineTypeListBullet]
line_type_list_number: type[nlp.cls_line_type_list_number.LineTypeListNumber]
line_type_table: type[nlp.cls_line_type_table.LineTypeTable]
line_type_toc: type[dcr_core.nlp.cls_line_type_toc.LineTypeToc]

text_parser: type[nlp.cls_text_parser.TextParser]

tokenizer_spacy: type[nlp.cls_tokenizer_spacy.TokenizerSpacy]
