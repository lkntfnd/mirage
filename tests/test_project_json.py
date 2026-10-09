"""Components of any kind, `include` and project-defined documents in .mirage/project.json."""

from __future__ import annotations

import json
import unittest
from typing import List, Tuple

from support import catalog_doc, check, edit, edit_json, errors, facets, fixture_copy, project, run, synthetic_catalog

CATALOG = synthetic_catalog(
    catalog_doc("base", "docs/base.md", "always"),
    catalog_doc("ux", "docs/ux.md", {"component": ["website"]}),
    catalog_doc("ai", "docs/ai.md", {"flag": "ai"}),
    catalog_doc("integration", "docs/integrations/{item}.md", {"per": "integrations"}),
    catalog_doc("screen", "docs/specs/{component}/{name}.md", {"listed_in": "ux"}, "sections", sections=("purpose",)),
    catalog_doc("component", "docs/components/{item}.md", {"per_custom_component": True}),
)

BASE = ("base", "docs/base.md", "always")
DECLARES = "project.json declares it"
OPEN_Q012 = "open: Q-012 Which reminders does the app send? (blocks: M2-E01-S01, REQ-NOTE-001)\n"
TEA = {
    "id": "tea-sourcing",
    "title": "Tea sourcing",
    "sections": [{"key": "suppliers", "title": "Suppliers"}, {"key": "seasons", "title": "Seasons and stock"}],
    "areas": [
        {"key": "suppliers", "ask": "Which estates supply each tea?"},
        {"key": "seasons", "ask": "Which teas are seasonal?"},
    ],
}
TEA_PLANNED = ("tea-sourcing", "docs/tea-sourcing.md", DECLARES)
MENU = {**TEA, "id": "menu", "title": "Menu", "path": "docs/shop/menu.md"}
MENU_PLANNED = ("menu", "docs/shop/menu.md", DECLARES)


def uncovered(key: str, ask: str) -> Tuple[str, None, str, str]:
    return ("docs/questions.md", None, "coverage-area", f"no question covers {key}: {ask}")


def without(document: dict, key: str) -> dict:
    return {k: v for k, v in document.items() if k != key}


def load(**overrides: object) -> Tuple[List[str], List[Tuple[str, str, str]]]:
    """The project-json messages and the (key, path, reason) of every planned document."""
    files = {".mirage/project.json": facets(**overrides), ".mirage/catalog.json": CATALOG}
    with project(files) as root:
        messages = [e["message"] for e in errors(root, "--only", "project")]
        plan = json.loads(run("plan", "--root", root, "--json")[1])["docs"]
    return messages, [(d["key"], d["path"], d["reason"]) for d in plan]


class ComponentKinds(unittest.TestCase):
    maxDiff = None

    def test_a_custom_kind_is_accepted_and_planned_a_component_specification(self):
        components = [{"id": "tool", "kind": "cli"}, {"id": "kiosk", "kind": "shop-kiosk"}]
        self.assertEqual(load(components=components), ([], [
            BASE,
            ("component:kiosk", "docs/components/kiosk.md", "component kiosk has kind shop-kiosk, which has no document of its own"),
        ]))

    def test_a_kind_that_is_not_a_slug_is_reported_and_its_component_dropped(self):
        for kind in ("Shop Kiosk", "", "-kiosk", 7, None):
            with self.subTest(kind=kind):
                components = [{"id": "tool", "kind": "cli"}, {"id": "kiosk", "kind": kind}]
                self.assertEqual(load(components=components),
                                 (["component kiosk needs a kind that is a lowercase slug"], [BASE]))

    def test_a_component_with_no_kind_is_reported_and_dropped(self):
        components = [{"id": "tool", "kind": "cli"}, {"id": "kiosk"}]
        self.assertEqual(load(components=components),
                         (["component kiosk needs a kind that is a lowercase slug"], [BASE]))


