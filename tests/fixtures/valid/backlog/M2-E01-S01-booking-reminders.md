---
id: M2-E01-S01
title: Booking reminders
status: blocked
priority: high
scope: must
release: v1.1
req: [REQ-NOTE-001]
questions: [Q-012]
inputs: [IN-002]
labels: [area:mobile, area:backend]
lane: mobile
replaces: M1-E01-S04
---

<!-- mirage:section context -->
## Context

A reminder cuts the number of missed slots (REQ-NOTE-001).

<!-- mirage:section acceptance -->
## Acceptance criteria

- [ ] A customer receives one reminder the day before the slot.

<!-- mirage:section verification -->
## Verification

App test T-NOTE-01 with a stubbed push service.

<!-- mirage:section out-of-scope -->
## Out of scope

SMS reminders.
