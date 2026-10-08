"""Parsers and scanners at the file boundary: frontmatter, registers, markers, links, references and secrets."""

from __future__ import annotations

import unittest

from support import append, check, edit, edit_json, errors, fixture_copy, run, write


def found(root, *extra):
    return [(e["path"], e["line"], e["code"], e["message"]) for e in errors(root, *extra)]


class Frontmatter(unittest.TestCase):
    maxDiff = None

    def test_accepts_the_strict_subset(self):
        fields, body_start, problems = check.parse_frontmatter([
            "---",
            'title: "Say \\"hi\\" \\\\ twice"',
            'labels: [area:mobile, "type:a, b", plain words]',
            "req: []",
            "evidence: text # not a comment",
            "",
            "lane:",
            "---",
            "body",
        ])
        self.assertEqual({key: value.value for key, value in fields.items()}, {
            "title": 'Say "hi" \\ twice',
            "labels": ("area:mobile", "type:a, b", "plain words"),
            "req": (),
            "evidence": "text # not a comment",
            "lane": "",
        })
        self.assertEqual((fields["labels"].line, body_start, problems), (3, 8, []))

    def test_rejects_anything_outside_the_subset(self):
        _, _, problems = check.parse_frontmatter([
            "---", "  nested: x", "# comment", "key:value", "list: [a, , b]", 'quote: "open',
            "title: a", "title: b", 'tail: "x" y', "esc: \"a\\nb\"", "---",
        ])
        self.assertEqual(problems, [
            (2, "a frontmatter line must read `key: value`"),
            (3, "a frontmatter line must read `key: value`"),
            (4, "a frontmatter line must read `key: value`"),
            (5, "list: list items must be bare words or double-quoted strings"),
            (6, "quote: unterminated quoted string"),
            (8, "key title appears twice"),
            (9, "tail: text follows the closing quote"),
            (10, 'esc: only \\" and \\\\ escapes are allowed'),
        ])

    def test_unclosed_or_absent_frontmatter(self):
        self.assertEqual(check.parse_frontmatter(["---", "id: M1"])[2], [(1, "the frontmatter has no closing --- line")])
        self.assertEqual(check.parse_frontmatter(["id: M1"])[2], [(1, "the file must start with a --- frontmatter line")])


class Markers(unittest.TestCase):
    maxDiff = None

    def test_placeholders_in_fenced_code_are_allowed_but_todo_markers_are_not(self):
        with fixture_copy() as root:
            append("docs/api.md", "```\n{{template}}\n<!-- mirage:todo -->\n```\n<!-- mirage:todo write limits -->\n")(root)
            self.assertEqual(found(root), [
                ("docs/api.md", 55, "doc-placeholder", "the line holds a mirage:todo marker; write the content or cite a question"),
                ("docs/api.md", 57, "doc-placeholder", "the line holds a mirage:todo marker; write the content or cite a question"),
            ])

    def test_a_second_or_foreign_doc_marker_is_reported(self):
        with fixture_copy() as root:
            append("docs/api.md", "<!-- mirage:doc api -->\n<!-- mirage:doc prd -->\n")(root)
            self.assertEqual(found(root), [
                ("docs/api.md", 53, "doc-marker", "the doc marker for api appears 2 times"),
                ("docs/api.md", 54, "doc-marker", "the doc marker names prd; this document is api"),
            ])

    def test_a_section_marker_must_sit_before_its_heading(self):
        with fixture_copy() as root:
            edit("docs/api.md", "<!-- mirage:section limits -->\n## Rate limits\n", "<!-- mirage:section limits -->\nRate limits.\n")(root)
            self.assertEqual(found(root), [
                ("docs/api.md", 39, "doc-section", "section marker limits must sit directly before its heading"),
            ])


class Registers(unittest.TestCase):
    maxDiff = None

    def test_a_malformed_question_heading_is_a_parse_error(self):
        with fixture_copy() as root:
            append("docs/questions.md", "\n### Q-12 Which bell?\n\n- Status: open\n")(root)
            self.assertEqual(found(root, "--only", "register"), [
                ("docs/questions.md", 98, "register-parse", "heading must read `### Q-nnn <title>`"),
            ])

    def test_answered_question_needs_an_answer_and_status_is_required(self):
        with fixture_copy() as root:
            edit("docs/questions.md", "- Answer: As recommended. Answered on 2026-09-20.\n", "")(root)
            edit("docs/questions.md", "- Status: answered\n- Covers: performance", "- Covers: performance")(root)
            self.assertEqual(found(root, "--only", "register"), [
                ("docs/questions.md", 12, "register-answer", "Q-002 is answered but has no Answer"),
                ("docs/questions.md", 54, "register-status", "Q-008 has no Status; use open, answered or delegated"),
            ])

    def test_an_answer_date_must_be_a_real_date(self):
        with fixture_copy() as root:
            edit("docs/questions.md", "Answered on 2026-09-20.\n\n### Q-003", "Answered on 2026-02-30.\n\n### Q-003")(root)
            self.assertEqual(found(root, "--only", "register"), [
                ("docs/questions.md", 17, "register-answer", "Q-002 has an Answer without a date YYYY-MM-DD"),
            ])


