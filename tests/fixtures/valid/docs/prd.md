<!-- mirage:doc prd -->
# Product requirements

<!-- mirage:section summary -->
## Product summary

Customers of Hollow Lane Cycles book a repair slot from their phone instead of calling the shop (Q-001).

<!-- mirage:section users -->
## Users and roles

Customers book and cancel slots. Mechanics see the day's bookings and check part stock.

<!-- mirage:section releases -->
## Releases and scope

v1.0 ships booking and stock checks. v1.1 adds reminders.

<!-- mirage:section metrics -->
## Success metrics

Half of all bookings arrive through the app within three months of v1.0 (Q-001).

<!-- mirage:section areas -->
## Requirement areas

| Code | Name |
|---|---|
| BOOK | Booking |
| NOTE | Notifications |
| PART | Parts |

<!-- mirage:section requirements -->
## Requirements

| ID | Requirement | Scope | Release |
|---|---|---|---|
| REQ-BOOK-001 | A customer books a repair slot from the app. | MUST | v1.0 |
| REQ-BOOK-002 | A customer cancels a booking up to two hours before the slot. | SHOULD | v1.0 |
| REQ-NOTE-001 | The app reminds the customer one day before the slot. | MUST | v1.1 |
| REQ-PART-001 | A mechanic checks part stock at Sprocket Supply. | MUST | v1.0 |
| `REQ-PART-002` | The API reorders parts automatically. | OUT | - |

<!-- mirage:section out-of-scope -->
## Out of scope

The app does not take payments; customers pay in the shop.
