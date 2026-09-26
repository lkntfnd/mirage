<!-- mirage:doc api -->
# API

{{One paragraph: which component this API belongs to, who calls it, and what this document fixes. Say the contract file named in the Contract file section below is the source of truth for every endpoint, and that an unresolved choice becomes a question in docs/questions.md.}}

<!-- mirage:section consumers -->
## Consumers

{{State which clients call this API, such as the mobile app, a partner integration or a public developer, and which of those consumers this project does not control. Note any consumer whose release cadence lags the API, since that consumer limits how fast a breaking change can ship. Cite the requirement that names each consumer as REQ-<AREA>-NNN.}}

<!-- mirage:section conventions -->
## Conventions

{{State the API style, such as REST, GraphQL or gRPC, the base URL pattern, and the request and response encoding. State the naming convention for resources and fields, and the date and time format every endpoint uses.}}

<!-- mirage:section auth -->
## Authentication

{{State how a caller proves its identity, such as a bearer token, an API key or mutual TLS, and how the API checks what that caller may do. Name which roles or scopes exist and which endpoints each one reaches. An unresolved choice of provider or token lifetime becomes a question in docs/questions.md rather than an invented default.}}

<!-- mirage:section errors -->
## Errors

{{Describe the error envelope every failed call returns and the status codes clients are told to branch on. State which error codes are part of the contract and must not change without a version bump, and which are free to evolve.}}

<!-- mirage:section pagination -->
## Pagination

{{State the pagination style, such as cursor or offset, the parameter and response field names, and the default and maximum page size. Mark the maximum as a hypothesis to confirm under load rather than a fixed number if it has not been measured.}}

<!-- mirage:section idempotency -->
## Idempotency

{{List which write operations must be safe to retry, citing each as REQ-<AREA>-NNN, and how a caller marks a retry, such as an idempotency key header. State how long the API remembers a key and what it returns for a repeated call.}}

<!-- mirage:section versioning -->
## Versioning

{{State how the version is carried, such as a URL segment or a header, what counts as a breaking change, and how long a deprecated version keeps working before removal. Cite the question that settled the deprecation window as (Q-nnn) where one exists.}}

<!-- mirage:section limits -->
## Rate limits

{{State the rate limit per caller or per key, the window it resets on, and the response when a caller exceeds it. Mark the limit as a hypothesis until it is measured against real traffic, and cite the input that supplies a production number as (IN-nnn) where one applies.}}

<!-- mirage:section endpoints -->
## Endpoint inventory

{{List every endpoint the first release ships, one row per endpoint, in the order the requirements introduce them. The Requirements column cites the REQ-<AREA>-NNN each endpoint satisfies. This table is a summary; the contract file below governs when the two disagree.}}

| Method | Path | Purpose | Auth | Requirements |
|---|---|---|---|---|
| {{GET}} | {{/v1/resource}} | {{One sentence}} | {{Bearer token or none}} | {{REQ-<AREA>-NNN}} |

<!-- mirage:section contract -->
## Contract file

{{Name the exact path of the machine-readable contract, for example {{docs/openapi.yaml}}, and state that it is the source of truth for the endpoint inventory above. State that the contract is versioned in the same commit as the code it describes, and that a contract test blocks a merge that would let them drift.}}
