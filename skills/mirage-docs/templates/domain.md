<!-- mirage:doc domain:{{item}} -->
# Domain rules: {{Topic name}}

{{One paragraph: which business rule this document fixes, why it needs its own document instead of living in the PRD, and that docs/questions.md holds every open decision about a rule this document has not yet settled.}}

<!-- mirage:section scope -->
## Scope and requirements

{{State what this topic covers and what it deliberately excludes, and list the requirements (REQ-<AREA>-<NNN>) that this document implements. An unscoped edge belongs in docs/questions.md, not in an assumption here.}}

<!-- mirage:section rules -->
## Rules

{{State each rule that decides the outcome, in the precise order the rules apply, as a numbered list. Write each rule so a reader could implement it without asking a follow-up question. Name how two rules that conflict are resolved.}}

<!-- mirage:section examples -->
## Worked examples

{{Give two or three worked examples that walk an input through the rules above to a stated result, including at least one edge case such as a boundary value or a conflict between rules. Mark an invented number as illustrative when a real one is not yet known.}}

<!-- mirage:section constants -->
## Tunable values

{{List every number in the rules above that can change after launch without a code change, and who owns changing it. Mark each value's status as "decided" with its question, as (Q-nnn), when the owner set it, as "hypothesis" when it is a starting guess that no release has measured, or as "measured" once one has.}}

| Name | Value | Unit | Owner | Status |
|---|---|---|---|---|
| {{Constant name}} | {{Current value}} | {{Unit}} | {{Role or team}} | {{Hypothesis or measured}} |

<!-- mirage:section admin -->
## Admin controls

{{State which of the tunable values and rules above staff can change from the admin tools without waiting for a release, and which role in docs/admin.md's roles table may change each one. A rule with no admin control ships fixed until a later release.}}

<!-- mirage:section scenarios -->
## Test scenarios

{{Add one row per rule and per edge case above, using the ID form <AREA>-T<NN>, where AREA is the requirement area code from docs/prd.md's areas table that this topic belongs to and NN counts up from 01. State the scenario in one sentence and the expected result in one sentence.}}

| ID | Scenario | Expected |
|---|---|---|
| {{AREA-T01}} | {{The situation under test, in one sentence}} | {{What must happen}} |
