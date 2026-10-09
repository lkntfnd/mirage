# Validator contract

`check.py` is the single mechanical authority over a mirage project. This document is its contract: the files it reads, the formats it accepts, the rules it enforces and the commands it offers. The code in `skills/mirage/scripts/check.py` and its tests in `tests/` must match this document. Change both together.

## Contents

1. Runtime
2. Files it reads
3. Catalog and plan
4. Markers
5. Registers
6. PRD
7. Backlog
8. Rules
9. Commands
10. Tests

## 1. Runtime

- Python 3.9 or newer, standard library only. Use `from __future__ import annotations`, and no `match` statements.
- One file, `check.py`, plus the data file `catalog.json` beside it. Mirage copies both into a project's `.mirage/` folder.
- The project root is `--root` when given. Otherwise, when the script's folder is named `.mirage`, the root is that folder's parent. Otherwise it is the current directory.
- `MIRAGE_VERSION = "0.1.0"` is a constant in the script.
- Exit codes are 0 for success, 1 when `check` finds errors, and 2 for a usage error or an unreadable `project.json` or `catalog.json`.

## 2. Files it reads

| File | Purpose |
|---|---|
| `.mirage/project.json` | Facets and settings. |
| `.mirage/catalog.json`, or `catalog.json` beside the script | Document kinds. |
| `docs/questions.md` | Question register. |
| `docs/inputs.md` | Inputs register. |
| `docs/prd.md` | Requirements and requirement areas. |
| `docs/**/*.md`, `AGENTS.md`, `CLAUDE.md`, `GLOSSARY.md` or `CONTEXT.md` | Documents. |
| `docs/adr/NNNN-slug.md` | Decision records. |
| `docs/sources/` | Preserved sources and `SHA256SUMS`. |
| `backlog/*.md` | Backlog items and the generated `backlog/README.md`. |
| `.mirage/trackers/<tracker>.json` | Tracker ID maps. |

`project.json`:

```json
{
  "mirage_version": "0.1.0",
  "name": "Fernleaf Tea",
  "language": "en",
  "components": [
    {"id": "api", "kind": "backend-service"},
    {"id": "kiosk", "kind": "shop-kiosk"}
  ],
  "flags": {"personal_data": true, "payments": true},
  "integrations": ["stripe"],
  "regulated": [],
  "domain_topics": [],
  "include": ["ux", "design-system"],
  "documents": [
    {
      "id": "tea-sourcing",
      "title": "Tea sourcing",
      "path": "docs/tea-sourcing.md",
      "sections": [
        {"key": "suppliers", "title": "Suppliers"},
        {"key": "seasons", "title": "Seasons and stock"}
      ],
      "areas": [
        {"key": "suppliers", "ask": "Which estates supply each tea, and what happens when one cannot deliver."},
        {"key": "seasons", "ask": "Which teas are seasonal, and how the shop shows one that has run out."}
      ]
    }
  ],
  "releases": ["v1.0", "v1.1"],
  "areas": ["frontend", "backend", "infra"],
  "require_confirmed_delegation": false
}
```

- `components` needs at least one entry. Component IDs are unique lowercase slugs, and each `kind` is a lowercase slug. A kind in the catalog's `component_kinds` switches on that kind's documents. Any other kind is a custom kind, and its component is planned a component specification (section 3). A component whose `kind` is not a lowercase slug is reported as `component <id> needs a kind that is a lowercase slug` and dropped.
- `include` is optional. It lists catalog document IDs that are planned even when no facet requires them. Each must be the ID of a catalog entry whose `when` is a single-instance form.
- `documents` is optional. It declares documents the catalog does not have, each planned for this project only.
- A flag that is missing counts as false. Only the catalog's `flags` are allowed.
- `integrations`, `regulated` and `domain_topics` are lists of lowercase slugs (`[a-z0-9][a-z0-9-]*`).
- `releases` is an ordered, non-empty list. Earlier entries ship first.
- `areas` is a non-empty list of lowercase slugs.

A project-defined document has these keys, and no others:

