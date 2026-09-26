<!-- mirage:doc agents -->
# Agent rules

{{One paragraph: which agents build this project, such as Claude Code, Codex or others, and that this file is the one place their operating rules live. State that CLAUDE.md carries only the line @AGENTS.md so every agent reads the same rules.}}

<!-- mirage:section read-first -->
## Read first

{{List the read-first order: this file, then CONTEXT.md for the project's vocabulary, then docs/README.md for the reading order, then docs/prd.md for the requirements, then docs/questions.md for settled and open decisions. Add any other document a new contributor must read before touching code, such as docs/architecture.md.}}

<!-- mirage:section authority -->
## Scope and authority

{{State the authority order: the owner's latest instruction in the conversation wins, then an answered or delegated question in docs/questions.md, then the PRD, then every other document. State that no agent invents an estimate, a date, a price, a credential or an approval, and that a missing fact becomes a question in docs/questions.md, citing the requirement or story it blocks.}}

<!-- mirage:section lanes -->
## Lanes

{{State how many lanes this project has and whether one agent covers every lane or several agents split the work.}}

| Lane | Area label | Owns | Contract with other lanes |
|---|---|---|---|
| {{Lane name}} | area:{{area}} | {{Paths this lane may edit}} | {{What this lane promises the others, such as a frozen API contract}} |

{{State that an item carrying more than one area label names its owning lane, that no lane edits another lane's paths, and the one exception this project allows, if any, such as a shared CI file edited only in a pull request that touches nothing else in it.}}

<!-- mirage:section workflow -->
## Picking and finishing work

{{Instruct the agent to run `python3 .mirage/check.py ready`, pick only items in its own lane, read the story's acceptance criteria, requirement links and blockers before starting, move status only with `python3 .mirage/check.py set-status <ID> <STATUS>`, reach done only with a commit SHA and its CI run as evidence, and run the ready check again at the end of every session.}}

<!-- mirage:section conventions -->
## Branches, commits and pull requests

{{State the base branch, the branch name pattern using the backlog ID, for example `feature/<ID>-<slug>`, that staging uses explicit paths only, the commit subject format naming the task ID, and the pull request title and body format linking the requirements and questions it settles. Name who reviews and who may merge.}}

<!-- mirage:section verification -->
## Verification

{{List the exact lint, type-check, test and build commands for each component, plus `python3 .mirage/check.py check` before any commit that touches docs or the backlog. State that a command that cannot run, such as missing CI access, counts as unverified work, never a pass.}}

<!-- mirage:section evidence -->
## Evidence

{{Define evidence as a commit SHA together with the CI run it triggered, checked on that exact commit. State where evidence is recorded, such as a comment on the backlog item or the pull request description, and that a test double or a fake response proves the code compiles, never that a live integration works.}}
