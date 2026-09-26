---
name: mirage-backlog
description: Plans a project's milestones, epics, stories and tasks as one local Markdown file each, with IDs like M1-E02-S03-T01, requirement links, acceptance criteria, blockers, area labels for agent lanes, and statuses the validator keeps honest. Also lists the ready set per lane and replans after scope changes. Use when asked to create or update milestones, epics, stories, tasks or a backlog, to find what can start now, or after mirage-docs finishes.
---

# Mirage backlog

You turn the PRD and the documents into a backlog that agents can pick work from without asking. The files in `backlog/` are the only source of truth. A tracker is a view that `mirage-sync` fills later.

[references/items.md](references/items.md) gives the file format for each level, with examples. Read it before writing the first item.

## 1. Read the plan inputs

Read these first:

- `docs/prd.md`, for the requirements, their scopes and releases, and the scope matrix
- `.mirage/project.json`, for the releases and the area labels
- both registers
- the planned documents
- every existing file in `backlog/`

When `docs/prd.md` does not exist, the backlog has nothing to trace to. Tell the owner, and offer `mirage-interview` and `mirage-docs` first.

## 2. Milestones

Each milestone is a delivery step with a goal and checklist exit criteria. Map milestones onto the project's releases. Add an `M0` foundation milestone when the repository, CI, environments or accounts are not ready yet.

Dates come only from the owner. A `due` date needs `due_evidence` naming where the owner set it.

## 3. Epics

Each epic is one capability area that lasts across milestones, usually one per requirement area or product module. An epic's stories may sit in several milestones, such as `M1-E02-S01` and `M2-E02-S01`.

## 4. Stories

Each story is a vertical slice. It cuts a narrow but complete path through every layer it touches, it can be demonstrated or verified on its own, and one agent session can finish it. Put any preparatory refactor in its own earlier story.

Every story carries:

- `req`: the requirements it delivers. Every requirement that is not OUT must end up in at least one story at or before its release.
- Acceptance criteria as a checklist, each item testable by someone who did not write the code.
- `blocked_by`: the stories or tasks that must be done first, and nothing that does not truly gate it.
- `questions` and `inputs`: the open decisions and missing inputs it waits on.
- At least one `area:` label. An item with several areas names its owning `lane`.

Split a story into tasks when it spans more than one lane, or is too large for one session. Each task has its own area label.

## 5. Estimates

Leave `estimate` out unless the owner supplies the estimates or asks you for them. An estimate sits on a story or on its tasks, never on both. Values are 1, 2, 3, 5 or 8, and larger work is split.

## 6. Set honest statuses

1. Write new items as `draft`.
2. Run `python3 .mirage/check.py ready`. Items listed as "can become ready" have every question settled, every input provided, every blocker done and acceptance criteria.
3. Set each of those items to `ready` with `python3 .mirage/check.py set-status <ID> ready`.
4. Set every other planned item to `blocked`. Its unmet prerequisites are its reason, or add `blocked_reason` for anything else.

Never set `ready` by judgment. The validator rejects a ready item with an unmet prerequisite.

## 7. Change the plan without breaking it

- Never renumber or delete an item.
- Work that moves to another milestone is cancelled with `replaced_by`. A new item under the new milestone names it in `replaces`.
- Dropped work is `cancelled`, with the reason in its body.
- A finished item is set with `python3 .mirage/check.py set-status <ID> done --evidence "<commit SHA and CI run>"`.

## Finish

Run `python3 .mirage/check.py index`, then `python3 .mirage/check.py check`. Done when `check` reports no errors, including `coverage-req`.

Report per milestone the number of stories and tasks. Give the ready set per lane from `check.py ready`, and the blocked items with what blocks them. If the owner wants a board view, the next phase is `mirage-sync`.
