<!-- mirage:doc screen -->
# Screen or page spec

<!-- mirage:section purpose -->
## Purpose

Book a repair slot for one bike (REQ-BOOK-001).

<!-- mirage:section entry -->
## Entry points

The booking tab and a reminder notification.

<!-- mirage:section layout -->
## Layout and content

A service picker above a list of free slots.

<!-- mirage:section states -->
## States

Loading shows placeholders; an empty day says no slots are free.

<!-- mirage:section interactions -->
## Interactions

Tapping a slot opens the confirmation step.

<!-- mirage:section data -->
## Data

Slots come from the slots endpoint.

<!-- mirage:section events -->
## Analytics events

No analytics events in v1.0.

<!-- mirage:section strings -->
## Text and translations

English only in v1.0.

<!-- mirage:section accessibility -->
## Accessibility

Every slot has a spoken label with its time.

<!-- mirage:section acceptance -->
## Acceptance criteria

A customer books a free slot in three taps.
