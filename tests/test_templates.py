from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = REPO_ROOT / "skills" / "mirage" / "scripts" / "catalog.json"
TEMPLATES_DIR = REPO_ROOT / "skills" / "mirage-docs" / "templates"

with open(CATALOG_PATH, encoding="utf-8") as f:
    CATALOG = json.load(f)

SECTIONS_DOCS = [doc for doc in CATALOG["docs"] if doc["check"] == "sections"]

DOC_MARKER_RE = re.compile(r"<!-- mirage:doc [^\n]*-->")
PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}")
# The shapes the validator's refs group resolves. Standard wording that holds one
# would fail `check` in every project that copies the template.
ID_RE = re.compile(r"\b(?:M\d+-E\d+-S\d+(?:-T\d+)?|REQ-[A-Z]+-\d{3}|Q-\d{3}|IN-\d{3}|ADR-\d{4})\b")
SECTION_MARKER_RE = re.compile(r"<!-- mirage:section (\S+) -->")


def strip_fenced_code(lines: list[str]) -> list[str]:
    """Blank out the interior of fenced code blocks, keeping line count and order."""
    out = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        out.append("" if in_fence else line)
    return out


def expected_doc_marker(doc: dict) -> str:
    doc_id = doc["id"]
    if doc_id == "screen":
        return "<!-- mirage:doc screen -->"
    when = doc.get("when")
    if isinstance(when, dict) and ("per" in when or "per_custom_component" in when):
        return "<!-- mirage:doc " + doc_id + ":{{item}} -->"
    if isinstance(when, dict) and "per_component" in when:
        return "<!-- mirage:doc " + doc_id + ":{{kind}} -->"
    return "<!-- mirage:doc " + doc_id + " -->"


class TestTemplates(unittest.TestCase):
    """One generated test per catalog doc whose check is 'sections'."""


def make_test(doc: dict):
    def test(self):
        path = TEMPLATES_DIR / f"{doc['id']}.md"
        self.assertTrue(path.exists(), f"missing template: {path}")
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        clean_lines = strip_fenced_code(lines)
        clean_text = "\n".join(clean_lines)

        doc_markers = DOC_MARKER_RE.findall(clean_text)
        self.assertEqual(
            len(doc_markers), 1,
            f"{doc['id']}: expected exactly one doc marker line, found {doc_markers}",
        )
        self.assertEqual(
            doc_markers[0], expected_doc_marker(doc),
            f"{doc['id']}: doc marker does not match the expected form",
        )

        section_keys = [m.group(1) for m in SECTION_MARKER_RE.finditer(clean_text)]
        expected_keys = [s["key"] for s in doc["sections"]]
        self.assertEqual(
            section_keys, expected_keys,
            f"{doc['id']}: section markers must appear in exactly the catalog order and set",
        )

        section_titles = {s["key"]: s["title"] for s in doc["sections"]}
        for i, line in enumerate(clean_lines):
            m = SECTION_MARKER_RE.match(line.strip())
            if not m:
                continue
            key = m.group(1)
            expected_heading = "## " + section_titles[key]
            heading_line = None
            if i + 1 < len(clean_lines) and clean_lines[i + 1].strip() == "":
                if i + 2 < len(clean_lines):
                    heading_line = clean_lines[i + 2]
            elif i + 1 < len(clean_lines):
                heading_line = clean_lines[i + 1]
            self.assertIsNotNone(
                heading_line, f"{doc['id']}/{key}: no heading follows the section marker"
            )
            self.assertEqual(
                heading_line.rstrip(), expected_heading,
                f"{doc['id']}/{key}: heading must match the catalog title verbatim",
            )

        h1_lines = [line for line in clean_lines if line.startswith("# ")]
        self.assertEqual(
            len(h1_lines), 1, f"{doc['id']}: expected exactly one H1, found {h1_lines}"
        )

        standard_wording = PLACEHOLDER_RE.sub("", clean_text)
        self.assertEqual(
            ID_RE.findall(standard_wording), [],
            f"{doc['id']}: standard wording holds an ID that no project will have; write a pattern such as M<n>-E<nn>-S<nn>",
        )

        self.assertIn(
            "{{", clean_text,
            f"{doc['id']}: template has no unfenced {{ placeholder, so an unfilled copy would pass the validator",
        )

    return test


for _doc in SECTIONS_DOCS:
    setattr(TestTemplates, f"test_{_doc['id'].replace('-', '_')}_template", make_test(_doc))


if __name__ == "__main__":
    unittest.main()
