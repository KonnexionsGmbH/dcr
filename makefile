.DEFAULT_GOAL := dev

dev: inst_dev qual api_doc
prod: inst_prod compile

inst_dev: pip pipenv install_dev
inst_prod: pip pipenv install_prod

qual: isort black bandit mypy pycodestyle pyflakes pylint pydocstyle mccabe radon

export PYTHONPATH=src/dcr

# https://pdoc3.github.io/pdoc/
api_doc:
	@echo "Info **********  Start: Create API Documentation ********************"
	pdoc3 -o docs/api --force --skip-errors src/dcr/dcr.py
	pdoc3 -o docs/api --force --skip-errors src/dcr/db/schema.py
	pdoc3 -o docs/api --force --skip-errors src/dcr/inbox/document.py
	pdoc3 -o docs/api --force --skip-errors src/dcr/utils/environ.py
	@echo "Info **********  End:   Create API Documentation ********************"

# https://github.com/PyCQA/bandit
bandit:
	@echo "Info **********  Start: Bandit **************************************"
	bandit -r src/*/*
	@echo "Info **********  End:   Bandit **************************************"

# https://github.com/psf/black
black:
	@echo "Info **********  Start: black ***************************************"
	black --line-length 79 src
	@echo "Info **********  End:   black ***************************************"

# https://docs.python.org/3/library/compileall.html
compile:
	@echo "Info **********  Start: Compile All Python Scripts ******************"
	python -m compileall
	@echo "Info **********  End:   Compile All Python Scripts ******************"

# https://pipenv.pypa.io/en/latest/
install_dev:
	@echo "Info **********  Start: Installation of Development Packages ********"
	pipenv install --dev
	@echo "Info **********  End:   Installation of Development Packages ********"

# https://pipenv.pypa.io/en/latest/
install_prod:
	@echo "Info **********  Start: Installation of Production Packages *********"
	pipenv install
	@echo "Info **********  End:   Installation of Production Packages *********"

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
	mypy --ignore-missing-imports --install-types src/*/*
	@echo "Info **********  End:   MyPy ****************************************"

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

# https://github.com/PyCQA/pycodestyle
pycodestyle:
	@echo "Info **********  Start: pycodestyle *********************************"
	pycodestyle --show-pep8 --show-source src/*/*
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

# https://radon.readthedocs.io/en/latest/
radon:
	@echo "Info **********  Start: Radon ***************************************"
	radon cc -s src/*/*
	@echo "Info **********  End:   Radon ***************************************"
