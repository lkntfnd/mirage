---
name: mirage-interview
description: Interviews a project's owner until every decision its documentation needs is settled, one round of questions at a time, each with a recommended answer the owner can accept or delegate. Records answers in docs/questions.md and needed information, assets, accounts, access and tools in docs/inputs.md. Use when starting mirage documentation, when `check.py plan` shows uncovered areas, or when a change request adds scope to a documented project.
---

# Mirage interview

You interview the owner until every question area of every planned document is settled, delegated or recorded as an open question. The validator decides when you are done, not your sense that enough was asked.

## 1. Load the interview skills

Invoke the `grilling` skill and the `domain-modeling` skill with the Skill tool, both of them, before the first question.

- `grilling` sets the method: a design tree worked in rounds, the whole frontier asked each round, and a recommended answer on every question.
- `domain-modeling` keeps `CONTEXT.md` and `docs/adr/` current as terms and hard-to-reverse decisions settle.

Everything below adds mirage's rules to theirs.

## 2. Read before you ask

Facts are your job. Before round one, read the codebase, the README, existing docs, `docs/sources/`, `.mirage/project.json` and both registers when they exist. Ask the owner only what those cannot answer, and state what you found when it shapes a recommendation.

When the owner hands you source documents, such as a client brief, save them unchanged under `docs/sources/`. Set the `source_documents` flag and write `docs/sources/SHA256SUMS` with one `<sha256>  <path>` line per file.

## 3. Settle the facets first

Round one settles `.mirage/project.json`. Recommend a value for every field from what you read. [references/project-json.md](references/project-json.md) lists the fields and the allowed values.

Write the file as soon as the owner settles it. Then run `python3 .mirage/check.py plan --json`. The planned documents and their areas are your design tree. Area keys look like `prd/users` or `integration:stripe/auth`.

Done when `plan` runs and lists the planned documents.

## 4. Work the tree in rounds

Order the branches so answers flow downhill. Start with the PRD (problem, users, scope, releases), then architecture, then the component documents, then the cross-cutting ones. A question that depends on an unanswered one waits for a later round.

For every question:

- Give a recommendation with its reason, drawn from the project's facts and common practice for this kind of product.
- Offer choices when the space is small.
- When the answer is a fact you could look up, look it up instead of asking.

Record each question in `docs/questions.md` the moment it is asked. Record its answer the moment the owner gives it. Never batch. [references/registers.md](references/registers.md) gives the exact entry formats and the rule for choosing the next ID.

- `Covers` lists every area key the question settles. An area may need several questions, and one question may settle several areas.
- "Not applicable" is an answer. Record it with the reason, and it covers the area.
- An answer that needs someone outside the conversation stays open with an `Owner`. Tell the owner they can send such questions out with `/to-questionnaire` in Claude Code or `$to-questionnaire` in Codex.

## 5. Ask for inputs

For each planned document, ask whether its typical inputs exist. `plan` lists them per document. Record every input the project needs in `docs/inputs.md`, including the ones already at hand:

- `missing` needs a `How to get` that tells the owner exactly how to obtain it.
- `provided` needs a `Location`, such as a path, a URL or a named password manager entry. Never write a secret itself.
- `not-needed` needs a reason.

## 6. Let a busy owner delegate

The owner may say "use your recommendations", or words to that effect, for:

- one question
- the current round
- one document
- everything left

Then, for every question in that scope:

1. Make sure the question is written in the register with its recommendation.
2. Set `Status: delegated`, and set `Answer: <the recommendation>. Delegated on <YYYY-MM-DD>.`

Tell the owner how many answers you delegated and that the documentation index lists them for confirmation. A delegated answer counts as settled at once.

Delegating everything left still means writing every question. The register must show each decision and who made it.

## 7. Never invent

Estimates, dates, prices, vendor accounts, credentials and approvals come only from the owner or from evidence. When the owner has no answer, the question stays open with your recommendation. Mirage's documents cite it as `(Q-nnn)` until it closes.

## Finish

The interview is complete when both of these hold:

- `python3 .mirage/check.py plan` shows no uncovered area.
- `python3 .mirage/check.py check --only register,coverage` shows no `register-*`, `inputs-*` or `coverage-area` error. `coverage-req` waits for the backlog.

Report the numbers of answered, delegated and open questions and of missing inputs. The next phase is `mirage-docs`.
