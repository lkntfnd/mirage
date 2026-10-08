"""Check that a mattpocock/skills checkout still provides what mirage relies on.

Usage: python3 scripts/check_upstream.py <path to a mattpocock/skills checkout>

Mirage cannot pin a version of mattpocock-skills (see docs/adr/0002), so this
check runs weekly in CI against upstream and fails when a skill mirage calls
moves, is renamed, or stops being callable by the model.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED = {
    "grilling": {"model_invocable": True},
    "domain-modeling": {"model_invocable": True, "files": ["ADR-FORMAT.md", "GLOSSARY-FORMAT.md"]},
    "to-questionnaire": {"model_invocable": False},
}


def frontmatter(text: str) -> dict:
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    failures: list[str] = []

    manifest = json.loads((root / ".claude-plugin" / "plugin.json").read_text())
    if manifest.get("name") != "mattpocock-skills":
        failures.append(f"plugin name is {manifest.get('name')!r}, expected 'mattpocock-skills'")
    listed = {Path(p).name: root / p for p in manifest.get("skills", [])}

    for name, needs in REQUIRED.items():
        folder = listed.get(name)
        if folder is None:
            failures.append(f"{name} is not listed in .claude-plugin/plugin.json")
            continue
        skill = folder / "SKILL.md"
        if not skill.is_file():
            failures.append(f"{name}: {skill.relative_to(root)} is missing")
            continue
        fields = frontmatter(skill.read_text())
        if fields.get("name") != name:
            failures.append(f"{name}: frontmatter name is {fields.get('name')!r}")
        user_only = fields.get("disable-model-invocation") == "true"
        if needs["model_invocable"] and user_only:
            failures.append(f"{name}: is now user-invoked only, so mirage skills cannot call it")
        for extra in needs.get("files", []):
            if not (folder / extra).is_file():
                failures.append(f"{name}: {extra} is missing")

    adr_format = listed.get("domain-modeling")
    if adr_format and (adr_format / "ADR-FORMAT.md").is_file():
        text = (adr_format / "ADR-FORMAT.md").read_text()
        if "docs/adr/" not in text or "0001-slug.md" not in text:
            failures.append("domain-modeling: ADR-FORMAT.md no longer names docs/adr/NNNN-slug.md")

    if adr_format and (adr_format / "SKILL.md").is_file() and "GLOSSARY.md" not in (adr_format / "SKILL.md").read_text():
        failures.append("domain-modeling: SKILL.md no longer names GLOSSARY.md, the file mirage plans as the glossary")

    if failures:
        print("\n".join(failures))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
