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
- The document-specific **`xml`** files are then parsed and the **DCR**-relevant contents are written to the **`JSON`** files. 
- From the **`JSON`** file(s) [spaCy](https://spacy.io){:target="_blank"} extracts qualified tokens and stores them either in a **`JSON`** file or in the database table **`token`**.

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

## 2. Detailed Processing Actions

The documents to be processed are divided into individual steps, so-called actions. 
Each action has the task of changing the state of a document by transforming an input file format into a different output file format.
The database tables **`run`**, **`document`**, and **`action`** document the current state of a document, as well as the actions performed so far.
If an error occurs during the processing of the document, this is recorded in the database tables **`document`** and **`action`**.
During the next run with the same action, the faulty documents are also processed again.

### 2.1 Preprocessor

#### 2.1.1 Preprocessor Architecture

![](img/architecture_preprocessor.png)

#### 2.1.2 Process the inbox directory (action: **`p_i`**)

In the first action, the file directory **`inbox`** is checked for new document files. 
An entry is created in the **`document`** database table for each new document, showing the current processing status of the document. 

The association of document and language is managed via subdirectories of the file folder **`inbox`**. 
In the database table **`language`**, the column **`directory_name_inbox`** specifies per language in which subdirectory the documents in this language are to be supplied. 
Detailed information on this can be found in the chapter **Running DCR** in the section **Document Language**.

The new document files are processed based on their file extension as follows:

##### 2.1.2.1 File extension **`pdf`**

The module **`fitz`** from package [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/module.html){:target="_blank"} is used to check whether the **`pdf`** document is a scanned image or not. 
A **`pdf`** document consisting of a scanned image is marked for conversion from **`pdf`** format to an image format and moved to the file directory **`ìnbox_accepted`**.
Other **`pdf`** documents are marked for further processing with the **`pdf`** parser and then also moved to the file directory **`ìnbox_accepted`**.
If, however, when checking the **`pdf`** document with **`fitz`**, it turns out that the document with the file extension **`pdf`** is not really a **`pdf`** document, then the document is moved to the file directory **`inbox_rejected`**.

##### 2.1.2.2 File extensions of documents for processing with [Pandoc](https://pandoc.org){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}

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

##### 2.1.2.3 File extensions of documents for processing with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}

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

##### 2.1.2.4 Other file extensions of documents

Document files that do not fall into one of the previous categories are marked as faulty and moved to the file directory **`ìnbox_rejected`**.

#### 2.1.3 Convert **`pdf`** documents to image files (action: **`p_2_i`**)

This processing action only has to be carried out if there are new **`pdf`** documents in the document input that only consist of scanned images.
**`pdf`** documents consisting of scanned images must first be processed with OCR software in order to extract text they contain. 
Since [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} does not support the **`pdf`** file format, such a **`pdf`** document must first be converted into one or more image files. 
This is done with the software [pdf2image](https://pypi.org/project/pdf2image){:target="_blank"}, which in turn is based on the [Poppler](https://poppler.freedesktop.org){:target="_blank"} software.

The processing of the original document (parent document) is then completed and the further processing is carried out with the newly created image file(s) (child document(s)).

Since an image file created here always contains only one page of a **`pdf`** document, a multi-page **`pdf`** document is distributed over several image files. 
After processing with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}, these separated files are then combined into one **`pdf`** document.

#### 2.1.4 Convert appropriate image files to **`pdf`** files (action: **`ocr`**)

This processing action only has to be performed if there are new documents in the document entry that correspond to one of the document types listed in section 2.1.2.3.
In this processing action, the documents of this document types are converted to the **`pdf`** format using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}.

After processing with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}, the files split in the previous processing action are combined into a single **`pdf`** document.

#### 2.1.5 Convert appropriate non-**`pdf`** documents to **`pdf`** files (action: **`n_2_p`**)

