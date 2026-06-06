# Contributing

Use this repository to evolve a local-first RBAC analysis tool without weakening security, clarity, or end-user usability.

## Workflow

1. Create a short-lived branch from `main` using `feature/*`, `bugfix/*`, or `hotfix/*`.
2. Keep the branch focused on one dashboard, ingestion, or documentation improvement.
3. Use Conventional Commits such as `feat: add scope hotspot chart` or `docs: update csv export guide`.
4. Validate the affected local run, Docker run, or data flow before opening a Pull Request.
5. Open a Pull Request with summary, testing performed, and screenshots if the UI changed.

## Repo-Specific Guidance

- Support both live Azure fetch and offline CSV upload paths.
- Keep RBAC data processing local-first and avoid introducing remote state unnecessarily.
- Use `st.session_state` and caching where needed to keep the UI responsive.
- Keep visuals and naming aligned with the README end-user flow.

## Guardrails

- Do not commit directly to `main`.
- Do not hardcode credentials, tokens, or tenant-specific secrets.
- Keep dependency changes intentional and documented.
- Update README and docs when ingestion flow or user workflow changes.

## Validation

Before opening a Pull Request:

- run `streamlit run app.py` and verify the UI loads
- validate live Azure fetch when relevant using `az login`
- validate CSV upload when relevant using a sample export
- run `docker-compose up --build` when container behavior changes
- review the diff for scope and secret safety

## Documentation Updates

- Update `HOW_TO_GUIDE.md` when export or audit steps change.
- Update `docs/project-spec.md` when scope or success criteria change.
- Update `docs/architecture.md` when a non-trivial design decision is introduced.
- Update `docs/tasks.md` when tracked work starts or finishes.
