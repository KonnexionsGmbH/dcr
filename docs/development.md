# DCR - Notes on the Software Development Process

## 1. System Environment

DCR is developed on the operating systems **`Ubuntu 20.04 LTS`** and **`Microsoft Windows 10`**.
Ubuntu is used here via the **`VM Workstation Player 16`**.

The GitHub actions for continuous integration run on **`Ubuntu 20.04`**, **`Micrsoft Windows Server 2019`** and **`2022`**.

Version **`3.10`** is used for the Python programming language.

## 2. Coding Standards

### 2.1 Python

- The [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code is strictly applied and enforced with static analysis tools.
- All program code must be commented with type hinting instructions.
- All functions, modules and packages must be commented with Docstrings.
- The program code must be covered as far as possible with appropriate tests - the aim is always 100 % test coverage.
- The successful execution of `make dev` ensures that the program code meets the required standards.

### 2.2. Scripts

- Scripts must always be available in identical functionality for both the Unix shell `bash` and the Windows command interpreter `cmd.exe`.
- The most important dynamic parameters of a script should be requested from the user in a dialogue.
- In the event of an error, the execution of the script must be terminated immediately.
- Apart from the main script, all other scripts should be present in the `scripts` file directory.

## 3. Code Formatting

The two tools `isort` and `Black` are used for formatting the programme code:

- [`Black`](https://black.readthedocs.io/en/stable/) - The uncompromising Python code formatter.
- [`isort`](https://pycqa.github.io/isort/) - A Python utility / library to sort imports.

Both tools are included in the call `make dev`. 
They can be executed individually with `make black` and `make isort`, whereby `sort` should run first and `black` afterwards.

## 4. Static Code Analysis

The tools `Bandit`, `Flake8`, `Mypy` and `Pylint` are used for formatting the programme code:

- [`Bandit`](https://bandit.readthedocs.io/en/latest/) - Bandit is a tool designed to find common security issues in Python code.
- [`Flake8`](https://flake8.pycqa.org/en/latest/index.html#quickstart) - A python tool that glues together pycodestyle, pyflakes, mccabe, and third-party plugins to check the style and quality of some python code.
- [`Mypy`](https://mypy.readthedocs.io/en/stable/introduction.html) - Optional static typing for Python.
- [`Pylint`](https://pylint.pycqa.org/en/latest/) - It's not just a linter that annoys you!

All tools are included in the call `make dev`.
They can be executed individually with `make bandit`, `make flake8`, `make mypy` and `make pylint`.

`Flake8` includes the following tools:

- [`McCabe`](https://github.com/PyCQA/mccabe) - McCabe complexity checker for Python.
- [`pycodestyle`](https://github.com/PyCQA/pycodestyle) - Simple Python style checker in one Python file.
- [`Pyflakes`](https://github.com/PyCQA/pyflakes) - A simple program which checks Python source files for errors.
- [`Radon`](https://radon.readthedocs.io/en/latest/) - https://github.com/PyCQA/pyflakes.

## 5. Software Documentation

### 5.1 API Documentation

## 6. Software Testing

## 7. Continuous Delivery

## 8. Development Environment

## 9. Planning

### Prio 1 

- inbox.py - process_inbox() - processing ocr & non-ocr in the same method
- error handling - highly defensive
- testing - verify os operatioons (rm, rmdir, mkdir, etc.)
- continuous delivery: running isort, black and mkdocs 

### Prio 2 

- docs
  - development.md
  - index.md
  - release_notes.md
  - API Documentation
  - beautify MkDocs documentation
- Tesseract OCR
  - Installation  

### Prio 3 

- tools.py - verify the content of the inbox directories
 