| Key | Rule |
|---|---|
| `id` | A lowercase slug, unique among `documents`, and not the ID of a catalog entry. It is the document's key. |
| `title` | A non-empty string. |
| `path` | Optional. A Markdown file under `docs/`, with no empty, `.` or `..` segment. It cannot sit under `docs/adr/`, `docs/sources/` or `docs/specs/`, whose files are read as decision records, preserved sources and screen specs. It defaults to `docs/<id>.md`. No other planned document may use the same path. |
| `sections` | A non-empty list of `{"key", "title"}`. Keys are lowercase slugs, unique within the document, and titles are non-empty. |
| `areas` | A non-empty list of `{"key", "ask"}`. Keys are lowercase slugs, unique within the document, and asks are non-empty. |

A project-defined document is checked as type `sections`: its file carries `<!-- mirage:doc <id> -->` and every section marker. Its area keys are `<id>/<area>`, and `coverage-area` applies to them as to any other.

Every problem in `project.json` is reported as `project-json`, and the entry that holds it is dropped. The messages for the keys above are:

| Problem | Message |
|---|---|
| `include` is not a list of strings | `include must be a list of catalog document IDs` |
| An entry names no catalog document | `include entry 'x' is not a catalog document` |
| An entry names a per-item or listed document | `include entry 'x' is planned per item, so it cannot be included by name` |
| `documents` is not a list | `documents must be a list` |
| An entry is not an object, or its `id` is not a slug | `documents[N] needs an id that is a lowercase slug` |
| An entry holds a key outside the table | `document <id> has unknown key <key>` |
| Two entries share an ID | `document <id> is declared twice` |
| The ID is a catalog entry's | `document <id> is already a catalog document` |
| The title is missing or empty | `document <id> needs a title` |
| The path breaks its rule | `document <id> needs a path that is a Markdown file under docs/` |
| The path belongs to another planned document | `document <id> uses the path of <other key>` |
| Sections are missing or malformed | `document <id> needs sections, each with a slug key and a title` |
| Areas are missing or malformed | `document <id> needs areas, each with a slug key and an ask` |
| A section or area key repeats | `document <id> uses the section key <key> twice`, or `the area key` |

## 3. Catalog and plan

Each catalog entry has `id`, `title`, `path`, `when`, `check`, `sections`, `areas` and `inputs`. The plan is the list of document instances the project requires.

An entry may also carry `alt_paths`, a list of older names for the same file. When `path` does not exist and one of them does, the instance's path is that older name. The glossary uses this: `domain-modeling` writes `GLOSSARY.md`, and wrote `CONTEXT.md` before 2026-09. When neither exists, `doc-missing` names `path` and says which older names are accepted.

`when` forms:

| Form | Meaning |
|---|---|
| `"always"` | One instance. |
| `{"component": [kinds]}` | One instance if any component has one of the kinds. |
| `{"flag": name}` | One instance if the flag is true. |
| `{"nonempty": list}` | One instance if the named list has entries. |
| `{"any": [forms]}` | One instance if any sub-form yields one. Sub-forms are never `per` forms. |
| `{"per": list}` | One instance per list item. `{item}` in the path becomes the item. |
| `{"per_component": [kinds]}` | One instance per distinct kind among matching components. `{kind}` in the path becomes the kind. |
| `{"per_custom_component": true}` | One instance per component whose kind is not in the catalog's `component_kinds`. `{item}` in the path becomes the component ID. |
| `{"listed_in": "ux"}` | Not planned. Every file under `docs/specs/` is an instance and is checked as one. |

- A single-instance document's key is its `id`, such as `prd`.
- A per-item document's key is `<id>:<item>` or `<id>:<kind>`, such as `integration:stripe` or `platform:mobile-app`. A component specification's key is `component:<component id>`.
- A screen spec's key is `screen`.

The plan holds, in this order:

1. Every catalog entry that a facet requires, in catalog order. Its reason names the facet, such as `flag payments is true`. A component specification's reason is `component <id> has kind <kind>, which has no document of its own`.
2. Among them, in the same catalog order, every entry that `include` names and no facet requires. Its reason is `project.json includes it`. An included entry that a facet already requires keeps the facet's reason.
3. Every project-defined document, in the order `documents` lists them. Its reason is `project.json declares it`.

