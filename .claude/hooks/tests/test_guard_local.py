import json
import unittest

from _helpers import TempRepoCase

import guard_local

PLAN = """# Plan

## 7. Checklist to do
> Summary

- [x] T1. first
- [ ] T2. second
- [ ] T3. third

## 8. Acceptance criteria
1. something
"""


class GuardLocalTest(TempRepoCase):
    def decide(self, tool, **tool_input):
        payload = {"tool_name": tool, "tool_input": tool_input, "cwd": self.root}
        return guard_local.decide(payload, self.root)[0]

    # --- design_system -----------------------------------------------------
    def test_write_design_system_is_denied(self):
        self.assertEqual(self.decide("Write", file_path=self.path(".local", "design_system", "x.md"), content="x"), "deny")

    def test_edit_design_system_relative_path_is_denied(self):
        self.assertEqual(self.decide("Edit", file_path=".local/design_system/spec.md", old_string="a", new_string="b"), "deny")

    def test_design_system_readme_is_allowed(self):
        self.assertIsNone(self.decide("Edit", file_path=self.path(".local", "design_system", "README.md"), old_string="a", new_string="b"))

    # --- test --------------------------------------------------------------
    def test_edit_test_data_asks(self):
        self.assertEqual(self.decide("Edit", file_path=self.path(".local", "test", "data.csv"), old_string="1", new_string="2"), "ask")

    def test_test_readme_is_allowed(self):
        self.assertIsNone(self.decide("Write", file_path=self.path(".local", "test", "README.md"), content="# test\n"))

    # --- free folders -------------------------------------------------------
    def test_temp_report_reference_session_log_are_free(self):
        for sub in ("temp", "report", "reference", "session_log"):
            self.assertIsNone(self.decide("Write", file_path=self.path(".local", sub, "a.md"), content="x"), sub)

    # --- plan --------------------------------------------------------------
    def test_write_new_plan_is_allowed(self):
        self.assertIsNone(self.decide("Write", file_path=self.path(".local", "plan", "new.md"), content=PLAN))

    def test_overwrite_existing_plan_asks(self):
        p = self.write(".local/plan/p.md", PLAN)
        self.assertEqual(self.decide("Write", file_path=p, content=PLAN + "more"), "ask")

    def test_tick_next_item_in_order_is_allowed(self):
        p = self.write(".local/plan/p.md", PLAN)
        self.assertIsNone(self.decide("Edit", file_path=p, old_string="- [ ] T2. second", new_string="- [x] T2. second"))

    def test_tick_out_of_order_asks(self):
        p = self.write(".local/plan/p.md", PLAN)
        self.assertEqual(self.decide("Edit", file_path=p, old_string="- [ ] T3. third", new_string="- [x] T3. third"), "ask")

    def test_mark_skipped_asks(self):
        p = self.write(".local/plan/p.md", PLAN)
        self.assertEqual(self.decide("Edit", file_path=p, old_string="- [ ] T2. second", new_string="- [~] T2. second"), "ask")

    def test_tick_after_skipped_item_is_allowed(self):
        p = self.write(".local/plan/p.md", PLAN.replace("- [ ] T2.", "- [~] T2."))
        self.assertIsNone(self.decide("Edit", file_path=p, old_string="- [ ] T3. third", new_string="- [x] T3. third"))

    def test_text_change_in_plan_asks(self):
        p = self.write(".local/plan/p.md", PLAN)
        self.assertEqual(self.decide("Edit", file_path=p, old_string="T2. second", new_string="T2. changed"), "ask")

    def test_tick_combined_with_text_change_asks(self):
        p = self.write(".local/plan/p.md", PLAN)
        self.assertEqual(self.decide("Edit", file_path=p, old_string="- [ ] T2. second", new_string="- [x] T2. other"), "ask")

    def test_multiedit_ticking_two_in_order_is_allowed(self):
        p = self.write(".local/plan/p.md", PLAN)
        edits = [
            {"old_string": "- [ ] T2. second", "new_string": "- [x] T2. second"},
            {"old_string": "- [ ] T3. third", "new_string": "- [x] T3. third"},
        ]
        self.assertIsNone(self.decide("MultiEdit", file_path=p, edits=edits))

    def test_edit_missing_plan_asks(self):
        self.assertEqual(self.decide("Edit", file_path=self.path(".local", "plan", "nope.md"), old_string="a", new_string="b"), "ask")

    def test_ordering_is_per_section(self):
        plan = PLAN + "\n## Extra\n- [ ] E1. a\n"
        p = self.write(".local/plan/p.md", plan)
        self.assertIsNone(self.decide("Edit", file_path=p, old_string="- [ ] E1. a", new_string="- [x] E1. a"))

    # --- source files must not reference .local content ---------------------
    def test_source_file_referencing_local_asks(self):
        self.assertEqual(self.decide("Write", file_path=self.path("src", "foo.py"), content="# see .local/plan/abc.md\n"), "ask")

    def test_source_edit_with_backslash_local_path_asks(self):
        self.assertEqual(self.decide("Edit", file_path=self.path("src", "foo.py"), old_string="a", new_string=r"x = 'C:\\repo\.local\test\data.csv'"), "ask")

    def test_source_file_without_reference_is_allowed(self):
        self.assertIsNone(self.decide("Write", file_path=self.path("src", "foo.py"), content="print('hi')\n"))

    def test_framework_files_may_describe_local(self):
        for rel in ("CLAUDE.md", "README.md", ".gitignore", "docs/workflow.md", ".claude/skills/plan/SKILL.md"):
            self.assertIsNone(self.decide("Write", file_path=self.path(*rel.split("/")), content="Plans live in .local/plan/\n"), rel)

    def test_nested_readme_is_not_framework(self):
        self.assertEqual(self.decide("Write", file_path=self.path("src", "README.md"), content="see .local/test/x\n"), "ask")

    def test_file_outside_project_is_ignored(self):
        self.assertIsNone(self.decide("Write", file_path="/somewhere/else/.local/design_system/a.md", content="x"))

    def test_notebook_edit_uses_notebook_path(self):
        self.assertEqual(self.decide("NotebookEdit", notebook_path=self.path(".local", "design_system", "n.ipynb"), new_source="x"), "deny")

    # --- end to end ---------------------------------------------------------
    def test_script_emits_permission_decision_json(self):
        payload = {"tool_name": "Write", "tool_input": {"file_path": ".local/design_system/x.md", "content": "x"}, "cwd": self.root}
        code, out = self.run_script("guard_local.py", payload)
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "PreToolUse")
        self.assertEqual(data["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertTrue(data["hookSpecificOutput"]["permissionDecisionReason"])

    def test_script_is_silent_when_no_opinion(self):
        payload = {"tool_name": "Write", "tool_input": {"file_path": "src/a.py", "content": "x"}, "cwd": self.root}
        code, out = self.run_script("guard_local.py", payload)
        self.assertEqual((code, out.strip()), (0, ""))

    def test_script_fails_open_on_bad_input(self):
        code, out = self.run_script("guard_local.py", "not-a-dict")
        self.assertEqual((code, out.strip()), (0, ""))


if __name__ == "__main__":
    unittest.main()
