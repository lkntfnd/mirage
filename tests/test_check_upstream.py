import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_upstream.py"


def make_upstream(root: Path, grilling_frontmatter: str = "name: grilling") -> None:
    skills = {
        "grilling": ("skills/productivity/grilling", grilling_frontmatter),
        "domain-modeling": ("skills/engineering/domain-modeling", "name: domain-modeling"),
        "to-questionnaire": ("skills/productivity/to-questionnaire",
                             "name: to-questionnaire\ndisable-model-invocation: true"),
    }
    for folder, fm in skills.values():
        (root / folder).mkdir(parents=True)
        (root / folder / "SKILL.md").write_text(f"---\n{fm}\ndescription: x\n---\n\nbody\n")
    dm = root / "skills/engineering/domain-modeling"
    (dm / "ADR-FORMAT.md").write_text("ADRs live in `docs/adr/` as `0001-slug.md`.\n")
    (dm / "CONTEXT-FORMAT.md").write_text("format\n")
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps(
        {"name": "mattpocock-skills", "skills": ["./" + f for f, _ in skills.values()]}))


def run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), str(root)], capture_output=True, text=True)


class CheckUpstreamTest(unittest.TestCase):
    def test_intact_upstream_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_upstream(Path(tmp))
            result = run(Path(tmp))
        self.assertEqual((result.returncode, result.stdout), (0, "ok\n"))

    def test_user_only_grilling_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_upstream(Path(tmp), "name: grilling\ndisable-model-invocation: true")
            result = run(Path(tmp))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "grilling: is now user-invoked only, so mirage skills cannot call it\n")

    def test_moved_adr_format_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_upstream(Path(tmp))
            (Path(tmp) / "skills/engineering/domain-modeling/ADR-FORMAT.md").unlink()
            result = run(Path(tmp))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "domain-modeling: ADR-FORMAT.md is missing\n")


if __name__ == "__main__":
    unittest.main()
