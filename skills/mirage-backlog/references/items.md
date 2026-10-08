# Backlog item format

## Contents

- Files and IDs
- Frontmatter
- Body sections
- Milestone, epic, story and task examples
- Status rules

## Files and IDs

One file per item, directly under `backlog/`, named `<ID>-<slug>.md`. The slug is lowercase words joined by hyphens.

| Level | ID | File name example |
|---|---|---|
| milestone | `M1` | `M1-public-launch.md` |
| epic | `E02` | `E02-checkout.md` |
| story | `M1-E02-S03` | `M1-E02-S03-pay-by-card.md` |
| task | `M1-E02-S03-T01` | `M1-E02-S03-T01-payment-endpoint.md` |

The ID gives the item's milestone, epic and parent, so no other field repeats them. A story needs its milestone file and its epic file to exist, and a task needs its story file.

## Frontmatter

The frontmatter sits between two `---` lines at the top of the file.

- Write one `key: value` per line.
- Lists are inline, as `[a, b]`, and an empty list is `[]`.
- Quote a value with double quotes when it contains a comma or a bracket.
- Nothing is nested, and nothing spans lines.

| Key | Used on | Value |
|---|---|---|
| `id` | all, required | the ID, equal to the start of the file name |
| `title` | all, required | a short imperative or noun phrase |
| `status` | all, required | `draft`, `blocked`, `ready`, `in-progress`, `in-review`, `done`, `cancelled` |
| `kind` | story | `feature` (default), `spike`, `bug`, `chore`, `docs` |
| `priority` | story, required | `urgent`, `high`, `medium`, `low` |
| `scope` | story, required | `must`, `should`, `may` |
| `release` | story, required | a release from `.mirage/project.json` |
| `req` | story | requirement IDs. A feature story needs at least one. |
| `questions` | story, task | question IDs it waits on. A spike story needs at least one, and lists the questions it answers, which do not block it. |
| `inputs` | story, task | input IDs it waits on |
| `blocked_by` | story, task | story or task IDs that must be done first |
| `labels` | story and task required | at least one `area:<area>` from `.mirage/project.json` |
| `lane` | story, task | the owning area when there are several area labels |
| `estimate` | story, task | 1, 2, 3, 5 or 8, only when the owner supplies estimates |
| `evidence` | all, required when done | commit SHA, pull request and CI run |
| `blocked_reason` | all | what blocks the item when no question, input or blocker explains it |
| `replaces` | all | the cancelled item this one replaces |
| `replaced_by` | all | the item that replaces this cancelled one |
| `due` | all | `YYYY-MM-DD`, only from the owner |
| `due_evidence` | all, required with `due` | where the owner set the date |

A task inherits its story's `questions`, `inputs` and `blocked_by`.

## Body sections

A story or task body has these sections. Each starts with its marker comment, followed by a heading in the project's language. The validator reads the markers. A tracker never shows them, because the sync removes them.

| Marker | Section | Required | Holds |
|---|---|---|---|
| `<!-- mirage:section context -->` | Context | yes | Why the item exists, in one to three lines, with its requirement IDs and links to the document sections it implements. |
| `<!-- mirage:section acceptance -->` | Acceptance criteria | yes | A checklist. Each line is testable by someone who did not write the code. |
| `<!-- mirage:section technical -->` | Technical notes | no | Endpoints, tables, configuration keys and files the documents already fix. |
| `<!-- mirage:section verification -->` | Verification | yes | The tests, scenario IDs or exact commands that prove the criteria. |
| `<!-- mirage:section out-of-scope -->` | Out of scope | yes | What the item leaves out, or a sentence saying nothing is excluded. |

A draft or blocked item may leave sections out while they are still unknown. From `ready` onward all four required sections must be written. Milestones and epics have no sections.

## Milestone

```markdown
---
id: M1
title: Public launch
status: in-progress
---

Goal: customers can browse the catalog, pay by card and receive their order confirmation.

Exit criteria:

- [ ] Every MUST requirement for release v1.0 is done.
- [ ] Production monitoring alerts the on-call channel.
```

## Epic

```markdown
---
id: E02
title: Checkout
status: in-progress
---

Everything between a full cart and a confirmed order: addresses, delivery, payment and confirmation. Requirement area: CHK.
```

## Story

```markdown
---
id: M1-E02-S03
title: Pay for an order by card
status: blocked
priority: high
scope: must
release: v1.0
req: [REQ-CHK-004, REQ-PAY-001]
questions: [Q-012]
inputs: [IN-004]
blocked_by: [M1-E02-S02]
labels: [area:backend, area:web]
lane: backend
---

<!-- mirage:section context -->
## Context

A signed-in customer with a full cart pays by card and sees the confirmation page (REQ-CHK-004, REQ-PAY-001). See docs/payments.md, "Payment flows", and docs/specs/web/Checkout.md.

<!-- mirage:section acceptance -->
## Acceptance criteria

- [ ] Given a full cart, when the customer pays with a valid test card, then exactly one paid order exists.
- [ ] Given a declined card, when the customer pays, then the decline reason shows and the cart is kept.
- [ ] Given a payment that timed out, when the customer retries, then the card is charged once.

<!-- mirage:section technical -->
## Technical notes

POST /v1/payments in docs/api.md. Table `payments` in docs/data-model.md.

<!-- mirage:section verification -->
## Verification

Scenarios PAY-T01, PAY-T02 and PAY-T03 in docs/payments.md pass in CI against the provider's test mode.

<!-- mirage:section out-of-scope -->
## Out of scope

Saved cards (REQ-PAY-006, release v1.1).
```

## Task

```markdown
---
id: M1-E02-S03-T01
title: Create the payment endpoint
status: draft
labels: [area:backend]
---

<!-- mirage:section context -->
## Context

POST /v1/payments per docs/api.md, idempotent on the order ID (REQ-PAY-001).

<!-- mirage:section acceptance -->
## Acceptance criteria

- [ ] The endpoint passes the contract tests for docs/api.md.
- [ ] A repeated request with the same idempotency key returns the first result.

<!-- mirage:section verification -->
## Verification

The backend test suite, including the payment contract tests.

<!-- mirage:section out-of-scope -->
## Out of scope

The web checkout screen, which is task T02.
```

## Status rules

| Status | The validator requires |
|---|---|
| `ready` | Every question answered or delegated, every input provided or not needed, every blocker done, the four required sections written with a checklist under acceptance, and requirement links on a feature story. |
| `blocked` | An unmet prerequisite, or `blocked_reason`. |
| `done` | `evidence`, with every task of a story, and every story of an epic or milestone, done or cancelled. |
