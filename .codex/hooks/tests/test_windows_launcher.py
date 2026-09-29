"""SPEC-001/AC-4, AC-6: real Windows launcher, disposable checkout and stdin."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

HOOKS = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('powershell.exe'), 'Windows launcher requires Windows PowerShell')
class WindowsLauncherTests(unittest.TestCase):
    def test_ac6_plan_mode_from_subdirectory(self):
        with tempfile.TemporaryDirectory(prefix='codex launch dấu ') as tmp:
            root = Path(tmp)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            target = root / '.codex/hooks'
            target.mkdir(parents=True)
            for name in ('dispatch.py', 'run-hook.cmd'):
                shutil.copyfile(str(HOOKS / name), str(target / name))
            sub = root / 'src'
            sub.mkdir()
            command = "& (Join-Path (git rev-parse --show-toplevel) '.codex/hooks/run-hook.cmd')"
            payload = {'hook_event_name': 'SessionStart', 'permission_mode': 'plan', 'cwd': str(sub)}
            proc = subprocess.run(['powershell.exe', '-NoLogo', '-NoProfile', '-Command', command],
                                  cwd=sub, input=json.dumps(payload), text=True, capture_output=True, timeout=20)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn('Plan Mode', json.loads(proc.stdout)['hookSpecificOutput']['additionalContext'])
            self.assertFalse((root / '.local').exists())
            self.assertFalse((sub / '.local').exists())
            self.assertFalse((target / '__pycache__').exists())


if __name__ == '__main__':
    unittest.main()
