# DCR - Document Content Recognition

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)

## 1. Introduction

Based on the paper "Unfolding the Structure of a Document using Deep Learning" (**[Rahman and Finin, 2019](https://arxiv.org/abs/1910.03678){:target="_blank"}**), this software project attempts to use various software techniques to automatically recognise the structure in any **`pdf`** documents and thus make them more searchable.

The processing logic is as follows:

- New documents are made available in the file directory **` inbox`**. If required, other language-related file directories can also be used (see section [Document Language](https://konnexionsgmbh.github.io/dcr/running_document_language){:target="_blank"}).
- Documents in a file format accepted by **DCR** are registered and moved to the file directory **`ìnbox_accepted`**. All other documents are registered and moved to the file directory **`ìnbox_rejected`**.
- Documents not in **`pdf`** format are converted to **`pdf`** format using [Pandoc](https://pandoc.org){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}. 
- Documents based on scanning which, therefore, do not contain text elements, are scanned and converted to **`pdf`** format using the [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} software. This process applies to all image format files e.g. **`jpeg`**, **`tiff`** etc., as well as scanned images in **`pdf`** format.  
- From all **`pdf`** documents, the text and associated metadata is extracted into a document-specific **`xml`** file using [PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"}.
- The document-specific **`xml`** files are then parsed and the **DCR**-relevant contents are written to the JSON files **`<document_name>>.line.json`**,  **`<document_name>>.page.json`**, or **`<document_name>>.word.json`**. 
- From the JSON file **`<document_name>>.line.json`** [spaCy](https://spacy.io){:target="_blank"} extracts qualified tokens and stores them in the database table **`content_token`**.

<div style="page-break-after: always;"></div>

### 1.1 Rahman & Finin Paper

![](img/index_rahman_finin.png)
### 1.2 Supported File Types

**DCR** can handle the following file types based on the file extension:

- **`bmp`** [bitmap image file](https://en.wikipedia.org/wiki/BMP_file_format){:target="_blank"}
- **`csv`** [comma-separated values](https://en.wikipedia.org/wiki/Comma-separated_values){:target="_blank"}
- **`docx`** [Office Open XML](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/){:target="_blank"}
- **`epub`** [e-book file format](https://www.w3.org/publishing/epub32/){:target="_blank"}
- **`gif`** [Graphics Interchange Format](https://www.w3.org/Graphics/GIF/spec-gif89a.txt){:target="_blank"}
- **`html`** [HyperText Markup Language](https://html.spec.whatwg.org){:target="_blank"}
- **`jp2`** [JPEG 2000](https://en.wikipedia.org/wiki/JPEG_2000){:target="_blank"}
- **`jpeg`** [Joint Photographic Experts Group](https://jpeg.org/jpeg/){:target="_blank"}
- **`odt`** [Open Document Format for Office Applications](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=office){:target="_blank"}
- **`pdf`** [Portable Document Format](https://www.iso.org/standard/75839.html){:target="_blank"}
- **`png`** [Portable Network Graphics](https://en.wikipedia.org/wiki/Portable_Network_Graphics){:target="_blank"}
- **`pnm`** [portable anymap format](https://en.wikipedia.org/wiki/Netpbm#File_formats){:target="_blank"}
- **`rst`** [reStructuredText (RST](https://docutils.sourceforge.io/rst.html){:target="_blank"}
- **`rtf`** [Rich Text Format](https://en.wikipedia.org/wiki/Rich_Text_Format){:target="_blank"}
- **`tif`** [Tag Image File Format](https://en.wikipedia.org/wiki/TIFF){:target="_blank"}
- **`tiff`** [Tag Image File Format](https://en.wikipedia.org/wiki/TIFF){:target="_blank"}
- **`webp`** [Image file format with lossless and lossy compression](https://developers.google.com/speed/webp){:target="_blank"}

<div style="page-break-after: always;"></div>

## 2. Detailed processing steps

### 2.1 Preprocessor

### 2.1.1 Preprocessor Architecture

![](img/architecture_preprocessor.png)

### 2.1.2 Process the inbox directory (step: **`p_i`**)

In the first step, the file directory **`inbox`** is checked for new document files. 
An entry is created in the **`document`** database table for each new document, showing the current processing status of the document. 

The association of document and language is managed via subdirectories of the file folder **`inbox`**. 
In the database table **`language`**, the column **`directory_name_inbox`** specifies per language in which subdirectory the documents in this language are to be supplied. 
Detailed information on this can be found in the chapter **Running DCR** in the section **Document Language**.

The new document files are processed based on their file extension as follows:

#### 2.1.2.1 File extension **`pdf`**

The module **`fitz`** from package [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/module.html){:target="_blank"} is used to check whether the **`pdf`** document is a scanned image or not. 
A **`pdf`** document consisting of a scanned image is marked for conversion from **`pdf`** format to an image format and moved to the file directory **`ìnbox_accepted`**.
Other **`pdf`** documents are marked for further processing with the **`pdf`** parser and then also moved to the file directory **`ìnbox_accepted`**.
If, however, when checking the **`pdf`** document with **`fitz`**, it turns out that the document with the file extension **`pdf`** is not really a **`pdf`** document, then the document is moved to the file directory **`inbox_rejected`**.

#### 2.1.2.2 File extensions of documents for processing with [Pandoc](https://pandoc.org){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}

Document files with the following file extensions are moved to the file directory **`ìnbox_accepted`** and 
marked for converting to **`pdf`** format using [Pandoc](https://pandoc.org){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}:

- **`csv`**
- **`docx`**
- **`epub`**
- **`html`**
- **`odt`**
- **`rst`**
- **`rtf`**

An exception are files with the file name **`README.md`**, which are ignored and not processed.

#### 2.1.2.3 File extensions of documents for processing with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}

Document files with the following file extensions are moved to the file directory **`ìnbox_accepted`** and marked for converting to **`pdf`** format using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}:

- **`bmp`**
- **`gif`**
- **`jp2`**
- **`jpeg`**
- **`png`**
- **`pnm`**
- **`tif`**
- **`tiff`**
- **`webp`**

#### 2.1.2.4 Other file extensions of documents

Document files that do not fall into one of the previous categories are marked as faulty and moved to the file directory **`ìnbox_rejected`**.

### 2.1.3 Convert **`pdf`** documents to image files (step: **`p_2_i`**)

This processing step only has to be carried out if there are new **`pdf`** documents in the document input that only consist of scanned images.
**`pdf`** documents consisting of scanned images must first be processed with OCR software in order to extract text they contain. 
Since [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} does not support the **`pdf`** file format, such a **`pdf`** document must first be converted into one or more image files. 
This is done with the software [pdf2image](https://pypi.org/project/pdf2image){:target="_blank"}, which in turn is based on the [Poppler](https://poppler.freedesktop.org){:target="_blank"} software.

The processing of the original document (parent document) is then completed and the further processing is carried out with the newly created image file(s) (child document(s)).

Since an image file created here always contains only one page of a **`pdf`** document, a multi-page **`pdf`** document is distributed over several image files. 
After processing with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}, these separated files are then combined into one **`pdf`** document.

### 2.1.4 Convert appropriate image documents to **`pdf`** files (step: **`ocr`**)

This processing step only has to be performed if there are new documents in the document entry that correspond to one of the document types listed in section 2.1.2.3.
In this processing step, the documents of this document types are converted to the **`pdf`** format using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}.

In case of success the processing of the original document (parent document) is then completed and the further processing is carried out with the newly created **`pdf`** file (child document).
In the event of an error, the original document is marked as erroneous and an explanatory entry is also written in the **`document`** table. 

After processing with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}, the files split in the previous processing step are combined into a single **`pdf`** document.

### 2.1.5 Convert appropriate non-**`pdf`** documents to **`pdf`** files (step: **`n_2_p`**)

This processing step only has to be performed if there are new documents in the document entry that correspond to one of the document types listed in section 2.1.2.2.
In this processing step, the documents of this document types are converted to **`pdf`** format using [Pandoc](https://pandoc.org){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}.

In case of success the processing of the original document (parent document) is then completed and the further processing is carried out with the newly created **`pdf`** file (child document).
In the event of an error, the original document is marked as erroneous and an explanatory entry is also written in the **`document`** table. 

### 2.2 Natural Language Processing (NLP)

### 2.2.1 NLP Architecture

![](img/architecture_nlp.png)

### 2.2.2 Extract text from **`pdf`** documents (step: **`tet`**)

In this processing step, the text of the **`pdf`** documents from sections 2.1.2.1, 2.1.4 and 2.1.5 are extracted and written to **`xml`** files in **`tetml`** format for each document.
The [PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"} library is used for this purpose.

In case of success the processing of the original document (parent document) is then completed and the further processing is carried out with the newly created **`xml`** files (child documents).
In the event of an error, the original document is marked as erroneous and an explanatory entry is also written in the **`document`** table. 

Depending on the configuration parameters **`tetml_page`** and **`tetml_word`**, up to three different **`xml`** files with different granularity can be created per document:

- **`tetml_line`**: granularity document `line` (generated by default),
- **`tetml_page`**: granularity document `page`,
- **`tetml_word`**: granularity document `word`.

The `word` variant is optional, but at least one of the variants `line` and `page` must be selected.

<div style="page-break-after: always;"></div>

**Example extract from granularity `line`**:

The output is written to a **`xml`** file named `<file_name>_<doc_id>.line.xml`:

    <Pages>
    <Page number="1" width="612.00" height="792.00">
    <Options>granularity=line</Options>
    <Content granularity="line" dehyphenation="false" dropcap="false" font="false" geometry="false" shadow="false" sub="false" sup="false">
    <Para>
     <Box llx="303.36" lly="746.40" urx="308.40" ury="756.48">
      <Line llx="303.36" lly="746.40" urx="308.40" ury="756.48">
       <Text>1</Text>
      </Line>
     </Box>
    </Para>
    <Para>
     <Box llx="126.00" lly="706.56" urx="153.84" ury="720.48">
      <Line llx="126.00" lly="706.56" urx="153.84" ury="720.48">
       <Text>1812</Text>
      </Line>
     </Box>
    </Para>
    <Para>
     <Box llx="126.00" lly="607.92" urx="420.27" ury="685.44">
      <Line llx="126.00" lly="671.52" urx="289.21" ury="685.44">
       <Text>GRIMM’S FAIRY TALES</Text>
      </Line>
      <Line llx="126.00" lly="639.36" urx="219.16" ury="653.28">
       <Text>CINDERELLA</Text>
      </Line>
      <Line llx="126.00" lly="607.92" urx="420.27" ury="621.84">
       <Text>Jacob Ludwig Grimm and Wilhelm Carl Grimm</Text>
      </Line>
     </Box>
    </Para>
    <Para>
     <Box llx="126.00" lly="460.32" urx="486.03" ury="589.44">
      <Line llx="126.00" lly="577.44" urx="485.98" ury="589.44">
       <Text>Grimm, Jacob (1785-1863) and Wilhelm (1786-1859) - German</Text>
      </Line>
      <Line llx="126.00" lly="562.80" urx="486.00" ury="574.80">
       <Text>philologists whose collection “Kinder- und Hausmarchen,” known</Text>
      </Line>

<div style="page-break-after: always;"></div>

**Example extract from granularity `page`**:

The output is written to the database table **`content_tetml_page`**:

    1
    1812
    GRIMM’S FAIRY TALES CINDERELLA Jacob Ludwig Grimm and Wilhelm Carl Grimm
    Grimm, Jacob (1785-1863) and Wilhelm (1786-1859) - German philologists whose collection “Kinder- und Hausmarchen,” known in English as “Grimm’s Fairy Tales,” is a timeless literary masterpiece. The brothers transcribed these tales directly from folk and fairy stories told to them by common villagers. Cinderella (1812) - The famous tale of a girl who is mistreated by her evil stepmother and step-sisters but goes on to marry the prince. This, the original “Cindrella,” differs greatly from many of its modern variations.
    CINDERELLA
    THERE WAS once a rich man whose wife lay sick, and when she felt her end drawing near she called to her only daughter to come near her bed, and said, “Dear child, be good and pious, and God will always take care of you, and I will look down upon you from heaven, and will be with you.” And then she closed her eyes and died. The maiden went every day to her mother’s grave and wept, and was always pious and good. When the winter came the snow covered the grave with a white covering, and when the sun came in the early spring and melted it away, the man took to himself another wife.
    The new wife brought two daughters home with her, and they were beautiful and fair in appearance, but at heart were black and ugly. And then began very evil times for the poor step-daughter.
    “Is the stupid creature to sit in the same room with us?” said they; “those who eat food must earn it. She is nothing but a kitchenmaid!” They took away her pretty dresses, and put on her an old gray kirtle, and gave her wooden shoes to wear.
    “Just look now at the proud princess, how she is decked out!” cried they laughing, and then they sent her into the kitchen. There she was obliged to do heavy work from morning to night, get up early in the morning, draw water, make the fires, cook, and wash. Besides that, the sisters did their utmost to torment her- mocking

<div style="page-break-after: always;"></div>

**Example extract from granularity `word`**:

The output is written to a **`xml`** file named `<file_name>_<doc_id>.word.xml`:

    <Page number="1" width="612.00" height="792.00">
    <Options>granularity=word tetml={elements={line}}</Options>
    <Content granularity="word" dehyphenation="false" dropcap="false" font="false" geometry="false" shadow="false" sub="false" sup="false">
    <Para>
     <Box llx="303.36" lly="746.40" urx="308.40" ury="756.48">
      <Line llx="303.36" lly="746.40" urx="308.40" ury="756.48">
       <Word>
        <Text>1</Text>
        <Box llx="303.36" lly="746.40" urx="308.40" ury="756.48"/>
       </Word>
      </Line>
     </Box>
    </Para>
    <Para>
     <Box llx="126.00" lly="706.56" urx="153.84" ury="720.48">
      <Line llx="126.00" lly="706.56" urx="153.84" ury="720.48">
       <Word>
        <Text>1812</Text>
        <Box llx="126.00" lly="706.56" urx="153.84" ury="720.48"/>
       </Word>
      </Line>
     </Box>
    </Para>
    <Para>
     <Box llx="126.00" lly="607.92" urx="420.27" ury="685.44">
      <Line llx="126.00" lly="671.52" urx="289.21" ury="685.44">
       <Word>
        <Text>GRIMM</Text>
        <Box llx="126.00" lly="671.52" urx="180.85" ury="685.44"/>
       </Word>
       <Word>
        <Text>’</Text>
        <Box llx="180.83" lly="671.52" urx="184.70" ury="685.44"/>
       </Word>
       <Word>
        <Text>S</Text>
        <Box llx="184.69" lly="671.52" urx="193.20" ury="685.44"/>
       </Word>

<div style="page-break-after: always;"></div>

### 2.2.3 Store the parser result in a JSON file (step: **`s_p_j`**)

From the **xml** files of the granularity document `line` (`<file_name>_<doc_id>.line.xml`) or document `word` (`<file_name>_<doc_id>.word.xml`) created in the previous step, the text contained is now extracted with the existing metadata using **xml** parsing and stored in a JSON format in the database tables `content_tetml_line` and `content_tetml_word`.

If successful, processing of the original document (parent document) is then completed and further processing takes place with the new entries in the database tables `content_tetml_line` and `content_tetml_page` (child document).
In the event of an error, the original document is marked as erroneous and an explanatory entry is also written in the **`document`** table. 

The document `line` granularity attempts to determine the headers and footers of the document by means of the [Levenstein distance](https://en.wikipedia.org/wiki/Levenshtein_distance){:target="_blank"}.
This processing step is controlled by the following configuration parameters:

- `line_footer_max_distance = 3`
- `line_footer_max_lines = 3`
- `line_footer_preference = true`
- `line_header_max_distance = 3`
- `line_header_max_lines = 3`

**Example extract from database table `content_tetml_line`**:

Possible line types are `h` for header lines, `f` for footers and `b` for the remaining lines.

    {
      "noLinesInPage": 37,
      "noParasInPage": 9,
      "pageLines": [
        {
          "paraIndexPage": 0,
          "lineIndexPage": 0,
          "lineIndexPara": 0,
          "lineText": "1",
          "lineType": "h"
        },
        {
          "paraIndexPage": 1,
          "lineIndexPage": 1,
          "lineIndexPara": 0,
          "lineText": "1812",
          "lineType": "b"
        },
        {
          "paraIndexPage": 2,
          "lineIndexPage": 2,
          "lineIndexPara": 0,
          "lineText": "GRIMM’S FAIRY TALES",
          "lineType": "b"
        },
        {
          "paraIndexPage": 2,
          "lineIndexPage": 3,
          "lineIndexPara": 1,
          "lineText": "CINDERELLA",
          "lineType": "b"
        },
        {
          "paraIndexPage": 2,
          "lineIndexPage": 4,
          "lineIndexPara": 2,
          "lineText": "Jacob Ludwig Grimm and Wilhelm Carl Grimm",
          "lineType": "b"
        },
        {
          "paraIndexPage": 3,
          "lineIndexPage": 5,
          "lineIndexPara": 0,
          "lineText": "Grimm, Jacob (1785-1863) and Wilhelm (1786-1859) - German",
          "lineType": "b"
        },
        {
          "paraIndexPage": 3,
          "lineIndexPage": 6,
          "lineIndexPara": 1,
          "lineText": "philologists whose collection “Kinder- und Hausmarchen,” known",
          "lineType": "b"
        },
        {
          "paraIndexPage": 3,
          "lineIndexPage": 7,
          "lineIndexPara": 2,
          "lineText": "in English as “Grimm’s Fairy Tales,” is a timeless literary",
          "lineType": "b"
        },
        {
          "paraIndexPage": 3,
          "lineIndexPage": 8,
          "lineIndexPara": 3,
          "lineText": "masterpiece. The brothers transcribed these tales directly from folk",
          "lineType": "b"
        },
        {
          "paraIndexPage": 3,
          "lineIndexPage": 9,
          "lineIndexPara": 4,
          "lineText": "and fairy stories told to them by common villagers. Cinderella",
          "lineType": "b"
        },
        {
          "paraIndexPage": 3,
          "lineIndexPage": 10,
          "lineIndexPara": 5,
          "lineText": "(1812) - The famous tale of a girl who is mistreated by her evil stepmother",
          "lineType": "b"
        },
        {
          "paraIndexPage": 3,
          "lineIndexPage": 11,
          "lineIndexPara": 6,
          "lineText": "and step-sisters but goes on to marry the prince. This, the",
          "lineType": "b"
        },
        {
          "paraIndexPage": 3,
          "lineIndexPage": 12,
          "lineIndexPara": 7,
          "lineText": "original “Cindrella,” differs greatly from many of its modern",
          "lineType": "b"
        },
        {
          "paraIndexPage": 3,
          "lineIndexPage": 13,
          "lineIndexPara": 8,
          "lineText": "variations.",
          "lineType": "b"
        },
        {
          "paraIndexPage": 4,
          "lineIndexPage": 14,
          "lineIndexPara": 0,
          "lineText": "CINDERELLA",
          "lineType": "b"
        },
        {
          "paraIndexPage": 5,
          "lineIndexPage": 15,
          "lineIndexPara": 0,
          "lineText": "THERE WAS once a rich man whose wife lay sick, and when she",
          "lineType": "b"
        },

**Example extract from database table `content_tetml_word`**:

    {
      "noLinesInPage": 37,
      "noParasInPage": 9,
      "noWordsInPage": 417,
      "pageWords": [
        {
          "lineIndexPage": 0,
          "wordIndexLine": 0,
          "wordText": "1"
        },
        {
          "lineIndexPage": 1,
          "wordIndexLine": 0,
          "wordText": "1812"
        },
        {
          "lineIndexPage": 2,
          "wordIndexLine": 0,
          "wordText": "GRIMM"
        },
        {
          "lineIndexPage": 2,
          "wordIndexLine": 1,
          "wordText": "’"
        },
        {
          "lineIndexPage": 2,
          "wordIndexLine": 2,
          "wordText": "S"
        },
        {
          "lineIndexPage": 2,
          "wordIndexLine": 3,
          "wordText": "FAIRY"
        },
        {
          "lineIndexPage": 2,
          "wordIndexLine": 4,
          "wordText": "TALES"
        },
        {
          "lineIndexPage": 3,
          "wordIndexLine": 0,
          "wordText": "CINDERELLA"
        },
        {
          "lineIndexPage": 4,
          "wordIndexLine": 0,
          "wordText": "Jacob"
        },
        {
          "lineIndexPage": 4,
          "wordIndexLine": 1,
          "wordText": "Ludwig"
        },
        {
          "lineIndexPage": 4,
          "wordIndexLine": 2,
          "wordText": "Grimm"
        },
        {
          "lineIndexPage": 4,
          "wordIndexLine": 3,
          "wordText": "and"
        },
        {
          "lineIndexPage": 4,
          "wordIndexLine": 4,
          "wordText": "Wilhelm"
        },
        {
          "lineIndexPage": 4,
          "wordIndexLine": 5,
          "wordText": "Carl"
        },
        {
          "lineIndexPage": 4,
          "wordIndexLine": 6,
          "wordText": "Grimm"
        },
        {
          "lineIndexPage": 5,
          "wordIndexLine": 0,
          "wordText": "Grimm"
        },
        {
          "lineIndexPage": 5,
          "wordIndexLine": 1,
          "wordText": ","
        },
        {
          "lineIndexPage": 5,
          "wordIndexLine": 2,
          "wordText": "Jacob"
        },

### 2.2.4 Create qualified document tokens (step: **`tkn`**)

For tokenisation, [spaCy](https://spacy.io/usage/models){:target="_blank"} is used. 

The document text is made available to spaCy page by page.
Either the granularity document `line` or document `page` can be used for this.
With the granularity document `line`, the recognised headers and footers are left out of the token creation.

spaCy provides a number of attributes for the token. 
Details can be found [here](https://spacy.io/api/token#attributes){:target="_blank"} in the spaCy documentation.
The configuration parameters of the type `spacy_tkn_attr_...` control which of these attributes are stored to the database table `content_token`.
By default, the following attributes are stored:

- `spacy_tkn_attr_ent_iob_ `
- `spacy_tkn_attr_ent_type_ `
- `spacy_tkn_attr_i `
- `spacy_tkn_attr_is_currency `
- `spacy_tkn_attr_is_digit `
- `spacy_tkn_attr_is_oov `
- `spacy_tkn_attr_is_punct `
- `spacy_tkn_attr_is_sent_end `
- `spacy_tkn_attr_is_sent_start `
- `spacy_tkn_attr_is_stop `
- `spacy_tkn_attr_is_title `
- `spacy_tkn_attr_lemma_ `
- `spacy_tkn_attr_like_email `
- `spacy_tkn_attr_like_num `
- `spacy_tkn_attr_like_url `
- `spacy_tkn_attr_norm_ `
- `spacy_tkn_attr_pos_ `
- `spacy_tkn_attr_tag_ `
- `spacy_tkn_attr_text `
- `spacy_tkn_attr_whitespace_ `

In the event of an error, the original document is marked as erroneous and an explanatory entry is also written in the **`document`** table. 

**Example extract from database table `content_token`**:

    [
      {
        "tknEntIob_": "B",
        "tknEntType_": "DATE",
        "tknI": 0,
        "tknIsDigit": true,
        "tknIsOov": true,
        "tknIsSentStart": true,
        "tknLemma_": "1812",
        "tknLikeNum": true,
        "tknNorm_": "1812",
        "tknPos_": "NUM",
        "tknTag_": "CD",
        "tknText": "1812"
      },
      {
        "tknEntIob_": "O",
        "tknI": 1,
        "tknIsOov": true,
        "tknLemma_": "\n",
        "tknNorm_": "\n",
        "tknPos_": "SPACE",
        "tknTag_": "_SP",
        "tknText": "\n"
      },
      {
        "tknEntIob_": "B",
        "tknEntType_": "WORK_OF_ART",
        "tknI": 2,
        "tknIsOov": true,
        "tknLemma_": "GRIMM",
        "tknNorm_": "grimm",
        "tknPos_": "PROPN",
        "tknTag_": "NNP",
        "tknText": "GRIMM"
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "WORK_OF_ART",
        "tknI": 3,
        "tknIsOov": true,
        "tknIsStop": true,
        "tknIsTitle": true,
        "tknLemma_": "’s",
        "tknNorm_": "'s",
        "tknPos_": "PART",
        "tknTag_": "POS",
        "tknText": "’S",
        "tknWhitespace_": " "
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "WORK_OF_ART",
        "tknI": 4,
        "tknIsOov": true,
        "tknLemma_": "FAIRY",
        "tknNorm_": "fairy",
        "tknPos_": "PROPN",
        "tknTag_": "NNP",
        "tknText": "FAIRY",
        "tknWhitespace_": " "
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "WORK_OF_ART",
        "tknI": 5,
        "tknIsOov": true,
        "tknLemma_": "TALES",
        "tknNorm_": "tales",
        "tknPos_": "PROPN",
        "tknTag_": "NNPS",
        "tknText": "TALES"
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "WORK_OF_ART",
        "tknI": 6,
        "tknIsOov": true,
        "tknLemma_": "\n",
        "tknNorm_": "\n",
        "tknPos_": "SPACE",
        "tknTag_": "_SP",
        "tknText": "\n"
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "WORK_OF_ART",
        "tknI": 7,
        "tknIsOov": true,
        "tknLemma_": "CINDERELLA",
        "tknNorm_": "cinderella",
        "tknPos_": "PROPN",
        "tknTag_": "NNP",
        "tknText": "CINDERELLA"
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "WORK_OF_ART",
        "tknI": 8,
        "tknIsOov": true,
        "tknIsSentEnd": true,
        "tknLemma_": "\n",
        "tknNorm_": "\n",
        "tknPos_": "SPACE",
        "tknTag_": "_SP",
        "tknText": "\n"
      },
      {
        "tknEntIob_": "B",
        "tknEntType_": "PERSON",
        "tknI": 9,
        "tknIsOov": true,
        "tknIsSentStart": true,
        "tknIsTitle": true,
        "tknLemma_": "Jacob",
        "tknNorm_": "jacob",
        "tknPos_": "PROPN",
        "tknTag_": "NNP",
        "tknText": "Jacob",
        "tknWhitespace_": " "
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "PERSON",
        "tknI": 10,
        "tknIsOov": true,
        "tknIsTitle": true,
        "tknLemma_": "Ludwig",
        "tknNorm_": "ludwig",
        "tknPos_": "PROPN",
        "tknTag_": "NNP",
        "tknText": "Ludwig",
        "tknWhitespace_": " "
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "PERSON",
        "tknI": 11,
        "tknIsOov": true,
        "tknIsTitle": true,
        "tknLemma_": "Grimm",
        "tknNorm_": "grimm",
        "tknPos_": "PROPN",
        "tknTag_": "NNP",
        "tknText": "Grimm",
        "tknWhitespace_": " "
      },
      {
        "tknEntIob_": "O",
        "tknI": 12,
        "tknIsOov": true,
        "tknIsStop": true,
        "tknLemma_": "and",
        "tknNorm_": "and",
        "tknPos_": "CCONJ",
        "tknTag_": "CC",
        "tknText": "and",
        "tknWhitespace_": " "
      },
      {
        "tknEntIob_": "B",
        "tknEntType_": "PERSON",
        "tknI": 13,
        "tknIsOov": true,
        "tknIsTitle": true,
        "tknLemma_": "Wilhelm",
        "tknNorm_": "wilhelm",
        "tknPos_": "PROPN",
        "tknTag_": "NNP",
        "tknText": "Wilhelm",
        "tknWhitespace_": " "
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "PERSON",
        "tknI": 14,
        "tknIsOov": true,
        "tknIsTitle": true,
        "tknLemma_": "Carl",
        "tknNorm_": "carl",
        "tknPos_": "PROPN",
        "tknTag_": "NNP",
        "tknText": "Carl",
        "tknWhitespace_": " "
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "PERSON",
        "tknI": 15,
        "tknIsOov": true,
        "tknIsTitle": true,
        "tknLemma_": "Grimm",
        "tknNorm_": "grimm",
        "tknPos_": "PROPN",
        "tknTag_": "NNP",
        "tknText": "Grimm"
      },
      {
        "tknEntIob_": "I",
        "tknEntType_": "PERSON",
        "tknI": 16,
        "tknIsOov": true,
        "tknLemma_": "\n",
        "tknNorm_": "\n",
        "tknPos_": "SPACE",
        "tknTag_": "_SP",
        "tknText": "\n"
      },