class Include(unittest.TestCase):
    maxDiff = None

    def test_an_included_entry_is_planned_in_catalog_order_with_its_own_reason(self):
        self.assertEqual(load(include=["ai", "ux"]), ([], [
            BASE,
            ("ux", "docs/ux.md", "project.json includes it"),
            ("ai", "docs/ai.md", "project.json includes it"),
        ]))

    def test_an_included_entry_that_a_facet_requires_keeps_the_facets_reason_and_appears_once(self):
        components = [{"id": "shop", "kind": "website"}]
        self.assertEqual(load(components=components, flags={"ai": True}, include=["ux", "ai"]), ([], [
            BASE,
            ("ux", "docs/ux.md", "components include website"),
            ("ai", "docs/ai.md", "flag ai is true"),
        ]))

    def test_include_must_be_a_list_of_strings_and_is_dropped_otherwise(self):
        for value in ("ux", ["ux", 3], {"ux": True}, None):
            with self.subTest(value=value):
                self.assertEqual(load(include=value),
                                 (["include must be a list of catalog document IDs"], [BASE]))

    def test_an_entry_that_is_not_a_catalog_document_is_reported_and_dropped(self):
        self.assertEqual(load(include=["ux", "tea"]), (
            ["include entry 'tea' is not a catalog document"],
            [BASE, ("ux", "docs/ux.md", "project.json includes it")],
        ))

    def test_a_per_item_or_listed_entry_cannot_be_included_by_name(self):
        self.assertEqual(load(include=["integration", "screen", "component"]), ([
            "include entry 'component' is planned per item, so it cannot be included by name",
            "include entry 'integration' is planned per item, so it cannot be included by name",
            "include entry 'screen' is planned per item, so it cannot be included by name",
        ], [BASE]))


class ProjectDocumentsPlan(unittest.TestCase):
    maxDiff = None

    def test_documents_follow_every_catalog_entry_in_declared_order(self):
        components = [{"id": "shop", "kind": "website"}]
        self.assertEqual(load(components=components, integrations=["mapper"], documents=[TEA, MENU]), ([], [
            BASE,
            ("ux", "docs/ux.md", "components include website"),
            ("integration:mapper", "docs/integrations/mapper.md", "integrations includes mapper"),
            TEA_PLANNED,
            MENU_PLANNED,
        ]))

    def test_the_path_defaults_to_docs_and_the_id(self):
        self.assertEqual(load(documents=[TEA]), ([], [BASE, ("tea-sourcing", "docs/tea-sourcing.md", DECLARES)]))

    def test_a_declared_path_is_kept(self):
        self.assertEqual(load(documents=[MENU]), ([], [BASE, MENU_PLANNED]))


