---
status: accepted
---

# The backlog is planned only from documentation that passes a sufficiency check

`mirage-backlog` writes no item until `check.py docs-ready` prints `sufficient`: every planned document exists with nothing left unfilled, every question area is covered, the registers and the PRD are valid, and a documents audit is logged. When the check fails, mirage does not plan around the gap. It goes back to the owner through the `grilling` interview, scoped to what is missing, then updates the documents and checks again. A task written from thin documents carries a guess into every lane that picks it up, and a wrong task costs more than a late one.

Decided by the owner on 2026-10-08.

## Consequences

- The phase order is interview, documents, documents audit, backlog, backlog audit, then sync.
- An open question does not fail the check. The check lists every open question, mirage puts the ones that block the next release to the owner, and stories that depend on a question left open are planned as blocked.
- The owner can also start the interview by hand with `/grill-me`. Other skills cannot call `/grill-me`, so mirage calls `grilling`, the skill behind it.
