---
name: mirage-audit
description: Audits a mirage project's documentation and backlog. Runs the validator, then reviews in a fresh context for contradictions between documents, claims with no source, requirements with no acceptance path, hollow acceptance criteria, missing inputs that block work, stale facets and delegated answers awaiting confirmation. Fixes mechanical defects, turns the rest into questions, and records each pass in docs/audit-log.md. Use when mirage-docs or mirage-backlog finishes, before tasks are planned, before a milestone starts, or when asked to review, audit or sanity-check the project documentation.
---

# Mirage audit

The writer of a document is the worst reviewer of it. You run the validator for the mechanical rules, then review with fresh eyes for what no rule can see. Every finding ends fixed or recorded as a question, and every pass is recorded in the audit log.

An audit has a scope:

- **Documents.** Run before any task is planned. `mirage-backlog` will not start until this pass is logged.
- **Backlog.** Run after items are written or changed, and before a milestone starts.

When the backlog exists, audit both.

## 1. Run the validator

Run `python3 .mirage/check.py check`. Fix every error it reports for the scope you audit. Each code names its rule, and most fixes are local:

- `index-stale` is fixed by running `python3 .mirage/check.py index`.
- A `ref-missing` is a typo or a missing entry.
- A `backlog-ready` or `backlog-section` means the item's status must follow its prerequisites and its written sections.

Before the first documents audit, `doc-missing` for `docs/audit-log.md` is expected, and `docs-ready` reports `audit-missing` until the log holds a `Documents` entry. Step 5 writes that entry. Before a backlog exists, `coverage-req` is expected too.

## 2. Review in a fresh context

Dispatch a read-only sub-agent with a fresh context, if your environment offers one. If it does not, run the review yourself after re-reading every file from disk. Give the reviewer the project root and the checks for the scope. It reports each finding with file, line, the check it fails and the evidence.

Checks on the documents:

1. **Contradictions.** Two documents, or a document and the register, state different facts about the same thing.
2. **Unsourced claims.** A number, date, price, vendor, limit or rule with no question, input, ADR, requirement or verified code fact behind it.
3. **Weak requirements.** A requirement that cannot be tested as written.
4. **Blocking inputs.** A missing input that blocks a document or planned work, and whether its `How to get` is concrete enough to act on.
5. **Stale facets.** A planned document whose facet no longer matches the codebase or the answers, or a facet the codebase implies but `project.json` lacks.
6. **Undecided decisions.** A document section that decides something no question records.
7. **Stale summary.** `docs/summary.md` says something the other documents, the registers or the backlog no longer support.

Checks on the backlog:

8. **Unproven requirements.** A requirement with no story whose acceptance criteria would prove it.
9. **Hollow acceptance.** A story whose checklist would pass without the requirement being met, or whose verification names nothing that can be run or observed.
10. **Wrong edges.** A `blocked_by` that does not truly gate the item, or a real dependency that is missing, including work another lane must deliver first.
11. **Lane gaps.** An item whose work falls in an area its labels do not name, or outside the paths `docs/delivery.md` gives that lane.

## 3. Resolve every finding

| Finding | Resolution |
|---|---|
| Mechanical, such as a wrong citation or a stale sentence that contradicts a settled answer | Fix it now. |
| A decision nobody made | Add a question with your recommendation, and cite it where the claim was. It is `open`, or `delegated` when the owner's standing delegation covers it. |
| Two settled answers that conflict | Add an open question naming both answers, and ask the owner. |
| A facet change | Update `.mirage/project.json` with the owner, then run `mirage-interview` and `mirage-docs` for the new plan. |
| A backlog defect | Fix the item. When the fix needs a decision, add the question to the item's `questions` and set the item to blocked. |

## 4. Put delegated answers before the owner

List every delegated answer from the documentation index. Group them by document, and show each recommendation and its reason. The owner can confirm them in one pass. When the owner is not there to answer, report the list and the count, and leave the statuses as they are. A confirmed answer becomes `Status: answered` with "Confirmed by the owner on YYYY-MM-DD.", and a changed answer is recorded the same way with the new text. Then update every document that cites a changed answer.

## 5. Record the pass

Append an entry to `docs/audit-log.md`, creating the file with an `# Audit log` heading when it does not exist. Never rewrite earlier entries.

```markdown
## 2026-10-08 Documents

- Reviewed: 21 documents, 96 questions, 14 inputs.
- Findings: 3 contradictions, 1 unsourced claim, 2 weak requirements.
- Fixed: 4. Questions added: Q-097, Q-098.
- Left for the owner: 31 delegated answers to confirm.
```

Use the date of the pass, the scope (`Documents`, `Backlog` or `Documents and backlog`), real counts and the IDs of the questions you added. Write the heading exactly in this form and keep the scope word in English, in every project language. `docs-ready` reads it to know that the documents were audited.

## Finish

Done when three things hold:

- `python3 .mirage/check.py check` prints `ok`, apart from `coverage-req` when no backlog exists yet.
- Every finding is fixed or recorded as a question.
- The pass is recorded in `docs/audit-log.md`.

Report the findings by type, what you fixed, the questions you added, and how many delegated answers await the owner.
