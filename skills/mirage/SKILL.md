---
name: mirage
description: Start or continue mirage in this project. Sets up .mirage/, checks the required skills, reports where the documentation and backlog stand, and runs the next phase.
disable-model-invocation: true
---

# Mirage

Mirage takes a project from idea to a complete, validated documentation set and a local backlog that agents build from. You run its phases in order and stop only where the owner must decide.

Mirage's vocabulary is fixed. The owner makes decisions, a question is a decision recorded in `docs/questions.md`, an input is something needed from outside the conversation recorded in `docs/inputs.md`, and the backlog in `backlog/` is the only source of truth for planned work.

## 1. Check the required skills

Mirage's interview runs on Matt Pocock's `grilling` and `domain-modeling` skills. Confirm both are in your available skills.

If either is missing, stop and tell the owner how to install them:

- **Claude Code.** `/plugin install mattpocock-skills@claude-plugins-official`, then `/reload-plugins`.
- **Codex and other agents.** `npx skills@latest add mattpocock/skills`, selecting `grilling`, `domain-modeling` and `to-questionnaire`.

Done when both skills are available.

## 2. Set up .mirage/

The validator lives in the project so the project's CI can run it without mirage installed.

- If `.mirage/check.py` is absent, create `.mirage/` and copy `scripts/check.py` and `scripts/catalog.json` from this skill's folder into it.
- If it is present, compare its `MIRAGE_VERSION` with this skill's copy. When this skill's copy is newer, tell the owner, and copy both files over when the owner agrees. Updating changes files in their repository.

Every later step runs the validator as `python3 .mirage/check.py <command>` from the project root. Python 3.9 or newer is required.

Done when `python3 .mirage/check.py version` prints a version.

## 3. Read the project state

Collect the state before choosing a phase:

- whether `.mirage/project.json` exists
- `python3 .mirage/check.py plan --json`, giving the planned documents, which exist, and which question areas are uncovered
- `python3 .mirage/check.py check --json`, giving every validation error
- whether `backlog/` holds items
- `python3 .mirage/check.py ready`, giving what can start now per lane

Tell the owner in a few lines what exists, what is missing, how many questions are open, how many delegated answers await confirmation, and how many inputs are missing.

## 4. Run the next phase

Pick the first phase that applies and invoke its skill. After it finishes, read the state again and continue with the next phase. Stop only when the owner stops you or a phase needs the owner.

| Condition | Phase |
|---|---|
| No `project.json`, or any question area is uncovered | `mirage-interview` |
| A planned document is missing or still has `{{` placeholders | `mirage-docs` |
| No backlog, or `coverage-req` or `backlog-*` errors | `mirage-backlog` |
| Any other `check` error, or no audit since the last change | `mirage-audit` |
| The owner wants a tracker board | `mirage-sync` |

For a change request on a documented project, run the same phases on the change only. First run `mirage-interview` for the new decisions, then `mirage-docs` for the affected documents, then `mirage-backlog` for the new or changed items, then `mirage-audit`.

## 5. Keep the validator in CI

When the project has CI and no step runs the validator yet, add one that runs `python3 .mirage/check.py check` on every pull request. [references/ci.md](references/ci.md) has ready-made steps for common CI services. Done when the step exists, or the owner declined it.

## Finish

End with a short status. Say which phases ran and whether `check` is clean. Give the counts of open questions, delegated answers awaiting confirmation and missing inputs. Finish with the ready set per lane.
