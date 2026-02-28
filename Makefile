.PHONY: help sync lint test tox check cli inspect-txt ingest-txt cleanup-runs cleanup-runs-apply precommit-install precommit-run

help:
	@echo "Available targets:"
	@echo "  make sync              - Install/update project + dev dependencies"
	@echo "  make lint              - Run Ruff lint checks"
	@echo "  make test              - Run pytest"
	@echo "  make tox               - Run tox environments"
	@echo "  make check             - Run lint + test"
	@echo "  make cli               - Show project CLI help"
	@echo "  make inspect-txt       - Inspect input/txt_chapters ordering and titles"
	@echo "  make ingest-txt        - Ingest input/txt_chapters into runs/latest/work"
	@echo "  make cleanup-runs      - Preview cleanup of old runs (keeps 3 newest)"
	@echo "  make cleanup-runs-apply - Delete old runs (keeps 3 newest)"
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
	PYTHONPATH=src .venv/bin/python -m webnovel_paraphraser --help

inspect-txt:
	PYTHONPATH=src .venv/bin/python -m webnovel_paraphraser inspect-txt input/txt_chapters

ingest-txt:
	PYTHONPATH=src .venv/bin/python -m webnovel_paraphraser ingest-txt input/txt_chapters --run-id latest

cleanup-runs:
	PYTHONPATH=src .venv/bin/python -m webnovel_paraphraser cleanup-runs --runs-dir runs --keep 3

cleanup-runs-apply:
	PYTHONPATH=src .venv/bin/python -m webnovel_paraphraser cleanup-runs --runs-dir runs --keep 3 --apply

precommit-install:
	uvx pre-commit install

precommit-run:
	uvx pre-commit run --all-files
