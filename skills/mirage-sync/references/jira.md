# Jira adapter

## Contents

- [What to use](#what-to-use)
- [Capability detection](#capability-detection)
- [Mapping](#mapping)
- [Status mapping](#status-mapping)
- [Executing each op kind](#executing-each-op-kind)
- [Pulling status back](#pulling-status-back)
- [Limits and gotchas](#limits-and-gotchas)

## What to use

Use the official Atlassian Remote MCP Server first, at `https://mcp.atlassian.com/v2/mcp`, connected over OAuth 2.1 or an API token ([github.com/atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server)). It exposes typed Jira tools, listed on the [supported tools page](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/): `createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`, `listJiraIssueTransitions`, `searchJiraIssuesUsingJql`, `getJiraIssue`, `createJiraIssueLink`, `listJiraIssueLinkTypes`, `listJiraProjects`, `getJiraIssueTypeMetaWithFields` and `getJiraProjectVersions`. `deleteJiraIssue` exists but needs admin enablement, and mirage never deletes a Jira item.

Atlassian also publishes an official CLI, ACLI, documented for Jira Cloud at [developer.atlassian.com/cloud/acli](https://developer.atlassian.com/cloud/acli/reference/commands/jira/). Use it for anything the MCP server has no tool for. Unverified: whether ACLI is generally available or still in an earlier release stage. Its own docs state no release status; confirm at `acli --version` and Atlassian's changelog before depending on it for a production sync. Its `acli jira workitem` group covers `create`, `edit`, `view`, `search`, `transition`, `link` and more ([reference](https://developer.atlassian.com/cloud/acli/reference/commands/jira-workitem/)), and `acli jira project` covers project-level operations.

Fall back to the REST API v3 for anything neither tool covers, such as creating a fix version. Authenticate with an Atlassian account email and an API token generated at id.atlassian.com, sent as `Authorization: Basic <base64(email:token)>` ([developer.atlassian.com](https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/)). Read the token, email and site URL from the environment as `JIRA_API_TOKEN`, `JIRA_EMAIL` and `JIRA_BASE_URL`, mirage's own convention for this adapter. Never write any of them to a file. The MCP server keeps its own OAuth session, and ACLI keeps its own session after `acli jira auth login`.

## Capability detection

Read the project before the first write, and record what it supports.

| Check | How | Fallback when missing |
|---|---|---|
| Project exists and its type | `listJiraProjects`, or `GET /rest/api/3/project/{key}` | Stop and tell the owner |
| Team-managed or company-managed | the same project read, since it changes how Epic and Sub-task nest ([support.atlassian.com](https://support.atlassian.com/jira-software-cloud/docs/upcoming-changes-epic-link-replaced-with-parent/)) | Confirm before assuming either |
| Epic and Sub-task issue types enabled | `getJiraIssueTypeMetaWithFields` per project | Report the missing type, never substitute another one silently |
| A "Blocks" link type is enabled | `listJiraIssueLinkTypes` | Use whichever enabled type reads closest to blocks and is blocked by, and name it to the owner |
| Fix versions configured, and this token can create them | `getJiraProjectVersions`, then a trial create | Ask the owner for Administer Projects, or have them create the milestone by hand |
| Custom workflow statuses in play | `listJiraIssueTransitions` on a sample issue, or the project's workflow scheme | Use the nearest existing status from the table below and record the mismatch |
| A story points field exists | `GET /rest/api/3/field`, matched by name | Skip pushing `estimate` and tell the owner which field is missing |

Unverified: the exact custom field name for story points. Jira ships no single Fibonacci estimate field. Team-managed projects commonly expose "Story point estimate" and company-managed ones "Story Points", but confirm the live name and id for this project before the first push.

## Mapping

| Mirage | Jira |
|---|---|
| milestone | fix version |
| epic | issue of type Epic |
| story | issue of type Story, `parent` set to the epic's key |
| task | issue of type Sub-task, `parent` set to the story's key |
| blocked_by | issue link of type "Blocks" |
| labels | Jira labels |
| priority | the project's priority scheme |
| estimate | the story points field |

A story or task nests under its parent through the `parent` field, not the legacy Epic Link field. Atlassian is replacing Epic Link and Parent Link with `parent` everywhere, and team-managed projects never had Epic Link ([support.atlassian.com](https://support.atlassian.com/jira-software-cloud/docs/upcoming-changes-epic-link-replaced-with-parent/)). An epic itself carries no fix version, because one mirage epic can span several milestones. Only its stories and tasks carry one.

Map each `area:<name>` label straight across. Jira labels cannot contain spaces ([support.atlassian.com](https://support.atlassian.com/jira/kb/how-to-create-and-use-labels-in-jira-cloud/)), and mirage's labels never do either.

Map priority against the project's own scheme, whose default is Highest, High, Medium, Low and Lowest ([support.atlassian.com](https://support.atlassian.com/jira-cloud-administration/docs/manage-priority-schemes/)). Use Highest for `urgent`, High for `high`, Medium for `medium` and Low for `low`. Nothing maps to Lowest.

Build an issue's description as Atlassian Document Format, one paragraph per blank-line-separated block of the body, each holding a single text node with that block's plain text ([atlassian.com/blog](https://www.atlassian.com/blog/development/creating-a-jira-cloud-issue-in-a-single-rest-call)). End with a paragraph containing exactly `mirage-id: <ID>`. A fix version has no ADF description, only a plain string ([developer.atlassian.com](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-versions/)), so put the marker line at the end of that string instead.

To find an item the map does not list, search issues with the JQL `description ~ "mirage-id: <ID>"`. The `~` operator runs a full text match on the description field rather than an exact substring match ([support.atlassian.com](https://support.atlassian.com/jira-software-cloud/docs/jql-operators/)). JQL does not index fix versions, so find an unmapped milestone by listing the project's versions with `getJiraProjectVersions` and reading each description directly.

The operation's `labels` list is complete. It holds the item's `area:*` labels and, for stories and tasks, `type:*`, `scope:*` and `release:*` labels. Create and apply every label in the list the same way as the area labels. The operation's `title` already starts with the backlog ID, so write it unchanged.

## Status mapping

| Mirage | Jira |
|---|---|
| draft | To Do |
| blocked | Blocked, or To Do if absent |
| ready | Ready, or To Do if absent |
| in-progress | In Progress |
| in-review | In Review, or In Progress if absent |
| done | Done |
| cancelled | Cancelled, or Done with a comment if absent |

To Do, In Progress and Done ship with every project's default workflow. The rest are common additions, not guarantees. Adding a workflow status needs Jira administrator rights, and project admins cannot do it even through the API. Unverified: whether this project's Jira edition exposes an API to add one at all, so treat it as unavailable until proven otherwise. When the target status is missing, transition to the nearest existing one from the table above and record the mismatch for the owner instead of inventing a status.

## Executing each op kind

**create.** For an epic, story or task, call `createJiraIssue` with `project`, `issuetype` from the level's row above, `summary` as the title, the ADF `description` built in Mapping, `labels`, and `parent` when the op carries one. Add `fixVersions` with the milestone's remote id for a story or task. Then call `transitionJiraIssue` toward the mapped status if a transition to it exists from the issue's start status. For a milestone, call `POST /rest/api/3/version` with `name`, `projectId` and the marker-suffixed `description` ([developer.atlassian.com](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-versions/)). Unverified: whether ACLI has since added a project-version create command, check `acli jira project --help` before defaulting to the REST call. A version carries no status. After success, run:
```
python3 .mirage/check.py sync-record jira --id ID --remote-id RID --key KEY --url URL
```

**update.** Call `editJiraIssue` with the same fields as create, replacing the whole `labels` and `fixVersions` lists rather than appending to them. Transition it toward the mapped status the same way as create. Record it with the same `sync-record --id` command.

**link.** For a `blocked_by` edge from FROM to TO, call `createJiraIssueLink` with `type.name` set to "Blocks", `outwardIssue` set to TO's key, since TO blocks FROM, and `inwardIssue` set to FROM's key, since FROM is blocked by TO ([developer.atlassian.com](https://developer.atlassian.com/cloud/jira/platform/issue-linking-model/)). Then run:
```
python3 .mirage/check.py sync-record jira --link FROM TO
```

**unlink.** List FROM's links with `getJiraIssue` or `acli jira workitem link list` to find the one matching TO and type Blocks, then delete it with `acli jira workitem link delete` ([developer.atlassian.com](https://developer.atlassian.com/cloud/acli/reference/commands/jira-workitem-link/)), since the MCP server exposes no delete tool for links. Unverified: its exact flags for identifying which link to remove, confirm with `acli jira workitem link delete --help` before scripting it. Then run:
```
python3 .mirage/check.py sync-record jira --unlink FROM TO
```

**orphan.** Report the ID and its last known key to the owner. Never delete the Jira item. Then run `python3 .mirage/check.py sync-record jira --forget ID` so the plan stops reporting it.

## Pulling status back

For every mapped item, read its current status with `getJiraIssue` or `listJiraIssueTransitions`, map it back through the status table above, and apply a difference with:
```
python3 .mirage/check.py set-status ID STATUS [--evidence TEXT]
```
Never copy a title, labels or hierarchy from Jira into the files. Status is the only field that comes back. Read the other fields only to find drift for the sync skill's drift step, which compares them with `python3 .mirage/check.py sync-expect jira`.

A Jira "Done" is not evidence by itself. Open the issue's development panel for a linked pull request or commit, or look for a smart-commit reference. When one exists, pass it as `--evidence`. When none exists, set `in-review` instead and tell the owner which items are missing evidence. Never invent it.

## Limits and gotchas

Jira Cloud enforces an hourly points quota, a per-second burst limit per endpoint, and a per-issue write cap of 20 operations per 2 seconds or 100 per 30 seconds. Any of the three returns `429` with a `Retry-After` header, so back off and retry rather than hammering the endpoint ([developer.atlassian.com](https://developer.atlassian.com/cloud/jira/platform/rate-limiting/)).

Search results lag writes. A search run right after a create or update can miss it or show stale fields. Pass the new issue's id in `reconcileIssues`, up to 50 per search, to force a consistent read for that one issue, and expect ordinary lag of seconds to minutes for anything else ([developer.atlassian.com](https://developer.atlassian.com/cloud/jira/platform/search-and-reconcile/)).

A large `sync-plan` output that touches one issue repeatedly, such as a create followed by several field edits and a transition, can trip the per-issue write cap even while the hourly quota still has room. Batch or space out repeated writes to the same issue.

A link type, a status or a custom field an admin renamed or removed between runs breaks a cached assumption silently. Re-run capability detection whenever `sync-plan` reports something unexpected, rather than trusting the last run's shape.
