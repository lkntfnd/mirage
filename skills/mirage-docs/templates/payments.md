<!-- mirage:doc payments -->
# Payments

{{One paragraph: state that this document fixes how the product takes payments, which provider and methods it uses, how money is reconciled and refunded, and that every claim about the provider or the merchant account traces to an input or a question rather than an assumption.}}

<!-- mirage:section provider -->
## Provider

{{Name the payment provider and state who inside the project owns the merchant account with it. Do not invent a provider or an account number, since neither belongs in this document. Cite the input that grants the merchant account as IN-nnn and the input that grants sandbox access as IN-nnn. An unresolved provider choice becomes a question in docs/questions.md.}}

<!-- mirage:section flows -->
## Payment flows

{{List every payment flow the product needs, such as a one off charge, a subscription or a deposit held for later capture, and for each one state the steps from a person's action to a confirmed payment. Cite the requirement each flow satisfies as REQ-<AREA>-<NNN>. A flow the product defers becomes a requirement with scope OUT rather than a silent gap.}}

<!-- mirage:section currencies -->
## Currencies and taxes

{{State which currencies the product accepts, how prices are rounded, which taxes apply and who calculates them, such as the provider, a tax service or a manual table. Cite the input that supplies tax rules from an accountant as IN-nnn. An undecided currency or tax rule becomes a question in docs/questions.md rather than a guessed rate.}}

<!-- mirage:section idempotency -->
## Idempotency

{{State how the product avoids charging a person twice for the same action, such as an idempotency key sent with every charge request, and what happens when a confirmation is lost and the same action is retried. Cite the requirement this satisfies as REQ-<AREA>-<NNN>. State how the product tells a genuine retry apart from a second, separate purchase.}}

<!-- mirage:section refunds -->
## Refunds and disputes

{{State who may issue a refund, whether it can be partial, and the approval a large refund needs. State how the product responds to a dispute or chargeback raised with the provider, and who is notified. Cite the requirement each rule satisfies. An unresolved refund limit becomes a question in docs/questions.md instead of an invented number.}}

<!-- mirage:section reconciliation -->
## Reconciliation

{{State how the product matches each payment against an order and a provider payout, how often this runs, and what happens when an amount does not match. Mark any reconciliation frequency as a hypothesis until a release has run it. Cite the requirement this satisfies and record an unresolved matching rule as a question in docs/questions.md.}}

<!-- mirage:section compliance -->
## Card data scope

{{State that raw card numbers never reach the project's own servers, and name the approach that keeps it that way, such as a hosted field or a redirect the provider controls. Cite the input that grants the merchant account as IN-nnn. State what the project's own logs and database may store about a payment, such as a provider reference, and what they must never store.}}

<!-- mirage:section scenarios -->
## Test scenarios

{{List the scenarios that prove the payment flows work, including at least one failed payment, one retried payment and one refund. Use the ID form PAY-T<NN> counting up from 01, matching the scheme docs/test-strategy.md defines. Add a row for every scenario a payment requirement depends on before that requirement can reach done.}}

| ID | Scenario | Expected |
|---|---|---|
| PAY-T01 | {{The situation under test, in one sentence}} | {{What must happen}} |
