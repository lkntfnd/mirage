"""ready, index, set-status, sync-plan and sync-record."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from typing import List
from unittest import mock

from support import FIXTURE, catalog_doc, check, delete, edit, edit_json, facets, fixture_copy, project, run, synthetic_catalog, write

S02 = "backlog/M1-E01-S02-cancel-booking.md"
S02_TEXT = """---
id: M1-E01-S02
title: Cancel a booking
status: ready
priority: medium
scope: should
release: v1.0
req: [REQ-BOOK-002]
questions: [Q-007]
blocked_by: [M1-E01-S01]
labels: [area:mobile, "type:feature"]
estimate: 2
---

## Acceptance criteria

- [ ] A customer cancels up to two hours before the slot.
- [ ] A later cancellation is refused with a reason.
"""


def ready_json(root: Path) -> list:
    code, out, _ = run("ready", "--root", root, "--json")
    assert code == 0
    return json.loads(out)["lanes"]


def lane(root: Path, name: str) -> dict:
    return next(entry for entry in ready_json(root) if entry["lane"] == name)


class Ready(unittest.TestCase):
    maxDiff = None

    def test_fixture_groups_by_lane(self):
        self.assertEqual(ready_json(FIXTURE), [
            {"lane": "mobile",
             "ready_now": [{"id": "M1-E01-S02", "title": "Cancel a booking", "status": "ready"}],
             "can_become_ready": [{"id": "M2-E01-S02", "title": "Move a booking to another slot", "status": "draft"}],
             "wrongly_ready": []},
        ])

    def test_text_output(self):
        self.assertEqual(run("ready", "--root", FIXTURE), (0, (
            "lane mobile\n"
            "  ready now\n"
            "    M1-E01-S02 Cancel a booking\n"
            "  can become ready\n"
            "    M2-E01-S02 Move a booking to another slot (draft)\n"
            "  wrongly ready\n"
            "    none\n"
        ), ""))

    def test_a_blocked_reason_keeps_an_item_out_of_can_become_ready(self):
        with fixture_copy() as root:
            edit("backlog/M1-E02-S01-T01-stock-client.md",
                 "\nblocked_reason: Waiting for Sprocket Supply to enable the stock endpoint in the sandbox.", "")(root)
            backend = lane(root, "backend")
        self.assertEqual(backend, {
            "lane": "backend", "ready_now": [], "wrongly_ready": [],
            "can_become_ready": [{"id": "M1-E02-S01-T01", "title": "Supplier stock client", "status": "blocked"}],
        })

    def test_wrongly_ready_names_each_unmet_prerequisite(self):
        with fixture_copy() as root:
            edit("backlog/M2-E01-S01-booking-reminders.md", "status: blocked", "status: ready")(root)
            mobile = lane(root, "mobile")
        self.assertEqual(mobile["wrongly_ready"], [{
            "id": "M2-E01-S01", "title": "Booking reminders", "status": "ready",
            "unmet": ["Q-012 is open", "IN-002 is missing"],
        }])

    def test_can_become_ready_needs_a_checklist_item(self):
        with fixture_copy() as root:
            edit("backlog/M2-E01-S02-reschedule.md", "- [ ] A customer moves", "A customer moves")(root)
            mobile = lane(root, "mobile")
        self.assertEqual(mobile["can_become_ready"], [])

    def test_a_task_inherits_its_story_prerequisites(self):
        with fixture_copy() as root:
            edit("docs/inputs.md", "- Status: provided", "- Status: missing\n- How to get: Ask the supplier.")(root)
            edit("backlog/M1-E02-S01-T01-stock-client.md", "status: blocked", "status: ready")(root)
            backend = lane(root, "backend")
        self.assertEqual(backend["wrongly_ready"], [{
            "id": "M1-E02-S01-T01", "title": "Supplier stock client", "status": "ready", "unmet": ["IN-001 is missing"],
        }])

    def test_a_task_inherits_its_story_questions_and_blockers(self):
        with fixture_copy() as root:
            edit("backlog/M1-E02-S01-check-part-stock.md", "inputs: [IN-001]",
                 "inputs: [IN-001]\nquestions: [Q-012]\nblocked_by: [M2-E01-S01]")(root)
            edit("backlog/M1-E02-S01-T01-stock-client.md", "status: blocked", "status: ready")(root)
            backend = lane(root, "backend")
        self.assertEqual(backend["wrongly_ready"][0]["unmet"], ["Q-012 is open", "M2-E01-S01 is blocked"])

    def test_confirmed_delegation_keeps_delegated_answers_unmet(self):
        with fixture_copy() as root:
            edit(S02, "questions: [Q-007]", "questions: [Q-003]")(root)
            self.assertEqual(lane(root, "mobile")["ready_now"][0]["id"], "M1-E01-S02")
            edit_json(".mirage/project.json", lambda d: d.update(require_confirmed_delegation=True))(root)
            mobile = lane(root, "mobile")
        self.assertEqual(mobile["ready_now"], [])
        self.assertEqual(mobile["wrongly_ready"][0]["unmet"], ["Q-003 is delegated and awaits confirmation"])


TINY = {
    ".mirage/project.json": facets(integrations=["tile-maps"]),
    ".mirage/catalog.json": synthetic_catalog(
        catalog_doc("index", "docs/README.md", "always", "generated"),
        catalog_doc("prd", "docs/prd.md", "always"),
        catalog_doc("integration", "docs/integrations/{item}.md", {"per": "integrations"}),
    ),
    "docs/prd.md": "| ID | Requirement | Scope | Release |\n|---|---|---|---|\n| REQ-CORE-001 | Print a receipt. | MUST | v1 |\n",
    "docs/questions.md": "### Q-001 Which printer | model?\n\n- Status: open\n- Blocks: M1-E01-S01\n- Recommendation: Any.\n\n"
                         "### Q-002 Which paper?\n\n- Status: delegated\n- Recommendation: Thermal.\n"
                         "- Answer: Thermal. Delegated on 2026-01-05.\n",
    "docs/inputs.md": "### IN-001 Printer driver\n\n- Status: missing\n- Kind: tool\n- Needed for: M1-E01-S01-T01\n"
                      "- How to get: Download it.\n",
    "docs/adr/0001-thermal-paper.md": "Thermal paper.\n",
    "backlog/M1-first.md": "---\nid: M1\ntitle: First | release\nstatus: in-progress\n---\n",
    "backlog/E01-core.md": "---\nid: E01\ntitle: Core\nstatus: draft\n---\n",
    "backlog/M1-E01-S01-print.md": "---\nid: M1-E01-S01\ntitle: Print\nstatus: blocked\npriority: high\nscope: must\n"
                                   "release: v1\nreq: [REQ-CORE-001]\nquestions: [Q-001]\nlabels: [area:core]\n---\n",
    "backlog/M1-E01-S01-T01-driver.md": "---\nid: M1-E01-S01-T01\ntitle: Driver\nstatus: draft\nlabels: [area:core]\n"
                                        "blocked_by: [M1-E01-S01]\n---\n",
    "backlog/M2-E01-S01-later.md": "---\nid: M2-E01-S01\ntitle: Later\nstatus: draft\npriority: low\nscope: may\n"
                                   "release: v1\nlabels: [area:core]\n---\n",
}

TINY_DOCS_INDEX = """<!-- mirage:generated index -->

