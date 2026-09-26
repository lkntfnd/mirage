<!-- mirage:doc migration -->
# Migration

{{One paragraph: what system this product replaces, and why the move is happening now.
State that docs/questions.md holds every open decision about cutover timing or data ownership.}}

<!-- mirage:section current -->
## Current system

{{Describe what the current system does today, and which of its behaviors must survive the move.
Cite the requirement (REQ-<AREA>-<NNN>) that carries each behavior forward.
Name the input (IN-nnn) needed to reach the current system if the team building this product does not already have it.}}

<!-- mirage:section data -->
## Data migration

{{State which data moves, and how each field is transformed on the way.
State how the result is verified against the source, such as a row count or a checksum comparison.
State whether the move runs once or repeats until cutover, and who signs off on the verified counts.}}

<!-- mirage:section urls -->
## URLs and redirects

{{List every URL pattern, link or external integration that must keep working after the move.
State the redirect rule that preserves each one, such as a permanent redirect to a new path.
An integration whose owner has not confirmed compatibility becomes a question in docs/questions.md.}}

<!-- mirage:section cutover -->
## Cutover

{{State how and when the switch happens, and what freezes on the old system beforehand.
Name who declares the cutover complete, and what evidence that decision rests on.
Treat any cutover date as a hypothesis until the owner confirms it in the register.}}

<!-- mirage:section rollback -->
## Rollback

{{State the condition that triggers a rollback, such as a failed data check or a broken integration.
List the steps that return the product to the old system.
State how long after cutover a rollback stays possible, and who has the authority to call one.}}
