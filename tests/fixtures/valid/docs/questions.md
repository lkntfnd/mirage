# Question register

Every question the owner decides, with a recommendation and a status.

### Q-001 What problem does the app solve, and for whom?

- Status: answered
- Covers: glossary/terms, prd/problem, prd/users, prd/goals, prd/scope, prd/releases, prd/constraints, prd/references, prd/exclusions
- Recommendation: Booking by phone call wastes the mechanics' time; the app lets customers book themselves.
- Answer: Customers book themselves; v1.0 before the spring season. Answered on 2026-09-20.

### Q-002 Which stack and hosting does the project use?

- Status: answered
- Covers: architecture/stack, architecture/hosting, architecture/data-flows, architecture/environments, architecture/repository, architecture/existing, architecture/scale
- Recommendation: One API service and a cross-platform app, on a managed container host.
- Answer: As recommended. Answered on 2026-09-20.

### Q-003 What must the security model protect?

- Status: delegated
- Covers: security/assets, security/threats, security/authorization, security/secrets, security/supply-chain, security/incidents, security/testing
- Recommendation: Protect customer contact data with one-time codes and rate limits.
- Answer: As recommended. Delegated on 2026-09-21.

### Q-004 How is the product tested?

- Status: answered
- Covers: test-strategy/levels, test-strategy/matrix, test-strategy/data, test-strategy/manual, test-strategy/acceptance, test-strategy/gates
- Recommendation: Unit, API and one end-to-end flow, with synthetic data only.
- Answer: As recommended. Answered on 2026-09-21.

### Q-005 How is the product deployed and operated?

- Status: answered
- Covers: operations/ci, operations/deploy, operations/cadence, operations/rollback, operations/monitoring, operations/backups, operations/domains, operations/support, operations/costs
- Recommendation: Deploy staging on merge and production on a tag.
- Answer: As recommended. Answered on 2026-09-21.

### Q-006 How do agents work on the project?

- Status: delegated
- Covers: agents/builders, agents/areas, agents/branching, agents/review, agents/autonomy
- Recommendation: Two agents, one per lane, that open pull requests but never merge.
- Answer: As recommended. Delegated on 2026-09-22.

### Q-007 How should the app look and flow?

- Status: answered
- Covers: ux/basis, ux/inventory, ux/flows, ux/navigation, ux/states, ux/accessibility, ux/responsive, ux/links, design-system/brand, design-system/typography, design-system/color, design-system/components, design-system/motion, design-system/imagery
- Blocks: M1-E01-S02
- Recommendation: Follow platform conventions with the shop's green.
- Answer: As recommended. Answered on 2026-09-22.

### Q-008 Which performance targets apply?

- Status: answered
- Covers: performance/budgets, performance/conditions, performance/load, performance/measurement
- Recommendation: Two-second start and 300 ms API latency at p95.
- Answer: As recommended. Answered on 2026-09-22.

### Q-009 What does the API expose and store?

- Status: answered
- Covers: api/consumers, api/style, api/auth, api/errors, api/versioning, api/limits, api/idempotency, api/webhooks, data-model/entities, data-model/storage, data-model/volume, data-model/retention, data-model/migrations
- Recommendation: A small JSON API over one relational database.
- Answer: As recommended. Answered on 2026-09-23.

### Q-010 Which mobile platforms are supported?

- Status: answered
- Covers: platform:mobile-app/targets, platform:mobile-app/distribution, platform:mobile-app/permissions, platform:mobile-app/updates, platform:mobile-app/signing, platform:mobile-app/crashes, platform:mobile-app/device-features
- Recommendation: Both major mobile platforms, two versions back.
- Answer: As recommended. Answered on 2026-09-23.

### Q-011 How does the app talk to Sprocket Supply?

- Status: answered
- Covers: integration:sprocket-supply/purpose, integration:sprocket-supply/direction, integration:sprocket-supply/auth, integration:sprocket-supply/limits, integration:sprocket-supply/mapping, integration:sprocket-supply/failures, integration:sprocket-supply/sandbox
- Blocks: M1-E02-S02
- Recommendation: Use the supplier's stock endpoint with an API key.
- Answer: As recommended. Answered on 2026-09-23.

### Q-012 Which reminders does the app send?

- Status: open
- Covers: notifications/channels, notifications/triggers, notifications/templates, notifications/preferences, notifications/caps, notifications/provider
- Blocks: M2-E01-S01, REQ-NOTE-001
- Recommendation: One push reminder the day before the booking.
