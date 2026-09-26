# Document catalog

Generated from `skills/mirage/scripts/catalog.json` by `scripts/render_catalog.py`. Edit the JSON, then rerun the script.

The catalog holds 37 document kinds, 198 question areas and 43 typical inputs.

## Facets

- Component kinds: `website`, `web-app`, `mobile-app`, `desktop-app`, `browser-extension`, `backend-service`, `cli`, `library`, `data-pipeline`, `embedded`, `game`.
- Flags: `accounts`, `personal_data`, `payments`, `cms`, `i18n`, `analytics`, `notifications`, `search`, `offline`, `realtime`, `ai`, `admin`, `migration`, `source_documents`.
- Lists: `integrations`, `regulated`, `domain_topics`.

## Documents

| Document | Path | Included when | Sections | Areas | Inputs |
|---|---|---|---|---|---|
| Glossary (`glossary`) | `CONTEXT.md` | always | 0 | 1 | 0 |
| Question register (`questions`) | `docs/questions.md` | always | 0 | 0 | 0 |
| Inputs register (`inputs`) | `docs/inputs.md` | always | 0 | 0 | 0 |
| Documentation index (`index`) | `docs/README.md` | always | 0 | 0 | 0 |
| Product requirements (`prd`) | `docs/prd.md` | always | 7 | 8 | 1 |
| Architecture (`architecture`) | `docs/architecture.md` | always | 6 | 7 | 2 |
| Security (`security`) | `docs/security.md` | always | 6 | 7 | 1 |
| Test strategy (`test-strategy`) | `docs/test-strategy.md` | always | 6 | 6 | 1 |
| Operations (`operations`) | `docs/operations.md` | always | 7 | 9 | 4 |
| Agent rules (`agents`) | `AGENTS.md` | always | 7 | 5 | 0 |
| User experience (`ux`) | `docs/ux.md` | a component of kind website, web-app, mobile-app, desktop-app, browser-extension, game | 7 | 8 | 2 |
| Screen or page spec (`screen`) | `docs/specs/{component}/{name}.md` | one per screen or page listed in `ux` | 10 | 0 | 0 |
| Design system (`design-system`) | `docs/design-system.md` | a component of kind website, web-app, mobile-app, desktop-app, browser-extension, game | 6 | 6 | 3 |
| Performance (`performance`) | `docs/performance.md` | a component of kind website, web-app, mobile-app, desktop-app, browser-extension, game, backend-service | 4 | 4 | 0 |
| Content (`content`) | `docs/content.md` | a component of kind website or flag `cms` | 6 | 6 | 4 |
| Search engine optimization (`seo`) | `docs/seo.md` | a component of kind website | 6 | 7 | 2 |
| API (`api`) | `docs/api.md` | a component of kind backend-service | 10 | 8 | 0 |
| Data model (`data-model`) | `docs/data-model.md` | a component of kind backend-service, data-pipeline or flag `accounts` | 5 | 5 | 1 |
| Command-line interface (`cli`) | `docs/cli.md` | a component of kind cli | 6 | 6 | 0 |
| Public API (`public-api`) | `docs/public-api.md` | a component of kind library | 6 | 6 | 0 |
| Platform (`platform`) | `docs/platforms/{kind}.md` | one per component kind among mobile-app, desktop-app, browser-extension, embedded, game | 6 | 7 | 3 |
| Data pipeline (`data-pipeline`) | `docs/data-pipeline.md` | a component of kind data-pipeline | 6 | 6 | 1 |
| AI features (`ai`) | `docs/ai.md` | flag `ai` | 7 | 7 | 2 |
| Authentication and accounts (`auth`) | `docs/auth.md` | flag `accounts` | 6 | 7 | 1 |
| Privacy (`privacy`) | `docs/privacy.md` | flag `personal_data` | 7 | 8 | 2 |
| Payments (`payments`) | `docs/payments.md` | flag `payments` | 8 | 8 | 3 |
| Localization (`i18n`) | `docs/i18n.md` | flag `i18n` | 6 | 7 | 1 |
| Analytics events (`events`) | `docs/events.md` | flag `analytics` | 6 | 6 | 1 |
| Integration (`integration`) | `docs/integrations/{item}.md` | one per entry in `integrations` | 7 | 7 | 2 |
| Notifications (`notifications`) | `docs/notifications.md` | flag `notifications` | 6 | 6 | 2 |
| Search (`search`) | `docs/search.md` | flag `search` | 7 | 6 | 0 |
| Offline and realtime (`offline-realtime`) | `docs/offline-realtime.md` | flag `offline` or flag `realtime` | 4 | 5 | 0 |
| Admin tools (`admin`) | `docs/admin.md` | flag `admin` | 4 | 5 | 0 |
| Compliance (`compliance`) | `docs/compliance.md` | `regulated` is not empty | 4 | 4 | 1 |
| Migration (`migration`) | `docs/migration.md` | flag `migration` | 5 | 5 | 2 |
| Domain rules (`domain`) | `docs/domain/{item}.md` | one per entry in `domain_topics` | 6 | 5 | 0 |
| Preserved sources (`sources`) | `docs/sources/SHA256SUMS` | flag `source_documents` | 0 | 0 | 1 |

