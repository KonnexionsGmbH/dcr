# DCR - Release Notes

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.8)

## 1. Version 0.9.8

Release Date: dd.mm.2022

### 1.1 Modified Features

- Delimitation of the documentation to the **`DCR`** application
- Delimitation of the tests to the **`DCR`** application
- Updating the third party software used

### 1.2 Applied Software

| Software                                                                      | Version         | Remark                              | Status |
|:------------------------------------------------------------------------------|:----------------|:------------------------------------|--------|
| DBeaver                                                                       | 22.2.0          | for virtual machine only [optional] |        |
| Docker Desktop                                                                | 20.10.17        | base version [Docker Image & VM]    |        | 
| Git                                                                           | 2.34.1          | base version                        |        |
| [Pandoc](https://pandoc.org){:target="_blank"}                                | 2.19.2          |                                     |        |
| [PFlib TET](https://www.pdflib.com/products/tet){:target="_blank"}            | 5.3             |                                     |        |
| [Poppler](https://poppler.freedesktop.org){:target="_blank"}                  | 22.02.0         |                                     |        |
| Python3                                                                       | 3.10.7          |                                     |        |
| [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} | 5.2.0-22-g0daf1 | base version                        |        |
| [TeX Live](https://www.tug.org/texlive){:target="_blank"}                     | 2022            | base version                        |        |

#### 1.2.1 Unix-specific Software

| Software                                                        | Version     | Remark                  | Status |
|:----------------------------------------------------------------|:------------|:------------------------|--------|
| asdf                                                            | v0.10.2     | base version (optional) |        |
| cURL                                                            | 7.81.0      | base version            |        |
| dos2unix                                                        | 7.4.2       | base version            |        |
| GCC & G++                                                       | 11.2.0      | base version            |        |
| GNU Autoconf                                                    | 2.71        | base version            |        |
| GNU Automake                                                    | 1.16.5      | base version            |        |
| GNU make                                                        | 4.3         | base version            |        |
| [htop](https://htop.dev){:target="_blank"}                      | 3.2.1       | optional                |        |
| [OpenSSL](https://www.openssl.org){:target="_blank"}            | 1.1.1o      |                         |        |
| [procps](https://github.com/warmchang/procps){:target="_blank"} | 3.3.17      | base version (optional) |        |
| [tmux](https://github.com/tmux/tmux/wiki){:target="_blank"}     | 3.3a        | optional                |        |
| Ubuntu                                                          | 22.04.4 LTS | base version            |        |
| Vim                                                             | 8.2.3995    | base version (optional) |        |
| Wget                                                            | 1.21.2      |                         |        |

#### 1.2.2 Windows-specific Software

| Software                                                                                | Version | Remark        | Status |
|:----------------------------------------------------------------------------------------|:--------|:--------------|--------|
| [Grep for Windows](http://gnuwin32.sourceforge.net/packages/grep.htm){:target="_blank"} | 2.5.4   | base version  |        |
| [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm){:target="_blank"} | 3.81    | base version  |        |
| [sed for Windows](http://gnuwin32.sourceforge.net/packages/sed.htm){:target="_blank"}   | 4.2.1   | base version  |        |

### 1.3 Open issues

1. Tesseract OCR: (see [here](#issues_tesseract_ocr){:target="_blank"})

## 2. Detailed Open Issues

### <a name="issues_tesseract_ocr"></a> 2.2 [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"}

- Issue: Images of type 'jp2': Error in pixReadStreamJp2k: version 2.3.0: differs from minor = 2 ... [see #57](https://github.com/UB-Mannheim/tesseract/issues/57){:target="_blank"}

```
Issue (ocr): Converting the file 'D:\SoftDevelopment\Projects\dcr\data\inbox_accepted\pdf_scanned_03_ok_5.jp2' to the file 'D:\SoftDevelopment\Projects\dcr\data\inbox_accepted\pdf_scanned_03_ok_5.pdf' with Tesseract OCR failed - error status: '1' - error: 'Error in pixReadStreamJp2k: version 2.3.0: differs from minor = 2 Error in pixReadStream: jp2: no pix returned Error in pixRead: pix not read Error during processing.'.
```
