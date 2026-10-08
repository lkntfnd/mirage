<!-- mirage:doc formats -->
# File and data formats

{{One paragraph: which files or payloads the product reads and writes that other people or tools depend on, and that this document is their contract. Name the requirements that call for each format as REQ-<AREA>-<NNN>.}}

<!-- mirage:section formats -->
## Formats

{{One row per format the product owns or must accept. Direction is read, write or both. Consumers names who else reads or writes the file, such as users editing it by hand, another tool or a later version of this product.}}

| Format | File name or location | Encoding | Direction | Consumers | Requirements |
|---|---|---|---|---|---|
| {{Format name}} | {{Pattern or path}} | {{Such as UTF-8 JSON}} | {{read, write or both}} | {{Who depends on it}} | {{REQ-AREA-001}} |

<!-- mirage:section schema -->
## Schema

{{One subsection per format. List every field with its type, whether it is required, its default and its meaning. State the units of every number and the format of every date. Point to a machine-readable schema file when one exists. A field whose meaning nobody decided becomes a question in docs/questions.md, never a guess.}}

| Field | Type | Required | Default | Meaning |
|---|---|---|---|---|
| {{field}} | {{type}} | {{yes or no}} | {{value or none}} | {{What it means}} |

<!-- mirage:section versioning -->
## Versioning and compatibility

{{State how a file declares its format version, which changes are compatible, how the product reads files written by older versions, and how long old versions stay readable. Cite the question that set the policy.}}

<!-- mirage:section validation -->
## Validation and errors

{{State what the product does with a malformed file, an unknown field, a missing required field and an unsupported version. Give the exact error a user sees for each, and say whether processing stops or continues.}}

<!-- mirage:section examples -->
## Examples

{{Give one minimal valid example and one realistic example per format, in fenced code blocks, plus one invalid example with the error it produces. Use invented data only.}}
