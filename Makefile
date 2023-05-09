# https://github.com/samuelcolvin/pydantic/blob/master/Makefile
.DEFAULT_GOAL := all
isort = poetry run isort . # tests/
black = poetry run black . # tests/
mypy = poetry run mypy .
flake8  = flake8 . # tests/
pyupgrade = pyupgrade --py310-plus

.PHONY: install-linting
install-linting:
	poetry add flake8 black isort mypy pyupgrade -G lint

.PHONY: install
install: install-linting
	pre-commit install
	@echo 'installed development requirements'

.PHONY: lint
lint: install-linting
	$(isort) --df --check-only
	$(black) --diff --check
	$(flake8)

.PHONY: format
format:
	$(pyupgrade)
	$(isort)
	$(black)
	$(flake8)
	$(mypy)

.PHONY: export-dependencies
export-dependencies:
	poetry export -f requirements.txt --output requirements.txt

.PHONY: all
all: format export-dependencies
