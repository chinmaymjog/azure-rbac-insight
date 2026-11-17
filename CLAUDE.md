# azure-rbac-insight

Local-first Streamlit dashboard for reviewing Azure RBAC assignments (live Azure fetch or offline CSV upload). Python, `app.py` is the entrypoint.

## Layout
- `app.py` — Streamlit app
- `tests/` — pytest tests
- `docs/` — `project-spec.md`, `architecture.md`, `tasks.md`; `HOW_TO_GUIDE.md` for export/audit steps

## Working on issues
- Verify before finishing: `pytest tests/ -q`.
- Add or update tests for every bug fix.
- Keep changes minimal and scoped to the issue; one issue per PR.
- Branch names `feature/*`, `bugfix/*` or `hotfix/*`; Conventional Commits (see CONTRIBUTING.md).
- Open a PR against `main` that references the issue (`Fixes #N`). Never push to `main` directly.
- Keep RBAC data processing local-first; never add remote state, telemetry, or hardcoded credentials/tenant IDs.
- Update README/docs when the ingestion flow or user workflow changes.
- Don't touch `.github/workflows/`, `Dockerfile`, or dependency pins unless the issue asks for it.
