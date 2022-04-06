# DCR - Document Content Recognition

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

## 1. Introduction

Based on the paper "Unfolding the Structure of a Document using Deep Learning" ([Rahman and Finin, 2019](developing_research_notes.md#Rahman){:target="_blank"}), this software project attempts to automatically recognize the structure in arbitrary **`pdf`** documents and thus make them better searchable in a more qualified manner.

The processing logic is as follows:

- New documents are made available in the file directory **` inbox`**. If required, other language-related file directories can also be used (see section [Document Language](https://konnexionsgmbh.github.io/dcr/running_document_language){:target="_blank"}).
- Documents in a file format accepted by **DCR** are registered and moved to the file directory **`ìnbox_accepted`**. All other documents are registered and moved to the file directory **`ìnbox_rejected`**.
- Documents not in **`pdf`** format are converted to **`pdf`** format using [Pandoc](https://pandoc.org){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}. 
- Documents based on scanning which, therefore, do not contain text elements, are scanned and converted to **`pdf`** format using the [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} software. This process applies to all image format files e.g. **`jpeg`**, **`tiff`** etc., as well as scanned images in **`pdf`** format.  
- From all **`pdf`** documents, the text and associated metadata is extracted into a document-specific **`xml`** file using [PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"}.
- The document-specific **`xml`** files are then parsed and the **DCR**-relevant contents are written to the database tables **`content`** and  **`document`**. 

### 1.1 Rahman & Finin Paper

---

![](img/Screen-Shot-2020-06-03-at-1.45.33-PM.png)

---

### 1.2 DCR Preprocessor Architecture

---

![](img/dcr_Overview.png)

---

## 2. Detailed processing steps

### 2.1 Preprocessor

### 2.1.1 Process the inbox directory (step: **`p_i`**)

In the first step, the file directory **`inbox`** is checked for new document files. 
An entry is created in the **`document`** database table for each new document, showing the current processing status of the document. 
In addition, document-related error messages and performance data are recorded in the **`journal`** database table.

The association of document and language is managed via subdirectories of the file folder **`inbox`**. 
In the database table **`language`**, the column **`directory_name_inbox`** specifies per language in which subdirectory the documents in this language are to be supplied. 
Detailed information on this can be found in the chapter **Running DCR** in the section **Document Language**.

The new document files are processed based on their file extension as follows:

#### 2.1.1.1 File extension **`pdf`**

The module **`fitz`** from package [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/module.html){:target="_blank"} is used to check whether the **`pdf`** document is a scanned image or not. 
A **`pdf`** document consisting of a scanned image is marked for conversion from **`pdf`** format to an image format and moved to the file directory **`ìnbox_accepted`**.
Other **`pdf`** documents are marked for further processing with the **`pdf`** parser and then also moved to the file directory **`ìnbox_accepted`**.
If, however, when checking the **`pdf`** document with **`fitz`**, it turns out that the document with the file extension **`pdf`** is not really a **`pdf`** document, then the document is moved to the file directory **`inbox_rejected`**.

#### 2.1.1.2 File extensions of documents for processing with Pandoc and TeX Live

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

#### 2.1.1.3 File extensions of documents for processing with Tesseract OCR

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

#### 2.1.1.4 Other file extensions of documents

Document files that do not fall into one of the previous categories are marked as faulty and moved to the file directory **`ìnbox_rejected`**.

### 2.1.2 Convert **`pdf`** documents to image files (step: **`p_2_i`**)

This processing step only has to be carried out if there are new **`pdf`** documents in the document input that only consist of scanned images.
**`pdf`** documents consisting of scanned images must first be processed with OCR software in order to extract text and metadata they contain. 
Since [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} does not support the **`pdf`** file format, such a **`pdf`** document must first be converted into one or more image files. 
This is done with the software [pdf2image](https://pypi.org/project/pdf2image){:target="_blank"}, which in turn is based on the [Poppler](https://poppler.freedesktop.org){:target="_blank"} software.
The processing of the original document (parent document) is then completed and the further processing is carried out with the newly created image file(s) (child document(s)).

Since an image file created here always contains only one page of a **`pdf`** document, a multi-page **`pdf`** document is distributed over several image files. 
After processing with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}, these separated files are then combined into one **`pdf`** document.

### 2.1.3 Convert appropriate image documents to **`pdf`** files (step: **`ocr`**)

This processing step only has to be performed if there are new documents in the document entry that correspond to one of the document types listed in section 2.1.3.
In this processing step, the document types listed in section 2.1.3 are converted to **`pdf`** format 
using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}.
In case of success the processing of the original document (parent document) is then completed and the further processing is carried out with the newly created **`pdf`** file (child document).
In the event of an error, the original document is marked as erroneous and an explanatory entry is also written in the **`journal`** table. 

After processing with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}, the files split in the previous processing step are combined into a single **`pdf`** document.

### 2.1.4 Convert appropriate non-pdf documents to **`pdf`** files (step: **`n_2_p`**)

This processing step only has to be performed if there are new documents in the document entry that correspond to one of the document types listed in section 2.1.2.
In this processing step, the document types listed in section 2.1.2 are converted to **`pdf`** format 
using [Pandoc](https://pandoc.org){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}.
In case of success the processing of the original document (parent document) is then completed and the further processing is carried out with the newly created **`pdf`** file (child document).
In the event of an error, the original document is marked as erroneous and an explanatory entry is also written in the **`journal`** table. 

### 2.1.5 Extract text and metadata from **`pdf`** documents (step: **`tet`**)

In this processing step, the text and metadata of the **`pdf`** documents from 2.1.1, 2.3 and 2.4 are extracted and written to an **`xml`** file in **`tetml`** format for each document.
The [PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"} library is used for this purpose.
In case of success the processing of the original document (parent document) is then completed and the further processing is carried out with the newly created **`xml`** file (child document).
In the event of an error, the original document is marked as erroneous and an explanatory entry is also written in the **`journal`** table. 

### 2.1.6 Store the document structure from the parser result (step: **`s_f_p`**)

The output of [PDFlib TET](https://www.pdflib.com/products/tet/){:target="_blank"} is parsed for document metadata relevant to **DCR** and the metadata thus found is written to the database tables **content** and **document** together with the original document text for further processing. 

#### 1. Database table **`document`**:

The database table **`document`** contains a basic entry for each processed document and an additional entry for each auxiliary file created in the processing process: 

![](img/index_2.1.6_example_document_1.png)

The fonts used in the document are stored in the JSON column **`fonts`** of the base entry of the document:

![](img/index_2.1.6_example_document_2.png)

The JSON property **`noWords`** shows the word-related frequency of use of the font:

    [
      {"id": "F0", "italicAngle": "0.00", "name": "Arial-BoldMT",   "noWords": 5,  "weight": "700.00"},
      {"id": "F1", "italicAngle": "0.00", "name": "ArialMT",        "noWords": 10, "weight": "400.00"},
      {"id": "F2", "italicAngle": "0.00", "name": "CourierNewPSMT", "noWords": 40, "weight": "400.00"}
    ]

#### 2. Database table **`content`**:

The database table **`content`** contains a separate entry for each sentence identified by PDFlib TET in the document:

![](img/index_2.1.6_example_content_1.png)

The main information about the respective sentence is in the JSON column **`sentence`**:

![](img/index_2.1.6_example_content_2.png)

An example JSON column **`sentence`**:

    {
      "noSentenceInPara": 2,
      "noWords": 10,
      "words": [
        {"fontId": "F2", "fontSize": "12.00", "noWordLine": 11, "noWordSentence": 1,  "wordParsed": "This"},
        {"fontId": "F2", "fontSize": "12.00", "noWordLine": 12, "noWordSentence": 2,  "wordParsed": "is"},
        {"fontId": "F2", "fontSize": "12.00", "noWordLine": 13, "noWordSentence": 3,  "wordParsed": "the"},
        {"fontId": "F2", "fontSize": "12.00", "noWordLine": 1,  "noWordSentence": 4,  "wordParsed": "second"},
        {"fontId": "F2", "fontSize": "12.00", "noWordLine": 2,  "noWordSentence": 5,  "wordParsed": "sentence"},
        {"fontId": "F2", "fontSize": "12.00", "noWordLine": 3,  "noWordSentence": 6,  "wordParsed": "of"},
        {"fontId": "F2", "fontSize": "12.00", "noWordLine": 4,  "noWordSentence": 7,  "wordParsed": "the"},
        {"fontId": "F2", "fontSize": "12.00", "noWordLine": 5,  "noWordSentence": 8,  "wordParsed": "first"},
        {"fontId": "F2", "fontSize": "12.00", "noWordLine": 6,  "noWordSentence": 9,  "wordParsed": "paragraph"},
        {"fontId": "F2", "fontSize": "12.00", "noWordLine": 7,  "noWordSentence": 10, "wordParsed": "."}
      ]
    }

### 2.2 TBD ...

