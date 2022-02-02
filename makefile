.DEFAULT_GOAL := dev

black: black_src black_tests
flake8: flake8_src flake8_tests
isort: isort_src isort_tests
pydocstyle: pydocstyle_src pydocstyle_tests
pylint: pylint_src pylint_tests

dev_ext: isort black compileall        bandit flake8 mypy pylint_src pydocstyle pytest
dev_int: isort black compileall mkdocs bandit flake8 mypy pylint_src pydocstyle pytest

inst_dev:  pip pipenv pipenv_dev
inst_prod: pip pipenv pipenv_prod

prod: inst_prod compileall

syntax: isort_src black_src compileall flake8_src mypy pylint_src pydocstyle_src

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
bandit:
	@echo "Info **********  Start: Bandit **************************************"
	pipenv run bandit --version
	pipenv run bandit -r src
	@echo "Info **********  End:   Bandit **************************************"

# The Uncompromising Code Formatter
# https://github.com/psf/black
# Configuration file: pyproject.toml
black_src:
	@echo "Info **********  Start: black ***************************************"
	pipenv run black --version
	pipenv run black src
	@echo "Info **********  End:   black ***************************************"
black_tests:
	@echo "Info **********  Start: black ***************************************"
	pipenv run black --version
	pipenv run black tests
	@echo "Info **********  End:   black ***************************************"

# Byte-compile Python libraries
# https://docs.python.org/3/library/compileall.html
# Configuration file: none
compileall:
	@echo "Info **********  Start: Compile All Python Scripts ******************"
	python --version
	python -m compileall
	@echo "Info **********  End:   Compile All Python Scripts ******************"

# Python interface to coveralls.io API
# https://github.com/TheKevJames/coveralls-python
# Configuration file: none
coveralls:
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
flake8_src:
	@echo "Info **********  Start: Flake8 **************************************"
	pipenv run flake8 --version
	pipenv run flake8 src
	@echo "Info **********  End:   Flake8 **************************************"
flake8_tests:
	@echo "Info **********  Start: Flake8 **************************************"
	pipenv run flake8 --version
	pipenv run flake8 tests
	@echo "Info **********  End:   Flake8 **************************************"

# isort your imports, so you don't have to.
# https://github.com/PyCQA/isort
# Configuration file: pyproject.toml
isort_src:
	@echo "Info **********  Start: isort ***************************************"
	pipenv run isort --version
	pipenv run isort src
	@echo "Info **********  End:   isort ***************************************"
isort_tests:
	@echo "Info **********  Start: isort ***************************************"
	pipenv run isort --version
	pipenv run isort tests
	@echo "Info **********  End:   isort ***************************************"

# Project documentation with Markdown.
# https://github.com/mkdocs/mkdocs/
# Configuration file: none
mkdocs:
	@echo "Info **********  Start: MkDocs **************************************"
	pipenv run mkdocs --version
	pipenv run mkdocs gh-deploy --force
	@echo "Info **********  End:   MkDocs **************************************"

# Mypy: Static Typing for Python
# https://github.com/python/mypy
# Configuration file: pyproject.toml
mypy:
	@echo "Info **********  Start: MyPy ****************************************"
	@echo MYPYPATH=${MYPYPATH}
	pipenv run pip freeze | grep mypy
	pipenv run mypy --version
	pipenv run mypy src
	@echo "Info **********  End:   MyPy ****************************************"

# pip is the package installer for Python.
# https://pypi.org/project/pip/
# Configuration file: none
pip:
	@echo "Info **********  Start: Install and / or Upgrade pip ****************"
	python -m pip install --upgrade pip
	python --version
	python -m pip --version
	@echo "Info **********  End:   Install and / or Upgrade pip ****************"

# Pipenv: Python Development Workflow for Humans.
# https://github.com/pypa/pipenv
# Configuration file: Pipfile
pipenv:
	@echo "Info **********  Start: Install and Upgrade pipenv ******************"
	python -m pip install pipenv
	python -m pip install --upgrade pipenv
	python -m pipenv --version
	@echo "Info **********  End:   Install and Upgrade pipenv ******************"
pipenv_dev:
	@echo "Info **********  Start: Installation of Development Packages ********"
	python -m pipenv install --dev
	pipenv run pip freeze
	@echo "Info **********  End:   Installation of Development Packages ********"
pipenv_prod:
	@echo "Info **********  Start: Installation of Production Packages *********"
	python -m pipenv install
	pipenv run pip freeze
	@echo "Info **********  End:   Installation of Production Packages *********"

# pydocstyle - docstring style checker.
# https://github.com/PyCQA/pydocstyle
# Configuration file: pyproject.toml
pydocstyle_src:
	@echo "Info **********  Start: pydocstyle **********************************"
	pipenv run pydocstyle --version
	pipenv run pydocstyle --count src
	@echo "Info **********  End:   pydocstyle **********************************"
pydocstyle_tests:
	@echo "Info **********  Start: pydocstyle **********************************"
	pipenv run pydocstyle --version
	pipenv run pydocstyle --count tests
	@echo "Info **********  End:   pydocstyle **********************************"

# Pylint is a tool that checks for errors in Python code.
# https://github.com/PyCQA/pylint/
# Configuration file: pyproject.toml
pylint_src:
	@echo "Info **********  Start: Pylint **************************************"
	pipenv run pylint --version
	pipenv run pylint src
	@echo "Info **********  End:   Pylint **************************************"
pylint_tests:
	@echo "Info **********  Start: Pylint **************************************"
	pipenv run pylint --version
	pipenv run pylint tests
	@echo "Info **********  End:   Pylint **************************************"

# pytest: helps you write better programs.
# https://github.com/pytest-dev/pytest/
# Configuration file: pyproject.toml
pytest:
	@echo "Info **********  Start: pytest **************************************"
	pipenv run pytest --version
	pipenv run pytest --dead-fixtures tests
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered --random-order tests
	@echo "Info **********  End:   pytest **************************************"
pytest_issue:
	@echo "Info **********  Start: pytest **************************************"
	pipenv run pytest --version
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered -m issue --setup-show tests
	@echo "Info **********  End:   pytest **************************************"
pytest_prod:
	@echo "Info **********  Start: pytest **************************************"
	pipenv install pytest
	pipenv install pytest-cov
	pipenv install pytest-deadfixtures
	pipenv install pytest-random-order
	pipenv run pytest --version
	pipenv run pytest --dead-fixtures tests
	pipenv run pytest --cov=src --cov-report term-missing:skip-covered --random-order tests
	@echo "Info **********  End:   pytest **************************************"
