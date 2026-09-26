<!-- mirage:doc agents -->
# Agent rules

<!-- mirage:section read-first -->
## Read first

Read the [PRD](docs/prd.md), the [question register](docs/questions.md) and the backlog before starting.

<!-- mirage:section authority -->
## Scope and authority

Agents implement ready items only; the shop owner decides scope (Q-006).

<!-- mirage:section lanes -->
## Lanes

One agent owns the `mobile` lane and one owns the `backend` lane.

<!-- mirage:section workflow -->
## Picking and finishing work

Pick a ready item in your lane, finish it, record evidence and run the check.

<!-- mirage:section conventions -->
## Branches, commits and pull requests

Branches are named after the item ID; commit subjects start with it.

<!-- mirage:section verification -->
## Verification

Run the project's tests and `python3 .mirage/check.py check` before asking for review.

<!-- mirage:section evidence -->
## Evidence

Evidence is a commit SHA with its CI run, recorded in the item's frontmatter.
