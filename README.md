# DCR - Document Content Recognition - README

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.1)

Based on the paper "Unfolding the Structure of a Document using Deep Learning" (**[Rahman and Finin, 2019](https://konnexionsgmbh.github.io/dcr/research/#rahman-m-finin-t-2019)**), this software project attempts to automatically recognize the structure in arbitrary **`pdf`** documents and thus make them more searchable in a more qualified manner.
Documents not in **`pdf`** format are converted in advance to **`pdf`** format using **[Pandoc](https://pandoc.org)** and **[TeX Live](https://www.tug.org/texlive)** .
Documents based on scanning which, therefore, do not contain text elements, are scanned and converted in advance to **`pdf`** format using the **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)** software.

Please see the **[Documentation](https://konnexionsgmbh.github.io/dcr)** for more detailed information.

## Features

- Converting **`bmp`**, **`gif`**, **`jp2`**, **`jpeg`**, **`png`**, **`pnm`**, **`tif`**, **`tiff`** or **`webp`** type documents to **`pdf`** format using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
- Converting **`csv`**, **`docx`**, **`epub`**, **`html`**, **`odt`**, **`rst`** or **`rtf`** type documents to **`pdf`** format using [Pandoc](https://pandoc.org) and [TeX Live](https://www.tug.org/texlive).
- Converting scanned image **`pdf`** documents to a series of **`jpeg`** or **`png`** files using [pdf2image](https://pypi.org/project/pdf2image) and [Poppler](https://poppler.freedesktop.org){:target="_blank"}.
- Extracting text and metadata from **`pdf`** documents using [PDFlib TET](https://www.pdflib.com/products/tet/).
- Identifying scanned image **`pdf`** documents using [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/module.html).
- Support for documents in different languages - English, French, German and Italian as standard.
- Much more!

## Support

If you need help with **DCR**, do not hesitate to get in contact with us!

- For questions and high-level discussions, use **[Discussions](https://github.com/KonnexionsGmbH/dcr/discussions)** on GitHub.
- To report a bug or make a feature request, open an **[Issue](https://github.com/KonnexionsGmbH/dcr/issues)** on GitHub.

Please note that we may only provide support for problems / questions regarding core features of **DCR**.
Any questions or bug reports about features of third-party themes, plugins, extensions or similar should be made to their respective projects. 
But, such questions are **not** banned from the **[Discussions](https://github.com/KonnexionsGmbH/dcr/discussions)**.

Make sure to stick around to answer some questions as well!

## Links

- **[Official Documentation](https://konnexionsgmbh.github.io/dcr)**
- **[Release Notes](https://konnexionsgmbh.github.io/dcr/release_notes)**
- **[Discussions](https://github.com/KonnexionsGmbH/dcr/discussions)** (Third-party themes, recipes, plugins and more)

## Contributing to DCR

The **DCR** project welcomes, and depends on, contributions from developers and
users in the open source community. Please see the **[Contributing Guide](https://konnexionsgmbh.github.io/dcr/contributing)** for
information on how you can help.

## Code of Conduct

Everyone interacting in the **DCR** project's codebases, issue trackers, and
discussion forums is expected to follow the **[Code of Conduct](https://konnexionsgmbh.github.io/dcr/code_of_conduct)**.

## License

**[Konnexions Public License (KX-PL)](https://konnexionsgmbh.github.io/dcr/license)**
