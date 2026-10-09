<!-- mirage:doc component:{{item}} -->
# Component: {{Component name}}

{{One paragraph: name the component by its ID from .mirage/project.json and its kind, say in plain words what kind of thing it is, and say what this document fixes. Say that an unsettled choice becomes a question in docs/questions.md rather than an invented one.}}

<!-- mirage:section purpose -->
## Purpose and scope

{{State what this component is for and who or what uses it. Cite the requirements it serves as REQ-<AREA>-NNN. Then list what it deliberately does not do, so no reader assumes it.}}

<!-- mirage:section interfaces -->
## Interfaces

{{One row per thing that crosses this component's boundary: data, files, signals, commands, events or physical connections. Name what sits on the other side, another component by its ID or an outside system or person. Give the exact format, protocol, connector or unit, and point to the document that defines it when one exists.}}

| Interface | Direction | Other side | Form | Defined in |
|---|---|---|---|---|
| {{Name}} | {{in, out or both}} | {{Component ID, system or role}} | {{Format, protocol, connector or unit}} | {{Document and section, or "here"}} |

<!-- mirage:section environment -->
## Environment and constraints

{{State where this component runs or exists: the platforms, hardware, materials, standards and versions it must work with. Then list the limits imposed from outside, such as size, power, memory, cost, licences or regulations, each with the question or requirement that set it.}}

<!-- mirage:section design -->
## Design

{{Describe the main parts inside this component and how they fit together, the state or data it holds, and where that lives. Cite each decision that is already fixed as ADR-NNNN or (Q-nnn). Keep to what a builder needs before starting, and leave detail the work itself will settle to the backlog.}}

<!-- mirage:section build -->
## Build and delivery

{{State how this component is produced from its sources, with which tools and versions, and the exact commands or steps once they exist. Then state how it is packaged, versioned and delivered to the people or systems that use it, and who may release it. Before the tooling exists, write the planned steps, cite the question that chose the tooling, and mark them as planned.}}

<!-- mirage:section quality -->
## Quality targets

{{One row per measurable target this component must meet, such as speed, accuracy, reliability, tolerance or cost. Status is "decided" with its question as (Q-nnn) when the owner set the value, "hypothesis" when it is a starting guess, or "measured" once a release has measured it.}}

| Target | Value | Unit | Measured how | Status |
|---|---|---|---|---|
| {{What is measured}} | {{Number}} | {{Unit}} | {{Tool or method}} | {{decided (Q-nnn), hypothesis or measured}} |

<!-- mirage:section verification -->
## Verification

{{State how someone proves this component works, and what that takes: equipment, test data, environments or other people, citing inputs as (IN-nnn). Then add one row per behaviour and per quality target above, using the ID form <AREA>-T<NN> from docs/test-strategy.md.}}

| ID | Scenario | Expected |
|---|---|---|
| {{AREA}}-T01 | {{The situation under test, in one sentence}} | {{What must happen}} |

<!-- mirage:section risks -->
## Risks and unknowns

{{List what is most likely to go wrong or is least understood about this component, and for each one how it will be found out early, such as a spike, a prototype or a measurement. Cite the open question as (Q-nnn). Write "None known" only when the owner confirmed it.}}
