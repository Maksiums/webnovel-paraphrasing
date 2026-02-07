.PHONY: help sync lint test tox check cli precommit-install precommit-run

help:
	@echo "Available targets:"
	@echo "  make sync              - Install/update project + dev dependencies"
	@echo "  make lint              - Run Ruff lint checks"
	@echo "  make test              - Run pytest"
	@echo "  make tox               - Run tox environments"
	@echo "  make check             - Run lint + test"
	@echo "  make cli               - Show project CLI help"
	@echo "  make precommit-install - Install git pre-commit hook"
	@echo "  make precommit-run     - Run pre-commit on all files"

sync:
	uv sync --group dev

lint:
	uv run ruff check .

test:
	PYTHONPATH=src uv run pytest

tox:
	uv run tox

check: lint test

cli:
	PYTHONPATH=src uv run python -m webnovel_paraphraser --help

precommit-install:
	uvx pre-commit install

precommit-run:
	uvx pre-commit run --all-files
