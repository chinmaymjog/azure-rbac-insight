# Tasks

Keep this short and current. Delete finished work you don't need a
record of - this is a working list, not an audit log.

## Now

- [ ] ...

## Next

- [ ] Add automated smoke test for local startup (validate the
      Streamlit boot path).
- [ ] Add export/reporting view for filtered results - useful for
      audit handoff.

## Done

- [x] Fixed a `KeyError` crash when an uploaded CSV is missing
      `Subscription`/`RoleDefinitionName`/`ObjectType`/`ObjectId` -
      now shows an actionable error and stops instead of crashing
      mid-render; a missing `Scope` (optional) now degrades to
      `Resource Name = "Unknown"` instead of crashing three sections
      later (2026-09-15)
- [x] Fixed the Roles filter silently showing all roles when every
      role was deselected, inconsistent with how the Subscriptions
      and Principal Types filters behave (2026-09-15)
- [x] Fixed a broken README link pointing at an absolute local
      filesystem path instead of a relative one (2026-09-15)
- [x] De-bloated `docs/project-spec.md`/`docs/architecture.md` to a
      lightweight format (2026-09-15)
