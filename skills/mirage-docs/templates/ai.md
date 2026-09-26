<!-- mirage:doc ai -->
# AI features

{{One paragraph: which user-facing features use a model, what this document fixes, and that a person, not the model, remains accountable for the outcome. Say an unsettled provider, data source or safety threshold becomes a question in docs/questions.md rather than an invented one.}}

<!-- mirage:section use-cases -->
## Use cases

{{Describe each problem an AI feature solves for the owner's users, what a good answer looks like, and what a bad answer costs them. Cite the requirement each use case satisfies as REQ-<AREA>-NNN.}}

<!-- mirage:section models -->
## Models and providers

{{Name the model provider and model this feature calls, and any provider the project must not use, such as one that trains on customer data. State whether data may leave the owner's region, and cite the question that settled the provider choice as (Q-nnn) where one exists.}}

<!-- mirage:section grounding -->
## Grounding data

{{Name the data that grounds each feature's answers, such as a retrieval index or a fine-tuning set, where it comes from, and whether users consented to that use. State how the grounding data is kept current.}}

<!-- mirage:section evaluation -->
## Evaluation

{{State how quality is measured before a feature ships and after, such as a labeled evaluation set and a target accuracy, and who reviews a regression. Mark a target score as a hypothesis until it is measured against real traffic, and cite the input that supplies evaluation examples as (IN-nnn).}}

<!-- mirage:section safety -->
## Safety

{{List the harmful or abusive outputs this feature must prevent, such as leaking another user's data or producing unsafe content, and the control that prevents each one. State when a person reviews a result before it reaches a user.}}

<!-- mirage:section cost -->
## Cost and limits

{{State the expected cost per request and the monthly budget this feature may spend, marking both as a hypothesis until measured against real usage. State what happens as the feature approaches its budget, such as throttling or falling back to a cheaper model.}}

<!-- mirage:section fallback -->
## Fallback

{{State what a user sees when the model is slow, wrong or unavailable, and whether the feature degrades to a simpler non-AI path or fails visibly. Cite the requirement that sets this behavior as REQ-<AREA>-NNN.}}
