# DCR - Developing - Version Planning

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

## 9. Version Planning

| Version   | Feature(s)                           |
|-----------|--------------------------------------|
| ~~0.5.0~~ | ~~Inbox processing~~                 |
| ~~0.6.0~~ | ~~pdf for Tesseract OCR processing~~ |
| ~~0.6.5~~ | ~~Pandoc processing~~                |
| ~~0.7.0~~ | ~~Tesseract OCR processing~~         |
| ~~0.8.0~~ | ~~PDFlib TET processing~~            |
| 0.9.0     | Parser                               |
| 0.9.1     | Text preprocessing and wrangling     |

## 10. Next Development Steps

- 0 parser result with JSON 
- 1 clean up the database before the next process retry - delete existing data
- 2 clean up the auxiliary files in file directory inbox_accepted - keep the base document
- 3 combine **`pdf`** files - scanned **`pdf`** documents - after Tesseract OCR
- 4 reconstruct original document
- 5 convert 'doc' documents to 'docx'
- 6 check the content of the file directory against the database
- 7 API documentation: Content improvement
- 8 API documentation: Layout improvement
- 9 Google Styleguide implementation
- ~~API Documentation~~
- ~~PDFlib TET processing~~
- ~~Tesseract OCR - Installation~~  
- ~~convert the appropriate documents into the **`pdf`** format with Pandoc and TeX Live~~
- ~~duplicate handling~~ 
- ~~error correction version 0.9.0~~
- ~~error handling - highly defensive~~
- ~~inbox.py - process_inbox() - processing ocr & non-ocr in the same method~~
- ~~introduce default language~~
- ~~introduce document language - eventually inbox subfolder per language~~
- ~~load initialisation data~~
- ~~optionally save the original document in the database~~
- ~~replace TeX Live by LuaLaTeX or XeLuTeX (Unicode)~~
- ~~test cases for file duplicate~~