`check` types:

| Type | Meaning |
|---|---|
| `sections` | The file must exist and carry the doc marker, every section marker and no placeholder. |
| `exists` | The file must exist. |
| `register` | The file is parsed as a register, section 5. |
| `generated` | The file must equal what `index` would write. |
| `sources` | The file is checked as a source list, rule group `sources`. |

When the `agents` document is planned, `CLAUDE.md` must exist and contain a line that is exactly `@AGENTS.md`.

## 4. Markers

Markers are HTML comments, so they stay invisible when rendered and work in any document language.

- `<!-- mirage:doc KEY -->` appears once in each `sections` document, where `KEY` is the document key.
- `<!-- mirage:section KEY -->` appears before the heading of each catalog section.
- A placeholder is `{{` outside fenced code blocks, or any `<!-- mirage:todo` comment.
- `<!-- mirage:generated NAME -->` is the first line of a generated file.

## 5. Registers

### Questions, `docs/questions.md`

```markdown
### Q-012 Which payment provider handles card payments?

- Status: delegated
- Covers: payments/provider, integration:stripe/purpose
- Blocks: REQ-PAY-001, M1-E04-S02
- Recommendation: Stripe, because it covers the target countries.
- Answer: Stripe. Delegated on 2026-09-26.
```

- A question starts at a line matching `### Q-\d{3} <title>`. Its fields are the lines `- <Key>: <value>` that follow, up to the next `###` or `##` heading.
- The allowed keys are `Status`, `Covers`, `Blocks`, `Recommendation`, `Answer`, `Owner` and `Questionnaire`.
- `Status` is `open`, `answered` or `delegated`.
- `Recommendation` is required and non-empty.
- `Answer` is required for an answered or delegated question, and must contain a date `YYYY-MM-DD`.
- `Covers` is a comma-separated list of area keys `<doc key>/<area key>`. Each must name an area of a planned document.
- `Blocks` is a comma-separated list of IDs. They are checked like any other reference.

### Inputs, `docs/inputs.md`

```markdown
### IN-003 Apple Developer Program account

- Status: missing
- Kind: account
- Needed for: platform:mobile-app, M2-E07-S01
- How to get: Enroll at developer.apple.com as an organization. Enrollment needs a D-U-N-S number.
- Location:
```

- An input starts at a line matching `### IN-\d{3} <title>`.
- The allowed keys are `Status`, `Kind`, `Needed for`, `How to get`, `Location`, `Reason` and `Owner`.
- `Status` is `missing`, `provided` or `not-needed`.
- `Kind` is `information`, `asset`, `account`, `access` or `tool`.
- `Needed for` is required and non-empty.
- `How to get` is required when the input is missing.
- `Location` is required when the input is provided. It names where the thing lives, never the thing itself when it is a secret.
- `Reason` is required when the input is not-needed.

## 6. PRD

- Requirement rows are Markdown table rows anywhere in `docs/prd.md` outside fenced code blocks whose first cell is a requirement ID, optionally in backticks. The columns are `ID | Requirement | Scope | Release`.
- The ID format is `REQ-<AREA>-<NNN>`, with `<AREA>` matching `[A-Z][A-Z0-9]{1,7}` and `<NNN>` exactly three digits.
- Scope is `MUST`, `SHOULD`, `MAY` or `OUT`.
- Release is one of the project's releases. A row with scope `OUT` may use `-` instead.
- Declared areas are the table rows inside the `areas` section, meaning between `<!-- mirage:section areas -->` and the next section marker. Their first cell is an area code and the header row is `Code | Name`. Every requirement's area must be declared.

## 7. Backlog

One file per item, directly under `backlog/`, named `<ID>-<slug>.md`, where the slug matches `[a-z0-9][a-z0-9-]*`.

| Level | ID pattern | Example |
|---|---|---|
| milestone | `M\d+` | `M1` |
| epic | `E\d{2}` | `E02` |
| story | `M\d+-E\d{2}-S\d{2}` | `M1-E02-S03` |
| task | `M\d+-E\d{2}-S\d{2}-T\d{2}` | `M1-E02-S03-T01` |