class ProjectDocumentProblems(unittest.TestCase):
    maxDiff = None

    def test_documents_must_be_a_list(self):
        for value in ({"id": "tea-sourcing"}, "tea-sourcing", None):
            with self.subTest(value=value):
                self.assertEqual(load(documents=value), (["documents must be a list"], [BASE]))

    def test_an_entry_must_be_an_object_with_a_slug_id(self):
        cases = (
            (["tea"], "documents[0]", [BASE]),
            ([TEA, {**TEA, "id": "Tea Sourcing"}], "documents[1]", [BASE, TEA_PLANNED]),
            ([without(TEA, "id")], "documents[0]", [BASE]),
            ([{**TEA, "id": 3}], "documents[0]", [BASE]),
        )
        for documents, where, planned in cases:
            with self.subTest(documents=documents):
                self.assertEqual(load(documents=documents), ([f"{where} needs an id that is a lowercase slug"], planned))

    def test_a_key_outside_the_table_is_reported_and_the_entry_dropped(self):
        self.assertEqual(load(documents=[{**TEA, "owner": "Mei", "extra": 1}]), ([
            "document tea-sourcing has unknown key extra",
            "document tea-sourcing has unknown key owner",
        ], [BASE]))

    def test_a_second_entry_with_the_same_id_is_reported_and_dropped(self):
        self.assertEqual(load(documents=[TEA, {**TEA, "path": "docs/tea-again.md"}]),
                         (["document tea-sourcing is declared twice"], [BASE, TEA_PLANNED]))

    def test_the_id_of_a_catalog_entry_is_reported_whether_or_not_it_is_planned(self):
        for doc_id in ("base", "ux"):
            with self.subTest(doc_id=doc_id):
                self.assertEqual(load(documents=[{**TEA, "id": doc_id}]),
                                 ([f"document {doc_id} is already a catalog document"], [BASE]))

    def test_a_title_is_required(self):
        for document in (without(TEA, "title"), {**TEA, "title": ""}, {**TEA, "title": "  "}, {**TEA, "title": 5}):
            with self.subTest(document=document):
                self.assertEqual(load(documents=[document]), (["document tea-sourcing needs a title"], [BASE]))

    def test_a_path_must_be_a_markdown_file_under_docs(self):
        paths = ("tea.md", "other/tea.md", "docs/tea.txt", "docs/tea", "docs/../tea.md", "docs/a/../tea.md",
                 "docs//tea.md", "docs/./tea.md", "docs/", "", 7)
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(
                    load(documents=[{**TEA, "path": path}]),
                    (["document tea-sourcing needs a path that is a Markdown file under docs/"], [BASE]),
                )

    def test_a_path_in_a_folder_read_as_something_else_is_refused(self):
        for path in ("docs/adr/0009-tea.md", "docs/sources/tea.md", "docs/specs/tea.md", "docs/specs/app/tea.md"):
            with self.subTest(path=path):
                self.assertEqual(
                    load(documents=[{**TEA, "path": path}]),
                    (["document tea-sourcing needs a path that is a Markdown file under docs/"], [BASE]),
                )

    def test_a_path_under_a_nested_folder_of_docs_is_accepted(self):
        self.assertEqual(load(documents=[{**TEA, "path": "docs/shop/tea.md"}]),
                         ([], [BASE, ("tea-sourcing", "docs/shop/tea.md", DECLARES)]))

    def test_a_path_that_a_planned_document_uses_is_reported(self):
        components = [{"id": "tool", "kind": "cli"}, {"id": "kiosk", "kind": "shop-kiosk"}]
        kiosk = ("component:kiosk", "docs/components/kiosk.md",
                 "component kiosk has kind shop-kiosk, which has no document of its own")
        mapper = ("integration:mapper", "docs/integrations/mapper.md", "integrations includes mapper")
        ai = ("ai", "docs/ai.md", "project.json includes it")
        cases = (
            ("tea-sourcing", "base", {"documents": [{**TEA, "path": "docs/base.md"}]}, [BASE]),
            ("tea-sourcing", "ai", {"documents": [{**TEA, "path": "docs/ai.md"}], "include": ["ai"]}, [BASE, ai]),
            ("tea-sourcing", "integration:mapper",
             {"documents": [{**TEA, "path": "docs/integrations/mapper.md"}], "integrations": ["mapper"]}, [BASE, mapper]),
            ("tea-sourcing", "component:kiosk",
             {"documents": [{**TEA, "path": "docs/components/kiosk.md"}], "components": components}, [BASE, kiosk]),
            ("menu", "tea-sourcing", {"documents": [TEA, {**MENU, "path": "docs/tea-sourcing.md"}]}, [BASE, TEA_PLANNED]),
        )
        for document, other, overrides, planned in cases:
            with self.subTest(other=other):
                self.assertEqual(load(**overrides), ([f"document {document} uses the path of {other}"], planned))

    def test_a_path_that_no_planned_document_uses_is_free(self):
        self.assertEqual(load(documents=[{**TEA, "path": "docs/ai.md"}]), ([], [BASE, ("tea-sourcing", "docs/ai.md", DECLARES)]))
        self.assertEqual(
            load(documents=[{**TEA, "title": ""}, {**MENU, "path": "docs/tea-sourcing.md"}]),
            (["document tea-sourcing needs a title"], [BASE, ("menu", "docs/tea-sourcing.md", DECLARES)]),
        )

    def test_sections_need_slug_keys_and_titles(self):
        sections = (None, [], "suppliers", ["suppliers"], [{"key": "Suppliers", "title": "Suppliers"}],
                    [{"key": "suppliers"}], [{"key": "suppliers", "title": ""}], [{"title": "Suppliers"}],
                    [TEA["sections"][0], {"key": "seasons", "title": 4}])
        for value in sections:
            with self.subTest(sections=value):
                document = without(TEA, "sections") if value is None else {**TEA, "sections": value}
                self.assertEqual(
                    load(documents=[document]),
                    (["document tea-sourcing needs sections, each with a slug key and a title"], [BASE]),
                )

    def test_areas_need_slug_keys_and_asks(self):
        areas = (None, [], "suppliers", ["suppliers"], [{"key": "Suppliers", "ask": "Which?"}],
                 [{"key": "suppliers"}], [{"key": "suppliers", "ask": " "}], [{"ask": "Which?"}],
                 [TEA["areas"][0], {"key": "seasons", "ask": 4}])
        for value in areas:
            with self.subTest(areas=value):
                document = without(TEA, "areas") if value is None else {**TEA, "areas": value}
                self.assertEqual(
                    load(documents=[document]),
                    (["document tea-sourcing needs areas, each with a slug key and an ask"], [BASE]),
                )

    def test_a_repeated_section_key_is_reported(self):
        sections = [{"key": "suppliers", "title": "Suppliers"}, {"key": "seasons", "title": "Seasons"},
                    {"key": "suppliers", "title": "Suppliers again"}]
        self.assertEqual(load(documents=[{**TEA, "sections": sections}]),
                         (["document tea-sourcing uses the section key suppliers twice"], [BASE]))

    def test_a_repeated_area_key_is_reported(self):
        areas = [{"key": "seasons", "ask": "When?"}, {"key": "seasons", "ask": "Which?"}, {"key": "seasons", "ask": "Why?"}]
        self.assertEqual(load(documents=[{**TEA, "areas": areas}]),
                         (["document tea-sourcing uses the area key seasons twice"], [BASE]))

    def test_every_problem_of_one_entry_is_reported_at_once(self):
        self.assertEqual(load(documents=[{"id": "tea-sourcing", "path": "tea.md"}]), ([
            "document tea-sourcing needs a path that is a Markdown file under docs/",
            "document tea-sourcing needs a title",
            "document tea-sourcing needs areas, each with a slug key and an ask",
            "document tea-sourcing needs sections, each with a slug key and a title",
        ], [BASE]))