# Tiny Kiosk

Generated by `check.py index`. Edit the source files and run it again; do not edit this file.

## Reading order

| Key | Document | Path | Exists |
|---|---|---|---|
| index | Index | `docs/README.md` | yes |
| prd | Prd | `docs/prd.md` | yes |
| integration:tile-maps | Integration | `docs/integrations/tile-maps.md` | no |

## Open questions

| ID | Question | Blocks |
|---|---|---|
| Q-001 | Which printer \\| model? | M1-E01-S01 |

## Delegated answers awaiting confirmation

| ID | Question | Answer |
|---|---|---|
| Q-002 | Which paper? | Thermal. Delegated on 2026-01-05. |

## Missing inputs

| ID | Input | Needed for |
|---|---|---|
| IN-001 | Printer driver | M1-E01-S01-T01 |

## Counts

| Kind | Count |
|---|---|
| Requirements | 1 |
| Questions | 2 |
| Inputs | 1 |
| ADRs | 1 |
| Milestones | 1 |
| Epics | 1 |
| Stories | 2 |
| Tasks | 1 |
"""

TINY_BACKLOG_INDEX = """<!-- mirage:generated backlog -->

# Backlog

Generated by `check.py index`. Edit the source files and run it again; do not edit this file.

## M1 First | release

