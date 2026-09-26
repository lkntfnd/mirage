<!-- mirage:doc privacy -->
# Privacy

{{One paragraph: state that this document fixes which personal data the product collects, the legal basis for each use, how consent and retention work, and how a person exercises their data rights. Name the jurisdictions this document covers and say that an unresolved legal question is recorded in docs/questions.md rather than assumed.}}

<!-- mirage:section inventory -->
## Personal data inventory

{{List every personal data item the product collects or stores, one row per item, and for each one state why the product needs it, where it comes from, how long it is kept and which legal basis covers it. Cite the requirement that creates the need for the item as REQ-<AREA>-<NNN>. An item whose retention or basis is not yet decided becomes a question in docs/questions.md instead of an assumed answer.}}

| Data item | Purpose | Source | Retention | Legal basis |
|---|---|---|---|---|
| {{Data item}} | {{Why the product needs it}} | {{Where it comes from}} | {{How long it is kept}} | {{Consent, contract, legal obligation or legitimate interest}} |

<!-- mirage:section legal-basis -->
## Legal basis

{{Name which privacy laws apply to this product, such as GDPR or CCPA, based on where the people using it live, and state which legal basis from the inventory table each law requires for each item. Record which jurisdiction the product treats as its baseline. Cite the input that supplies the privacy policy text as IN-nnn where relevant, and record an unresolved jurisdiction as a question in docs/questions.md.}}

<!-- mirage:section consent -->
## Consent

{{State which processing in the inventory table needs consent rather than another legal basis, how that consent is collected at the moment it is needed, and how a person withdraws it later. State what happens to already collected data once consent is withdrawn. Cite the requirement this satisfies and record an undecided consent flow as a question in docs/questions.md.}}

<!-- mirage:section retention -->
## Retention

{{State the retention period for each data item not already fixed in the inventory table, what triggers its deletion, such as account deletion or a fixed schedule, and how a backup or log copy is eventually purged. Mark any retention period as a hypothesis until an owner or a lawyer confirms it, and record an unconfirmed period as a question in docs/questions.md.}}

<!-- mirage:section requests -->
## Data subject requests

{{State how a person asks to access, export or delete their personal data, who inside the project handles the request, and the deadline the product commits to. Cite the input that supplies the privacy or legal contact as IN-nnn. An unhandled request type, such as a request to correct data, becomes its own requirement rather than a silent gap.}}

<!-- mirage:section processors -->
## Processors

{{List every third party that receives personal data from this product, what it receives, why, and whether a data processing agreement exists with it. Do not name a vendor the project has not actually chosen. An undecided processor becomes a question in docs/questions.md instead of an invented name.}}

<!-- mirage:section cookies -->
## Cookies and tracking

{{List the cookies and trackers the product sets, grouped into those that are essential and those that need consent first, and state how a person changes that choice later. State whether children may use the product and, if so, the extra rule that applies. Cite the requirement each tracker satisfies and record an unresolved consent design as a question in docs/questions.md.}}
