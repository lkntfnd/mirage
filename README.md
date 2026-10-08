# Mirage

Mirage turns a project idea into the documentation and backlog that coding agents need to build it without guessing.

It interviews you about the project and asks every question the project's documents need. It writes the full documentation set, which covers requirements with stable IDs, architecture, data, API, UX, security, operations, tests, delivery conventions and agent rules. Only when that documentation is sufficient does it plan milestones, epics, stories and tasks, as files in your repository. A bundled validator fails your CI when the docs and the plan drift apart.

> **Status: pre-release.** The validator has a full test suite, and mirage passed its three end-to-end evaluations on 2026-10-08. The tracker adapters are written from each vendor's documentation and have not yet been run against a live tracker. [docs/design.md](docs/design.md) section 11 says what the evaluations do and do not prove.

## Everything is local first

Mirage writes every document and every backlog item as a file in your repository before anything else. Your tracker is only a view of those files. Plane, Jira, GitHub Issues and Linear are supported as board views.

- The files are the source of truth. Pull requests review them, and CI validates them.
- The tracker is a board for people who prefer one. Mirage pushes the plan there, and only status comes back.
- Each tracker item's title starts with its backlog ID, such as `M1-E02-S03`, so the board, the branches and the files all use the same name.
- Mirage reports an edit someone made on the board before it pushes. You choose whether to copy the edit into the file or let the push replace it.
- Comments, attachments and assignees on the board are yours. Mirage never changes them, and it never deletes a tracker item.
- You can plan without any tracker, and without tracker credentials.

## How it works

1. **Interview.** Mirage first settles what kind of project this is: a website, a mobile app, an API or anything else, and whether it has accounts, payments, several languages and so on. Then it asks every question the documents for those facets need, a round at a time, and each question comes with a recommended answer.
2. **Delegate when you are busy.** Say "use your recommendations" for one question, a round, a document or everything left. Mirage records those answers as delegated. They unblock work at once, and you can confirm them later in one pass.
3. **Inputs.** Mirage tells you what it cannot finish without and how to get each item:
   - information, such as legal texts
   - assets, such as logos and designs
   - accounts, such as app stores or payment providers
   - access to existing systems
   - tools
4. **Documents.** Mirage writes only the documents your project needs, from a catalog of 42 document kinds. Unknowns become tracked questions instead of invented facts.
5. **Audit.** A fresh-context review looks for contradictions, unsupported claims and requirements nobody could test. Each pass is logged in `docs/audit-log.md`.
6. **Sufficiency check.** No task is written until `check.py docs-ready` says the documentation is sufficient. When it is not, mirage comes back to you with the interview, scoped to exactly what is missing.
7. **Backlog.** Milestones, epics, stories and tasks become one Markdown file each, with IDs like `M1-E02-S03-T01`. Every story and task has:
   - its context, with requirement links
   - acceptance criteria
   - how it is verified
   - what is out of scope
   - its blockers
   - an area label that tells agents whose lane it is in
8. **Sync.** Optionally, mirage projects the backlog into your tracker.

## Skills

| Skill | What it does |
|---|---|
| [`/mirage`](skills/mirage/SKILL.md) | Sets up the project, reports where it stands and runs the next phase. Start here. |
| [`mirage-interview`](skills/mirage-interview/SKILL.md) | Settles every decision the documents need, with a recommendation per question. |
| [`mirage-docs`](skills/mirage-docs/SKILL.md) | Writes each required document from its template. |
| [`mirage-audit`](skills/mirage-audit/SKILL.md) | Validates and reviews the documents and the backlog, and logs each pass. |
| [`mirage-backlog`](skills/mirage-backlog/SKILL.md) | Checks that the documentation is sufficient, plans milestones, epics, stories and tasks locally, and lists what can start now. |
| [`mirage-sync`](skills/mirage-sync/SKILL.md) | Projects the backlog into Plane, Jira, GitHub Issues or Linear, and pulls status back. |

## What it writes into your project

```
README.md, AGENTS.md, CLAUDE.md, CONTEXT.md   entry points, agent rules and glossary
docs/summary.md                               one page for someone who reads nothing else
docs/questions.md, docs/inputs.md             every decision, and everything still needed
docs/prd.md, docs/*.md                        the documents your project needs
docs/delivery.md                              how work is written, tracked and finished
docs/adr/, docs/audit-log.md                  decision records and the audit trail
backlog/                                      one file per milestone, epic, story and task
.mirage/                                      project facets and the validator your CI runs
```

Your project stays usable without mirage installed. `docs/delivery.md` explains the item format and the tracker rules, and `.mirage/check.py` needs only Python.

## Requirements

- Python 3.9 or newer, for the validator.
- [Matt Pocock's skills](https://github.com/mattpocock/skills). Mirage uses his `grilling` skill, the engine behind `/grill-me`, for the interview, and his `domain-modeling` skill for the glossary and decision records.

## Install

### Claude Code

```
/plugin marketplace add lkntfnd/mirage
/plugin install mirage@mirage
```

Installing mirage also installs `mattpocock-skills` from the official Claude Code marketplace. Did you already copy Matt Pocock's skills into `~/.claude/skills` with `npx skills`? Then remove those copies, or you will have every skill twice.

### Codex and other agents

```bash
npx skills@latest add mattpocock/skills
npx skills@latest add lkntfnd/mirage
```

When the first installer asks which skills to take, select at least `grilling`, `grill-me`, `domain-modeling` and `to-questionnaire`. In Codex, start with `$mirage`.

## Usage

Run `/mirage` in your project. It sets up `.mirage/`, finds what already exists and runs the next step. Run it again at any time to continue, or after a change in scope. Run `/grill-me` when you want to stress-test one decision in depth, then `/mirage` again to record what you decided.

## Contributing

- [CONTEXT.md](CONTEXT.md) holds the vocabulary.
- [docs/design.md](docs/design.md) covers the design, and [docs/adr/](docs/adr/) the decisions behind it.
- [docs/validator.md](docs/validator.md) is the validator's contract.
- [docs/catalog.md](docs/catalog.md) lists every document kind.

Run the tests with `python3 -m unittest discover tests`. After editing `skills/mirage/scripts/catalog.json`, run `python3 scripts/render_catalog.py`.

## License

MIT