class Prd(unittest.TestCase):
    maxDiff = None

    def test_areas_come_from_the_areas_section_without_its_header(self):
        with fixture_copy() as root:
            edit("docs/prd.md", "| Code | Name |", "| AREA | Name |")(root)
            edit("docs/prd.md", "Customers book and cancel slots.", "| Code | Name |\n|---|---|\n| PAY | Payments |\n\nCustomers book and cancel slots.")(root)
            append("docs/prd.md", "| REQ-AREA-001 | Header row. | OUT | - |\n| REQ-PAY-001 | Other table. | OUT | - |\n")(root)
            self.assertEqual(found(root, "--only", "prd"), [
                ("docs/prd.md", 52, "prd-area", "REQ-AREA-001 uses area AREA, which the areas section does not declare"),
                ("docs/prd.md", 53, "prd-area", "REQ-PAY-001 uses area PAY, which the areas section does not declare"),
            ])


class FencedPrd(unittest.TestCase):
    def test_requirement_rows_inside_fenced_code_are_ignored(self):
        with fixture_copy() as root:
            append("docs/prd.md", "```\n| REQ-ZZZ-001 | An example row. | MUST | v9 |\n| REQ-BOOK-001 | Twice. | MUST | v1.0 |\n```\n")(root)
            self.assertEqual(run("check", "--root", root), (0, "ok\n", ""))


class Sources(unittest.TestCase):
    maxDiff = None

    def test_a_listed_directory_is_named_as_one(self):
        with fixture_copy() as root:
            write("docs/sources/scans/page-1.txt", "Scanned page.\n")(root)
            append("docs/sources/SHA256SUMS", "0" * 64 + "  scans\n")(root)
            self.assertEqual(found(root, "--only", "sources"), [
                ("docs/sources/SHA256SUMS", 2, "sources-missing", "scans is listed but is a directory, not a file"),
                ("docs/sources/scans/page-1.txt", None, "sources-unlisted", "the file is not listed in docs/sources/SHA256SUMS"),
            ])


class ProjectJson(unittest.TestCase):
    maxDiff = None

    def test_each_facet_rule(self):
        def change(data):
            data["components"].append({"id": "app", "kind": "mobile-app"})
            data["components"].append({"id": "Kiosk", "kind": "kiosk"})
            data["integrations"].append("Sprocket")
            data["releases"] = []
            data["colour"] = "green"
        with fixture_copy() as root:
            edit_json(".mirage/project.json", change)(root)
            self.assertEqual([m for _, _, _, m in found(root, "--only", "project")], [
                "component id app is used twice",
                "components[3] needs an id that is a lowercase slug",
                "integrations entry 'Sprocket' is not a lowercase slug",
                "releases must be a non-empty list of names",
                "unknown key colour",
            ])


class Links(unittest.TestCase):
    maxDiff = None

    def test_only_relative_targets_outside_code_are_checked(self):
        lines = [
            "[anchor](#states) [site](https://example.invalid) [mail](mailto:shop@example.invalid)",
            "[same file](api.md#errors) [image](../AGENTS.md) [absolute](/CLAUDE.md) [spaced](<missing%20file.md>)",
            "`[code](nowhere.md)` [deep](adr/0001-one-booking-api.md) [gone](adr/0002-gone.md#top)",
            "```",
            "[fenced](nowhere.md)",
            "```",
            "[ref]: missing-ref.md",
        ]
        with fixture_copy() as root:
            append("docs/api.md", "\n".join(lines) + "\n")(root)
            self.assertEqual(found(root, "--only", "links"), [
                ("docs/api.md", 54, "link-broken", "the link target <missing%20file.md> does not exist"),
                ("docs/api.md", 55, "link-broken", "the link target adr/0002-gone.md#top does not exist"),
                ("docs/api.md", 59, "link-broken", "the link target missing-ref.md does not exist"),
            ])


