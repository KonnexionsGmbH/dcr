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
docs: pydocstyle mkdocs
## format:             Format the code with isort and Black.
format: isort black
## lint:               Lint the code with Bandit, Flake8, Mypy and Pylint.
lint: bandit flake8 mypy pylint
## tests:              Run all tests with pytest.
tests: pytest
## ----------------------------------------------------------------------------

help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

ifeq ($(OS),Windows_NT)
    export MYPYPATH=src\\dcr
    export PYTHONPATH=src\\dcr
else
    export MYPYPATH=src/dcr
    export PYTHONPATH=src/dcr
endif

# Bandit is a tool designed to find common security issues in Python code.
# https://github.com/PyCQA/bandit
# Configuration file: none
bandit:             ## Find common security issues with Bandit.
	@echo "Info **********  Start: Bandit **************************************"
	pipenv run bandit --version
	pipenv run bandit -r src
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

# Flake8: Your Tool For Style Guide Enforcement.
# includes McCabe:      https://github.com/PyCQA/mccabe
# includes pycodestyle: https://github.com/PyCQA/pycodestyle
# includes Pyflakes:    https://github.com/PyCQA/pyflakes
# includes Radon:       https://github.com/rubik/radon
# https://github.com/pycqa/flake8
# Configuration file: setup.cfg
flake8:             ## Enforce the Python Style Guides with Flake8.
	@echo "Info **********  Start: Flake8 **************************************"
	pipenv run flake8 --version
	pipenv run flake8 src tests
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
	pipenv run mypy src
	@echo "Info **********  End:   Mypy ****************************************"

# pip is the package installer for Python.
# https://pypi.org/project/pip/
# Configuration file: none
pip:                ## Install and / or Upgrade pip.
	@echo "Info **********  Start: Install and / or Upgrade pip ****************"
	python -m pip install --upgrade pip
	python --version
	python -m pip --version
	@echo "Info **********  End:   Install and / or Upgrade pip ****************"

# Pipenv: Python Development Workflow for Humans.
# https://github.com/pypa/pipenv
# Configuration file: Pipfile
pipenv:             ## Install and upgrade pipenv.
	@echo "Info **********  Start: Install and Upgrade pipenv ******************"
	python -m pip install pipenv
	python -m pip install --upgrade pipenv
	python -m pipenv --version
	@echo "Info **********  End:   Install and Upgrade pipenv ******************"
pipenv-dev:         ## Install the package dependencies for development.
	@echo "Info **********  Start: Installation of Development Packages ********"
	python -m pipenv install --dev
	pipenv run pip freeze
	@echo "Info **********  End:   Installation of Development Packages ********"
pipenv-prod:        ## Install the package dependencies for production.
	@echo "Info **********  Start: Installation of Production Packages *********"
	python -m pipenv install
	pipenv run pip freeze
	@echo "Info **********  End:   Installation of Production Packages *********"

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
# Configuration file: pyproject.toml
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
	pipenv run pytest --version
	pipenv run pytest --dead-fixtures tests
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered --random-order tests
	@echo "Info **********  End:   pytest **************************************"
pytest-issue:       ## Run only the tests marked with issue.
	@echo "Info **********  Start: pytest **************************************"
	pipenv run pytest --version
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered -m issue --setup-show tests
	@echo "Info **********  End:   pytest **************************************"
pytest-ci:          ## Run all tests with pytest after test tool installation.
	@echo "Info **********  Start: pytest **************************************"
	pipenv install pytest
	pipenv install pytest-cov
	pipenv install pytest-deadfixtures
	pipenv install pytest-random-order
	pipenv run pytest --version
	pipenv run pytest --dead-fixtures tests
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered --random-order tests
	@echo "Info **********  End:   pytest **************************************"

## ============================================================================
