"""SPEC-001/AC-4..6: regressions from independent review and runtime boundaries."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HOOK = Path(__file__).resolve().parents[1] / 'dispatch.py'
spec = importlib.util.spec_from_file_location('dispatch', HOOK)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ReviewRegressionTests(unittest.TestCase):
    def test_ac4_option_aware_shell_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            for command in ['Copy-Item src/a .local/project-requirements/a -Force',
                            'Copy-Item -Destination .local/project-requirements/a -Path src/a -Force',
                            'git -C .local add -f plan/p.md',
                            'Remove-Item -Recurse .local/*']:
                with self.subTest(command=command):
                    result = mod.guard_shell(command, root, root)
                    self.assertEqual(result.get('hookSpecificOutput', {}).get('permissionDecision'), 'deny')

    def test_ac5_ambiguous_patch_not_exempt(self):
        self.assertIsNone(mod.patched_text('a\na\n', ['-a', '+b']))
        self.assertFalse(mod.ticks_only('- [ ] a\n', '- [x] changed\n'))

    def test_ac6_malformed_input_visible_and_no_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run([sys.executable, '-B', str(HOOK)], cwd=tmp, input='not-json',
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0)
            self.assertIn('No enforcement claimed', json.loads(proc.stdout)['systemMessage'])
            self.assertEqual(list(Path(tmp).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
