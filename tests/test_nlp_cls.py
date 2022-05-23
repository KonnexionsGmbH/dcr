# pylint: disable=unused-argument
"""Testing Module nlp.cls_..."""

import cfg.cls_setup
import cfg.glob
import db.cls_action
import db.cls_run
import db.driver
import defusedxml.ElementTree
import nlp.cls_text_parser
import pytest

# -----------------------------------------------------------------------------
# Constants & Globals.
# -----------------------------------------------------------------------------
# @pytest.mark.issue

XML_DATEN: str = """<?xml version="1.0" encoding="UTF-8"?>
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
    root = defusedxml.ElementTree.fromstring(XML_DATEN)

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
@pytest.mark.issue
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
    root = defusedxml.ElementTree.fromstring(XML_DATEN)

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
