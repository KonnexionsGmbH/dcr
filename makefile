.DEFAULT_GOAL := dev

eco_dev: isort black bandit flake8 mypy pylint pydocstyle radon pytest pdoc

inst_dev:  pip pipenv pipenv_dev
inst_prod: pip pipenv pipenv_prod

prod: inst_prod compileall

ifeq ($(OS),Windows_NT)
    export DCR_PDOC_OUT=docs\\api
    export DCR_PDOC_OUT_DEL=if exist ${DCR_PDOC_OUT} rmdir /s /q ${DCR_PDOC_OUT}
    export DCR_SOURCE_PATH=$(dir src\\dcr\\*.py src\\dcr\\*\\*.py)
    export MYPYPATH=src\\dcr
    export PYTHONPATH=src\\dcr
else
    export DCR_PDOC_OUT=docs/api
    export DCR_PDOC_OUT_DEL=rm -rf ${DCR_PDOC_OUT}
    export DCR_SOURCE_PATH=src/dcr/*.py src/dcr/*/*.py
    export MYPYPATH=src/dcr
    export PYTHONPATH=src/dcr
endif

# Bandit is a tool designed to find common security issues in Python code.
# https://github.com/PyCQA/bandit
# Configuration file: none
bandit:
	@echo "Info **********  Start: Bandit **************************************"
	python -m bandit -r src
	@echo "Info **********  End:   Bandit **************************************"

# The Uncompromising Code Formatter
# https://github.com/psf/black
# Configuration file: pyproject.toml
black:
	@echo "Info **********  Start: black ***************************************"
	python -m black src
	@echo "Info **********  End:   black ***************************************"

# Byte-compile Python libraries
# https://docs.python.org/3/library/compileall.html
# Configuration file: none
compileall:
	@echo "Info **********  Start: Compile All Python Scripts ******************"
	python -m compileall
	@echo "Info **********  End:   Compile All Python Scripts ******************"

# Flake8: Your Tool For Style Guide Enforcement.
# includes McCabe:      https://github.com/PyCQA/mccabe
# includes pycodestyle: https://github.com/PyCQA/pycodestyle
# includes Pyflakes:    https://github.com/PyCQA/pyflakes
# https://github.com/pycqa/flake8
# Configuration file: setup.cfg
flake8:
	@echo "Info **********  Start: Flake8 **************************************"
	python -m flake8 src
	@echo "Info **********  End:   Flake8 **************************************"

# isort your imports, so you don't have to.
# https://github.com/PyCQA/isort
# Configuration file: pyproject.toml
isort:
	@echo "Info **********  Start: isort ***************************************"
	python -m isort src
	@echo "Info **********  End:   isort ***************************************"

# Mypy: Static Typing for Python
# https://github.com/python/mypy
# Configuration file: pyproject.toml
mypy:
	@echo "Info **********  Start: MyPy ****************************************"
	@echo MYPYPATH=${MYPYPATH}
	python -m mypy src
	@echo "Info **********  End:   MyPy ****************************************"

# Auto-generate API documentation for Python projects.
# https://github.com/mitmproxy/pdoc
# Configuration file: none
pdoc:
	@echo "Info **********  Start: Create API Documentation ********************"
	@echo DCR_PDOC_OUT_DEL=${DCR_PDOC_OUT_DEL}
	@echo DCR_SOURCE_PATH=${DCR_SOURCE_PATH}
	${DCR_PDOC_OUT_DEL}
	python -m pdoc -o ${DCR_PDOC_OUT} ${DCR_SOURCE_PATH}
	@echo "Info **********  End:   Create API Documentation ********************"

# pip is the package installer for Python.
# https://pypi.org/project/pip/
# Configuration file: none
pip:
	@echo "Info **********  Start: Install and / or Upgrade pip ****************"
	python -m pip install --upgrade pip
	@echo "Info **********  End:   Install and / or Upgrade pip ****************"

# Pipenv: Python Development Workflow for Humans.
# https://github.com/pypa/pipenv
# Configuration file: Pipfile
pipenv:
	@echo "Info **********  Start: Install and Upgrade pipenv ******************"
	python -m pip install pipenv
	python -m pip install --upgrade pipenv
	@echo "Info **********  End:   Install and Upgrade pipenv ******************"
pipenv_dev:
	@echo "Info **********  Start: Installation of Development Packages ********"
	python -m pipenv install --dev
	@echo "Info **********  End:   Installation of Development Packages ********"
pipenv_prod:
	@echo "Info **********  Start: Installation of Production Packages *********"
	python -m pipenv install
	@echo "Info **********  End:   Installation of Production Packages *********"

# pydocstyle - docstring style checker.
# https://github.com/PyCQA/pydocstyle
# Configuration file: pyproject.toml
pydocstyle:
	@echo "Info **********  Start: pydocstyle **********************************"
	python -m pydocstyle --count src
	@echo "Info **********  End:   pydocstyle **********************************"

# Pylint is a tool that checks for errors in Python code.
# https://github.com/PyCQA/pylint/
# Configuration file: pyproject.toml
pylint:
	@echo "Info **********  Start: Pylint **************************************"
	@echo PYTHONPATH=${PYTHONPATH}
	python -m pylint src
	@echo "Info **********  End:   Pylint **************************************"

# pytest: helps you write better programs.
# https://github.com/pytest-dev/pytest/
# Configuration file: pyproject.toml
pytest:
	@echo "Info **********  Start: pytest **************************************"
	python -m pytest
	@echo "Info **********  End:   pytest **************************************"

# Radon is a Python tool which computes various code metrics.
# https://github.com/rubik/radon
# Configuration file: setup.cfg
radon:
	@echo "Info **********  Start: Radon ***************************************"
	python -m radon cc src
	@echo "Info **********  End:   Radon ***************************************"
