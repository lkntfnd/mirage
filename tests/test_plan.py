"""Every `when` form of the catalog, through the plan command."""

from __future__ import annotations

import json
import unittest

from support import catalog_doc, errors, facets, project, run, synthetic_catalog

CATALOG = synthetic_catalog(
    catalog_doc("base", "docs/base.md", "always"),
    catalog_doc("site", "docs/site.md", {"component": ["website", "desktop-app"]}),
    catalog_doc("ai", "docs/ai.md", {"flag": "ai"}),
    catalog_doc("rules", "docs/rules.md", {"nonempty": "regulated"}),
    catalog_doc("content", "docs/content.md", {"any": [{"component": ["website"]}, {"flag": "cms"}]}),
    catalog_doc("integration", "docs/integrations/{item}.md", {"per": "integrations"},
                areas=("auth", "limits"), inputs=(("sandbox", "account"),)),
    catalog_doc("platform", "docs/platforms/{kind}.md", {"per_component": ["mobile-app", "desktop-app"]}),
    catalog_doc("screen", "docs/specs/{component}/{name}.md", {"listed_in": "ux"}, "sections",
                sections=("purpose", "states")),
)


def plan_of(**overrides: object) -> list:
    with project({".mirage/project.json": facets(**overrides), ".mirage/catalog.json": CATALOG}) as root:
        code, out, err = run("plan", "--root", root, "--json")
    assert code == 0, err
    return [(d["key"], d["path"], d["reason"]) for d in json.loads(out)["docs"]]


BASE = ("base", "docs/base.md", "always")


class WhenForms(unittest.TestCase):
    maxDiff = None

    def test_always_plans_one_instance(self):
        self.assertEqual(plan_of(), [BASE])

    def test_component_matches_any_listed_kind(self):
        self.assertEqual(plan_of(components=[{"id": "shop", "kind": "website"}, {"id": "till", "kind": "desktop-app"}]), [
            BASE,
            ("site", "docs/site.md", "components include website, desktop-app"),
            ("content", "docs/content.md", "components include website"),
            ("platform:desktop-app", "docs/platforms/desktop-app.md", "components include desktop-app"),
        ])

    def test_flag_plans_only_when_true(self):
        self.assertEqual(plan_of(flags={"ai": True}), [BASE, ("ai", "docs/ai.md", "flag ai is true")])
        self.assertEqual(plan_of(flags={"ai": False}), [BASE])

    def test_nonempty_names_the_sorted_entries(self):
        self.assertEqual(plan_of(regulated=["pci-dss", "hipaa"]),
                         [BASE, ("rules", "docs/rules.md", "regulated includes hipaa, pci-dss")])
        self.assertEqual(plan_of(regulated=[]), [BASE])

    def test_any_plans_one_instance_with_every_matching_reason(self):
        self.assertEqual(plan_of(flags={"cms": True}), [BASE, ("content", "docs/content.md", "flag cms is true")])
        self.assertEqual(plan_of(components=[{"id": "shop", "kind": "website"}], flags={"cms": True}), [
            BASE,
            ("site", "docs/site.md", "components include website"),
            ("content", "docs/content.md", "components include website; flag cms is true"),
        ])

    def test_per_plans_one_instance_per_distinct_item(self):
        self.assertEqual(plan_of(integrations=["tile-maps", "billing-hub", "tile-maps"]), [
            BASE,
            ("integration:billing-hub", "docs/integrations/billing-hub.md", "integrations includes billing-hub"),
            ("integration:tile-maps", "docs/integrations/tile-maps.md", "integrations includes tile-maps"),
        ])

    def test_per_component_plans_one_instance_per_distinct_kind(self):
        components = [{"id": "phone", "kind": "mobile-app"}, {"id": "tablet", "kind": "mobile-app"},
                      {"id": "till", "kind": "desktop-app"}, {"id": "tool", "kind": "cli"}]
        self.assertEqual(plan_of(components=components), [
            BASE,
            ("site", "docs/site.md", "components include desktop-app"),
            ("platform:desktop-app", "docs/platforms/desktop-app.md", "components include desktop-app"),
            ("platform:mobile-app", "docs/platforms/mobile-app.md", "components include mobile-app"),
        ])

    def test_listed_in_is_not_planned_but_every_spec_file_is_checked(self):
        spec_ok = "<!-- mirage:doc screen -->\n# Home\n\n<!-- mirage:section purpose -->\n## Purpose\n\nx\n\n" \
                  "<!-- mirage:section states -->\n## States\n\ny\n"
        files = {
            ".mirage/project.json": facets(),
            ".mirage/catalog.json": CATALOG,
            "docs/base.md": "Base.\n",
            "docs/specs/app/home.md": spec_ok,
            "docs/specs/app/cart.md": spec_ok.replace("<!-- mirage:section states -->\n", ""),
        }
        with project(files) as root:
            self.assertEqual(json.loads(run("plan", "--root", root, "--json")[1])["docs"][0]["key"], "base")
            found = [(e["path"], e["code"], e["message"]) for e in errors(root, "--only", "docs")]
        self.assertEqual(found, [
            ("docs/specs/app/cart.md", "doc-section", "missing the section marker <!-- mirage:section states --> for States"),
        ])


