"""Verify independence and safe rollback using temporary homes only."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)

    def run_install(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(ROOT / 'tools/install.py'), '--home', str(self.home), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return result

    def put(self, name, data):
        p = self.home / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def selection(self):
        return json.loads((self.home / '.config/cmux/reading-selection.json').read_text())

    def test_cmux_does_not_touch_prompt_shell_or_cli(self):
        files = {'.zshrc': b'# personal shell\n', '.config/cmux/starship-reading.toml': b'# personal prompt\n', '.codex/config.toml': b'# personal codex\n', '.claude/settings.json': b'{}\n'}
        for name, data in files.items(): self.put(name, data)
        self.put('.config/cmux/cmux.json', b'{"watchGitStatus":false,"unrelated":"keep"}')
        self.run_install('--cmux', 'slate', '--apply')
        for name, data in files.items(): self.assertEqual((self.home / name).read_bytes(), data)
        self.assertEqual(json.loads((self.home / '.config/cmux/cmux.json').read_text())['unrelated'], 'keep')
        self.assertFalse((self.home / '.codex/themes').exists())
        self.assertFalse((self.home / '.claude/themes').exists())
        self.assertEqual(self.selection(), {'preset': 'slate'})

    def test_starship_first_install_does_not_install_terminal_or_cli(self):
        self.run_install('--starship', '10-adithsureshbabu', '--apply')
        for name in ['Library', '.config/cmux/cmux.json', '.codex', '.claude']:
            self.assertFalse((self.home / name).exists())
        self.assertEqual(self.selection(), {'starship_style': '10-adithsureshbabu'})

    def test_switches_preserve_the_other_layer(self):
        self.run_install('--cmux', 'slate', '--apply')
        terminal = self.home / 'Library/Application Support/com.cmuxterm.app/config.ghostty'
        before = terminal.read_bytes()
        self.run_install('--starship', 'tokyo-night', '--apply')
        self.assertEqual(terminal.read_bytes(), before)
        prompt = self.home / '.config/cmux/starship-reading.toml'
        before = prompt.read_bytes()
        self.run_install('--cmux', 'cool-light', '--apply')
        self.assertEqual(prompt.read_bytes(), before)
        self.assertEqual(self.selection(), {'preset': 'cool-light', 'starship_style': 'tokyo-night'})

    def test_dry_run_and_idempotence(self):
        self.run_install('--cmux', 'slate')
        self.assertEqual(list(self.home.iterdir()), [])
        self.run_install('--starship', 'tokyo-night', '--apply')
        base = self.home / '.config/cmux/reading-backups'
        before = sorted(base.iterdir())
        self.run_install('--starship', 'tokyo-night', '--apply')
        self.assertEqual(sorted(base.iterdir()), before)

    def test_rollback_refuses_edits_then_restores(self):
        shell = self.put('.zshrc', b'# original shell\n')
        self.run_install('--starship', 'tokyo-night', '--apply')
        installed = shell.read_bytes()
        backup = next((self.home / '.config/cmux/reading-backups').iterdir())
        shell.write_bytes(b'# subsequent edit\n')
        self.run_install('--rollback', str(backup), '--apply', ok=False)
        self.assertEqual(shell.read_bytes(), b'# subsequent edit\n')
        shell.write_bytes(installed)
        self.run_install('--rollback', str(backup), '--apply')
        self.assertEqual(shell.read_bytes(), b'# original shell\n')
        self.assertFalse((self.home / '.config/cmux/starship-reading.toml').exists())

    def test_symlink_target_is_refused(self):
        target = self.put('unrelated.toml', b'# do not touch\n')
        link = self.home / '.config/cmux/starship-reading.toml'
        link.parent.mkdir(parents=True)
        link.symlink_to(target)
        self.run_install('--starship', 'tokyo-night', '--apply', ok=False)
        self.assertEqual(target.read_bytes(), b'# do not touch\n')

if __name__ == '__main__':
    unittest.main()
