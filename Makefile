.DEFAULT_GOAL := help

##                                                                            .
## ============================================================================
## DCR - Document Content Recognition - make Documentation.
##       ---------------------------------------------------------------
##       The purpose of this Makefile is to support the whole software
##       development process for DCR. it contains also the necessary
##       tools for the CI activities.
##       ---------------------------------------------------------------
##       The available make commands are:
## ----------------------------------------------------------------------------
## help:               Show this help.
## ----------------------------------------------------------------------------
## dev:                Format, lint and test the code.
dev: format lint pydocstyle tests
## docs:               Check the API docs, create and upload the user docs.
# docs: pydocstyle pydoc-markdown mkdocs
docs: pydocstyle mkdocs
## format:             Format the code with isort, Black and docformatter.
format: isort black docformatter
## lint:               Lint the code with Bandit, Flake8, Mypy and Pylint.
lint: bandit flake8 mypy pylint
## tests:              Run all tests with pytest.
tests: pytest
## ----------------------------------------------------------------------------

help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

export DCR_ENVIRONMENT_TYPE=test

ifeq ($(OS),Windows_NT)
	DCR_DOCKER_CONTAINER=scripts\\run_setup_postgresql.bat test
    export MYPYPATH=src\\dcr;src\\dcr\\db;src\\dcr\\db\\orm;src\\dcr\\libs;src\\dcr\\nlp;src\\dcr\\PDFlib;src\\dcr\\pp;src\\dcr\\setup
    export PYTHONPATH=src\\dcr;src\\dcr\\db;src\\dcr\\db\\orm;src\\dcr\\libs;src\\dcr\\nlp;src\\dcr\\PDFlib;src\\dcr\\pp;src\\dcr\\setup
else
	DCR_DOCKER_CONTAINER=./scripts/run_setup_postgresql.sh test
    export MYPYPATH=src/dcr:src/dcr/db:src/dcr/db/orm:src/dcr/libs:src/dcr/nlp:src/dcr/PDFlib:src/dcr/pp:src/dcr/setup
    export PYTHONPATH=src/dcr:src/dcr/db:src/dcr/db/orm:src/dcr/libs:src/dcr/nlp:src/dcr/PDFlib:src/dcr/pp:src/dcr/setup
endif

# Bandit is a tool designed to find common security issues in Python code.
# https://github.com/PyCQA/bandit
# Configuration file: none
bandit:             ## Find common security issues with Bandit.
	@echo "Info **********  Start: Bandit **************************************"
	pipenv run bandit --version
	pipenv run bandit -c pyproject.toml -r src
	@echo "Info **********  End:   Bandit **************************************"

# The Uncompromising Code Formatter
# https://github.com/psf/black
# Configuration file: pyproject.toml
black:              ## Format the code with Black.
	@echo "Info **********  Start: black ***************************************"
	pipenv run black --version
	pipenv run black src tests
	@echo "Info **********  End:   black ***************************************"

# Byte-compile Python libraries
# https://docs.python.org/3/library/compileall.html
# Configuration file: none
compileall:         ## Byte-compile the Python libraries.
	@echo "Info **********  Start: Compile All Python Scripts ******************"
	python --version
	python -m compileall
	@echo "Info **********  End:   Compile All Python Scripts ******************"

# Python interface to coveralls.io API
# https://github.com/TheKevJames/coveralls-python
# Configuration file: none
coveralls:          ## Run all the tests and upload the coverage data to coveralls.
	@echo "Info **********  Start: coveralls ***********************************"
	pipenv run pytest --cov=src --cov-report=xml tests
	pipenv run coveralls --service=github
	@echo "Info **********  End:   coveralls ***********************************"

# Formats docstrings to follow PEP 257
# https://github.com/PyCQA/docformatter
# Configuration file: none
docformatter:       ## Format the docstrings with docformatter.
	@echo "Info **********  Start: docformatter ********************************"
	pipenv run docformatter --version
	pipenv run docformatter --in-place -r src tests
	@echo "Info **********  End:   docformatter ********************************"

# Flake8: Your Tool For Style Guide Enforcement.
# includes McCabe:      https://github.com/PyCQA/mccabe
# includes pycodestyle: https://github.com/PyCQA/pycodestyle
# includes Pyflakes:    https://github.com/PyCQA/pyflakes
# includes Radon:       https://github.com/rubik/radon
# https://github.com/pycqa/flake8
# Configuration file: cfg.cfg
flake8:             ## Enforce the Python Style Guides with Flake8.
	@echo "Info **********  Start: Flake8 **************************************"
	pipenv run flake8 --version
	pipenv run flake8 --exclude TET.py src tests
	@echo "Info **********  End:   Flake8 **************************************"

# isort your imports, so you don't have to.
# https://github.com/PyCQA/isort
# Configuration file: pyproject.toml
isort:              ## Edit and sort the imports with isort.
	@echo "Info **********  Start: isort ***************************************"
	pipenv run isort --version
	pipenv run isort src tests
	@echo "Info **********  End:   isort ***************************************"

# Project documentation with Markdown.
# https://github.com/mkdocs/mkdocs/
# Configuration file: none
mkdocs:             ## Create and upload the user documentation with MkDocs.
	@echo "Info **********  Start: MkDocs **************************************"
	pipenv run mkdocs --version
	pipenv run mkdocs gh-deploy --force
	@echo "Info **********  End:   MkDocs **************************************"

