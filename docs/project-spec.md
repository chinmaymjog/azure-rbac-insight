# Problem

## What are you building, and why?

Reviewing Azure RBAC permissions at scale is slow and fragmented in
the Azure Portal - there's no single view to see who has access to
what across subscriptions. Azure RBAC Insight is a local Streamlit
dashboard that aggregates role assignments (live via the Azure SDK, or
offline from a CSV export) into one filterable, chartable view.

## Goals

- Let an operator inspect RBAC assignments across one or more Azure
  subscriptions from a single interface.
- Support two ingestion modes: live Azure fetch and offline CSV
  upload.
- Make privilege analysis fast through filtering, sorting, and visual
  summaries.
- Keep runtime local-first so sensitive RBAC data never leaves the
  user's machine.

## Non-Goals

- The tool does not modify Azure RBAC assignments - read-only
  analysis only.
- The tool does not persist RBAC data to a remote backend.
- The tool does not replace enterprise identity governance or policy
  tooling.

## Success Criteria

- Operators can load a subscription export or complete a live fetch
  without code changes.
- Users can filter results by subscription, role, and principal type
  from the dashboard.
- The README and HOW_TO_GUIDE.md are sufficient for a first-time user
  to run the tool locally in under 10 minutes.
- No secrets or tenant-specific credentials are committed to the
  repository.

## Risks

- Azure API or CSV export schema changes break ingestion - mitigated
  by validating required columns up front and showing an actionable
  error instead of a stack trace when a CSV doesn't match.
- Large RBAC datasets make the dashboard sluggish - mitigated with
  `st.cache_data`/`st.cache_resource` on fetch/transform paths.
- Users misinterpret principal IDs from live mode (the Azure SDK only
  returns object IDs, not display names) - CSV mode is documented as
  the display-name-friendly option.

## Notes

- Primary users: cloud platform engineers, security reviewers,
  auditors.
- Live mode needs `az login` and Reader access to the target
  subscription(s); CSV mode needs an Azure Portal role-assignments
  export (see [HOW_TO_GUIDE.md](../HOW_TO_GUIDE.md)).
- `samples/sample-rbac-export.csv` shows the expected CSV shape.
