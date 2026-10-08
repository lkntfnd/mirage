# Register formats

The validator parses both registers, so write one field per line and keep each field name exactly as shown, with nothing added inside it. A note such as "hypothesis" belongs in the value, after the colon. Field values may be in the project's language. Status and kind values stay English.

The validator resolves every ID it finds in a register, so a string shaped like a requirement, question, input, ADR or backlog ID must name something that exists. In an example of a naming pattern, write the pattern, such as `<ID>-<slug>`, and never a made-up ID.

## Choosing the next ID

Take the highest existing number in the register and add one. IDs are three digits, such as `Q-001` and `IN-001`. Never reuse or renumber an ID. A withdrawn question stays in the register, answered with the reason it was withdrawn.

## docs/questions.md

Create the file with a `# Questions` heading and one line saying it holds every product decision, followed by the entries.

```markdown
### Q-012 Which payment provider handles card payments?

- Status: delegated
- Covers: payments/provider, integration:stripe/purpose
- Blocks: REQ-PAY-001, M1-E04-S02
- Recommendation: Stripe, because it supports every target country and has a test mode.
- Answer: Stripe. Delegated on 2026-09-26.
```

| Field | Rule |
|---|---|
| `Status` | `open`, `answered` or `delegated`. |
| `Covers` | A comma-separated list of area keys from `check.py plan`, each written `<document>/<area>`. Leave it empty for a question that settles something outside every planned area. |
| `Blocks` | Optional. A comma-separated list of the requirement, backlog and input IDs that wait on this question. Name only IDs that exist. Backlog items need no entry here, because the index adds every item that lists the question in its own `questions`. |
| `Recommendation` | Always present. The answer you propose, and why. |
| `Answer` | Required once the question is answered or delegated. It includes the date as `YYYY-MM-DD`. A confirmation of a delegated answer becomes `Status: answered` with "Confirmed by the owner on YYYY-MM-DD." |
| `Owner` | Optional. Who must answer, when that is not the owner. |
| `Questionnaire` | Optional. The path of a questionnaire that carries this question to someone else. |

## docs/inputs.md

Create the file with a `# Inputs` heading and one line saying it holds everything the project needs from outside the conversation, followed by the entries.

```markdown
### IN-003 Apple Developer Program account

- Status: missing
- Kind: account
- Needed for: platform:mobile-app, M2-E07-S01
- How to get: Enroll the company at developer.apple.com. Organization enrollment needs a D-U-N-S number and takes several days.
- Location:
```

| Field | Rule |
|---|---|
| `Status` | `missing`, `provided` or `not-needed`. |
| `Kind` | `information`, `asset`, `account`, `access` or `tool`. |
| `Needed for` | A comma-separated list of what needs it: document keys from `check.py plan`, such as `operations` or `platform:mobile-app`, and backlog IDs. Add the backlog IDs once the items exist. |
| `How to get` | Required while missing. Concrete steps the owner can follow. |
| `Location` | Required once provided. Where it lives, such as a path, a URL or a password manager entry name. Never a secret itself. |
| `Reason` | Required for `not-needed`. One sentence saying why the project does not need it. |
| `Owner` | Optional. Who obtains it. |
