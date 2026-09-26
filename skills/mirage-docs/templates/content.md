<!-- mirage:doc content -->
# Content

{{One paragraph: which kinds of content this product publishes and what this document fixes about who writes it, where it lives and how it reaches the page. Say that docs/questions.md holds every open decision about the content management system, and that an unresolved owner or vendor becomes a question there rather than an invented one.}}

<!-- mirage:section model -->
## Content model

{{One row per content type, such as a page, a post or a product: its fields and which are required. Cite the REQ-<AREA>-<NNN> requirement that introduced each type.}}

| Content type | Fields | Required fields |
|---|---|---|
| {{Type name}} | {{Field list}} | {{Which fields cannot be empty}} |

<!-- mirage:section inventory -->
## Page content inventory

{{One row per page the product needs at launch: its content type, who owns writing it and whether the text exists yet. Record existing content to reuse as an input in docs/inputs.md with ID IN-nnn.}}

| Page | Content type | Owner | Status |
|---|---|---|---|
| {{Page name or path}} | {{Type from the model above}} | {{Who writes it}} | {{drafted, reviewed or published}} |

<!-- mirage:section workflow -->
## Editorial workflow

{{One paragraph: how a piece of content moves from draft to review to published, who approves it at each step, and how a correction reaches a live page after launch.}}

<!-- mirage:section cms -->
## Content management

{{One paragraph: which content management system holds this content, who edits in it day to day, and how a new field or content type gets added to it. Record the content management system account as an input in docs/inputs.md with ID IN-nnn if it does not exist yet.}}

<!-- mirage:section media -->
## Media

{{One paragraph: how images and video are sourced, the sizes and formats each surface needs, and where originals are stored. Record missing photos, video or other media as an input in docs/inputs.md with ID IN-nnn.}}

<!-- mirage:section legal -->
## Legal pages

{{One row per required legal page, such as a privacy policy, terms of service or an imprint: who writes its text and whether it exists yet. Record missing legal text as an input in docs/inputs.md with ID IN-nnn.}}

| Page | Required by | Written by | Status |
|---|---|---|---|
| {{Legal page name}} | {{Law or market that requires it}} | {{Who writes it}} | {{missing, drafted or published}} |
