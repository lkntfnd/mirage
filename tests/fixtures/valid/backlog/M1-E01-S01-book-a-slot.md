---
id: M1-E01-S01
title: Book a repair slot
status: done
priority: high
scope: must
release: v1.0
req: [REQ-BOOK-001]
labels: [area:mobile, area:backend]
lane: backend
evidence: "merge 4be81c0, CI run 212 green"
---

<!-- mirage:section context -->
## Context

A customer picks a free slot and books it (REQ-BOOK-001).

<!-- mirage:section acceptance -->
## Acceptance criteria

- [x] A customer books a free slot.
- [x] A taken slot cannot be booked twice.

<!-- mirage:section technical -->
## Technical notes

`GET /slots` and `POST /bookings`, see [the API](../docs/api.md).

<!-- mirage:section verification -->
## Verification

API tests T-BOOK-01 and T-BOOK-02; the booking flow in the app test suite.

<!-- mirage:section out-of-scope -->
## Out of scope

Payments; customers pay in the shop.
