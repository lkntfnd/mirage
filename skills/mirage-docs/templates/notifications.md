<!-- mirage:doc notifications -->
# Notifications

{{One paragraph: state that this document fixes which channels the product uses to reach people, which events trigger a message, who writes the templates, and the frequency caps and preferences that keep messages welcome rather than unwanted.}}

<!-- mirage:section channels -->
## Channels

{{List every channel the product uses, such as email, push, SMS or an in-app message, and state which channel is required against which is optional for a given account. Cite the requirement each channel satisfies as REQ-<AREA>-<NNN>. An undecided channel becomes a question in docs/questions.md.}}

<!-- mirage:section triggers -->
## Triggers

{{List every event that sends a notification, who receives it, and which channel carries it. Cite the requirement each trigger satisfies as REQ-<AREA>-<NNN>. A trigger the product defers to a later release becomes a requirement with scope OUT rather than a silent gap.}}

<!-- mirage:section templates -->
## Templates

{{State who writes each message, in which languages, and how a template's variables are filled for a specific person. Point to docs/i18n.md for the translation workflow it shares, or state that the product ships in one language when that document is not planned. An undecided template owner becomes a question in docs/questions.md.}}

<!-- mirage:section preferences -->
## Preferences

{{State which notifications a person can turn on or off, where that choice lives in the product, and which notifications, if any, cannot be turned off, such as a security alert. Cite the requirement this satisfies as REQ-<AREA>-<NNN>.}}

<!-- mirage:section caps -->
## Frequency caps

{{State the maximum number of messages a person may receive per day or week on each channel, and what happens to a message that would exceed the cap, such as queuing or dropping it. Mark any cap as a hypothesis until a release has measured real complaint or unsubscribe rates.}}

<!-- mirage:section deliverability -->
## Deliverability

{{Name the delivery provider for each channel. Cite the input that grants its account as IN-nnn, along with the input for a sender domain and its DNS access. State how the team notices a channel's delivery rate dropping. An undecided provider becomes a question in docs/questions.md instead of an invented vendor.}}
