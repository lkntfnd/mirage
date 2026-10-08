---
id: M1-E01-S01-T01
title: Slot and booking endpoints
status: done
labels: [area:backend]
estimate: 3
evidence: merge 9a3d2f1, CI run 198 green
---

<!-- mirage:section context -->
## Context

The server side of the booking story.

<!-- mirage:section acceptance -->
## Acceptance criteria

- [x] Slots endpoint.
- [x] Booking endpoint with an idempotency key.

<!-- mirage:section verification -->
## Verification

API tests T-BOOK-01 and T-BOOK-02.

<!-- mirage:section out-of-scope -->
## Out of scope

Cancelling a booking.
