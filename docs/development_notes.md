# DCR - Development Notes

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.6.5)

----

## 1. System Environment

**`DCR`** is developed on the operating systems **`Ubuntu 20.04 LTS`** and **`Microsoft Windows 10`**.
Ubuntu is used here via the **`VM Workstation Player 16`**.
**`Ubuntu`** can also be used in conjunction with the **`Windows Subsystem for Linux (WSL2)`**.

The GitHub actions for continuous integration run on **`Ubuntu 18.04`**, **`Ubuntu 20.04`**, **`Micrsoft Windows Server 2019`** and **`Micrsoft Windows Server 2022`**.

Version **`3.10`** is used for the **`Python`** programming language.

## 2. Coding Standards

### 2.1 **`Python`**

- The [PEP 8](https://www.python.org/dev/peps/pep-0008){:target="_blank"} style guide for **`Python`** code is strictly applied and enforced with static analysis tools.
- All program code must be commented with type hinting instructions.
- All functions, modules and packages must be commented with **`Docstring`**.
- The program code must be covered as far as possible with appropriate tests - the aim is always 100 % test coverage.
- The successful execution of **`make dev`** ensures that the program code meets the required standards.

### 2.2. Scripts

- Scripts must always be available in identical functionality for both the Unix shell **`bash`** and the Windows command interpreter **`cmd.exe`**.
- The most important dynamic parameters of a script should be requested from the user in a dialogue.
- In the event of an error, the execution of the script must be terminated immediately.
- Apart from the main scripts, all other scripts should be present in the **`scripts`** file directory.
- The main scripts are:
    - `run_dcr_dev` - Running the DCR functionality for development purposes.
    - `run_dcr_prod` - Performing the DCR functionality for productive operation.

## 3. Code Formatting

The tools **`Black`**, **`docformatter`** and **`isort`** are used for formatting the programme code:

- [Black](https://black.readthedocs.io/en/stable){:target="_blank"} - The uncompromising **`Python`** code formatter.
- [docformatter](https://github.com/PyCQA/docformatter){:target="_blank"} - Formats docstrings to follow **PEP 257**.
- [isort](https://pycqa.github.io/isort){:target="_blank"} - A **`Python`** utility / library to sort imports.

All these tools are included in the call **`make format`** as well as in the call **`make dev`**.
They can be executed individually with **`make black`**,  **`make pydocstyle`** or **`make isort`**, 
where the recommended order is first **`make isort`**, then **`make black`** and finally **`make pydocstyle`**.

## 4. Static Code Analysis

The tools **`Bandit`**, **`Flake8`**, **`Mypy`** and **`Pylint`** are used for static code analysis:

- [Bandit](https://bandit.readthedocs.io/en/latest){:target="_blank"} - **`Bandit`** is a tool designed to find common security issues in **`Python`** code.
- [Flake8](https://flake8.pycqa.org/en/latest/index.html#quickstart){:target="_blank"} - A **`Python`** tool that glues together **`pycodestyle`**, **`Pyflakes`**, **`McCabe`**, and third-party plugins to check the style and quality of some **`Python`** code.
- [Mypy](https://mypy.readthedocs.io/en/stable/introduction.html){:target="_blank"} - Optional static typing for **`Python`**.
- [Pylint](https://pylint.pycqa.org/en/latest){:target="_blank"} - It's not just a linter that annoys you!

All these tools are included in the call **`make lint`** as well as in the call **`make dev`**.
They can be executed individually with **`make bandit`**, **`make flake8`**, **`make mypy`** and **`make pylint`**.

**`Flake8`** includes the following tools:

- [McCabe](https://github.com/PyCQA/mccabe){:target="_blank"} - McCabe complexity checker for **`Python`**.
- [pycodestyle](https://github.com/PyCQA/pycodestyle){:target="_blank"} - Simple **`Python`** style checker in one **`Python`** file.
- [Pyflakes](https://github.com/PyCQA/pyflakes){:target="_blank"} - A simple program which checks **`Python`** source files for errors.
- [Radon](https://radon.readthedocs.io/en/latest){:target="_blank"} - Various code metrics for **`Python`** code.

## 5. Software Documentation

### 5.1 API Documentation

The creation of API documentation for functions, modules and packages is mandatory and enforced with the static analysis tool [pydocstyle](https://github.com/PyCQA/pydocstyle){:target="_blank"}.
**`pydocstyle`** is a static analysis tool for checking compliance with **`Python`** **`Docstring`** conventions.
**`pydocstyle`** can be executed individually with **`make pydocstyle`** and is also included in both calls **`make docs`** and  **`make dev`**.

The **`Docstring`** format used in **`DCR`** is that of type Google. 
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
        p_i   - Process the inbox directory.
        p_2_i - Convert pdf documents to image files.

    With the option all, the following process steps are executed
    in this order:

        1. p_i
        2. p_2_i
        3. n_2_p

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

## 6. Software Testing

[pytest](https://github.com/pytest-dev/pytest){:target="_blank"} is used as a software testing framework with the following plugins::

- [pytest-cov](https://github.com/pytest-dev/pytest-cov){:target="_blank"} for coverage reporting,
- [pytest-deadfixture](https://github.com/jllorencetti/pytest-deadfixtures){:target="_blank"} to list unused or duplicate fixtures, and
- [pytest-random-order](https://github.com/jbasko/pytest-random-order){:target="_blank"} to randomise the order of the tests.

On the one hand, the tests must be as complete as possible, i.e. a test coverage of 100% is aimed for, but on the other hand, the scope of the test code should be minimal, i.e. unnecessary repetitions must be strictly avoided. 
The best strategy for this is to first create a test case for the normal case and then add special tests for the special cases not yet covered.

Finally, the tool [Coveralls for Python](https://github.com/TheKevJames/coveralls-python){:target="_blank"} is used to enable a connection to [Coveralls](https://coveralls.io/github/KonnexionsGmbH/dcr){:target="_blank"}.

## 7. Continuous Delivery

The GitHub Actions are used to enforce the following good practices of the software engineering process in the CI/CD process:

- uniform formatting of all source code,
- static source code analysis,
- execution of the software testing framework, and
- creation of up-to-date user documentation.

The branch **`Development Standards`** in the GitHub Actions guarantees compliance with the required standards, the branch **`Production`** ensures error-free compilation for production use and the branch **`Test Framework`** runs the tests against various operating system and **`Python`** versions.
The branches **`Production`** and **`Test Framework`** must be able to run error-free on operating systems **`Ubuntu 18.04`**, **`Ubuntu 20.04`**, **`Micrsoft Windows Server 2019`** and **`2022`** and with **`Python`** version **`3.10`**, the branch **`Development Standards`** is only required error-free for the latest versions of **`Ubuntu`** and **`Python`**.

The individual steps to be carried out 

1. in the branch **`standards`** are:
    1. set up **`Python`**, **`pip`** and **`pipenv`**
    1. install the development specific packages with **`pipenv`**
    1. compile the **`Python`** code
    1. format the code with isort, Black and docformatter
    1. lint the code with Bandit, Flake8, Mypy and Pylint
    1. check the API docs with pydocstyle
    1. create and upload the user docs with Pydoc-Markdown and Mkdocs
    1. publish the code coverage results to **`coveralls.io`**

1. in the branch **`development`** are:
    1. set up **`Python`**, **`pip`** and **`pipenv`**
    1. install the `**development**` specific packages with **`pipenv`**
    1. compile the **`Python`** code
    1. run pytest for writing better program

1. in the branch **`production`** are:
    1. set up **`Python`**, **`pip`** and **`pipenv`**
    1. install the `**production**` specific packages with **`pipenv`**
    1. compile the **`Python`** code
    1. run pytest for writing better program

## 8. Development Environment

To set up a suitable development environment under **`Ubuntu 20.04 LTS`**, on the one hand a suitable ready-made Docker image is provided and on the other hand two scripts to create the development system in a standalone system, a virtual environment or the **`Windows Subsystem for Linux (WSL2)`** are available.

### 8.1 Docker Image

The ready-made Docker images are available on [DockerHub](https://hub.docker.com){:target="_blank"} under the following link:

[dcr_dev - Document Content Recognition Development Image](https://hub.docker.com/repository/docker/konnexionsgmbh/dcr_dev){:target="_blank"}

When selecting the Docker image, care must be taken to select the appropriate version of the Docker image.

### 8.2 Script-based Solution

Alternatively, for a **`Ubuntu 20.04 LTS`** environment that is as unspoiled as possible, the following two scripts are available in the **`scripts`** file directory:

- **`scripts/0.6.5/run_install_4-vm_wsl2_1.sh`**
- **`scripts/0.6.5/run_install_4-vm_wsl2_2.sh`**

After a **`cd scripts`** command in a terminal window, the script **`run_install_4-vm_wsl2_1.sh`** must first be executed. 
Administration rights (**`sudo`**) are required for this. 
Afterwards, the second script **`run_install_4-vm_wsl2_2.sh`** must be executed in a new terminal window.

## 9. Version Planning

| Version   | Feature(s)                           |
|-----------|--------------------------------------|
| ~~0.5.0~~ | ~~Inbox processing~~                 |
| ~~0.6.0~~ | ~~pdf for Tesseract OCR processing~~ |
| ~~0.6.5~~ | ~~Pandoc processing~~                |
| 0.7.0     | Tesseract OCR processing             |
| 0.8.0     | PDFlib TET processing                |
| 0.9.0     | Parser                               |

## 10. Next Development Steps

**1<sup>st</sup> Priority:**

- ~~convert the appropriate documents into the `pdf` format with Pandoc and TeX Live~~
- test cases for file duplicate
- tools.py - verify the content of the inbox directories
- ~~API Documentation~~
- ~~duplicate handling~~ 
- ~~error handling - highly defensive~~
- ~~inbox.py - process_inbox() - processing ocr & non-ocr in the same method~~

**2<sup>nd</sup> Priority:** 

- Layout improvement API documentation
- Tesseract OCR - Installation  

**3<sup>rd</sup> Priority**

- n/a

**No Priority (yet)**

- n/a
