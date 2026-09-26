<!-- mirage:doc architecture -->
# Architecture

{{One paragraph: name every component in .mirage/project.json and what this document fixes about how they fit together. Say that docs/questions.md holds every open decision about the stack, hosting or data flow, and that an unresolved number, date or vendor becomes a question there rather than an invented one.}}

<!-- mirage:section context -->
## System context

{{One paragraph: the people and external systems that interact with the product, drawn from docs/prd.md's users and roles, and the systems already in place that this project must reuse or connect to. State the load the system must handle at launch and a year later, marking any target a hypothesis until an owner confirms it, and record an unconfirmed access need as an input in docs/inputs.md with ID IN-nnn.}}

<!-- mirage:section components -->
## Components and stack

{{One row per component in .mirage/project.json. Name the language, framework and runtime for each, and call out any choice the owner mandated or forbade. Record hosting account ownership here, or note it is unresolved and belongs in docs/questions.md as (Q-nnn).}}

| Component | Kind | Stack | Hosted on | Account owner |
|---|---|---|---|---|
| {{component id}} | {{component kind, such as website or backend-service}} | {{language, framework, runtime}} | {{provider or environment}} | {{who holds the account}} |

<!-- mirage:section data-flows -->
## Data flows

{{One row per flow that crosses a component or system boundary. Name what data moves, not just that data moves, cite the REQ-<AREA>-<NNN> requirement each flow serves where one exists, and say which flows carry personal data or payment data so docs/security.md can classify them.}}

| Flow | From | To | Data | Trigger |
|---|---|---|---|---|
| {{Flow name}} | {{Source component or system}} | {{Destination component or system}} | {{What moves}} | {{What starts the flow}} |

<!-- mirage:section environments -->
## Environments

{{One row per environment the project runs, such as local, staging and production. State what differs between them, such as data, secrets or scale, and which environment each release targets.}}

| Environment | Purpose | Differs from production by |
|---|---|---|
| {{Environment name}} | {{What it is for}} | {{The differences}} |

<!-- mirage:section decisions -->
## Decision index

{{One row per architecture decision record under docs/adr/. Keep this table in ID order and add a row the day a new ADR is written, never renumbering an existing one.}}

| ID | Title | Status |
|---|---|---|
| ADR-{{0001}} | {{Decision title}} | {{proposed, accepted or superseded}} |

<!-- mirage:section repository -->
## Repository layout

{{One paragraph naming whether the project keeps one repository or several, followed by a table mapping each top-level directory to the component it holds. Name the lane that owns each path when the project splits work by area.}}

| Path | Component | Owning lane |
|---|---|---|
| {{Directory}} | {{Component id}} | {{Area from .mirage/project.json, or "-" with one lane}} |