The ID alone gives the level, the milestone, the epic and the parent. A story needs its milestone file and its epic file. A task needs its story file.

### Frontmatter

The frontmatter is a strict YAML subset between two `---` lines at the top of the file:

- one `key: value` per line, where keys match `[a-z_]+`
- a value is bare text up to the end of the line and trimmed, or a double-quoted string with `\"` escapes, or an inline list `[a, b, "c d"]`, where `[]` is empty
- no nesting, no multi-line values and no comments
- blank lines are ignored
- a line that does not parse is an error

| Key | Levels | Value |
|---|---|---|
| `id` | all, required | the ID, equal to the file name prefix |
| `title` | all, required | text |
| `status` | all, required | `draft`, `blocked`, `ready`, `in-progress`, `in-review`, `done`, `cancelled` |
| `kind` | story | `feature` (default), `spike`, `bug`, `chore`, `docs` |
| `priority` | story, required | `urgent`, `high`, `medium`, `low` |
| `scope` | story, required | `must`, `should`, `may` |
| `release` | story, required | one of the project's releases |
| `req` | story | list of requirement IDs |
| `questions` | story, task | list of question IDs |
| `inputs` | story, task | list of input IDs |
| `blocked_by` | story, task | list of story or task IDs |
| `labels` | story and task required, others optional | list, including at least one `area:<area>` |
| `lane` | story, task | an area, required when the item has more than one area label |
| `estimate` | story, task | 1, 2, 3, 5 or 8 |
| `evidence` | all | text, required when done |
| `blocked_reason` | all | text |
| `replaces` | all | an ID of a cancelled item |
| `replaced_by` | all | an ID |
| `due` | all | `YYYY-MM-DD` |
| `due_evidence` | all | text, required when `due` is set |

Any other key is an error.

### Body sections

The body of a story or a task uses the same markers as documents (section 4). Each marker is followed by a heading in the project's language.

| Marker | Holds | Required |
|---|---|---|
| `<!-- mirage:section context -->` | why the item exists, with its requirement and document links | yes |
| `<!-- mirage:section acceptance -->` | the checklist of testable criteria | yes |
| `<!-- mirage:section technical -->` | endpoints, tables, configuration keys and files | no |
| `<!-- mirage:section verification -->` | the tests, scenario IDs or commands that prove the criteria | yes |
| `<!-- mirage:section out-of-scope -->` | what the item leaves out, or a sentence saying nothing is excluded | yes |

A story or task whose status is `ready`, `in-progress`, `in-review` or `done` carries every required marker. Each required section holds at least one non-blank line after its heading and before the next marker. The acceptance section holds at least one checklist item (`- [ ]` or `- [x]`). Items in `draft`, `blocked` or `cancelled` may omit sections. Milestones and epics have no body sections.

### Status meaning

A task inherits its story's `questions`, `inputs` and `blocked_by` in addition to its own. An item's prerequisites are:

- every question it depends on is answered, or delegated unless `require_confirmed_delegation` is true
- every input is provided or not-needed
- every blocker is done

A spike is the exception. The questions a spike story lists are the ones it answers, so they are not prerequisites of the spike or of its tasks. A spike whose status is `done` while one of its questions is still `open` is reported as `backlog-done`, because its outcome was not recorded.

Status rules:

- **ready.** Every prerequisite is met and a feature story lists at least one requirement. A story or task also meets the body-section rule above. A milestone or epic holds at least one checklist item.
- **blocked.** At least one prerequisite is unmet, or `blocked_reason` is set.
- **done.** `evidence` is set, and every descendant is done or cancelled. The descendants are a story's tasks, an epic's stories in every milestone, and a milestone's stories.
- **in-progress and in-review.** No prerequisite check applies.
- A spike story lists at least one question.
- An estimate may sit on a story or on its tasks, never on both.

## 8. Rules

`check` runs every group unless `--only` names some. Each diagnostic has a code, a file path and, where it applies, a 1-based line.

