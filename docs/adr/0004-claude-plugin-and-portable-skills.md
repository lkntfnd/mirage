---
status: accepted
---

# Ship as a Claude Code marketplace plugin and as portable Agent Skills

Claude Code users install mirage from its marketplace, which also installs the dependency. Codex and other agents install the same `skills/` folders with `npx skills add`. Each skill keeps its frontmatter to the portable keys and carries an `agents/openai.yaml` beside `SKILL.md`, and the generated project docs are agent-neutral, with `AGENTS.md` canonical and `CLAUDE.md` importing it.

## Consequences

- The one Claude-only key is `disable-model-invocation: true` on the `/mirage` entry point, which keeps its description out of every session's context. Its `agents/openai.yaml` sets `allow_implicit_invocation: false` for the same effect in Codex. Strict portable validators flag the key, and that is accepted.

Decided by the owner on 2026-09-26.
