# Repository Guidelines

## Project Structure & Module Organization
- `app/main.py` creates the FastAPI app and wires routes/config.
- `app/api/routes.py` defines `/parse` and `/health` endpoints.
- `app/services/parser.py` wraps Docling conversion.
- `app/core/config.py` centralizes environment-driven settings.
- `main.py` is a thin launcher for local runs.
- `deploy/systemd/pd_parser.service` is the production unit file.
- `tests/` holds test modules.
- `pyproject.toml` defines runtime dependencies; `uv.lock` pins them.

## Build, Test, and Development Commands
- `python main.py` starts the FastAPI server on port 29999.
- `uvicorn app.main:app --reload --port 29999` is the explicit dev command.
- Dependency install: use `uv sync --all-extras` (preferred) or any tool that honors `pyproject.toml`.
- `uv run pytest` runs the test suite.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation.
- Use `snake_case` for functions and variables; `CapWords` for class names.
- Keep FastAPI routes small and focused; move reusable logic into helpers if it grows.
- No formatter or linter is configured; keep changes minimal and readable.

## Testing Guidelines
- Tests live in `tests/` and use `pytest`.
- Name test files `test_*.py`.
- Add or update tests when API behavior changes (e.g., `/parse` or `/health`).

## Commit & Pull Request Guidelines
- There is no existing Git history, so no established commit convention.
- Use clear, imperative commit subjects (e.g., "Add PDF conversion endpoint").
- PRs should include: a short summary, how you ran the app locally, and any new dependencies.
- Include example requests/responses if API behavior changes.

## Configuration & Data Notes
- Temp files are written to `PDF_PARSER_TEMP_DIR` (default `/tmp/pdf_parser`).
- `/parse` accepts either a multipart PDF file or a URL; it returns Markdown only.
- Be mindful of large files and conversion time when changing parsing behavior.

## Deployment Notes
- GitHub Actions runs tests and deploys to Ubuntu via SSH.
- Systemd expects the app at `/opt/pdf_parser` with a virtualenv in `/opt/pdf_parser/.venv`.
- Required secrets: `SSH_HOST`, `SSH_USER`, `SSH_KEY`.
