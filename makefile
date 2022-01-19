.DEFAULT_GOAL := dev

dev: inst_dev qual pdoc3
prod: inst_prod compileall

inst_dev: pip pipenv pipenv_dev
inst_prod: pip pipenv pipenv_prod

qual: isort black bandit mypy pycodestyle pyflakes pylint pydocstyle mccabe radon pytest

export PYTHONPATH=src/dcr

# https://github.com/PyCQA/bandit
bandit:
	@echo "Info **********  Start: Bandit **************************************"
	bandit -r src/*/*
	@echo "Info **********  End:   Bandit **************************************"

# https://github.com/psf/black
black:
	@echo "Info **********  Start: black ***************************************"
	black src
	@echo "Info **********  End:   black ***************************************"

# https://docs.python.org/3/library/compileall.html
compileall:
	@echo "Info **********  Start: Compile All Python Scripts ******************"
	python -m compileall
	@echo "Info **********  End:   Compile All Python Scripts ******************"

# https://github.com/PyCQA/isort
isort:
	@echo "Info **********  Start: isort ***************************************"
	isort src/*/*
	@echo "Info **********  End:   isort ***************************************"

# https://github.com/PyCQA/mccabe
mccabe:
	@echo "Info **********  Start: McCabe **************************************"
	python3 -m mccabe src/dcr/*.py src/*/*.py
	@echo "Info **********  End:   McCabe **************************************"

# http://mypy-lang.org
mypy:
	@echo "Info **********  Start: MyPy ****************************************"
	mypy  src/*/*
	@echo "Info **********  End:   MyPy ****************************************"

# https://pdoc3.github.io/pdoc/
pdoc3:
	@echo "Info **********  Start: Create API Documentation ********************"
	pdoc -o docs/api --force --skip-errors src/dcr/dcr.py
	pdoc -o docs/api --force --skip-errors src/dcr/db/schema.py
	pdoc -o docs/api --force --skip-errors src/dcr/inbox/document.py
	pdoc -o docs/api --force --skip-errors src/dcr/utils/environ.py
	@echo "Info **********  End:   Create API Documentation ********************"

# https://pypi.org/project/pip/
pip:
	@echo "Info **********  Start: Install and / or Upgrde pip *****************"
	python -m pip install --upgrade pip
	@echo "Info **********  End:   Install and / or Upgrde pip *****************"

# https://pipenv.pypa.io/en/latest/
pipenv:
	@echo "Info **********  Start: Install and Upgrde pipenv *******************"
	python -m pip install pipenv
	python -m pip install --upgrade pipenv
	@echo "Info **********  End:   Install and Upgrde pipenv *******************"
pipenv_dev:
	@echo "Info **********  Start: Installation of Development Packages ********"
	pipenv install --dev
	@echo "Info **********  End:   Installation of Development Packages ********"
pipenv_prod:
	@echo "Info **********  Start: Installation of Production Packages *********"
	pipenv install
	@echo "Info **********  End:   Installation of Production Packages *********"

# https://github.com/PyCQA/pycodestyle
pycodestyle:
	@echo "Info **********  Start: pycodestyle *********************************"
	pycodestyle src/*/*
	@echo "Info **********  End:   pycodestyle *********************************"

# https://github.com/PyCQA/pydocstyle
pydocstyle:
	@echo "Info **********  Start: pydocstyle **********************************"
	pydocstyle --count src/*/*
	@echo "Info **********  End:   pydocstyle **********************************"

# https://github.com/PyCQA/pyflakes
pyflakes:
	@echo "Info **********  Start: PyFlakes ************************************"
	pyflakes src/*/*
	@echo "Info **********  End:   PyFlakes ************************************"

# https://www.pylint.org
pylint:
	@echo "Info **********  Start: Pylint **************************************"
	@echo PYTHONPATH=${PYTHONPATH}
	pylint src/*/*
	@echo "Info **********  End:   Pylint **************************************"

# https://docs.pytest.org/en/6.2.x/
pytest:
	@echo "Info **********  Start: pytest **************************************"
	pytest
	@echo "Info **********  End:   pytest **************************************"

# https://radon.readthedocs.io/en/latest/
radon:
	@echo "Info **********  Start: Radon ***************************************"
	radon cc -s src/*/*
	@echo "Info **********  End:   Radon ***************************************"
