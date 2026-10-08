---
id: M1-E02-S01
title: Check part stock
status: in-progress
priority: high
scope: must
release: v1.0
req: [REQ-PART-001]
inputs: [IN-001]
labels: [area:backend]
---

<!-- mirage:section context -->
## Context

A mechanic checks a part before promising a repair date (REQ-PART-001).

<!-- mirage:section acceptance -->
## Acceptance criteria

- [ ] A mechanic sees stock for a part number.

<!-- mirage:section verification -->
## Verification

API test T-PART-01 against the supplier sandbox.

<!-- mirage:section out-of-scope -->
## Out of scope

Ordering parts.
