<!-- mirage:doc delivery -->
# Delivery conventions

This document fixes how planned work is written, tracked and finished in this project. The files in `backlog/` are the plan, and the project uses no tracker (Q-013).

<!-- mirage:section levels -->
## Backlog levels and IDs

Every item is one Markdown file in `backlog/`, named `<ID>-<slug>.md`. A milestone is `M1`, an epic `E02`, a story `M1-E02-S01` and a task `M1-E02-S01-T01`. Items are never renumbered; replaced work is cancelled with `replaced_by`.

<!-- mirage:section statuses -->
## Statuses

Items move through draft, blocked, ready, in-progress, in-review, done and cancelled. Change one with `python3 .mirage/check.py set-status`.

<!-- mirage:section ready -->
## Definition of ready

An item is ready when its questions are answered, its inputs are provided, its blockers are done and its body holds every required section. A feature story links a requirement.

<!-- mirage:section done -->
## Definition of done

An item is done when its acceptance checklist is ticked and its evidence names the merged commit and a green CI run. The booking screens are also checked on one phone of each platform (Q-013).

<!-- mirage:section labels -->
## Labels and lanes

| Area label | Builds | Owned paths |
|---|---|---|
| area:mobile | The booking app | `app/` |
| area:backend | The API | `api/` |

<!-- mirage:section template -->
## Item template

A story or task body has these sections, each starting with a marker comment and followed by a heading:

```markdown
<!-- mirage:section context -->
## Context

<!-- mirage:section acceptance -->
## Acceptance criteria

- [ ] ...

<!-- mirage:section verification -->
## Verification

<!-- mirage:section out-of-scope -->
## Out of scope
```

Technical notes are optional.

<!-- mirage:section requests -->
## Requests between lanes

A lane that needs something from the other writes a draft item with the other lane's area label and lists it in its own `blocked_by`. The API contract in `docs/api.md` is the contract between the lanes.

<!-- mirage:section tracker -->
## Tracker projection

The project uses no tracker (Q-013); the backlog files are the only board.

<!-- mirage:section agreements -->
## Working agreements

Each lane has at most two stories in progress. Work is estimated in points on either a story or its tasks. A spike lasts at most two days (Q-013).
