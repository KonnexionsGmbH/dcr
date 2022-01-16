.DEFAULT_GOAL := install

pip:
	python -m pip install --upgrade pip
.PHONY:pip

pipx: pip
	python -m pip install pipx
.PHONY:pipx

pipenv: pipx
	python -m pip install pipenv
.PHONY:pipenv

install: pipenv
    pipenv shell
	pipenv --bare install
.PHONY:install
