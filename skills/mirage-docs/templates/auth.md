<!-- mirage:doc auth -->
# Authentication and accounts

{{One paragraph: state that this document fixes how people sign up, sign in and are identified in the product, which identity providers and roles exist, and how an account is recovered or removed. Name docs/prd.md as the source for the requirements this document satisfies and docs/questions.md as where an unresolved choice about accounts is recorded as a question.}}

<!-- mirage:section identity -->
## Identity providers

{{State which sign-in methods this document covers, such as an email and password, a phone number, a social account or a workplace single sign-on. If the product supports more than one method for the same account, state whether they can be linked and how. Cite the requirement each provider satisfies as REQ-<AREA>-<NNN>. An unsettled provider choice becomes a question in docs/questions.md instead of a named vendor.}}

<!-- mirage:section sign-in -->
## Sign-up and sign-in

{{Describe what sign-up collects and why each field is needed, whether an email or phone number must be verified before the account is usable, and whether any role needs manual approval before it can sign in. State what a person can do before creating an account, if anything, and cite the requirement that allows it. An unresolved approval rule becomes a question in docs/questions.md rather than an assumed one.}}

<!-- mirage:section sessions -->
## Sessions

{{State how long a session stays signed in, whether it renews on activity, and how many concurrent devices or sessions one account may hold. Mark any duration or device limit as a hypothesis until a release has measured real use. State what happens to other open sessions when a password changes or an account is recovered.}}

<!-- mirage:section roles -->
## Roles and permissions

{{List every role this product defines and, for each capability area drawn from the requirements, mark whether that role may act on it fully, not at all or only on records it owns. Name the capability columns after the areas that matter most for this product. Cite the requirement that grants each capability as REQ-<AREA>-<NNN>. A role or capability still undecided becomes a question in docs/questions.md instead of a guessed default.}}

| Role | {{Capability 1}} | {{Capability 2}} | {{Capability 3}} |
|---|---|---|---|
| {{Role name}} | {{yes, no or own-only}} | {{yes, no or own-only}} | {{yes, no or own-only}} |

<!-- mirage:section recovery -->
## Account recovery

{{State how a person recovers a lost account, such as an emailed reset link or a phone code, and how the product checks it is really them before granting access. State how long a recovery link or code stays valid and what happens to open sessions once recovery succeeds. Cite the requirement this satisfies and record an unresolved identity check as a question in docs/questions.md.}}

<!-- mirage:section deletion -->
## Account deletion

{{State how a person deletes their own account, whether the request needs a waiting period or a support step, and what happens to their content and personal data afterward. Point to docs/privacy.md for retention rules that outlive the account itself. Cite the requirement that grants self deletion and record any exception, such as data a law requires the product to keep, as a question or as a requirement with scope OUT.}}
