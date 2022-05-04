# DCR - Developing - Version Planning

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)

## 1. Version Planning

| Version | Feature(s)                            | Status |
|---------|---------------------------------------|--------|
| 0.9.3   | User interface based on tkinter       | Open   |
| 0.9.2   | Admin interface based on tkinter      | Open   |
| 0.9.1   | Core text preprocessing and wrangling | Done   |
| 0.9.0   | Parser                                | Done   |
| 0.8.0   | PDFlib TET processing                 | Done   |
| 0.7.0   | Tesseract OCR processing              | Done   |
| 0.6.5   | Pandoc processing                     | Done   |
| 0.6.0   | pdf for Tesseract OCR processing      | Done   |
| 0.5.0   | Inbox processing                      | Done   |

## 2. Next Development Steps

### 2.1 Still Open

#### 2.1.1 High Priority

- pandocdcr: convert **`doc`** documents to **`docx`**
- user: reconstruct original document

#### 2.1.2 Normal Priority

- API documentation: Content improvement
- API documentation: Layout improvement
- admin: reset a list of documents: clean up the database before the next process retry - delete existing data
- tool: check the content of the file directory against the database

#### 2.1.3 Low Priority

- Google Styleguide implementation

### 2.2 Already implemented

- API Documentation
- PDFlib TET processing
- Tesseract OCR - Installation  
- all: database table 'document': new column file_size
- all: database table 'document': new column no_pages_pdf
- all: merge database table 'journal' into 'document'
- clean up the auxiliary files in file directory inbox_accepted - keep the base document
- combine **`pdf`** files - scanned **`pdf`** documents - after Tesseract OCR
- convert the appropriate documents into the **`pdf`** format with Pandoc and TeX Live
- duplicate handling 
- error correction version 0.9.0
- error handling - highly defensive
- inbox.py - process_inbox() - processing ocr & non-ocr in the same method
- introduce default language
- introduce document language - eventually inbox subfolder per language
- load initialisation data
- optionally save the original document in the database
- parser result with JSON 
- parser: classify the lines, e.g. body, footer, header etc. 
- replace TeX Live by LuaLaTeX or XeLuTeX (Unicode)
- test cases for file duplicate
