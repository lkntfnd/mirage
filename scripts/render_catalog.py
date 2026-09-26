"""Render skills/mirage/scripts/catalog.json into docs/catalog.md.

Run from the repository root: python3 scripts/render_catalog.py
tests/test_catalog_doc.py fails when docs/catalog.md is stale.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "skills" / "mirage" / "scripts" / "catalog.json"
OUT = ROOT / "docs" / "catalog.md"


def describe_when(when) -> str:
    if when == "always":
        return "always"
    if "component" in when:
        return "a component of kind " + ", ".join(when["component"])
    if "flag" in when:
        return f"flag `{when['flag']}`"
    if "nonempty" in when:
        return f"`{when['nonempty']}` is not empty"
    if "any" in when:
        return " or ".join(describe_when(w) for w in when["any"])
    if "per" in when:
        return f"one per entry in `{when['per']}`"
    if "per_component" in when:
        return "one per component kind among " + ", ".join(when["per_component"])
    if "listed_in" in when:
        return f"one per screen or page listed in `{when['listed_in']}`"
    raise ValueError(f"unknown when form: {when}")


def render(catalog: dict) -> str:
    lines = [
        "# Document catalog",
        "",
        "Generated from `skills/mirage/scripts/catalog.json` by `scripts/render_catalog.py`. Edit the JSON, then rerun the script.",
        "",
        f"The catalog holds {len(catalog['docs'])} document kinds, "
        f"{sum(len(d['areas']) for d in catalog['docs'])} question areas and "
        f"{sum(len(d['inputs']) for d in catalog['docs'])} typical inputs.",
        "",
        "## Facets",
        "",
        "- Component kinds: " + ", ".join(f"`{k}`" for k in catalog["component_kinds"]) + ".",
        "- Flags: " + ", ".join(f"`{k}`" for k in catalog["flags"]) + ".",
        "- Lists: " + ", ".join(f"`{k}`" for k in catalog["lists"]) + ".",
        "",
        "## Documents",
        "",
        "| Document | Path | Included when | Sections | Areas | Inputs |",
        "|---|---|---|---|---|---|",
    ]
    for d in catalog["docs"]:
        lines.append(
            f"| {d['title']} (`{d['id']}`) | `{d['path']}` | {describe_when(d['when'])} | "
            f"{len(d['sections'])} | {len(d['areas'])} | {len(d['inputs'])} |"
        )
    lines += ["", "## Question areas", ""]
    for d in catalog["docs"]:
        if not d["areas"]:
            continue
        lines += [f"### {d['title']} (`{d['id']}`)", ""]
        for a in d["areas"]:
            lines.append(f"- `{a['key']}`: {a['ask']}")
        if d["inputs"]:
            lines.append("")
            lines.append("Typical inputs: " + "; ".join(f"{i['title']} ({i['kind']})" for i in d["inputs"]) + ".")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUT.write_text(render(json.loads(CATALOG.read_text())))


if __name__ == "__main__":
    main()
