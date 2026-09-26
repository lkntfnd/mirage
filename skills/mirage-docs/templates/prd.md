<!-- mirage:doc prd -->
# Product requirements

{{One paragraph: what the product is, who it serves and what this document fixes. Name the governing sources and say that docs/questions.md holds every open decision.}}

<!-- mirage:section summary -->
## Product summary

{{Two or three paragraphs: the problem, the people who have it, the product's answer, and why it is worth building now. Cite questions as (Q-nnn) where an answer shaped the text.}}

<!-- mirage:section users -->
## Users and roles

| Role | Who they are | What they can do |
|---|---|---|
| {{Role name}} | {{One sentence}} | {{The capabilities this role has, in plain words}} |

<!-- mirage:section releases -->
## Releases and scope

{{One sentence per release naming what it adds. The release names must match the releases in .mirage/project.json.}}

| Module | {{Release 1}} | {{Release 2}} |
|---|---|---|
| {{Module name}} | {{MUST, SHOULD, MAY or OUT}} | {{MUST, SHOULD, MAY or OUT}} |

<!-- mirage:section metrics -->
## Success metrics

| Metric | Target | Measured by | By |
|---|---|---|---|
| {{What is measured}} | {{Number with unit}} | {{Tool or method}} | {{Release or date from the register}} |

<!-- mirage:section areas -->
## Requirement areas

| Code | Name |
|---|---|
| {{AREA}} | {{Area name}} |

<!-- mirage:section requirements -->
## Requirements

{{One subsection per area, in the order of the areas table. Each requirement is one testable obligation. IDs are REQ-<AREA>-<NNN>, never renumbered; a withdrawn requirement keeps its row with scope OUT. Scope uses MUST, SHOULD, MAY or OUT. Release is a project release, or "-" for OUT.}}

### {{Area name}}

| ID | Requirement | Scope | Release |
|---|---|---|---|
| REQ-{{AREA}}-001 | {{The product must ...}} | {{MUST}} | {{v1.0}} |

<!-- mirage:section out-of-scope -->
## Out of scope

{{A list of what the product will not do, each with the question or reason that excluded it. Deferred work that should stay possible later is a requirement with scope OUT, plus a note on what keeps it possible.}}
