<!-- mirage:doc design-system -->
# Design system

{{One paragraph: which brand identity governs this product and what this document fixes about typography, color, components, motion and imagery so every surface stays consistent. Say that an unresolved license, vendor or version becomes a question in docs/questions.md as (Q-nnn) rather than an invented one.}}

<!-- mirage:section tokens -->
## Tokens

{{One paragraph: which values are stored as reusable tokens, such as spacing, radius and elevation, and where the token source of truth lives, such as a file or a design tool. Name the brand elements that may not change, and record missing brand guidelines as an input in docs/inputs.md with ID IN-nnn.}}

<!-- mirage:section typography -->
## Typography

{{One row per typeface used: its role, its weights and whether its license covers this product's distribution. Record a missing font file or license as an input in docs/inputs.md with ID IN-nnn.}}

| Typeface | Role | Weights | License covers this use |
|---|---|---|---|
| {{Typeface name}} | {{Heading, body or code}} | {{Weights used}} | {{Yes, no or unconfirmed}} |

<!-- mirage:section color -->
## Color

{{One row per color role: its value and whether a dark theme variant exists. State whether the product requires a dark theme, and record that decision as a question in docs/questions.md as (Q-nnn) if it is still open.}}

| Role | Light value | Dark value |
|---|---|---|
| {{Role, such as background, primary or danger}} | {{Hex or token}} | {{Hex or token, or "same"}} |

<!-- mirage:section components -->
## Components

{{One paragraph: whether the product builds on an existing component library or a custom one, which library and version if so, and where its documentation lives. Name any component this product must not use from that library, and record an unconfirmed vendor or version as a question in docs/questions.md as (Q-nnn).}}

<!-- mirage:section motion -->
## Motion

{{One paragraph: how much animation the product uses and where, such as transitions, loading states or feedback, and whether reduced motion preferences are respected. Cite the REQ-<AREA>-<NNN> requirement that calls for an animated interaction.}}

<!-- mirage:section imagery -->
## Icons and imagery

{{One paragraph: which icon set the product uses and the style rules for photography or illustration, such as aspect ratio, tone and subject. State where images are sourced from, and record missing logo files or other media as an input in docs/inputs.md with ID IN-nnn.}}
