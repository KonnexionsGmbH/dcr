# pylint: disable=unused-argument
"""Testing Module nlp.cls_..."""
import os.path
from typing import List
from typing import Tuple

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_run
import db.driver
import defusedxml.ElementTree
import nlp.cls_line_type
import nlp.cls_text_parser
import pytest

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# pylint: disable=W0212
# @pytest.mark.issue
import utils

import dcr

XML_DATA: str = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Created by the PDFlib Text and Image Extraction Toolkit TET (www.pdflib.com) -->
<TET xmlns="http://www.pdflib.com/XML/TET5/TET-5.0"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.pdflib.com/XML/TET5/TET-5.0
 http://www.pdflib.com/XML/TET5/TET-5.0.xsd"
 version="5.2">
<Creation platform="Win64" tetVersion="5.3" date="2022-05-23T12:57:11+02:00" />
<Document filename="data\\inbox_dev_accepted\\pdf_single_word_1.pdf"
          pageCount="1" filesize="7301" linearized="true" pdfVersion="1.5" tagged="true">
<DocInfo>
<Author>Walter Weinmann</Author>
<CreationDate>2022-05-23T12:47:03+02:00</CreationDate>
<Creator>Acrobat PDFMaker 11 for Word</Creator>
<ModDate>2022-05-23T12:47:04+02:00</ModDate>
<Producer>Adobe PDF Library 11.0</Producer>
<Custom key="SourceModified">D:20220523104654</Custom>
</DocInfo>
<Metadata>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 5.4-c006 80.159825, 2016/09/16-03:31:08        ">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about=""
            xmlns:xmp="http://ns.adobe.com/xap/1.0/"
            xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:pdf="http://ns.adobe.com/pdf/1.3/"
            xmlns:pdfx="http://ns.adobe.com/pdfx/1.3/">
         <xmp:ModifyDate>2022-05-23T12:47:04+02:00</xmp:ModifyDate>
         <xmp:CreateDate>2022-05-23T12:47:03+02:00</xmp:CreateDate>
         <xmp:MetadataDate>2022-05-23T12:47:04+02:00</xmp:MetadataDate>
         <xmp:CreatorTool>Acrobat PDFMaker 11 for Word</xmp:CreatorTool>
         <xmpMM:DocumentID>uuid:e39ca48d-d9cf-4999-97da-e7b74e33c740</xmpMM:DocumentID>
         <xmpMM:InstanceID>uuid:450f14ac-790b-4d9f-8501-2bcfae7ac17c</xmpMM:InstanceID>
         <xmpMM:subject>
            <rdf:Seq>
               <rdf:li>2</rdf:li>
            </rdf:Seq>
         </xmpMM:subject>
         <dc:format>application/pdf</dc:format>
         <dc:title>
            <rdf:Alt>
               <rdf:li xml:lang="x-default"/>
            </rdf:Alt>
         </dc:title>
         <dc:description>
            <rdf:Alt>
               <rdf:li xml:lang="x-default"/>
            </rdf:Alt>
         </dc:description>
         <dc:creator>
            <rdf:Seq>
               <rdf:li>Walter Weinmann</rdf:li>
            </rdf:Seq>
         </dc:creator>
         <pdf:Producer>Adobe PDF Library 11.0</pdf:Producer>
         <pdf:Keywords/>
         <pdfx:SourceModified>D:20220523104654</pdfx:SourceModified>
         <pdfx:Company/>
         <pdfx:Comments/>
      </rdf:Description>
   </rdf:RDF>
</x:xmpmeta>
</Metadata>
<Options>tetml={filename={data\\inbox_dev_accepted\\pdf_single_word_1.line.xml}}
         engines={noannotation noimage text notextcolor novector}</Options>
<Pages>
<Page number="1" width="595.32" height="841.92">
<Options>granularity=line</Options>
<Content granularity="line" dehyphenation="false" dropcap="false" font="false"
         geometry="false" shadow="false" sub="false" sup="false">