This processing action only has to be performed if there are new documents in the document entry that correspond to one of the document types listed in section 2.1.2.2.
In this processing action, the documents of this document types are converted to **`pdf`** format using [Pandoc](https://pandoc.org){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}.

### 2.2 NLP

#### 2.2.1 NLP Architecture

![](img/architecture_nlp.png)

#### 2.2.2 Extract text from **`pdf`** documents (action: **`tet`**)

In this processing action, the text of the **`pdf`** documents from sections 2.1.2.1, 2.1.4 and 2.1.5 are extracted and written to **`xml`** files in **`tetml`** format for each document.
The [PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"} library is used for this purpose.

Depending on the configuration parameters **`tetml_page`** and **`tetml_word`**, up to three different **`xml`** files with different granularity can be created per document:

- **`tetml_line`**: granularity document `line` (generated by default),
- **`tetml_page`**: granularity document `page`,
- **`tetml_word`**: granularity document `word`.

The `page` variant and the `word` variant are both optional.

**Example extract from granularity `line`**:

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

**Example extract from granularity `page`**:

    1
    1812
    GRIMM’S FAIRY TALES CINDERELLA Jacob Ludwig Grimm and Wilhelm Carl Grimm
    Grimm, Jacob (1785-1863) and Wilhelm (1786-1859) - German philologists whose collection “Kinder- und Hausmarchen,” known in English as “Grimm’s Fairy Tales,” is a timeless literary masterpiece. The brothers transcribed these tales directly from folk and fairy stories told to them by common villagers. Cinderella (1812) - The famous tale of a girl who is mistreated by her evil stepmother and step-sisters but goes on to marry the prince. This, the original “Cindrella,” differs greatly from many of its modern variations.
    CINDERELLA
    THERE WAS once a rich man whose wife lay sick, and when she felt her end drawing near she called to her only daughter to come near her bed, and said, “Dear child, be good and pious, and God will always take care of you, and I will look down upon you from heaven, and will be with you.” And then she closed her eyes and died. The maiden went every day to her mother’s grave and wept, and was always pious and good. When the winter came the snow covered the grave with a white covering, and when the sun came in the early spring and melted it away, the man took to himself another wife.
    The new wife brought two daughters home with her, and they were beautiful and fair in appearance, but at heart were black and ugly. And then began very evil times for the poor step-daughter.
    “Is the stupid creature to sit in the same room with us?” said they; “those who eat food must earn it. She is nothing but a kitchenmaid!” They took away her pretty dresses, and put on her an old gray kirtle, and gave her wooden shoes to wear.
    “Just look now at the proud princess, how she is decked out!” cried they laughing, and then they sent her into the kitchen. There she was obliged to do heavy work from morning to night, get up early in the morning, draw water, make the fires, cook, and wash. Besides that, the sisters did their utmost to torment her- mocking

**Example extract from granularity `word`**:

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

#### 2.2.3 Store the parser result in a JSON file (action: **`s_p_j`**)

From the **xml** files of the granularity document `line` (`<file_name>_<doc_id>.line.xml`) or document `word` (`<file_name>_<doc_id>.word.xml`) created in the previous action, the text contained is now extracted with the existing metadata using **xml** parsing and stored in a **`JSON`** format in the database tables `content_tetml_line` and `content_tetml_word`.

The document `line` granularity attempts to type the lines. Details on this process can be found in section 4.
  
**Example extract from granularity `line`**:

    {
        "documentId": 1,
        "documentFileName": "Grimms_Fairy_Tales_Cinderella_Standalone.pdf",
        "noPagesInDocument": 6,
        "noParagraphsInDocument": 39,
        "noLinesInDocument": 248,
        "noLinesFooter": 0,
        "noLinesHeader": 1,
        "noLinesToc": 0,
        "pages": [
            {
                "pageNo": 1,
                "noParagraphsInPage": 9,
                "noLinesInPage": 37,
                "lines": [
                    {
                        "lineNo": 1,
                        "lineIndexPage": 0,
                        "lineIndexParagraph": 0,
                        "lineType": "h",
                        "lowerLeftX": 303.36,
                        "paragraphNo": 1,
                        "text": "1"
                    },
                    {
                        "lineNo": 1,
                        "lineIndexPage": 1,
                        "lineIndexParagraph": 0,
                        "lineType": "b",
                        "lowerLeftX": 126.0,
                        "paragraphNo": 2,
                        "text": "1812"
                    },
                    {
                        "lineNo": 1,
                        "lineIndexPage": 2,
                        "lineIndexParagraph": 0,
                        "lineType": "b",
                        "lowerLeftX": 126.0,
                        "paragraphNo": 3,
                        "text": "GRIMM\u2019S FAIRY TALES"
                    },
                    {
                        "lineNo": 2,
                        "lineIndexPage": 3,
                        "lineIndexParagraph": 1,
                        "lineType": "b",
                        "lowerLeftX": 126.0,
                        "paragraphNo": 3,
                        "text": "CINDERELLA"
                    },
                    {
                        "lineNo": 3,
                        "lineIndexPage": 4,
                        "lineIndexParagraph": 2,
                        "lineType": "b",
                        "lowerLeftX": 126.0,
                        "paragraphNo": 3,
                        "text": "Jacob Ludwig Grimm and Wilhelm Carl Grimm"
                    },
                    {
                        "lineNo": 1,
                        "lineIndexPage": 5,
                        "lineIndexParagraph": 0,
                        "lineType": "b",
                        "lowerLeftX": 126.0,
                        "paragraphNo": 4,
                        "text": "Grimm, Jacob (1785-1863) and Wilhelm (1786-1859) - German"
                    },
                    {
                        "lineNo": 2,
                        "lineIndexPage": 6,
                        "lineIndexParagraph": 1,
                        "lineType": "b",
                        "lowerLeftX": 126.0,
                        "paragraphNo": 4,
                        "text": "philologists whose collection \u201cKinder- und Hausmarchen,\u201d known"
                    },
                    {
                        "lineNo": 3,
                        "lineIndexPage": 7,
                        "lineIndexParagraph": 2,
                        "lineType": "b",
                        "lowerLeftX": 126.0,
                        "paragraphNo": 4,
                        "text": "in English as \u201cGrimm\u2019s Fairy Tales,\u201d is a timeless literary"
                    },

**Example extract from granularity `word`**:

    {
        "documentId": 1,
        "documentFileName": "Grimms_Fairy_Tales_Cinderella_Standalone.pdf",
        "noPagesInDocument": 6,
        "noParagraphsInDocument": 39,
        "noLinesInDocument": 248,
        "noWordsInDocument": 3267,
        "pages": [
            {
                "pageNo": 1,
                "noParagraphsInPage": 9,
                "noLinesInPage": 37,
                "noWordsInPage": 417,
                "paragraphs": [
                    {
                        "paragraphNo": 1,
                        "noLinesInParagraph": 1,
                        "noWordsInParagraph": 1,
                        "lines": [
                            {
                                "lineNo": 1,
                                "noWordsInLine": 1,
                                "words": [
                                    {
                                        "wordNo": 1,
                                        "text": "1"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "paragraphNo": 2,
                        "noLinesInParagraph": 1,
                        "noWordsInParagraph": 1,
                        "lines": [
                            {
                                "lineNo": 1,
                                "noWordsInLine": 1,
                                "words": [
                                    {
                                        "wordNo": 1,
                                        "text": "1812"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "paragraphNo": 3,
                        "noLinesInParagraph": 3,
                        "noWordsInParagraph": 13,
                        "lines": [
                            {
                                "lineNo": 1,
                                "noWordsInLine": 5,
                                "words": [
                                    {
                                        "wordNo": 1,
                                        "text": "GRIMM"
                                    },
                                    {
                                        "wordNo": 2,
                                        "text": "\u2019"
                                    },
                                    {
                                        "wordNo": 3,
                                        "text": "S"
                                    },
                                    {
                                        "wordNo": 4,
                                        "text": "FAIRY"
                                    },
                                    {
                                        "wordNo": 5,
                                        "text": "TALES"
                                    }
                                ]
                            },

#### 2.2.4 Create qualified document tokens (action: **`tkn`**)

For tokenization, [spaCy](https://spacy.io/usage/models){:target="_blank"} is used. 

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

**Example extract from granularity `line`**:

    {
        "documentId": 1,
        "documentFileName": "Grimms_Fairy_Tales_Cinderella_Standalone.pdf",
        "noPagesInDocument": 6,
        "noParagraphsInDocument": 33,
        "noSentencesInDocument": 121,
        "noLinesInDocument": 242,
        "noTokensInDocument": 1085,
        "pages": [
            {
                "pageNo": 1,
                "noParagraphsInPage": 8,
                "noSentencesInPage": 19,
                "noLinesInPage": 36,
                "noTokensInPage": 174,
                "paragraphs": [
                    {
                        "paragraphNo": 2,
                        "noSentencesInParagraph": 1,
                        "noLinesInParagraph": 1,
                        "noTokensInParagraph": 1,
                        "sentences": [
                            {
                                "sentenceNo": 1,
                                "lowerLeftX": 126.0,
                                "noTokensInSentence": 1,
                                "text": "1812",
                                "tokens": [
                                    {
                                        "tknEntIob_": "B",
                                        "tknEntType_": "DATE",
                                        "tknI": 0,
                                        "tknIsDigit": true,
                                        "tknIsOov": true,
                                        "tknIsSentEnd": true,
                                        "tknIsSentStart": true,
                                        "tknLemma_": "1812",
                                        "tknLikeNum": true,
                                        "tknNorm_": "1812",
                                        "tknPos_": "NUM",
                                        "tknTag_": "CD",
                                        "tknText": "1812"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "paragraphNo": 3,
                        "noSentencesInParagraph": 1,
                        "noLinesInParagraph": 3,
                        "noTokensInParagraph": 10,
                        "sentences": [
                            {
                                "sentenceNo": 1,
                                "lowerLeftX": 126.0,
                                "noTokensInSentence": 10,
                                "text": "GRIMM\u2019S FAIRY TALES CINDERELLA Jacob Ludwig Grimm and Wilhelm Carl Grimm",
                                "tokens": [
                                    {
                                        "tknEntIob_": "B",
                                        "tknEntType_": "PERSON",
                                        "tknI": 0,
                                        "tknIsOov": true,
                                        "tknIsSentStart": true,
                                        "tknLemma_": "GRIMM",
                                        "tknNorm_": "grimm",
                                        "tknPos_": "PROPN",
                                        "tknTag_": "NNP",
                                        "tknText": "GRIMM"
                                    },
                                    {
                                        "tknEntIob_": "O",
                                        "tknI": 2,
                                        "tknIsOov": true,
                                        "tknLemma_": "fairy",
                                        "tknNorm_": "fairy",
                                        "tknPos_": "ADJ",
                                        "tknTag_": "JJ",
                                        "tknText": "FAIRY",
                                        "tknWhitespace_": " "
                                    },

## 3. Auxiliary File Namess

The processing actions are based on different flat files, each of which is generated from the original document on an action-related basis.
Apart from the **`JSON`** files optionally created during the 'tokenizer' action, these can be automatically deleted after error-free processing.

### 3.1 Naming System

**Action** `p_i` - process the inbox directory

    in : <ost>.<oft>              
    out: <ost>_<di>.<oft>

**Action** `p_2_i` - convert pdf documents to image files

    in : <ost>_<di>.pdf                
    out: <ost>_<di>.<jpeg|png>
                                       
**Action** `ocr` - convert image files to pdf documents

    in : <ost>_<di>.<oft>              
    or : <ost>_<di>.<jpeg|png>        
    out: <ost>_<di>_<pn>.pdf 
         <ost>_<di>_0.pdf        

**Action** `n_2_p` - convert non-pdf documents to pdf documents

    in : <ost>_<di>.<oft>              
    out: <ost>_<di>.pdf                                      

**Action** `tet` - extract text and metadata from pdf documents

    in : <ost>_<di>[_<pn>|_0].pdf       
    out: <ost>_<di>[_<pn>|_0]_line.xml        
         <ost>_<di>[_<pn>|_0]_page.xml 
         <ost>_<di>[_<pn>|_0]_word.xml

**Action** `s_p_j` - store the parser result in a **`JSON`** file

    in : <ost>_<di>[_<pn>|_0]_line.xml  
         <ost>_<di>[_<pn>|_0]_page.xml        
         <ost>_<di>[_<pn>|_0]_word.xml 
    out: <ost>_<di>[_<pn>|_0]_line.json 
         <ost>_<di>[_<pn>|_0]_line.toc.json 
         <ost>_<di>[_<pn>|_0]_page.json 
         <ost>_<di>[_<pn>|_0]_word.json

**Action** `tkn` - create qualified document tokens

    in : <ost>_<di>[_<pn>|_0]_line.json 
    out: <ost>_<di>[_<pn>|_0]_line_token.json 


| Abbr.  | Meaning             |
|--------|---------------------|
| `oft`  | original file type  |
| `osn`  | original stem name  |
| `di`   | document identifier |
| `pn`   | page number         |


### 3.2 Examples

#### 3.2.1 Possible intermediate files from a **`docx`** document:

    case_2_docx_route_inbox_pandoc_pdflib_2.docx

    case_2_docx_route_inbox_pandoc_pdflib_2.pdf

    case_2_docx_route_inbox_pandoc_pdflib_2.line.xml
    case_2_docx_route_inbox_pandoc_pdflib_2.page.xml
    case_2_docx_route_inbox_pandoc_pdflib_2.word.xml

    case_2_docx_route_inbox_pandoc_pdflib_2.line.json
    case_2_docx_route_inbox_pandoc_pdflib_2.line_toc.json
    case_2_docx_route_inbox_pandoc_pdflib_2.page.json
    case_2_docx_route_inbox_pandoc_pdflib_2.word.json

    case_2_docx_route_inbox_pandoc_pdflib_2.line.token.json

#### 3.2.2 Possible intermediate files from a **`jpg`** document:

    case_6_jpg_route_inbox_tesseract_pdflib_6.jpg

    case_6_jpg_route_inbox_tesseract_pdflib_6.pdf

    case_6_jpg_route_inbox_tesseract_pdflib_6.line.xml
    case_6_jpg_route_inbox_tesseract_pdflib_6.page.xml
    case_6_jpg_route_inbox_tesseract_pdflib_6.word.xml

    case_6_jpg_route_inbox_tesseract_pdflib_6.line.json
    case_6_jpg_route_inbox_tesseract_pdflib_6.line_toc.json
    case_6_jpg_route_inbox_tesseract_pdflib_6.page.json
    case_6_jpg_route_inbox_tesseract_pdflib_6.word.json

    case_6_jpg_route_inbox_tesseract_pdflib_6.line.token.json

#### 3.2.3 Possible intermediate files from a proper **`pdf`** document:

    case_3_pdf_text_route_inbox_pdflib_3.pdf

    case_3_pdf_text_route_inbox_pdflib_3.line.xml
    case_3_pdf_text_route_inbox_pdflib_3.page.xml
    case_3_pdf_text_route_inbox_pdflib_3.word.xml

    case_3_pdf_text_route_inbox_pdflib_3.line.json
    case_3_pdf_text_route_inbox_pdflib_3.line_toc.json
    case_3_pdf_text_route_inbox_pdflib_3.page.json
    case_3_pdf_text_route_inbox_pdflib_3.word.json

    case_3_pdf_text_route_inbox_pdflib_3.line.token.json

#### 3.2.4 Possible intermediate files from a single page scanned image **`pdf`** document:

    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4.pdf

    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4_1.jpeg

    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4_1.pdf

    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4_1.line.xml
    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4_1.page.xml
    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4_1.word.xml

    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4_1.line.json
    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4_1.line_toc.json
    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4_1.page.json
    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4_1.word.json

    case_4_pdf_image_small_route_inbox_pdf2image_tesseract_pdflib_4_1.line.token.json

#### 3.2.5 Possible intermediate files from a multi page scanned image **`pdf`** document:

    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5.pdf

    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_1.jpeg
    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_2.jpeg

    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_1.pdf
    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_2.pdf
    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_0.pdf

    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_0.line.xml
    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_0.page.xml
    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_0.word.xml

    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_0.line.json
    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_0.line_toc.json
    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_0.page.json
    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_0.word.json

    case_5_pdf_image_large_route_inbox_pdf2image_tesseract_pypdf2_pdflib_5_0.line.token.json

## 4 Line Type Algorithms

The granularity of the document `line` tries to classify the individual lines.
The possible line types are :

| line type | Meaning                                           |
|-----------|---------------------------------------------------|
| b         | non-classifiable line, i.e. normal text body line |
| f         | footer line                                       |
| h         | header line                                       |
| h_9       | level 9 heading line                              |
| lb        | line of a bulleted list                           |
| ln        | line of a numbered list                           |
| tab       | line of a table                                   |
| toc       | line of a table of content                        |

The following three rule-based algorithms are used to determine the line type in the order given:

1. `headers & footers`
The headers and footers are determined by a similarity comparison of the first `line_header_max_lines` and last `line_footer_max_lines` lines respectively. 

2. `close together`
The elements of bulleted or numbered lists must be close together and are determined by regular expressions. 
Tables have already been marked accordingly by PDFlib TET.
A table of contents must be in the first `toc_last_page` pages and consists of either a list or a table with ascending page numbers.

3. `headings`
Headings extend across the entire document and can have hierarchical structures. 
The headings are determined with rule-enriched regular expressions. 

### 4.1 Headings & Footers

The following parameter controls both the classification of the headers and the footers:

**`verbose_line_type_headers_footers`**

Default value: **`false`** - the verbose mode is an option that provides additional details as to what the processing algorithm is doing.

#### 4.1.1 Footers

**4.1.1.1 Parameters**

The following parameters control the classification of the footers:

**`line_footer_max_distance`**

Default value: **`3`** - The degree of similarity of rows is determined by means of the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance){:target="_blank"}. 
The value zero stands for identical lines. 
The larger the Levenshtein distance, the more different the rows are. 
If the header lines do not contain a page numbers, then the parameter should be set to `0`.

**`line_footer_max_lines`**

Default value: **`3`** - the number of lines from the bottom of the page to be analyzed as possible candidates for footers.
With the value zero the classification of footers is prevented.

**4.1.1.2 Algorithm**

1. On all pages, the last line `n`, the line `n-1`, etc. are compared up to the maximum specified line. 
2. The Levenshtein distance is determined for each pair of lines in the specified range for each current page and the previous page.
3. The line is considered a footer if, except for pages `1` and `2` and pages `n-1` and `n`, the Levenshtein distance is not greater than the specified maximum value.

#### 4.1.2 Headers

**4.1.2.1 Parameters**

The following parameters control the classification of the headers:

**`line_header_max_distance`**

Default value: **`3`** - the degree of similarity of rows is determined by means of the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance){:target="_blank"}. 
The value zero stands for identical lines. 
The larger the Levenshtein distance, the more different the rows are. 
If the footer lines contain a page number, then depending on the number of pages in the document, the following values are useful:

| document pages | Levenshtein distance |
|----------------|----------------------|
 | < 10           | 1                    |
 | < 100          | 2                    |
 | < 1000         | 3                    |

**`line_header_max_lines`**

Default value: **`3`** - the number of lines from the top of the page to be analyzed as possible candidates for headers.
A value of zero prevents the classification of headers.

**4.1.2.2 Algorithm**

1. On all pages, the first line, the second line, etc. are compared up to the maximum specified line. 
2. The Levenshtein distance is determined for each pair of lines in the specified range for each current page and the previous page.
3. The line is considered a header if, except for pages `1` and `2` and pages `n-1` and `n`, the Levenshtein distance is not greater than the specified maximum value.

### 4.2 Close Together

Here all line types are determined whose underlying text structures  have a closeness in space.
The order of processing is as follows

1. table of contents
2. tables which have already been marked accordingly by PDFlib TET
3. bulleted and numbered lists which must be close together and are determined by regular expressions. 

#### 4.2.1 TOC (Table of Content)

**4.2.1.1 Parameters**

The following parameters control the classification of the table of content:

- `toc_last_page = 3`
- `toc_min_entries = 3`
- `verbose_line_type_toc = false`

**`toc_last_page`**

Default value: **`3`** - sets the number of pages that will be searched for a table of contents from the beginning of the document.
A value of zero prevents the search for a table of contents.

**`toc_min_entries`**

Default value: **`3`** - defines the minimum number of entries that a table of contents must contain.

**`verbose_line_type_toc`**

Default value: **`false`** - the verbose mode is an option that provides additional details as to what the processing algorithm is doing.

**4.2.1.2 Algorithm Table-based**

A table with the following properties is searched for:

   - except for the first row, the last column of the table must contain an integer greater than zero,
   - the number found there must be ascending,
   - the number must not be greater than the last page number of the document, and
   - if such a table was found, then the algorithm ends here.

**4.2.1.3 Algorithm Line-based**

A block of lines with the following properties is searched here:

   - the last token from each line must contain an integer greater than zero,
   - the number found there must be ascending, and
   - the number must not be greater than the last page number of the document.

#### 4.2.2 Tables

TBD

#### 4.2.3 Bulleted Lists

TBD

#### 4.2.4 Numbered Lists

TBD

### 4.3 Headings

#### 4.3.1 Parameters

The following parameters control the classification of the headings:

**`heading_max_level`**

Default value: **`3`** - the maximum number of hierarchical heading levels.

**`heading_min_pages`**

Default value: **`2`** - the minimum number of document pages for determining headings.

**`heading_rules_file`**

Default value: **`none`** - name of a file including file directory that contains the rules for determining the headings.
**`none`** means that the given default rules are applied.

**`heading_toc_create`**

Default value: **`true`** - if true, a **`JSON`** file named `<document_name>_toc.json` is created in the file directory `data_accepted` with the identified headings.

**`heading_toc_incl_no_ctx`**

Default value: **`1`** - the `n` lines following the heading are included as context into the **`JSON`** file.

**`heading_toc_incl_regexp`**

Default value: **`false`** - if true, the regular expression for the heading is included in the **`JSON`** file..

**`heading_tolerance_x`**

Default value: **`5`** - percentage tolerance for the differences in indentation of a heading at the same level.

**`verbose_line_type_heading`**

Default value: **`false`** - the verbose mode is an option that provides additional details as to what the processing algorithm is doing.

#### 4.3.2 Heading Rules

A heading rule contains the following 5 elements:

| Nr. | element name        | description                                                                                              |
|-----|---------------------|----------------------------------------------------------------------------------------------------------|
| 1   | **`name`**          | for documentation purposes, a name that characterises the rule                                           |
| 2   | **`isFirstToken`**  | if true, the rule is applied to the first token of the line, <br/>otherwise to the beginning of the line |
| 3   | **`regexp`**        | the regular expression to be applied                                                                     |
| 4   | **`functionIsAsc`** | a comparison function for the values of the predecessor and the successor                                |
| 5   | **`startValues`**   | a list of allowed start values                                                                           |

The following comparison functions (**`functionIsAsc`**) can be used:

| function                | description                                                                                                         |
|-------------------------|---------------------------------------------------------------------------------------------------------------------|
| **`ignore`**            | no comparison is performed                                                                                          |
| **`lowercase_letters`** | two lowercase letters are compared,  <br/>whereby the ASCII difference must be exactly **`1`**                      |
| **`romans`**            | two Roman numerals are compared, <br/>whereby the difference must be exactly **`1`**                                |
| **`strings`**           | two strings are compared on ascending                                                                               |
| **`string_floats`**     | floating point numbers are compared, <br/>whereby the difference must be greater than **`0`** and less than **`1`** |
| **`string_integers`**   | two integer numbers are compared, <br/>whereby the difference must be exactly **`1`**                               |
| **`uppercase_letters`** | two uppercase letters are compared,  <br/>whereby the ASCII difference must be exactly **`1`**                      |

The following table shows the standard rules in the default processing order:

| name    | isFirstToken | regexp           | functionIsAsc      | startValues  |
|---------|--------------|------------------|--------------------|--------------|
| (999)   | True         | `"\(\d+\)$"`     | string_integers    | `["(1)"]`    |
| (A)     | True         | `"\([A-Z]\)$"`   | uppercase_letters  | `["(A)"]`    |
| (ROM)   | True         | see a)           | romans             | `["(I)"]`    |
| (a)     | True         | `"\([a-z]\)$"`   | lowercase_letters  | `["(a)"]`    |
| (rom)   | True         | see b)           | romans             | `["(i)"]`    |
| 999)    | True         | `"\d+\)$"`       | string_integers    | `["1)"]`     |
| 999.    | True         | `"\d+\.$"`       | string_integers    | `["1."]`     |
| 999.999 | True         | `"\d+\.\d+\.?$"` | string_floats      | `[]`         |
| A)      | True         | `"[A-Z]\)$"`     | uppercase_letters  | `["A)"]`     |
| A.      | True         | `"[A-Z]\.$"`     | uppercase_letters  | `["A, "A."]` |
| ROM)    | True         | see c)           | romans             | `["I)"]`     |
| ROM.    | True         | see d)           | romans             | `["I."]`     |
| a)      | True         | `"[a-z]\)$"`     | lowercase_letters  | `["a)"]`     |
| a.      | True         | `"[a-z]\.$"`     | lowercase_letters  | `["a, "a."]` |
| rom)    | True         | see e)           | romans             | `["i)"]`     |
| rom.    | True         | see f)           | romans             | `["i."]`     |

a) `"\(M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$"`

b) `"\(m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$"`

c) `"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\)$"`

d) `"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.$"`

e) `"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\)$"`

f) `"m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\.$"`

However, these default rules can also be overridden via a **`JSON`** file (see parameter **`heading_rules_file`**). 
An example file can be found in the file directory **`data`** with the file name **`heading_rules_test.json`**.

    {
      "lineTypeHeadingRules": [
        {
          "name": "(a)",
          "isFirstToken": true,
          "regexp": "\\([a-z]\\)$",
          "functionIsAsc": "lowercase_letters",
          "startValues": [
            "(a)"
          ]
        },
        {
          "name": "(A)",
          "isFirstToken": true,
          "regexp": "\\([A-Z]\\)$",
          "functionIsAsc": "uppercase_letters",
          "startValues": [
            "(A)"
          ]
        },

#### 4.3.3 Algorithm

- the document is worked through page by page and within a page line by line
- for each current heading level there is an entry in a hierarchy table
- for each document line, this hierarchy table is searched from bottom to top for a matching entry
- an entry is considered to be matching if
    - the regular expression is satisfied, and
    - the indentation is within the specified tolerance (`heading_tolerance_x`), and
    - the comparison function is fulfilled
- if there is a match, the following processing steps are carried out and then the next document line is processed
    - an entry for the JSON fileii is optionally created
    - any existing lower entries in the hierarchy table are deleted
- if no match is found, then the given heading rules are searched in the specified order
- a heading rule is matching if
    - the regular expression is satisfied, and
    - one of the optional start values matches the document line, and
    - the new heading level is within the specified limit (`heading_max_level`)
- if there is a match, the following processing steps are carried out and then the next document line is processed
    - the last heading level is increased by 1,
    - a new entry is added to the hierarchy table
    - an entry for the JSON fileii is optionally created
