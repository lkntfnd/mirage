---
name: mirage-sync
description: Projects a mirage backlog into a tracker (Plane, Jira, GitHub Issues or Linear) as a board view, and pulls item status back into the local files, which stay the only source of truth. Idempotent, so reruns never duplicate items. Use when asked to sync, push or publish the backlog to a tracker, to create milestones, epics, stories and tasks in Plane, Jira, GitHub or Linear, or to pull tracker status into the backlog.
---

# Mirage sync

The backlog files are the plan. The tracker is a board that people look at. You push the plan to the board and pull only status back. The validator computes every operation, and you carry them out with the tracker's tools.

## 1. Pick the tracker and its adapter

Ask the owner which tracker and which project or repository to use, unless `.mirage/trackers/<tracker>.json` already names them under `settings`. Read the adapter for that tracker:

| Tracker | Adapter |
|---|---|
| Plane | [references/plane.md](references/plane.md) |
| Jira Cloud | [references/jira.md](references/jira.md) |
| GitHub Issues | [references/github.md](references/github.md) |
| Linear | [references/linear.md](references/linear.md) |

For any other tracker, map mirage's levels, labels, statuses and links onto it by the same pattern. Tell the owner which parts of the mapping you could not verify.

Store the non-secret settings under `settings` in `.mirage/trackers/<tracker>.json`, such as the workspace, project key or repository. Credentials stay in the environment or in the tracker's own MCP or CLI login, and never go into a file.

## 2. Check capabilities

Follow the adapter's capability checks before the first write, such as whether the project has epics, sub-items, milestones, relations and custom states. When one is missing, use the adapter's named fallback and tell the owner which one.

## 3. Confirm before the first push

Writing to a tracker is visible to other people. Run `python3 .mirage/check.py sync-plan <tracker>`, count the operations by kind, and show the owner the counts and the target project. Push only after the owner agrees. Later runs against the same project need no new confirmation unless they create more than they did before or target another project.

## 4. Push until the plan is empty

1. Run `python3 .mirage/check.py sync-plan <tracker>`. It prints one JSON operation per line, and prints nothing when the tracker is in step.
2. Carry out each operation in order with the adapter's call.
3. After each successful call, record it at once:
   - `python3 .mirage/check.py sync-record <tracker> --id <ID> --remote-id <remote id> --key <key> --url <url>` for a create or update
   - `--link FROM TO` or `--unlink FROM TO` for a relation
4. Run `sync-plan` again.

Repeat until it prints no operations. When a call fails, stop and report the operation and the error. The map is already correct for everything recorded, so a rerun continues where you stopped.

Never delete a tracker item. An `orphan` operation means a mapped item's file is gone. Report it to the owner with its tracker key and URL, then run `python3 .mirage/check.py sync-record <tracker> --forget <ID>` so the plan converges.

## 5. Pull status back

For every mapped item, read its tracker state and map it to a mirage status with the adapter's table. When the two differ, apply it with `python3 .mirage/check.py set-status <ID> <status>`.

A tracker "done" needs evidence, such as a linked pull request or commit. Without evidence, set the item to `in-review` and tell the owner which items lack it.

## 6. Report drift

Status is the only field that comes back from the tracker. When a tracker item's title, body, labels or parent differ from what was pushed, list it as drift. The next push overwrites it, unless the owner first copies the change into the file.

## Finish

Done when three things hold:

- `sync-plan` prints no operations.
- Every status difference is applied or reported.
- `python3 .mirage/check.py check` prints `ok`.

Report the created, updated and linked counts, the pulled status changes, the items awaiting evidence, the drift and the orphans.
