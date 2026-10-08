# Linear adapter

## Contents

- [What to use](#what-to-use)
- [Capability detection](#capability-detection)
- [Mapping](#mapping)
- [Status mapping](#status-mapping)
- [Executing each op kind](#executing-each-op-kind)
- [Pulling status back](#pulling-status-back)
- [Limits and gotchas](#limits-and-gotchas)

## What to use

Linear publishes an official, centrally hosted MCP server at `https://mcp.linear.app/mcp`, with a read-only variant at `https://mcp.linear.app/mcp/readonly`, documented at [linear.app/docs/mcp](https://linear.app/docs/mcp). Connect an MCP client there first. It authenticates through OAuth 2.1 with dynamic client registration, or through a bearer token or a personal API key passed directly (same page). Its own docs describe its tools only loosely, as ones "for finding, creating, and updating objects in Linear like issues, projects, and comments... with more functionality on the way" (same page), and name no tool for project milestones, issue relations or labels. Use its issue, project and comment tools when they cover an operation, and fall back to the GraphQL API below for project milestones, issue relations and labels until the tool list documents them.

Linear publishes no official CLI. Its developers index lists a GraphQL API, a TypeScript SDK and agent tooling, with no CLI section ([linear.app/developers](https://linear.app/developers)).

Call the GraphQL API directly at `https://api.linear.app/graphql` for everything the MCP server does not cover. Authenticate a personal API key with the header `Authorization: <API_KEY>`, or an OAuth access token with `Authorization: Bearer <ACCESS_TOKEN>` ([linear.app/developers/graphql](https://linear.app/developers/graphql)). The TypeScript SDK, `@linear/sdk`, wraps the same API and accepts either credential as `apiKey` or `accessToken` on `LinearClient` ([linear.app/developers/sdk](https://linear.app/developers/sdk)).

Read the key from a `LINEAR_API_KEY` environment variable, or read an OAuth session from wherever the MCP client already holds it. Never write a key, token or `Authorization` header value to any file, including `.mirage/trackers/linear.json`. That file holds only the workspace and the team key under `settings`.

## Capability detection

Run each check once before the first write.

| Capability | Check | Fallback when missing |
|---|---|---|
| Team exists | The team key in `settings` resolves to a team id; every issue belongs to one team ([linear.app/developers/graphql](https://linear.app/developers/graphql)) | Stop and tell the owner, since no item below can be created |
| Project usable as epic container | A Linear [project](https://linear.app/docs/projects) is "a grouping of issues that have a clear outcome," and can span teams, matching mirage's epic | None needed, this is the confirmed mapping, see Mapping |
| Project milestones creatable | Milestones ship as part of every project, not behind a toggle ([linear.app/docs/project-milestones](https://linear.app/docs/project-milestones)) | If `projectMilestoneCreate` ever fails, add a plain label such as `milestone:M1` instead, and tell the owner |
| A blocking relation type is available | `blocks` is a fixed value of Linear's relation type, not something a team configures ([linear.app/docs/issue-relations](https://linear.app/docs/issue-relations)) | If the relation call fails, note the block in a comment on both issues and tell the owner |
| Team's estimate scale fits 1, 2, 3, 5, 8 | Read the team's scale, set at Team Settings, General, Estimates; Fibonacci is exactly 1, 2, 3, 5, 8, the other three scales are not ([linear.app/docs/estimates](https://linear.app/docs/estimates)) | Ask the owner to switch the team to the Fibonacci scale; never coerce a mirage estimate into a mismatched scale's nearest value |
| Team's workflow states cover mirage's seven statuses | List the team's states; a new team ships only Backlog, Todo, In Progress, Done and Canceled, with no In Review state ([linear.app/docs/configuring-workflows](https://linear.app/docs/configuring-workflows)) | Ask the owner to add the missing states, as described under Status mapping |

## Mapping

| Mirage | Linear |
|---|---|
| milestone | a project milestone, scoped to one epic's project |
| epic | a project |
| story | an issue |
| task | a sub-issue of the story's issue |
| blocked_by | an issue relation of type `blocks`, from the blocker to the blocked issue |
| labels (`area:*`, `type:*`, `scope:*`, `release:*`) | workspace-level labels, same name |

One point needs care. A project milestone belongs to exactly one project; asked whether one can be shared across projects, Linear's docs answer "this isn't currently possible, you will need to recreate milestones in each individual project" ([linear.app/docs/project-milestones](https://linear.app/docs/project-milestones)). A mirage epic's stories can sit in several milestones, so one mirage milestone realizes as a separate project milestone inside every epic's project that has stories in it, never as a single Linear object. Treat a milestone-level `create` or `update` op as satisfied once at least one such project milestone exists for it. Do not expect the map's one `remote_id` to name all of them; create the rest lazily the first time a story of that epic and milestone is pushed, and record only the first with `sync-record`.

Create `area:*` labels at the workspace level, not per team, so a shared project reads the same label on every team it touches; Linear's labels can be workspace-wide or team-only ([linear.app/docs/labels](https://linear.app/docs/labels)). Never put them in a Linear label group, because only one label from a group can sit on an issue at a time (same page), which would break a story carrying more than one area.

| Mirage priority | Linear `priority` |
|---|---|
| urgent | 1 |
| high | 2 |
| medium | 3 |
| low | 4 |

Mirage never sends `priority: 0`, which means no priority. 1, 2 and 4 come from a filtering example: querying urgent and high together with `priority: { lte: 2 }`, and noting that the same query "will also return any issues that haven't been given any priority (their priority is 0)"; a separate example filters low-priority issues with `priority: { eq: 4 }` ([linear.app/developers/filtering](https://linear.app/developers/filtering)). 3 is medium by elimination, the one level [linear.app/docs/priority](https://linear.app/docs/priority) names that the filtering page never numbers.

Send a mirage estimate straight through as the issue's `estimate`, once the capability check confirms the team's scale is Fibonacci; mirage's 1, 2, 3, 5, 8 is that scale exactly ([linear.app/docs/estimates](https://linear.app/docs/estimates)).

Write the issue's description exactly as the op's `body` field gives it. It is the Markdown body followed by a footer whose last line is `mirage-id: <ID>`. Add or strip nothing. When the map has no entry for an ID, search before creating, with an `issues` query filtered on `description: { contains: "mirage-id: <ID>" } }`; `contains` is a documented string comparator ([linear.app/developers/filtering](https://linear.app/developers/filtering)). Record whatever it finds with `sync-record` before creating anything.

The operation's `labels` list is complete. It holds the item's `area:*` labels and, for stories and tasks, `type:*`, `scope:*` and `release:*` labels. Create and apply every label in the list the same way as the area labels. The operation's `title` already starts with the backlog ID, so write it unchanged.

## Status mapping

| Mirage | Linear workflow state |
|---|---|
| draft | Backlog |
| blocked | Blocked, a custom state added to the backlog category |
| ready | Todo |
| in-progress | In Progress |
| in-review | In Review, a custom state added to the started category |
| done | Done |
| cancelled | Canceled |

A new team ships only Backlog, Todo, In Progress, Done and Canceled ([linear.app/docs/configuring-workflows](https://linear.app/docs/configuring-workflows)), short of mirage's seven. Add Blocked and In Review once, from Settings, Teams, Issue statuses, the "+" control, naming the status and picking its category (same page). Put Blocked in the backlog category and In Review in the started category, next to the states they sit beside in the table above. When pulling status back from a state this adapter did not create, match it by name; if an owner renamed a state, report the drift instead of guessing its category.

## Executing each op kind

Resolve `stateId` from the op's `status` against a cached list of the team's states before any create or update.

**create, milestone.** Call `projectMilestoneCreate` with `projectId` set to the epic's project and `name` set to the milestone id, for the first epic that needs it. Run `python3 .mirage/check.py sync-record linear --id ID --remote-id RID --url URL`. Repeat the create, without a further `sync-record`, for every other epic whose stories share this milestone.

**create, epic.** Call `projectCreate` with `name` and the team id. Projects carry their own short identifier, formatted `P-TEAM-123` ([linear.app/docs/projects](https://linear.app/docs/projects)); use it as `key`. Run `python3 .mirage/check.py sync-record linear --id ID --remote-id RID --key KEY --url URL`.

**create, story.** Call `issueCreate` with `teamId`, `title`, `description` set to the op's `body`, `stateId`, `priority`, `estimate`, `labelIds` and `projectId` set to the epic's project; `teamId`, `title`, `description` and `stateId` are the fields `issueCreate` and `issueUpdate` show verbatim ([linear.app/developers/graphql](https://linear.app/developers/graphql)). Set `projectMilestoneId` to the id from the create-milestone step. Run `sync-record` with the issue's id as `remote_id`, its human-readable identifier (for example `ENG-123`, the same shape the docs use to reference an issue directly, `id: "BLA-123"`, same page) as `key`, and its URL.

**create, task.** Call `issueCreate` the same way, with `parentId` set to the story's `remote_id`. A sub-issue inherits its parent's team and project automatically ([linear.app/docs/parent-and-sub-issues](https://linear.app/docs/parent-and-sub-issues)), so omit `teamId` and `projectId`. Run `sync-record` as above.

**update.** Call `issueUpdate` with the mapped `remote_id` as `id`, sending only the fields the op changed, the same `id`, `input: { title, stateId, ... }` shape shown on [linear.app/developers/graphql](https://linear.app/developers/graphql). Use `projectUpdate` for an epic and `projectMilestoneUpdate` for a milestone. Run `sync-record` again, which refreshes the stored hash and status.

**link.** Create an issue relation of type `blocks`, with `issueId` set to `TO`'s remote id, the blocker, and `relatedIssueId` set to `FROM`'s remote id, the blocked item. Run `python3 .mirage/check.py sync-record linear --link FROM TO`.

**unlink.** Remove that relation. Run `python3 .mirage/check.py sync-record linear --unlink FROM TO`.

**orphan.** Report the mapped item's `key` and `url` to the owner. Make no Linear call. Then run `python3 .mirage/check.py sync-record linear --forget ID` so the plan stops reporting it.

Unverified: the exact input fields for `projectMilestoneCreate`, `projectCreate`, `projectUpdate`, `projectMilestoneUpdate`, the issue relation create and delete mutations, and `parentId` and `labelIds` on `issueCreate`. Linear's interactive schema reference, linked from the getting-started page as "GraphQL Schema" ([linear.app/developers/graphql](https://linear.app/developers/graphql)), did not render as static text this session. Confirm each field there, or by introspection, before the first live call.

## Pulling status back

For every mapped item, read the issue's current workflow state and map its name with the Status mapping table in reverse. When it differs from the map's stored status, run `python3 .mirage/check.py set-status ID STATUS`.

Before setting `done`, look for evidence. Read the issue's attachments; Linear's GitHub integration links a pull request to an issue as one ([linear.app/developers/attachments](https://linear.app/developers/attachments)). When a pull request or commit link is present, run `set-status ID done --evidence "<the URL>"`. When none is present, run `set-status ID in-review` instead and tell the owner which items are missing evidence. A Linear state named Done is never evidence by itself.

Never copy a title, a label, a project or a parent from Linear into the files. Status is the only field that comes back. Read the other fields only to find drift for the sync skill's drift step, which compares them with `python3 .mirage/check.py sync-expect linear`.

## Limits and gotchas

A personal API key is capped at 2,500 requests an hour and 3,000,000 complexity points; an OAuth app gets 5,000 requests and 2,000,000 points; a single query cannot exceed 10,000 points ([linear.app/developers/rate-limiting](https://linear.app/developers/rate-limiting)). Watch the `X-RateLimit-Requests-Remaining` and `X-RateLimit-Complexity-Remaining` response headers rather than counting calls by hand.

A connection defaults to 50 items per page, and each returned object and property adds to a query's complexity (same page). Page explicitly through the team's states, labels and issues rather than fetching every mapped item's state in one unbounded query.

A sub-issue always takes its team, its project and its priority from its parent ([linear.app/docs/parent-and-sub-issues](https://linear.app/docs/parent-and-sub-issues)). Never set a task's team or project to anything other than its story's, and never set a task's own `priority`, since mirage keeps priority on the story only.

Unverified: whether a read immediately after a write can return stale data. Nothing in the fetched pages addresses read-after-write consistency for this API; verify empirically with one created issue before trusting an immediate follow-up read in the push-then-verify loop.
