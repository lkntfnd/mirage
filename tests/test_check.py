"""The valid fixture, one mutation per diagnostic code, and the command-line surface."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from support import (
    FIXTURE, SCRIPT, Mutation, append, check, delete, edit, edit_json, errors, fixture_copy, run, write,
)


@dataclass(frozen=True)
class Case:
    code: str
    mutation: Mutation
    expect: Tuple[Tuple[str, Optional[int], str], ...]
    reindex: bool = True


FAKE_AWS_KEY = "AKIA" + "Q" * 16
NEW_STORY = """---
id: M3-E01-S01
title: Loyalty card
status: draft
priority: low
scope: may
release: v1.1
labels: [area:mobile]
---

A stamp card for repeat customers.
"""

# Each case applies one defect to a copy of the fixture. Unless reindex is off, the generated
# index files are then rewritten, as a user would, so that only the defect itself is reported.
CASES = (
    Case("project-json", edit_json(".mirage/project.json", lambda d: d["flags"].update(telepathy=True)),
         ((".mirage/project.json", None, "unknown flag telepathy"),)),
    Case("doc-missing", delete("docs/performance.md"),
         (("docs/performance.md", None,
           "Performance (performance) is missing; it is planned because components include mobile-app, backend-service"),)),
    Case("doc-marker", edit("docs/security.md", "<!-- mirage:doc security -->\n", ""),
         (("docs/security.md", None, "missing the doc marker <!-- mirage:doc security -->"),)),
    Case("doc-section", edit("docs/security.md", "<!-- mirage:section threats -->\n", ""),
         (("docs/security.md", None, "missing the section marker <!-- mirage:section threats --> for Threats"),)),
    Case("doc-placeholder", append("docs/security.md", "Escalation contact: {{contact}}\n"),
         (("docs/security.md", 33, "the line holds a {{ placeholder; write the content or cite a question"),)),
    Case("claude-import", write("CLAUDE.md", "Read AGENTS.md first.\n"),
         (("CLAUDE.md", None, "CLAUDE.md has no line that is exactly @AGENTS.md"),)),
    Case("adr-duplicate", write("docs/adr/0001-zz-second-api.md", "A second decision with a reused number.\n"),
         (("docs/adr/0001-zz-second-api.md", None, "ADR number 0001 is already used by docs/adr/0001-one-booking-api.md"),)),
    Case("index-stale", append("backlog/README.md", "Hand-edited note.\n"),
         (("backlog/README.md", 37, "the generated file differs from what index writes; run index"),), reindex=False),
    Case("register-parse", edit("docs/questions.md", "- Recommendation: One API", "- Hosting is undecided\n- Recommendation: One API"),
         (("docs/questions.md", 16, "a field line must read `- Key: value` with Key one of: Status, Covers, Blocks, Recommendation, Answer, Owner, Questionnaire"),)),
    Case("register-duplicate",
         append("docs/questions.md", "\n### Q-004 How is the product tested?\n\n- Status: answered\n"
                "- Recommendation: Unit tests.\n- Answer: Unit tests. Answered on 2026-09-21.\n"),
         (("docs/questions.md", 98, "Q-004 is already defined on line 26"),)),
    Case("register-field", edit("docs/questions.md", "- Recommendation: One API", "- Priority: high\n- Recommendation: One API"),
         (("docs/questions.md", 16,
           "Q-002 has unknown field Priority; allowed: Status, Covers, Blocks, Recommendation, Answer, Owner, Questionnaire"),)),
    Case("register-status", edit("docs/questions.md", "- Status: answered\n- Covers: operations/ci", "- Status: closed\n- Covers: operations/ci"),
         (("docs/questions.md", 35, "Q-005 has Status 'closed'; use open, answered or delegated"),)),
    Case("register-recommendation",
         edit("docs/questions.md", "- Recommendation: One API service and a cross-platform app, on a managed container host.",
              "- Recommendation:"),
         (("docs/questions.md", 16, "Q-002 needs a non-empty Recommendation"),)),
    Case("register-answer", edit("docs/questions.md", "- Answer: As recommended. Answered on 2026-09-20.", "- Answer: As recommended."),
         (("docs/questions.md", 17, "Q-002 has an Answer without a date YYYY-MM-DD"),)),
    Case("register-covers", edit("docs/questions.md", "- Covers: performance/budgets", "- Covers: billing/refunds, performance/budgets"),
         (("docs/questions.md", 58, "Q-008 covers billing/refunds, which is not an area of a planned document"),)),
    Case("inputs-parse", edit("docs/inputs.md", "- Kind: asset", "- Kind: asset\n- vector files later"),
         (("docs/inputs.md", 24, "a field line must read `- Key: value` with Key one of: Status, Kind, Needed for, How to get, Location, Reason, Owner"),)),
    Case("inputs-duplicate",
         append("docs/inputs.md", "\n### IN-003 Shop logo again\n\n- Status: not-needed\n- Kind: asset\n- Needed for: design-system\n- Reason: Same as above.\n"),
         (("docs/inputs.md", 27, "IN-003 is already defined on line 20"),)),
    Case("inputs-field", edit("docs/inputs.md", "- Kind: asset", "- Kind: asset\n- Cost: free"),
         (("docs/inputs.md", 24, "IN-003 has unknown field Cost; allowed: Status, Kind, Needed for, How to get, Location, Reason, Owner"),)),
    Case("inputs-status", edit("docs/inputs.md", "- Status: not-needed", "- Status: pending"),
         (("docs/inputs.md", 22, "IN-003 has Status 'pending'; use missing, provided or not-needed"),)),
    Case("inputs-kind", edit("docs/inputs.md", "- Kind: asset", "- Kind: logo"),
         (("docs/inputs.md", 23, "IN-003 has Kind 'logo'; use information, asset, account, access, tool"),)),
    Case("inputs-needed-for", edit("docs/inputs.md", "- Needed for: design-system", "- Needed for:"),
         (("docs/inputs.md", 24, "IN-003 needs a non-empty Needed for"),)),
    Case("inputs-how", edit("docs/inputs.md", "- How to get: Enroll the shop as an organization with both app stores.\n", ""),
         (("docs/inputs.md", 12, "IN-002 is missing and needs How to get"),)),
    Case("inputs-reason", edit("docs/inputs.md", "- Reason: The v1.0 app uses a text wordmark instead.\n", ""),
         (("docs/inputs.md", 20, "IN-003 is not-needed and needs a Reason"),)),
    Case("inputs-location", edit("docs/inputs.md", '- Location: The shop\'s password manager, entry "Sprocket Supply sandbox".', "- Location:"),
         (("docs/inputs.md", 10, "IN-001 is provided and needs a Location"),)),
    Case("prd-id", edit("docs/prd.md", "| `REQ-PART-002` |", "| REQ-PART-01 | A mechanic sees the part price. | MAY | v1.1 |\n| `REQ-PART-002` |"),
         (("docs/prd.md", 42, "REQ-PART-01 must read REQ-<AREA>-<NNN>, such as REQ-PAY-001"),)),
    Case("prd-duplicate", append("docs/prd.md", "\n| REQ-PART-002 | Automatic reordering again. | OUT | - |\n"),
         (("docs/prd.md", 49, "REQ-PART-002 is already defined on line 42"),)),
    Case("prd-scope", edit("docs/prd.md", "| SHOULD | v1.0 |", "| NICE | v1.0 |"),
         (("docs/prd.md", 39, "REQ-BOOK-002 has scope 'NICE'; use MUST, SHOULD, MAY or OUT"),)),
    Case("prd-release", edit("docs/prd.md", "| SHOULD | v1.0 |", "| SHOULD | v2.0 |"),
         (("docs/prd.md", 39, "REQ-BOOK-002 has release 'v2.0'; use one of v1.0, v1.1"),)),
    Case("prd-area", edit("docs/prd.md", "| PART | Parts |\n", ""),
         (("docs/prd.md", 40, "REQ-PART-001 uses area PART, which the areas section does not declare"),
          ("docs/prd.md", 41, "REQ-PART-002 uses area PART, which the areas section does not declare"))),
    Case("ref-missing", append("docs/architecture.md", "Hosting costs are tracked in Q-099.\n"),
         (("docs/architecture.md", 33, "Q-099 is not a question in docs/questions.md"),)),
    Case("coverage-req", edit("docs/prd.md", "| MUST | v1.1 |", "| MUST | v1.0 |"),
         (("docs/prd.md", 40, "REQ-NOTE-001 is in no live story's req with release v1.0 or earlier"),)),
    Case("coverage-area", edit("docs/questions.md", "notifications/caps, ", ""),
         (("docs/questions.md", None, "no question covers notifications/caps: How many messages a user may receive per day or week."),)),
    Case("backlog-filename", write("backlog/notes.md", "Loose notes from the workshop.\n"),
         (("backlog/notes.md", None, "the file name must be <ID>-<slug>.md, such as M1-E02-S03-pay-by-card.md"),)),
    Case("backlog-id", edit("backlog/M1-E02-S02-supplier-spike.md", "id: M1-E02-S02", "id: M1-E02-S09"),
         (("backlog/M1-E02-S02-supplier-spike.md", 2, "id M1-E02-S09 does not match the file name prefix M1-E02-S02"),)),
    Case("backlog-frontmatter", edit("backlog/M2-E01-S02-reschedule.md", "status: draft\n", "status: draft\n# owner asked for this\n"),
         (("backlog/M2-E01-S02-reschedule.md", 5, "a frontmatter line must read `key: value`"),)),
    Case("backlog-field", edit("backlog/M1-E01-S02-cancel-booking.md", "priority: medium", "priority: critical"),
         (("backlog/M1-E01-S02-cancel-booking.md", 5, "priority 'critical' must be one of urgent, high, medium, low"),)),
    Case("backlog-hierarchy", write("backlog/M3-E01-S01-loyalty-card.md", NEW_STORY),
         (("backlog/M3-E01-S01-loyalty-card.md", None, "story M3-E01-S01 needs its milestone file backlog/M3-<slug>.md"),)),
    Case("backlog-ref", edit("backlog/M1-E01-S02-cancel-booking.md", "req: [REQ-BOOK-002]", "req: [REQ-BOOK-002, REQ-BOOK-404]"),
         (("backlog/M1-E01-S02-cancel-booking.md", 8, "req names REQ-BOOK-404, which does not exist"),)),
    Case("backlog-cycle", edit("backlog/M1-E01-S01-book-a-slot.md", "lane: backend", "lane: backend\nblocked_by: [M1-E01-S02]"),
         (("backlog/M1-E01-S01-book-a-slot.md", 11, "blocked_by cycle: M1-E01-S01 -> M1-E01-S02 -> M1-E01-S01"),)),
    Case("backlog-ready", edit("backlog/M1-E01-S02-cancel-booking.md", "questions: [Q-007]", "questions: [Q-012]"),
         (("backlog/M1-E01-S02-cancel-booking.md", 4, "status is ready but Q-012 is open"),)),
    Case("backlog-blocked",
         edit("backlog/M1-E02-S01-T01-stock-client.md",
              "\nblocked_reason: Waiting for Sprocket Supply to enable the stock endpoint in the sandbox.", ""),
         (("backlog/M1-E02-S01-T01-stock-client.md", 4,
           "status is blocked but every prerequisite is met and blocked_reason is not set"),)),
    Case("backlog-done", edit("backlog/M1-E01-S01-T01-slot-api.md", "\nevidence: merge 9a3d2f1, CI run 198 green", ""),
         (("backlog/M1-E01-S01-T01-slot-api.md", 4, "status is done but evidence is not set"),)),
    Case("backlog-section", edit("backlog/M1-E01-S02-cancel-booking.md", "<!-- mirage:section verification -->\n", ""),
         (("backlog/M1-E01-S02-cancel-booking.md", None,
           "section verification is missing; add the marker <!-- mirage:section verification --> before its heading"),)),
    Case("backlog-estimate", edit("backlog/M1-E01-S01-book-a-slot.md", "lane: backend", "lane: backend\nestimate: 5"),
         (("backlog/M1-E01-S01-book-a-slot.md", 11,
           "the estimate sits on the story and on its tasks M1-E01-S01-T01, M1-E01-S01-T02; keep one"),)),
    Case("backlog-label", edit("backlog/M1-E01-S02-cancel-booking.md", 'labels: [area:mobile, "type:feature"]', 'labels: ["type:feature"]'),
         (("backlog/M1-E01-S02-cancel-booking.md", 11, "a story needs at least one area:<area> label"),)),
    Case("backlog-kind", edit("backlog/M1-E02-S02-supplier-spike.md", "kind: spike", "kind: research"),
         (("backlog/M1-E02-S02-supplier-spike.md", 5, "kind 'research' must be one of feature, spike, bug, chore, docs"),)),
    Case("backlog-due", edit("backlog/M2-reminders.md", "status: draft", "status: draft\ndue: 2027-03-01"),
         (("backlog/M2-reminders.md", 5, "due needs due_evidence"),)),
    Case("backlog-replace", edit("backlog/M1-E01-S04-reminder-sms.md", "\nreplaced_by: M2-E01-S01", ""),
         (("backlog/M2-E01-S01-booking-reminders.md", 13, "M1-E01-S04 must name M2-E01-S01 in replaced_by"),)),
    Case("sources-missing", delete("docs/sources/workshop-brief.txt"),
         (("docs/sources/SHA256SUMS", 1, "workshop-brief.txt is listed but does not exist"),)),
    Case("sources-hash", append("docs/sources/workshop-brief.txt", "Late addition.\n"),
         (("docs/sources/SHA256SUMS", 1, "workshop-brief.txt does not match its listed hash"),)),
    Case("sources-unlisted", write("docs/sources/price-list.txt", "Tune-up: 40\n"),
         (("docs/sources/price-list.txt", None, "the file is not listed in docs/sources/SHA256SUMS"),)),
    Case("link-broken", append("docs/operations.md", "See the [runbook](runbook.md).\n"),
         (("docs/operations.md", 47, "the link target runbook.md does not exist"),)),
    Case("secret", append("docs/security.md", f"Backup access: {FAKE_AWS_KEY}\n"),
         (("docs/security.md", 33, "the line matches the AWS access key pattern; keep the secret out of the "
           "repository and record where it lives in docs/inputs.md"),)),
)


class ValidFixture(unittest.TestCase):
    maxDiff = None

    def test_check_prints_ok(self):
        self.assertEqual(run("check", "--root", FIXTURE), (0, "ok\n", ""))

    def test_check_json_is_empty(self):
        self.assertEqual(errors(FIXTURE), [])

    def test_plan_covers_per_item_per_component_and_flag_documents(self):
        docs = check.plan_entries(check.load_project(FIXTURE))
        self.assertEqual([(d["key"], d["path"], d["reason"]) for d in docs], [
            ("readme", "README.md", "always"),
            ("glossary", "GLOSSARY.md", "always"),
            ("index", "docs/README.md", "always"),
            ("summary", "docs/summary.md", "always"),
            ("questions", "docs/questions.md", "always"),
            ("inputs", "docs/inputs.md", "always"),
            ("prd", "docs/prd.md", "always"),
            ("architecture", "docs/architecture.md", "always"),
            ("security", "docs/security.md", "always"),
            ("test-strategy", "docs/test-strategy.md", "always"),
            ("operations", "docs/operations.md", "always"),
            ("delivery", "docs/delivery.md", "always"),
            ("agents", "AGENTS.md", "always"),
            ("ux", "docs/ux.md", "components include mobile-app"),
            ("design-system", "docs/design-system.md", "components include mobile-app"),
            ("performance", "docs/performance.md", "components include mobile-app, backend-service"),
            ("api", "docs/api.md", "components include backend-service"),
            ("data-model", "docs/data-model.md", "components include backend-service"),
            ("platform:mobile-app", "docs/platforms/mobile-app.md", "components include mobile-app"),
            ("integration:sprocket-supply", "docs/integrations/sprocket-supply.md", "integrations includes sprocket-supply"),
            ("notifications", "docs/notifications.md", "flag notifications is true"),
            ("sources", "docs/sources/SHA256SUMS", "flag source_documents is true"),
            ("audit-log", "docs/audit-log.md", "always"),
        ])
        self.assertTrue(all(d["exists"] for d in docs))
        self.assertTrue(all(a["covered"] for d in docs for a in d["areas"]))


class GlossaryName(unittest.TestCase):
    """domain-modeling wrote CONTEXT.md before it wrote GLOSSARY.md, and a project may hold either."""

    def test_the_older_name_is_planned_when_only_it_exists(self):
        with fixture_copy() as root:
            (root / "GLOSSARY.md").rename(root / "CONTEXT.md")
            run("index", "--root", root)
            docs = {d["key"]: (d["path"], d["exists"]) for d in check.plan_entries(check.load_project(root))}
            self.assertEqual(docs["glossary"], ("CONTEXT.md", True))
            self.assertEqual(run("check", "--root", root), (0, "ok\n", ""))

    def test_references_in_the_older_file_are_still_resolved(self):
        with fixture_copy() as root:
            (root / "GLOSSARY.md").rename(root / "CONTEXT.md")
            append("CONTEXT.md", "See Q-404.\n")(root)
            found = [(e["path"], e["code"], e["message"]) for e in errors(root, "--only", "refs")]
        self.assertEqual(found, [("CONTEXT.md", "ref-missing", "Q-404 is not a question in docs/questions.md")])

    def test_a_missing_glossary_names_both_files(self):
        with fixture_copy() as root:
            (root / "GLOSSARY.md").unlink()
            found = [(e["path"], e["code"], e["message"]) for e in errors(root, "--only", "docs")]
        self.assertEqual(found, [(
            "GLOSSARY.md", "doc-missing",
            "Glossary (glossary) is missing; it is planned because always; CONTEXT.md is accepted too",
        )])


class Mutations(unittest.TestCase):
    maxDiff = None

    def test_cases_cover_every_check_code_exactly_once(self):
        group_codes = sorted(code for codes in check.GROUPS.values() for code in codes)
        self.assertEqual(sorted(case.code for case in CASES), group_codes)

    def test_the_only_codes_outside_the_groups_are_reported_by_docs_ready(self):
        # These have no mutation case: check never reports them, and test_commands.DocsReady covers them.
        self.assertEqual(sorted(set(check.CODES) - {c for codes in check.GROUPS.values() for c in codes}),
                         ["audit-missing", "prd-empty"])
        self.assertEqual(check.COMMAND_CODES, {"prd-empty": "docs-ready", "audit-missing": "docs-ready"})
        self.assertEqual(sorted(case.code for case in CASES), sorted(set(check.CODES) - set(check.COMMAND_CODES)))

    def test_a_diagnostic_cannot_carry_an_unlisted_code(self):
        with self.assertRaises(ValueError):
            check.Diagnostic("docs/prd.md", 1, "prd-typo", "never emitted")


def _mutation_test(case: Case):
    def test(self: Mutations) -> None:
        with fixture_copy() as root:
            case.mutation(root)
            if case.reindex:
                self.assertEqual(run("index", "--root", root)[0], 0)
            found = [(e["code"], e["path"], e["line"], e["message"]) for e in errors(root)]
            self.assertEqual(found, [(case.code, path, line, message) for path, line, message in case.expect])
    return test


for _case in CASES:
    setattr(Mutations, "test_" + _case.code.replace("-", "_"), _mutation_test(_case))


class CommandLine(unittest.TestCase):
    maxDiff = None

    def cli(self, *argv: str, cwd: Optional[Path] = None, script: Path = SCRIPT) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(script), *argv], cwd=cwd, capture_output=True, text=True)

    def test_version(self):
        result = self.cli("version")
        self.assertEqual((result.returncode, result.stdout), (0, "0.1.0\n"))

    def test_check_text_output_and_exit_code(self):
        with fixture_copy() as root:
            append("docs/security.md", "Owner: {{name}}\n")(root)
            append("docs/api.md", "See Q-404.\n")(root)
            result = self.cli("check", "--root", str(root))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, (
            "docs/api.md:53: ref-missing: Q-404 is not a question in docs/questions.md\n"
            "docs/security.md:33: doc-placeholder: the line holds a {{ placeholder; write the content or cite a question\n"
            "2 errors\n"
        ))

    def test_only_runs_the_named_groups(self):
        with fixture_copy() as root:
            append("docs/security.md", "Owner: {{name}}\n")(root)
            edit("docs/prd.md", "| SHOULD | v1.0 |", "| NICE | v1.0 |")(root)
            code, out, _ = run("check", "--root", root, "--only", "prd,refs")
        self.assertEqual((code, out), (1, (
            "docs/prd.md:39: prd-scope: REQ-BOOK-002 has scope 'NICE'; use MUST, SHOULD, MAY or OUT\n1 error\n"
        )))

    def test_unknown_group_is_a_usage_error(self):
        self.assertEqual(run("check", "--root", FIXTURE, "--only", "prd,typo"),
                         (2, "", "error: unknown group typo; groups: project, docs, index, register, prd, refs, "
                                 "coverage, backlog, sources, links, secrets\n"))

    def test_missing_project_json_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.cli("check", "--root", tmp)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.startswith("error: cannot read .mirage/project.json:"), result.stderr)

    def test_unparseable_project_json_exits_2(self):
        with fixture_copy() as root:
            write(".mirage/project.json", "{not json")(root)
            code, _, err = run("plan", "--root", root)
        self.assertEqual(code, 2)
        self.assertTrue(err.startswith("error: cannot read .mirage/project.json: Expecting property name"), err)

    def test_vendored_copy_finds_its_root_and_catalog(self):
        with fixture_copy() as root, tempfile.TemporaryDirectory() as elsewhere:
            shutil.copy(SCRIPT, root / ".mirage" / "check.py")
            shutil.copy(SCRIPT.parent / "catalog.json", root / ".mirage" / "catalog.json")
            ok = self.cli("check", cwd=Path(elsewhere), script=root / ".mirage" / "check.py")
            delete("CLAUDE.md")(root)
            broken = self.cli("check", cwd=Path(elsewhere), script=root / ".mirage" / "check.py")
        self.assertEqual((ok.returncode, ok.stdout), (0, "ok\n"))
        self.assertEqual((broken.returncode, broken.stdout), (
            1, "CLAUDE.md: claude-import: CLAUDE.md is missing; it must hold the line @AGENTS.md\n1 error\n"))

    def test_every_command_accepts_root(self):
        for argv in (["check"], ["plan"], ["docs-ready"], ["ready"], ["index"], ["version"], ["sync-plan", "plane"],
                     ["sync-expect", "plane"],
                     ["set-status", "M9", "draft"], ["sync-record", "plane", "--unlink", "M1", "M2"],
                     ["sync-record", "plane", "--forget", "M1"]):
            with self.subTest(argv=argv):
                self.assertEqual(check.build_parser().parse_args([*argv, "--root", "x"]).root, "x")


if __name__ == "__main__":
    unittest.main()
