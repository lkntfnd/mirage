<!-- mirage:doc performance -->
# Performance

{{One paragraph: which user-facing moments must feel fast, such as page load, app start or an API response, and what this document fixes about proving they do. Say that every target below is a hypothesis until a measurement confirms it, and that an unresolved target becomes a question in docs/questions.md as (Q-nnn) rather than an invented number.}}

<!-- mirage:section budgets -->
## Budgets

{{One row per speed target. Name the device and network condition it must hold under, drawn from the product's real user base rather than an ideal case, and cite the REQ-<AREA>-<NNN> requirement it protects where one exists. Mark each row's status hypothesis until a measurement moves it to measured.}}

| Metric | Target | Condition | Status |
|---|---|---|---|
| {{Such as largest contentful paint}} | {{Number with unit}} | {{Device and network}} | {{hypothesis or measured}} |

<!-- mirage:section measurement -->
## Measurement

{{One paragraph: how and where each budget above is measured, such as a lab tool run in CI or a real-user monitoring service, and how often it runs. Name the peak load the system must serve, marking the number a hypothesis until real traffic confirms it.}}

<!-- mirage:section techniques -->
## Techniques

{{One row per technique the product relies on to hit its budgets, such as caching, lazy loading or a content delivery network. Name the budget row each technique protects and the component from docs/architecture.md it applies to.}}

| Technique | Protects | Component |
|---|---|---|
| {{Technique name}} | {{Budget row from above}} | {{Component id from docs/architecture.md}} |

<!-- mirage:section monitoring -->
## Monitoring

{{One paragraph: which dashboard or alert watches each budget in production, who receives an alert when a budget is missed, and what happens next. Cite docs/operations.md's observability section for the tool this reuses.}}
