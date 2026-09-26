# Mirage design

Status: accepted by the owner in two interview rounds on 2026-09-26. The exact file formats and rules live in [validator.md](validator.md). The full document list lives in [catalog.md](catalog.md), which is generated from the catalog data.

## Contents

1. What mirage produces
2. Skills and flow
3. Facets
4. Catalog
5. Interview
6. Registers
7. Backlog
8. Validator
9. Tracker projection
10. Audit
11. Evaluation
12. Build order

## 1. What mirage produces

Mirage writes into the project it documents. After a full run the project holds this layout.

```
AGENTS.md                  agent operating rules, canonical for every agent
CLAUDE.md                  one line, @AGENTS.md
CONTEXT.md                 glossary, owned by domain-modeling
docs/
  README.md                generated index, reading order, open work
  questions.md             every question, recommendation and answer
  inputs.md                every piece of information, asset, account, access or tool still needed
  prd.md                   requirements REQ-<AREA>-<NNN>
  <catalog docs>.md        only the documents the facets require
  adr/NNNN-slug.md         decisions, owned by domain-modeling
  specs/<component>/       one spec per screen or page
  integrations/<system>.md one spec per external system
  domain/<topic>.md        one spec per complex rule set
  platforms/<kind>.md      one per mobile, desktop, extension, embedded or game component kind
  sources/                 preserved inputs and SHA256SUMS, when there are any
backlog/
  README.md                generated index by milestone and epic
  <ID>-<slug>.md           one file per milestone, epic, story and task
.mirage/
  project.json             facets, language, releases, areas, settings
  check.py, catalog.json   vendored validator and catalog, stamped with the mirage version
  trackers/<name>.json     local ID to tracker ID map, one file per tracker
```

The validator is copied into the project because the project's CI must run it on machines where mirage is not installed.

## 2. Skills and flow

| Skill | Invocation | Job |
|---|---|---|
| `mirage` | user (`/mirage`) | Sets up `.mirage/`, checks that `grilling` and `domain-modeling` are available, reads the project state and runs the next phase. |
| `mirage-interview` | model | Settles facets, then asks every question the catalog requires for them through `grilling`, and records answers and inputs as they land. |
| `mirage-docs` | model | Writes or updates each planned document from its template, the registers and the codebase. |
| `mirage-backlog` | model | Plans milestones, epics, stories and tasks as local files and keeps statuses honest. Usable on its own when docs already exist. |
| `mirage-audit` | model | Runs the validator, then reviews the docs adversarially in a fresh context. |
| `mirage-sync` | model | Projects the backlog into a tracker and pulls status back. |

The router is user-invoked, so it costs no context until someone types `/mirage`. The five phase skills are model-invoked. The router must be able to call them, and a request such as "plan milestones for this repo" should reach `mirage-backlog` directly.

A new project runs interview, docs, backlog and audit, then optionally sync. A later change runs the same phases on the delta only. In an existing codebase the agent reads the code and existing docs first, because finding facts is its job, and the interview asks only what they cannot answer.

## 3. Facets

The first interview round settles `.mirage/project.json`:

- the project name
- the document language, English by default
- the components, each with a kind: website, web-app, mobile-app, desktop-app, browser-extension, backend-service, cli, library, data-pipeline, embedded or game
- the flags, each true or false: accounts, personal data, payments, content edited by non-developers, several languages, analytics, notifications, search, offline use, realtime updates, AI features, admin tools, migration from an existing system, source documents to preserve
- three lists: third-party integrations, regulated regimes, and complex rule sets that need their own spec
- the release names in order
- the area labels that name the lanes, such as `mobile`, `backend` and `infra`

Every later question and document hangs off these answers.

## 4. Catalog

The catalog is data in `skills/mirage/scripts/catalog.json`. It holds 37 document kinds. For each kind it names:

- the facet that switches it on
- its path
- the sections its file must carry
- the question areas the interview must cover
- the inputs it typically needs

[catalog.md](catalog.md) renders it for reading. `check.py plan` prints the documents a given project needs and why, so the skills never keep their own copy.

Specialist documents (integration, domain, payments, search and the like) share one shape. They open with the scope and the requirements they serve, state the contract, mark every tunable value as a hypothesis, name the admin controls, and end with a test-scenario table.

Each document kind has a template in `skills/mirage-docs/templates/`. A template carries the section markers and headings, fixed tables where structure matters, and `{{...}}` guidance. The validator rejects any leftover `{{`, so an unfinished document cannot pass. Markers are HTML comments, so they work in any document language.

## 5. Interview

`mirage-interview` calls `grilling` and `domain-modeling` and adds these rules on top.

1. **Coverage.** The design tree starts from the facets. Each planned document contributes its question areas as branches. The interview is complete when every area of every planned document is named by at least one question in the register. The validator checks this.
2. **Persistence.** Each answer goes into `docs/questions.md` the moment it is settled, never in a batch.
3. **Delegation.** At any point the owner can say "use your recommendations" for one question, the current round, one document or everything left. The agent records each accepted recommendation as a delegated answer, dated. It never fills a question silently. A delegated answer unblocks work at once, and the index lists every one of them for later confirmation.
4. **Inputs.** For each planned document the interview asks about its typical inputs and records what is missing in `docs/inputs.md`, with how to get it.
5. **No invention.** Estimates, dates, prices, accounts and approvals come only from the owner or from evidence. Anything else becomes an open question.

