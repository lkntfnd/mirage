---
status: accepted
---

# Interviews, glossary and ADRs come from Matt Pocock's skills

Mirage requires the `mattpocock-skills` plugin and calls its `grilling` skill for the owner interview and its `domain-modeling` skill for `CONTEXT.md` and `docs/adr/`. Mirage adds only what those skills lack: persisting answers in a register, coverage by project facet, the full document set, the backlog, the validator and tracker projections. Writing a second interview skill would duplicate maintained work.

Decided by the owner on 2026-09-26.

## Consequences

- Mirage adopts the upstream file conventions: `CONTEXT.md` at the root and `docs/adr/NNNN-slug.md`.
- `grill-me` is user-invoked only, so mirage calls `grilling` directly.
- Upstream tags are `v1.2.3`, not the `mattpocock-skills--v<version>` form Claude Code needs to resolve a version range. The dependency is unversioned, and the official marketplace pins it to a reviewed commit. A contract check must fail loudly when `grilling` changes shape.
- The dependency comes from `claude-plugins-official`, so mirage's `marketplace.json` lists that marketplace in `allowCrossMarketplaceDependenciesOn`.
