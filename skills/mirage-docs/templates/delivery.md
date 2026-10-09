<!-- mirage:doc delivery -->
# Delivery conventions

{{One paragraph: this document fixes how planned work is written, tracked and finished in this project, for people and agents alike. The files in backlog/ are the plan. Name the tracker that shows them as a board, or say the project uses none.}}

<!-- mirage:section levels -->
## Backlog levels and IDs

Every item is one Markdown file in `backlog/`, named `<ID>-<slug>.md`. The ID states where the item sits and never changes.

| Level | ID | Meaning |
|---|---|---|
| Milestone | `M<n>` | A delivery step with a goal and exit criteria. |
| Epic | `E<nn>` | A capability area that lasts across milestones. |
| Story | `M<n>-E<nn>-S<nn>` | A vertical slice that one session can finish and someone can verify. |
| Task | `M<n>-E<nn>-S<nn>-T<nn>` | One step of a story, usually in a single lane. |

Work that moves to another milestone is cancelled with `replaced_by`, and a new item names it in `replaces`. No item is renumbered or deleted.

The generated index, `backlog/README.md`, lists every milestone and epic with its items.

<!-- mirage:section statuses -->
## Statuses

| Status | Meaning |
|---|---|
| `draft` | Being written. Not yet startable. |
| `blocked` | Waits on an open question, a missing input, an unfinished blocker or a stated reason. |
| `ready` | Meets the definition of ready. Work can start now. |
| `in-progress` | Someone is working on it. |
| `in-review` | The work is finished and awaits review, merge or evidence. |
| `done` | Meets the definition of done, with evidence recorded. |
| `cancelled` | Dropped or replaced, with the reason in its body. |

Stories and tasks are the work that gets picked up. A milestone or an epic stays `draft` while it is planned, becomes `in-progress` when its first story starts, and becomes `done` when every story under it is done or cancelled.

Change a status with `python3 .mirage/check.py set-status <ID> <status>`. Run `python3 .mirage/check.py ready` to see what can start in each lane.

<!-- mirage:section ready -->
## Definition of ready

An item is ready when all of these hold. The validator enforces them.

- Every question it depends on is answered or delegated in docs/questions.md.
- Every input it needs is provided in docs/inputs.md.
- Every item in its `blocked_by` is done.
- Its body states its context, acceptance criteria, verification and out of scope.
- A feature story links at least one requirement.

{{Add any project rule on top, such as "a screen story needs its design delivered" or "an API story needs its endpoints in the contract file". Cite the question that set each rule.}}

<!-- mirage:section done -->
## Definition of done

An item is done when its acceptance criteria are met and its `evidence` names what proves it: the commit and its CI run, or for work no pipeline can check, the dated record committed to the repository. A story is done only when every task under it is done or cancelled.

{{List what else done means in this project, from the answers in docs/questions.md: who reviews, where the change must be deployed, on which devices or in which languages it is verified, which analytics or documents must be updated. Each line is checkable by someone who did not do the work.}}

<!-- mirage:section labels -->
## Labels and lanes

Every story and task carries at least one `area:<name>` label. The area is the lane that does the item's work. An item with several areas names its owning `lane`. The label decides who builds an item, and the plan sets no assignee in the tracker.

| Area label | Does | Owned paths |
|---|---|---|
| area:{{area}} | {{What this lane builds or looks after}} | {{Paths this lane may edit, including the documents of its own parts}} |

{{Name who may edit the files no lane owns: the registers, shared documents and automation files.}}

Stories also carry a kind (`feature`, `spike`, `bug`, `chore` or `docs`), a scope (`must`, `should` or `may`), a release and a priority (`urgent`, `high`, `medium` or `low`). In the tracker these appear as `type:`, `scope:` and `release:` labels.

<!-- mirage:section template -->
## Item template

A story or task body has these sections. Each starts with a marker comment that the validator reads and the tracker never shows. The marker is followed by a heading in the project's language.

| Section | Marker key | Holds |
|---|---|---|
| Context | `context` | Why the item exists, in one to three lines, with its requirement and document links. |
| Acceptance criteria | `acceptance` | A checklist. Each line is testable by someone who did not write the code. Given, when, then phrasing is welcome. |
| Technical notes | `technical` | Optional. Endpoints, tables, configuration keys and files the work touches. |
| Verification | `verification` | The tests, scenario IDs or commands that prove the criteria. |
| Out of scope | `out-of-scope` | What the item deliberately leaves out, or a sentence saying nothing is excluded. |

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

Blockers, questions and inputs go in the frontmatter, never in prose.

<!-- mirage:section requests -->
## Requests between lanes

When one lane needs something from another, it writes a draft item with the other lane's area label and adds that item to its own `blocked_by`. The request states:

- the requirement and document section that call for it
- the exact shape needed, such as a request and response
- its acceptance criteria
- how the requester will verify it

The owning lane picks it up like any other item. Lanes never edit each other's paths.

{{Name the contract between this project's lanes, such as the API contract file, and who may change it.}}

<!-- mirage:section tracker -->
## Tracker projection

{{Name the tracker and the project that show this backlog, citing the question that chose them, or state that the project uses no tracker.}}

The files in `backlog/` are the only source of truth. The tracker is a board for people who prefer one.

- Each tracker item's title starts with the backlog ID, and its description ends with `mirage-id: <ID>`.
- Only status comes back from the tracker into the files. A tracker "done" needs evidence before the file says done.
- A title, description, label or parent changed in the tracker is reported as drift and replaced on the next push, unless someone copies the change into the file first.
- Comments and anything else people add in the tracker are never touched.
- Nothing is ever deleted in the tracker.

<!-- mirage:section agreements -->
## Working agreements

{{State each agreement with the question that set it. Cover how many stories one lane may have in progress at once, how a bug is filed and linked to the story it affects, how long a spike may run and where its outcome is recorded, whether work is estimated and in which unit, and when work may move between milestones.}}

Every session ends by running `python3 .mirage/check.py ready` and setting the status of each item it lists under "can become ready".