## Question areas

### Glossary (`glossary`)

- `terms`: Which words the project uses for its core concepts, and which synonyms to avoid.

### Product requirements (`prd`)

- `problem`: What problem the product solves, for whom, and why now.
- `users`: Which kinds of users exist, what each role may do, and which role matters most.
- `goals`: Which measurable outcomes define success, with target values and a date or release.
- `scope`: Which capabilities the first release must have, and which can wait.
- `releases`: Which releases are planned, their names, and what each one adds.
- `constraints`: Which fixed constraints apply: budget, deadlines, mandated technology, legal limits.
- `references`: Which existing products to learn from, and what to copy or avoid in each.
- `exclusions`: What the product will explicitly not do.

Typical inputs: Existing briefs, specifications or pitch documents (information).

### Architecture (`architecture`)

- `stack`: Which languages, frameworks and runtimes each component uses, and any mandated or forbidden choices.
- `hosting`: Where each component runs, and who owns those accounts.
- `data-flows`: How data moves between components and external systems.
- `environments`: Which environments exist, such as local, staging and production, and what differs between them.
- `repository`: Whether the code lives in one repository or several, and how directories map to components.
- `existing`: Which existing systems, code or infrastructure the project must reuse or connect to.
- `scale`: What load and growth the system must handle at launch and a year later.

Typical inputs: Access to existing code repositories (access); Hosting or cloud account (account).

### Security (`security`)

- `assets`: Which data and capabilities would hurt most if leaked, altered or lost.
- `threats`: Who might attack or abuse the product, and how.
- `authorization`: How access is decided for each role and resource.
- `secrets`: Where secrets live, who can read them, and how they rotate.
- `supply-chain`: How dependencies and committed secrets are scanned, and what blocks a merge.
- `incidents`: Who responds to a security incident, how they are reached, and who must be told.
- `testing`: Which security testing is required before launch, such as a penetration test.

Typical inputs: Security contact and escalation path (information).

### Test strategy (`test-strategy`)

- `levels`: Which test levels are expected, such as unit, integration and end-to-end, and what each must cover.
- `matrix`: Which devices, browsers, operating systems or runtimes must be tested.
- `data`: Which test data and fixtures exist, and whether production data may be used.
- `manual`: Which checks stay manual, and who runs them.
- `acceptance`: Who accepts finished work, and on what evidence.
- `gates`: Which checks must pass before a merge and before a release.

Typical inputs: Test devices or device-cloud access (tool).

### Operations (`operations`)

- `ci`: Which CI service runs the checks, and on which events.
- `deploy`: How each component is deployed, and who may deploy.
- `cadence`: How often releases ship, and how they are announced.
- `rollback`: How a bad release is rolled back, and how fast.
- `monitoring`: Which logs, metrics, alerts and error tracking exist, and who receives alerts.
- `backups`: What is backed up, how often, and how much data loss and downtime are acceptable.
- `domains`: Which domains exist, who controls DNS, and how certificates renew.
- `support`: How users report problems, and who handles them.
- `costs`: What the running costs may be, and who pays them.

