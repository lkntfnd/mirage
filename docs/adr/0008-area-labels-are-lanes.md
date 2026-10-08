---
status: accepted
---

# Area labels, not assignees, decide who builds an item

Each project declares its areas, such as `mobile`, `backend` and `infra`. Every story and task carries at least one `area:<name>` label, and an item with more than one names its owning `lane`. An agent or person picks up only items in its lane. Mirage does not use tracker assignees, because agents are not tracker users and one agent often owns a whole area.

Decided by the owner on 2026-09-26.

## Consequences

- Status is the only field that flows back from a tracker into the files. A title, description, label or hierarchy edit made in a tracker is drift. Mirage reports it before pushing, and the owner chooses for each item whether to copy the change into the file or let the push replace it.
- Mirage writes each tracker item's title, description, labels, parent, milestone, priority, estimate, due date, status and blocking links, and nothing else. Comments, attachments and assignees that people add on the board are never changed.
