---
status: accepted
---

# Backlog IDs encode milestone, epic, story and task, and never change

Every backlog item's ID states where it sits: `M1` is a milestone, `E02` an epic, `M1-E02-S03` a story in milestone M1 under epic E02, and `M1-E02-S03-T01` a task of that story. Teams move through the plan milestone by milestone, and branch names and commit subjects that carry the full ID make every change self-describing. Epics span milestones, so `M0-E02-S01` and `M1-E02-S01` are different stories of the same epic.

Decided by the owner on 2026-09-26.

## Consequences

- The ID is the only record of an item's milestone, epic and parent. There is no separate field that could disagree with it.
- Work that moves to another milestone is not renumbered. The old item is cancelled with `replaced_by`, and the new item names it in `replaces`.
- Mirage calls the fourth level a task. It never calls it a subtask, even when a tracker does.
