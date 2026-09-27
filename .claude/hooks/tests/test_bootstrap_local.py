import json
import os
import shutil
import unittest

from _helpers import TempRepoCase

import bootstrap_local


class BootstrapLocalTest(TempRepoCase):
    def test_creates_all_subfolders_with_readme(self):
        shutil.rmtree(self.path(".local"))
        created = bootstrap_local.ensure_local(self.root)
        for sub in self.SUBFOLDERS:
            readme = self.path(".local", sub, "README.md")
            self.assertTrue(os.path.isfile(readme), sub)
            with open(readme, encoding="utf-8") as fh:
                text = fh.read()
            self.assertIn("| Path | Description |", text)
        self.assertEqual(len(created), len(self.SUBFOLDERS))

    def test_readme_contains_only_heading_and_table(self):
        bootstrap_local.ensure_local(self.root)
        with open(self.path(".local", "temp", "README.md"), encoding="utf-8") as fh:
            lines = [l for l in fh.read().splitlines() if l.strip()]
        self.assertTrue(lines[0].startswith("# "))
        self.assertTrue(all(l.startswith("|") for l in lines[1:]))

    def test_existing_readme_is_not_overwritten(self):
        self.write(".local/plan/README.md", "# plan\n\n| Path | Description |\n|---|---|\n| `a.md` | A |\n")
        created = bootstrap_local.ensure_local(self.root)
        with open(self.path(".local", "plan", "README.md"), encoding="utf-8") as fh:
            self.assertIn("`a.md`", fh.read())
        self.assertNotIn(self.path(".local", "plan", "README.md"), created)

    def test_plan_progress_lists_unfinished_plans(self):
        self.write(".local/plan/a.md", "- [x] T1\n- [~] T2\n- [ ] T3\n")
        self.write(".local/plan/b.md", "- [x] T1\n- [x] T2\n")
        progress = bootstrap_local.plan_progress(self.root)
        self.assertEqual(progress, [("a.md", 2, 3)])

    def test_script_outputs_session_context(self):
        shutil.rmtree(self.path(".local", "temp"))
        self.write(".local/plan/a.md", "- [x] T1\n- [ ] T2\n")
        code, out = self.run_script("bootstrap_local.py", {"hook_event_name": "SessionStart", "cwd": self.root})
        self.assertEqual(code, 0)
        data = json.loads(out)
        ctx = data["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("a.md", ctx)
        self.assertIn("1/2", ctx)
        self.assertTrue(os.path.isdir(self.path(".local", "temp")))


if __name__ == "__main__":
    unittest.main()
