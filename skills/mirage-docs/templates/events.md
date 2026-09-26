<!-- mirage:doc events -->
# Analytics events

{{One paragraph: state that this document fixes which business questions analytics must answer, the shape every event follows, the catalog of events the product sends, and how the team verifies that events actually arrive.}}

<!-- mirage:section questions -->
## Questions analytics must answer

{{List the business questions this product's analytics exist to answer, such as which step of a flow loses the most people or which capability drives return visits. Tie each question to the metric it feeds in docs/prd.md's success metrics table. A tool with no question behind it does not belong in the catalog below.}}

<!-- mirage:section envelope -->
## Event envelope

{{Define the fields every event carries no matter what it is, such as a name, a timestamp, an identity reference and a source, and state which fields are required against which are optional. Cite the requirement this satisfies as REQ-<AREA>-<NNN>. An undecided field becomes a question in docs/questions.md.}}

<!-- mirage:section catalog -->
## Event catalog

{{List every event the product sends, one row per event, and for each one state what triggers it, which properties it carries beyond the envelope, and which destinations receive it. Cite the requirement each event supports as REQ-<AREA>-<NNN>. An event still undecided becomes a question in docs/questions.md rather than a guessed name.}}

| Event | Trigger | Properties | Destinations |
|---|---|---|---|
| {{event_name}} | {{What action or system state causes it}} | {{The properties beyond the envelope}} | {{Which tools receive it}} |

<!-- mirage:section sinks -->
## Destinations

{{Name every analytics tool that receives events and why each one is needed. Cite the input that grants its account as IN-nnn. State whether any destination receives a filtered or delayed copy of the catalog rather than every event. An undecided tool becomes a question in docs/questions.md instead of an invented name.}}

<!-- mirage:section consent -->
## Consent

{{State which events depend on tracking consent and what the product sends, if anything, before that consent is given. Point to docs/privacy.md for the consent mechanism itself and cite the requirement this satisfies. An unresolved consent gate becomes a question in docs/questions.md.}}

<!-- mirage:section verification -->
## Verification

{{State how the team confirms an event actually arrives at its destination with the right properties, such as a debug view, a staging destination or an automated check in the test suite. Cite the test scenario or requirement this verification closes. Mark any volume or accuracy target as a hypothesis until a release has measured it.}}
