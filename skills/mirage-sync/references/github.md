# GitHub Issues adapter

## Contents

- [What to use](#what-to-use)
- [Capability detection](#capability-detection)
- [Mapping](#mapping)
- [Status mapping](#status-mapping)
- [Executing each op kind](#executing-each-op-kind)
- [Pulling status back](#pulling-status-back)
- [Limits and gotchas](#limits-and-gotchas)

## What to use

Prefer GitHub's official MCP server, [github/github-mcp-server](https://github.com/github/github-mcp-server), when it is connected in the agent's session. Connect it at the hosted endpoint `https://api.githubcopilot.com/mcp/`, or run the `ghcr.io/github/github-mcp-server` Docker image locally, per its [README](https://github.com/github/github-mcp-server). The tools that matter here are `issue_write`, `issue_read`, `list_issues`, `search_issues`, `sub_issue_write`, `list_issue_types`, `list_issue_fields`, `label_write`, `get_label` and `list_label`. These are the server's own tool names. In a session each one carries the prefix of the name the server was connected under. The server ships no milestone tool as of this writing, so create and update milestones with `gh` or the REST API even when the MCP server handles the rest.

Unverified: whether the MCP server exposes any tool for issue dependencies. None appeared in its published tool list, so use `gh` or the REST API for `blocked_by` links.

When the MCP server is not connected, use the official [`gh` CLI](https://cli.github.com/manual/). `gh issue create` and `gh issue edit` accept `--type`, `--parent`, `--add-sub-issue`, `--add-blocked-by` and `--add-blocking` directly, per the [gh issue create](https://cli.github.com/manual/gh_issue_create) and [gh issue edit](https://cli.github.com/manual/gh_issue_edit) manuals, so the CLI alone covers hierarchy and dependencies without a raw API call.

When neither is available, call the REST API with `gh api` or an authenticated HTTP client, using the endpoints named below.

Credentials come from a `gh auth login` session, the `GITHUB_TOKEN` or `GH_TOKEN` environment variable that `gh` and most GitHub tooling read, or the MCP server's own `GITHUB_PERSONAL_ACCESS_TOKEN` variable or OAuth login. Never write a credential to a file in the repository or under `.mirage/`.

## Capability detection

Run each check once per repository before the first write, and record the result under `settings` in `.mirage/trackers/github.json` so later runs skip it.

| Capability | Check | Fallback when missing |
|---|---|---|
| Repository reachable | `gh repo view OWNER/REPO`, or `GET /repos/{owner}/{repo}` on the [issues API](https://docs.github.com/en/rest/issues/issues), succeeds | Stop and report; no operation below can run |
| Milestones | `GET /repos/{owner}/{repo}/milestones` on the [milestones API](https://docs.github.com/en/rest/issues/milestones) returns 200; milestones ship with Issues on every plan | None needed |
| Custom issue types | The repository is organization owned, and `GET /orgs/{org}/issue-types` on the [issue types API](https://docs.github.com/en/rest/orgs/issue-types) lists a type named `Epic`; types are configured per organization, not per personal account, per [managing issue types](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization) | Tag the epic issue with a plain `epic` label instead of an issue type, and say so in the sync report |
| Sub-issues | `GET /repos/{owner}/{repo}/issues/{n}/sub_issues` on the [sub-issues API](https://docs.github.com/en/rest/issues/sub-issues) returns 200 rather than 404; sub-issues have been generally available since April 2025, per the [changelog](https://github.blog/changelog/2025-04-09-evolving-github-issues-and-projects/) | Create the story or task as a plain issue, name its parent's issue number in the body, and report that the hierarchy is text only |
| Issue dependencies | `GET /repos/{owner}/{repo}/issues/{n}/dependencies/blocked_by` on the [issue dependencies API](https://docs.github.com/en/rest/issues/issue-dependencies) returns 200; dependencies have been generally available since August 2025, per the [changelog](https://github.blog/changelog/2025-08-21-dependencies-on-issues/) | Write a `Blocked by #{n}` line in the body instead of an API link, and report the link as unproven |

Never fold a missing capability into free text without naming the fallback in the sync report.

## Mapping

| Mirage | GitHub Issues |
|---|---|
| milestone | a [milestone](https://docs.github.com/en/rest/issues/milestones) |
| epic | an issue of type `Epic` when the organization has one configured, otherwise an issue labeled `epic` |
| story | an issue, added as a [sub-issue](https://docs.github.com/en/rest/issues/sub-issues) of the epic issue |
| task | a sub-issue of the story issue |
| blocked_by | an [issue dependency](https://docs.github.com/en/rest/issues/issue-dependencies), "this issue is blocked by that issue" |

Two facts shape this mapping. An `Epic` issue type, when the organization has configured one, is a cleaner mapping than the `epic` label, because it survives a search or a board grouped by type. Sub-issues and issue dependencies are both real, GA GitHub relationships now, not text conventions.

Every `area:<name>` label becomes a GitHub label of the same name. Create the label first with `POST /repos/{owner}/{repo}/labels` on the [labels API](https://docs.github.com/en/rest/issues/labels) when it does not already exist. A label description is capped at 100 characters, but the docs give no length cap on the name itself.

Unverified: whether assigning an issue a label name that has no matching label object auto-creates it or fails. Create the label explicitly first rather than relying on either behavior.

GitHub issues have no built-in priority field. Fall back to a label, created the same defensive way.

| Mirage priority | GitHub fallback |
|---|---|
| urgent | label `priority:urgent` |
| high | label `priority:high` |
| medium | label `priority:medium` |
| low | label `priority:low` |

GitHub issues have no built-in estimate field either. Fall back to a label.

| Mirage estimate | GitHub fallback |
|---|---|
| 1 | label `estimate:1` |
| 2 | label `estimate:2` |
| 3 | label `estimate:3` |
| 5 | label `estimate:5` |
| 8 | label `estimate:8` |

Write the issue body exactly as `sync-plan` emits it in the operation's `body` field. It is the Markdown body followed by a footer whose last line is `mirage-id: <ID>`. Do not add or strip anything.

When the map has no entry for an ID, search for it before creating anything, with `GET /search/issues?q=repo:{owner}/{repo}+"mirage-id:+<ID>"+in:body` on the [search API](https://docs.github.com/en/rest/search/search), or `gh issue list --search "mirage-id: <ID> in:body"` per the [gh issue list](https://cli.github.com/manual/gh_issue_list) manual. Record whatever it finds with `sync-record` before creating, so a rerun never duplicates the issue.

The operation's `labels` list is complete. It holds the item's `area:*` labels and, for stories and tasks, `type:*`, `scope:*` and `release:*` labels. Create and apply every label in the list the same way as the area labels. The operation's `title` already starts with the backlog ID, so write it unchanged.

## Status mapping

| Mirage status | GitHub state |
|---|---|
| draft | open, label `status:draft` |
| blocked | open, label `status:blocked` |
| ready | open, label `status:ready` |
| in-progress | open, label `status:in-progress` |
| in-review | open, label `status:in-review` |
| done | closed, `state_reason: completed` |
| cancelled | closed, `state_reason: not_planned` |

GitHub Issues models only open and closed, plus an optional `state_reason` on close, per the [issues API](https://docs.github.com/en/rest/issues/issues). It has no native in-progress or in-review state. The `status:<name>` label is the named fallback for every open mirage status, stated here rather than left silent. On every status change, remove the previous `status:*` label and add the new one; GitHub does not do this for you.

## Executing each op kind

**create, milestone.** `gh api repos/{owner}/{repo}/milestones -f title="{title}"`, or `POST /repos/{owner}/{repo}/milestones` with `title`. Then `python3 .mirage/check.py sync-record github --id {id} --remote-id {milestone number} --url {html_url}`.

**create, epic.** `gh issue create --title "{title}" --body "{body}" --type Epic` when the capability check passed, otherwise `--label epic` (the MCP tool is `issue_write`). Then `sync-record github --id {id} --remote-id {issue id} --url {html_url}`. Store the issue's numeric `id` field as `remote_id`, not its `number`, because the sub-issue and dependency endpoints below take that id, per the [issues API](https://docs.github.com/en/rest/issues/issues).

**create, story or task.** `gh issue create --title "{title}" --body "{body}" --label {labels} --parent {parent issue number} --milestone "{milestone title}"` (the MCP tools are `issue_write` then `sub_issue_write`). The `--parent` flag both creates the issue and files it as a sub-issue in one call. `--milestone` takes the milestone's title as mirage pushed it, which starts with the op's `milestone` ID. The REST API takes the milestone number from the map instead. Then `sync-record` as above.

**update.** `gh issue edit {number} --title "{title}" --body "{body}"`, then diff the current labels against the operation's `labels` plus the adapter's own `status:*`, `priority:*` and `estimate:*` labels, applying `--add-label`/`--remove-label` for each difference (the MCP tool is `issue_write`). Then `sync-record github --id {id} --remote-id {issue id} --url {html_url}`, which refreshes the stored hash and status.

**link (blocked_by FROM TO).** `gh issue edit {FROM number} --add-blocked-by {TO number}`, or `POST /repos/{owner}/{repo}/issues/{FROM number}/dependencies/blocked_by` with `{"issue_id": {TO id}}`. Then `sync-record github --link {FROM} {TO}`.

**unlink (FROM TO).** `gh issue edit {FROM number} --remove-blocked-by {TO number}`, or `DELETE /repos/{owner}/{repo}/issues/{FROM number}/dependencies/blocked_by/{TO id}`. Then `sync-record github --unlink {FROM} {TO}`.

**orphan.** Read the mapped issue's `url` from the map and report it to the owner. Never close or delete it. Then run `python3 .mirage/check.py sync-record github --forget ID` so the plan stops reporting it.

## Pulling status back

For every mapped item, read its current GitHub state with `GET /repos/{owner}/{repo}/issues/{number}` (or the milestone equivalent for a milestone), then apply the status mapping table in reverse and run `python3 .mirage/check.py set-status {id} {status}`.

A closed issue with `state_reason: not_planned` maps straight to `cancelled`. A closed issue with `state_reason: completed` needs evidence before it can become `done`. Read the issue's timeline with `GET /repos/{owner}/{repo}/issues/{number}/timeline` on the [timeline API](https://docs.github.com/en/rest/issues/timeline) and look for a `closed` event whose `commit_id` is set, or a `cross-referenced` event whose `source` is a merged pull request. When you find one, pass it as `--evidence "PR #{n}"` or `--evidence "commit {sha}"`. When you find neither, run `set-status {id} in-review` instead and tell the owner the item closed without traceable evidence; never fabricate the evidence to satisfy `set-status`'s check.

An open issue maps back through its `status:*` label. Two or more `status:*` labels on one issue, or none at all on an open issue, is drift; report it and leave the file's own status alone rather than guessing.

## Limits and gotchas

Authenticated REST requests are capped at 5000 per hour, or 15000 for a GitHub Enterprise Cloud organization, per [rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api). The GraphQL API carries its own separate primary limit and its own point cost, so mixing GraphQL calls into a REST-based sync run spends a different budget than the numbers here. Watch the `x-ratelimit-remaining` and `x-ratelimit-reset` response headers rather than counting calls by hand.

A secondary rate limit also applies on top of the hourly cap. Run the create and update loop serially, never in parallel, and expect trouble at or above roughly 80 content-creating requests a minute, or more than 100 concurrent requests, per [best practices for the REST API](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api). Continuing to call the API after a 403 or 429 risks a temporary ban of the token, so stop and report instead of retrying immediately.

The `/search/issues` endpoint used to locate an unmapped item by its `mirage-id` marker is limited to 30 requests a minute for an authenticated user, well below the general limit, per the same search docs. Trust the map file first on every rerun and reach for search only for the item the map is missing, never as the default matching path.

List endpoints such as milestones, sub-issues, dependencies, labels and search results page at up to 100 items; follow the response's `Link` header for the next page instead of incrementing a page number by hand. Save each response's `etag` header and send it back as `if-none-match` on a repeat read, such as the per-item reads in pulling status back; an unchanged read then costs nothing against the primary rate limit.
