<!-- mirage:doc admin -->
# Admin tools

{{One paragraph: who staffs the admin tools, and what the tools let them do that end users cannot.
State that docs/questions.md holds every open decision about roles, retention or bulk operations.}}

<!-- mirage:section modules -->
## Modules

{{List every admin screen or tool the product needs, one sentence each naming what it manages.
Cite the requirement (REQ-<AREA>-<NNN>) that calls for each one.
Order the list the way an owner would find it in a navigation menu.}}

<!-- mirage:section roles -->
## Roles

{{Name every staff role, distinct from the end-user roles in docs/auth.md.
Fill one matrix row per role naming exactly what that role may do in each admin module.
An undecided permission becomes a question in docs/questions.md instead of a guess.}}

| Role | {{Module or capability 1}} | {{Module or capability 2}} |
|---|---|---|
| {{Role name}} | {{Full, read-only or none}} | {{Full, read-only or none}} |

<!-- mirage:section workflows -->
## Workflows

{{Name every operational workflow staff perform through the admin tools, such as moderation, refunds, or a bulk import or export.
Describe the steps each workflow follows, from trigger to completion.
State which role from the roles table may perform each workflow.}}

<!-- mirage:section audit -->
## Audit log

{{State which staff actions the audit log records, such as a role change, a refund or a deletion.
State what each entry captures, such as the actor, the action and the time.
Treat any retention period as a hypothesis until a release has measured the storage cost.}}
