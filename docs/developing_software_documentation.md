# DCR - Developing - Software Documentation

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

## 5. Software Documentation

### 5.1 API Documentation

The creation of API documentation for functions, modules and packages is mandatory and enforced with the static analysis tool [pydocstyle](https://github.com/PyCQA/pydocstyle){:target="_blank"}.
**`pydocstyle`** is a static analysis tool for checking compliance with **`Python`** **`Docstring`** conventions.
**`pydocstyle`** can be executed individually with **`make pydocstyle`** and is also included in both calls **`make docs`** and  **`make dev`**.

The **`Docstring`** format used in **DCR** is that of [type Google](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#383-functions-and-methods){:target="_blank"}. 
For Visual Studio Code, the extension [VSCode Python Docstring Generator](https://github.com/NilsJPWerner/autoDocstring){:target="_blank"} can be used when creating API documentation.  
With the [Pydoc-Markdown](https://github.com/NiklasRosenstein/pydoc-markdown){:target="_blank"} tool, the API documentation is extracted from the source files and put into Markdown format. 
In this format, the API documentation can then be integrated into the user documentation.

### 5.2 Examples for the format of the API documentation

**Package Documentation**:

    Package libs: DCR libraries.

**Module Dokumentation**:

    Module libs.inbox: Check and distribute incoming documents.
  
    New documents are made available in the file directory inbox.
    These are then checked and moved to the accepted or
    rejected file directories depending on the result of the check.
    Depending on the file format, the accepted documents are then
    converted into the pdf file format either with the help of Pandoc
    and TeX Live or with the help of Tesseract OCR.

**Function  Documentation**:

    Load the command line arguments into memory.Pandoc and TeX Live

    The command line arguments define the process steps to be executed.
    The valid arguments are:

        all   - Run the complete processing of all new documents.
        db_c  - Create the database.
        db_u  - Upgrade the database.
        n_2_p - Convert non-pdf docuents to pdf files.
        ocr   - Convert image docuents to pdf files.
        p_i   - Process the inbox directory.
        p_2_i - Convert pdf documents to image files.
        tet   - Extract text and metadata from pdf documents.

    With the option all, the following process steps are executed
    in this order:

        1. p_i
        2. p_2_i
        3. n_2_p
        4. ocr
        5. tet

    Args:
        argv (List[str]): Command line arguments.

    Returns:
        dict[str, bool]: The processing steps based on CLI arguments.

In Visual Studio Code, the [VSCode Python Docstring Generator](https://github.com/NilsJPWerner/autoDocstring){:target="_blank"} tool can be used to create a framework for API documentation.

### 5.3 User Documention

The remaining documents for the user documentation can be found in the file directory **`docs`** in Markdown format:

| File                     | Headline                      | Remarks                                   |
|--------------------------|-------------------------------|-------------------------------------------|
| **`code_of_conduct.md`** | Code of Conduct               |                                           |
| **`contributing.md`**    | Contributing Guide            |                                           |
| **`dcr_api.md`**         | API Documentation             |                                           |
| **`development.md`**     | Development                   | Notes on the software development process |
| **`index.md`**           | Document Content Recognition  | Background, installation and user guide   |
| **`license.md`**         | Text of the licence agreement |                                           |
| **`release_history.md`** | Release History               | Previous release notes                    |
| **`release_notes.md`**   | Release Notes                 | Release notes of the current version      |
| **`research.md`**        | Research                      | Reference to the relevant research papers |

The [MkDocs](https://github.com/mkdocs/mkdocs){:target="_blank"} tool is used to create the user documentation. 
With the command **`make mkdocs`** the user documentation is created by MkDocs and uploaded to the GitHub pages of the repository.
The command **`make mkdocs`** is also included in the calls **`make docs`** and **`make dev`**.
