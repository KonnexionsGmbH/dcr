# DCR - Document Content Recognition

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.8.0)

----

## 1. Introduction

Based on the paper "Unfolding the Structure of a Document using Deep Learning" ([Rahman and Finin, 2019](research_notes.md#Rahman){:target="_blank"}), this software project attempts to automatically recognize the structure in arbitrary PDF documents and thus make them more searchable in a more qualified manner.

The processing logic is as follows:

- New documents are made available in the file directory **`ìnbox`**.
- Documents in a file format accepted by DCR are registered and moved to the file directory **`ìnbox_accepted`**. All other documents are registered and moved to the file directory **`ìnbox_rejected`**.
- Documents not in PDF format are converted to PDF format using [Pandoc](https://pandoc.org){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}. 
- Documents based on scanning which, therefore, do not contain text elements, are scanned and converted to PDF format using the [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} software. This process applies to all image format files e.g. jpeg, tiff etc., as well as scanned images in PDF format.  
- TBD_TET

### 1.1 Rahman & Finin Paper

---

![](img/Screen-Shot-2020-06-03-at-1.45.33-PM.png)

---

### 1.2 DCR Architecture

---

![](img/dcr_Overview.png)

---

## 2. Detailed processing steps

### 2.1 Process the inbox directory (step: **`p_i`**)

In the first step, the file directory **`inbox`** is checked for new document files. 
An entry is created in the **`document`** database table for each new document, showing the current processing status of the document. 
In addition, each processing step of a document is recorded in the database table **`journal`**.
The new document files are processed based on their file extension as follows:

#### 2.1.1 File extension **`pdf`**

The module **`fitz`** from package [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/module.html){:target="_blank"} is used to check whether the **`pdf`** document is a scanned image or not. 
A **`pdf`** document consisting of a scanned image is marked for conversion from **`pdf`** format to an image format and moved to the file directory **`ìnbox_accepted`**.
Other **`pdf`** documents are marked for further processing with the **`pdf`** parser and then also moved to the file directory **`ìnbox_accepted`**.
If, however, when checking the **`pdf`** document with **`fitz`**, it turns out that the document with the file extension **`pdf`** is not really a **`pdf`** document, then the document is moved to the file directory **`inbox_rejected`**.

#### 2.1.2 File extensions of documents for processing with Pandoc and TeX Live

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

#### 2.1.3 File extensions of documents for processing with Tesseract OCR

Document files with the following file extensions are moved to the file directory **`ìnbox_accepted`** and marked for converting to **`pdf`** format using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}:

- **`bmp`**
- **`gif`**
- **`jp2`**
- **`jpeg`**
- **`png`**
- **`pnm`**
- **`tiff`**
- **`webp`**

#### 2.1.4 Other file extensions of documents

Document files that do not fall into one of the previous categories are marked as faulty and moved to the file directory **`ìnbox_rejected`**.

### 2.2 Convert pdf documents to image files (step: **`p_2_i`**)

pdf documents consisting of scanned images must first be processed with OCR software in order to extract the text they contain. 
Since [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} does not support the pdf file format, such a pdf document must first be converted into one or more image files. 
This is done with the software [pdf2image](https://pypi.org/project/pdf2image){:target="_blank"}, which in turn is based on the [Poppler](https://poppler.freedesktop.org){:target="_blank"} software.
The processing of the original document (parent document) is then completed and the further processing is carried out with the newly created image files (child document(s)).

### 2.3 Convert appropriate non-pdf documents to pdf files (step: **`n_2_p`**)

In this processing step, the document types listed in section 2.1.2 are converted to pdf format 
using [Pandoc](https://pandoc.org){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}.
In case of success the processing of the original document (parent document) is then completed and the further processing is carried out with the newly created pdf file (child document).
In the event of an error, the original document is marked as erroneous and an explanatory entry is also written in the **`journal`** table. 

### 2.4 Convert appropriate image documents to pdf files (step: **`ocr`**)

In this processing step, the document types listed in section 2.1.3 are converted to pdf format 
using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}.
In case of success the processing of the original document (parent document) is then completed and the further processing is carried out with the newly created pdf file (child document).
In the event of an error, the original document is marked as erroneous and an explanatory entry is also written in the **`journal`** table. 

### 2.5 Extract the text from pdf documents (step: **`tet`**)

TBD_TET

TBD_TET

## 3. Requirements

### 3.1 Operating System

Continuous delivery / integration (CD/CI) runs on **`Ubunto 18.04`**, **`Ubuntu 20.04`**~~, **`Windows Server 2019`** and **`Windows Server 2022`**~~.
This means that **`DCR`** also runs under **`Windows 10`** and **`Windows 11`**. 
In this case, only the functionality of the **`grep`**, **`make`**  and **`sed`** tools must be made available, e.g. via [Grep for Windows](http://gnuwin32.sourceforge.net/packages/grep.htm){:target="_blank"}, [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm){:target="_blank"} or [sed for Windows](http://gnuwin32.sourceforge.net/packages/sed.htm){:target="_blank"}.

### 3.2 Pandoc & TeX Live

To convert the non-PDF documents (see 2.1.2) into pdf files for PDFlib TET processing, 
the universal document converter [Pandoc](https://pandoc.org){:target="_blank"} 
and [TeX Live](https://www.tug.org/texlive){:target="_blank"} are used and must therefore also be installed.
The installation of the TeX Live Frontend is not required.

### 3.3 Poppler

To convert the scanned PDF documents into image files for Tesseract OCR, the rendering library [Poppler](https://poppler.freedesktop.org){:target="_blank"} is used and must therefore also be installed.

### 3.4 Python

Because of the use of the new typing features, **`Python`** version [3.10](https://docs.python.org/3/whatsnew/3.10.html){:target="_blank"} or higher is required.

### 3.5 Tesseract OCR

To convert image documents into 'pdf' files, **`Tesseract OCR`** version [5.10](https://github.com/tesseract-ocr/tesseract){:target="_blank"} or higher is required.

## 4. Installation

1. Clone or copy the **`DCR`** repository from [here](https://github.com/KonnexionsGmbH/dcr){:target="_blank"}.

2. Switch to **`DCR`**:

    **`cd dcr`**

3. Install the necessary Python packages:

    **`make pipenv-prod`**

4. Create a PostgreSQL database container with the script **`scripts/run_setup_postgresql`** and action **`prod`**.

5. Create the **`DCR`** database with the script **`run_dcr_prod`** and action **`db_c`**.

6. Optionally, adjustments can be made in the following configuration files:

   - **`logging_cfg.yaml`**: for the logging functionality

   - **`setup.cfg`**: for the **`DCR`** application in section **`dcr`**

### 4.1 **`setup.cfg`**

The customisable entries are:

      [dcr]
      db_connection_port = see environment
      db_connection_prefix = postgresql+psycopg2://
      db_database = see environment
      db_database_admin = see environment
      db_dialect = postgresql
      db_host = localhost
      db_password = postgresql
      db_password_admin = postgresql
      db_schema = dcr_schema
      db_user = dcr_user
      db_user_admin = dcr_user_admin
      dcr_version = 0.8.0
      directory_inbox = data/inbox
      directory_inbox_accepted = data/inbox_accepted
      directory_inbox_rejected = data/inbox_rejected
      ignore_duplicates = false
      pdf2image_type = jpeg
      tesseract_timeout = 10
      verbose = true

| Parameter                | Default value                | Description                                                                   |
|--------------------------|------------------------------|-------------------------------------------------------------------------------|
| db_connection_port       | environment specific         | port number the DBMS server is listening on                                   |
| db_connection_prefix     | **`postgresql+psycopg2://`** | front part of the database URL                                                |
| db_database              | environment specific         | DCR database name                                                             |
| db_database_admin        | environment specific         | administrative database name                                                  |
| db_dialect               | **`postgresql`**             | DBMS used, currently: only PostgreSQL allowed                                 |
| db_host                  | **`localhost`**              | host name of the DBMS server                                                  |
| db_password              | **`postgresql`**             | DCR database user password                                                    |
| db_password_admin        | **`postgresql`**             | administrative database password                                              |
| db_schema                | **`dcr_schema`**             | database schema name                                                          |
| db_user                  | **`postgresql`**             | DCR database user name                                                        |
| db_user_admin            | **`postgresql`**             | administrative database user name                                             |
| dcr_version              | **`0.8.0`**                  | current version number of the DCR application                                 |
| directory_inbox          | **`data/inbox`**             | directory for the new documents received                                      |
| directory_inbox_accepted | **`data/inbox_accepted`**    | directory for the accepted documents                                          |
| directory_inbox_rejected | **`data/inbox_rejected`**    | directory for the rejected documents                                          |
| ignore_duplicates        | **`false`**                  | accept presumably duplicated documents <br/>based on a SHA256 hash key        |
| pdfimage_type            | **`jpeg`**                   | format of the image files for the scanned <br/>`pdf` document: `jpeg`or `pdf` |
| tesseract_timeout        | **`10`**                     | terminate the tesseract job after a period of time (seconds)                  |
| verbose                  | **`true`**                   | display progress messages for processing                                      |

The configuration parameters can be set differently for the individual environments (`dev`, `prod` and `test`).

**Examples**:
      
      [dcr_dev]
      db_connection_port = 5432
      db_database = dcr_db_dev
      db_database_admin = dcr_db_dev_admin
      
      [dcr_prod]
      db_connection_port = 5433
      db_database = dcr_db_prod
      db_database_admin = dcr_db_prod_admin
      
      [dcr_test]
      db_connection_port = 5434
      db_database = dcr_db_test
      db_database_admin = dcr_db_test_admin

## 5. Operation

**`DCR`** should be operated via the script **`run_dcr_prod`**. 
The following actions are available:

| Action      | Process                                                                                                            |
|-------------|--------------------------------------------------------------------------------------------------------------------|
| **`all`**   | Run the complete processing of all new documents.                                                                  |
| **`db_c`**  | Create the database.                                                                                               |
| **`db_u`**  | Upgrade the database.                                                                                              |
| **`m_d`**   | Run the installation of the necessary 3rd party packages <br/>for development and run the development ecosystem.   |
| **`m_p`**   | Run the installation of the necessary 3rd party packages <br/>for production and compile all packages and modules. |
| **`n_2_p`** | Convert appropriate non-pdf documents to pdf files.                                                                |
| **`ocr`**   | Convert appropriate image documents to pdf files.                                                                  |
| **`p_i`**   | Process the inbox directory.                                                                                       |
| **`p_2_i`** | Convert pdf documents to image files.                                                                              |
| **`tet`**   | Extract the text from pdf documents.                                                                               |
