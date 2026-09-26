<!-- mirage:doc operations -->
# Operations

<!-- mirage:section environments -->
## Environments

Staging deploys on every merge; production deploys on a tagged release (Q-005).

<!-- mirage:section ci-cd -->
## CI/CD

CI runs lint, tests and the mirage check on every pull request.

<!-- mirage:section release -->
## Release and rollback

A release is a tag; rollback redeploys the previous tag.

<!-- mirage:section hosting -->
## Hosting and domains

The API runs on a managed container host; DNS sits with the shop's registrar.

<!-- mirage:section observability -->
## Observability

Error tracking and uptime alerts go to the shop owner's phone.

<!-- mirage:section backups -->
## Backups and recovery

The database is backed up nightly and kept for 30 days.

<!-- mirage:section support -->
## Support

Customers report problems by phone or at the counter.
