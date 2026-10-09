---
name: mirage-interview
description: Interviews a project's owner until every decision its documentation needs is settled, one round of questions at a time, each with a recommended answer the owner can accept or delegate. Records answers in docs/questions.md and needed information, assets, accounts, access and tools in docs/inputs.md. Use when starting mirage documentation, when `check.py plan` shows uncovered areas, when `check.py docs-ready` says the documentation is not sufficient to plan tasks, or when a change request adds scope to a documented project.
---

# Mirage interview

You interview the owner until every question area of every planned document is settled, delegated or recorded as an open question. The validator decides when you are done, not your sense that enough was asked.

## 1. Load the interview skills

Invoke the `grilling` skill and the `domain-modeling` skill with the Skill tool, both of them, before the first question. `grilling` is the engine behind `/grill-me`.

- `grilling` sets the method: a design tree worked in rounds, the whole frontier asked each round, and a recommended answer on every question.
- `domain-modeling` keeps the glossary and `docs/adr/` current as terms and hard-to-reverse decisions settle. The glossary is `GLOSSARY.md`, or `CONTEXT.md` with an older version of that skill. Use whichever name the installed skill writes, and never keep both.

Everything below adds mirage's rules to theirs.

## 2. Read before you ask

Facts are your job. Before round one, read the codebase, the README, existing docs, `docs/sources/`, `.mirage/project.json` and both registers when they exist. Ask the owner only what those cannot answer, and state what you found when it shapes a recommendation.

When the owner hands you source documents, such as a client brief, save them unchanged under `docs/sources/` and set the `source_documents` flag. Then write `docs/sources/SHA256SUMS` by running `shasum -a 256 <files>` inside `docs/sources/`, so each line is `<sha256>  <path relative to docs/sources/>`.

## 3. Settle what is being built

Round one is about the thing itself. Mirage has no fixed list of project kinds, so do not start from one. Have the owner describe what they are building in their own words, unless the sources and the codebase already say it. Then turn that description into `.mirage/project.json`, with a recommended value for every field. [references/project-json.md](references/project-json.md) lists the fields.

1. **Components.** Name every part that is built and delivered on its own, and give each an ID and a kind. Use a catalog kind when it describes the part, because it switches on that kind's documents. When no catalog kind describes it, name the kind in your own slug, such as `terraform-module` or `sensor-board`. Never force a part into a kind that does not describe it. A part of any other kind gets a component specification, which asks what it is for, what crosses its boundary, where it runs, how it is built and delivered, what it must achieve and how that is proved.
2. **Flags and lists.** Set each flag from what the owner described. List the outside systems, the regulations and the rule sets that need their own document.
3. **Releases and lanes.** Name the releases in order, and the areas that will build the parts.
4. **Show the plan.** Write the file, run `python3 .mirage/check.py plan`, and tell the owner in a few lines which documents it plans and why.
5. **Ask what the plan lacks.** Put this to the owner as its own question: what must be written down for this project that these documents do not hold? Recommend additions yourself from what you have learned.
   - A catalog document that no facet switched on goes into `include`. `plan` ends with the catalog documents that are available by name.
   - Anything the catalog does not have becomes a project document in `documents`. Agree three things with the owner for each one: its title, its outline as sections, and the questions it must answer as areas.
6. Run `plan` again.

The file is the record of these decisions. Add a question for one only when the owner chose between real alternatives, and leave its `Covers` empty unless it also settles a listed area. Record the owner's answer to step 5 as a question in the same way.

Then run `python3 .mirage/check.py plan --json`. The planned documents and their areas are your design tree. Area keys look like `prd/users`, `integration:stripe/auth` or `component:sensor-board/interfaces`.

Done when `plan` lists the planned documents and the owner has answered step 5.

## 4. Work the tree in rounds

Order the branches so answers flow downhill. Start with the PRD (problem, users, scope, releases), then architecture, then the documents for each component, then the cross-cutting ones, then the project's own documents, then delivery. A question that depends on an unanswered one waits for a later round.

When an answer raises a topic that no planned document holds, do not squeeze it into the nearest one. Propose a project document for it, add it to `documents` when the owner agrees, and run `plan` again.

For every question:

