# Backlog item format

## Contents

- Files and IDs
- Frontmatter
- Milestone, epic, story and task examples
- Status rules

## Files and IDs

One file per item, directly under `backlog/`, named `<ID>-<slug>.md`. The slug is lowercase words joined by hyphens.

| Level | ID | File name example |
|---|---|---|
| milestone | `M1` | `M1-public-launch.md` |
| epic | `E02` | `E02-checkout.md` |
| story | `M1-E02-S03` | `M1-E02-S03-pay-by-card.md` |
| task | `M1-E02-S03-T01` | `M1-E02-S03-T01-payment-intent-endpoint.md` |

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
| `questions` | story, task | question IDs it waits on. A spike story needs at least one. |
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

A signed-in customer with a full cart pays by card and sees the confirmation page. See docs/payments.md and docs/specs/web/Checkout.md.

- [ ] A test card payment creates exactly one paid order.
- [ ] A declined card shows the decline reason and keeps the cart.
- [ ] Retrying a timed-out payment never charges twice (PAY-T03).

Out of scope: saved cards (REQ-PAY-006, v1.1).
```

## Task

```markdown
---
id: M1-E02-S03-T01
title: Create the payment endpoint
status: draft
labels: [area:backend]
---

POST /v1/payments per docs/api.md, idempotent on the order ID.

- [ ] The endpoint passes the contract tests in docs/api.md.
- [ ] A repeated request with the same idempotency key returns the first result.
```

## Status rules

| Status | The validator requires |
|---|---|
| `ready` | Every question answered or delegated, every input provided or not needed, every blocker done, at least one checklist item, and requirement links on a feature story. |
| `blocked` | An unmet prerequisite, or `blocked_reason`. |
| `done` | `evidence`, with every task of a story, and every story of an epic or milestone, done or cancelled. |
