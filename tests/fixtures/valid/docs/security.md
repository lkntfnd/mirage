<!-- mirage:doc security -->
# Security

<!-- mirage:section assets -->
## Assets and data classification

Customer names, phone numbers and booking history (Q-003).

<!-- mirage:section threats -->
## Threats

Account takeover through guessed phone numbers, and scraping of the booking calendar.

<!-- mirage:section controls -->
## Controls

One-time codes by SMS, rate limits on the booking API, and least-privilege database roles.

<!-- mirage:section secrets -->
## Secrets management

Secrets live in the hosting provider's secret store; the repository holds none.

<!-- mirage:section supply-chain -->
## Dependency and secret scanning

Dependency and secret scanning run on every pull request and block the merge on a finding.

<!-- mirage:section incidents -->
## Incident response

The shop owner is the incident contact and informs affected customers within 72 hours.
