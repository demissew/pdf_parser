## Install dependencies

Preferred (uses lockfile):

```bash
uv sync --all-extras --frozen
```

Alternative (resolves without lockfile):

```bash
uv sync --all-extras
```

## Run locally

```bash
uvicorn app.main:app --reload --port 29999
```

## Tests

```bash
uv run pytest
```
