<!-- mirage:doc integration:{{item}} -->
# Integration: {{Name}}

{{One paragraph: name the external system this file covers and state that this document is written once for every entry in the project's integrations list. State which requirements depend on this integration and that an unresolved detail about the system becomes a question in docs/questions.md rather than a guess.}}

<!-- mirage:section purpose -->
## Purpose and requirements

{{State what this integration is for in one or two sentences and list every requirement that depends on it, cited as REQ-<AREA>-<NNN>. State which way data flows between the product and the system, and whether that flow runs in real time or on a schedule.}}

<!-- mirage:section contract -->
## Contract

{{Describe the calls or events this integration relies on, such as the requests it sends and the responses or webhooks it expects. Cite the input that supplies the system's own API documentation as IN-nnn. State the version of the system's interface this document assumes.}}

<!-- mirage:section auth -->
## Authentication

{{State how the product authenticates with this system, such as an API key, an OAuth flow or a signed request, and who inside the project owns the credential. Never write the credential value itself here. Cite the input that grants access as IN-nnn.}}

<!-- mirage:section limits -->
## Limits and quotas

{{State the rate limits, quotas and costs this system imposes, and what the product does when it approaches or exceeds one, such as queuing or backing off. Mark any numeric limit as a hypothesis until the system's own documentation or a real run confirms it.}}

<!-- mirage:section mapping -->
## Data mapping

{{State how each field or object this system returns maps onto the product's own data, and what happens to a field the system adds that the product does not yet expect. Cite the requirement this mapping satisfies as REQ-<AREA>-<NNN>. An undecided mapping becomes a question in docs/questions.md.}}

<!-- mirage:section failures -->
## Failure handling

{{State what the product does when this system is slow, unavailable or returns a bad response, such as a retry with backoff, a cached fallback or a visible error to the person waiting on it. State whether a sandbox or test environment exists for rehearsing these failures, citing the input that grants it as IN-nnn.}}

<!-- mirage:section scenarios -->
## Test scenarios

{{List the scenarios that prove this integration works, including at least one failure case such as a timeout or an error response. Use the ID form <AREA>-T<NN> counting up from 01, where AREA is the requirement area this integration serves most, matching the scheme docs/test-strategy.md defines. An integration that mainly serves payments, for example, would use the area code PAY, as in PAY-T01.}}

| ID | Scenario | Expected |
|---|---|---|
| {{AREA}}-T01 | {{The situation under test, in one sentence}} | {{What must happen}} |