class ProjectDocumentChecks(unittest.TestCase):
    """A project-defined document is checked as type sections, like any catalog document."""

    maxDiff = None

    FILLED = (
        "<!-- mirage:doc tea-sourcing -->\n# Tea sourcing\n\n"
        "<!-- mirage:section suppliers -->\n## Suppliers\n\nThree estates.\n\n"
        "<!-- mirage:section seasons -->\n## Seasons and stock\n\nSpring and autumn flushes.\n"
    )

    def found(self, files: dict, *only: str) -> list:
        base = {".mirage/project.json": facets(documents=[TEA]), ".mirage/catalog.json": CATALOG, "docs/base.md": "Base.\n"}
        with project({**base, **files}) as root:
            return [(e["path"], e["code"], e["message"]) for e in errors(root, "--only", *only)]

    def test_a_filled_document_passes(self):
        self.assertEqual(self.found({"docs/tea-sourcing.md": self.FILLED}, "docs"), [])

    def test_a_missing_file_is_doc_missing(self):
        self.assertEqual(self.found({}, "docs"), [(
            "docs/tea-sourcing.md", "doc-missing",
            "Tea sourcing (tea-sourcing) is missing; it is planned because project.json declares it",
        )])

    def test_a_missing_doc_marker_is_doc_marker(self):
        text = self.FILLED.replace("<!-- mirage:doc tea-sourcing -->\n", "")
        self.assertEqual(self.found({"docs/tea-sourcing.md": text}, "docs"), [
            ("docs/tea-sourcing.md", "doc-marker", "missing the doc marker <!-- mirage:doc tea-sourcing -->"),
        ])

    def test_a_missing_section_marker_is_doc_section(self):
        text = self.FILLED.replace("<!-- mirage:section seasons -->\n", "")
        self.assertEqual(self.found({"docs/tea-sourcing.md": text}, "docs"), [(
            "docs/tea-sourcing.md", "doc-section",
            "missing the section marker <!-- mirage:section seasons --> for Seasons and stock",
        )])

    def test_an_area_no_question_covers_is_coverage_area(self):
        self.assertEqual(self.found({}, "coverage"), [
            ("docs/questions.md", "coverage-area", "no question covers tea-sourcing/seasons: Which teas are seasonal?"),
            ("docs/questions.md", "coverage-area", "no question covers tea-sourcing/suppliers: Which estates supply each tea?"),
        ])
        question = "### Q-001 Who supplies the tea?\n\n- Status: open\n- Covers: tea-sourcing/suppliers\n- Recommendation: Three estates.\n"
        self.assertEqual(self.found({"docs/questions.md": question}, "coverage"), [
            ("docs/questions.md", "coverage-area", "no question covers tea-sourcing/seasons: Which teas are seasonal?"),
        ])

    def test_the_plan_entry_carries_the_sections_and_areas(self):
        question = "### Q-001 Who supplies the tea?\n\n- Status: open\n- Covers: tea-sourcing/suppliers\n- Recommendation: Three estates.\n"
        files = {".mirage/project.json": facets(documents=[TEA]), ".mirage/catalog.json": CATALOG,
                 "docs/tea-sourcing.md": self.FILLED, "docs/questions.md": question}
        with project(files) as root:
            docs = json.loads(run("plan", "--root", root, "--json")[1])["docs"]
        self.assertEqual(docs[-1], {
            "key": "tea-sourcing",
            "id": "tea-sourcing",
            "title": "Tea sourcing",
            "path": "docs/tea-sourcing.md",
            "reason": "project.json declares it",
            "exists": True,
            "sections": [{"key": "suppliers", "title": "Suppliers"}, {"key": "seasons", "title": "Seasons and stock"}],
            "areas": [
                {"key": "tea-sourcing/suppliers", "ask": "Which estates supply each tea?", "covered": True},
                {"key": "tea-sourcing/seasons", "ask": "Which teas are seasonal?", "covered": False},
            ],
            "inputs": [],
        })


