import json
import unittest

from _helpers import TempRepoCase

import guard_shell


class GuardShellTest(TempRepoCase):
    def decide(self, command, tool="Bash"):
        payload = {"tool_name": tool, "tool_input": {"command": command}, "cwd": self.root}
        return guard_shell.decide(payload, self.root)[0]

    def test_redirect_into_project_requirements_is_denied(self):
        self.assertEqual(self.decide("echo x > .local/project-requirements/a.txt"), "deny")

    def test_append_into_test_asks(self):
        self.assertEqual(self.decide("echo x >> .local/test/data.csv"), "ask")

    def test_rm_plan_asks(self):
        self.assertEqual(self.decide("rm .local/plan/p.md"), "ask")

    def test_sed_inplace_plan_asks(self):
        self.assertEqual(self.decide("sed -i 's/a/b/' .local/plan/p.md"), "ask")

    def test_powershell_set_content_project_requirements_is_denied(self):
        self.assertEqual(self.decide("Set-Content -Path .local\\project-requirements\\a.md -Value x", tool="PowerShell"), "deny")

    def test_powershell_remove_item_test_asks(self):
        self.assertEqual(self.decide("Remove-Item .local/test/x.json", tool="PowerShell"), "ask")

    def test_copy_out_of_protected_folder_is_allowed(self):
        self.assertIsNone(self.decide("cp .local/test/data.csv .local/temp/data.csv"))

    def test_copy_into_protected_folder_is_denied(self):
        self.assertEqual(self.decide("cp notes.md .local/project-requirements/notes.md"), "deny")

    def test_reading_protected_folder_is_allowed(self):
        self.assertIsNone(self.decide("cat .local/project-requirements/spec.md | grep foo"))

    def test_readme_update_is_allowed(self):
        self.assertIsNone(self.decide("echo '| a | b |' >> .local/project-requirements/README.md"))

    def test_free_folder_writes_are_allowed(self):
        self.assertIsNone(self.decide("echo x > .local/temp/a.txt && rm .local/report/old.md"))

    def test_worst_decision_wins_across_segments(self):
        self.assertEqual(self.decide("rm .local/plan/p.md; rm .local/project-requirements/a.md"), "deny")

    def test_git_commit_mentioning_local_asks(self):
        self.assertEqual(self.decide('git commit -m "see .local/plan/x.md"'), "ask")

    def test_plain_git_commit_is_allowed(self):
        self.assertIsNone(self.decide('git commit -m "feat: add parser"'))

    def test_force_adding_local_is_denied(self):
        self.assertEqual(self.decide("git add -f .local/plan/p.md"), "deny")

    def test_unrelated_command_is_allowed(self):
        self.assertIsNone(self.decide("python -m unittest discover"))

    def test_script_end_to_end(self):
        payload = {"tool_name": "Bash", "tool_input": {"command": "rm -rf .local/project-requirements"}, "cwd": self.root}
        code, out = self.run_script("guard_shell.py", payload)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["hookSpecificOutput"]["permissionDecision"], "deny")


if __name__ == "__main__":
    unittest.main()
