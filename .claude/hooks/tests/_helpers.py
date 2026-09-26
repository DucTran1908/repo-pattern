"""Shared fixtures for hook tests."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HOOKS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HOOKS_DIR not in sys.path:
    sys.path.insert(0, HOOKS_DIR)


class TempRepoCase(unittest.TestCase):
    """Creates an isolated project root with the standard .local layout."""

    SUBFOLDERS = ("plan", "design_system", "report", "reference", "test", "temp", "session_log")

    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="hooktest_")
        for sub in self.SUBFOLDERS:
            os.makedirs(os.path.join(self.root, ".local", sub))

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def path(self, *parts):
        return os.path.join(self.root, *parts)

    def write(self, rel, content):
        full = self.path(*rel.split("/"))
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        return full

    def run_script(self, script, payload, env=None):
        """Runs a hook script end-to-end and returns (exit_code, stdout)."""
        full_env = dict(os.environ)
        full_env["CLAUDE_PROJECT_DIR"] = self.root
        full_env.update(env or {})
        proc = subprocess.run(
            [sys.executable, os.path.join(HOOKS_DIR, script)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=full_env,
            cwd=self.root,
        )
        return proc.returncode, proc.stdout
