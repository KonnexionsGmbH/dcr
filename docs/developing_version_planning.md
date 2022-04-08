# DCR - Developing - Version Planning

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)

----

## 1. Version Planning

| Version   | Feature(s)                            |
|-----------|---------------------------------------|
| ~~0.5.0~~ | ~~Inbox processing~~                  |
| ~~0.6.0~~ | ~~pdf for Tesseract OCR processing~~  |
| ~~0.6.5~~ | ~~Pandoc processing~~                 |
| ~~0.7.0~~ | ~~Tesseract OCR processing~~          |
| ~~0.8.0~~ | ~~PDFlib TET processing~~             |
| ~~0.9.0~~ | ~~Parser~~                            |
| 0.9.1     | Admin interface based on tkinter      |
| 0.9.2     | Core text preprocessing and wrangling |
| 0.9.3     | User interface based on tkinter       |

## 2. Next Development Steps

- 9 API documentation: Content improvement
- 9 API documentation: Layout improvement
- 9 Google Styleguide implementation
- 9 admin: reset a list of documents: clean up the database before the next process retry - delete existing data
- 9 all: database table 'document': new column file_size
- 9 all: database table 'document': new column no_pages_pdf
- 9 all: merge database table 'journal' into 'document'
- 9 all: remove database table 'run', eventually keep some run related information in database table 'document'
- 9 pandocdcr: convert 'doc' documents to 'docx'
- 9 parser: classify the sentences, e.g. footer, header, title etc. 
- 9 parser: count and process gross words to net words, e.g. urls, email addresses etc.
- 9 parser: count and store no_words per font and per page
- 9 parser: take into account cross-pages sentences
- 9 tool: check the content of the file directory against the database
- 9 user: reconstruct original document
- ~~API Documentation~~
- ~~PDFlib TET processing~~
- ~~Tesseract OCR - Installation~~  
- ~~clean up the auxiliary files in file directory inbox_accepted - keep the base document~~
- ~~combine **`pdf`** files - scanned **`pdf`** documents - after Tesseract OCR~~
- ~~convert the appropriate documents into the **`pdf`** format with Pandoc and TeX Live~~
- ~~duplicate handling~~ 
- ~~error correction version 0.9.0~~
- ~~error handling - highly defensive~~
- ~~inbox.py - process_inbox() - processing ocr & non-ocr in the same method~~
- ~~introduce default language~~
- ~~introduce document language - eventually inbox subfolder per language~~
- ~~load initialisation data~~
- ~~optionally save the original document in the database~~
- ~~parser result with JSON~~ 
- ~~replace TeX Live by LuaLaTeX or XeLuTeX (Unicode)~~
- ~~test cases for file duplicate~~