Typical inputs: CI service account (account); Hosting and deployment access (access); Domain registrar and DNS access (access); Error tracking account (account).

### Agent rules (`agents`)

- `builders`: Which agents and people build the project, and which area each owns.
- `areas`: Which area labels the project uses.
- `branching`: Which base branch work starts from, and how branches are named.
- `review`: Who reviews and who merges, and whether agents may merge.
- `autonomy`: What agents may do without asking, such as pushing, opening pull requests or deploying.

### User experience (`ux`)

- `basis`: Whether designs already exist, where, and how closely to follow them.
- `inventory`: Which screens or pages exist in the first release.
- `flows`: Which user journeys matter most, step by step.
- `navigation`: How users move between screens, and what the main navigation holds.
- `states`: How each screen behaves while loading, when empty, on error and offline.
- `accessibility`: Which accessibility standard applies, such as WCAG 2.2 AA.
- `responsive`: Which screen sizes, orientations and input methods must work.
- `links`: Which screens can be opened from a link, a notification or another app.

Typical inputs: Design files or wireframes (asset); Access to the design tool (tool).

### Design system (`design-system`)

- `brand`: Which brand identity exists, and what may not change.
- `typography`: Which typefaces are used, and whether their licenses cover the product.
- `color`: Which colors are used, and whether a dark theme is required.
- `components`: Whether to use an existing component library, and which one.
- `motion`: How much animation the product uses, and whether reduced motion is respected.
- `imagery`: Which icon set and image style are used, and where images come from.

Typical inputs: Logo files in vector format (asset); Brand guidelines (asset); Font files and licenses (asset).

### Performance (`performance`)

- `budgets`: Which speed targets apply, such as page load, app start or API latency.
- `conditions`: On which devices and networks the targets must hold.
- `load`: How many users or requests the system must serve at peak.
- `measurement`: How and where each target is measured.

### Content (`content`)

- `types`: Which kinds of content exist, such as pages, posts or products, and their fields.
- `sources`: Who writes the content, and which content already exists.
- `cms`: Which content management system is used, and who edits in it.
- `workflow`: How content is drafted, reviewed and published.
- `media`: How images and videos are sourced, sized and stored.
- `legal`: Which legal pages are required, such as privacy policy, terms and imprint, and who writes them.

Typical inputs: Existing content to reuse (information); Legal texts (information); Photos, videos and other media (asset); Content management system account (account).

### Search engine optimization (`seo`)

- `markets`: Which markets, languages and search terms matter.
- `indexing`: Which pages search engines should index, and which not.
- `metadata`: How page titles and descriptions are written.
- `structured-data`: Which structured data types apply, such as organization, product or article.
- `redirects`: Which old URLs must redirect, and where.
- `social`: How shared links look on social networks and messengers.
- `tools`: Which search console accounts exist, and who owns them.

Typical inputs: Search console access (access); List of existing URLs (information).

### API (`api`)

- `consumers`: Which clients call the API, and which of them are outside the team's control.
- `style`: Which API style is used, such as REST, GraphQL or gRPC, and which contract format.
- `auth`: How callers authenticate, and how permissions are checked.
- `errors`: How errors are reported, and which error codes clients rely on.
- `versioning`: How breaking changes are introduced, and how long old versions live.
- `limits`: Which rate limits and quotas apply.
- `idempotency`: Which operations must be safe to retry.
- `webhooks`: Which webhooks the system sends or receives.

### Data model (`data-model`)

- `entities`: Which entities exist, and how they relate.
- `storage`: Which databases or stores hold the data, and why.
- `volume`: How much data exists at launch, and how fast it grows.
- `retention`: How long each kind of data is kept, and how it is deleted.
- `migrations`: How schema changes are applied and rolled back.

Typical inputs: Access to existing data (access).

