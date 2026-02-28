# webnovel-paraphrasing

Project skeleton for a local-first webnovel paraphrasing pipeline.

## Quickstart

```bash
uv sync --group dev
PYTHONPATH=src uv run python -m webnovel_paraphraser --help
```

## Make aliases

```bash
make help
make sync
make lint
make test
make tox
make check
make cli
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
