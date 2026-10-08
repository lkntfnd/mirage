# Mirage design

Status: accepted by the owner in two interview rounds on 2026-09-26 and revised after the owner's review of 2026-10-08. The exact file formats and rules live in [validator.md](validator.md). The full document list lives in [catalog.md](catalog.md), which is generated from the catalog data.

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
12. Build status

## 1. What mirage produces

Mirage writes into the project it documents. After a full run the project holds this layout.

```
README.md                  what the project is and where its documentation starts
AGENTS.md                  agent operating rules, canonical for every agent
CLAUDE.md                  one line, @AGENTS.md
GLOSSARY.md                glossary, owned by domain-modeling (CONTEXT.md with older versions of it)
docs/
  README.md                generated index, reading order, open work
  questions.md             every question, recommendation and answer
  inputs.md                every piece of information, asset, account, access or tool still needed
  summary.md               one page for someone who reads nothing else
  prd.md                   requirements REQ-<AREA>-<NNN>
  delivery.md              how work is written, tracked and finished
  audit-log.md             one entry per audit pass
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
| `mirage-backlog` | model | Checks that the documentation is sufficient, then plans milestones, epics, stories and tasks as local files and keeps statuses honest. |
| `mirage-audit` | model | Runs the validator, then reviews the documents or the backlog adversarially in a fresh context, and logs each pass. |
| `mirage-sync` | model | Projects the backlog into a tracker, pulls status back and reports edits people made on the board. |

The router is user-invoked, so it costs no context until someone types `/mirage`. The five phase skills are model-invoked. The router must be able to call them, and a request such as "plan milestones for this repo" should reach `mirage-backlog` directly.

A new project runs interview, documents, a documents audit, backlog and a backlog audit, then optionally sync. A later change runs the same phases on the delta only.

The backlog waits for the documentation (ADR 0010). `mirage-backlog` writes no item until `check.py docs-ready` prints `sufficient`. When it does not, mirage goes back to the owner through the grilling interview, scoped to the gaps, then updates the documents and checks again. In an existing codebase the agent reads the code and existing docs first, because finding facts is its job, and the interview asks only what they cannot answer.

## 3. Facets

The first interview round settles `.mirage/project.json`:

- the project name
- the document language, English by default
- the components, each with a kind: website, web-app, mobile-app, desktop-app, browser-extension, backend-service, cli, library, data-pipeline, embedded or game
- the flags, each true or false: accounts, personal data, payments, content edited by non-developers, several languages, analytics, notifications, search, offline use, realtime updates, AI features, admin tools, migration from an existing system, own file formats, source documents to preserve
- three lists: third-party integrations, regulated regimes, and complex rule sets that need their own spec
- the release names in order
- the area labels that name the lanes, such as `mobile`, `backend` and `infra`

Every later question and document hangs off these answers.

## 4. Catalog

The catalog is data in `skills/mirage/scripts/catalog.json`. It holds 42 document kinds. For each kind it names:

- the facet that switches it on
- its path
- the sections its file must carry
- the question areas the interview must cover
- the inputs it typically needs

[catalog.md](catalog.md) renders it for reading. `check.py plan` prints the documents a given project needs and why, so the skills never keep their own copy.

Every project gets a README, an executive summary, the PRD, architecture, security, test strategy, operations, delivery conventions, agent rules, both registers, the generated index and an audit log. The delivery conventions document puts the item format, the status rules and the tracker rules inside the project, so the project stays usable by people and agents who do not have mirage installed.

Specialist documents (integration, domain, payments, search and the like) share one shape. They open with the scope and the requirements they serve, state the contract, mark every tunable value as a hypothesis, name the admin controls, and end with a test-scenario table.

Each document kind has a template in `skills/mirage-docs/templates/`. A template carries the section markers and headings, fixed tables where structure matters, and `{{...}}` guidance. The validator rejects any leftover `{{`, so an unfinished document cannot pass. Markers are HTML comments, so they work in any document language.

## 5. Interview

`mirage-interview` calls `grilling` and `domain-modeling` and adds these rules on top.

1. **Coverage.** The design tree starts from the facets. Each planned document contributes its question areas as branches. The interview is complete when every area of every planned document is named by at least one question in the register. The validator checks this.
2. **Persistence.** Each answer goes into `docs/questions.md` the moment it is settled, never in a batch.
3. **Delegation.** At any point the owner can say "use your recommendations" for one question, the current round, one document or everything left. The agent records each accepted recommendation as a delegated answer, dated. It never fills a question silently. A delegated answer unblocks work at once, and the index lists every one of them for later confirmation. Delegation covers decisions, never facts: a question whose answer is a date, a price, an estimate or a target number stays open for the owner.
4. **Inputs.** For each planned document the interview asks about its typical inputs and records what is missing in `docs/inputs.md`, with how to get it.
5. **No invention.** Estimates, dates, prices, accounts and approvals come only from the owner or from evidence. Anything else becomes an open question.
6. **Gap mode.** When `docs-ready` fails or open questions block planned work, the interview covers only the reported gaps and the blocking questions.

When a question needs someone outside the conversation, the interview keeps it open with that person as its owner. It suggests `to-questionnaire`, which only the owner can start, to send such questions out.

## 6. Registers

`docs/questions.md` holds one section per question: status (`open`, `answered` or `delegated`), the areas it covers, what it blocks, the agent's recommendation and the dated answer. `docs/inputs.md` holds one section per input: status (`missing`, `provided` or `not-needed`), kind, what needs it, how to get it, where it lives, and the reason when it is not needed. An input records a location, never a secret. [validator.md](validator.md) section 5 gives both formats.

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

A spike is a story that answers a question by trying something. The question it lists does not block it, and it cannot be done while that question is still open.

From `ready` onward, a story or task body carries four sections under markers: context, acceptance criteria, verification and out of scope. Technical notes are optional. The markers make the template checkable in any language, and the sync removes them before anything reaches a tracker.

Estimates sit on a story or on its tasks, never both. [validator.md](validator.md) section 7 gives the frontmatter format.

## 8. Validator

`check.py` is one Python file using only the standard library. It has these commands:

- `check` validates everything, and CI runs it.
- `plan` prints the required documents and their coverage.
- `docs-ready` says whether the documentation is sufficient to plan the backlog, and lists the open questions. Sufficient means every planned document exists with no placeholder, every question area is covered, every reference and link resolves, the PRD has a requirement in scope, and the audit log records a documents audit.
- `ready` prints what can start now per lane. It replaces the end-of-session unblock sweep.
- `index` regenerates the two index files.
- `set-status` changes an item's status safely.
- `sync-plan`, `sync-record` and `sync-expect` drive tracker projection.

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

Each tracker item's title starts with the backlog ID. Its labels are the item's area labels plus `type:`, `scope:` and `release:` labels. Its description ends with a footer naming its requirements, questions, inputs, blockers, evidence and `mirage-id`.

A sync run works in this order, so nothing a person did on the board is lost:

1. Check the tracker's capabilities.
2. Pull status. A tracker "done" needs evidence, such as a linked pull request. Without it the item goes to in-review and the agent reports it.
3. Find drift with `sync-expect`, which prints what mirage last pushed. A title, description, label or parent that differs was edited by a person, and the owner chooses whether to copy the change into the file or let the push replace it (ADR 0008).
4. Push, looking each item up by its `mirage-id` before creating it.
5. Read back what was written and report any mismatch.

Mirage writes only titles, descriptions, labels, parents, milestones, priorities, estimates, due dates, statuses and blocking links. Comments, attachments and assignees belong to the people using the board. Mirage uses an existing project and never creates one, and it changes the project's configuration, such as adding a workflow state, only after the owner agrees. Each adapter reference in `skills/mirage-sync/references/` detects the tracker's capabilities before writing and names its fallback when one is missing. Credentials come from the environment and are never written to files.

## 10. Audit

`mirage-audit` runs in two scopes. The documents audit runs before any task is planned, and the backlog audit runs after items are written and before a milestone starts. Each pass appends an entry to `docs/audit-log.md`.

It runs `check.py check`, then reviews in a fresh context for:

- contradictions between documents
- claims with no source in the registers, an ADR or evidence
- requirements that cannot be tested, or that no story's acceptance criteria would prove
- acceptance criteria that would pass without the requirement being met
- blocking links that do not truly gate, or real dependencies that are missing
- items whose work falls outside their lane
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

### Runs of 2026-10-08

Each run was a fresh agent that read the skill files and followed them from the interview through the backlog audit. The owner was simulated by one standing answer, "use your recommendations for everything the brief does not answer".

| Evaluation | Result | Documents | Questions | Backlog items |
|---|---|---|---|---|
| `corporate-website` | pass | 20, plus 10 screen specs | 81, of which 5 left open | 97 |
| `csv-cli` | pass | 19 | 69, of which 1 left open | 50 |
| `booking-app` | pass | 33, plus 23 screen specs | 162, of which 9 left open | 156 |

In every run `docs-ready` refused the backlog until the documents and their audit existed. The questions the agents left open were the ones only an owner can answer, such as prices, launch dates and target numbers.

The runs reported 56 points of friction between them. Most were fixed in the validator, the templates or the skill wording. The larger fixes were:

- A spike could never become ready, because the question it answers blocked it.
- `docs-ready` accepted an audit log with no audit in it.
- The delivery template's example IDs failed the validator in every project.
- A blanket delegation could turn an agent's guess at a date or a price into a recorded answer.
- An input marked not-needed had no field for its reason.

Left as they are:

- `check` has no per-path filter, so an agent reads one document's errors out of the sorted output.
- Whether the backlog changed since the last audit is the agent's judgement, not a machine check.
- `docs-ready` checks structure, coverage and that an audit ran. How deep the documents go remains the audit's job.
- In one run the agent harness refused to let a sub-agent write a file named `summary.md`, and the agent wrote it through the shell.

What these runs do not prove:

- The skills changed after the runs, in response to them. The final wording has not been run end to end.
- The agents read the skill files directly. No run went through an installed plugin and `/mirage`.
- Each audit ran in the same context that wrote the documents, not in a fresh one.
- The second pass, which changes two answers, was not run.
- No run synced to a tracker. The Plane adapter was checked against the tool definitions of a connected Plane server, and the Jira, GitHub and Linear adapters only against the vendors' documentation.

## 12. Build status

Each step ends with a check that proves it.

| Step | Proved by | Status |
|---|---|---|
| Scaffold, glossary, ADRs and design | `claude plugin validate --strict` | done |
| Catalog, `check.py` and mutation tests | the test suite | done |
| Templates | the template structure test | done |
| The six skills | `claude plugin validate --strict` and the evaluation runs | done |
| Tracker adapters for Plane, Jira, GitHub Issues and Linear | a sync against a throwaway project in each tracker | written, not yet run against a live tracker |
| All three evaluations | `evals/check_eval.py` | passed on 2026-10-08, with the limits listed in section 11 |
| Release 0.1.0 | an install from the marketplace, and one sync against a live tracker | open |
