<!-- mirage:doc data-model -->
# Data model

{{One paragraph: which component this data model belongs to and what this document fixes. Say an entity or field with no settled owner or shape becomes a question in docs/questions.md rather than an invented schema.}}

<!-- mirage:section entities -->
## Entities

{{Describe the entities this component owns and how they relate to entities owned by other components. Cite the requirement each entity exists to satisfy as REQ-<AREA>-NNN.}}

| Entity | Key fields | Relates to | Owner |
|---|---|---|---|
| {{Entity name}} | {{Field list}} | {{Other entity, or none}} | {{Lane that owns writes to it}} |

<!-- mirage:section storage -->
## Storage

{{Name which database or store holds each entity and why that choice fits its access pattern and volume. State the expected data volume at launch and its growth rate, marking any number as a hypothesis until measured, and cite the input that supplies a real volume figure as (IN-nnn) where one exists.}}

<!-- mirage:section constraints -->
## Constraints

{{List the invariants the schema must enforce, such as uniqueness, foreign keys, required fields and value ranges, and say which layer enforces each one, the database or the application. Cite the requirement each constraint exists to satisfy as REQ-<AREA>-NNN.}}

<!-- mirage:section migrations -->
## Migrations

{{State how a schema change is written, reviewed and applied, and how it is rolled back if it fails partway. State whether migrations run automatically on deploy or by a separate step, and who may run one against production.}}

<!-- mirage:section retention -->
## Retention

{{State how long each kind of data is kept, what deletes or anonymizes it, and which requirement or regulation sets that period. An undecided retention period becomes a question in docs/questions.md instead of an invented number.}}
