"""SPEC-001/AC-4, AC-5, AC-6, AC-8: disposable repository behavior checks."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
HOOK = ROOT / '.codex/hooks/dispatch.py'
CHECKER = ROOT / '.codex/scripts/check_compatibility.py'


class HookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='codex repo dấu ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)

    def write(self, path, text='original'):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
        return target

    def hook(self, event='PreToolUse', **fields):
        payload = dict(cwd=str(self.root), hook_event_name=event)
        payload.update(fields)
        proc = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload),
                              text=True, capture_output=True, encoding='utf-8')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout) if proc.stdout.strip() else {}

    def decision(self, command, tool='apply_patch', **fields):
        result = self.hook(tool_name=tool, tool_input={'command': command}, **fields)
        self.assertNotIn('"ask"', json.dumps(result))
        return result.get('hookSpecificOutput', {})

    def test_ac4_patch_operations(self):
        for body in [
            '*** Add File: .local/project-requirements/a.md\n+x',
            '*** Update File: .local/project-requirements/a.md\n@@\n-old\n+new',
            '*** Delete File: .local/project-requirements/a.md',
            '*** Update File: src/a.md\n*** Move to: .local/project-requirements/a.md\n@@\n-x\n+y',
            '*** Update File: .local/project-requirements/a.md\n*** Move to: src/a.md\n@@\n-x\n+y',
            '*** Add File: .local\\project-requirements\\a.md\n+x',
            '*** Add File: .local/project-requirements/../project-requirements/a.md\n+x',
        ]:
            with self.subTest(body=body):
                self.assertEqual(self.decision('*** Begin Patch\n' + body + '\n*** End Patch').get('permissionDecision'), 'deny')

    def test_ac4_multifile_absolute(self):
        target = self.root / '.local/project-requirements/tên file.md'
        patch = '*** Begin Patch\n*** Add File: src/ok.py\n+ok\n*** Add File: ' + str(target) + '\n+bad\n*** End Patch'
        self.assertEqual(self.decision(patch).get('permissionDecision'), 'deny')

    def test_ac4_index_and_ordinary_allowed(self):
        for target in ['.local/project-requirements/README.md', '.local/test/README.md', 'src/ok.py']:
            self.assertNotIn('permissionDecision', self.decision('*** Begin Patch\n*** Add File: ' + target + '\n+ok\n*** End Patch'))

    def test_ac5_advisory_ignores_forged_approval(self):
        for target in ['.local/test/data.txt', '.local/plan/p.md']:
            self.write(target)
            out = self.decision('*** Begin Patch\n*** Delete File: ' + target + '\n*** End Patch', approved=True)
            self.assertNotIn('permissionDecision', out)
            self.assertIn('authorization', out.get('additionalContext', ''))

    def test_ac5_new_plan_and_ticks(self):
        self.assertNotIn('additionalContext', self.decision('*** Begin Patch\n*** Add File: .local/plan/new.md\n+plan\n*** End Patch'))
        self.write('.local/plan/p.md', '# Plan\n- [ ] T1. a\n- [ ] T2. b\n')
        patch = '*** Begin Patch\n*** Update File: .local/plan/p.md\n@@\n-- [ ] T1. a\n+- [x] T1. a\n*** End Patch'
        self.assertNotIn('additionalContext', self.decision(patch))
        self.assertIn('authorization', self.decision(patch.replace('T1. a', 'T2. b')).get('additionalContext', ''))

    def test_ac4_shell_forbidden_and_reads(self):
        for command in ['git add -f .local/', 'git -C "{}" add --force .'.format(self.root),
                        'Remove-Item -Recurse .local', 'Move-Item .local backup',
                        "Set-Content '.local/project-requirements/tên file.md' x",
                        "Copy-Item src/a '.local/project-requirements/a'",
                        'rm .local/project-requirements/a', 'echo x > .local/project-requirements/a',
                        'rm .local\\project-requirements\\a']:
            with self.subTest(command=command):
                self.assertEqual(self.decision(command, 'Bash').get('permissionDecision'), 'deny')
        for command in ['Get-Content .local/project-requirements/a', 'git status --short', 'ls .local']:
            self.assertNotIn('permissionDecision', self.decision(command, 'Bash'))

    def test_ac5_shell_advisory(self):
        out = self.decision('Set-Content .local/test/data.csv x', 'Bash')
        self.assertNotIn('permissionDecision', out)
        self.assertIn('authorization', out.get('additionalContext', ''))

    def test_ac4_leak_framework_exception(self):
        for target in ['src/a.py', 'AGENTS.md', '.agents/skills/plan/SKILL.md', '.codex/README.md']:
            out = self.decision('*** Begin Patch\n*** Add File: ' + target + '\n+See .local/plan/\n*** End Patch')
            self.assertEqual('additionalContext' in out, target == 'src/a.py')

    def test_ac6_plan_read_only(self):
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*'))
        out = self.hook('SessionStart', permission_mode='plan')
        self.hook('Stop', permission_mode='plan')
        self.assertEqual(before, sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*')))
        self.assertIn('Plan Mode', json.dumps(out))

    def test_ac6_bootstrap_idempotent_root(self):
        existing = self.write('.local/plan/README.md', '# custom\n')
        sub = self.root / 'src'
        sub.mkdir()
        self.hook('SessionStart', cwd=str(sub))
        self.assertEqual(existing.read_text(encoding='utf-8'), '# custom\n')
        for name in ['plan', 'project-requirements', 'report', 'reference', 'test', 'temp', 'session_log']:
            self.assertTrue((self.root / '.local' / name / 'README.md').is_file())
        self.assertFalse((sub / '.local').exists())

    def test_ac6_stop_and_loop_prevention(self):
        self.write('src/a.txt')
        self.assertEqual(self.hook('Stop').get('decision'), 'block')
        self.assertEqual(self.hook('Stop', stop_hook_active=True), {})
        self.write('.local/session_log/log.md', 'evidence')
        self.assertEqual(self.hook('Stop'), {})


class CompatibilityTests(unittest.TestCase):
    def test_ac8_drift_missing_newlines(self):
        self.assertTrue(CHECKER.is_file(), 'compatibility implementation missing')
        spec = importlib.util.spec_from_file_location('compat', CHECKER)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'source.md').write_bytes(b'a\r\nb\r\n')
            (root / 'target.md').write_bytes(b'a\nb\n')
            digest = mod.fingerprint(root / 'source.md')
            self.assertEqual(digest, mod.fingerprint(root / 'target.md'))
            manifest = {'version': 1, 'pairs': [{'id': 'rules', 'source': 'source.md', 'target': 'target.md',
                        'source_sha256': digest, 'target_sha256': digest, 'differences': 'reviewed'}]}
            self.assertEqual(mod.check(root, manifest), [])
            for path in ['source.md', 'target.md']:
                (root / path).write_text('changed', encoding='utf-8')
                self.assertTrue(mod.check(root, manifest))
                (root / path).write_text('a\nb\n', encoding='utf-8')
            (root / 'target.md').unlink()
            self.assertTrue(mod.check(root, manifest))


if __name__ == '__main__':
    unittest.main()
