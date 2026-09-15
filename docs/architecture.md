# Architecture

## What This Is

A single-file Streamlit dashboard (`app.py`) for reviewing Azure RBAC
role assignments. It supports two ingestion paths into the same
filterable UI: live fetch via the Azure SDK, or an offline CSV export
from the Azure Portal. See the Quick Start in `README.md`.

## How It Works

1. The sidebar's Input Source radio picks live fetch or CSV upload.
2. Live mode calls `get_subscriptions()` then `fetch_all_rbac()`,
   pulling role assignments per subscription via
   `AuthorizationManagementClient` and mapping role definition GUIDs
   to names. CSV mode calls `process_csv()`, which normalizes column
   names and derives a `Subscription` label from the filename when the
   export doesn't already have one.
3. The resulting DataFrame is validated against `REQUIRED_COLUMNS`
   (`Subscription`, `RoleDefinitionName`, `ObjectType`, `ObjectId`) -
   a mismatch shows an actionable error instead of continuing into a
   render that would crash.
4. A `Resource Name` column is derived from `Scope` when present, or
   falls back to `"Unknown"` when it isn't - `Scope` is the one
   optional column, since a CSV export may omit it even though live
   fetch always includes it.
5. Sidebar multiselects filter the DataFrame in place; metrics, two
   Plotly charts, and a detail table render from the filtered result.

## Key Decisions

- **Decision:** Support both live Azure SDK access and offline CSV
  upload in the same app.
  **Why:** Some users can access Azure live; others need offline
  review from an export (restricted environments, point-in-time audit
  snapshots).
  **Revisit if:** One mode turns out to cover the vast majority of
  real usage and the other becomes maintenance overhead.
- **Decision:** Keep execution entirely local - no backend, no remote
  storage of RBAC data.
  **Why:** RBAC exports are sensitive; a local-only tool has a much
  simpler security posture than a hosted one.
  **Revisit if:** Team-shared dashboards become a real need.
- **Decision:** Validate required columns before rendering, rather
  than letting a missing column surface as a `KeyError` mid-render.
  **Why:** A CSV schema mismatch (a different Azure Portal export
  version, a hand-edited file) is a normal, expected failure mode for
  offline mode - it should tell the user what's wrong, not crash.
  **Revisit if:** Azure Portal's export format stabilizes enough that
  this becomes dead code.

## Known Risks / Rough Edges

- No automated tests - `app.py` is a single Streamlit script with no
  test suite. `docs/tasks.md` tracks this as a known gap.
- Live mode's Azure SDK response only includes principal object IDs,
  not display names - CSV mode (which includes `DisplayName` from the
  Portal export) is the better choice when human-readable identity
  names matter.
- Large multi-subscription live fetches run sequentially per
  subscription with no concurrency - fine for a handful of
  subscriptions, slow for dozens.
