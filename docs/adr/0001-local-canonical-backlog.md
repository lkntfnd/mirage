---
status: accepted
---

# The repository is the only source of truth; trackers are projections

Mirage writes every document and every backlog item as a file in the project's repository first. A tracker such as Plane, Jira, GitHub Issues or Linear holds only a projection that people use as a board view. Local files can be validated, diffed and reviewed in a pull request, and a rerun of the sync matches items by ID instead of creating duplicates. Writing straight to a tracker loses all three.

Decided by the owner on 2026-09-26.

## Consequences

- An edit made in the tracker does not change the plan until it reaches the files. How status and assignee edits flow back is decided separately.
- Mirage never needs tracker credentials to plan. Only the sync step does.