| Group | Codes |
|---|---|
| `project` | `project-json` |
| `docs` | `doc-missing`, `doc-marker`, `doc-section`, `doc-placeholder`, `claude-import`, `adr-duplicate` |
| `index` | `index-stale` |
| `register` | `register-parse`, `register-duplicate`, `register-field`, `register-status`, `register-recommendation`, `register-answer`, `register-covers`, `inputs-parse`, `inputs-duplicate`, `inputs-field`, `inputs-status`, `inputs-kind`, `inputs-needed-for`, `inputs-how`, `inputs-location`, `inputs-reason` |
| `prd` | `prd-id`, `prd-duplicate`, `prd-scope`, `prd-release`, `prd-area` |
| `refs` | `ref-missing` |
| `coverage` | `coverage-req`, `coverage-area` |
| `backlog` | `backlog-filename`, `backlog-id`, `backlog-frontmatter`, `backlog-field`, `backlog-hierarchy`, `backlog-ref`, `backlog-cycle`, `backlog-ready`, `backlog-blocked`, `backlog-done`, `backlog-section`, `backlog-estimate`, `backlog-label`, `backlog-kind`, `backlog-due`, `backlog-replace` |
| `sources` | `sources-missing`, `sources-hash`, `sources-unlisted` |
| `links` | `link-broken` |
| `secrets` | `secret` |

Group details:

- **refs.** Scan every scanned file outside fenced code blocks for `REQ-…`, `Q-\d{3}`, `IN-\d{3}`, `ADR-\d{4}` and story or task IDs. Each must exist: a requirement in the PRD, a question in the register, an input in the inputs register, a file `docs/adr/NNNN-*.md`, or a backlog file. The scanned files are `docs/**/*.md` except `docs/sources/**`, `backlog/*.md`, `AGENTS.md`, `GLOSSARY.md` and `CONTEXT.md`. Generated files are not scanned by any group, because every ID they hold is checked at its source.
- **adr-duplicate.** Two files in `docs/adr/` share the same `NNNN` number.
- **coverage-req.** Every requirement whose scope is not OUT is listed in the `req` of at least one story that is not cancelled and whose release is the same as or earlier than the requirement's.
- **coverage-area.** Every area of every planned document is named in the `Covers` of at least one question, whatever its status.
- **backlog-ref.** Every ID in `req`, `questions`, `inputs`, `blocked_by`, `replaces` and `replaced_by` exists. An item cannot block itself. A blocker cannot be cancelled.
- **backlog-cycle.** The `blocked_by` graph has no cycle. Report one cycle path.
- **backlog-section.** A story or task in `ready`, `in-progress`, `in-review` or `done` misses a required body section, has one that is empty, or has no checklist item in its acceptance section. The message names the section.
- **backlog-label.** A story or task has at least one `area:` label. Every area is declared in `project.json`. With several areas, `lane` is set and is one of them.
- **backlog-replace.** The target of `replaces` is cancelled, and it names this item in `replaced_by`.
- **sources.** Only when the `sources` document is planned. `docs/sources/SHA256SUMS` holds lines `<sha256>  <path>`, with each path relative to `docs/sources/`, as `shasum -a 256` writes them when run inside that folder. Every listed file matches its hash, and every file under `docs/sources/` other than `SHA256SUMS` is listed.
- **links.** Every relative Markdown link target in a scanned file exists, ignoring `#anchor` parts, `http:`, `https:` and `mailto:` links.
- **secrets.** A scanned file or `.mirage/project.json` holds any of these:
  - a private key header `-----BEGIN [A-Z ]*PRIVATE KEY-----`
  - an AWS key `AKIA[0-9A-Z]{16}`
  - a Stripe live key `sk_live_[0-9A-Za-z]{10,}`
  - a GitHub token `gh[pousr]_[A-Za-z0-9]{36,}`
  - a Slack token `xox[abprs]-[A-Za-z0-9-]{10,}`

  The message names the pattern, never the match.

## 9. Commands

