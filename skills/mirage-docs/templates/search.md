<!-- mirage:doc search -->
# Search

{{One paragraph: what search covers in this product, which requirement areas it serves, and that docs/questions.md holds every open decision about ranking, coverage or language support.}}

<!-- mirage:section scope -->
## Searchable content

{{Name every content type and entity a user can search for, and which fields on each are indexed. State what is deliberately excluded from search, such as draft or archived records, and cite the requirement (REQ-<AREA>-<NNN>) that scopes it. An unclear boundary becomes a question in docs/questions.md rather than a guess.}}

<!-- mirage:section engine -->
## Engine and index

{{Name the search engine or library the product uses and why it fits the expected scale and query pattern. State how the index is built, how often it refreshes and what triggers a rebuild. If no engine is chosen yet, record the choice as a question (Q-nnn) instead of naming one.}}

<!-- mirage:section ranking -->
## Ranking

{{State the factors that decide result order, such as text match, recency or popularity, and how they are weighted against each other. State how ties are broken. Treat any weight or boost value as a hypothesis until a release has measured it.}}

<!-- mirage:section filters -->
## Filters and facets

{{List the filters and facets offered alongside search results, what values populate each one, and whether facet counts must stay accurate as filters combine. State which filters are required at launch and which are later work, with scope tied to a requirement.}}

<!-- mirage:section languages -->
## Languages

{{Name every language search must handle and cite the requirement that sets that list. State how the product handles misspellings, partial words and mixed-language content. An unset language list becomes a question in docs/questions.md.}}

<!-- mirage:section zero-results -->
## Zero results

{{Describe what a user sees when a query returns nothing, such as a broadened query, spelling suggestions or a fallback listing. State whether zero-result queries are logged and who reviews them.}}

<!-- mirage:section scenarios -->
## Test scenarios

{{List the scenarios that prove search behaves as specified, including at least one misspelled query, one query in each supported language, one filter combination and one query with no results. Use the ID form <AREA>-T<NN> with the search requirement area code, counting up from 01, matching the scheme docs/test-strategy.md defines.}}

| ID | Scenario | Expected |
|---|---|---|
| {{AREA}}-T01 | {{The query and the content it runs against}} | {{The results and their order}} |