Status: in-progress.

| ID | Title | Status | Lane | Blockers |
|---|---|---|---|---|
| M1-E01-S01 | Print | blocked | core | - |
| M1-E01-S01-T01 | Driver | draft | core | M1-E01-S01 |

## M2

| ID | Title | Status | Lane | Blockers |
|---|---|---|---|---|
| M2-E01-S01 | Later | draft | core | - |

## Epics

| ID | Title | Status |
|---|---|---|
| E01 | Core | draft |
"""


class Index(unittest.TestCase):
    maxDiff = None

    def test_writes_both_files_exactly(self):
        with project(TINY) as root:
            self.assertEqual(run("index", "--root", root), (0, "docs/README.md written\nbacklog/README.md written\n", ""))
            docs_index = (root / "docs/README.md").read_text(encoding="utf-8")
            backlog_index = (root / "backlog/README.md").read_text(encoding="utf-8")
            again = run("index", "--root", root)
            stale = run("check", "--root", root, "--only", "index")
        self.assertEqual(docs_index, TINY_DOCS_INDEX)
        self.assertEqual(backlog_index, TINY_BACKLOG_INDEX)
        self.assertEqual(again, (0, "docs/README.md unchanged\nbacklog/README.md unchanged\n", ""))
        self.assertEqual(stale, (0, "ok\n", ""))

    def test_regenerates_the_fixture_files(self):
        with fixture_copy() as root:
            delete("docs/README.md")(root)
            delete("backlog/README.md")(root)
            self.assertEqual(run("check", "--root", root, "--only", "index")[1], (
                "backlog/README.md: index-stale: the generated file is missing; run index\n"
                "docs/README.md: index-stale: the generated file is missing; run index\n"
                "2 errors\n"
            ))
            run("index", "--root", root)
            for rel in ("docs/README.md", "backlog/README.md"):
                self.assertEqual((root / rel).read_bytes(), (FIXTURE / rel).read_bytes(), rel)

    def test_adr_count_counts_numbers_once(self):
        with fixture_copy() as root:
            write("docs/adr/0001-zz-second-api.md", "A reused number.\n")(root)
            write("docs/adr/0002-parts-cache.md", "Cache supplier stock.\n")(root)
            stale = run("check", "--root", root, "--only", "index")
            run("index", "--root", root)
            counts = (root / "docs/README.md").read_text(encoding="utf-8").split("\n")
        self.assertEqual(stale, (1, "docs/README.md:57: index-stale: the generated file differs from what index writes; run index\n1 error\n", ""))
        self.assertIn("| ADRs | 2 |", counts)

    def test_exists_column_follows_the_files(self):
        with fixture_copy() as root:
            delete("docs/api.md")(root)
            run("index", "--root", root)
            text = (root / "docs/README.md").read_text(encoding="utf-8")
        self.assertIn("| api | API | `docs/api.md` | no |", text.split("\n"))


class SetStatus(unittest.TestCase):
    maxDiff = None

    def test_rewrites_only_the_status_line(self):
        with fixture_copy() as root:
            result = run("set-status", "M1-E01-S02", "in-progress", "--root", root)
            text = (root / S02).read_text(encoding="utf-8")
        self.assertEqual(result, (0, "M1-E01-S02: ready -> in-progress\n", ""))
        self.assertEqual(text, S02_TEXT.replace("status: ready\n", "status: in-progress\n"))

    def test_done_with_evidence_adds_the_evidence_line(self):
        with fixture_copy() as root:
            result = run("set-status", "M1-E01-S02", "done", "--evidence", 'merge 77c1d2e, CI "run" 240', "--root", root)
            text = (root / S02).read_text(encoding="utf-8")
            fields, _, problems = check.parse_frontmatter(text.split("\n"))
        self.assertEqual(result[0], 0)
        self.assertEqual(text, S02_TEXT.replace("status: ready\n", "status: done\n").replace(
            "estimate: 2\n---", 'estimate: 2\nevidence: merge 77c1d2e, CI "run" 240\n---'))
        self.assertEqual((fields["evidence"].value, problems), ('merge 77c1d2e, CI "run" 240', []))

    def test_evidence_that_needs_quotes_is_quoted(self):
        with fixture_copy() as root:
            run("set-status", "M1-E01-S01", "done", "--evidence", '"quoted" start', "--root", root)
            text = (root / "backlog/M1-E01-S01-book-a-slot.md").read_text(encoding="utf-8")
        self.assertIn('evidence: "\\"quoted\\" start"\n', text)
        self.assertNotIn("merge 4be81c0", text)

    def test_done_without_evidence_is_refused(self):
        with fixture_copy() as root:
            result = run("set-status", "M1-E01-S02", "done", "--root", root)
            text = (root / S02).read_text(encoding="utf-8")
        self.assertEqual(result, (2, "", "error: M1-E01-S02 has no evidence; pass --evidence to mark it done\n"))
        self.assertEqual(text, S02_TEXT)

    def test_done_keeps_evidence_already_present(self):
        with fixture_copy() as root:
            run("set-status", "M1-E02-S02", "in-review", "--root", root)
            result = run("set-status", "M1-E02-S02", "done", "--root", root)
        self.assertEqual(result, (0, "M1-E02-S02: in-review -> done\n", ""))

    def test_unknown_status_and_unknown_item_are_refused(self):
        self.assertEqual(run("set-status", "M1-E01-S02", "finished", "--root", FIXTURE), (
            2, "", "error: unknown status 'finished'; use one of draft, blocked, ready, in-progress, in-review, done, cancelled\n"))
        self.assertEqual(run("set-status", "M7-E01-S01", "draft", "--root", FIXTURE),
                         (2, "", "error: M7-E01-S01 has no file in backlog/\n"))

    def test_crlf_line_endings_survive(self):
        with fixture_copy() as root:
            path = root / S02
            path.write_bytes(S02_TEXT.replace("\n", "\r\n").encode())
            run("set-status", "M1-E01-S02", "blocked", "--root", root)
            data = path.read_bytes()
        self.assertEqual(data, S02_TEXT.replace("status: ready", "status: blocked").replace("\n", "\r\n").encode())


def plan_ops(root: Path) -> List[dict]:
    code, out, err = run("sync-plan", "plane", "--root", root)
    assert code == 0, err
    return [json.loads(line) for line in out.splitlines()]


def digest(root: Path, rel: str) -> str:
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


ALL_IDS = [
    "M1", "M2", "E01", "E02",
    "M1-E01-S01", "M1-E01-S02", "M1-E01-S04", "M1-E02-S01", "M1-E02-S02", "M2-E01-S01", "M2-E01-S02",
    "M1-E01-S01-T01", "M1-E01-S01-T02", "M1-E02-S01-T01",
]


def record_all(root: Path) -> None:
    for number, item_id in enumerate(ALL_IDS, 1):
        code, _, err = run("sync-record", "plane", "--root", root, "--id", item_id, "--remote-id", f"r{number}",
                           "--key", f"HL-{number}", "--url", f"https://tracker.invalid/HL-{number}")
        assert code == 0, err


class SyncPlan(unittest.TestCase):
    maxDiff = None

    def test_first_plan_creates_milestones_then_epics_stories_and_tasks(self):
        ops = plan_ops(FIXTURE)
        self.assertEqual([(op["op"], op["id"]) for op in ops], [("create", item_id) for item_id in ALL_IDS])

    def test_create_carries_the_item_fields(self):
        ops = {op["id"]: op for op in plan_ops(FIXTURE)}
        self.assertEqual(ops["M1-E01-S02"], {
            "op": "create",
            "id": "M1-E01-S02",
            "level": "story",
            "title": "Cancel a booking",
            "status": "ready",
            "priority": "medium",
            "labels": ["area:mobile", "type:feature"],
            "estimate": 2,
            "milestone": "M1",
            "epic": "E01",
            "parent": "E01",
            "body": "## Acceptance criteria\n\n- [ ] A customer cancels up to two hours before the slot.\n"
                    "- [ ] A later cancellation is refused with a reason.\n\nmirage-id: M1-E01-S02",
            "hash": digest(FIXTURE, S02),
        })
        self.assertEqual(
            {key: ops["M1-E02-S01-T01"][key] for key in ("level", "priority", "estimate", "milestone", "epic", "parent")},
            {"level": "task", "priority": None, "estimate": 3, "milestone": "M1", "epic": "E02", "parent": "M1-E02-S01"},
        )
        self.assertEqual(
            {key: ops["E01"][key] for key in ("level", "milestone", "epic", "parent", "estimate")},
            {"level": "epic", "milestone": None, "epic": None, "parent": None, "estimate": None},
        )

    def test_recording_every_result_converges_to_no_operations(self):
        with fixture_copy() as root:
            record_all(root)
            self.assertEqual(plan_ops(root), [
                {"op": "link", "from": "M1-E01-S02", "to": "M1-E01-S01", "from_remote_id": "r6", "to_remote_id": "r5"},
            ])
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
            self.assertEqual(run("sync-plan", "plane", "--root", root), (0, "", ""))

            run("set-status", "M1-E01-S02", "in-progress", "--root", root)
            self.assertEqual([(op["op"], op["id"], op["remote_id"], op["status"]) for op in plan_ops(root)],
                             [("update", "M1-E01-S02", "r6", "in-progress")])
            run("sync-record", "plane", "--root", root, "--id", "M1-E01-S02", "--remote-id", "r6")
            self.assertEqual(run("sync-plan", "plane", "--root", root), (0, "", ""))

    def test_forgetting_an_orphan_converges(self):
        with fixture_copy() as root:
            record_all(root)
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
            delete("backlog/M1-E01-S01-book-a-slot.md")(root)
            self.assertEqual([(op["op"], op.get("id") or (op["from"], op["to"])) for op in plan_ops(root)], [
                ("unlink", ("M1-E01-S02", "M1-E01-S01")),
                ("orphan", "M1-E01-S01"),
            ])
            self.assertEqual(run("sync-record", "plane", "--root", root, "--forget", "M1-E01-S01"),
                             (0, "forgot M1-E01-S01\n", ""))
            self.assertEqual(run("sync-plan", "plane", "--root", root), (0, "", ""))
            data = json.loads((root / ".mirage/trackers/plane.json").read_text(encoding="utf-8"))
        self.assertNotIn("M1-E01-S01", data["items"])
        self.assertEqual(data["links"], [])

    def test_operations_come_in_dependency_order(self):
        with fixture_copy() as root:
            record_all(root)
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
            delete("backlog/M2-E01-S02-reschedule.md")(root)
            edit(S02, "blocked_by: [M1-E01-S01]", "blocked_by: [M1-E02-S02]")(root)
            write("backlog/M2-E01-S03-gift-voucher.md", "---\nid: M2-E01-S03\ntitle: Gift voucher\nstatus: draft\n"
                  "priority: low\nscope: may\nrelease: v1.1\nlabels: [area:mobile]\n---\n")(root)
            ops = plan_ops(root)
        self.assertEqual([(op["op"], op.get("id") or (op["from"], op["to"])) for op in ops], [
            ("create", "M2-E01-S03"),
            ("update", "M1-E01-S02"),
            ("link", ("M1-E01-S02", "M1-E02-S02")),
            ("unlink", ("M1-E01-S02", "M1-E01-S01")),
            ("orphan", "M2-E01-S02"),
        ])
        self.assertEqual(ops[3], {"op": "unlink", "from": "M1-E01-S02", "to": "M1-E01-S01",
                                  "from_remote_id": "r6", "to_remote_id": "r5"})
        self.assertEqual(ops[4], {"op": "orphan", "id": "M2-E01-S02", "remote_id": "r11"})


class SyncRecord(unittest.TestCase):
    maxDiff = None

    def test_id_stores_remote_id_key_url_hash_and_status(self):
        with fixture_copy() as root:
            result = run("sync-record", "plane", "--root", root, "--id", "M1-E01-S02", "--remote-id", "a1b2",
                         "--key", "HL-7", "--url", "https://tracker.invalid/HL-7")
            run("sync-record", "plane", "--root", root, "--id", "M1", "--remote-id", "m1")
            text = (root / ".mirage/trackers/plane.json").read_text(encoding="utf-8")
            expected_hash = digest(root, S02)
        self.assertEqual(result, (0, "recorded M1-E01-S02 as a1b2\n", ""))
        self.assertEqual(json.loads(text), {
            "tracker": "plane",
            "items": {
                "M1": {"remote_id": "m1", "key": None, "url": None, "hash": digest(FIXTURE, "backlog/M1-booking-launch.md"),
                       "status": "in-progress"},
                "M1-E01-S02": {"remote_id": "a1b2", "key": "HL-7", "url": "https://tracker.invalid/HL-7",
                               "hash": expected_hash, "status": "ready"},
            },
            "links": [],
        })
        self.assertTrue(text.startswith('{\n  "tracker": "plane",\n  "items": {\n    "M1": {'))

    def test_recording_again_keeps_key_and_url(self):
        with fixture_copy() as root:
            run("sync-record", "plane", "--root", root, "--id", "M1", "--remote-id", "m1", "--key", "HL-1", "--url", "u")
            run("sync-record", "plane", "--root", root, "--id", "M1", "--remote-id", "m1b")
            entry = json.loads((root / ".mirage/trackers/plane.json").read_text())["items"]["M1"]
        self.assertEqual((entry["remote_id"], entry["key"], entry["url"]), ("m1b", "HL-1", "u"))

    def test_link_and_unlink_edit_the_links_list(self):
        with fixture_copy() as root:
            for item_id in ("M1-E01-S01", "M1-E01-S02", "M1-E02-S02"):
                run("sync-record", "plane", "--root", root, "--id", item_id, "--remote-id", item_id.lower())
            path = root / ".mirage/trackers/plane.json"
            run("sync-record", "plane", "--root", root, "--link", "M1-E02-S02", "M1-E01-S01")
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
            linked = json.loads(path.read_text())["links"]
            result = run("sync-record", "plane", "--root", root, "--unlink", "M1-E02-S02", "M1-E01-S01")
            unlinked = json.loads(path.read_text())["links"]
            missing = run("sync-record", "plane", "--root", root, "--unlink", "M1-E02-S02", "M1-E01-S01")
        self.assertEqual(linked, [["M1-E01-S02", "M1-E01-S01"], ["M1-E02-S02", "M1-E01-S01"]])
        self.assertEqual(result, (0, "unlinked M1-E02-S02 -> M1-E01-S01\n", ""))
        self.assertEqual(unlinked, [["M1-E01-S02", "M1-E01-S01"]])
        self.assertEqual(missing[0], 0)

    def test_link_needs_both_ends_mapped(self):
        with fixture_copy() as root:
            run("sync-record", "plane", "--root", root, "--id", "M1-E01-S02", "--remote-id", "r")
            result = run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
        self.assertEqual(result, (2, "", "error: M1-E01-S01 is not in the map; record it with --id first\n"))

    def test_unknown_item_and_missing_remote_id_are_refused(self):
        self.assertEqual(run("sync-record", "plane", "--root", FIXTURE, "--id", "M9", "--remote-id", "x"),
                         (2, "", "error: M9 has no file in backlog/\n"))
        self.assertEqual(run("sync-record", "plane", "--root", FIXTURE, "--id", "M1"),
                         (2, "", "error: --id needs --remote-id\n"))
        self.assertEqual(run("sync-record", "../escape", "--root", FIXTURE, "--id", "M1", "--remote-id", "x"),
                         (2, "", "error: tracker name '../escape' must be a lowercase slug\n"))

    def test_every_action_keeps_the_keys_it_does_not_own(self):
        settings = {"workspace": "hollow-lane", "project": "a1b2"}
        with fixture_copy() as root:
            path = root / ".mirage/trackers/plane.json"
            write(".mirage/trackers/plane.json", {"tracker": "plane", "settings": settings, "items": {}, "links": [],
                                                  "notes": ["kept"]})(root)
            write("backlog/M9-temporary.md", "---\nid: M9\ntitle: Temporary\nstatus: draft\n---\n")(root)
            for item_id in ("M1-E01-S01", "M1-E01-S02", "M9"):
                run("sync-record", "plane", "--root", root, "--id", item_id, "--remote-id", item_id.lower())
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M9")
            run("sync-record", "plane", "--root", root, "--unlink", "M1-E01-S02", "M1-E01-S01")
            delete("backlog/M9-temporary.md")(root)
            run("sync-record", "plane", "--root", root, "--forget", "M9")
            data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(list(data), ["tracker", "settings", "items", "links", "notes"])
        self.assertEqual((data["settings"], data["notes"]), (settings, ["kept"]))
        self.assertEqual(sorted(data["items"]), ["M1-E01-S01", "M1-E01-S02"])
        self.assertEqual(data["links"], [])

    def test_forget_refuses_an_item_that_still_has_a_file(self):
        with fixture_copy() as root:
            run("sync-record", "plane", "--root", root, "--id", "M1", "--remote-id", "m1")
            result = run("sync-record", "plane", "--root", root, "--forget", "M1")
            absent = run("sync-record", "plane", "--root", root, "--forget", "M7")
            items = json.loads((root / ".mirage/trackers/plane.json").read_text(encoding="utf-8"))["items"]
        self.assertEqual(result, (2, "", "error: M1 still has a backlog file; forget only orphaned items\n"))
        self.assertEqual(absent, (0, "forgot M7\n", ""))
        self.assertEqual(list(items), ["M1"])

    def test_a_failed_write_leaves_the_old_map_and_no_temporary_file(self):
        with fixture_copy() as root:
            run("sync-record", "plane", "--root", root, "--id", "M1", "--remote-id", "m1")
            folder = root / ".mirage/trackers"
            before = (folder / "plane.json").read_bytes()
            with mock.patch.object(check.os, "replace", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    run("sync-record", "plane", "--root", root, "--id", "M2", "--remote-id", "m2")
            self.assertEqual((folder / "plane.json").read_bytes(), before)
            self.assertEqual(sorted(p.name for p in folder.iterdir()), ["plane.json"])


if __name__ == "__main__":
    unittest.main()
