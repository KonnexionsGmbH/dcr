# DCR - Document Content Recognition - README

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.7)

Based on the paper "Unfolding the Structure of a Document using Deep Learning" (**[Rahman and Finin, 2019](https://arxiv.org/abs/1910.03678)**), this software project attempts to use various software techniques to automatically recognise the structure in any **`pdf`** documents and thus make them more searchable.

The computer linguistic methods used here assume that the documents to be processed are in **`pdf`** format.
However, in order to be flexible in the selection of documents with regard to the file format, **DCR** contains a sophisticated preprocessor that can convert many of the non **`pdf`** formats into the **`pdf`** format.

From the documents in **`pdf`** format, the next steps are to extract the text with relevant metadata word by word, line by line or page by page. In the case of line-by-line extraction, the identified headers and footers are marked accordingly so that they can be neglected later in the token creation process.

In what is currently the last step, qualified tokens can be created, which on the one hand contain information about the localisation of the token in the document and on the other hand token classification features such as lemma, shape, normalisation, etc.

Please see the **[Documentation](https://konnexionsgmbh.github.io/dcr)** for more detailed information.

## 1. Features

### 1.1 General 
 
- Support for documents in different languages - English, French, German and Italian as standard.

### 1.2 Preprocessor 

- Identifying scanned image **`pdf`** documents using [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/module.html).
- Converting scanned image **`pdf`** documents to a series of **`jpeg`** or **`png`** files using [pdf2image](https://pypi.org/project/pdf2image) and [Poppler](https://poppler.freedesktop.org).
- Converting **`bmp`**, **`gif`**, **`jp2`**, **`jpeg`**, **`png`**, **`pnm`**, **`tif`**, **`tiff`** or **`webp`** type documents to **`pdf`** format using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
- Converting **`csv`**, **`docx`**, **`epub`**, **`html`**, **`odt`**, **`rst`** or **`rtf`** type documents to **`pdf`** format using [Pandoc](https://pandoc.org) and [TeX Live](https://www.tug.org/texlive).

### 1.3 Natural Language Processing (NLP) 

- Extracting text and metadata from **`pdf`** documents using [PDFlib TET](https://www.pdflib.com/products/tet/).
- Categorisation of the lines in the document, e.g. body, footer, header lines etc.
- Determination of the token structure sentence by sentence with the help of [spaCy](https://spacy.io).
- Storage of the analysis result optional in a [PostgreSQL](https://www.postgresql.org) database or in a JSON flat file.

## 2. Directory and File Structure of this Repository

### 2.1 Directories

| Directory         | Content                                                                     |
|-------------------|-----------------------------------------------------------------------------|
| .github/workflows | [GitHub Action](https://github.com/actions) workflows                       |
| data              | Inbox directories and database setup data                                   |
| docs              | **DCR** documentation files                                                 |
| resources         | DBeaver configuration, Gammadyne utility and various external documentation |
| scripts           | Ubuntu and Windows Script for running the application                       |
| src               | Python scripts and [PDFlib TET](https://www.pdflib.com/products/tet/) files |
| tests             | Scripts and data for pytest                                                 |

### 2.2 Files

| File             | Functionality                                                                                                                                                                                                                                                                                                                                                                |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| .gitignore       | Configuration of files and folders to be ignored.                                                                                                                                                                                                                                                                                                                            |
| .pylintrc        | Configuration file for [pylint](https://github.com/PyCQA/pylint).                                                                                                                                                                                                                                                                                                            |
| LICENSE          | Text of the licence terms.                                                                                                                                                                                                                                                                                                                                                   |
| logging_cfg.yaml | Configuration of the Logger functionality.                                                                                                                                                                                                                                                                                                                                   |
| Makefile         | Definition of tasks to be excuted with the `make` command.                                                                                                                                                                                                                                                                                                                   |
| mkdocs.yml       | Configuration file for [MkDocs](https://github.com/mkdocs/mkdocs/).                                                                                                                                                                                                                                                                                                          |
| Pipfile          | Definition of the Python package requirements.                                                                                                                                                                                                                                                                                                                               |
| Pipfile.lock     | Definition of the specific versions of the Python packages.                                                                                                                                                                                                                                                                                                                  |
| pyproject.toml   | Configuration file for [bandit](https://github.com/PyCQA/bandit), [black](https://github.com/psf/black), [isort](https://github.com/PyCQA/isort), [mypy](https://github.com/python/mypy),<br/> [pydoc-markdown](https://github.com/NiklasRosenstein/pydoc-markdown), [pydocstyle](https://github.com/PyCQA/pydocstyle), and [pytest](https://github.com/pytest-dev/pytest/). |
| README.md        | This file.                                                                                                                                                                                                                                                                                                                                                                   |
| run_dcr_dev      | Running the **DCR** functionality for development purposes.                                                                                                                                                                                                                                                                                                                  |
| run_dcr_prod     | Running the **DCR** functionality for productiove operation.                                                                                                                                                                                                                                                                                                                 |
| setup.cfg        | Configuration file for [coverage](https://github.com/nedbat/coveragepy/blob/6.3.2/doc/index.rst), **DCR**, [flake8](https://github.com/pycqa/flake8), and [radon](https://github.com/rubik/radon).                                                                                                                                                                           |
| setup.cfg.reference | Original setup configuration file.                                                                                                                                                                                                                                                                                                                                           |

## 3. Support

If you need help with **DCR**, do not hesitate to get in contact with us!

- For questions and high-level discussions, use **[Discussions](https://github.com/KonnexionsGmbH/dcr/discussions)** on GitHub.
- To report a bug or make a feature request, open an **[Issue](https://github.com/KonnexionsGmbH/dcr/issues)** on GitHub.

Please note that we may only provide support for problems / questions regarding core features of **DCR**.
Any questions or bug reports about features of third-party themes, plugins, extensions or similar should be made to their respective projects. 
But, such questions are **not** banned from the **[Discussions](https://github.com/KonnexionsGmbH/dcr/discussions)**.

Make sure to stick around to answer some questions as well!

## 4. Links

- **[Official Documentation](https://konnexionsgmbh.github.io/dcr)**
- **[Release Notes](https://konnexionsgmbh.github.io/dcr/release_notes)**
- **[Discussions](https://github.com/KonnexionsGmbH/dcr/discussions)** (Third-party themes, recipes, plugins and more)

## 5. Contributing to DCR

The **DCR** project welcomes, and depends on, contributions from developers and users in the open source community. 
Please see the **[Contributing Guide](https://konnexionsgmbh.github.io/dcr/contributing)** for
information on how you can help.

## 6. Code of Conduct

Everyone who interacts in the **DCR** project's codebase, issue trackers, and discussion forums is expected to follow the **[Code of Conduct](https://konnexionsgmbh.github.io/dcr/code_of_conduct)**.

## 7. License

**[Konnexions Public License (KX-PL)](https://konnexionsgmbh.github.io/dcr/license)**
