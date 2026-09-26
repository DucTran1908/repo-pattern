import json
import os
import subprocess
import time
import unittest

from _helpers import TempRepoCase

import session_log_check


class SessionLogCheckTest(TempRepoCase):
    def touch(self, rel, mtime, content="x"):
        full = self.write(rel, content)
        os.utime(full, (mtime, mtime))
        return full

    def decide(self, changed, stop_hook_active=False):
        payload = {"hook_event_name": "Stop", "stop_hook_active": stop_hook_active, "cwd": self.root}
        return session_log_check.decide(payload, self.root, changed_files=changed)

    def test_no_changes_does_not_block(self):
        self.assertIsNone(self.decide([]))

    def test_change_newer_than_log_blocks(self):
        now = time.time()
        self.touch(".local/session_log/2026-01-01_main_x.md", now - 100)
        self.touch("src/a.py", now)
        result = self.decide(["src/a.py"])
        self.assertEqual(result["decision"], "block")
        self.assertIn("session_log", result["reason"])

    def test_missing_log_blocks(self):
        self.touch("src/a.py", time.time())
        self.assertEqual(self.decide(["src/a.py"])["decision"], "block")

    def test_log_newer_than_change_does_not_block(self):
        now = time.time()
        self.touch("src/a.py", now - 100)
        self.touch(".local/session_log/2026-01-01_main_x.md", now)
        self.assertIsNone(self.decide(["src/a.py"]))

    def test_readme_does_not_count_as_log(self):
        now = time.time()
        self.touch("src/a.py", now - 100)
        self.touch(".local/session_log/README.md", now)
        self.assertEqual(self.decide(["src/a.py"])["decision"], "block")

    def test_stop_hook_active_never_blocks(self):
        self.touch("src/a.py", time.time())
        self.assertIsNone(self.decide(["src/a.py"], stop_hook_active=True))

    def test_deleted_files_are_ignored(self):
        self.assertIsNone(self.decide(["gone.py"]))

    def test_end_to_end_with_git(self):
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        self.write(".gitignore", ".local/\n")
        self.write("src/a.py", "x")
        code, out = self.run_script("session_log_check.py", {"hook_event_name": "Stop", "stop_hook_active": False, "cwd": self.root})
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["decision"], "block")


if __name__ == "__main__":
    unittest.main()
