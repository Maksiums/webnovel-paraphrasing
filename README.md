# webnovel-paraphrasing

Project skeleton for a local-first webnovel paraphrasing pipeline.

## Quickstart

```bash
uv sync --group dev
make cli
```

## Preferred Workflow (`make`)

Use `make` targets as the default interface for day-to-day commands.

```bash
make help
make sync
make lint
make test
make tox
make check
make cli
make inspect-txt
make ingest-txt
make cleanup-runs          # dry-run preview
make cleanup-runs-apply    # actually delete old runs
make precommit-install
make precommit-run
```

## Tooling

```bash
uv run ruff check .
PYTHONPATH=src uv run pytest
uv run tox
uvx pre-commit run --all-files
```
