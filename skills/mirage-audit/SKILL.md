---
name: mirage-audit
description: Audits a mirage project's documentation and backlog. Runs the validator, then reviews in a fresh context for contradictions between documents, claims with no source, requirements with no acceptance path, missing inputs that block work, stale facets and delegated answers awaiting confirmation. Fixes mechanical defects and turns the rest into questions. Use when mirage-docs or mirage-backlog finishes, before a milestone starts, or when asked to review, audit or sanity-check the project documentation.
---

# Mirage audit

The writer of a document is the worst reviewer of it. You run the validator for the mechanical rules, then review with fresh eyes for what no rule can see. Every finding ends fixed or recorded as a question.

## 1. Run the validator

Run `python3 .mirage/check.py check`. Fix every error before the review. Each code names its rule, and most fixes are local:

- `index-stale` is fixed by running `python3 .mirage/check.py index`.
- A `ref-missing` is a typo or a missing entry.
- A `backlog-ready` means the item's status must follow its prerequisites.

Done when `check` prints `ok`.

## 2. Review in a fresh context

Dispatch a read-only sub-agent with a fresh context, if your environment offers one. If it does not, run the review yourself after re-reading every file from disk. Give the reviewer the project root and these checks. It reports each finding with file, line, the check it fails and the evidence.

1. **Contradictions.** Two documents, or a document and the register, state different facts about the same thing.
2. **Unsourced claims.** A number, date, price, vendor, limit or rule with no question, input, ADR, requirement or verified code fact behind it.
3. **Weak requirements.** A requirement that cannot be tested as written, or with no story whose acceptance criteria would prove it.
4. **Hollow acceptance.** A story whose checklist would pass without the requirement being met.
5. **Blocking inputs.** A missing input that blocks a document or a ready-soon item, and whether its `How to get` is concrete enough to act on.
6. **Stale facets.** A planned document whose facet no longer matches the codebase or the answers, or a facet the codebase implies but `project.json` lacks.
7. **Undecided decisions.** A document section that decides something no question records.
8. **Lane gaps.** A story whose work falls in an area its labels do not name.

## 3. Resolve every finding

| Finding | Resolution |
|---|---|
| Mechanical, such as a wrong citation or a stale sentence that contradicts a settled answer | Fix it now. |
| A decision nobody made | Add an open question with your recommendation, and cite it where the claim was. |
| Two settled answers that conflict | Add an open question naming both answers, and ask the owner. |
| A facet change | Update `.mirage/project.json` with the owner, then run `mirage-interview` and `mirage-docs` for the new plan. |

## 4. Put delegated answers before the owner

List every delegated answer from the documentation index. Group them by document, and show each recommendation and its reason. The owner can confirm them in one pass. A confirmed answer becomes `Status: answered` with "Confirmed by the owner on YYYY-MM-DD.", and a changed answer is recorded the same way with the new text. Then update every document that cites a changed answer.

## Finish

Done when two things hold:

- `python3 .mirage/check.py check` prints `ok` after your fixes.
- Every finding is fixed or recorded as a question.

Report the findings by type, what you fixed, the questions you added, and how many delegated answers await the owner.
