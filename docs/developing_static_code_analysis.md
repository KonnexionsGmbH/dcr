# DCR - Developing - Static Code Analysis

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

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