class References(unittest.TestCase):
    maxDiff = None

    def test_each_reference_kind(self):
        with fixture_copy() as root:
            append("docs/api.md", "REQ-BOOK-001 Q-001 IN-001 ADR-0001 M1-E01-S01-T01 are fine.\n"
                   "REQ-BOOK-009 IN-009 ADR-0009 M1-E01-S01-T09 and Q-099 twice: Q-099.\n"
                   "```\nQ-777 in code\n```\n")(root)
            self.assertEqual(found(root, "--only", "refs"), [
                ("docs/api.md", 54, "ref-missing", "ADR-0009 has no file docs/adr/NNNN-*.md"),
                ("docs/api.md", 54, "ref-missing", "IN-009 is not an input in docs/inputs.md"),
                ("docs/api.md", 54, "ref-missing", "M1-E01-S01-T09 has no file in backlog/"),
                ("docs/api.md", 54, "ref-missing", "Q-099 is not a question in docs/questions.md"),
                ("docs/api.md", 54, "ref-missing", "REQ-BOOK-009 is not a requirement in docs/prd.md"),
            ])

    def test_generated_files_are_not_scanned(self):
        with fixture_copy() as root:
            edit("backlog/M2-E01-S02-reschedule.md", "labels: [area:mobile]", "labels: [area:mobile]\nblocked_by: [M1-E01-S09]")(root)
            edit("docs/inputs.md", "- Needed for: platform:mobile-app, M2-E01-S01", "- Needed for: platform:mobile-app, M9-E01-S01")(root)
            write("docs/notes.md", "<!-- mirage:generated notes -->\nSee [nothing](nowhere.md) and Q-404 with "
                  + "AKIA" + "Z" * 16 + ".\n")(root)
            run("index", "--root", root)
            self.assertIn("| M2-E01-S02 | Move a booking to another slot | draft | mobile | M1-E01-S09 |",
                          (root / "backlog/README.md").read_text(encoding="utf-8").split("\n"))
            self.assertEqual(found(root), [
                ("backlog/M2-E01-S02-reschedule.md", 9, "backlog-ref", "blocked_by names M1-E01-S09, which does not exist"),
                ("docs/inputs.md", 16, "ref-missing", "M9-E01-S01 has no file in backlog/"),
            ])

    def test_backlog_frontmatter_is_left_to_the_backlog_group(self):
        with fixture_copy() as root:
            edit("backlog/M2-E01-S02-reschedule.md", "labels: [area:mobile]", "labels: [area:mobile]\nquestions: [Q-404]")(root)
            append("backlog/M2-E01-S02-reschedule.md", "Depends on Q-405.\n")(root)
            self.assertEqual(found(root, "--only", "refs,backlog"), [
                ("backlog/M2-E01-S02-reschedule.md", 9, "backlog-ref", "questions names Q-404, which does not exist"),
                ("backlog/M2-E01-S02-reschedule.md", 15, "ref-missing", "Q-405 is not a question in docs/questions.md"),
            ])


class Secrets(unittest.TestCase):
    maxDiff = None

    TOKENS = {
        "private key header": "-----BEGIN RSA " + "PRIVATE KEY-----",
        "AWS access key": "AKIA" + "7" * 16,
        "Stripe live key": "sk_" + "live_" + "a" * 24,
        "GitHub token": "ghp_" + "b" * 36,
        "Slack token": "xox" + "b-" + "1234567890-abc",
    }

    def test_each_pattern_is_named_and_the_match_is_never_printed(self):
        for name, token in self.TOKENS.items():
            with self.subTest(name=name), fixture_copy() as root:
                append("docs/api.md", f"```\n{token}\n```\n")(root)
                code, out, _ = run("check", "--root", root)
                self.assertEqual((code, out), (1, (
                    f"docs/api.md:54: secret: the line matches the {name} pattern; keep the secret out of the "
                    "repository and record where it lives in docs/inputs.md\n1 error\n"
                )))
                self.assertNotIn(token, out)

    def test_project_json_is_scanned_and_the_generated_index_is_not(self):
        with fixture_copy() as root:
            edit_json(".mirage/project.json", lambda d: d.update(name="Hollow Lane " + self.TOKENS["GitHub token"]))(root)
            run("index", "--root", root)
            self.assertIn(self.TOKENS["GitHub token"], (root / "docs/README.md").read_text(encoding="utf-8"))
            self.assertEqual([(p, n, c) for p, n, c, _ in found(root, "--only", "secrets")],
                             [(".mirage/project.json", 3, "secret")])


if __name__ == "__main__":
    unittest.main()
