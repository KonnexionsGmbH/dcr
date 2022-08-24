# Copyright (c) 2022 Konnexions GmbH. All rights reserved. Use of this
# source code is governed by the Konnexions Public License (KX-PL)
# Version 2020.05, that can be found in the LICENSE file.

"""Module stub file."""
LINE_TET_DOCUMENT_OPT_LIST: str
LINE_TET_PAGE_OPT_LIST: str
LINE_XML_VARIATION: str
PAGE_TET_DOCUMENT_OPT_LIST: str
PAGE_TET_PAGE_OPT_LIST: str
PAGE_XML_VARIATION: str
WORD_TET_DOCUMENT_OPT_LIST: str
WORD_TET_PAGE_OPT_LIST: str
WORD_XML_VARIATION: str

def extract_text_from_pdf() -> None: ...
def extract_text_from_pdf_file(document_opt_list: str, page_opt_list: str, xml_variation: str) -> bool: ...