<Para>
 <Box llx="70.80" lly="756.12" urx="205.04" ury="772.08">
  <Line llx="70.80" lly="756.12" urx="205.04" ury="772.08">
   <Text>Konnexions GmbH</Text>
  </Line>
 </Box>
</Para>
</Content>
</Page>
<Resources>
<Fonts>
 <Font id="F0" name="ArialMT" type="TrueType" embedded="false" ascender="1040.00"
       capheight="716.00" italicangle="0.00" descender="-325.00" weight="400.00" xheight="519.00"/>
 <Font id="F1" name="CourierNewPSMT" type="TrueType" embedded="false" ascender="1021.00"
       capheight="571.00" italicangle="0.00" descender="-680.00" weight="400.00" xheight="423.00"/>
</Fonts>
<ColorSpaces>
 <ColorSpace id="CS0" name="ICCBased" components="1" iccprofile="ICC0"/>
</ColorSpaces>
</Resources>
<Graphics>
<ICCProfiles>
 <ICCProfile id="ICC0" embedded="true" iccversion="2.1" profilename="Gray Gamma 2.2"
             checksum="66043AD0DE86F27B977BAB702FB1A778" profilecs="GRAY" deviceclass="mntr"
             fromCIE="true" toCIE="true"/>
</ICCProfiles>
</Graphics>
</Pages>
</Document>
</TET>"""


# -----------------------------------------------------------------------------
# Test LineType.
# -----------------------------------------------------------------------------
def check_cls_line_type(
    json_file: str, target_footer: List[Tuple[int, List[int]]], target_header: List[Tuple[int, List[int]]]
) -> None:
    """Test LineType.

    Args:
        json_file (str): JSON file from trxt parser.
        target_footer (List[Tuple[int, List[int]]]): Target footer lines.
        target_header (List[Tuple[int, List[int]]]): Target header lines.
    """
    instance = nlp.cls_text_parser.TextParser.from_files(full_name_line=json_file)

    actual_footer = []
    actual_header = []

    pages = instance.parse_result_line_4_document[nlp.cls_text_parser.TextParser.JSON_NAME_PAGES]

    for page in pages:
        page_no = page[nlp.cls_text_parser.TextParser.JSON_NAME_PAGE_NO]

        actual_page_footer = []
        actual_page_header = []

        for line in page[nlp.cls_text_parser.TextParser.JSON_NAME_LINES]:
            line_type = line[nlp.cls_text_parser.TextParser.JSON_NAME_LINE_TYPE]
            if line_type == cfg.glob.DOCUMENT_LINE_TYPE_FOOTER:
                actual_page_footer.append(line[nlp.cls_text_parser.TextParser.JSON_NAME_LINE_INDEX_PAGE])
            elif line_type == cfg.glob.DOCUMENT_LINE_TYPE_HEADER:
                actual_page_header.append(line[nlp.cls_text_parser.TextParser.JSON_NAME_LINE_INDEX_PAGE])

        if actual_page_footer:
            actual_footer.append((page_no, actual_page_footer))

        if actual_page_header:
            actual_header.append((page_no, actual_page_header))

    assert (
        actual_header == target_header
    ), f"file={json_file} header difference: \ntarget={target_header} \nactual={actual_header}"
    assert (
        actual_footer == target_footer
    ), f"file={json_file} footer difference: \ntarget={target_footer} \nactual={actual_footer}"


# -----------------------------------------------------------------------------
# Test LineType.
# -----------------------------------------------------------------------------
def test_cls_line_type(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test LineType."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("p_1_h_0_f_0", "pdf"),
            ("p_2_h_0_f_0", "pdf"),
            ("p_2_h_0_f_2", "pdf"),
            ("p_2_h_1_f_0", "pdf"),
            ("p_2_h_1_f_1", "pdf"),
            ("p_2_h_2_f_0", "pdf"),
            ("p_2_h_2_f_2", "pdf"),
            ("p_3_h_0_f_4", "pdf"),
            ("p_3_h_2_f_2", "pdf"),
            ("p_3_h_3_f_3", "pdf"),
            ("p_3_h_4_f_0", "pdf"),
            ("p_3_h_4_f_4", "pdf"),
            ("p_4_h_4_f_4_different_first", "pdf"),
            ("p_4_h_4_f_4_different_last", "pdf"),
            ("p_4_h_4_f_4_empty_first", "pdf"),
            ("p_4_h_4_f_4_empty_last", "pdf"),
            ("p_5_h_0_f_0", "pdf"),
            ("p_5_h_0_f_2", "pdf"),
            ("p_5_h_2_f_0", "pdf"),
            ("p_5_h_2_f_2", "pdf"),
            ("p_5_h_4_f_4_different_both", "pdf"),
            ("p_5_h_4_f_4_empty_both", "pdf"),
            ("p_5_h_4_f_4_empty_center", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_DELETE_AUXILIARY_FILES, "true"),
            (cfg.glob.setup._DCR_CFG_LINE_FOOTER_MAX_LINES, "3"),
            (cfg.glob.setup._DCR_CFG_LINE_HEADER_MAX_LINES, "3"),
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "false"),
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "false"),
            (cfg.glob.setup._DCR_CFG_VERBOSE_LINE_TYPE, "false"),
            (cfg.glob.setup._DCR_CFG_VERBOSE_PARSER, "false"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_1_h_0_f_0_1.line.json")),
        target_footer=[],
        target_header=[],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_0_f_0_2.line.json")),
        target_footer=[],
        target_header=[],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_0_f_2_3.line.json")),
        target_footer=[(1, [0, 1]), (2, [0, 1])],
        target_header=[],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_1_f_0_4.line.json")),
        target_footer=[],
        target_header=[(1, [0]), (2, [0])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_1_f_1_5.line.json")),
        target_footer=[(1, [4]), (2, [4])],
        target_header=[(1, [0]), (2, [0])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_2_f_0_6.line.json")),
        target_footer=[(1, [0, 1]), (2, [0, 1])],
        target_header=[],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_2_h_2_f_2_7.line.json")),
        target_footer=[(1, [1, 2, 3]), (2, [1, 2, 3])],
        target_header=[(1, [0]), (2, [0])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_3_h_0_f_4_8.line.json")),
        target_footer=[(1, [4, 5, 6]), (2, [4, 5, 6]), (3, [4, 5, 6])],
        target_header=[],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_3_h_2_f_2_9.line.json")),
        target_footer=[(1, [5, 6]), (2, [5, 6]), (3, [5, 6])],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_3_h_3_f_3_10.line.json")),
        target_footer=[(1, [6, 7, 8]), (2, [6, 7, 8]), (3, [6, 7, 8])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_3_h_4_f_0_11.line.json")),
        target_footer=[],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_3_h_4_f_4_12.line.json")),
        target_footer=[(1, [8, 9, 10]), (2, [8, 9, 10]), (3, [8, 9, 10])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_different_first_13.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_different_last_14.line.json")),
        target_footer=[(1, [8, 9, 10]), (2, [8, 9, 10]), (3, [8, 9, 10])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_empty_first_15.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_4_h_4_f_4_empty_last_16.line.json")),
        target_footer=[(1, [8, 9, 10]), (2, [8, 9, 10]), (3, [8, 9, 10])],
        target_header=[(1, [0, 1, 2]), (2, [0, 1, 2]), (3, [0, 1, 2])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_0_f_0_17.line.json")),
        target_footer=[],
        target_header=[],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_0_f_2_18.line.json")),
        target_footer=[(1, [5, 6]), (2, [5, 6]), (3, [5, 6]), (4, [3, 4]), (5, [5, 6])],
        target_header=[],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_2_f_0_19.line.json")),
        target_footer=[],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1]), (4, [0, 1]), (5, [0, 1])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_2_f_2_20.line.json")),
        target_footer=[(1, [5, 6]), (2, [5, 6]), (3, [5, 6]), (4, [5, 6]), (5, [5, 6])],
        target_header=[(1, [0, 1]), (2, [0, 1]), (3, [0, 1]), (4, [0, 1]), (5, [0, 1])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_4_f_4_different_both_21.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_4_f_4_empty_both_22.line.json")),
        target_footer=[(2, [8, 9, 10]), (3, [8, 9, 10]), (4, [8, 9, 10])],
        target_header=[(2, [0, 1, 2]), (3, [0, 1, 2]), (4, [0, 1, 2])],
    )
    check_cls_line_type(
        json_file=str(os.path.join(cfg.glob.setup.directory_inbox_accepted, "p_5_h_4_f_4_empty_center_23.line.json")),
        target_footer=[],
        target_header=[],
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test TextParser - .
# -----------------------------------------------------------------------------
def test_cls_text_parser(fxtr_rmdir_opt, fxtr_setup_empty_db_and_inbox):
    """Test TextParser."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    pytest.helpers.copy_files_4_pytest_2_dir(
        source_files=[
            ("pdf_mini", "pdf"),
        ],
        target_path=cfg.glob.setup.directory_inbox,
    )

    # -------------------------------------------------------------------------
    values_original = pytest.helpers.backup_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        [
            (cfg.glob.setup._DCR_CFG_TETML_PAGE, "true"),
            (cfg.glob.setup._DCR_CFG_TETML_WORD, "true"),
        ],
    )

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_INBOX])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PDFLIB])

    dcr.main([cfg.glob.DCR_ARGV_0, db.cls_run.Run.ACTION_CODE_PARSER])

    pytest.helpers.restore_config_params(
        cfg.glob.setup._DCR_CFG_SECTION_ENV_TEST,
        values_original,
    )

    # -------------------------------------------------------------------------
    nlp.cls_text_parser.TextParser.from_files(
        full_name_line=utils.get_full_name(cfg.glob.setup.directory_inbox_accepted, "pdf_mini_1.line.json"),
        full_name_page=utils.get_full_name(cfg.glob.setup.directory_inbox_accepted, "pdf_mini_1.page.json"),
        full_name_word=utils.get_full_name(cfg.glob.setup.directory_inbox_accepted, "pdf_mini_1.word.json"),
    )

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type - Action (action_curr).
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_action_curr(fxtr_setup_logger_environment):
    """# Test Function - missing dependencies - line_type - Action (action_curr).
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    try:
        cfg.glob.action_curr.exists()  # type: ignore

        del cfg.glob.action_curr

        cfg.glob.logger.debug("The existing object 'cfg.glob.action_curr' of the class Action was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        nlp.cls_line_type.LineType()

    assert expt.type == SystemExit, "Instance of class 'Action (action_curr)' is missing"
    assert expt.value.code == 1, "Instance of class 'Action (action_curr)' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type - coverage.
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_coverage(fxtr_setup_empty_db_and_inbox):
    """# Test Function - missing dependencies - line_type - coverage.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    # -------------------------------------------------------------------------
    cfg.glob.run = db.cls_run.Run(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    cfg.glob.action_curr = db.cls_action.Action(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    cfg.glob.text_parser = nlp.cls_text_parser.TextParser()

    cfg.glob.text_parser.exists()

    # -------------------------------------------------------------------------
    instance = nlp.cls_line_type.LineType()

    instance.exists()

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type - Setup.
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_setup(fxtr_setup_empty_db_and_inbox):
    """# Test Function - missing dependencies - line_type - Setup.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    # -------------------------------------------------------------------------
    cfg.glob.run = db.cls_run.Run(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    cfg.glob.action_curr = db.cls_action.Action(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    try:
        cfg.glob.setup.exists()  # type: ignore

        del cfg.glob.setup

        cfg.glob.logger.debug("The existing object 'cfg.glob.setup' of the class Setup was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        nlp.cls_line_type.LineType()

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - line_type - TextParser.
# -----------------------------------------------------------------------------
def test_missing_dependencies_line_type_text_parser(fxtr_setup_empty_db_and_inbox):
    """# Test Function - missing dependencies - line_type - TextParser.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    # -------------------------------------------------------------------------
    cfg.glob.run = db.cls_run.Run(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
    )

    # -------------------------------------------------------------------------
    cfg.glob.action_curr = db.cls_action.Action(
        _row_id=1,
        action_code=db.cls_run.Run.ACTION_CODE_INBOX,
        id_run_last=1,
    )

    # -------------------------------------------------------------------------
    try:
        cfg.glob.text_parser.exists()  # type: ignore

        del cfg.glob.text_parser

        cfg.glob.logger.debug("The existing object 'cfg.glob.text_parser' of the class TextParser was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    with pytest.raises(SystemExit) as expt:
        nlp.cls_line_type.LineType()

    assert expt.type == SystemExit, "Instance of class 'TextParser' is missing"
    assert expt.value.code == 1, "Instance of class 'TextParser' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - text_parser - Action (action_next).
# -----------------------------------------------------------------------------
def test_missing_dependencies_text_parser_action_next(fxtr_setup_logger_environment):
    """# Test Function - missing dependencies - text_parser - Action (action_next).
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    instance = nlp.cls_text_parser.TextParser()

    # -------------------------------------------------------------------------
    try:
        cfg.glob.action_next.exists()  # type: ignore

        del cfg.glob.action_next

        cfg.glob.logger.debug("The existing object 'cfg.glob.action_next' of the class Action was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    root = defusedxml.ElementTree.fromstring(XML_DATA)

    with pytest.raises(SystemExit) as expt:
        for child in root:
            child_tag = child.tag[nlp.cls_text_parser.TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case nlp.cls_text_parser.TextParser.PARSE_TAG_DOCUMENT:
                    instance.parse_tag_document(child_tag, child)
                case nlp.cls_text_parser.TextParser.PARSE_TAG_CREATION:
                    pass

    assert expt.type == SystemExit, "Instance of class 'Action (action_next)' is missing"
    assert expt.value.code == 1, "Instance of class 'Action (action_next)' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - text_parser - Document.
# -----------------------------------------------------------------------------
def test_missing_dependencies_text_parser_document(fxtr_setup_empty_db_and_inbox):
    """# Test Function - missing dependencies - text_parser - Document.
    ."""
    cfg.glob.logger.debug(cfg.glob.LOGGER_START)

    # -------------------------------------------------------------------------
    instance = nlp.cls_text_parser.TextParser()

    # -------------------------------------------------------------------------
    try:
        cfg.glob.document.exists()  # type: ignore

        del cfg.glob.document

        cfg.glob.logger.debug("The existing object 'cfg.glob.document' of the class Document was deleted.")
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    db.driver.connect_db()

    db.cls_run.Run.id_run_umbrella = -1

    cfg.glob.run = db.cls_run.Run(
        action_code=db.cls_run.Run.ACTION_CODE_TOKENIZE,
        id_run=-1,
    )

    cfg.glob.action_next = db.cls_action.Action(
        action_code=db.cls_run.Run.ACTION_CODE_TOKENIZE,
        id_run_last=-1,
        _row_id=-1,
    )

    # -------------------------------------------------------------------------
    root = defusedxml.ElementTree.fromstring(XML_DATA)

    with pytest.raises(SystemExit) as expt:
        for child in root:
            child_tag = child.tag[nlp.cls_text_parser.TextParser.PARSE_TAG_FROM :]
            match child_tag:
                case nlp.cls_text_parser.TextParser.PARSE_TAG_DOCUMENT:
                    instance.parse_tag_document(child_tag, child)
                case nlp.cls_text_parser.TextParser.PARSE_TAG_CREATION:
                    pass

    assert expt.type == SystemExit, "Instance of class 'Document' is missing"
    assert expt.value.code == 1, "Instance of class 'Document' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)


# -----------------------------------------------------------------------------
# Test Function - missing dependencies - text_parser - Setup.
# -----------------------------------------------------------------------------
def test_missing_dependencies_text_parser_setup(fxtr_setup_logger):
    """# Test Function - missing dependencies - text_parser - Setup.
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
        nlp.cls_text_parser.TextParser()

    assert expt.type == SystemExit, "Instance of class 'Setup' is missing"
    assert expt.value.code == 1, "Instance of class 'Setup' is missing"

    # -------------------------------------------------------------------------
    cfg.glob.logger.debug(cfg.glob.LOGGER_END)
