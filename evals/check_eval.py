"""Grade one mirage evaluation run.

Usage: python3 evals/check_eval.py <eval name> <project dir>

The project dir is where an agent ran mirage on evals/<eval name>/brief.md.
Exits 1 when any criterion fails.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

EVALS = Path(__file__).resolve().parent
DATE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
MONEY = re.compile(r"(?:[$€£]\s?\d[\d,.]*)|(?:\b\d[\d,.]*\s?(?:EUR|USD|GBP)\b)")
SECTION = re.compile(r"<!-- mirage:section ([a-z0-9-]+) -->")
# Worked examples and test scenarios hold sample data, not project facts.
SAMPLE_SECTIONS = {"examples", "scenarios"}


def factual_text(text: str) -> str:
    kept, current = [], None
    for line in text.splitlines():
        marker = SECTION.search(line)
        if marker:
            current = marker.group(1)
        if current not in SAMPLE_SECTIONS:
            kept.append(line)
    return "\n".join(kept)


def run(project: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(project / ".mirage" / "check.py"), *args, "--root", str(project)],
        capture_output=True, text=True,
    )


def main() -> int:
    name, project = sys.argv[1], Path(sys.argv[2]).resolve()
    expected = json.loads((EVALS / name / "expected.json").read_text())
    brief = (EVALS / name / "brief.md").read_text()
    failures: list[str] = []

    result = run(project, "check")
    if result.returncode != 0:
        failures.append("check is not clean:\n" + result.stdout.strip())

    plan = json.loads(run(project, "plan", "--json").stdout)
    keys = {d["key"] for d in plan["docs"]}
    for d in plan["docs"]:
        if not d["exists"]:
            failures.append(f"planned document missing: {d['path']}")
        for a in d["areas"]:
            if not a["covered"]:
                failures.append(f"area not covered: {a['key']}")

    facets = json.loads((project / ".mirage" / "project.json").read_text())
    kinds = sorted(c["kind"] for c in facets["components"])
    if kinds != sorted(expected["components"]):
        failures.append(f"component kinds {kinds} != expected {sorted(expected['components'])}")
    true_flags = {k for k, v in facets.get("flags", {}).items() if v}
    for flag in expected["flags_true"]:
        if flag not in true_flags:
            failures.append(f"flag expected true: {flag}")
    for item in expected["integrations_include"]:
        if item not in facets.get("integrations", []):
            failures.append(f"integration expected: {item}")
    for key in expected["docs_include"]:
        if key not in keys:
            failures.append(f"document expected in plan: {key}")

    allowed = brief
    for register in ("docs/questions.md", "docs/inputs.md"):
        path = project / register
        if path.exists():
            allowed += path.read_text()
    scanned = [p for p in (project / "docs").rglob("*.md")
               if p.relative_to(project).as_posix() not in ("docs/questions.md", "docs/inputs.md")
               and "sources" not in p.relative_to(project).parts]
    scanned += list((project / "backlog").glob("*.md")) + [project / "AGENTS.md"]
    for path in scanned:
        if not path.exists():
            continue
        text = factual_text(path.read_text())
        for pattern, label in ((DATE, "date"), (MONEY, "amount")):
            for match in sorted(set(pattern.findall(text))):
                if match not in allowed:
                    failures.append(f"unsourced {label} {match!r} in {path.relative_to(project)}")

    if failures:
        print("\n".join(failures))
        print(f"FAIL: {len(failures)} problems")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
