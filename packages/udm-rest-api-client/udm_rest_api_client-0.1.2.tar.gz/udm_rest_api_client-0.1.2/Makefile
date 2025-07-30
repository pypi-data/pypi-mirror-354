.PHONY: clean clean-pyc clean-build
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re
import sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc ## remove all build and Python artifacts

clean-build:
	hatch clean || true
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr '{}' +
	find . -name '*.egg' -exec rm -fr '{}' +

clean-pyc:
	find . -name '*.pyc' -exec rm -f '{}' +
	find . -name '*.pyo' -exec rm -f '{}' +
	find . -name '*~' -exec rm -f '{}' +
	find . -name '__pycache__' -exec rm -fr '{}' +

lint: ## This checks python files modified by you.
	{ git diff --name-only; git ls-files --others --exclude-standard; git diff --cached --name-only; } | xargs pre-commit run --files

lint-all: ## This checks all python files in the repository
	pre-commit run -a

format: ## This formats all changed python files.
	-{ git diff --name-only; git ls-files --others --exclude-standard; git diff --cached --name-only; } | xargs pre-commit run --hook-stage manual ucr-autopep8 --files
	-{ git diff --name-only; git ls-files --others --exclude-standard; git diff --cached --name-only; } | xargs pre-commit run --hook-stage manual ucr-ruff-fix --files
	-{ git diff --name-only; git ls-files --others --exclude-standard; git diff --cached --name-only; } | xargs pre-commit run --hook-stage manual ruff-fix --files
	-{ git diff --name-only; git ls-files --others --exclude-standard; git diff --cached --name-only; } | xargs pre-commit run --hook-stage manual isort-fix --files
	-{ git diff --name-only; git ls-files --others --exclude-standard; git diff --cached --name-only; } | xargs pre-commit run --hook-stage manual autopep8-fix --files

format-all: ## This formats all python files in the repository
	-pre-commit run -a --hook-stage manual ucr-autopep8
	-pre-commit run -a --hook-stage manual ucr-ruff-fix
	-pre-commit run -a --hook-stage manual ruff-fix
	-pre-commit run -a --hook-stage manual isort-fix
	-pre-commit run -a --hook-stage manual autopep8-fix

build: clean ## builds source and wheel package
	hatch build

publish: build ## package and upload a release to pypi
	hatch publish

publish-test: build ## package and upload a release to the pypi test site
	hatch publish -r test

install-hatch:  ## install 'hatch' using 'pipx'
	apt install pipx
	pipx install hatch