- Give a recommendation with its reason, drawn from the project's facts and common practice for this kind of product.
- Offer choices when the space is small.
- When the answer is a fact you could look up, look it up instead of asking.

Record each question in `docs/questions.md` the moment it is asked. Record its answer the moment the owner gives it. Never hold answers back to write them in one batch at the end. [references/registers.md](references/registers.md) gives the exact entry formats and the rule for choosing the next ID.

- `Covers` lists every area key the question settles. An area may need several questions, and one question may settle several areas.
- "Not applicable" is an answer. Record it with the reason, and it covers the area.
- An answer that needs someone outside the conversation stays open with an `Owner`. Tell the owner they can send such questions out with `/to-questionnaire` in Claude Code or `$to-questionnaire` in Codex.

## 5. Ask for inputs

`plan` lists typical inputs per document. They are prompts, and the validator does not require an entry for each. For each one that applies to this project, ask whether it exists, and record it in `docs/inputs.md`:

- `missing` needs a `How to get` that tells the owner exactly how to obtain it.
- `provided` needs a `Location`, such as a path, a URL or a named password manager entry. Never write a secret itself.

- `not-needed` needs a `Reason`. Use it only where a reader would otherwise expect the input.

Skip a typical input that plainly does not apply, such as hosting access for a tool that runs on the user's machine.

## 6. Let a busy owner delegate

The owner may say "use your recommendations", or words to that effect, for:

- one question
- the current round
- one document
- everything left

Then, for every question in that scope:

1. Make sure the question is written in the register with its recommendation.
2. Set `Status: delegated`, and set `Answer: <the recommendation>. Delegated on <YYYY-MM-DD>.` Write the decision out in full, never "as recommended". The index shows the answer without the recommendation, and the owner confirms from that list.

Inside a delegated scope, `grilling`'s rule to wait for the owner's reply does not apply. Write the questions, record them as delegated and move on without pausing. Outside that scope, keep waiting for answers as `grilling` says.

Tell the owner how many answers you delegated and that the documentation index lists them for confirmation. A delegated answer counts as settled at once.

Delegating everything left still means writing every question. The register must show each decision and who made it.

Delegation covers decisions, never facts. A question whose answer is an estimate, a date, a price, a target number, an account or an approval stays `open` inside a delegated scope, with your recommendation, because step 7 lets only the owner or evidence supply those. Tell the owner which questions you kept open for that reason.

Three cases sit near that line:

- A target number is one the product promises, such as an accuracy or a response time in a requirement. It stays open. A value inside the design, such as a timeout or a sampling interval, is yours to set and mark as a hypothesis.
- A working agreement, such as how long a spike may run or how much work a lane has in progress, is a decision. Delegation covers it.
- A decision that only a measurement, an experiment, a datasheet or an outside ruling can settle is neither the owner's guess nor yours. Keep it open and say what would settle it. `mirage-backlog` plans a spike that answers it.

A standing delegation, such as "everything left", also covers questions that come up later while documents are written, audited or planned. Record each of those as delegated in the same way.

## 7. Never invent

Estimates, dates, prices, vendor accounts, credentials and approvals come only from the owner or from evidence. When the owner has no answer, the question stays open with your recommendation. Mirage's documents cite it as `(Q-nnn)` until it closes.

## 8. Closing gaps before planning

When you were called because `python3 .mirage/check.py docs-ready` did not print `sufficient`, or because open questions block work the owner wants planned, do not rerun the whole interview. Scope it to the gaps:

- every uncovered area the command reports
- every open question it lists, most-blocking first, put to the owner again with your recommendation and the work it holds up
- every decision a document made that no question records, which `mirage-audit` reports

For each open question the owner settles it, delegates it or says it stays open. A question that stays open is fine. The stories that depend on it will be planned as blocked, and the owner knows why.

## Finish

The interview is complete when both of these hold:

- `python3 .mirage/check.py plan` shows no uncovered area.
- `python3 .mirage/check.py check --only register,coverage` shows no `register-*`, `inputs-*` or `coverage-area` error. `coverage-req` waits for the backlog.

Report the numbers of answered, delegated and open questions and of missing inputs. The next phase is `mirage-docs`.
