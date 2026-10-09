# Mirage

Mirage interviews a project's owner, writes every document the project needs, and plans the work as a local backlog that agents and people build from. This glossary fixes the words mirage uses in its skills, its generated files and its own docs.

## Interview

**Owner**:
The person who makes product decisions for the project being documented. Only the owner answers questions.
_Avoid_: user, client, stakeholder

**Facet**:
A property of the project that decides which documents and questions apply, such as "takes payments" or "has a command-line tool".
_Avoid_: feature flag, project type

**Component**:
A part of the project that is built and delivered on its own, with an ID and a kind. The kind may be any slug.
_Avoid_: module, app, service

**Custom kind**:
A component kind the catalog has no document of its own for. Its component gets a component specification.
_Avoid_: unknown kind, other

**Project document**:
A document a project declares for itself in `project.json`, with its own outline and question areas, because the catalog has none for the subject.
_Avoid_: custom doc, extra doc

**Question**:
A decision the owner must make, recorded in the register with an ID `Q-nnn`, an agent recommendation and a status.
_Avoid_: ticket, issue

**Recommendation**:
The answer the agent proposes for a question, with its reason. Every question carries one.
_Avoid_: default, suggestion

**Delegated answer**:
An answer the owner accepted from the agent's recommendation without deciding it themselves. It counts as settled and stays marked as delegated so the owner can review it later.
_Avoid_: assumption, auto-answer

**Register**:
The file `docs/questions.md` that holds every question, its recommendation, its answer and its status.
_Avoid_: FAQ, decision log

**Input**:
Information, an asset, an account, access or a tool that the documentation or the build needs from outside the conversation, recorded in `docs/inputs.md` with an ID `IN-nnn`. An input records where the thing lives, never a secret itself.
_Avoid_: requirement, dependency, prerequisite

## Documents

**Catalog**:
The library of document kinds mirage knows, each with the facets that switch it on and the question areas it must cover. A project is not limited to it.
_Avoid_: template list

**Requirement**:
One atomic product obligation in the PRD, with an ID `REQ-<AREA>-<NNN>`, a scope keyword and a target release.
_Avoid_: feature, user story

**Source**:
An input document the project did not write, such as a client brief, preserved unchanged under `docs/sources/` and pinned by hash.
_Avoid_: attachment, reference doc

## Backlog

**Backlog item**:
One milestone, epic, story or task, stored as one Markdown file under `backlog/`. Its ID states its place: `M1`, `E02`, `M1-E02-S03`, `M1-E02-S03-T01`.
_Avoid_: ticket, issue, card

**Task**:
The fourth backlog level, one step of a story.
_Avoid_: subtask, sub-issue

**Canonical backlog**:
The backlog files in the repository. They are the only source of truth for planned work.
_Avoid_: master backlog

**Projection**:
A copy of the canonical backlog in a tracker such as Plane or Jira, kept for people who prefer a board view.
_Avoid_: mirror, sync target, tracker backlog

**Drift**:
A change a person made to a tracker item's title, description, labels or parent that the backlog files do not hold. Mirage reports it before pushing.
_Avoid_: conflict, out-of-sync

**Adapter**:
The instructions that map backlog items onto one tracker's objects and statuses.
_Avoid_: connector, integration

**Ready set**:
The backlog items whose questions are settled, whose inputs are provided and whose blockers are done, so work on them can start now.
_Avoid_: todo list, sprint

## Delivery

**Area**:
A field of work that one lane owns, such as `backend`, `firmware` or `infra`, declared per project and carried on items as an `area:<name>` label.
_Avoid_: component, module

**Lane**:
The area an agent or person picks work from. An item with several areas names its owning lane.
_Avoid_: team, stream, assignee

**Evidence**:
A pointer that proves a claim, such as a commit SHA with its CI run, a test log, or a dated record of a measurement or a delivery. An item is done only with evidence.
_Avoid_: proof, receipt
