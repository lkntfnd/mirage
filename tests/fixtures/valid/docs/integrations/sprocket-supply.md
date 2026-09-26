<!-- mirage:doc integration:sprocket-supply -->
# Integration

<!-- mirage:section purpose -->
## Purpose and requirements

Sprocket Supply, an invented parts wholesaler, answers stock queries for REQ-PART-001 (Q-011).

<!-- mirage:section contract -->
## Contract

A REST endpoint returns stock per part number.

<!-- mirage:section auth -->
## Authentication

An API key held in the secret store; its location is recorded as IN-001.

<!-- mirage:section limits -->
## Limits and quotas

Sixty requests per minute.

<!-- mirage:section mapping -->
## Data mapping

Part numbers map one to one onto the shop's parts list.

<!-- mirage:section failures -->
## Failure handling

When the supplier is down, the mechanic sees stock as unknown.

<!-- mirage:section scenarios -->
## Test scenarios

T-PART-01 checks a part in stock; T-PART-02 checks a supplier timeout.
