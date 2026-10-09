<!-- mirage:doc test-strategy -->
# Test strategy

{{One paragraph: which components this project tests, and that every specialist document ends with its own test-scenario table using the ID scheme this document defines.}}

<!-- mirage:section levels -->
## Test levels

{{Name each test level this project runs and what each one must cover for every component. For software these are levels such as unit, integration and end-to-end. For anything else, name the checks that play the same parts, such as an inspection, a bench measurement and a trial with a real user. State the minimum a change must add before it can merge, such as a unit test for new logic and an end-to-end test for a new flow.}}

<!-- mirage:section tools -->
## Tools

{{Name the test framework and runner for each component, and any tool that checks types, lints or measures coverage. State the coverage threshold if the project sets one, marked as a hypothesis until a release has actually measured it.}}

<!-- mirage:section environments -->
## Test environments and data

{{Name every environment tests run against, such as local, a CI container, a staging deployment or a test bench, and which devices, browsers, operating systems or equipment must be covered, from docs/ux.md, docs/platforms/ or the component specifications. State whether production data may ever be used, and if not, where fixtures and seed data come from.}}

<!-- mirage:section scenarios -->
## Scenario IDs

{{State that every specialist document, such as an integration, a domain rule set or the payments document, ends with a table of test scenarios. State the ID form <AREA>-T<NN>, where AREA is the requirement area code from docs/prd.md's areas table and NN counts up from 01 in one sequence per area across every document, for example PAY-T01, so two documents that share an area never reuse a number. State that a scenario about a requirement area takes that area's code wherever it is written, and that TS is only for a scenario that belongs to no requirement area.}}

| ID | Scenario | Expected |
|---|---|---|
| {{TS-T01}} | {{The situation under test, in one sentence}} | {{What must happen}} |

<!-- mirage:section evidence -->
## Evidence

{{State what counts as evidence for a passed test, such as a CI run URL, a log file or a recording, tied to the commit SHA it ran against. For a check no pipeline can run, such as a measurement or a trial build, state the dated record that is committed instead and what it must hold. State that a mock or a stub proves the code runs, never that a live scenario, such as a third-party integration or a payment flow, actually works.}}
