<!-- mirage:doc test-strategy -->
# Test strategy

{{One paragraph: which components this project tests, and that every specialist document ends with its own test-scenario table using the ID scheme this document defines.}}

<!-- mirage:section levels -->
## Test levels

{{Name each test level this project runs, such as unit, integration and end-to-end, and what each one must cover for every component. State the minimum a change must add before it can merge, such as a unit test for new logic and an end-to-end test for a new flow.}}

<!-- mirage:section tools -->
## Tools

{{Name the test framework and runner for each component, and any tool that checks types, lints or measures coverage. State the coverage threshold if the project sets one, marked as a hypothesis until a release has actually measured it.}}

<!-- mirage:section environments -->
## Test environments and data

{{Name every environment tests run against, such as local, a CI container or a staging deployment, and which devices, browsers or operating systems from docs/ux.md or docs/platforms/ must be covered. State whether production data may ever be used, and if not, where fixtures and seed data come from.}}

<!-- mirage:section scenarios -->
## Scenario IDs

{{State that every specialist document, such as an integration, a domain rule set or the payments document, ends with a table of test scenarios. State the ID form <AREA>-T<NN>, where AREA is the requirement area code from docs/prd.md's areas table and NN counts up from 01 within that area, for example PAY-T01. State that a scenario this test strategy owns directly, not tied to one specialist document, uses the area TS.}}

| ID | Scenario | Expected |
|---|---|---|
| {{TS-T01}} | {{The situation under test, in one sentence}} | {{What must happen}} |

<!-- mirage:section done -->
## Definition of done

{{State what a story needs before its status can become done: which test levels passed, which scenario IDs it closes, and whether a person must also sign off.}}

<!-- mirage:section evidence -->
## Evidence

{{State what counts as evidence for a passed test, such as a CI run URL, a log file or a recording, tied to the commit SHA it ran against. State that a mock or a stub proves the code runs, never that a live scenario, such as a third-party integration or a payment flow, actually works.}}
