"""ready, index, set-status, sync-plan and sync-record."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from typing import List
from unittest import mock

from support import (
    FIXTURE, append, catalog_doc, check, delete, edit, edit_json, facets, fixture_copy, project, run,
    synthetic_catalog, write,
)

S02 = "backlog/M1-E01-S02-cancel-booking.md"
DRAFT = "backlog/M2-E01-S02-reschedule.md"
DRAFT_ID = "M2-E01-S02"
BLOCKED_TASK = "backlog/M1-E02-S01-T01-stock-client.md"
FAKE_AWS_KEY = "AKIA" + "Q" * 16
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

<!-- mirage:section context -->
## Context

A customer who cannot come frees the slot for someone else (REQ-BOOK-002).

<!-- mirage:section acceptance -->
## Acceptance criteria

- [ ] A customer cancels up to two hours before the slot.
- [ ] A later cancellation is refused with a reason.

<!-- mirage:section verification -->
## Verification

API test T-BOOK-03 and the cancel flow in the app test suite.

<!-- mirage:section out-of-scope -->
## Out of scope

Refunds; the app takes no payments.
"""
DRAFT_LABELS = "labels: [area:mobile]"
DRAFT_REQ = "\nreq: [REQ-BOOK-002]"
DRAFT_BODY = "## Acceptance criteria\n\n- [ ] A customer moves a booking to a free slot.\n"
SECTIONS = """<!-- mirage:section context -->
## Context

Why the item exists.

<!-- mirage:section acceptance -->
## Acceptance criteria

- [ ] A customer moves a booking to a free slot.

<!-- mirage:section verification -->
## Verification

A test proves it.

<!-- mirage:section out-of-scope -->
## Out of scope

Nothing is excluded.
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
        # M2-E01-S02 has its prerequisites met but no body sections yet, so it cannot become ready.
        self.assertEqual(ready_json(FIXTURE), [
            {"lane": "mobile",
             "ready_now": [{"id": "M1-E01-S02", "title": "Cancel a booking", "status": "ready"}],
             "can_become_ready": [],
             "wrongly_ready": []},
        ])

    def test_text_output(self):
        self.assertEqual(run("ready", "--root", FIXTURE), (0, (
            "lane mobile\n"
            "  ready now\n"
            "    M1-E01-S02 Cancel a booking\n"
            "  can become ready\n"
            "    none\n"
            "  wrongly ready\n"
            "    none\n"
        ), ""))

    def test_a_blocked_reason_keeps_an_item_out_of_can_become_ready(self):
        with fixture_copy() as root:
            edit(BLOCKED_TASK,
                 "\nblocked_reason: Waiting for Sprocket Supply to enable the stock endpoint in the sandbox.", "")(root)
            edit(BLOCKED_TASK, "- [ ] Client with timeouts and retries.\n", SECTIONS)(root)
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

    def test_can_become_ready_needs_every_required_section_complete(self):
        listed = [{"id": "M2-E01-S02", "title": "Move a booking to another slot", "status": "draft"}]
        with fixture_copy() as root:
            edit(DRAFT, DRAFT_LABELS, DRAFT_LABELS + DRAFT_REQ)(root)
            edit(DRAFT, DRAFT_BODY, SECTIONS)(root)
            self.assertEqual(lane(root, "mobile")["can_become_ready"], listed)
        with fixture_copy() as root:
            edit(DRAFT, DRAFT_LABELS, DRAFT_LABELS + DRAFT_REQ)(root)
            edit(DRAFT, DRAFT_BODY, SECTIONS.replace("A test proves it.\n\n", ""))(root)
            self.assertEqual(lane(root, "mobile")["can_become_ready"], [])
        with fixture_copy() as root:
            edit(DRAFT, DRAFT_LABELS, DRAFT_LABELS + DRAFT_REQ)(root)
            edit(DRAFT, DRAFT_BODY, SECTIONS.replace("- [ ] A customer moves", "A customer moves"))(root)
            self.assertEqual(lane(root, "mobile")["can_become_ready"], [])
        with fixture_copy() as root:
            edit(DRAFT, DRAFT_LABELS, DRAFT_LABELS + DRAFT_REQ)(root)
            edit(DRAFT, DRAFT_BODY, SECTIONS.replace("<!-- mirage:section out-of-scope -->\n", ""))(root)
            self.assertEqual(lane(root, "mobile")["can_become_ready"], [])

    def test_a_feature_story_needs_a_requirement_to_become_ready(self):
        listed = [{"id": "M2-E01-S02", "title": "Move a booking to another slot", "status": "draft"}]
        with fixture_copy() as root:
            edit(DRAFT, DRAFT_BODY, SECTIONS)(root)
            self.assertEqual(lane(root, "mobile")["can_become_ready"], [])
        # A chore story proves no requirement, so it needs none.
        with fixture_copy() as root:
            edit(DRAFT, DRAFT_LABELS, DRAFT_LABELS + "\nkind: chore")(root)
            edit(DRAFT, DRAFT_BODY, SECTIONS)(root)
            self.assertEqual(lane(root, "mobile")["can_become_ready"], listed)

    def test_a_spike_can_start_on_the_open_question_it_answers(self):
        listed = [{"id": "M2-E01-S02", "title": "Move a booking to another slot", "status": "draft"}]
        with fixture_copy() as root:
            edit(DRAFT, DRAFT_LABELS, DRAFT_LABELS + "\nkind: spike\nquestions: [Q-012]")(root)
            edit(DRAFT, DRAFT_BODY, SECTIONS)(root)
            self.assertEqual(lane(root, "mobile")["can_become_ready"], listed)
            edit(DRAFT, "status: draft", "status: ready")(root)
            self.assertEqual(lane(root, "mobile")["wrongly_ready"], [])
            self.assertEqual(run("check", "--root", root, "--only", "backlog"), (0, "ok\n", ""))

    def test_unmet_prerequisites_keep_an_item_with_complete_sections_out_of_can_become_ready(self):
        with fixture_copy() as root:
            edit(DRAFT, DRAFT_BODY, SECTIONS)(root)
            edit(DRAFT, DRAFT_LABELS, DRAFT_LABELS + DRAFT_REQ + "\nquestions: [Q-012]")(root)
            self.assertEqual(lane(root, "mobile")["can_become_ready"], [])

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
| M1-E01-S01 | Print | blocked | core | Q-001 |
| M1-E01-S01-T01 | Driver | draft | core | M1-E01-S01, Q-001 |

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
        self.assertEqual(stale, (1, "docs/README.md:61: index-stale: the generated file differs from what index writes; run index\n1 error\n", ""))
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

    def test_several_items_change_in_one_call(self):
        with fixture_copy() as root:
            result = run("set-status", "M1-E01-S02", DRAFT_ID, "M1-E01-S02", "blocked", "--root", root)
            texts = [(root / path).read_text(encoding="utf-8") for path in (S02, DRAFT)]
        self.assertEqual(result, (0, "M1-E01-S02: ready -> blocked\nM2-E01-S02: draft -> blocked\n", ""))
        self.assertEqual([text.split("\n")[3] for text in texts], ["status: blocked", "status: blocked"])

    def test_one_refused_item_leaves_every_item_unchanged(self):
        with fixture_copy() as root:
            result = run("set-status", "M1-E01-S02", "M9-E01-S01", "blocked", "--root", root)
            text = (root / S02).read_text(encoding="utf-8")
        self.assertEqual(result, (2, "", "error: M9-E01-S01 has no file in backlog/\n"))
        self.assertEqual(text, S02_TEXT)

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


def payload_hash(op: dict) -> str:
    """The contract's hash, computed here on its own: SHA-256 of the canonical JSON of the payload fields."""
    fields = {key: value for key, value in op.items() if key not in ("op", "hash", "remote_id")}
    text = json.dumps(fields, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def expect_ops(root: Path, tracker: str = "plane") -> List[dict]:
    code, out, err = run("sync-expect", tracker, "--root", root)
    assert code == 0, err
    return [json.loads(line) for line in out.splitlines()]


def plan_hashes(root: Path) -> dict:
    return {op["id"]: op["hash"] for op in plan_ops(root) if op["op"] == "create"}


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

    def test_a_story_create_carries_the_item_fields(self):
        ops = {op["id"]: op for op in plan_ops(FIXTURE)}
        story = ops["M1-E01-S02"]
        self.assertEqual(story, {
            "op": "create",
            "id": "M1-E01-S02",
            "level": "story",
            "title": "M1-E01-S02 Cancel a booking",
            "status": "ready",
            "priority": "medium",
            "labels": ["area:mobile", "type:feature", "scope:should", "release:v1.0"],
            "estimate": 2,
            "due": None,
            "milestone": "M1",
            "epic": "E01",
            "parent": "E01",
            "body": "## Context\n\nA customer who cannot come frees the slot for someone else (REQ-BOOK-002).\n\n"
                    "## Acceptance criteria\n\n- [ ] A customer cancels up to two hours before the slot.\n"
                    "- [ ] A later cancellation is refused with a reason.\n\n"
                    "## Verification\n\nAPI test T-BOOK-03 and the cancel flow in the app test suite.\n\n"
                    "## Out of scope\n\nRefunds; the app takes no payments.\n\n"
                    "---\nRequirements: REQ-BOOK-002\nQuestions: Q-007\nBlocked by: M1-E01-S01\nmirage-id: M1-E01-S02",
            "hash": payload_hash(story),
        })

    def test_a_task_create_takes_the_scope_and_release_of_its_story(self):
        task = {op["id"]: op for op in plan_ops(FIXTURE)}["M1-E01-S01-T01"]
        self.assertEqual(task, {
            "op": "create",
            "id": "M1-E01-S01-T01",
            "level": "task",
            "title": "M1-E01-S01-T01 Slot and booking endpoints",
            "status": "done",
            "priority": None,
            "labels": ["area:backend", "scope:must", "release:v1.0"],
            "estimate": 3,
            "due": None,
            "milestone": "M1",
            "epic": "E01",
            "parent": "M1-E01-S01",
            "body": "## Context\n\nThe server side of the booking story.\n\n"
                    "## Acceptance criteria\n\n- [x] Slots endpoint.\n- [x] Booking endpoint with an idempotency key.\n\n"
                    "## Verification\n\nAPI tests T-BOOK-01 and T-BOOK-02.\n\n"
                    "## Out of scope\n\nCancelling a booking.\n\n"
                    "---\nEvidence: merge 9a3d2f1, CI run 198 green\nmirage-id: M1-E01-S01-T01",
            "hash": payload_hash(task),
        })

    def test_a_milestone_create_carries_its_due_date_and_no_derived_labels(self):
        milestone = {op["id"]: op for op in plan_ops(FIXTURE)}["M1"]
        self.assertEqual(milestone, {
            "op": "create",
            "id": "M1",
            "level": "milestone",
            "title": "M1 Booking launch",
            "status": "in-progress",
            "priority": None,
            "labels": [],
            "estimate": None,
            "due": "2026-11-02",
            "milestone": None,
            "epic": None,
            "parent": None,
            "body": "Booking and stock checks for the first release.\n\n- [ ] Every v1.0 story is done.\n\n---\nmirage-id: M1",
            "hash": payload_hash(milestone),
        })

    def test_every_hash_is_the_sha256_of_the_canonical_payload(self):
        ops = plan_ops(FIXTURE)
        self.assertEqual(len(ops), len(ALL_IDS))
        for op in ops:
            with self.subTest(id=op["id"]):
                self.assertEqual(op["hash"], payload_hash(op))
        self.assertEqual(len({op["hash"] for op in ops}), len(ops))

    def test_the_footer_lists_the_non_empty_fields_in_order_and_markers_are_stripped(self):
        with fixture_copy() as root:
            edit(S02, "estimate: 2", "estimate: 2\ninputs: [IN-001]\nevidence: spec reviewed")(root)
            write("backlog/M1-E01-S03-fenced.md", "---\nid: M1-E01-S03\ntitle: Fenced\nstatus: draft\npriority: low\n"
                  "scope: may\nrelease: v1.1\nlabels: [area:mobile]\n---\n\n  <!-- mirage:section context -->  \n"
                  "Text <!-- mirage:section context --> stays.\n<!-- not mirage -->\n")(root)
            ops = {op["id"]: op for op in plan_ops(root)}
        self.assertTrue(ops["M1-E01-S02"]["body"].endswith(
            "\n\n---\nRequirements: REQ-BOOK-002\nQuestions: Q-007\nInputs: IN-001\nBlocked by: M1-E01-S01\n"
            "Evidence: spec reviewed\nmirage-id: M1-E01-S02"))
        self.assertEqual(ops["M1-E01-S03"]["body"],
                         "Text <!-- mirage:section context --> stays.\n<!-- not mirage -->\n\n---\nmirage-id: M1-E01-S03")
        self.assertEqual(ops["M1-E01-S03"]["labels"], ["area:mobile", "type:feature", "scope:may", "release:v1.1"])

    def test_a_spike_story_labels_use_its_kind(self):
        ops = {op["id"]: op for op in plan_ops(FIXTURE)}
        self.assertEqual(ops["M1-E02-S02"]["labels"], ["area:backend", "type:spike", "scope:must", "release:v1.0"])

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

    def test_changing_only_a_story_release_updates_the_story_and_each_of_its_tasks(self):
        with fixture_copy() as root:
            record_all(root)
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
            edit("backlog/M1-E01-S01-book-a-slot.md", "release: v1.0", "release: v1.1")(root)
            ops = plan_ops(root)
            self.assertEqual([(op["op"], op["id"], op["remote_id"], op["labels"]) for op in ops], [
                ("update", "M1-E01-S01", "r5", ["area:mobile", "area:backend", "type:feature", "scope:must", "release:v1.1"]),
                ("update", "M1-E01-S01-T01", "r12", ["area:backend", "scope:must", "release:v1.1"]),
                ("update", "M1-E01-S01-T02", "r13", ["area:mobile", "scope:must", "release:v1.1"]),
            ])
            for op in ops:
                run("sync-record", "plane", "--root", root, "--id", op["id"], "--remote-id", op["remote_id"])
            self.assertEqual(run("sync-plan", "plane", "--root", root), (0, "", ""))

    def test_changing_only_a_milestone_due_date_updates_the_milestone(self):
        with fixture_copy() as root:
            record_all(root)
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
            edit("backlog/M1-booking-launch.md", "due: 2026-11-02", "due: 2026-11-09")(root)
            ops = plan_ops(root)
        self.assertEqual([(op["op"], op["id"], op["due"], op["remote_id"]) for op in ops], [("update", "M1", "2026-11-09", "r1")])

    def test_forgetting_an_orphan_converges(self):
        with fixture_copy() as root:
            record_all(root)
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
            for rel in ("book-a-slot", "T01-slot-api", "T02-slot-screen"):
                delete(f"backlog/M1-E01-S01-{rel}.md")(root)
            self.assertEqual([(op["op"], op.get("id") or (op["from"], op["to"])) for op in plan_ops(root)], [
                ("unlink", ("M1-E01-S02", "M1-E01-S01")),
                ("orphan", "M1-E01-S01"),
                ("orphan", "M1-E01-S01-T01"),
                ("orphan", "M1-E01-S01-T02"),
            ])
            self.assertEqual(run("sync-record", "plane", "--root", root, "--forget", "M1-E01-S01"),
                             (0, "forgot M1-E01-S01\n", ""))
            run("sync-record", "plane", "--root", root, "--forget", "M1-E01-S01-T01")
            run("sync-record", "plane", "--root", root, "--forget", "M1-E01-S01-T02")
            self.assertEqual(run("sync-plan", "plane", "--root", root), (0, "", ""))
            data = json.loads((root / ".mirage/trackers/plane.json").read_text(encoding="utf-8"))
        self.assertEqual(sorted(data["items"], key=ALL_IDS.index), [i for i in ALL_IDS if not i.startswith("M1-E01-S01")])
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
            hashes = plan_hashes(FIXTURE)
        self.assertEqual(result, (0, "recorded M1-E01-S02 as a1b2\n", ""))
        self.assertEqual(json.loads(text), {
            "tracker": "plane",
            "items": {
                "M1": {"remote_id": "m1", "key": None, "url": None, "hash": hashes["M1"], "status": "in-progress"},
                "M1-E01-S02": {"remote_id": "a1b2", "key": "HL-7", "url": "https://tracker.invalid/HL-7",
                               "hash": hashes["M1-E01-S02"], "status": "ready"},
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


OPEN_Q012 = "open: Q-012 Which reminders does the app send? (blocks: M2-E01-S01, REQ-NOTE-001)\n"
PLACEHOLDER = "docs/security.md:33: doc-placeholder: the line holds a {{ placeholder; write the content or cite a question\n"
MISSING_PERFORMANCE = ("docs/performance.md: doc-missing: Performance (performance) is missing; "
                       "it is planned because components include mobile-app, backend-service\n")


def docs_ready_json(root: Path) -> tuple:
    code, out, _ = run("docs-ready", "--root", root, "--json")
    return code, json.loads(out)


def all_requirements_out(root: Path) -> None:
    path = root / "docs/prd.md"
    text = path.read_text(encoding="utf-8")
    for scope in ("MUST", "SHOULD", "MAY"):
        text = text.replace(f"| {scope} |", "| OUT |")
    path.write_text(text, encoding="utf-8")


class DocsReady(unittest.TestCase):
    maxDiff = None

    def test_the_fixture_is_sufficient_and_lists_its_open_question(self):
        self.assertEqual(run("docs-ready", "--root", FIXTURE), (0, "sufficient\n" + OPEN_Q012, ""))

    def test_json_shape(self):
        self.assertEqual(docs_ready_json(FIXTURE), (0, {
            "sufficient": True,
            "errors": [],
            "open_questions": [
                {"id": "Q-012", "title": "Which reminders does the app send?", "blocks": ["M2-E01-S01", "REQ-NOTE-001"]},
            ],
        }))

    def test_json_shape_when_not_sufficient(self):
        with fixture_copy() as root:
            append("docs/security.md", "Escalation contact: {{contact}}\n")(root)
            all_requirements_out(root)
            result = docs_ready_json(root)
        self.assertEqual(result, (1, {
            "sufficient": False,
            "errors": [
                {"path": "docs/prd.md", "line": None, "code": "prd-empty", "message": "no requirement is in scope"},
                {"path": "docs/security.md", "line": 33, "code": "doc-placeholder",
                 "message": "the line holds a {{ placeholder; write the content or cite a question"},
            ],
            "open_questions": [
                {"id": "Q-012", "title": "Which reminders does the app send?", "blocks": ["M2-E01-S01", "REQ-NOTE-001"]},
            ],
        }))

    def test_a_removed_planned_document_is_reported(self):
        with fixture_copy() as root:
            delete("docs/performance.md")(root)
            result = run("docs-ready", "--root", root)
        self.assertEqual(result, (1, MISSING_PERFORMANCE + "not sufficient: 1 problem\n" + OPEN_Q012, ""))

    def test_a_placeholder_is_reported(self):
        with fixture_copy() as root:
            append("docs/security.md", "Escalation contact: {{contact}}\n")(root)
            result = run("docs-ready", "--root", root)
        self.assertEqual(result, (1, PLACEHOLDER + "not sufficient: 1 problem\n" + OPEN_Q012, ""))

    def test_an_uncovered_area_is_reported(self):
        with fixture_copy() as root:
            edit("docs/questions.md", "notifications/caps, ", "")(root)
            result = run("docs-ready", "--root", root)
        self.assertEqual(result, (1, (
            "docs/questions.md: coverage-area: no question covers notifications/caps: "
            "How many messages a user may receive per day or week.\n"
            "not sufficient: 1 problem\n" + OPEN_Q012
        ), ""))

    def test_a_prd_whose_only_requirements_are_out_of_scope_is_empty(self):
        with fixture_copy() as root:
            all_requirements_out(root)
            result = run("docs-ready", "--root", root)
            plain = run("check", "--root", root)
        self.assertEqual(result, (1, "docs/prd.md: prd-empty: no requirement is in scope\n"
                                     "not sufficient: 1 problem\n" + OPEN_Q012, ""))
        self.assertEqual(plain, (0, "ok\n", ""))  # check never reports prd-empty

    def test_an_audit_log_without_a_documents_entry_is_not_an_audit(self):
        entry = "## 2026-09-25 Documents\n"
        for heading in ("No audit has been run yet.\n", "## 2026-09-25 Backlog\n", "## Documents\n"):
            with fixture_copy() as root:
                edit("docs/audit-log.md", entry, heading)(root)
                result = run("docs-ready", "--root", root)
                plain = run("check", "--root", root)
            self.assertEqual(result, (1, "docs/audit-log.md: audit-missing: no documents audit is recorded; run mirage-audit\n"
                                         "not sufficient: 1 problem\n" + OPEN_Q012, ""), heading)
            self.assertEqual(plain, (0, "ok\n", ""))  # check never reports audit-missing
        with fixture_copy() as root:
            edit("docs/audit-log.md", entry, "## 2026-09-25 Documents and backlog\n")(root)
            self.assertEqual(run("docs-ready", "--root", root), (0, "sufficient\n" + OPEN_Q012, ""))

    def test_a_prd_without_any_requirement_row_is_empty(self):
        with fixture_copy() as root:
            path = root / "docs/prd.md"
            lines = path.read_text(encoding="utf-8").split("\n")
            path.write_text("\n".join(line for line in lines if not line.startswith("| REQ-") and not line.startswith("| `REQ-")),
                            encoding="utf-8")
            result = run("docs-ready", "--root", root)
        self.assertEqual(result[0], 1)
        self.assertIn("docs/prd.md: prd-empty: no requirement is in scope\n", result[1])

    def test_problems_are_counted_and_sorted_by_path(self):
        with fixture_copy() as root:
            delete("docs/performance.md")(root)
            append("docs/security.md", "Escalation contact: {{contact}}\n")(root)
            result = run("docs-ready", "--root", root)
        self.assertEqual(result, (1, MISSING_PERFORMANCE + PLACEHOLDER + "not sufficient: 2 problems\n" + OPEN_Q012, ""))

    def test_open_questions_never_change_the_exit_code_and_show_an_empty_blocks_field_as_nothing(self):
        with fixture_copy() as root:
            edit("docs/questions.md", "### Q-004 How is the product tested?\n\n- Status: answered",
                 "### Q-004 How is the product tested?\n\n- Status: open")(root)
            text = run("docs-ready", "--root", root)
            code, data = docs_ready_json(root)
        self.assertEqual(text, (0, "sufficient\nopen: Q-004 How is the product tested? (blocks: nothing)\n" + OPEN_Q012, ""))
        self.assertEqual((code, [q["blocks"] for q in data["open_questions"]]), (0, [[], ["M2-E01-S01", "REQ-NOTE-001"]]))

    def test_nothing_after_the_verdict_when_no_question_is_open(self):
        with fixture_copy() as root:
            edit("docs/questions.md", "- Status: open", "- Status: answered\n- Answer: Dropped. Answered on 2026-09-25.")(root)
            self.assertEqual(run("docs-ready", "--root", root), (0, "sufficient\n", ""))

    def test_a_broken_backlog_does_not_change_the_output(self):
        with fixture_copy() as root:
            before = run("docs-ready", "--root", root)
            edit(DRAFT, "labels: [area:mobile]", "labels: [area:mobile]\nblocked_by: [M9-E01-S09]")(root)
            append(DRAFT, f"Needs Q-404, see [notes](missing.md). Key: {FAKE_AWS_KEY}\n")(root)
            write("backlog/notes.md", "Loose notes.\n")(root)
            edit("docs/prd.md", "| MUST | v1.1 |", "| MUST | v1.0 |")(root)
            append("backlog/README.md", "Hand-edited note.\n")(root)
            edit("backlog/M1-E01-S02-cancel-booking.md", "questions: [Q-007]", "questions: [Q-012]")(root)
            after = run("docs-ready", "--root", root)
            problems = {e["code"] for e in json.loads(run("check", "--root", root, "--json")[1])["errors"]}
        self.assertEqual(before, (0, "sufficient\n" + OPEN_Q012, ""))
        # The verdict holds. The open question now also names the story that was made to list it.
        self.assertEqual(after, (0, "sufficient\n" + OPEN_Q012.replace("REQ-NOTE-001)", "REQ-NOTE-001, M1-E01-S02)"), ""))
        self.assertEqual(problems, {"backlog-filename", "backlog-ref", "coverage-req", "index-stale", "link-broken",
                                    "ref-missing", "backlog-ready", "secret"})

    def test_an_unreadable_project_is_a_usage_error(self):
        with fixture_copy() as root:
            write(".mirage/project.json", "{not json")(root)
            code, out, err = run("docs-ready", "--root", root)
        self.assertEqual((code, out), (2, ""))
        self.assertTrue(err.startswith("error: cannot read .mirage/project.json:"), err)


class SyncExpect(unittest.TestCase):
    maxDiff = None

    SORTED_IDS = [
        "E01", "E02", "M1", "M1-E01-S01", "M1-E01-S01-T01", "M1-E01-S01-T02", "M1-E01-S02", "M1-E01-S04",
        "M1-E02-S01", "M1-E02-S01-T01", "M1-E02-S02", "M2", "M2-E01-S01", "M2-E01-S02",
    ]

    def test_a_missing_or_empty_map_prints_nothing(self):
        with fixture_copy() as root:
            self.assertEqual(run("sync-expect", "plane", "--root", root), (0, "", ""))
            write(".mirage/trackers/plane.json", {"tracker": "plane", "items": {}, "links": []})(root)
            self.assertEqual(run("sync-expect", "plane", "--root", root), (0, "", ""))

    def test_every_recorded_item_is_expected_exactly_as_it_was_pushed(self):
        with fixture_copy() as root:
            created = {op["id"]: op for op in plan_ops(root)}
            record_all(root)
            expected = expect_ops(root)
        self.assertEqual([op["id"] for op in expected], self.SORTED_IDS)
        remote = {item_id: f"r{number}" for number, item_id in enumerate(ALL_IDS, 1)}
        for op in expected:
            with self.subTest(id=op["id"]):
                self.assertEqual(op, {**created[op["id"]], "op": "expect", "remote_id": remote[op["id"]]})

    def test_a_story_is_printed_with_its_literal_payload(self):
        with fixture_copy() as root:
            record_all(root)
            story = next(op for op in expect_ops(root) if op["id"] == "M1-E01-S02")
        self.assertEqual(story, {
            "op": "expect",
            "id": "M1-E01-S02",
            "level": "story",
            "title": "M1-E01-S02 Cancel a booking",
            "status": "ready",
            "priority": "medium",
            "labels": ["area:mobile", "type:feature", "scope:should", "release:v1.0"],
            "estimate": 2,
            "due": None,
            "milestone": "M1",
            "epic": "E01",
            "parent": "E01",
            "body": "## Context\n\nA customer who cannot come frees the slot for someone else (REQ-BOOK-002).\n\n"
                    "## Acceptance criteria\n\n- [ ] A customer cancels up to two hours before the slot.\n"
                    "- [ ] A later cancellation is refused with a reason.\n\n"
                    "## Verification\n\nAPI test T-BOOK-03 and the cancel flow in the app test suite.\n\n"
                    "## Out of scope\n\nRefunds; the app takes no payments.\n\n"
                    "---\nRequirements: REQ-BOOK-002\nQuestions: Q-007\nBlocked by: M1-E01-S01\nmirage-id: M1-E01-S02",
            "hash": payload_hash(story),
            "remote_id": "r6",
        })

    def test_only_recorded_items_are_printed(self):
        with fixture_copy() as root:
            for item_id in ("M1-E01-S02", "M1"):
                run("sync-record", "plane", "--root", root, "--id", item_id, "--remote-id", item_id.lower())
            self.assertEqual([(op["id"], op["remote_id"]) for op in expect_ops(root)], [("M1", "m1"), ("M1-E01-S02", "m1-e01-s02")])

    def test_an_edited_item_leaves_the_output_and_appears_as_an_update(self):
        with fixture_copy() as root:
            record_all(root)
            run("sync-record", "plane", "--root", root, "--link", "M1-E01-S02", "M1-E01-S01")
            edit(S02, "title: Cancel a booking", "title: Cancel a booked slot")(root)
            ids = [op["id"] for op in expect_ops(root)]
            plan = plan_ops(root)
        self.assertEqual(ids, [i for i in self.SORTED_IDS if i != "M1-E01-S02"])
        self.assertEqual([(op["op"], op["id"], op["title"], op["remote_id"]) for op in plan],
                         [("update", "M1-E01-S02", "M1-E01-S02 Cancel a booked slot", "r6")])

    def test_a_task_leaves_the_output_when_its_story_release_changes(self):
        with fixture_copy() as root:
            record_all(root)
            edit("backlog/M1-E01-S01-book-a-slot.md", "release: v1.0", "release: v1.1")(root)
            ids = [op["id"] for op in expect_ops(root)]
        self.assertEqual(ids, [i for i in self.SORTED_IDS if not i.startswith("M1-E01-S01")])

    def test_an_item_whose_file_is_gone_is_not_printed(self):
        with fixture_copy() as root:
            record_all(root)
            delete("backlog/M2-E01-S02-reschedule.md")(root)
            ids = [op["id"] for op in expect_ops(root)]
        self.assertEqual(ids, [i for i in self.SORTED_IDS if i != "M2-E01-S02"])

    def test_recording_an_item_again_brings_it_back(self):
        with fixture_copy() as root:
            record_all(root)
            edit(S02, "title: Cancel a booking", "title: Cancel a booked slot")(root)
            run("sync-record", "plane", "--root", root, "--id", "M1-E01-S02", "--remote-id", "r6")
            story = next(op for op in expect_ops(root) if op["id"] == "M1-E01-S02")
        self.assertEqual((story["title"], story["remote_id"]), ("M1-E01-S02 Cancel a booked slot", "r6"))

    def test_an_unreadable_map_is_a_usage_error(self):
        with fixture_copy() as root:
            write(".mirage/trackers/plane.json", "{not json")(root)
            code, out, err = run("sync-expect", "plane", "--root", root)
        self.assertEqual((code, out), (2, ""))
        self.assertTrue(err.startswith("error: cannot read .mirage/trackers/plane.json:"), err)


if __name__ == "__main__":
    unittest.main()
