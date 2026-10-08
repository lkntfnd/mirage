"""Backlog rule variants beyond the one-mutation-per-code table."""

from __future__ import annotations

import unittest

from support import catalog_doc, edit, errors, facets, fixture_copy, project, synthetic_catalog, write

S02 = "backlog/M1-E01-S02-cancel-booking.md"
DRAFT = "backlog/M2-E01-S02-reschedule.md"
BLOCKED_TASK = "backlog/M1-E02-S01-T01-stock-client.md"
CANCELLED = "backlog/M1-E01-S04-reminder-sms.md"
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
MISSING = "section {} is missing; add the marker <!-- mirage:section {} --> before its heading"


def backlog_errors(root):
    return [(e["path"], e["line"], e["code"], e["message"]) for e in errors(root, "--only", "backlog")]


class Backlog(unittest.TestCase):
    maxDiff = None

    def test_done_needs_every_descendant_done_or_cancelled(self):
        with fixture_copy() as root:
            edit("backlog/E01-booking.md", "status: in-progress", "status: done\nevidence: all merged")(root)
            edit("backlog/M2-reminders.md", "status: draft", "status: done\nevidence: shipped")(root)
            edit("backlog/M1-E02-S01-check-part-stock.md", "status: in-progress", "status: done\nevidence: merged")(root)
            self.assertEqual(backlog_errors(root), [
                ("backlog/E01-booking.md", 4, "backlog-done",
                 "status is done but not every descendant is done or cancelled: M1-E01-S02, M2-E01-S01, M2-E01-S02"),
                ("backlog/M1-E02-S01-check-part-stock.md", 4, "backlog-done",
                 "status is done but not every descendant is done or cancelled: M1-E02-S01-T01"),
                ("backlog/M2-reminders.md", 4, "backlog-done",
                 "status is done but not every descendant is done or cancelled: M2-E01-S01, M2-E01-S02"),
            ])

    def test_ready_names_unmet_prerequisites_and_a_missing_requirement(self):
        with fixture_copy() as root:
            edit("backlog/M2-E01-S01-booking-reminders.md", "status: blocked", "status: ready")(root)
            edit(DRAFT, "status: draft", "status: ready")(root)
            edit(DRAFT, DRAFT_BODY, SECTIONS)(root)
            self.assertEqual(backlog_errors(root), [
                ("backlog/M2-E01-S01-booking-reminders.md", 4, "backlog-ready", "status is ready but Q-012 is open, IN-002 is missing"),
                (DRAFT, 4, "backlog-ready", "status is ready but the feature story lists no requirement"),
            ])

    def test_blockers_must_be_other_live_stories_or_tasks(self):
        with fixture_copy() as root:
            edit(DRAFT, "labels: [area:mobile]", "labels: [area:mobile]\nblocked_by: [M2-E01-S02, M1, M1-E01-S04]")(root)
            self.assertEqual(backlog_errors(root), [
                (DRAFT, 9, "backlog-ref", "M2-E01-S02 cannot block itself"),
                (DRAFT, 9, "backlog-ref", "blocked_by names M1, a milestone; blockers are stories or tasks"),
                (DRAFT, 9, "backlog-ref", "blocker M1-E01-S04 is cancelled"),
            ])

    def test_areas_and_lanes(self):
        with fixture_copy() as root:
            edit(DRAFT, "labels: [area:mobile]", "labels: [area:mobile, area:backend, area:infra]")(root)
            edit(S02, "estimate: 2", "estimate: 2\nlane: backend")(root)
            self.assertEqual(backlog_errors(root), [
                (S02, 13, "backlog-label", "lane backend is not one of the item's areas"),
                (DRAFT, 8, "backlog-label", "area:infra is not an area declared in .mirage/project.json"),
                (DRAFT, 8, "backlog-label", "several areas (mobile, backend, infra); set lane to the owning one"),
            ])

    def test_a_done_spike_has_answered_its_question(self):
        with fixture_copy() as root:
            edit("backlog/M1-E02-S02-supplier-spike.md", "questions: [Q-011]", "questions: [Q-012]")(root)
            self.assertEqual(backlog_errors(root), [
                ("backlog/M1-E02-S02-supplier-spike.md", 4, "backlog-done",
                 "status is done but the spike's outcome is not recorded: Q-012 is still open"),
            ])

    def test_kind_due_replacement_and_estimate_values(self):
        with fixture_copy() as root:
            edit("backlog/M1-E02-S02-supplier-spike.md", "questions: [Q-011]\n", "")(root)
            edit("backlog/M2-reminders.md", "status: draft", "status: draft\ndue: 2027-02-30\ndue_evidence: set by the owner")(root)
            edit("backlog/M1-E01-S04-reminder-sms.md", "status: cancelled", "status: draft")(root)
            edit(S02, "estimate: 2", "estimate: 4")(root)
            self.assertEqual(backlog_errors(root), [
                (S02, 12, "backlog-estimate", "estimate 4 must be 1, 2, 3, 5 or 8"),
                ("backlog/M1-E02-S02-supplier-spike.md", 5, "backlog-kind", "a spike story lists at least one question"),
                ("backlog/M2-E01-S01-booking-reminders.md", 13, "backlog-replace",
                 "replaces M1-E01-S04, which is draft, not cancelled"),
                ("backlog/M2-reminders.md", 5, "backlog-due", "due '2027-02-30' must be a date YYYY-MM-DD"),
            ])

    def test_keys_levels_types_and_required_fields(self):
        with fixture_copy() as root:
            edit(DRAFT, "scope: may\nrelease: v1.1", "release: v3\nreq: REQ-BOOK-002\nowner: sam")(root)
            edit("backlog/M2-reminders.md", "title: Reminders", "title: [Reminders]\npriority: high")(root)
            self.assertEqual(backlog_errors(root), [
                ("backlog/M2-E01-S02-reschedule.md", None, "backlog-field", "scope is required on a story"),
                ("backlog/M2-E01-S02-reschedule.md", 6, "backlog-field", "release 'v3' is not one of v1.0, v1.1"),
                ("backlog/M2-E01-S02-reschedule.md", 7, "backlog-field", "req must be an inline list such as [a, b]"),
                ("backlog/M2-E01-S02-reschedule.md", 8, "backlog-field", "unknown key owner"),
                ("backlog/M2-reminders.md", 3, "backlog-field", "title must be a single value, not a list"),
                ("backlog/M2-reminders.md", 4, "backlog-field", "priority is not allowed on a milestone"),
            ])

    def test_hierarchy_ids_and_duplicates(self):
        with fixture_copy() as root:
            write("backlog/M1-E01-S03-T01-orphan-task.md", "---\nid: M1-E01-S03-T01\ntitle: Orphan\nstatus: draft\n"
                  "labels: [area:backend]\n---\n")(root)
            write("backlog/M1-E05-S01-no-epic.md", "---\nid: M1-E05-S01\ntitle: No epic\nstatus: draft\npriority: low\n"
                  "scope: may\nrelease: v1.1\nlabels: [area:backend]\n---\n")(root)
            write("backlog/M1-zz-duplicate.md", "---\nid: M1\ntitle: Again\nstatus: draft\n---\n")(root)
            edit(DRAFT, "id: M2-E01-S02\n", "")(root)
            self.assertEqual(backlog_errors(root), [
                ("backlog/M1-E01-S03-T01-orphan-task.md", None, "backlog-hierarchy",
                 "task M1-E01-S03-T01 needs its story file backlog/M1-E01-S03-<slug>.md"),
                ("backlog/M1-E05-S01-no-epic.md", None, "backlog-hierarchy", "story M1-E05-S01 needs its epic file backlog/E05-<slug>.md"),
                ("backlog/M1-zz-duplicate.md", None, "backlog-id", "M1 is already used by backlog/M1-booking-launch.md"),
                (DRAFT, None, "backlog-id", "the frontmatter has no id; the file name says M2-E01-S02"),
            ])

    def test_a_cycle_is_reported_once_from_its_smallest_id(self):
        def story(number, blocked_by):
            return (f"---\nid: M1-E01-S0{number}\ntitle: Step {number}\nstatus: draft\npriority: low\nscope: may\n"
                    f"release: v1\nlabels: [area:core]\nblocked_by: [{blocked_by}]\n---\n")
        files = {
            ".mirage/project.json": facets(),
            ".mirage/catalog.json": synthetic_catalog(catalog_doc("base", "docs/base.md", "always")),
            "backlog/M1-first.md": "---\nid: M1\ntitle: First\nstatus: draft\n---\n",
            "backlog/E01-core.md": "---\nid: E01\ntitle: Core\nstatus: draft\n---\n",
            "backlog/M1-E01-S01-entry.md": story(1, "M1-E01-S03"),
            "backlog/M1-E01-S02-loop.md": story(2, "M1-E01-S03"),
            "backlog/M1-E01-S03-loop.md": story(3, "M1-E01-S04"),
            "backlog/M1-E01-S04-loop.md": story(4, "M1-E01-S02"),
        }
        with project(files) as root:
            self.assertEqual(backlog_errors(root), [
                ("backlog/M1-E01-S02-loop.md", 9, "backlog-cycle",
                 "blocked_by cycle: M1-E01-S02 -> M1-E01-S03 -> M1-E01-S04 -> M1-E01-S02"),
            ])


