---
status: accepted
---

# The catalog is a library of known documents, not a boundary on what a project can be

Mirage documents whatever the owner is building. A component may have any kind. A kind the catalog knows switches on that kind's documents, and a component of any other kind gets a component specification with fixed question areas. A project can also plan a catalog document by name, and can declare documents the catalog does not have, each with its own outline and question areas. The interview starts from what is being built, and it ends by asking what this project must write down that the plan still lacks.

The first design checked every component's kind against eleven kinds, so a project made of anything else could not be described, and every planned document came from the catalog. The owner asked on 2026-10-09 that mirage not be bound to particular kinds of project. The mechanism here is the agent's design from that request.

## Considered options

- **Drop the kinds and derive every document from the interview.** Rejected. The catalog's fixed question areas are what make the depth repeatable and let the validator say when the interview is complete.
- **Open the kinds and nothing else.** Rejected. A part of an unknown kind would be accepted and then never asked about.
- **Open the kinds and add project-defined documents, with no component specification.** Rejected. How deep an unknown kind is documented would depend on what the agent thought to declare.

## Consequences

- `project.json` accepts any slug as a component's kind. A mistyped catalog kind is no longer an error. It shows up in `plan` as a component specification where the specialist documents were expected.
- `include` plans a catalog document that no facet switches on, so a part of an unknown kind can still use the catalog's documents, such as UX for a kiosk.
- `documents` declares a project's own documents. Each needs sections and question areas, so it is covered and checked like a catalog document. It has no template, and `mirage-docs` writes it from its declared outline.
- The documents every project gets (requirements, architecture, security, tests, operations, delivery, agent rules) stay fixed. A section that does not apply says so with a reason.
- A catalog kind earns its place only when its documents fit. `embedded` planned an app-distribution document for firmware, so it was removed, and firmware gets a component specification.
