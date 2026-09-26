# .mirage/project.json

The facets decide every later question and document, so settle them first. `python3 .mirage/check.py check --only project` validates the file.

```json
{
  "mirage_version": "0.1.0",
  "name": "Fernleaf Tea",
  "language": "en",
  "components": [
    {"id": "site", "kind": "website"},
    {"id": "api", "kind": "backend-service"}
  ],
  "flags": {"personal_data": true, "payments": true, "analytics": true},
  "integrations": ["stripe", "mailchimp"],
  "regulated": [],
  "domain_topics": ["loyalty-points"],
  "releases": ["v1.0", "v1.1"],
  "areas": ["frontend", "backend", "infra"],
  "require_confirmed_delegation": false
}
```

| Field | What to settle |
|---|---|
| `mirage_version` | The version printed by `python3 .mirage/check.py version`. |
| `name` | The product's name. |
| `language` | The language documents are written in. English (`en`) is the default. IDs, file names, markers and frontmatter keys stay English in every language. |
| `components` | Every deliverable part, each with a lowercase `id` and a `kind`: `website`, `web-app`, `mobile-app`, `desktop-app`, `browser-extension`, `backend-service`, `cli`, `library`, `data-pipeline`, `embedded` or `game`. A mobile app with an API and an admin panel is three components. |
| `flags` | Each true or false, and missing means false. The flags are listed below. |
| `integrations` | One lowercase slug per third-party system the product talks to, such as `stripe` or `hubspot`. Each gets its own document. |
| `regulated` | One slug per regulation or standard that applies, such as `gdpr`, `hipaa` or `pci-dss`. |
| `domain_topics` | One slug per business rule set complex enough for its own spec, such as `pricing`, `loyalty-points` or `scheduling`. |
| `releases` | Release names in shipping order, such as `beta`, `v1.0` and `v1.1`. |
| `areas` | The lanes that build the product, used as `area:<name>` labels, such as `mobile`, `backend`, `web` and `infra`. |
| `require_confirmed_delegation` | `true` makes delegated answers block work until the owner confirms them. The default is `false`. |

The flags:

| Flag | True when |
|---|---|
| `accounts` | People sign up or sign in. |
| `personal_data` | The product stores or processes data about identifiable people, including contact forms and analytics identifiers. |
| `payments` | Money moves through the product. |
| `cms` | People who are not developers edit content. |
| `i18n` | The product ships in more than one language. |
| `analytics` | User behavior is measured. |
| `notifications` | The product sends email, push, SMS or in-app messages. |
| `search` | Users search the product's content. |
| `offline` | Part of the product must work without a connection. |
| `realtime` | Views update live without a refresh. |
| `ai` | The product calls a machine learning model or a large language model. |
| `admin` | Staff use back-office tools. |
| `migration` | The product replaces an existing system, site or app. |
| `source_documents` | Input documents, such as a client brief, must be preserved unchanged under `docs/sources/`. |
