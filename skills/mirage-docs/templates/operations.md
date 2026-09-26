<!-- mirage:doc operations -->
# Operations

{{One paragraph: what keeps the product running day to day and what this document fixes about deploying, monitoring and recovering it. Name the components from docs/architecture.md this document covers, and say that an unresolved cost, date or vendor becomes a question in docs/questions.md as (Q-nnn) rather than an invented one.}}

<!-- mirage:section environments -->
## Environments

{{One paragraph: how docs/architecture.md's environments are reached day to day, who can promote a change from one to the next, and what gate a change must pass before promotion.}}

<!-- mirage:section ci-cd -->
## CI/CD

{{One paragraph: which CI service runs the checks, on which events, such as a pull request or a push to the base branch, and what a green run proves. Record the CI service account as an input in docs/inputs.md with ID IN-nnn if it does not exist yet.}}

<!-- mirage:section release -->
## Release and rollback

{{One paragraph: how each component deploys, who may trigger a deploy, how often releases ship and how they are announced. State how a bad release is rolled back and the target time to roll it back, marking that time a hypothesis until a real rollback measures it.}}

<!-- mirage:section hosting -->
## Hosting and domains

{{One row per domain the project owns: who controls its DNS and how its certificate renews. State where each component is hosted, citing docs/architecture.md, and record hosting or DNS access as an input in docs/inputs.md with ID IN-nnn.}}

| Domain | Points to | DNS owner | Certificate renewal |
|---|---|---|---|
| {{example.com}} | {{Component or environment}} | {{Who controls DNS}} | {{Automatic or manual, and by whom}} |

<!-- mirage:section observability -->
## Observability

{{One paragraph: which logs, metrics, alerts and error tracking exist for each component, where they are viewed, and who receives an alert when one fires. Record the error tracking account as an input in docs/inputs.md with ID IN-nnn if it does not exist yet.}}

<!-- mirage:section backups -->
## Backups and recovery

{{One row per store that is backed up: how often it is backed up and the acceptable data loss and downtime if it must be restored. Mark an untested recovery time as a hypothesis until a restore drill measures it.}}

| Store | Frequency | Acceptable data loss | Acceptable downtime |
|---|---|---|---|
| {{Database or store name}} | {{How often}} | {{Time window}} | {{Time window}} |

<!-- mirage:section support -->
## Support

{{One paragraph: how users report a problem, who triages it, and what the running costs are expected to be and who pays them. Mark an unconfirmed cost figure as a hypothesis until an actual bill confirms it, and record who pays as a question in docs/questions.md as (Q-nnn) if that is undecided.}}
