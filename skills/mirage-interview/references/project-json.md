# .mirage/project.json

This file describes what is being built. It decides every later question and document, so settle it first. `python3 .mirage/check.py check --only project` validates the file.

```json
{
  "mirage_version": "0.1.0",
  "name": "Fernleaf Tea",
  "language": "en",
  "components": [
    {"id": "api", "kind": "backend-service"},
    {"id": "kiosk", "kind": "shop-kiosk"}
  ],
  "flags": {"personal_data": true, "payments": true, "analytics": true},
  "integrations": ["stripe", "mailchimp"],
  "regulated": [],
  "domain_topics": ["loyalty-points"],
  "include": ["ux", "design-system"],
  "documents": [
    {
      "id": "tea-sourcing",
      "title": "Tea sourcing",
      "sections": [
        {"key": "suppliers", "title": "Suppliers"},
        {"key": "seasons", "title": "Seasons and stock"}
      ],
      "areas": [
        {"key": "suppliers", "ask": "Which estates supply each tea, and what happens when one cannot deliver."},
        {"key": "seasons", "ask": "Which teas are seasonal, and how the shop shows one that has run out."}
      ]
    }
  ],
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
| `components` | Every part that is built and delivered on its own, each with a lowercase `id` and a `kind`. The kinds are described below. |
| `flags` | Each true or false, and missing means false. The flags are listed below. |
| `integrations` | One lowercase slug per third-party system the product's own code calls or receives calls from at runtime, such as `stripe` or `hubspot`. Each gets its own document. Tools the team only uses, such as the CI service, hosting or error tracking, belong in `docs/operations.md` instead. |
| `regulated` | One slug per regulation or standard that applies, such as `gdpr`, `hipaa` or `pci-dss`. |
| `domain_topics` | One slug per business rule set complex enough for its own spec, such as `pricing`, `loyalty-points` or `scheduling`. |
| `include` | Optional. Catalog documents to plan although no facet switched them on, by ID. `plan` lists the ones available. |
| `documents` | Optional. Documents this project needs that the catalog does not have. They are described below. |
| `releases` | Release names in shipping order, such as `beta`, `v1.0` and `v1.1`. |
| `areas` | The lanes that do the work, used as `area:<name>` labels, such as `backend`, `firmware`, `docs` and `infra`. Count the work that is not building, such as sourcing, compliance or production. |
| `require_confirmed_delegation` | `true` makes delegated answers block work until the owner confirms them. The default is `false`. |

## Component kinds

A kind is a lowercase slug. The catalog has documents of its own for these kinds:

`website`, `web-app`, `mobile-app`, `desktop-app`, `browser-extension`, `backend-service`, `cli`, `library`, `data-pipeline`, `game`

Use one of them when it describes the part. A phone app with an API and an admin panel is three components.

When none describes the part, write the kind in your own slug, such as `firmware`, `smart-contract`, `terraform-module`, `ml-model` or `circuit-board`. The part is then planned a component specification at `docs/components/<id>.md`. A custom kind is not a lesser choice. It is the right one whenever a catalog kind would describe the part wrongly.

A part of a custom kind can still use catalog documents. A kiosk that people operate through a screen needs the UX and design system documents, so the example lists them in `include`.

## Project documents

Declare a project document when the project must write something down that no planned document holds, such as a bill of materials, a model evaluation plan or a curriculum outline.

| Key | What to settle |
|---|---|
| `id` | A lowercase slug that no catalog document uses. Area keys start with it. |
| `title` | The document's title. |
| `path` | Optional. A Markdown file under `docs/`. The default is `docs/<id>.md`. |
| `sections` | The outline: one `key` and `title` per section, in reading order. The validator requires each one in the file. |
| `areas` | What the interview must settle for this document: one `key` and `ask` per question area. Write each `ask` as the question itself. |

Keep a project document to one subject. Two subjects are two documents.

## Flags

| Flag | True when |
|---|---|
| `accounts` | People sign up or sign in to the product you build. Staff signing in to a vendor's hosted tool, such as a CMS, does not count. |
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
| `admin` | Staff use back-office tools that you build. A vendor's own admin screens do not count. |
| `migration` | The product replaces an existing system, site or app. |
| `file_formats` | The product reads or writes its own file formats or configuration files that people or other tools depend on. |
| `source_documents` | Input documents, such as a client brief, must be preserved unchanged under `docs/sources/`. |
