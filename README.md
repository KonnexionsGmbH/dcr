# dcr - Document Content Recognition

![Travis (.org)](https://img.shields.io/travis/KonnexionsGmbH/dcr.svg?branch=master)
![GitHub release](https://img.shields.io/github/release/KonnexionsGmbH/dcr.svg)
![GitHub Release Date](https://img.shields.io/github/release-date/KonnexionsGmbH/dcr.svg)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/1.0.0.svg)

----

### Table of Contents

**[1. Introduction](#introduction)**<br>
**[2. Requirements](#requirements)**<br>
**[3. Installation](#installation)**<br>
**[4. Operation](#operation)**<br>
**[5. API Documentation](#api_documentation)**<br>

----

## <a name="introduction"></a> 1. Introduction

Based on the paper "Unfolding the Structure of a Document using Deep Learning" ([Rahman and Finin, 2019](docs/research.md#Rahman)), this software project attempts to automatically recognize the structure in arbitrary PDF documents and thus make them more searchable in a more qualified manner.
Documents not in PDF format are converted to PDF format using [Pandoc](https://pandoc.org). 
Documents based on scanning which, therefore, do not contain text elements, are scanned and converted to PDF format using the [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) software. 
This process applies to all image format files e.g. jpeg, tiff etc., as well as scanned images in PDF format.  

### High level system architecture from the paper:

![](docs/img/Screen-Shot-2020-06-03-at-1.45.33-PM.png)

### High level dcr architecture:

![](docs/img/dcr_Overview.png)

## <a name="requirements"></a> 2. Requirements

## <a name="installation"></a> 3. Installation

## <a name="operation"></a> 4. Operation

## <a name="api_documentation"></a> 5. API Documentation

### Modules

TBD
