<!-- mirage:doc public-api -->
# Public API

{{One paragraph: which library this document covers, who consumes it, and what this document fixes. Say an unsettled export, version policy or platform target becomes a question in docs/questions.md rather than an invented one.}}

<!-- mirage:section audience -->
## Audience

{{Describe who uses this library and in which kinds of projects, and what those consumers already assume about its behavior. Cite the requirement that names the audience as REQ-<AREA>-NNN.}}

<!-- mirage:section exports -->
## Exports

{{List the functions, types and modules the library exposes as public, grouped by the module they live in. State which parts are internal and must not be imported even though the language allows it.}}

<!-- mirage:section versioning -->
## Versioning

{{State the versioning scheme, such as semantic versioning, and give a concrete example of what counts as a major, minor and patch change for this library. State who decides a version bump.}}

<!-- mirage:section compatibility -->
## Compatibility

{{List the language, runtime and platform versions the library supports, and the oldest version it still tests against. State the policy for dropping support for an old version.}}

<!-- mirage:section deprecation -->
## Deprecation

{{State how a deprecated export is marked, how long it keeps working after the warning appears, and where the migration path is documented. Cite the question that settled the deprecation window as (Q-nnn) where one exists.}}

<!-- mirage:section distribution -->
## Distribution

{{Name the registry that publishes the library, who holds publish rights, and how the reference documentation is generated and hosted. State what blocks a publish, such as a failing contract test.}}