### Command-line interface (`cli`)

- `commands`: Which commands and subcommands exist, and what each does.
- `output`: Which output formats are supported, such as text for people and JSON for scripts.
- `configuration`: How the tool is configured: flags, files and environment variables, and their precedence.
- `errors`: How errors are reported, and which exit codes scripts rely on.
- `distribution`: How the tool is installed, such as a package registry, Homebrew or binaries.
- `platforms`: Which operating systems and architectures are supported.

### Public API (`public-api`)

- `audience`: Who uses the library, and in which kinds of projects.
- `exports`: Which functions, types and modules are public.
- `versioning`: Which versioning policy applies, and what counts as a breaking change.
- `compatibility`: Which language, runtime and platform versions are supported.
- `distribution`: Which registry publishes the library, and who can publish.
- `reference`: How the API reference is generated and hosted.

### Platform (`platform`)

- `targets`: Which platforms and minimum versions are supported.
- `distribution`: Which stores or channels distribute the product, and whose accounts publish it.
- `permissions`: Which device permissions are needed, and why each one.
- `updates`: How updates reach users, and whether old versions can be forced to update.
- `signing`: Who holds the signing keys and certificates.
- `crashes`: How crashes are reported and triaged.
- `device-features`: Which device features are used, such as camera, location, push or biometrics.

Typical inputs: App store or distribution accounts (account); Access to signing keys and certificates (access); Physical test devices (tool).

### Data pipeline (`data-pipeline`)

- `sources`: Which systems the data comes from, and in which formats.
- `freshness`: How fresh the output must be.
- `transformations`: Which transformations produce the output.
- `quality`: Which quality checks run, and what happens when one fails.
- `backfills`: How historical data is reprocessed.
- `consumers`: Who uses the output, and how.

Typical inputs: Access to source systems (access).

### AI features (`ai`)

- `use-cases`: Which user problems the AI features solve, and what a good answer looks like.
- `provider`: Which model providers are allowed, and whether data may leave the region.
- `data`: Which data grounds or trains the features, and whether users consented to that use.
- `evaluation`: How quality is measured before and after release.
- `safety`: Which harmful outputs or abuse must be prevented, and when a person reviews results.
- `cost`: What each request may cost, and the monthly limit.
- `fallback`: What users see when the model is slow, wrong or unavailable.

Typical inputs: Model provider account (account); Evaluation examples (information).

### Authentication and accounts (`auth`)

- `providers`: Which sign-in methods are offered, such as email, phone, social or single sign-on.
- `sign-up`: What sign-up collects, and whether it needs verification or approval.
- `sessions`: How long sessions last, and on how many devices.
- `roles`: Which roles exist, and what each may do.
- `recovery`: How users recover a lost account.
- `deletion`: How users delete their account, and what happens to their data.
- `guests`: What people can do without an account.

Typical inputs: Identity provider console access (account).

### Privacy (`privacy`)

- `data`: Which personal data is collected, and why each item is needed.
- `jurisdictions`: Which privacy laws apply, such as GDPR or CCPA, based on where users live.
- `consent`: Which processing needs consent, and how it is collected and withdrawn.
- `retention`: How long personal data is kept.
- `requests`: How users access, export or delete their data, and who handles requests.
- `processors`: Which third parties receive personal data.
- `cookies`: Which cookies and trackers are set, and which need consent.
- `children`: Whether children may use the product.

Typical inputs: Privacy policy text or its author (information); Privacy or legal contact (information).

### Payments (`payments`)

- `provider`: Which payment provider is used, and who owns the merchant account.
- `methods`: Which payment methods are offered.
- `flows`: Which payment flows exist, such as one-off payments, subscriptions or deposits.
- `currencies`: Which currencies are accepted, and how prices are rounded.
- `taxes`: Which taxes apply, and who calculates them.
- `refunds`: Who may refund, how much, and how disputes are handled.
- `reconciliation`: How payments are matched against orders and payouts.
- `failures`: What happens when a payment fails, times out or is confirmed twice.

