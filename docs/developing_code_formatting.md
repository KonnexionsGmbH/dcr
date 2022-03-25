# DCR - Developing - Code Formatting

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.0)

----

## 3. Code Formatting

The tools **`Black`**, **`docformatter`** and **`isort`** are used for formatting the programme code:

- [Black](https://black.readthedocs.io/en/stable){:target="_blank"} - The uncompromising **`Python`** code formatter.
- [docformatter](https://github.com/PyCQA/docformatter){:target="_blank"} - Formats docstrings to follow **PEP 257**.
- [isort](https://pycqa.github.io/isort){:target="_blank"} - A **`Python`** utility / library to sort imports.

All these tools are included in the call **`make format`** as well as in the call **`make dev`**.
They can be executed individually with **`make black`**,  **`make pydocstyle`** or **`make isort`**, 
where the recommended order is first **`make isort`**, then **`make black`** and finally **`make pydocstyle`**.
