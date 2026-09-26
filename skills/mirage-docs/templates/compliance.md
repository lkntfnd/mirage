<!-- mirage:doc compliance -->
# Compliance

{{One paragraph: which regulations or standards this product must satisfy, and who is accountable for compliance.
State that docs/questions.md holds every open decision about certification scope or timing.}}

<!-- mirage:section regimes -->
## Regimes

{{Name every regulation or standard that applies, such as HIPAA, PCI DSS or SOC 2.
State why each one applies to this product, such as the data it holds or the market it sells into.
An unconfirmed regime becomes a question in docs/questions.md rather than an assumed one.}}

<!-- mirage:section obligations -->
## Obligations

{{List the concrete obligations each regime in the regimes section imposes on this product, one group per regime.
State which requirement (REQ-<AREA>-<NNN>) implements each obligation.
State which audits or certifications are needed, and by when, treating any date as a hypothesis until the owner confirms it.}}

<!-- mirage:section controls -->
## Controls mapping

{{Map each obligation to the control that satisfies it, such as encryption at rest, access logging or a retention policy.
Name who owns that control.
A row with no owner yet is a question in docs/questions.md.}}

| Obligation | Control | Owner | Status |
|---|---|---|---|
| {{Obligation from the section above}} | {{What is implemented}} | {{Role or team}} | {{Planned, in place or verified}} |

<!-- mirage:section evidence -->
## Evidence

{{State what evidence each obligation needs, such as a policy document, a signed attestation or an audit report.
State where each piece of evidence is kept and who can produce it on request.
State that a claim of compliance without stored evidence does not count as met.}}
