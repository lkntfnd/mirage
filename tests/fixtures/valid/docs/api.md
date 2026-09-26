<!-- mirage:doc api -->
# API

<!-- mirage:section consumers -->
## Consumers

The mobile app is the only consumer (Q-009).

<!-- mirage:section conventions -->
## Conventions

JSON over HTTPS with snake_case fields.

<!-- mirage:section auth -->
## Authentication

A session token issued after the one-time code.

<!-- mirage:section errors -->
## Errors

Errors return a code and a message; clients switch on the code.

<!-- mirage:section pagination -->
## Pagination

My bookings is paginated with a cursor.

<!-- mirage:section idempotency -->
## Idempotency

Creating a booking takes an idempotency key.

<!-- mirage:section versioning -->
## Versioning

The path carries the major version.

<!-- mirage:section limits -->
## Rate limits

Ten booking attempts per phone number per hour.

<!-- mirage:section endpoints -->
## Endpoint inventory

Slots, bookings and stock, each listed in the contract file.

<!-- mirage:section contract -->
## Contract file

The contract file is `api/openapi.yaml`.
