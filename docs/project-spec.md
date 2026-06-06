# Problem

## Document Control

- Project: Azure RBAC Insight
- Owner: Chinmay Jog
- Last updated: 2026-06-06
- Version: 0.1

## How To Use This File

- Keep scope, goals, and success criteria concrete.
- Reference requirement IDs in architecture and task tracking.
- Update this file when the operating model or target users change.

# Goals

- FR-001: Let an operator inspect RBAC assignments across one or more Azure subscriptions from a single interface.
- FR-002: Support two ingestion modes: live Azure fetch and offline CSV upload.
- FR-003: Make privilege analysis fast through filtering, sorting, and visual summaries.
- NFR-001: Keep runtime local-first so sensitive RBAC data does not need external processing.
- NFR-002: Keep setup simple enough for a user to run locally with Python or Docker in under 10 minutes.

# Non Goals

- The tool does not modify Azure RBAC assignments.
- The tool does not persist customer RBAC data to a remote backend.
- The tool does not replace enterprise identity governance or policy tooling.

# Success Criteria

- Operators can load at least one subscription export or complete a live fetch without code changes.
- Users can filter results by subscription, role, and scope from the dashboard.
- The README and user guide are sufficient for a first-time user to run the tool locally.
- No secrets or tenant-specific credentials are committed to the repository.

# Stakeholders

- Project owner: Chinmay Jog
- Primary users: Cloud platform engineers, security reviewers, auditors
- Secondary users: Contributors extending ingestion, filtering, or analytics

# Assumptions

- Users already have Azure Reader access for subscriptions they inspect.
- Azure CLI authentication is available for live mode.
- CSV exports from Azure Portal remain a supported offline path.

# Risks

- Risk: Azure API or export schema changes break ingestion.
  Mitigation: Keep ingestion logic isolated and validate with sample exports.
- Risk: Large RBAC datasets make the dashboard sluggish.
  Mitigation: Use caching and avoid unnecessary recomputation.
- Risk: Users misinterpret principal IDs from live mode.
  Mitigation: Keep CSV mode documented as the display-name friendly option.

# Scope Summary

- In scope: local dashboard UX, Azure RBAC ingestion, filtering, charts, containerized local run.
- Out of scope: managed hosting, write-back remediation, cross-tenant automation workflows.

# References

- README.md
- HOW_TO_GUIDE.md
- docs/architecture.md
- docs/tasks.md