# Mypy: Static Typing for Python
# https://github.com/python/mypy
# Configuration file: pyproject.toml
mypy:               ## Find typing issues with Mypy.
	@echo "Info **********  Start: Mypy ****************************************"
	@echo MYPYPATH=${MYPYPATH}
	pipenv run pip freeze | grep mypy
	pipenv run mypy --version
	pipenv run mypy --exclude src/dcr/PDFlib/TET.py src
	@echo "Info **********  End:   Mypy ****************************************"

# pip is the package installer for Python.
# https://pypi.org/project/pip/
# Configuration file: none
# Pipenv: Python Development Workflow for Humans.
# https://github.com/pypa/pipenv
# Configuration file: Pipfile
pipenv-dev:         ## Install the package dependencies for development.
	@echo "Info **********  Start: Installation of Development Packages ********"
	python -m pip install --upgrade pip
	python -m pip install --upgrade pipenv
	python -m pipenv install --dev
	python -m pipenv --rm
	exit
	python -m pipenv update --dev
	pipenv run spacy download de_dep_news_trf
	pipenv run spacy download en_core_web_trf
	pipenv run spacy download fr_dep_news_trf
	pipenv run spacy download it_core_news_lg
	pipenv run pip freeze
	python --version
	python -m pip --version
	@echo "Info **********  End:   Installation of Development Packages ********"
pipenv-prod:        ## Install the package dependencies for production.
	@echo "Info **********  Start: Installation of Production Packages *********"
	python -m pip install --upgrade pip
	python -m pip install --upgrade pipenv
	python -m pipenv install
	python -m pipenv --rm
	exit
	python -m pipenv update
	pipenv run spacy download de_dep_news_trf
	pipenv run spacy download en_core_web_trf
	pipenv run spacy download fr_dep_news_trf
	pipenv run spacy download it_core_news_lg
	pipenv run pip freeze
	python --version
	python -m pip --version
	@echo "Info **********  End:   Installation of Production Packages *********"

# Pydoc-Markdown - create Python API documentation in Markdown format.
# https://github.com/NiklasRosenstein/pydoc-markdown
# Configuration file: pyproject.toml
pydoc-markdown:     ## Create Python API documentation in Markdown format with Pydoc-Markdown.
	@echo "Info **********  Start: Pydoc-Markdown ******************************"
	pipenv run pydoc-markdown --version
	pipenv run pydoc-markdown -I src/dcr --render-toc > docs/developing_api_documentation.md
	@echo "Info **********  End:   Pydoc-Markdown ******************************"

# pydocstyle - docstring style checker.
# https://github.com/PyCQA/pydocstyle
# Configuration file: pyproject.toml
pydocstyle:         ## Check the API documentation with pydocstyle.
	@echo "Info **********  Start: pydocstyle **********************************"
	pipenv run pydocstyle --version
	pipenv run pydocstyle --count src tests
	@echo "Info **********  End:   pydocstyle **********************************"

# Pylint is a tool that checks for errors in Python code.
# https://github.com/PyCQA/pylint/
# Configuration file: .pylintrc
pylint:             ## Lint the code with Pylint.
	@echo "Info **********  Start: Pylint **************************************"
	pipenv run pylint --version
	pipenv run pylint src tests
	@echo "Info **********  End:   Pylint **************************************"

# pytest: helps you write better programs.
# https://github.com/pytest-dev/pytest/
# Configuration file: pyproject.toml
pytest:             ## Run all tests with pytest.
	@echo "Info **********  Start: pytest **************************************"
	$(DCR_DOCKER_CONTAINER)
	pipenv run pytest --version
	pipenv run pytest --dead-fixtures tests
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered --random-order -v tests
	@echo "Info **********  End:   pytest **************************************"
pytest-ci:          ## Run all tests with pytest after test tool installation.
	@echo "Info **********  Start: pytest **************************************"
	$(DCR_DOCKER_CONTAINER)
	pipenv install pytest
	pipenv install pytest-cov
	pipenv install pytest-deadfixtures
	pipenv install pytest-helpers-namespace
	pipenv install pytest-random-order
	pipenv install roman
	pipenv run pytest --version
	pipenv run pytest --dead-fixtures tests
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered --random-order -v tests
	@echo "Info **********  End:   pytest **************************************"
pytest-first-issue: ## Run all tests with pytest until the first issue occurs.
	@echo "Info **********  Start: pytest **************************************"
	pipenv run pytest --version
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered --random-order -v -x tests
	@echo "Info **********  End:   pytest **************************************"
pytest-issue:       ## Run only the tests with pytest which are marked with 'issue'.
	@echo "Info **********  Start: pytest **************************************"
	pipenv run pytest --version
	@echo DCR_ENVIRONMENT_TYPE=${DCR_ENVIRONMENT_TYPE}
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered -m issue -s --setup-show -v -x tests
	@echo "Info **********  End:   pytest **************************************"
pytest-module:      ## Run tests of specific module(s) with pytest - test_db_cls.
	@echo "Info **********  Start: pytest **************************************"
	pipenv run pytest --version
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered -v tests/test_db_cls.py
	@echo "Info **********  End:   pytest **************************************"

## ============================================================================
