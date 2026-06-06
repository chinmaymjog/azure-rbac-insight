# Task Tracker

## Document Control

- Project: Azure RBAC Insight
- Owner: Chinmay Jog
- Last updated: 2026-06-06
- Version: 0.1

## How To Use This File

- Track current work only.
- Keep each task tied to requirement IDs from docs/project-spec.md.
- Record validation evidence for completed work.

## Current Focus

- Theme: Repository alignment and maintainability
- Current objective: Bring the project in line with shared engineering-system repo practices.
- This week target: Standardize docs and repo hygiene without changing app behavior.

## Now (Do First)

| ID | Task | Requirement IDs | Owner | Verification | Status |
| -- | ---- | --------------- | ----- | ------------ | ------ |
| T-001 | Add standard project docs set for scope, architecture, and tasks | NFR-002 | Human+AI | Files present under docs/ | Done |
| T-002 | Align repo hygiene and contribution workflow with engineering standards | NFR-001, NFR-002 | Human+AI | README, CONTRIBUTING.md, and .gitignore updated | Done |

## Next (Queue)

| ID | Task | Requirement IDs | Verification | Notes |
| -- | ---- | --------------- | ------------ | ----- |
| T-003 | Add lightweight validation for CSV schema handling | FR-002 | Test command or manual sample run | Reduce ingestion regression risk |
| T-004 | Document troubleshooting for Azure live fetch failures | FR-001, NFR-002 | HOW_TO_GUIDE.md update | Improve first-run experience |

## Later (Backlog)

| ID | Task | Requirement IDs | Notes |
| -- | ---- | --------------- | ----- |
| T-005 | Add automated smoke test for local startup | NFR-002 | Validate Streamlit boot path |
| T-006 | Add export or reporting view for filtered results | FR-003 | Useful for audit handoff |

## Done

| ID | Completed On | Requirement IDs | Validation Evidence | Notes |
| -- | ------------ | --------------- | ------------------- | ----- |
| T-001 | 2026-06-06 | NFR-002 | docs/project-spec.md, docs/architecture.md, docs/tasks.md added | Repo alignment work |
| T-002 | 2026-06-06 | NFR-001, NFR-002 | README.md, CONTRIBUTING.md, .gitignore updated | Standardized repo hygiene |

## Blocked

| ID | Blocker | Owner | Mitigation | Next Check |
| -- | ------- | ----- | ---------- | ---------- |
| T-... |  |  |  | YYYY-MM-DD |