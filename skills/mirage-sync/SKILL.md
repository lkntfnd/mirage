---
name: mirage-sync
description: Projects a mirage backlog into a tracker (Plane, Jira, GitHub Issues or Linear) as a board view, and pulls item status back into the local files, which stay the only source of truth. Idempotent, so reruns never duplicate items, and it reports edits people made in the tracker before replacing them. Use when asked to sync, push or publish the backlog to a tracker, to create milestones, epics, stories and tasks in Plane, Jira, GitHub or Linear, or to pull tracker status into the backlog.
---

# Mirage sync

The backlog files are the plan. The tracker is a board that people look at. You push the plan to the board and pull only status back. The validator computes every operation, and you carry them out with the tracker's tools.

What mirage owns in the tracker is each item's title, description, labels, parent, milestone, priority, estimate, due date and blocking links. Status is shared: mirage pulls it first, then pushes the file's status for items that changed locally. Everything else belongs to the people using the board: comments, attachments, assignees, watchers and any field mirage does not write. Never change or remove those.

## 1. Pick the tracker and its adapter

Ask the owner which tracker and which existing project or repository to use, unless `.mirage/trackers/<tracker>.json` already names them under `settings`. Use a project that exists. Never create a workspace or a project, and never pick a replacement when the named one is not found. Stop and ask.

Read the adapter for that tracker:

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

Some adapters need a change to the project's own configuration, such as a new workflow state, an estimate scale or a set of status labels. That changes the board for everyone who uses it. Make no such change yet. Collect them for the confirmation in step 4.

## 3. Pull status and find drift first

Do this before any push, so nothing a person did on the board is lost.

For every item already in the map, read it from the tracker.

- **Status.** Map its tracker state to a mirage status with the adapter's table. When that differs from the file, apply it with `python3 .mirage/check.py set-status <ID> <status>`. A tracker "done" needs evidence, such as a linked pull request or commit. Without evidence, set the item to `in-review` and tell the owner which items lack it.
- **Drift.** Run `python3 .mirage/check.py sync-expect <tracker>`. It prints, for each mapped item with no local change pending, exactly what mirage last pushed. When the tracker item's title, labels or parent differ from that, or its description differs in more than formatting, a person edited it. List every such item with what changed, and ask the owner for each one whether to copy the change into the file or let the push replace it. Push nothing for an item until the owner has answered. Items with a local change pending are not listed, so tell the owner how many there are and that the push replaces whatever the board holds for them.

## 4. Confirm before the first push

Writing to a tracker is visible to other people. Run `python3 .mirage/check.py sync-plan <tracker>`, count the operations by kind, and show the owner the counts, the target project and every configuration change from step 2. Push only after the owner agrees. When the owner declines a configuration change, use the adapter's fallback for it or leave that field unsynced, and say which. Later runs against the same project need no new confirmation unless they create more than they did before or target another project.

## 5. Push until the plan is empty

1. Run `python3 .mirage/check.py sync-plan <tracker>`. It prints one JSON operation per line, and prints nothing when the tracker is in step.
2. Carry out each operation in order with the adapter's call. Every operation carries the finished title, labels and description to write.
3. Before each `create`, look the item up in the tracker by its `mirage-id` with the adapter's lookup. When it already exists, record it and create nothing. An earlier run may have created it and stopped before recording.
4. After each successful call, record it at once:
   - `python3 .mirage/check.py sync-record <tracker> --id <ID> --remote-id <remote id> --key <key> --url <url>` for a create or update
   - `--link FROM TO` or `--unlink FROM TO` for a relation
5. Run `sync-plan` again.

Repeat until it prints no operations. When a call fails or its result is uncertain, stop and report the operation and the error. The map is already correct for everything recorded, so a rerun continues where you stopped.

Never delete a tracker item. An `orphan` operation means a mapped item's file is gone. Report it to the owner with its tracker key and URL, then run `python3 .mirage/check.py sync-record <tracker> --forget <ID>` so the plan converges.

## 6. Read back what you wrote

For every item created or updated in this run, read it from the tracker once and compare its title, parent, milestone, labels and status with the operation you sent. Report every mismatch. A tracker that silently drops a field is a capability gap, so name the adapter fallback you used.

## Finish

Done when four things hold:

- `sync-plan` prints no operations.
- Every status difference is applied or reported, and every drifted item is resolved with the owner.
- The read-back found no mismatch, or each mismatch is reported.
- `python3 .mirage/check.py check` prints `ok`.

Report the created, updated and linked counts, the pulled status changes, the items awaiting evidence, the drift and how it was resolved, and the orphans. A synced board shows the plan. It does not mean any work is finished.
