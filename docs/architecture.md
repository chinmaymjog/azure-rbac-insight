# Architecture and Decisions

## Document Control

- Project: Azure RBAC Insight
- Owner: Chinmay Jog
- Last updated: 2026-06-06
- Version: 0.1

## How To Use This File

- Explain design decisions for future contributors.
- Keep decisions traceable to requirement IDs in docs/project-spec.md.
- Add an ADR-lite entry when a material design choice changes.

## System Context

### Business and Technical Context

Azure RBAC Insight helps engineers and auditors inspect Azure role assignments without relying on repetitive portal navigation. It supports both connected and disconnected workflows so the same tool can be used in day-to-day operations and in restricted review environments.

### Architecture Goals

- Support live Azure access and offline CSV analysis in the same UI.
- Keep data processing local to reduce security and compliance risk.

## High-Level Design

### Component Overview

| Component | Responsibility | Owner |
| --------- | -------------- | ----- |
| Streamlit UI | Collect inputs, render filters, tables, and charts | Project |
| Azure ingestion layer | Fetch subscriptions, roles, and assignments in live mode | Project |
| CSV ingestion layer | Normalize exported RBAC CSV data for offline use | Project |
| Data shaping layer | Standardize columns and derive chart-ready summaries | Project |

## Data and Control Flow

### Request/Response Flow

1. User chooses live fetch or CSV upload.
2. Data is fetched or loaded into memory.
3. The app normalizes records into a consistent tabular structure.
4. Filters are applied in-memory.
5. Charts and detailed tables are rendered from the filtered dataset.

### State and Data Model Notes

- Streamlit session state preserves user progress between interactions.
- Cached data should be used for expensive fetch or transform paths.
- RBAC data is treated as transient runtime state, not repository state.

### Failure Paths

- Azure auth failures should fail early with a clear message to re-run `az login`.
- CSV schema mismatches should surface actionable guidance rather than stack traces.
- Large data loads should degrade gracefully through cached processing and filtered views.

## Deployment Architecture

### Environments

- Local Python execution
- Local Docker container execution

### Runtime Topology

- Single-process Streamlit app
- Azure CLI / SDK access only in live mode
- No remote application database or service dependency

### Release and Rollback Strategy

- Repository changes follow branch -> PR -> merge workflow.
- Rollback is performed by redeploying or re-running the previous known-good container or commit.

## Security and Compliance

- AuthN/AuthZ model: inherited Azure identity through local Azure CLI or uploaded local files.
- Secret management: no secrets in repo; runtime credentials stay in local user context only.
- Input validation boundaries: uploaded CSVs and Azure API responses must be normalized before rendering.
- Audit/logging requirements: avoid writing RBAC dataset contents to committed artifacts or debug files.

## Observability Strategy

- Logs: local app logs for ingestion and parsing failures.
- Metrics: not currently instrumented.
- Traces: not currently instrumented.
- Alerts/SLOs: not applicable for local-first execution.

## External Dependencies

| Dependency | Purpose | SLA/Risk | Backup Plan |
| ---------- | ------- | -------- | ----------- |
| Azure SDK | Live RBAC retrieval | API/schema drift risk | Use CSV upload mode |
| Azure CLI auth | Local credential source | Login/session expiry | Re-auth with `az login` |
| Streamlit | Dashboard UI runtime | Package/runtime regression | Pin versions and run local smoke test |

## Architecture Decision Records (ADR-lite)

### ADR-001

- ID: ADR-001
- Title: Support dual ingestion modes
- Status: Accepted
- Date: 2026-06-06
- Context: Some users can access Azure live, while others need offline review from exports.
- Decision: Keep both live Azure SDK and CSV upload modes in the same application.
- Requirement links: FR-001, FR-002, NFR-001
- Alternatives considered: live-only dashboard, CSV-only dashboard
- Consequences: More ingestion logic to maintain, but broader operational usability.
- Review trigger: Azure APIs or CSV schemas change materially.

### ADR-002

- ID: ADR-002
- Title: Keep execution local-first
- Status: Accepted
- Date: 2026-06-06
- Context: RBAC exports can contain sensitive permission data.
- Decision: Run analysis locally without a managed backend.
- Requirement links: NFR-001, NFR-002
- Alternatives considered: hosted dashboard with remote storage
- Consequences: Simpler security posture, but limited collaboration features.
- Review trigger: future need for team-shared dashboards.

## Requirement to Design Mapping

| Requirement ID | Architectural Element | ADR ID | Notes |
| -------------- | --------------------- | ------ | ----- |
| FR-001 | Streamlit UI + ingestion layers | ADR-001 | Unified analysis path |
| FR-002 | Azure ingestion and CSV ingestion | ADR-001 | Dual-mode support |
| FR-003 | Data shaping + filterable UI | ADR-001 | Interactive review |
| NFR-001 | Local-first runtime model | ADR-002 | Avoid remote data storage |
| NFR-002 | Local Python and Docker execution | ADR-002 | Fast onboarding |

## Pending Decisions

- Decision needed: whether to add automated tests for ingestion transforms.
- Owner: Chinmay Jog
- Due date: 2026-06-30