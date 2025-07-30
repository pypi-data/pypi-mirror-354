.DEFAULT_GOAL := help

PYTHON := venv/bin/python

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@grep '^[^.#]\+:\s\+.*#' Makefile | \
	  sed "s/\(.\+\):\s*\(.*\) #\s*\(.*\)/`printf "\033[93m"`  \1`printf "\033[0m"`	\3 [\2]/" | \
	  expand -35
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

.PHONY: clean
clean: # Remove all builds and Python artifacts
	find wagtail_cblocks tests \
	  \( -name '*.py[co]' -o -name '__pycache__' \) -exec rm -rf {} +
	rm -rf build dist .eggs *.egg-info

.PHONY: test
test: # Run tests quickly with the current Python
	$(PYTHON) -m pytest --cov --cov-report=term:skip-covered

.PHONY: test-wip
test-wip: # Run tests marked as wip with the current Python
	$(PYTHON) -m pytest -vv -m 'wip' --pdb

.PHONY: test-all
test-all: # Run tests on all Django and Wagtail versions
	tox

.PHONY: lint
lint: # Check the Python code syntax and style
	@$(PYTHON) -m ruff check
	@$(PYTHON) -m ruff format --check --quiet

.PHONY: format
format: # Format and fix the Python code syntax
	$(PYTHON) -m ruff check --fix
	$(PYTHON) -m ruff format

.PHONY: release
release: dist # Package and upload a release
	$(PYTHON) -m twine upload dist/*

.PHONY: dist
dist: clean # Build source and wheel package
	$(PYTHON) -m build
