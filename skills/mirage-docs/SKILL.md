---
name: mirage-docs
description: Writes or updates every document a mirage project needs from its catalog templates, grounding each statement in the question register, the inputs register, preserved sources and the codebase. Covers the PRD with stable requirement IDs, architecture, UX with screen specs, API, data model, security, operations, test strategy, delivery conventions, AGENTS.md, the project README, an executive summary and every facet-specific document. Use when the mirage interview is complete, when `check.py plan` shows missing documents, or when answers change and documents must follow.
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
4. `api`, `data-model` and `formats`
5. every other planned document in plan order
6. `delivery`, then `agents`
7. `readme`, then `summary` last, because it condenses everything else

`index` and `audit-log` are not yours. The validator generates the index, and `mirage-audit` writes the audit log.

## 2. Write one document

For each planned document that is missing, or that has `{{` left in it:

1. Copy `templates/<id>.md` from this skill's folder to the planned path. For a per-item document, replace `{{item}}` or `{{kind}}` in the doc marker with the item. `integration:stripe` uses `templates/integration.md` and `item` becomes `stripe`.
2. Replace every `{{...}}` with real content. Each `{{...}}` says what belongs there. Keep every `<!-- mirage:doc -->` and `<!-- mirage:section -->` marker exactly as written. Text outside `{{...}}` is standard wording that stays. Headings, tables and prose may be in the project's language from `.mirage/project.json`.
3. Ground every statement:
   - In the answers, cited as `(Q-nnn)`.
   - In the inputs, cited as `(IN-nnn)`.
   - In decisions, cited as `ADR-NNNN`.
   - In requirements, cited as `REQ-<AREA>-<NNN>`.
   - In facts you verified in the codebase.
4. When a statement needs something nobody decided, do not write your best guess. Add a question to `docs/questions.md` with your recommendation, and cite it in the document. It is `open`, or `delegated` when the owner's standing delegation covers it. A date, a price, an estimate or a target number is never covered and stays open. The `mirage-interview` skill's `references/registers.md` has the format.
5. Mark every tunable number, such as a timeout, a threshold or a budget, as a hypothesis until it is measured or decided.
6. When a section does not apply to this project, keep its marker and heading and say so in one sentence with the reason.
7. Every string shaped like an ID must name something that exists. In an example of a naming pattern, write the pattern, such as `<ID>-<slug>`, and never a made-up ID.
8. Sample data, such as an invented date or amount in an example, belongs in the document's examples or test-scenarios section. Anywhere else, a date or an amount needs a question, an input or a source behind it.
9. A test scenario ID is `<AREA>-T<NN>`, numbered in one sequence per area across all documents. Search `docs/` for the area's highest number before you add one.
10. Run `python3 .mirage/check.py check --only docs,refs,links,prd,secrets` and fix what it reports for this document. The output is sorted by path. Leave `index-stale` for the last step, which regenerates the index.

Done for a document when the check reports nothing for its path.

## 3. Requirements

The PRD owns requirements. Each one is one testable obligation.

- IDs are `REQ-<AREA>-<NNN>`, with the area declared in the requirement areas table.
- Never renumber an ID. A withdrawn requirement keeps its row with scope `OUT` and a note.
- Scope is `MUST`, `SHOULD`, `MAY` or `OUT`, and release is a project release.
- Other documents cite requirement IDs and never restate a requirement in different words.
- A requirement that cannot be tested as written is not finished. Give it a measure, a named field or an example.

## 4. Screens and pages

`docs/ux.md` holds the screen inventory. Each row links to its spec at `docs/specs/<component id>/<Name>.md` with a Markdown link, so a missing spec is reported as `link-broken`. Write each spec from `templates/screen.md` straight after the inventory. Until the last one exists, `link-broken` for the others is expected. A spec must name:

- its requirements
- the endpoints or data it uses
- its analytics events, when analytics is on
- every state
- checklist acceptance criteria

## 5. Decisions and terms

When a decision is hard to reverse, surprising without context and the result of a real trade-off, record it as an ADR through the `domain-modeling` skill and cite it as `ADR-NNNN`. Add new project terms to `CONTEXT.md` the same way.

## 6. Delivery conventions, AGENTS.md and CLAUDE.md

`docs/delivery.md` is the project's own reference for how work is written, tracked and finished, so the project stays usable without mirage installed. Most of its template is standard wording. Fill the project's parts from the answers: the definition of done, the lanes, the tracker and the working agreements.

Write `AGENTS.md` from `templates/agents.md` and keep it short, because agents load it in every session. Point to `docs/delivery.md` for the detail.

- Read the lint, type-check, test and build commands from the build files when code exists.
- Before any code exists, write the commands the chosen stack will use, cite the question that chose the stack, and mark them as planned until the scaffolding story lands.

When `CLAUDE.md` does not exist, create it with the single line `@AGENTS.md`. When it exists, add that line to it.

## 7. README and summary

- **README.md.** When the project has none, write a short one: what the product is, its status, how to run it once code exists, its license, how to contribute or report a problem, and a Documentation section linking `docs/README.md`, `docs/summary.md` and `AGENTS.md`. When one exists, add only what is missing from that list. For a public project, the license file, the contribution guide and the security policy are files someone must write, so `mirage-backlog` plans them as items.
- **docs/summary.md.** Write it last, from `templates/summary.md`. It is the one page for someone who will read nothing else, so use plain words and no requirement IDs outside the open-decisions list.

## 8. Updating after a change

When answers change, find every document that cites the changed questions, with a search such as `grep -rn "Q-012" docs AGENTS.md`. Rewrite only the affected sections. Rerun the check for each changed document. Then bring `docs/summary.md` up to date, because it restates the others.

## Finish

Run `python3 .mirage/check.py index`, then `python3 .mirage/check.py docs-ready`.

Done when the only thing it still reports is the audit log, either missing or without a `Documents` entry, which `mirage-audit` writes, and `plan` shows every other planned document as existing.

Report which documents you wrote or changed and which open questions you added. The next phase is `mirage-audit`, and then `mirage-backlog`.
