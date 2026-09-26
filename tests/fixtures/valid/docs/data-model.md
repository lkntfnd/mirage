<!-- mirage:doc data-model -->
# Data model

<!-- mirage:section entities -->
## Entities

Customer, Booking, Slot and Service (Q-009).

<!-- mirage:section storage -->
## Storage

One relational database.

<!-- mirage:section constraints -->
## Constraints

A slot holds at most one booking.

<!-- mirage:section migrations -->
## Migrations

Forward-only migrations run on deploy.

<!-- mirage:section retention -->
## Retention

Bookings older than two years are deleted.
