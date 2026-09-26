---
name: mirage-docs
description: Writes or updates every document a mirage project needs from its catalog templates, grounding each statement in the question register, the inputs register, preserved sources and the codebase. Covers the PRD with stable requirement IDs, architecture, UX with screen specs, API, data model, security, operations, test strategy, AGENTS.md and every facet-specific document. Use when the mirage interview is complete, when `check.py plan` shows missing documents, or when answers change and documents must follow.
---

# Mirage docs

You write the documents `check.py plan` requires. Every statement comes from the registers, the sources, the codebase or another document. Anything unknown becomes an open question. The validator decides when a document is finished.

## 1. Get the plan

Run `python3 .mirage/check.py plan --json`. Each planned document has:

- a `key`
- a `path`
- the `sections` it must carry
- the `areas` whose answers feed it

If any area is uncovered, run `mirage-interview` first. A document written ahead of its answers invents them.

Write in the order that lets later documents cite earlier ones:

1. `prd`
2. `architecture`
3. `ux` and its screen specs
4. `api` and `data-model`
5. every other planned document in plan order
6. `agents`, which needs the real build and test commands

## 2. Write one document

For each planned document that is missing, or that has `{{` left in it:

1. Copy `templates/<id>.md` from this skill's folder to the planned path. For a per-item document, replace `{{item}}` or `{{kind}}` in the doc marker with the item. `integration:stripe` uses `templates/integration.md` and `item` becomes `stripe`.
2. Replace every `{{...}}` with real content. Each `{{...}}` says what belongs there. Keep every `<!-- mirage:doc -->` and `<!-- mirage:section -->` marker exactly as written. Headings, tables and prose may be in the project's language from `.mirage/project.json`.
3. Ground every statement:
   - In the answers, cited as `(Q-nnn)`.
   - In the inputs, cited as `(IN-nnn)`.
   - In decisions, cited as `ADR-NNNN`.
   - In requirements, cited as `REQ-<AREA>-<NNN>`.
   - In facts you verified in the codebase.
4. When a statement needs something nobody decided, do not write your best guess. Add an open question to `docs/questions.md` with your recommendation, and cite it in the document. The `mirage-interview` skill's `references/registers.md` has the format.
5. Mark every tunable number, such as a timeout, a threshold or a budget, as a hypothesis until it is measured or decided.
6. Run `python3 .mirage/check.py check --only docs,refs,links,prd,secrets` and fix what it reports for this document.

Done for a document when the check reports nothing for its path.

## 3. Requirements

The PRD owns requirements. Each one is one testable obligation.

- IDs are `REQ-<AREA>-<NNN>`, with the area declared in the requirement areas table.
- Never renumber an ID. A withdrawn requirement keeps its row with scope `OUT` and a note.
- Scope is `MUST`, `SHOULD`, `MAY` or `OUT`, and release is a project release.
- Other documents cite requirement IDs and never restate a requirement in different words.

## 4. Screens and pages

`docs/ux.md` holds the screen inventory. Each row links to its spec at `docs/specs/<component id>/<Name>.md`. Write each spec from `templates/screen.md`. A spec must name:

- its requirements
- the endpoints or data it uses
- its analytics events, when analytics is on
- every state
- checklist acceptance criteria

## 5. Decisions and terms

When a decision is hard to reverse, surprising without context and the result of a real trade-off, record it as an ADR through the `domain-modeling` skill and cite it as `ADR-NNNN`. Add new project terms to `CONTEXT.md` the same way.

## 6. AGENTS.md and CLAUDE.md

Write `AGENTS.md` from `templates/agents.md` with the project's real commands. Read them from the build files, and never guess them. When `CLAUDE.md` does not exist, create it with the single line `@AGENTS.md`. When it exists, add that line to it.

## 7. Updating after a change

When answers change, find every document that cites the changed questions, with a search such as `grep -rn "Q-012" docs AGENTS.md`. Rewrite only the affected sections. Rerun the check for each changed document.

## Finish

Run `python3 .mirage/check.py index`, then `python3 .mirage/check.py check --only docs,index,refs,links,prd,secrets`. Done when it reports no errors and `plan` shows every planned document as existing. `coverage-req` errors wait for `mirage-backlog`.

Report which documents you wrote or changed and which open questions you added. The next phase is `mirage-backlog`.
