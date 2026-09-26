import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import render_catalog  # noqa: E402


class CatalogDocTest(unittest.TestCase):
    def test_catalog_md_is_current(self):
        catalog = json.loads(render_catalog.CATALOG.read_text())
        expected = render_catalog.render(catalog)
        self.assertEqual(
            (ROOT / "docs" / "catalog.md").read_text(),
            expected,
            "docs/catalog.md is stale; run python3 scripts/render_catalog.py",
        )


if __name__ == "__main__":
    unittest.main()
