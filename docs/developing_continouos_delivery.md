# DCR - Developing - Continuous Delivery

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)

The GitHub Actions are used to enforce the following good practices of the software engineering process in the CI/CD process:

- uniform formatting of all source code,
- static source code analysis,
- execution of the software testing framework, and
- creation of up-to-date user documentation.

The action **`standards`** in the GitHub Actions guarantees compliance with the required standards, the action **`ubuntu_all_production`** ensures error-free compilation for production use and the action **`all_development`** runs the tests against various operating system and **`Python`** versions.
The actions **`all_development`** and **`all_production`** must be able to run error-free on operating systems **`Ubuntu 18.04`**, **`Ubuntu 20.04`** and **`Ubuntu 22.04`**~~, **`Micrsoft Windows Server 2019`** and **`2022`**~~ and with **`Python`** version **`3.10`**, the action **`standards`** is only required error-free for the latest versions of **`Ubuntu`** and **`Python`**.

The individual steps to be carried out 

1. in the action **`standards`** are:
    1. set up **`Python`**, **`pip`** and **`pipenv`**
    2. install the development specific packages with **`pipenv`**
    3. compile the **`Python`** code
    4. format the code with isort, Black and docformatter
    5. lint the code with Bandit, Flake8, Mypy and Pylint
    6. check the API docs with pydocstyle
    7. create and upload the user docs with Pydoc-Markdown and Mkdocs
    8. install [Pandoc](https://pandoc.org){:target="_blank"}, [Poppler](https://poppler.freedesktop.org){:target="_blank"}, [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}
    9. publish the code coverage results to **`coveralls.io`**

2. in the action **`all_development`** are:
    1. set up **`Python`**, **`pip`** and **`pipenv`**
    2. install the **`development`** specific packages with **`pipenv`**
    3. compile the **`Python`** code
    4. install [Pandoc](https://pandoc.org){:target="_blank"}, [Poppler](https://poppler.freedesktop.org){:target="_blank"}, [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}
    5. run pytest for writing better program

3. in the action **`all_production`** are:
    1. set up **`Python`**, **`pip`** and **`pipenv`**
    2. install the **`production`** specific packages with **`pipenv`**
    3. compile the **`Python`** code
    4. install [Pandoc](https://pandoc.org){:target="_blank"}, [Poppler](https://poppler.freedesktop.org){:target="_blank"}, [Tesseract OCR](https://github.com/tesseract-ocr/tesseract){:target="_blank"} and [TeX Live](https://www.tug.org/texlive){:target="_blank"}
    5. run pytest for writing better program
    