When a question needs someone outside the conversation, the interview keeps it open with that person as its owner. It suggests `to-questionnaire`, which only the owner can start, to send such questions out.

## 6. Registers

`docs/questions.md` holds one section per question: status (`open`, `answered` or `delegated`), the areas it covers, what it blocks, the agent's recommendation and the dated answer. `docs/inputs.md` holds one section per input: status (`missing`, `provided` or `not-needed`), kind, what needs it, how to get it and where it lives. An input records a location, never a secret. [validator.md](validator.md) section 5 gives both formats.

## 7. Backlog

Each item is one Markdown file in `backlog/`, named by its ID (ADR 0007).

| Level | ID |
|---|---|
| milestone | `M1` |
| epic | `E02` |
| story | `M1-E02-S03` |
| task | `M1-E02-S03-T01` |

The ID alone gives an item's milestone, epic and parent. Work that moves to another milestone is cancelled and replaced by a new item. Every story and task carries at least one `area:` label, and an item with several names its owning lane (ADR 0008).

Statuses are `draft`, `blocked`, `ready`, `in-progress`, `in-review`, `done` and `cancelled`, and the validator enforces what each means:

- **ready.** Every question is settled, every input is provided, every blocker is done, and the item has acceptance criteria.
- **blocked.** The item names what blocks it.
- **done.** The item carries evidence, such as a commit SHA with its CI run.

Estimates sit on a story or on its tasks, never both. [validator.md](validator.md) section 7 gives the frontmatter format.

## 8. Validator

`check.py` is one Python file using only the standard library. It has these commands:

- `check` validates everything, and CI runs it.
- `plan` prints the required documents and their coverage.
- `ready` prints what can start now per lane. It replaces the end-of-session unblock sweep.
- `index` regenerates the two index files.
- `set-status` changes an item's status safely.
- `sync-plan` and `sync-record` drive tracker projection.

[validator.md](validator.md) is its contract, and its tests break a valid fixture project in one place per rule and assert that each defect is caught.

## 9. Tracker projection

Sync splits into a deterministic plan and an execution run by the agent. `check.py sync-plan` compares the files with `.mirage/trackers/<name>.json` and prints operations. The agent runs each one with whatever the environment offers, such as the tracker's MCP server, its CLI or its API, and records the result with `check.py sync-record`. The loop repeats until the plan is empty, so a crash or a rerun never duplicates items. Items are matched by the map first, then by a `mirage-id` line in the tracker item body.

| Mirage | Plane | Jira | GitHub Issues | Linear |
|---|---|---|---|---|
| milestone | milestone | fix version | milestone | project milestone |
| epic | work item of type Epic, or a module | Epic | parent issue with an `epic` label | project |
| story | work item | Story | issue, sub-issue of the epic | issue |
| task | child work item | Sub-task | sub-issue | sub-issue |
| blocked_by | blocking relation | "is blocked by" link | "blocked by" relationship | blocking relation |
| area labels | labels | labels | labels | labels |

Only status flows back from a tracker. A tracker "done" needs evidence, such as a linked pull request. Without it the item goes to in-review and the agent reports it. Edits to titles, bodies, labels or hierarchy made in the tracker are reported as drift and overwritten on the next push (ADR 0008). Each adapter reference in `skills/mirage-sync/references/` detects the tracker's capabilities before writing and names its fallback when one is missing. Credentials come from the environment and are never written to files.

## 10. Audit

`mirage-audit` runs `check.py check`, then reviews the documents in a fresh context for:

- contradictions between documents
- claims with no source in the registers, an ADR or evidence
- requirements with no acceptance path
- missing inputs that block planned work
- delegated answers waiting for the owner's confirmation
- documents whose facet no longer applies

It reports findings with file and line, fixes mechanical ones, and leaves decisions to the owner.

## 11. Evaluation

Three invented projects live under `evals/`: a corporate website, a mobile app with a backend and an admin panel, and a command-line tool. A run passes only if four things hold after the agent delegates every answer:

- `check.py check` is clean.
- Every planned document exists.
- Every question area is covered.
- No date, estimate or price appears without a question or evidence behind it.

A second pass answers a few questions differently and checks that only the affected documents change.

## 12. Build order

Each step ends with a check that proves it.

1. Scaffold, glossary, ADRs and design. Proved by `claude plugin validate --strict`.
2. Catalog, `check.py` and mutation tests. Proved by the test suite.
3. Templates. Proved by the template structure test.
4. The six skills. Proved by `claude plugin validate --strict` and by an interview run on an evaluation project.
5. Tracker adapters for Plane, Jira, GitHub Issues and Linear. Proved against a throwaway project in one tracker, with the others marked unverified until run.
6. All three evaluations, the Codex metadata, the README and release 0.1.0.