class AnyKindProject(unittest.TestCase):
    """The valid fixture grows a part of a custom kind, an included catalog document and a document of its own."""

    maxDiff = None

    GROWTH = {
        "components": [
            {"id": "app", "kind": "mobile-app"},
            {"id": "api", "kind": "backend-service"},
            {"id": "wall-display", "kind": "shop-display"},
        ],
        "include": ["formats"],
        "documents": [{
            "id": "workshop-stock",
            "title": "Workshop stock",
            "sections": [{"key": "bins", "title": "Bins and shelves"}, {"key": "counts", "title": "Counting"}],
            "areas": [
                {"key": "bins", "ask": "How the workshop labels bins and where each part lives."},
                {"key": "counts", "ask": "When the stock is counted, and who corrects a wrong number."},
            ],
        }],
    }

    def test_the_new_parts_are_reported_until_they_are_written_and_covered(self):
        with fixture_copy() as root:
            edit_json(".mirage/project.json", lambda data: data.update(self.GROWTH))(root)
            found = [(e["path"], e["line"], e["code"], e["message"]) for e in errors(root)]
            self.assertTrue(run("docs-ready", "--root", root)[1].endswith("not sufficient: 18 problems\n" + OPEN_Q012))
            self.assertEqual(found, [
                ("docs/README.md", 29, "index-stale", "the generated file differs from what index writes; run index"),
                ("docs/components/wall-display.md", None, "doc-missing",
                 "Component specification (component:wall-display) is missing; "
                 "it is planned because component wall-display has kind shop-display, which has no document of its own"),
                ("docs/formats.md", None, "doc-missing",
                 "File and data formats (formats) is missing; it is planned because project.json includes it"),
                uncovered("component:wall-display/build", "How it is produced from its sources, and with which tools."),
                uncovered("component:wall-display/delivery",
                          "How it is packaged, versioned and delivered to the people or systems that use it."),
                uncovered("component:wall-display/environment",
                          "Where it runs or exists: the platforms, hardware, materials, standards and versions it must "
                          "work with, and the limits they impose."),
                uncovered("component:wall-display/interfaces",
                          "What goes into it and comes out of it, such as data, files, signals, commands or physical "
                          "connections, and what sits on the other side of each."),
                uncovered("component:wall-display/purpose",
                          "What this part is for, who or what uses it, and what it deliberately does not do."),
                uncovered("component:wall-display/quality",
                          "Which measurable targets it must meet, such as speed, accuracy, reliability, tolerance or cost."),
                uncovered("component:wall-display/risks",
                          "What is most likely to go wrong or is least understood, and how that will be found out early."),
                uncovered("component:wall-display/structure",
                          "Which main parts it has inside, what state or data it holds, and which design decisions are already fixed."),
                uncovered("component:wall-display/verification",
                          "How someone proves it works, and what that takes: equipment, test data, environments or other people."),
                uncovered("formats/formats", "Which files or payloads the product reads and writes, and who else consumes them."),
                uncovered("formats/schema", "Which fields each format has, with types and which are required."),
                uncovered("formats/validation", "What happens when an input is malformed or carries unknown fields."),
                uncovered("formats/versioning", "How a format changes without breaking files that already exist."),
                uncovered("workshop-stock/bins", "How the workshop labels bins and where each part lives."),
                uncovered("workshop-stock/counts", "When the stock is counted, and who corrects a wrong number."),
                ("docs/workshop-stock.md", None, "doc-missing",
                 "Workshop stock (workshop-stock) is missing; it is planned because project.json declares it"),
            ])

    def test_the_project_is_ok_once_the_files_exist_and_the_questions_cover_the_areas(self):
        with fixture_copy() as root:
            edit_json(".mirage/project.json", lambda data: data.update(self.GROWTH))(root)
            entries = check.plan_entries(check.load_project(root))
            new = [entry for entry in entries if not entry["exists"] and entry["key"] != "index"]
            self.assertEqual([entry["key"] for entry in new], ["formats", "component:wall-display", "workshop-stock"])
            for entry in new:
                lines = [f"<!-- mirage:doc {entry['key']} -->", f"# {entry['title']}", ""]
                for section in entry["sections"]:
                    lines += [f"<!-- mirage:section {section['key']} -->", f"## {section['title']}", "", "Written down.", ""]
                (root / entry["path"]).parent.mkdir(parents=True, exist_ok=True)
                (root / entry["path"]).write_text("\n".join(lines), encoding="utf-8")
            covers = ", ".join(area["key"] for entry in new for area in entry["areas"])
            edit("docs/questions.md", "- Covers: delivery/done, ", f"- Covers: {covers}, delivery/done, ")(root)
            self.assertEqual(run("index", "--root", root)[0], 0)
            self.assertEqual(run("check", "--root", root), (0, "ok\n", ""))
            self.assertEqual(run("docs-ready", "--root", root), (0, "sufficient\n" + OPEN_Q012, ""))


if __name__ == "__main__":
    unittest.main()
