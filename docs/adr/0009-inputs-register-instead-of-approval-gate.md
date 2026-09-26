---
status: accepted
---

# Mirage lists the inputs the documentation needs instead of gating on approval

Mirage does not wait for anyone's sign-off. It tells the developer what the documentation cannot be completed without: information such as legal texts or existing content, assets such as logos and design files, accounts such as app store or payment-provider accounts, access to existing systems, and tools. Each one becomes an input `IN-nnn` in `docs/inputs.md` with what needs it and how to get it. Documents and backlog items that depend on a missing input stay blocked until it is provided.

Decided by the owner on 2026-09-26.

## Considered options

- A scope-approval gate for projects with an external client. Rejected because mirage serves the developer building the project, whoever they answer to.