```
python3 .mirage/check.py check [--only GROUP[,GROUP]] [--json]
python3 .mirage/check.py plan [--json]
python3 .mirage/check.py docs-ready [--json]
python3 .mirage/check.py ready [--json]
python3 .mirage/check.py index
python3 .mirage/check.py set-status ID [ID ...] STATUS [--evidence TEXT]
python3 .mirage/check.py sync-plan TRACKER
python3 .mirage/check.py sync-expect TRACKER
python3 .mirage/check.py sync-record TRACKER --id ID --remote-id RID [--key KEY] [--url URL]
python3 .mirage/check.py sync-record TRACKER --link FROM TO
python3 .mirage/check.py sync-record TRACKER --unlink FROM TO
python3 .mirage/check.py sync-record TRACKER --forget ID
python3 .mirage/check.py version
```

Every command accepts `--root PATH`.

**check.** Prints `path:line: code: message` sorted by path and line, then `ok` or `N errors`. With `--json` it prints `{"errors": [{"path", "line", "code", "message"}]}`.

**plan.** Prints each planned document instance with its key, path, reason, sections and areas. Each area shows `covered` or `uncovered`, and each typical input is listed. The reason is the facet that required it.

After the planned documents it lists the catalog entries that are not planned and that `include` can name, which are the unplanned entries with a single-instance `when` form, in catalog order:

```
available by name, through include in .mirage/project.json:
  ux: User experience
  cli: Command-line interface
```

The block is left out when there is no such entry. With `--json` the same list is the `available` key, as `[{"id", "title"}]`, and it is `[]` when empty.

With `--json`:

```json
{"docs": [{"key": "integration:stripe", "id": "integration", "title": "...", "path": "docs/integrations/stripe.md",
  "reason": "integrations includes stripe", "exists": true,
  "sections": [{"key": "...", "title": "..."}],
  "areas": [{"key": "integration:stripe/auth", "ask": "...", "covered": false}],
  "inputs": [{"key": "...", "title": "...", "kind": "account"}]}],
 "available": [{"id": "cli", "title": "Command-line interface"}]}
```

**docs-ready.** Answers one question: is the documentation sufficient to plan the backlog? It runs the `project`, `docs`, `register`, `prd`, `refs`, `links`, `sources` and `secrets` groups and the `coverage-area` rule. It ignores `coverage-req`, the `backlog` and `index` groups, and every diagnostic whose path is under `backlog/`. It adds two conditions of its own: `docs/prd.md` defines at least one requirement whose scope is not `OUT`, and `docs/audit-log.md` records a documents audit, meaning it holds a line that starts with `## YYYY-MM-DD Documents`.

- When nothing is reported it prints `sufficient` and exits 0.
- Otherwise it prints the diagnostics in `check` format, then `not sufficient: N problems`, and exits 1. A PRD with no in-scope requirement is reported as `docs/prd.md: prd-empty: no requirement is in scope`. An audit log with no documents entry is reported as `docs/audit-log.md: audit-missing: no documents audit is recorded; run mirage-audit`. A missing audit log is `doc-missing`, as for any planned document. `prd-empty` and `audit-missing` are reported only by this command.
- In both cases it then prints every open question, as `open: Q-nnn <title> (blocks: <what it blocks, as in the index, or nothing>)`. Open questions never change the exit code.

With `--json` it prints `{"sufficient": true, "errors": [...], "open_questions": [{"id", "title", "blocks"}]}`.

**ready.** Groups stories and tasks by lane in three lists. Every area in `project.json` is a lane and is printed, even when all three of its lists are empty:

- ready now, meaning status ready with every prerequisite met
- can become ready, meaning status draft or blocked with every prerequisite met, every required body section complete, no `blocked_reason` and, for a feature story, at least one requirement in `req`
- wrongly ready, meaning status ready with an unmet prerequisite, with the unmet ones named

`--json` gives the same data.

**index.** Writes `docs/README.md` and `backlog/README.md`. The output is deterministic, with no timestamps. The `check` group `index` compares both files with what `index` would write.

- `docs/README.md` starts with `<!-- mirage:generated index -->` and holds:
  - the project name
  - a reading-order table of every planned document with its path and whether it exists
  - the open questions with what they block: the question's `Blocks` field, then every story or task that lists the question in `questions`, except the spike that answers it
  - the delegated answers awaiting confirmation
  - the missing inputs with what needs them
  - a count table of requirements, questions, inputs, ADRs, milestones, epics, stories and tasks
