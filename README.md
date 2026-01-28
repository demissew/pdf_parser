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

## Configuration (env)

```bash
PDF_PARSER_DOCLING_NUM_THREADS=2
PDF_PARSER_DOCLING_DEVICE=cpu
PDF_PARSER_DOCLING_TIMEOUT_S=180
PDF_PARSER_DOCLING_MAX_NUM_PAGES=300
PDF_PARSER_DOCLING_MAX_FILE_SIZE_MB=25
```

## Tests

```bash
uv run pytest
```
