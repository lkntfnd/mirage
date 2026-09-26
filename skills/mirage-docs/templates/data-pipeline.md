<!-- mirage:doc data-pipeline -->
# Data pipeline

{{One paragraph: what this pipeline produces, who consumes the output, and what this document fixes. Say an unsettled source, schedule or quality threshold becomes a question in docs/questions.md rather than an invented one.}}

<!-- mirage:section sources -->
## Sources

{{List every system this pipeline reads from, the format each one delivers, and how the pipeline authenticates to it. Cite the requirement each source satisfies as REQ-<AREA>-NNN, and the input that grants access as (IN-nnn).}}

<!-- mirage:section schedules -->
## Schedules

{{State how often the pipeline runs, whether on a fixed schedule or triggered by an event, and how fresh the output must be for its consumers. Mark a freshness target as a hypothesis until it is measured against a real run.}}

<!-- mirage:section transformations -->
## Transformations

{{Describe the transformations that turn each source into the published output, in the order they run, and which step owns each business rule. Cite the requirement each transformation satisfies as REQ-<AREA>-NNN.}}

<!-- mirage:section quality -->
## Data quality

{{List the checks that run against the output, such as row counts, null rates or schema checks, and what happens when one fails, such as blocking the publish or alerting an owner. Name who is alerted and how.}}

<!-- mirage:section backfills -->
## Backfills

{{State how historical data is reprocessed when a transformation changes or a source is corrected, and how a backfill is verified before it replaces the existing output. Name who may trigger a backfill.}}

<!-- mirage:section consumers -->
## Consumers

{{List who reads the output and how, such as a dashboard, a downstream service or an export, and what each consumer assumes about freshness and schema stability. State how a consumer is warned before a breaking schema change.}}
