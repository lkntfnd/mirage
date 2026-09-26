<!-- mirage:doc seo -->
# Search engine optimization

{{One paragraph: which markets, languages and search terms matter to this product and what this document fixes about how search engines find and present its pages. Say that an unresolved market or account owner becomes a question in docs/questions.md as (Q-nnn) rather than an invented one.}}

<!-- mirage:section indexing -->
## Indexable pages

{{One row per page type: whether search engines should index it and why. A page that must stay out of the index, such as an account page or a duplicate, still gets a row stating the reason, and a page created by a REQ-<AREA>-<NNN> requirement cites it here.}}

| Page type | Indexable | Reason |
|---|---|---|
| {{Page type or path pattern}} | {{yes or no}} | {{Why}} |

<!-- mirage:section metadata -->
## Metadata

{{One paragraph: the pattern used to write a title and description for each page type, including the target search terms from the markets named above, and who reviews metadata before it ships.}}

<!-- mirage:section structured-data -->
## Structured data

{{One row per schema.org type the product marks up, such as Organization, Product or Article: which pages carry it and what data feeds it.}}

| Schema type | Pages | Data source |
|---|---|---|
| {{Schema.org type}} | {{Which pages carry it}} | {{Where the data comes from}} |

<!-- mirage:section sitemaps -->
## Sitemaps and robots

{{One paragraph: how the sitemap is generated and kept current, and which rules the robots file sets, citing the indexable pages table above for what it excludes.}}

<!-- mirage:section redirects -->
## Redirects

{{One row per old URL that must redirect: its destination and the redirect type. Record a missing list of existing URLs as an input in docs/inputs.md with ID IN-nnn.}}

| Old URL | Redirects to | Type |
|---|---|---|
| {{Old path}} | {{New path}} | {{301 or 302}} |

<!-- mirage:section social -->
## Social previews

{{One paragraph: how a shared link looks on social networks and messengers, naming the image, title and description source for each page type. Record search console access as an input in docs/inputs.md with ID IN-nnn if it does not exist yet.}}