- `backlog/README.md` starts with `<!-- mirage:generated backlog -->` and holds:
  - one section per milestone with a table of its stories and tasks, giving ID, title, status, lane and blockers. The blockers are the item's own `blocked_by` IDs, then every question and input among its prerequisites that is still unmet.
  - a table of epics

**set-status.** Rewrites only the `status` line of each named item's frontmatter, and the `evidence` line when `--evidence` is given. When any named item is refused, no file is changed. It prints one `ID: old -> new` line per item. It adds the `evidence` line if it is absent. It refuses an unknown status, and it refuses `done` without evidence, either given or already present.

**sync-plan.** Compares the backlog with `.mirage/trackers/<TRACKER>.json` and prints one JSON object per line, one operation each, in dependency order. No output means nothing to do.

1. `create` for unmapped items: milestones, then epics, stories and tasks, each sorted by ID
2. `update` for mapped items whose content hash changed
3. `link` for `blocked_by` edges whose ends are both mapped and that the map does not list
4. `unlink` for mapped edges that no longer exist
5. `orphan` for mapped items whose file is gone

Each `create` and `update` carries the payload below. Its `hash` is the SHA-256 of the canonical JSON of the payload fields other than `hash` and `remote_id`, with sorted keys, so any change in what would be pushed produces an `update`.

- `id`, `level`, `status`, `priority`, `estimate`
- `due`: the item's `due` date, or null
- `title`: the ID, a space and the item's title, such as `M1-E02-S03 Pay for an order by card`
- `labels`: the item's own labels. A story adds `type:<kind>`, `scope:<scope>` and `release:<release>`. A task adds its story's `scope:` and `release:` labels.
- `milestone`, which is the M ID or null
- `epic`, which is the E ID or null
- `parent`: the epic for a story, the story for a task, and null otherwise
- `body`: the Markdown body with every line that holds only a `<!-- mirage:... -->` comment removed, followed by a footer. The footer is a blank line, a `---` line, then one line per non-empty field in this order, and always ends with the `mirage-id` line:

  ```
  Requirements: REQ-PAY-001, REQ-PAY-004
  Questions: Q-012
  Inputs: IN-004
  Blocked by: M1-E02-S02
  Evidence: <evidence text>
  mirage-id: M1-E02-S03
  ```
- `hash`
- `remote_id`, on `update` only

An agent runs the operations, records each result with `sync-record`, then runs `sync-plan` again until it prints no operations.

**sync-expect.** Prints one JSON object per line for every mapped item whose current payload hash equals the hash in the map, sorted by ID. Each object is `{"op": "expect", ...}` with the same payload fields as an `update`, including `remote_id`. It is what the tracker holds for that item unless a person edited it there, so an agent compares it with the tracker to find drift. Mapped items with a pending `update` are left out, because their last pushed payload is not known.

**sync-record.** Writes the map file atomically. `--id` stores `remote_id`, `key`, `url`, the current content hash and the current status. `--link` and `--unlink` edit the map's `links` list. `--forget ID` removes an orphaned item and every link that touches it, after the agent has reported the orphan. Every other top-level key, such as the adapter's `settings`, is preserved as it was. Map format:

```json
{"tracker": "plane",
 "settings": {"workspace": "hollow-lane", "project": "a1b2"},
 "items": {"M1-E02-S03": {"remote_id": "…", "key": "FT-12", "url": "…", "hash": "…", "status": "ready"}},
 "links": [["M1-E02-S03", "M1-E01-S02"]]}
```

## 10. Tests

`tests/test_check.py` uses `unittest` and runs with `python3 -m unittest discover tests`.

- A valid fixture project under `tests/fixtures/valid/` passes `check` with no errors. Its facets must plan at least one per-item document, one per-component document and one flag-driven document.
- For every diagnostic code in section 8, one test copies the fixture into a temporary directory, applies one mutation, and asserts that `check` reports that code and nothing else.
- Every `when` form, `include`, project-defined documents, and the `ready`, `index`, `set-status`, `sync-plan` and `sync-record` commands, have tests that assert exact output values. Every `project-json` message in section 2 has a test.
- The fixture and every example use invented projects only.