class PlanOutput(unittest.TestCase):
    maxDiff = None

    FILES = {
        ".mirage/project.json": facets(integrations=["tile-maps"]),
        ".mirage/catalog.json": CATALOG,
        "docs/integrations/tile-maps.md": "Tile maps.\n",
        "docs/questions.md": "### Q-001 How does the map authenticate?\n\n- Status: open\n"
                             "- Covers: integration:tile-maps/auth\n- Recommendation: An API key.\n",
    }

    def test_json_carries_sections_areas_coverage_and_inputs(self):
        with project(self.FILES) as root:
            docs = json.loads(run("plan", "--root", root, "--json")[1])["docs"]
        self.assertEqual(docs[1], {
            "key": "integration:tile-maps",
            "id": "integration",
            "title": "Integration",
            "path": "docs/integrations/tile-maps.md",
            "reason": "integrations includes tile-maps",
            "exists": True,
            "sections": [],
            "areas": [
                {"key": "integration:tile-maps/auth", "ask": "What about auth?", "covered": True},
                {"key": "integration:tile-maps/limits", "ask": "What about limits?", "covered": False},
            ],
            "inputs": [{"key": "sandbox", "title": "Sandbox", "kind": "account"}],
        })
        self.assertEqual(docs[0]["exists"], False)

    def test_text_lists_each_instance(self):
        with project(self.FILES) as root:
            code, out, _ = run("plan", "--root", root)
        self.assertEqual((code, out), (0, (
            "base: Base\n"
            "  path: docs/base.md (missing)\n"
            "  reason: always\n"
            "\n"
            "integration:tile-maps: Integration\n"
            "  path: docs/integrations/tile-maps.md (exists)\n"
            "  reason: integrations includes tile-maps\n"
            "  area integration:tile-maps/auth: covered\n"
            "  area integration:tile-maps/limits: uncovered\n"
            "  input sandbox: Sandbox (account)\n"
        )))

    def test_vendored_catalog_wins_over_the_bundled_one(self):
        with project(self.FILES) as root:
            keys = [d["key"] for d in json.loads(run("plan", "--root", root, "--json")[1])["docs"]]
            (root / ".mirage" / "catalog.json").unlink()
            bundled = [d["key"] for d in json.loads(run("plan", "--root", root, "--json")[1])["docs"]]
        self.assertEqual(keys, ["base", "integration:tile-maps"])
        self.assertEqual(bundled[:4], ["glossary", "questions", "inputs", "index"])
        self.assertIn("cli", bundled)
        self.assertIn("integration:tile-maps", bundled)


if __name__ == "__main__":
    unittest.main()
