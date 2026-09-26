<!-- mirage:doc security -->
# Security

{{One paragraph: what the product handles that makes it a target, citing docs/architecture.md's data flows, and what this document fixes about protecting it. Say that docs/questions.md holds every open decision about authorization and testing, and that an unresolved date or vendor becomes a question there rather than an invented one.}}

<!-- mirage:section assets -->
## Assets and data classification

{{One row per asset, meaning data or a capability that would hurt most if leaked, altered or lost. Classify each by sensitivity and name the REQ-<AREA>-<NNN> requirement or data flow it comes from.}}

| Asset | Classification | Comes from |
|---|---|---|
| {{Asset name}} | {{public, internal, confidential or restricted}} | {{REQ-<AREA>-<NNN> or a data flow from docs/architecture.md}} |

<!-- mirage:section threats -->
## Threats

{{One paragraph per credible threat: who might attack or abuse the product, what they would target from the assets table above, and how. Cite the requirement or role from docs/prd.md that creates the exposure.}}

<!-- mirage:section controls -->
## Controls

{{One row per control that closes a threat above, plus a statement of how access is decided for each role and resource from docs/prd.md's roles. State the control that exists today, never one merely planned, and mark a gap as a question in docs/questions.md as (Q-nnn).}}

| Threat | Control | Owner |
|---|---|---|
| {{Threat from the table above}} | {{What stops or limits it}} | {{Role or person responsible}} |

<!-- mirage:section secrets -->
## Secrets management

{{One row per secret the product depends on: where it lives, who can read it and how often it rotates. Never write a secret's value here, only its location and rotation rule, and record a missing secret as an input in docs/inputs.md with ID IN-nnn.}}

| Secret | Where it lives | Who can read it | Rotation |
|---|---|---|---|
| {{Example: database password}} | {{Example: the hosting provider's secret store}} | {{Example: the backend lane}} | {{Example: every 90 days}} |

<!-- mirage:section supply-chain -->
## Dependency and secret scanning

{{One paragraph: which tool scans dependencies for known vulnerabilities and which tool scans commits for leaked secrets, on which event each runs, and what blocks a merge when either finds something. Name the CI service from docs/operations.md.}}

<!-- mirage:section incidents -->
## Incident response

{{One paragraph: who responds to a security incident, how they are reached outside normal hours, and who must be told, including any owner or authority with a legal deadline. Name the security testing required before launch, such as a penetration test, and record its date as a question in docs/questions.md as (Q-nnn) instead of inventing one.}}