Typical inputs: Merchant account (account); Payment provider sandbox access (access); Tax rules from an accountant (information).

### Localization (`i18n`)

- `locales`: Which languages and regions are supported at launch and later.
- `default`: Which language is the default, and how the language is chosen.
- `fallback`: What is shown when a translation is missing.
- `workflow`: Who translates, with which tools, and how translations are reviewed.
- `formats`: How dates, numbers, currencies and addresses are formatted per locale.
- `rtl`: Whether any right-to-left language is supported.
- `content`: Whether user and editorial content is translated, and how.

Typical inputs: Existing translations or translators (information).

### Analytics events (`events`)

- `questions`: Which business questions analytics must answer.
- `tools`: Which analytics tools receive events.
- `events`: Which user actions and system events are tracked.
- `identity`: How users are identified across sessions and devices.
- `consent`: Which tracking needs consent.
- `verification`: How the team verifies that events arrive correctly.

Typical inputs: Analytics tool account (account).

### Integration (`integration`)

- `purpose`: What the integration is for, and which requirements depend on it.
- `direction`: Which way data flows, and whether it is real time or scheduled.
- `auth`: How the project authenticates with the system, and who owns the credentials.
- `limits`: Which rate limits, quotas and costs apply.
- `mapping`: How the system's data maps onto the project's data.
- `failures`: What happens when the system is slow, down or returns bad data.
- `sandbox`: Whether a sandbox or test environment exists.

Typical inputs: API documentation (information); Sandbox or test account (account).

### Notifications (`notifications`)

- `channels`: Which channels are used, such as email, push, SMS or in-app.
- `triggers`: Which events send a notification, and to whom.
- `templates`: Who writes the messages, and in which languages.
- `preferences`: What users can switch on or off.
- `caps`: How many messages a user may receive per day or week.
- `provider`: Which delivery providers are used.

Typical inputs: Email, push or SMS provider account (account); Sender domain and DNS access (access).

### Search (`search`)

- `scope`: What users can search for.
- `engine`: Which search engine is used, and how the index stays fresh.
- `ranking`: What decides the order of results.
- `filters`: Which filters and facets are offered.
- `languages`: Which languages and spelling mistakes search must handle.
- `zero-results`: What users see when nothing matches.

### Offline and realtime (`offline-realtime`)

- `offline-scope`: What must work without a connection.
- `caching`: What is cached on the device, and for how long.
- `conflicts`: How conflicting edits are resolved.
- `realtime-scope`: What must update live without a refresh.
- `transport`: Which mechanism delivers live updates, such as WebSockets or server-sent events.

### Admin tools (`admin`)

- `modules`: Which admin screens and tools exist.
- `roles`: Which staff roles exist, and what each may do.
- `workflows`: Which operational workflows staff perform, such as moderation or refunds.
- `audit`: Which staff actions are logged, and for how long.
- `bulk`: Which bulk imports, exports or edits are needed.

### Compliance (`compliance`)

- `regimes`: Which regulations or standards apply, such as HIPAA, PCI DSS or SOC 2.
- `obligations`: Which concrete obligations each regime imposes on this product.
- `audits`: Which audits or certifications are needed, and when.
- `evidence`: Which evidence each obligation needs, and where it is kept.

Typical inputs: Existing compliance documents or policies (information).

### Migration (`migration`)

- `current`: What the current system does, and what must survive the move.
- `data`: Which data moves, how it is transformed, and how it is verified.
- `urls`: Which URLs, links or integrations must keep working.
- `cutover`: How and when the switch happens, and what freezes during it.
- `rollback`: How to return to the old system if the cutover fails.

Typical inputs: Access to the current system (access); Export of the current data (information).

### Domain rules (`domain`)

- `rules`: Which rules decide the outcome, stated precisely.
- `examples`: Which worked examples show the rules in action.
- `edge-cases`: Which edge cases and conflicts between rules must be handled.
- `constants`: Which numbers may be tuned after launch, and who tunes them.
- `admin`: Which rules staff can change without a release.