def bare_body(rel: str, status: str, extra: str = ""):
    """Give an item a new status and a body without any section markers."""
    def apply(root):
        path = root / rel
        head = path.read_text(encoding="utf-8").split("\n---\n", 1)[0].replace("status: ready", f"status: {status}")
        path.write_text(f"{head}\n{extra}---\n\nOnly a first idea so far.\n", encoding="utf-8")
    return apply


class BodySections(unittest.TestCase):
    maxDiff = None

    def test_the_fixture_has_draft_blocked_and_cancelled_items_without_sections(self):
        with fixture_copy() as root:
            for rel, status in ((DRAFT, "draft"), (BLOCKED_TASK, "blocked"), (CANCELLED, "cancelled")):
                text = (root / rel).read_text(encoding="utf-8")
                self.assertIn(f"\nstatus: {status}\n", text)
                self.assertNotIn("mirage:section", text)
            self.assertEqual(backlog_errors(root), [])

    def test_draft_blocked_and_cancelled_items_may_omit_sections(self):
        for status, extra in (("draft", ""), ("blocked", "blocked_reason: Waiting for the owner.\n"), ("cancelled", "")):
            with self.subTest(status=status), fixture_copy() as root:
                bare_body(S02, status, extra)(root)
                self.assertEqual(backlog_errors(root), [])

    def test_ready_in_progress_in_review_and_done_need_every_required_section(self):
        missing = [
            (S02, None, "backlog-section", MISSING.format(key, key))
            for key in ("acceptance", "context", "out-of-scope", "verification")
        ]
        for status, extra in (("ready", ""), ("in-progress", ""), ("in-review", ""), ("done", "evidence: merge 1a2b3c4\n")):
            with self.subTest(status=status), fixture_copy() as root:
                bare_body(S02, status, extra)(root)
                self.assertEqual(backlog_errors(root), missing)

    def test_a_ready_task_needs_the_sections_too(self):
        with fixture_copy() as root:
            edit(BLOCKED_TASK, "status: blocked", "status: ready")(root)
            self.assertEqual(backlog_errors(root), [
                (BLOCKED_TASK, None, "backlog-section", MISSING.format(key, key))
                for key in ("acceptance", "context", "out-of-scope", "verification")
            ])

    def test_an_empty_section_is_reported_at_its_marker(self):
        with fixture_copy() as root:
            edit(S02, "API test T-BOOK-03 and the cancel flow in the app test suite.\n\n", "")(root)
            self.assertEqual(backlog_errors(root), [
                (S02, 26, "backlog-section", "section verification is empty; write at least one line after its heading"),
            ])

    def test_a_section_holding_only_a_code_block_is_not_empty(self):
        with fixture_copy() as root:
            edit(S02, "API test T-BOOK-03 and the cancel flow in the app test suite.\n", "```\npytest tests/cancel\n```\n")(root)
            self.assertEqual(backlog_errors(root), [])

    def test_a_checklist_outside_the_acceptance_section_does_not_count(self):
        with fixture_copy() as root:
            edit(S02, "- [ ] A customer cancels up to two hours before the slot.\n- [ ] A later cancellation is refused with a reason.\n",
                 "A customer cancels up to two hours before the slot.\n")(root)
            edit(S02, "Refunds; the app takes no payments.", "- [ ] Refunds; the app takes no payments.")(root)
            self.assertEqual(backlog_errors(root), [
                (S02, 20, "backlog-section", "section acceptance has no checklist item"),
            ])

    def test_a_missing_checklist_is_a_section_problem_and_never_also_a_ready_problem(self):
        with fixture_copy() as root:
            edit(S02, "- [ ] A customer cancels up to two hours before the slot.\n- [ ] A later cancellation is refused with a reason.\n",
                 "A customer cancels up to two hours before the slot.\n")(root)
            self.assertEqual([(e["code"], e["line"]) for e in errors(root)], [("backlog-section", 20)])

    def test_a_marker_must_sit_directly_before_a_heading(self):
        with fixture_copy() as root:
            edit(S02, "<!-- mirage:section context -->\n## Context\n", "<!-- mirage:section context -->\nWhy.\n## Context\n")(root)
            self.assertEqual(backlog_errors(root), [
                (S02, 15, "backlog-section", "section marker context must sit directly before its heading"),
            ])

    def test_markers_inside_a_code_block_are_not_markers(self):
        with fixture_copy() as root:
            edit(S02, "<!-- mirage:section context -->\n## Context\n", "```\n<!-- mirage:section context -->\n```\n## Context\n")(root)
            self.assertEqual(backlog_errors(root), [(S02, None, "backlog-section", MISSING.format("context", "context"))])

    def test_the_technical_section_is_optional_and_may_be_empty_but_needs_a_heading(self):
        with fixture_copy() as root:
            edit(S02, "<!-- mirage:section verification -->\n",
                 "<!-- mirage:section technical -->\n## Technical notes\n\n<!-- mirage:section verification -->\n")(root)
            self.assertEqual(backlog_errors(root), [])
        with fixture_copy() as root:
            edit(S02, "<!-- mirage:section verification -->\n",
                 "<!-- mirage:section technical -->\nNotes without a heading.\n\n<!-- mirage:section verification -->\n")(root)
            self.assertEqual(backlog_errors(root), [
                (S02, 26, "backlog-section", "section marker technical must sit directly before its heading"),
            ])

    def test_milestones_and_epics_have_no_sections_but_a_ready_one_needs_a_checklist_item(self):
        with fixture_copy() as root:
            edit("backlog/M1-booking-launch.md", "status: in-progress", "status: ready")(root)
            self.assertEqual(backlog_errors(root), [])
            edit("backlog/M2-reminders.md", "status: draft", "status: ready")(root)
            edit("backlog/E02-parts.md", "status: in-progress", "status: ready")(root)
            self.assertEqual(backlog_errors(root), [
                ("backlog/E02-parts.md", 4, "backlog-ready", "status is ready but the body has no checklist item"),
                ("backlog/M2-reminders.md", 4, "backlog-ready", "status is ready but the body has no checklist item"),
            ])


if __name__ == "__main__":
    unittest.main()
