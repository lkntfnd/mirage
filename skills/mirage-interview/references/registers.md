# Register formats

The validator parses both registers, so keep the field names exactly as shown and write one field per line. Field values may be in the project's language. Status and kind values stay English.

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
| `Covers` | A comma-separated list of area keys from `check.py plan`. |
| `Blocks` | Optional. A comma-separated list of the requirement, backlog and input IDs that wait on this question. |
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
| `Needed for` | Document keys and backlog IDs that need it. |
| `How to get` | Required while missing. Concrete steps the owner can follow. |
| `Location` | Required once provided. Where it lives, such as a path, a URL or a password manager entry name. Never a secret itself. |
| `Owner` | Optional. Who obtains it. |
