<!-- mirage:doc test-strategy -->
# Test strategy

<!-- mirage:section levels -->
## Test levels

Unit tests for booking rules, API tests for every endpoint, one end-to-end booking flow (Q-004).

<!-- mirage:section tools -->
## Tools

The app and API each use their platform's standard test runner.

<!-- mirage:section environments -->
## Test environments and data

Staging uses synthetic customers only; production data is never copied.

<!-- mirage:section scenarios -->
## Scenario IDs

Scenario IDs run from T-BOOK-01 upward, one range per requirement area.

<!-- mirage:section evidence -->
## Evidence

Evidence is the merged commit SHA with its CI run.
