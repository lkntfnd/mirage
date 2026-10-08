---
name: mirage-backlog
description: Plans a project's milestones, epics, stories and tasks as one local Markdown file each, with IDs like M1-E02-S03-T01, requirement links, acceptance criteria, verification, blockers, area labels for agent lanes, and statuses the validator keeps honest. First checks that the documentation is sufficient to plan from, and goes back to the grilling interview when it is not. Also lists the ready set per lane and replans after scope changes. Use when asked to create or update milestones, epics, stories, tasks or a backlog, to find what can start now, or after mirage-docs and mirage-audit finish.
---

# Mirage backlog

You turn the PRD and the documents into a backlog that agents can pick work from without asking. The files in `backlog/` are the only source of truth. A tracker is a board that `mirage-sync` fills later, and it never replaces the files.

[references/items.md](references/items.md) gives the file format for each level, with examples. Read it before writing the first item.

## 1. Check that the documentation is sufficient

A task written from thin documents carries a guess into every lane that touches it. So before you write or change any item, run:

```
python3 .mirage/check.py docs-ready
```

**When it prints `sufficient`,** read the open questions it lists and go to step 2.

**When it does not,** stop planning and get on the same page with the owner first:

1. Tell the owner in plain words what is missing: which documents, which undecided areas, which broken references.
2. Invoke `mirage-interview` for the missing decisions. It runs the `grilling` interview, scoped to the gaps, with a recommendation on every question. The owner can also start it by typing `/grill-me`, and can delegate any part of it.
3. Invoke `mirage-docs` for the documents that are missing or changed, then `mirage-audit` when no documents audit is recorded or the documents changed since the last one.
4. Run `docs-ready` again. Continue only when it prints `sufficient`.

When `.mirage/` or `docs/prd.md` does not exist at all, the project has not been through mirage. Say so, and offer `/mirage`.

## 2. Put the open questions to the owner

`docs-ready` lists every open question and what it blocks. Open questions do not stop planning, but the owner should choose that knowingly. Before writing items, show the owner the open questions that block requirements of the next release, each with your recommendation, and ask for each one whether to settle it now, delegate it or leave it open. A question whose answer is a figure, a date, a price or a name only the owner knows cannot be delegated. It is settled by the owner or stays open.

Record the outcome in `docs/questions.md`. Stories that depend on a question left open are planned as blocked.

## 3. Read the plan inputs

Read these first:

- `docs/prd.md`, for the requirements, their scopes and releases, and the scope matrix
- `docs/delivery.md`, for the definition of done, the lanes and the working agreements
- `.mirage/project.json`, for the releases and the area labels
- both registers and every planned document
- every existing file in `backlog/`

## 4. Milestones

Each milestone is a delivery step with a goal and checklist exit criteria. Map milestones onto the project's releases. Several milestones may lead up to one release. Add an `M0` foundation milestone when the repository, CI, environments or accounts are not ready yet. Its stories carry the first release in `release`.

Dates come only from the owner. A `due` date needs `due_evidence` naming where the owner set it.

## 5. Epics

Each epic is one capability area that lasts across milestones, usually one per requirement area or product module. An epic's stories may sit in several milestones, such as `M1-E02-S01` and `M2-E02-S01`.

## 6. Stories and tasks

Each story is a vertical slice. It cuts a narrow but complete path through every layer it touches, it can be demonstrated or verified on its own, and one agent session can finish it. Put any preparatory refactor in its own earlier story.

Every story carries:

- `req`: the requirements it delivers. Every requirement that is not OUT must end up in at least one story at or before its release. That holds for later releases too. A story for a later release can stay `draft`, with its `req` and a one-line context, until that release is planned in detail.
- `blocked_by`: the stories or tasks that must be done first, and nothing that does not truly gate it. A story that consumes another lane's work is blocked by the story that provides it. A task inherits its story's blockers, so on a story with tasks in several lanes put each blocker on the task that needs it, not on the story.
- `questions` and `inputs`: the open decisions and missing inputs it waits on.
- At least one `area:` label. An item with several areas names its owning `lane`.

Every story and task body has four sections, each under its marker:

- **Context.** Why the item exists, in one to three lines, with its requirement IDs and links to the document sections it implements.
- **Acceptance criteria.** A checklist. Each line is testable by someone who did not write the code, and the lines together prove the linked requirements. Given, when, then phrasing works well. Include every language, device or performance target the documents require for this item.
- **Verification.** The tests, scenario IDs or exact commands that prove the criteria.
- **Out of scope.** What the item deliberately leaves out, or a sentence saying nothing is excluded.

Add **Technical notes** when the documents already fix endpoints, tables, configuration keys or files.

Split a story into tasks when it spans more than one lane, or is too large for one session. Each task has its own area label and its own four sections.

A spike is a story of kind `spike` that answers a question by trying something. It lists that question in `questions` and sets a timebox in its context. The question does not block the spike, because answering it is the spike's work, so a spike can be ready while its question is open. Its outcome is recorded as that question's answer, plus an ADR when the decision is hard to reverse. The validator rejects a done spike whose question is still open.

When one lane needs something from another, write that need as its own item in the other lane, with the exact shape needed in its context, and add it to the requesting item's `blocked_by`.

## 7. Estimates

Leave `estimate` out unless the owner supplies the estimates or asks you for them. An estimate sits on a story or on its tasks, never on both. Values are 1, 2, 3, 5 or 8, and larger work is split.

## 8. Set honest statuses

1. Write new items as `draft`. Write every item of a milestone before you run `check`, because a `blocked_by` that names an item not yet written is reported as `backlog-ref`.
2. Run `python3 .mirage/check.py ready`. Items listed as "can become ready" have every question settled, every input provided, every blocker done, every required section written and, for a feature story, a requirement linked.
3. Set each of those items to `ready` with `python3 .mirage/check.py set-status <ID> ready`. The command takes several IDs before the status.
4. Set every other planned story and task to `blocked`. Its unmet prerequisites are its reason, or add `blocked_reason` for anything else.
5. Milestones and epics are not picked up as work. Leave each one `draft` while it is planned. Set it to `in-progress` when its first story starts, and to `done`, with evidence, when every story under it is done or cancelled.

Never set `ready` by judgment. The validator rejects a ready item with an unmet prerequisite or a missing section.

## 9. Change the plan without breaking it

- Never renumber or delete an item.
- Work that moves to another milestone is cancelled with `replaced_by`. A new item under the new milestone names it in `replaces`.
- Dropped work is `cancelled`, with the reason in its body.
- A finished item is set with `python3 .mirage/check.py set-status <ID> done --evidence "<commit SHA and CI run>"`.

## Finish

Run `python3 .mirage/check.py index`, then `python3 .mirage/check.py check`. Done when `check` reports no errors, including `coverage-req`.

Report per milestone the number of stories and tasks. Give the ready set per lane from `check.py ready`, and the blocked items with what blocks them. Then run `mirage-audit` on the new items. If the owner wants a board view, `mirage-sync` comes after that.
