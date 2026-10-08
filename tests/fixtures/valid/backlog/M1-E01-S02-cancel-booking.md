---
id: M1-E01-S02
title: Cancel a booking
status: ready
priority: medium
scope: should
release: v1.0
req: [REQ-BOOK-002]
questions: [Q-007]
blocked_by: [M1-E01-S01]
labels: [area:mobile, "type:feature"]
estimate: 2
---

<!-- mirage:section context -->
## Context

A customer who cannot come frees the slot for someone else (REQ-BOOK-002).

<!-- mirage:section acceptance -->
## Acceptance criteria

- [ ] A customer cancels up to two hours before the slot.
- [ ] A later cancellation is refused with a reason.

<!-- mirage:section verification -->
## Verification

API test T-BOOK-03 and the cancel flow in the app test suite.

<!-- mirage:section out-of-scope -->
## Out of scope

Refunds; the app takes no payments.
