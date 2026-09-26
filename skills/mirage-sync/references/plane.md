# Plane adapter

## What to use

Plane publishes an official MCP server, `plane-mcp-server`, documented at [developers.plane.so/dev-tools/mcp-server](https://developers.plane.so/dev-tools/mcp-server) and open sourced at [github.com/makeplane/plane-mcp-server](https://github.com/makeplane/plane-mcp-server), which that page links directly. Use it first. It exposes one tool per resource, including `workitem`, `workitem_type`, `workitem_relation`, `milestone`, `module`, `label`, `state`, `project` and `project_estimate`, each with `create`, `list`, `retrieve`, `update` and `delete` actions ([developers.plane.so/dev-tools/mcp-server-tools](https://developers.plane.so/dev-tools/mcp-server-tools)).

Connect with one of three transports. On Plane Cloud or Commercial Edition, use the hosted endpoint `https://mcp.plane.so/http/mcp` with OAuth, or `https://mcp.plane.so/http/api-key/mcp` with a personal access token sent as `Authorization: Bearer <token>` plus `x-workspace-slug: <slug>`. OAuth needs Plane Cloud or Commercial Edition; on Community Edition run the server locally with `uvx plane-mcp-server stdio`, reading `PLANE_API_KEY` and `PLANE_WORKSPACE_SLUG` from the environment ([developers.plane.so/dev-tools/mcp-server](https://developers.plane.so/dev-tools/mcp-server)). Create the personal access token from the Plane UI under Profile Settings, Personal Access Tokens ([developers.plane.so/api-reference/introduction](https://developers.plane.so/api-reference/introduction)).

Plane publishes no official CLI. Fall back to the REST API only when the MCP server is unreachable. The base URL is `https://api.plane.so/` on Plane Cloud, or the self-hosted domain; authenticate with `X-API-Key: plane_api_<token>` (same source).

Set `PLANE_API_KEY` and `PLANE_WORKSPACE_SLUG` in the agent's environment, or use the OAuth flow's own session. Never write the token, or `Authorization` or `X-API-Key` header values, to any file, including `.mirage/trackers/plane.json`. That file holds only the workspace slug and project id under `settings`.

## Capability detection

Check each of these before the first write, and stop or fall back as stated.

- The project exists. Call `project retrieve` with the project id from `settings`. Stop and tell the owner if it does not exist; mirage never creates a Plane project.
- The Epic work item type is enabled. Call `workitem_type resolve` with `project_id` and `name="Epic"` ([developers.plane.so/dev-tools/mcp-server-tools](https://developers.plane.so/dev-tools/mcp-server-tools)). A project gets Epic only by enabling Work item Types once from the UI, under Project Settings, Work item Types, Enable; Plane then creates Task and Epic together ([docs.plane.so/work-items/project-work-item-types](https://docs.plane.so/work-items/project-work-item-types)). Never enable it over the REST API. A confirmed bug makes the API path create only Task and permanently skip Epic, with no later fix from the API ([forum.plane.so, work item types bug report](https://forum.plane.so/t/enabling-work-item-types-via-rest-api-silently-and-permanently-prevents-the-project-from-ever-having-the-native-epic-type/291)). When Epic is missing, tell the owner to enable it from the UI, and map epics to modules until they do.
- Milestones are enabled. Call `milestone list` for the project. Plane ships Milestones as an optional per-project feature, turned on under Project Settings, Features ([docs.plane.so/core-concepts/projects/milestones](https://docs.plane.so/core-concepts/projects/milestones)). When it is off, tell the owner to enable it. There is no equivalent fallback object, so report milestone-level operations as blocked rather than substituting a module or a label.
- Modules are available, needed only as the epic fallback above. Call `module list`. Modules are on by default and can be switched off in Project Settings ([docs.plane.so/core-concepts/modules](https://docs.plane.so/core-concepts/modules)).
- States cover the seven mirage statuses. Call `state list` for the project and compare names against the Status mapping table. Plane ships five default states, one per state group ([docs.plane.so/core-concepts/issues/states](https://docs.plane.so/core-concepts/issues/states)), short of mirage's seven. Create the two missing ones before the first push, as described under Status mapping.
- An estimate system with mirage's point values exists. Call `project_estimate list_points`. Plane ships no default values; `type` is `categories`, `points` or `time` ([developers.plane.so/dev-tools/mcp-server-tools](https://developers.plane.so/dev-tools/mcp-server-tools)). When points 1, 2, 3, 5 and 8 are missing, create a `points` estimate system with `project_estimate create` and `create_points`, and tell the owner you did.
- Work item relations. Call `workitem_relation list_definitions`. `blocking` and `blocked_by` are default relation types and need no setup (same source). If the tool reports them inactive, tell the owner instead of writing `blocked_by` links.

## Mapping

| Mirage | Plane |
|---|---|
| milestone | milestone ([docs.plane.so/core-concepts/projects/milestones](https://docs.plane.so/core-concepts/projects/milestones)) |
| epic | work item of type Epic, or a module when Epic is not enabled ([docs.plane.so/core-concepts/issues/epics](https://docs.plane.so/core-concepts/issues/epics)) |
| story | work item |
| task | child work item, nested by setting `parent` to the story's work item id ([developers.plane.so/dev-tools/mcp-server-tools](https://developers.plane.so/dev-tools/mcp-server-tools)) |
| blocked_by | work item relation with `relation_type` `blocked_by`, the inverse stored as `blocking` (same source) |
| `area:*` labels | labels, created with the same name |
| priority | the work item's `priority` field, one of `urgent`, `high`, `medium`, `low` (same source); mirage never sends `none` |
| estimate | the work item's `estimate_point`, a UUID naming one of the project's configured point values, never the raw number ([developers.plane.so/dev-tools/mcp-server-tools](https://developers.plane.so/dev-tools/mcp-server-tools)) |

An epic is not a separate object. Resolve its work item type once per project with `workitem_type resolve`, `project_id` and `name="Epic"`, keep the returned `id` as `type_id`, and pass that on `workitem create` (same source, the epics recipe). List an epic's children with `workitem list` and `pql='childOf("PROJ-12")'`, using its human-readable identifier, which is the project's `identifier` joined to the work item's `sequence_id` with a hyphen ([developers.plane.so/api-reference/issue/get-issue-sequence-id](https://developers.plane.so/api-reference/issue/get-issue-sequence-id)).

Put the mirage-id marker in two places. Set `external_id` to the mirage ID and `external_source` to `"mirage"` on every create call, a field Plane's `workitem`, `milestone`, `module` and `label` tools all accept, and their `list` actions accept the same two fields as filters, so an unmapped item is found by filtering on them instead of scanning text ([developers.plane.so/dev-tools/mcp-server-tools](https://developers.plane.so/dev-tools/mcp-server-tools)). Also write the literal `mirage-id: <ID>` line the operation's `body` already carries into the item's own text, using `description_stripped` on a work item or `description` on a module or a label. A milestone has no body or description field in the documented `create` and `update` actions (same source), so `external_id` is the only marker a milestone carries.

## Status mapping

| Mirage | Plane |
|---|---|
| draft | Backlog (`backlog` group, default) |
| ready | Todo (`unstarted` group, default) |
| blocked | Blocked, a custom state in the `started` group |
| in-progress | In Progress (`started` group, default) |
| in-review | In Review, a custom state in the `started` group |
| done | Done (`completed` group, default) |
| cancelled | Cancelled (`cancelled` group, default) |

Plane ships only the five states marked default ([docs.plane.so/core-concepts/issues/states](https://docs.plane.so/core-concepts/issues/states)). Create Blocked and In Review once per project with `state create`, passing `project_id`, `name`, a `color` and `group="started"` ([developers.plane.so/dev-tools/mcp-server-tools](https://developers.plane.so/dev-tools/mcp-server-tools)). When pulling status back from a state this adapter did not create, map by its group using the table above rather than its name, since an owner can rename or add states freely.

## Executing each op kind

Resolve `state_id` from the op's `status` with a cached `state list` result before any create or update call.

**create.** Dispatch on `level`. For a milestone, call `milestone create` with `project_id`, `title`, `target_date` when `due` is set, `external_id` and `external_source="mirage"`. For an epic, call `workitem create` with `project_id`, the Epic `type_id`, `name=title`, `description_stripped=body`, `state`, `labels`, `external_id` and `external_source`. For a story or a task, call `workitem create` with the same fields plus `priority`, `estimate_point` and `parent` set to the epic's or the story's `remote_id`. After success, run `python3 .mirage/check.py sync-record plane --id ID --remote-id RID --key KEY --url URL`, where `KEY` is the project `identifier` joined to the returned `sequence_id` with a hyphen, for example `FT-12`.

**update.** Call the same tool's `update` action, passing the item's `remote_id` from the map as `milestone_id` or `workitem_id`, and the same fields as create. Record with the same `sync-record` command.

**link.** Call `workitem_relation create` with `project_id`, the `blocked_by` item's `workitem_id`, `workitem_ids=[<the blocker's remote_id>]` and `relation_type="blocked_by"`. Then run `python3 .mirage/check.py sync-record plane --link FROM TO`.

**unlink.** Call `workitem_relation delete` with `project_id`, `workitem_id` and `related_workitem_id` set to the two ends' `remote_id`s. Then run `python3 .mirage/check.py sync-record plane --unlink FROM TO`.

**orphan.** Make no Plane call. Report the item and its `remote_id` and `url` from the map to the owner. Then run `python3 .mirage/check.py sync-record plane --forget ID` so the plan stops reporting it.

## Pulling status back

For every mapped item, call the level's `retrieve` action on its `remote_id` and read its current `state`. Map the state to a mirage status with the Status mapping table, by name for Blocked and In Review and by group otherwise. When it differs from the map's stored `status`, run `python3 .mirage/check.py set-status ID STATUS`.

Before setting `done`, look for evidence. Call `workitem_link list` for an attached pull request or commit URL, then `workitem_comment list` if none is linked. When you find one, run `set-status ID done --evidence "<the URL>"`. When you find none, run `set-status ID in-review` instead and tell the owner which items are missing evidence; a Plane state named Done is never evidence by itself.

## Limits and gotchas

The REST API allows 60 requests per minute per client, with `X-RateLimit-Remaining` and `X-RateLimit-Reset` response headers; the MCP server calls the same API, so a large sync-plan can exhaust it ([developers.plane.so/api-reference/introduction](https://developers.plane.so/api-reference/introduction)). Batch list calls with `per_page` up to 100 and follow `cursor` rather than looping single-item retrieves.

A rich-text round trip through `description_html` can add empty paragraph nodes that render as blank lines or bullets on the next read, a known open issue in the MCP server ([github.com/makeplane/plane-mcp-server/issues/196](https://github.com/makeplane/plane-mcp-server/issues/196)). Prefer `description_stripped` for the body mirage generates, and when comparing a work item's body for drift, compare it loosely rather than byte for byte, since Plane's own formatting can add these artifacts without an owner having touched the item.

A self-hosted Community Edition instance can lag the documented API. One open report shows `workitem_relation create` calling an endpoint Community Edition does not expose, where an older one still works ([github.com/makeplane/plane-mcp-server/issues/185](https://github.com/makeplane/plane-mcp-server/issues/185)). Treat a not-found error from that call as this gap rather than a real failure, and report the installed server version to the owner instead of stopping the whole sync.

Unverified: whether Plane's PQL supports a text search over a work item's description; treat it as unsupported and match by `external_id` and `external_source` instead, per Mapping.

Unverified: the browser URL for a single work item. `docs.plane.so/core-concepts/issues/work-item-url` documents only a creation link. Use the tool result's own link field if one is returned, otherwise leave `--url` unset and tell the owner rather than guessing the pattern.

Unverified: whether `description_stripped` renders mirage's Markdown as formatted text or shows it literally once wrapped in HTML. Check one created item before a full sync-plan run, and switch to a converted `description_html` body if the Markdown shows literally.
