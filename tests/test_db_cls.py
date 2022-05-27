# pylint: disable=unused-argument
"""Testing Module db.cls_..."""
import time

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_document
import db.cls_language
import db.cls_run
import db.cls_token
import db.cls_version
import db.dml
import db.driver
import pytest
import utils

import dcr

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=C0302
# @pytest.mark.issue
MISSING_ID: int = 4711


# -----------------------------------------------------------------------------
# Check existing action object.
# -----------------------------------------------------------------------------
def check_existing_action():
    """Check existing action object."""
    expected_values = (
        1,
        db.cls_run.Run.ACTION_CODE_INBOX,
        db.cls_run.Run.get_action_text(db.cls_run.Run.ACTION_CODE_INBOX),
        cfg.glob.setup.directory_inbox,
        "inbox",
        "",
        "",
        0,
        "pdf_text_ok.pdf",
        53651,
        1,
        1,
        1,
        0,
        3,
        db.cls_document.Document.DOCUMENT_STATUS_END,
    )

    cfg.glob.action_curr = db.cls_action.Action.from_id(expected_values[0])

    actual_values = cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != tuple(expected_values):
        print(f"issue with dbt action instance id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt action id={expected_values[0]} - see above"

    cfg.glob.action_curr.exists()

    # -----------------------------------------------------------------------------
    # Finalise the current action with error.
    # -----------------------------------------------------------------------------
    cfg.glob.action_curr.finalise_error("error_code", "error_msg")

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    cfg.glob.action_curr.get_file_type()

    cfg.glob.action_curr.action_file_name = ""

    cfg.glob.action_curr.get_file_type()

    cfg.glob.action_curr.action_file_name = expected_values[8]

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name.
    # -----------------------------------------------------------------------------
    cfg.glob.action_curr.get_stem_name()

    cfg.glob.action_curr.action_file_name = ""

    cfg.glob.action_curr.get_stem_name()

    cfg.glob.action_curr.action_file_name = expected_values[8]

    # -----------------------------------------------------------------------------
    # Select unprocessed actions based on action_code und document id.
    # -----------------------------------------------------------------------------
    with cfg.glob.db_orm_engine.begin() as conn:
        cfg.glob.action_curr.select_action_by_action_code_id_document(
            conn=conn, action_code=db.cls_run.Run.ACTION_CODE_INBOX, id_document=1
        )


# -----------------------------------------------------------------------------
# Check existing document object.
# -----------------------------------------------------------------------------
def check_existing_document():
    """Check existing document object."""
    expected_values = pytest.helpers.get_values_document()

    expected_values[0] = 1
    expected_values[1] = "tkn"
    expected_values[2] = "tokenize      (nlp)"
    expected_values[10] = 8
    expected_values[11] = 3
    expected_values[13] = db.cls_document.Document.DOCUMENT_STATUS_END

    cfg.glob.document = db.cls_document.Document.from_id(expected_values[0])

    actual_values = cfg.glob.document.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print(f"issue with dbt document cfg.glob.document id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt document id={expected_values[0]} - see above"

    cfg.glob.document.exists()

    # -----------------------------------------------------------------------------
    # Get the duplicate file name based on the hash key.
    # -----------------------------------------------------------------------------
    db.cls_document.Document.select_duplicate_file_name_by_sha256(MISSING_ID, expected_values[12])

    # -----------------------------------------------------------------------------
    # Finalise the current row with error.
    # -----------------------------------------------------------------------------
    cfg.glob.document.finalise_error("error_code", "error_msg")

    # -----------------------------------------------------------------------------
    # Get the file type from the file name.
    # -----------------------------------------------------------------------------
    cfg.glob.document.document_file_name = ""

    cfg.glob.document.get_file_type()

    cfg.glob.document.document_file_name = expected_values[7]

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name - positive.
    # -----------------------------------------------------------------------------
    cfg.glob.document.get_stem_name()

    # -----------------------------------------------------------------------------
    # Get the stem name from the file name - negative.
    # -----------------------------------------------------------------------------
    cfg.glob.document.document_file_name = ""

    cfg.glob.document.get_stem_name()

    cfg.glob.document.document_file_name = expected_values[7]

    # -----------------------------------------------------------------------------
    # Get the stem name from the first processed document.
    # -----------------------------------------------------------------------------
    cfg.glob.document.document_file_name = ""

    cfg.glob.document.get_stem_name_next()

    cfg.glob.document.document_file_name = expected_values[7]


# -----------------------------------------------------------------------------
# Check existing language object.
# -----------------------------------------------------------------------------
def check_existing_language():
    """Check existing language object."""
    expected_values = [
        1,
        True,
        "eng",
        "en",
        "en_core_web_trf",
        "eng",
        utils.get_os_independent_name("data/inbox_test"),
        "English",
    ]

    cfg.glob.language = db.cls_language.Language.from_id(expected_values[0])

    actual_values = cfg.glob.language.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print(f"issue with dbt language cfg.glob.language id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt language id={expected_values[0]} - see above"

    cfg.glob.language.exists()


# -----------------------------------------------------------------------------
# Check existing run object.
# -----------------------------------------------------------------------------
def check_existing_run():
    """Check existing run object."""
    expected_values = pytest.helpers.get_values_run()

    expected_values[0] = 1
    expected_values[4] = db.cls_document.Document.DOCUMENT_STATUS_END
    expected_values[5] = 0
    expected_values[6] = 1
    expected_values[7] = 1

    cfg.glob.run = db.cls_run.Run.from_id(expected_values[0])

    actual_values = cfg.glob.run.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print(f"issue with dbt run cfg.glob.run id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt run id={expected_values[0]} - see above"

    cfg.glob.run.exists()


# -----------------------------------------------------------------------------
# Check existing token object.
# -----------------------------------------------------------------------------
def check_existing_token():
    """Check existing token object."""
    db.driver.connect_db()

    expected_values = [
        1,
        cfg.glob.document.document_id,
        {
            "pageNo": 1,
            "noTokensInPage": 221,
            "tokens": [
                {
                    "tknEntIob_": "O",
                    "tknI": 0,
                    "tknIsOov": True,
                    "tknIsSentStart": True,
                    "tknIsTitle": True,
                    "tknLemma_": "Start",
                    "tknNorm_": "start",
                    "tknPos_": "PROPN",
                    "tknTag_": "NNP",
                    "tknText": "Start",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 1,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "document",
                    "tknNorm_": "document",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "Document",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 2,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknIsSentEnd": True,
                    "tknLemma_": "...",
                    "tknNorm_": "...",
                    "tknPos_": "PUNCT",
                    "tknTag_": ":",
                    "tknText": "...",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 3,
                    "tknIsOov": True,
                    "tknIsSentStart": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 4,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "Konnexions",
                    "tknNorm_": "konnexions",
                    "tknPos_": "PROPN",
                    "tknTag_": "NNP",
                    "tknText": "Konnexions",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 5,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "Public",
                    "tknNorm_": "public",
                    "tknPos_": "PROPN",
                    "tknTag_": "NNP",
                    "tknText": "Public",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 6,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "License",
                    "tknNorm_": "license",
                    "tknPos_": "PROPN",
                    "tknTag_": "NNP",
                    "tknText": "License",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 7,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": "(",
                    "tknNorm_": "(",
                    "tknPos_": "PUNCT",
                    "tknTag_": "-LRB-",
                    "tknText": "(",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 8,
                    "tknIsOov": True,
                    "tknLemma_": "KX",
                    "tknNorm_": "kx",
                    "tknPos_": "PROPN",
                    "tknTag_": "NNP",
                    "tknText": "KX",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 9,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": "-",
                    "tknNorm_": "-",
                    "tknPos_": "PUNCT",
                    "tknTag_": "HYPH",
                    "tknText": "-",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 10,
                    "tknIsOov": True,
                    "tknLemma_": "PL",
                    "tknNorm_": "pl",
                    "tknPos_": "PROPN",
                    "tknTag_": "NNP",
                    "tknText": "PL",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 11,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ")",
                    "tknNorm_": ")",
                    "tknPos_": "PUNCT",
                    "tknTag_": "-RRB-",
                    "tknText": ")",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 12,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 13,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "version",
                    "tknNorm_": "version",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "Version",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 14,
                    "tknIsOov": True,
                    "tknLemma_": "2020.05",
                    "tknLikeNum": True,
                    "tknNorm_": "2020.05",
                    "tknPos_": "NUM",
                    "tknTag_": "CD",
                    "tknText": "2020.05",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 15,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": ",",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "B",
                    "tknEntType_": "DATE",
                    "tknI": 16,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknIsTitle": True,
                    "tknLemma_": "May",
                    "tknNorm_": "may",
                    "tknPos_": "PROPN",
                    "tknTag_": "NNP",
                    "tknText": "May",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "I",
                    "tknEntType_": "DATE",
                    "tknI": 17,
                    "tknIsDigit": True,
                    "tknIsOov": True,
                    "tknLemma_": "2020",
                    "tknLikeNum": True,
                    "tknNorm_": "2020",
                    "tknPos_": "NUM",
                    "tknTag_": "CD",
                    "tknText": "2020",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 18,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 19,
                    "tknIsOov": True,
                    "tknLemma_": "https://github.com/konnexionsgmbh/shared_resources"
                    + "/blob/master/license/kx-pl-2020.05.pdf",
                    "tknLikeUrl": True,
                    "tknNorm_": "https://github.com/konnexionsgmbh/shared_resources"
                    + "/blob/master/license/kx-pl-2020.05.pdf",
                    "tknPos_": "X",
                    "tknTag_": "ADD",
                    "tknText": "https://github.com/KonnexionsGmbH/shared_resources"
                    + "/blob/master/License/KX-PL-2020.05.pdf",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 20,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 21,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknIsTitle": True,
                    "tknLemma_": "this",
                    "tknNorm_": "this",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "This",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 22,
                    "tknIsOov": True,
                    "tknLemma_": "license",
                    "tknNorm_": "license",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "license",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 23,
                    "tknIsOov": True,
                    "tknLemma_": "govern",
                    "tknNorm_": "governs",
                    "tknPos_": "VERB",
                    "tknTag_": "VBZ",
                    "tknText": "governs",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 24,
                    "tknIsOov": True,
                    "tknLemma_": "use",
                    "tknNorm_": "use",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "use",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 25,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "of",
                    "tknNorm_": "of",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "of",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 26,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "the",
                    "tknNorm_": "the",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "the",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 27,
                    "tknIsOov": True,
                    "tknLemma_": "accompany",
                    "tknNorm_": "accompanying",
                    "tknPos_": "VERB",
                    "tknTag_": "VBG",
                    "tknText": "accompanying",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 28,
                    "tknIsOov": True,
                    "tknLemma_": "software",
                    "tknNorm_": "software",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "software",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 29,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknIsSentEnd": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "PUNCT",
                    "tknTag_": ".",
                    "tknText": ".",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 30,
                    "tknIsOov": True,
                    "tknIsSentStart": True,
                    "tknIsStop": True,
                    "tknIsTitle": True,
                    "tknLemma_": "if",
                    "tknNorm_": "if",
                    "tknPos_": "SCONJ",
                    "tknTag_": "IN",
                    "tknText": "If",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 31,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "you",
                    "tknNorm_": "you",
                    "tknPos_": "PRON",
                    "tknTag_": "PRP",
                    "tknText": "you",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 32,
                    "tknIsOov": True,
                    "tknLemma_": "use",
                    "tknNorm_": "use",
                    "tknPos_": "VERB",
                    "tknTag_": "VBP",
                    "tknText": "use",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 33,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "the",
                    "tknNorm_": "the",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "the",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 34,
                    "tknIsOov": True,
                    "tknLemma_": "software",
                    "tknNorm_": "software",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "software",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 35,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": ",",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 36,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "you",
                    "tknNorm_": "you",
                    "tknPos_": "PRON",
                    "tknTag_": "PRP",
                    "tknText": "you",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 37,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 38,
                    "tknIsOov": True,
                    "tknLemma_": "accept",
                    "tknNorm_": "accept",
                    "tknPos_": "VERB",
                    "tknTag_": "VB",
                    "tknText": "accept",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 39,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "this",
                    "tknNorm_": "this",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "this",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 40,
                    "tknIsOov": True,
                    "tknLemma_": "license",
                    "tknNorm_": "license",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "license",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 41,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknIsSentEnd": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "PUNCT",
                    "tknTag_": ".",
                    "tknText": ".",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 42,
                    "tknIsOov": True,
                    "tknIsSentStart": True,
                    "tknIsStop": True,
                    "tknIsTitle": True,
                    "tknLemma_": "if",
                    "tknNorm_": "if",
                    "tknPos_": "SCONJ",
                    "tknTag_": "IN",
                    "tknText": "If",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 43,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "you",
                    "tknNorm_": "you",
                    "tknPos_": "PRON",
                    "tknTag_": "PRP",
                    "tknText": "you",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 44,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "do",
                    "tknNorm_": "do",
                    "tknPos_": "AUX",
                    "tknTag_": "VBP",
                    "tknText": "do",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 45,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "not",
                    "tknNorm_": "not",
                    "tknPos_": "PART",
                    "tknTag_": "RB",
                    "tknText": "not",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 46,
                    "tknIsOov": True,
                    "tknLemma_": "accept",
                    "tknNorm_": "accept",
                    "tknPos_": "VERB",
                    "tknTag_": "VB",
                    "tknText": "accept",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 47,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "the",
                    "tknNorm_": "the",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "the",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 48,
                    "tknIsOov": True,
                    "tknLemma_": "license",
                    "tknNorm_": "license",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "license",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 49,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": ",",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 50,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "do",
                    "tknNorm_": "do",
                    "tknPos_": "AUX",
                    "tknTag_": "VB",
                    "tknText": "do",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 51,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "not",
                    "tknNorm_": "not",
                    "tknPos_": "PART",
                    "tknTag_": "RB",
                    "tknText": "not",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 52,
                    "tknIsOov": True,
                    "tknLemma_": "use",
                    "tknNorm_": "use",
                    "tknPos_": "VERB",
                    "tknTag_": "VB",
                    "tknText": "use",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 53,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "the",
                    "tknNorm_": "the",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "the",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 54,
                    "tknIsOov": True,
                    "tknLemma_": "software",
                    "tknNorm_": "software",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "software",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 55,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknIsSentEnd": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "PUNCT",
                    "tknTag_": ".",
                    "tknText": ".",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 56,
                    "tknIsOov": True,
                    "tknIsSentStart": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "B",
                    "tknEntType_": "CARDINAL",
                    "tknI": 57,
                    "tknIsDigit": True,
                    "tknIsOov": True,
                    "tknLemma_": "1",
                    "tknLikeNum": True,
                    "tknNorm_": "1",
                    "tknPos_": "X",
                    "tknTag_": "LS",
                    "tknText": "1",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 58,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "PUNCT",
                    "tknTag_": ".",
                    "tknText": ".",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 59,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "definition",
                    "tknNorm_": "definitions",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "Definitions",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 60,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknIsSentEnd": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "PUNCT",
                    "tknTag_": ".",
                    "tknText": ".",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 61,
                    "tknIsOov": True,
                    "tknIsSentStart": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 62,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknIsTitle": True,
                    "tknLemma_": "the",
                    "tknNorm_": "the",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "The",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 63,
                    "tknIsOov": True,
                    "tknLemma_": "term",
                    "tknNorm_": "terms",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "terms",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 64,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "``",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 65,
                    "tknIsOov": True,
                    "tknLemma_": "reproduce",
                    "tknNorm_": "reproduce",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "reproduce",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 66,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "''",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 67,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": "''",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 68,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "``",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 69,
                    "tknIsOov": True,
                    "tknLemma_": "reproduction",
                    "tknNorm_": "reproduction",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "reproduction",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 70,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "''",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 71,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": "''",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 72,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "``",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 73,
                    "tknIsOov": True,
                    "tknLemma_": "derivative",
                    "tknNorm_": "derivative",
                    "tknPos_": "ADJ",
                    "tknTag_": "JJ",
                    "tknText": "derivative",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 74,
                    "tknIsOov": True,
                    "tknLemma_": "work",
                    "tknNorm_": "works",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "works",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 75,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "''",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 76,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": "''",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 77,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "and",
                    "tknNorm_": "and",
                    "tknPos_": "CCONJ",
                    "tknTag_": "CC",
                    "tknText": "and",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 78,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "``",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 79,
                    "tknIsOov": True,
                    "tknLemma_": "distribution",
                    "tknNorm_": "distribution",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "distribution",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 80,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "''",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 81,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 82,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "have",
                    "tknNorm_": "have",
                    "tknPos_": "VERB",
                    "tknTag_": "VBP",
                    "tknText": "have",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 83,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "the",
                    "tknNorm_": "the",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "the",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 84,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "same",
                    "tknNorm_": "same",
                    "tknPos_": "ADJ",
                    "tknTag_": "JJ",
                    "tknText": "same",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 85,
                    "tknIsOov": True,
                    "tknLemma_": "meaning",
                    "tknNorm_": "meaning",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "meaning",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 86,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "here",
                    "tknNorm_": "here",
                    "tknPos_": "ADV",
                    "tknTag_": "RB",
                    "tknText": "here",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 87,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "as",
                    "tknNorm_": "as",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "as",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 88,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "under",
                    "tknNorm_": "under",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "under",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "B",
                    "tknEntType_": "GPE",
                    "tknI": 89,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "U.S.",
                    "tknNorm_": "u.s.",
                    "tknPos_": "PROPN",
                    "tknTag_": "NNP",
                    "tknText": "U.S.",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 90,
                    "tknIsOov": True,
                    "tknLemma_": "copyright",
                    "tknNorm_": "copyright",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "copyright",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 91,
                    "tknIsOov": True,
                    "tknLemma_": "law",
                    "tknNorm_": "law",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "law",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 92,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknIsSentEnd": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "PUNCT",
                    "tknTag_": ".",
                    "tknText": ".",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 93,
                    "tknIsOov": True,
                    "tknIsSentStart": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 94,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknIsTitle": True,
                    "tknLemma_": "a",
                    "tknNorm_": "a",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "A",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 95,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "``",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 96,
                    "tknIsOov": True,
                    "tknLemma_": "contribution",
                    "tknNorm_": "contribution",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "contribution",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 97,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "''",
                    "tknText": '"',
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 98,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "be",
                    "tknNorm_": "is",
                    "tknPos_": "AUX",
                    "tknTag_": "VBZ",
                    "tknText": "is",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 99,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "the",
                    "tknNorm_": "the",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "the",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 100,
                    "tknIsOov": True,
                    "tknLemma_": "original",
                    "tknNorm_": "original",
                    "tknPos_": "ADJ",
                    "tknTag_": "JJ",
                    "tknText": "original",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 101,
                    "tknIsOov": True,
                    "tknLemma_": "software",
                    "tknNorm_": "software",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "software",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 102,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": ",",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 103,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "or",
                    "tknNorm_": "or",
                    "tknPos_": "CCONJ",
                    "tknTag_": "CC",
                    "tknText": "or",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 104,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "any",
                    "tknNorm_": "any",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "any",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 105,
                    "tknIsOov": True,
                    "tknLemma_": "addition",
                    "tknNorm_": "additions",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "additions",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 106,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "or",
                    "tknNorm_": "or",
                    "tknPos_": "CCONJ",
                    "tknTag_": "CC",
                    "tknText": "or",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 107,
                    "tknIsOov": True,
                    "tknLemma_": "change",
                    "tknNorm_": "changes",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "changes",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 108,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "to",
                    "tknNorm_": "to",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "to",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 109,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "the",
                    "tknNorm_": "the",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "the",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 110,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 111,
                    "tknIsOov": True,
                    "tknLemma_": "software",
                    "tknNorm_": "software",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "software",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 112,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknIsSentEnd": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "PUNCT",
                    "tknTag_": ".",
                    "tknText": ".",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 113,
                    "tknIsOov": True,
                    "tknIsSentStart": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 114,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknIsTitle": True,
                    "tknLemma_": "a",
                    "tknNorm_": "a",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "A",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 115,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "``",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 116,
                    "tknIsOov": True,
                    "tknLemma_": "contributor",
                    "tknNorm_": "contributor",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "contributor",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 117,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "''",
                    "tknText": '"',
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 118,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "be",
                    "tknNorm_": "is",
                    "tknPos_": "AUX",
                    "tknTag_": "VBZ",
                    "tknText": "is",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 119,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "any",
                    "tknNorm_": "any",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "any",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 120,
                    "tknIsOov": True,
                    "tknLemma_": "person",
                    "tknNorm_": "person",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "person",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 121,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "that",
                    "tknNorm_": "that",
                    "tknPos_": "PRON",
                    "tknTag_": "WDT",
                    "tknText": "that",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 122,
                    "tknIsOov": True,
                    "tknLemma_": "distribute",
                    "tknNorm_": "distributes",
                    "tknPos_": "VERB",
                    "tknTag_": "VBZ",
                    "tknText": "distributes",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 123,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "its",
                    "tknNorm_": "its",
                    "tknPos_": "PRON",
                    "tknTag_": "PRP$",
                    "tknText": "its",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 124,
                    "tknIsOov": True,
                    "tknLemma_": "contribution",
                    "tknNorm_": "contribution",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "contribution",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 125,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "under",
                    "tknNorm_": "under",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "under",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 126,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "this",
                    "tknNorm_": "this",
                    "tknPos_": "PRON",
                    "tknTag_": "DT",
                    "tknText": "this",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 127,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 128,
                    "tknIsOov": True,
                    "tknLemma_": "license",
                    "tknNorm_": "license",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "license",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 129,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknIsSentEnd": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "PUNCT",
                    "tknTag_": ".",
                    "tknText": ".",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 130,
                    "tknIsOov": True,
                    "tknIsSentStart": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 131,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "``",
                    "tknText": '"',
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 132,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "licensed",
                    "tknNorm_": "licensed",
                    "tknPos_": "ADJ",
                    "tknTag_": "JJ",
                    "tknText": "Licensed",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 133,
                    "tknIsOov": True,
                    "tknLemma_": "patent",
                    "tknNorm_": "patents",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "patents",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 134,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": '"',
                    "tknNorm_": '"',
                    "tknPos_": "PUNCT",
                    "tknTag_": "''",
                    "tknText": '"',
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 135,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "be",
                    "tknNorm_": "are",
                    "tknPos_": "AUX",
                    "tknTag_": "VBP",
                    "tknText": "are",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 136,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "a",
                    "tknNorm_": "a",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "a",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 137,
                    "tknIsOov": True,
                    "tknLemma_": "contributor",
                    "tknNorm_": "contributor",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "contributor",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 138,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "'s",
                    "tknNorm_": "'s",
                    "tknPos_": "PART",
                    "tknTag_": "POS",
                    "tknText": "'s",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 139,
                    "tknIsOov": True,
                    "tknLemma_": "patent",
                    "tknNorm_": "patent",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "patent",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 140,
                    "tknIsOov": True,
                    "tknLemma_": "claim",
                    "tknNorm_": "claims",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "claims",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 141,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "that",
                    "tknNorm_": "that",
                    "tknPos_": "PRON",
                    "tknTag_": "WDT",
                    "tknText": "that",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 142,
                    "tknIsOov": True,
                    "tknLemma_": "read",
                    "tknNorm_": "read",
                    "tknPos_": "VERB",
                    "tknTag_": "VBD",
                    "tknText": "read",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 143,
                    "tknIsOov": True,
                    "tknLemma_": "directly",
                    "tknNorm_": "directly",
                    "tknPos_": "ADV",
                    "tknTag_": "RB",
                    "tknText": "directly",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 144,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "on",
                    "tknNorm_": "on",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "on",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 145,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "its",
                    "tknNorm_": "its",
                    "tknPos_": "PRON",
                    "tknTag_": "PRP$",
                    "tknText": "its",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 146,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 147,
                    "tknIsOov": True,
                    "tknLemma_": "contribution",
                    "tknNorm_": "contribution",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "contribution",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 148,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknIsSentEnd": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "PUNCT",
                    "tknTag_": ".",
                    "tknText": ".",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 149,
                    "tknIsOov": True,
                    "tknIsSentStart": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "B",
                    "tknEntType_": "CARDINAL",
                    "tknI": 150,
                    "tknIsDigit": True,
                    "tknIsOov": True,
                    "tknLemma_": "2",
                    "tknLikeNum": True,
                    "tknNorm_": "2",
                    "tknPos_": "X",
                    "tknTag_": "LS",
                    "tknText": "2",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 151,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "X",
                    "tknTag_": "LS",
                    "tknText": ".",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 152,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "grant",
                    "tknNorm_": "grant",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "Grant",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 153,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "of",
                    "tknNorm_": "of",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "of",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 154,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "right",
                    "tknNorm_": "rights",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "Rights",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 155,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 156,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": "(",
                    "tknNorm_": "(",
                    "tknPos_": "PUNCT",
                    "tknTag_": "-LRB-",
                    "tknText": "(",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 157,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "a",
                    "tknNorm_": "a",
                    "tknPos_": "X",
                    "tknTag_": "LS",
                    "tknText": "a",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 158,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ")",
                    "tknNorm_": ")",
                    "tknPos_": "PUNCT",
                    "tknTag_": "-RRB-",
                    "tknText": ")",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 159,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "copyright",
                    "tknNorm_": "copyright",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "Copyright",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 160,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "grant-",
                    "tknNorm_": "grant-",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "Grant-",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 161,
                    "tknIsOov": True,
                    "tknIsTitle": True,
                    "tknLemma_": "subject",
                    "tknNorm_": "subject",
                    "tknPos_": "ADJ",
                    "tknTag_": "JJ",
                    "tknText": "Subject",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 162,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "to",
                    "tknNorm_": "to",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "to",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 163,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "the",
                    "tknNorm_": "the",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "the",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 164,
                    "tknIsOov": True,
                    "tknLemma_": "term",
                    "tknNorm_": "terms",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "terms",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 165,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "of",
                    "tknNorm_": "of",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "of",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 166,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "this",
                    "tknNorm_": "this",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "this",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 167,
                    "tknIsOov": True,
                    "tknLemma_": "license",
                    "tknNorm_": "license",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "license",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 168,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": ",",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 169,
                    "tknIsOov": True,
                    "tknLemma_": "include",
                    "tknNorm_": "including",
                    "tknPos_": "VERB",
                    "tknTag_": "VBG",
                    "tknText": "including",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 170,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "the",
                    "tknNorm_": "the",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "the",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 171,
                    "tknIsOov": True,
                    "tknLemma_": "license",
                    "tknNorm_": "license",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "license",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 172,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 173,
                    "tknIsOov": True,
                    "tknLemma_": "condition",
                    "tknNorm_": "conditions",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "conditions",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 174,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "and",
                    "tknNorm_": "and",
                    "tknPos_": "CCONJ",
                    "tknTag_": "CC",
                    "tknText": "and",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 175,
                    "tknIsOov": True,
                    "tknLemma_": "limitation",
                    "tknNorm_": "limitations",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "limitations",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 176,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "in",
                    "tknNorm_": "in",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "in",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "B",
                    "tknEntType_": "LAW",
                    "tknI": 177,
                    "tknIsOov": True,
                    "tknLemma_": "section",
                    "tknNorm_": "section",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "section",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "I",
                    "tknEntType_": "LAW",
                    "tknI": 178,
                    "tknIsDigit": True,
                    "tknIsOov": True,
                    "tknLemma_": "3",
                    "tknLikeNum": True,
                    "tknNorm_": "3",
                    "tknPos_": "NUM",
                    "tknTag_": "CD",
                    "tknText": "3",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 179,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": ",",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 180,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "each",
                    "tknNorm_": "each",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "each",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 181,
                    "tknIsOov": True,
                    "tknLemma_": "contributor",
                    "tknNorm_": "contributor",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "contributor",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 182,
                    "tknIsOov": True,
                    "tknLemma_": "grant",
                    "tknNorm_": "grants",
                    "tknPos_": "VERB",
                    "tknTag_": "VBZ",
                    "tknText": "grants",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 183,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "you",
                    "tknNorm_": "you",
                    "tknPos_": "PRON",
                    "tknTag_": "PRP",
                    "tknText": "you",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 184,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "a",
                    "tknNorm_": "a",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "a",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 185,
                    "tknIsOov": True,
                    "tknLemma_": "nonexclusive",
                    "tknNorm_": "nonexclusive",
                    "tknPos_": "ADJ",
                    "tknTag_": "JJ",
                    "tknText": "nonexclusive",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 186,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": ",",
                    "tknText": ",",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 187,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 188,
                    "tknIsOov": True,
                    "tknLemma_": "worldwide",
                    "tknNorm_": "worldwide",
                    "tknPos_": "ADJ",
                    "tknTag_": "JJ",
                    "tknText": "worldwide",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 189,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": ",",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 190,
                    "tknIsOov": True,
                    "tknLemma_": "royalty",
                    "tknNorm_": "royalty",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "royalty",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 191,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": "-",
                    "tknNorm_": "-",
                    "tknPos_": "PUNCT",
                    "tknTag_": "HYPH",
                    "tknText": "-",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 192,
                    "tknIsOov": True,
                    "tknLemma_": "free",
                    "tknNorm_": "free",
                    "tknPos_": "ADJ",
                    "tknTag_": "JJ",
                    "tknText": "free",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 193,
                    "tknIsOov": True,
                    "tknLemma_": "copyright",
                    "tknNorm_": "copyright",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "copyright",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 194,
                    "tknIsOov": True,
                    "tknLemma_": "license",
                    "tknNorm_": "license",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "license",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 195,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "to",
                    "tknNorm_": "to",
                    "tknPos_": "PART",
                    "tknTag_": "TO",
                    "tknText": "to",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 196,
                    "tknIsOov": True,
                    "tknLemma_": "reproduce",
                    "tknNorm_": "reproduce",
                    "tknPos_": "VERB",
                    "tknTag_": "VB",
                    "tknText": "reproduce",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 197,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "its",
                    "tknNorm_": "its",
                    "tknPos_": "PRON",
                    "tknTag_": "PRP$",
                    "tknText": "its",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 198,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 199,
                    "tknIsOov": True,
                    "tknLemma_": "contribution",
                    "tknNorm_": "contribution",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "contribution",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 200,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": ",",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 201,
                    "tknIsOov": True,
                    "tknLemma_": "prepare",
                    "tknNorm_": "prepare",
                    "tknPos_": "VERB",
                    "tknTag_": "VB",
                    "tknText": "prepare",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 202,
                    "tknIsOov": True,
                    "tknLemma_": "derivative",
                    "tknNorm_": "derivative",
                    "tknPos_": "ADJ",
                    "tknTag_": "JJ",
                    "tknText": "derivative",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 203,
                    "tknIsOov": True,
                    "tknLemma_": "work",
                    "tknNorm_": "works",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "works",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 204,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "of",
                    "tknNorm_": "of",
                    "tknPos_": "ADP",
                    "tknTag_": "IN",
                    "tknText": "of",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 205,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "its",
                    "tknNorm_": "its",
                    "tknPos_": "PRON",
                    "tknTag_": "PRP$",
                    "tknText": "its",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 206,
                    "tknIsOov": True,
                    "tknLemma_": "contribution",
                    "tknNorm_": "contribution",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "contribution",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 207,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknLemma_": ",",
                    "tknNorm_": ",",
                    "tknPos_": "PUNCT",
                    "tknTag_": ",",
                    "tknText": ",",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 208,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "and",
                    "tknNorm_": "and",
                    "tknPos_": "CCONJ",
                    "tknTag_": "CC",
                    "tknText": "and",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 209,
                    "tknIsOov": True,
                    "tknLemma_": "distribute",
                    "tknNorm_": "distribute",
                    "tknPos_": "VERB",
                    "tknTag_": "VB",
                    "tknText": "distribute",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 210,
                    "tknIsOov": True,
                    "tknLemma_": "\n",
                    "tknNorm_": "\n",
                    "tknPos_": "SPACE",
                    "tknTag_": "_SP",
                    "tknText": "\n",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 211,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "its",
                    "tknNorm_": "its",
                    "tknPos_": "PRON",
                    "tknTag_": "PRP$",
                    "tknText": "its",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 212,
                    "tknIsOov": True,
                    "tknLemma_": "contribution",
                    "tknNorm_": "contribution",
                    "tknPos_": "NOUN",
                    "tknTag_": "NN",
                    "tknText": "contribution",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 213,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "or",
                    "tknNorm_": "or",
                    "tknPos_": "CCONJ",
                    "tknTag_": "CC",
                    "tknText": "or",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 214,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "any",
                    "tknNorm_": "any",
                    "tknPos_": "DET",
                    "tknTag_": "DT",
                    "tknText": "any",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 215,
                    "tknIsOov": True,
                    "tknLemma_": "derivative",
                    "tknNorm_": "derivative",
                    "tknPos_": "ADJ",
                    "tknTag_": "JJ",
                    "tknText": "derivative",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 216,
                    "tknIsOov": True,
                    "tknLemma_": "work",
                    "tknNorm_": "works",
                    "tknPos_": "NOUN",
                    "tknTag_": "NNS",
                    "tknText": "works",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 217,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "that",
                    "tknNorm_": "that",
                    "tknPos_": "PRON",
                    "tknTag_": "WDT",
                    "tknText": "that",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 218,
                    "tknIsOov": True,
                    "tknIsStop": True,
                    "tknLemma_": "you",
                    "tknNorm_": "you",
                    "tknPos_": "PRON",
                    "tknTag_": "PRP",
                    "tknText": "you",
                    "tknWhitespace_": " ",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 219,
                    "tknIsOov": True,
                    "tknLemma_": "create",
                    "tknNorm_": "create",
                    "tknPos_": "VERB",
                    "tknTag_": "VBP",
                    "tknText": "create",
                },
                {
                    "tknEntIob_": "O",
                    "tknI": 220,
                    "tknIsOov": True,
                    "tknIsPunct": True,
                    "tknIsSentEnd": True,
                    "tknLemma_": ".",
                    "tknNorm_": ".",
                    "tknPos_": "PUNCT",
                    "tknTag_": ".",
                    "tknText": ".",
                },
            ],
        },
        1,
    ]

    cfg.glob.token = db.cls_token.Token.from_id(expected_values[0])

    actual_values = cfg.glob.token.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print(f"issue with dbt token cfg.glob.token id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt token id={expected_values[0]} - see above"

    cfg.glob.token.exists()


# -----------------------------------------------------------------------------
# Check existing version object.
# -----------------------------------------------------------------------------
def check_existing_version():
    """Check existing version object."""
    expected_values = [1, cfg.glob.setup.dcr_version]

    cfg.glob.version = db.cls_version.Version.from_id(expected_values[0])

    actual_values = cfg.glob.version.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print(f"issue with dbt version cfg.glob.version id={expected_values[0]}:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, f"issue with dbt version id={expected_values[0]} - see above"

    cfg.glob.version.exists()


# -----------------------------------------------------------------------------
# Check missing action object.
# -----------------------------------------------------------------------------
def check_missing_action():
    """Check missing action object."""
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_action.Action.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt action instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt action instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing document object.
# -----------------------------------------------------------------------------
def check_missing_document():
    """Check missing document object."""
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_document.Document.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt document instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt document instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing language object.
# -----------------------------------------------------------------------------
def check_missing_language():
    """Check missing language object."""
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_language.Language.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt language instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt language instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing run object.
# -----------------------------------------------------------------------------
def check_missing_run():
    """Check missing run object."""
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_run.Run.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt run instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt run instance id={MISSING_ID}"

    # -----------------------------------------------------------------------------
    # Invalid action code.
    # -----------------------------------------------------------------------------
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_run.Run(
            _row_id=0,
            action_code=cfg.glob.INFORMATION_NOT_YET_AVAILABLE,
            total_erroneous=1,
        )

    assert expt.type == SystemExit, f"invalid action code={cfg.glob.INFORMATION_NOT_YET_AVAILABLE}"
    assert expt.value.code == 1, f"invalid action code={cfg.glob.INFORMATION_NOT_YET_AVAILABLE}"

    # -----------------------------------------------------------------------------
    # Untested action codes.
    # -----------------------------------------------------------------------------
    db.driver.connect_db()

    db.cls_run.Run(
        action_code=db.cls_run.Run.ACTION_CODE_PARSER_PAGE,
    )

    db.cls_run.Run(
        action_code=db.cls_run.Run.ACTION_CODE_PARSER_WORD,
    )

    db.cls_run.Run(
        action_code=db.cls_run.Run.ACTION_CODE_TOKENIZE_LINE,
    )


# -----------------------------------------------------------------------------
# Check missing token object.
# -----------------------------------------------------------------------------
def check_missing_token():
    """Check missing token object."""
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_token.Token.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt token instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt token instance id={MISSING_ID}"


# -----------------------------------------------------------------------------
# Check missing version object.
# -----------------------------------------------------------------------------
def check_missing_version():
    """Check missing version object."""
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.from_id(MISSING_ID)

    assert expt.type == SystemExit, f"issue with missing dbt version instance id={MISSING_ID}"
    assert expt.value.code == 1, f"issue with missing dbt version instance id={MISSING_ID}"

    # -----------------------------------------------------------------------------
    # Column version in database table version not found.
    # -----------------------------------------------------------------------------
    db.driver.connect_db()

    db.dml.delete_dbt_id(
        table_name=cfg.glob.DBT_VERSION,
        id_where=1,
    )

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    assert expt.type == SystemExit, "issue column version in database table version not found"
    assert expt.value.code == 1, "issue column version in database table version not found"

    # -----------------------------------------------------------------------------
    # Column version in database table version not unique.
    # -----------------------------------------------------------------------------
    db.driver.connect_db()

    cfg.glob.version = db.cls_version.Version(
        version="1",
    )

    cfg.glob.version.persist_2_db()

    cfg.glob.version = db.cls_version.Version(
        version="2",
    )

    cfg.glob.version.persist_2_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    assert expt.type == SystemExit, "issue column version in database table version not unique"
    assert expt.value.code == 1, "issue column version in database table version not unique"


# -----------------------------------------------------------------------------
# Check new action object.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def check_new_action():
    """Check new action object."""

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_action()

    cfg.glob.action_curr = db.cls_action.Action.from_id(expected_values[0])

    actual_values = cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != tuple(expected_values):
        print("issue with new dbt action instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt action instance - see above"

    cfg.glob.action_curr = db.cls_action.Action(
        action_code=expected_values[1],
        action_text=expected_values[2],
        directory_name=expected_values[3],
        directory_type=expected_values[4],
        file_name=expected_values[8],
        file_size_bytes=0,
        id_document=expected_values[10],
        id_parent=expected_values[11],
        id_run_last=expected_values[12],
        no_children=expected_values[13],
        no_pdf_pages=0,
        status=expected_values[15],
    )

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    cfg.glob.action_curr = db.cls_action.Action.from_id(expected_values[0])

    expected_values[15] = db.cls_document.Document.DOCUMENT_STATUS_END

    cfg.glob.action_curr.action_status = expected_values[15]

    cfg.glob.action_curr.persist_2_db()

    actual_values = cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False)

    if actual_values != tuple(expected_values):
        print("issue with updated dbt action instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt action instance - see above"

    # -----------------------------------------------------------------------------
    # coverage.
    # -----------------------------------------------------------------------------
    expected_values[0] = 5
    expected_values[1] = "s_p_j_line"
    expected_values[2] = "parser_line   (nlp)"

    instance = db.cls_action.Action(
        _row_id=0,
        action_code=expected_values[1],
        action_text=expected_values[2],
        directory_name=expected_values[3],
        directory_type=expected_values[4],
        file_name=expected_values[8],
        file_size_bytes=expected_values[9],
        id_document=expected_values[10],
        id_parent=expected_values[11],
        id_run_last=expected_values[12],
        no_children=expected_values[13],
        no_pdf_pages=expected_values[14],
        status=expected_values[15],
    )

    instance.action_file_size_bytes = 0
    instance.action_no_pdf_pages = 0

    instance.finalise()

    instance.finalise_error("error_code", "error_msg")


# -----------------------------------------------------------------------------
# Check new document object.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def check_new_document():
    """Check new document object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_document()

    cfg.glob.document = db.cls_document.Document.from_id(expected_values[0])

    actual_values = cfg.glob.document.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print("issue with new dbt document cfg.glob.document:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt document cfg.glob.document - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[13] = db.cls_document.Document.DOCUMENT_STATUS_END

    cfg.glob.document.document_status = expected_values[13]

    cfg.glob.document.finalise()

    actual_values = cfg.glob.document.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print("issue with updated dbt document cfg.glob.document:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt document cfg.glob.document - see above"


# -----------------------------------------------------------------------------
# Check new language object.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def check_new_language():
    """Check new language object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_language()

    cfg.glob.language = db.cls_language.Language.from_id(expected_values[0])

    actual_values = cfg.glob.language.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print("issue with new dbt language instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt language instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[6] = ""

    cfg.glob.language.language_directory_name_inbox = expected_values[6]

    cfg.glob.language.persist_2_db()

    actual_values = cfg.glob.language.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print("issue with updated dbt language instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt language instance - see above"


# -----------------------------------------------------------------------------
# Check new run object.
# -----------------------------------------------------------------------------
# noinspection PyArgumentList
def check_new_run():
    """Check new run object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_run()

    cfg.glob.run = db.cls_run.Run.from_id(expected_values[0])

    actual_values = cfg.glob.run.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print("issue with new dbt run instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt run instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[4] = db.cls_document.Document.DOCUMENT_STATUS_END

    cfg.glob.run.run_status = expected_values[4]

    cfg.glob.run.persist_2_db()

    actual_values = cfg.glob.run.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print("issue with updated dbt run instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt run instance - see above"

    # -----------------------------------------------------------------------------
    # Delete object.
    # -----------------------------------------------------------------------------
    db.cls_run.Run.ID_RUN_UMBRELLA = 0

    db.cls_run.Run(
        _row_id=0,
        action_code=expected_values[1],
        status=expected_values[4],
        total_erroneous=0,
    )

    cfg.glob.run.persist_2_db()


# -----------------------------------------------------------------------------
# Check new token object.
# -----------------------------------------------------------------------------
def check_new_token():
    """Check new token object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_token()

    cfg.glob.token = db.cls_token.Token.from_id(expected_values[0])

    actual_values = cfg.glob.token.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print("issue with new dbt token instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt token instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[3] = 2

    cfg.glob.token.token_page_no = expected_values[3]

    cfg.glob.token.persist_2_db()

    actual_values = cfg.glob.token.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print("issue with updated dbt token instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt token instance - see above"

    cfg.glob.token.finalise()


# -----------------------------------------------------------------------------
# Check new version object.
# -----------------------------------------------------------------------------
def check_new_version():
    """Check new version object."""
    # -----------------------------------------------------------------------------
    # Insert object.
    # -----------------------------------------------------------------------------
    expected_values = pytest.helpers.create_version()

    cfg.glob.version = db.cls_version.Version.from_id(expected_values[0])

    actual_values = cfg.glob.version.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print("issue with new dbt version instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with new dbt version instance - see above"

    # -----------------------------------------------------------------------------
    # Update object.
    # -----------------------------------------------------------------------------
    expected_values[1] = ""

    cfg.glob.version.version_version = expected_values[1]

    cfg.glob.version.finalise()

    actual_values = cfg.glob.version.get_columns_in_tuple()

    if actual_values != tuple(expected_values):
        print("issue with updated dbt version instance:")
        print(f"values expected={expected_values}")
        print(f"values actual  ={actual_values}")
        assert False, "issue with updated dbt version instance - see above"


# -----------------------------------------------------------------------------
# Test Function - existing objects.
# -----------------------------------------------------------------------------
def test_existing_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - existing objects."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    db.cls_run.Run.ID_RUN_UMBRELLA = 0

    dcr.main([dcr.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_ALL_COMPLETE])

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    check_existing_language()
    check_existing_run()
    check_existing_version()

    check_existing_document()

    check_existing_action()

    check_existing_token()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - action - case 1.
# -----------------------------------------------------------------------------
def test_missing_dependencies_action_1(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - action - case 1."""
    try:
        cfg.glob.run.exists()  # type: ignore

        del cfg.glob.run

        cfg.glob.logger.debug("The existing object 'cfg.glob.run' of the class Run was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    directory_name = cfg.glob.setup.directory_inbox
    file_name = "pdf_text_ok.pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    values_run = pytest.helpers.create_run()

    values_document = pytest.helpers.create_document()

    with pytest.raises(SystemExit) as expt:
        db.cls_action.Action(
            action_code=db.cls_run.Run.ACTION_CODE_INBOX,
            directory_name=directory_name,
            file_name=file_name,
            id_document=values_document[0],
            id_run_last=values_run[0],
        )

    assert expt.type == SystemExit, "Class Action requires class Run"
    assert expt.value.code == 1, "Class Action requires class Run"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - action - case 2.
# -----------------------------------------------------------------------------
def test_missing_dependencies_action_2(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing dependencies - action - case 2."""
    try:
        cfg.glob.action_curr.exists()  # type: ignore

        del cfg.glob.action_curr

        cfg.glob.logger.debug("The existing object 'cfg.glob.action_curr' of the class Action was deleted.")
    except AttributeError:
        pass

    try:
        cfg.glob.document.exists()  # type: ignore

        del cfg.glob.document

        cfg.glob.logger.debug("The existing object 'cfg.glob.document' of the class Document was deleted.")
    except AttributeError:
        pass

    try:
        cfg.glob.run.exists()  # type: ignore

        del cfg.glob.run

        cfg.glob.logger.debug("The existing object 'cfg.glob.run' of the class Run was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    cfg.glob.start_time_document = time.perf_counter_ns()

    directory_name = cfg.glob.setup.directory_inbox
    file_name = "pdf_text_ok.pdf"

    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_text_ok", "pdf"),
        ],
        target_path=directory_name,
    )

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    values_run = pytest.helpers.create_run()

    cfg.glob.run = db.cls_run.Run.from_id(values_run[0])

    # -----------------------------------------------------------------------------
    cfg.glob.language = db.cls_language.Language.from_id(1)

    cfg.glob.language.persist_2_db()

    # -------------------------------------------------------------------------
    # _expected_values_document = pytest.helpers.create_document()
    values_document = pytest.helpers.create_document()

    # -------------------------------------------------------------------------
    local_action = db.cls_action.Action(
        action_code="p_i",
        directory_name=directory_name,
        file_name=file_name,
        id_document=values_document[0],
        id_run_last=values_run[0],
    )

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        local_action.finalise()

    assert expt.type == SystemExit, "Class Action requires class Document (finalise)"
    assert expt.value.code == 1, "Class Action requires class Document (finalise)"

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        local_action.finalise_error("error_code", "error_msg")

    assert expt.type == SystemExit, "Class Action requires class Document (finalise_error)"
    assert expt.value.code == 1, "Class Action requires class Document (finalise_error)"

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    cfg.glob.document = db.cls_document.Document.from_id(1)

    local_action.action_action_code = db.cls_run.Run.ACTION_CODE_PDF2IMAGE

    with pytest.raises(SystemExit) as expt:
        local_action.finalise_error("error_code", "error_msg")

    assert expt.type == SystemExit, "Class Action requires class Action (finalise_error)"
    assert expt.value.code == 1, "Class Action requires class Action (finalise_error)"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - language.
# -----------------------------------------------------------------------------
def test_missing_dependencies_language(fxtr_setup_logger):
    """# Test Function - missing dependencies - language.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    try:
        cfg.glob.setup.exists()  # type: ignore

        del cfg.glob.setup

        cfg.glob.logger.debug("The existing object 'cfg.glob.setup' of the class Setup was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        db.cls_language.Language(
            active=True,
            code_iso_639_3="",
            code_pandoc="",
            code_spacy="",
            code_tesseract="",
            iso_language_name="",
        )

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing objects.
# -----------------------------------------------------------------------------
def test_missing_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - missing objects."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    check_missing_language()
    check_missing_run()
    check_missing_version()

    check_missing_document()

    check_missing_action()

    check_missing_token()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - new objects.
# -----------------------------------------------------------------------------
def test_new_objects(fxtr_setup_empty_db_and_inbox):
    """Test Function - new objects."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    cfg.glob.start_time_document = time.perf_counter_ns()

    db.cls_run.Run.ID_RUN_UMBRELLA = 0

    check_new_language()
    check_new_run()
    check_new_version()

    check_new_document()

    check_new_action()

    cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=True, is_file_size_bytes=True)
    cfg.glob.action_curr.get_columns_in_tuple(is_duration_ns=False, is_file_size_bytes=False)

    check_new_token()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique_driver(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    db.dml.insert_dbt_row(cfg.glob.DBT_VERSION, {cfg.glob.DBC_VERSION: "0.0.0"})

    db.driver.disconnect_db()

    db.driver.connect_db()

    cfg.glob.db_driver_cur = cfg.glob.db_driver_conn.cursor()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (driver)"
    assert expt.value.code == 1, "Version not unique (driver)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    db.driver.connect_db()

    cfg.glob.db_driver_cur = cfg.glob.db_driver_conn.cursor()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version missing (driver)"
    assert expt.value.code == 1, "Version missing (driver)"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - select_version_version_unique().
# -----------------------------------------------------------------------------
def test_select_version_version_unique_orm(fxtr_setup_empty_db_and_inbox):
    """Test: select_version_version_unique()."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    db.dml.insert_dbt_row(cfg.glob.DBT_VERSION, {cfg.glob.DBC_VERSION: "0.0.0"})

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version not unique (orm)"
    assert expt.value.code == 1, "Version not unique (orm)"

    # -------------------------------------------------------------------------
    pytest.helpers.delete_version_version()

    db.driver.connect_db()

    with pytest.raises(SystemExit) as expt:
        db.cls_version.Version.select_version_version_unique()

    db.driver.disconnect_db()

    assert expt.type == SystemExit, "Version missing (orm)"
    assert expt.value.code == 1, "Version missing (orm)"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
