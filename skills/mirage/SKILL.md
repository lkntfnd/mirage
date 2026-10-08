---
name: mirage
description: Start or continue mirage in this project. Sets up .mirage/, checks the required skills, reports where the documentation and backlog stand, and runs the next phase. Use when the owner types /mirage, or asks to start, continue or check the project's mirage documentation and backlog.
disable-model-invocation: true
---

# Mirage

Mirage takes a project from idea to a complete, validated documentation set and a local backlog that agents build from. You run its phases in order and stop only where the owner must decide.

Mirage's vocabulary is fixed. The owner makes decisions, a question is a decision recorded in `docs/questions.md`, an input is something needed from outside the conversation recorded in `docs/inputs.md`, and the backlog in `backlog/` is the only source of truth for planned work. A tracker such as Plane or Jira only shows that backlog as a board.

## 1. Check the required skills

Mirage's interview runs on Matt Pocock's `grilling` and `domain-modeling` skills. Confirm both are in your available skills.

If either is missing, stop and tell the owner how to install them:

- **Claude Code.** `/plugin install mattpocock-skills@claude-plugins-official`, then `/reload-plugins`.
- **Codex and other agents.** `npx skills@latest add mattpocock/skills`, selecting `grilling`, `grill-me`, `domain-modeling` and `to-questionnaire`.

Done when both skills are available.

## 2. Set up .mirage/

The validator lives in the project so the project's CI can run it without mirage installed.

- If `.mirage/check.py` is absent, create `.mirage/` and copy `scripts/check.py` and `scripts/catalog.json` from this skill's folder into it.
- If it is present, compare it with this skill's copy, by `MIRAGE_VERSION` and then by content. When this skill's copy is newer, or is the same version with different content, tell the owner, and copy both files over when the owner agrees. Updating changes files in their repository. A newer validator can report things the older one accepted, so run `python3 .mirage/check.py check` after an update and fix what it reports first.

Every later step runs the validator as `python3 .mirage/check.py <command>` from the project root. Python 3.9 or newer is required.

Done when `python3 .mirage/check.py version` prints a version.

## 3. Read the project state

When `.mirage/project.json` does not exist, this is a new project. Skip the commands below, because each one needs that file, and go to `mirage-interview`.

Otherwise collect the state before choosing a phase:

- `python3 .mirage/check.py plan`, giving the planned documents, which exist, and which question areas are uncovered
- `python3 .mirage/check.py docs-ready`, saying whether the documentation is sufficient to plan work, and listing the open questions
- `python3 .mirage/check.py check --json`, giving every validation error
- whether `backlog/` holds item files, not counting the generated `backlog/README.md`, and `python3 .mirage/check.py ready`, giving what can start now per lane

Tell the owner in a few lines what exists, what is missing, how many questions are open, how many delegated answers await confirmation, and how many inputs are missing.

`check --only` takes any of these groups, comma-separated: `project`, `docs`, `index`, `register`, `prd`, `refs`, `coverage`, `backlog`, `sources`, `links`, `secrets`.

## 4. Run the next phase

Pick the first row that applies and invoke its skill. After it finishes, read the state again and continue. Stop only when the owner stops you or a phase needs the owner.

| Condition | Phase |
|---|---|
| No `project.json`, or any question area is uncovered | `mirage-interview` |
| A planned document is missing or still has `{{` placeholders | `mirage-docs` |
| The documents were never audited, so `docs/audit-log.md` is missing or holds no `Documents` entry | `mirage-audit` |
| `docs-ready` prints `sufficient`, and there is no backlog or `check` reports `coverage-req` or `backlog-*` errors | `mirage-backlog` |
| Any other `check` error, or the backlog changed since the last audit entry | `mirage-audit` |
| The owner wants a tracker board | `mirage-sync` |

**The backlog waits for the documentation.** Never start `mirage-backlog` while `docs-ready` is not `sufficient`. Tasks written from thin documents carry guesses into every lane. Close the gaps first: `mirage-interview` for missing decisions, then `mirage-docs`, then `mirage-audit`.

For a change request on a documented project, run the same phases on the change only: `mirage-interview` for the new decisions, `mirage-docs` for the affected documents, `mirage-audit`, then `mirage-backlog` for the new or changed items.

The owner can run `/grill-me` at any time to stress-test one decision in depth. Afterwards run `/mirage` again, so `mirage-interview` records what was decided.

## 5. Keep the validator in CI

When the project has CI and no step runs the validator yet, add one that runs `python3 .mirage/check.py check` on every pull request. [references/ci.md](references/ci.md) has ready-made steps for common CI services. Done when the step exists, or the owner declined it.

## Finish

End with a short status:

- which phases ran
- whether `docs-ready` and `check` are clean
- the counts of open questions, delegated answers awaiting confirmation and missing inputs
- the ready set per lane
