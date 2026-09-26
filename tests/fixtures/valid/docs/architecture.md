<!-- mirage:doc architecture -->
# Architecture

<!-- mirage:section context -->
## System context

A mobile app talks to one booking API, which calls Sprocket Supply for part stock.

<!-- mirage:section components -->
## Components and stack

The app is a cross-platform mobile client; the API is a small web service with one database (Q-002).

<!-- mirage:section data-flows -->
## Data flows

Bookings flow from the app to the API; stock queries flow from the API to Sprocket Supply.

<!-- mirage:section environments -->
## Environments

Local, staging and production, each with its own database.

<!-- mirage:section decisions -->
## Decision index

ADR-0001 records the choice of a single booking API.

<!-- mirage:section repository -->
## Repository layout

One repository with `app/` and `api/` directories.
