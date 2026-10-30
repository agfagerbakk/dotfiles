import os
from pathlib import Path
import pty
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASH = shutil.which("bash")


class BashStartupTests(unittest.TestCase):
    def run_startup(self, config, *, zsh_available=False, terminal=True):
        with tempfile.TemporaryDirectory(prefix="dotfiles-bash-test-") as directory:
            home = Path(directory)
            if zsh_available:
                zsh = home / "zsh"
                zsh.write_text("#!" + BASH + "\nprintf 'zsh started\\n' >&2\n")
                zsh.chmod(0o755)
            env = dict(os.environ, HOME=directory, PATH=directory)
            env.pop("BASH_ENV", None)
            master, slave = pty.openpty()
            try:
                return subprocess.run(
                    [BASH, "--noprofile", "--norc", "-c",
                     '. "$1"; printf "bash continued\\n" >&2', "bash",
                     str(ROOT / "config" / config)],
                    env=env,
                    stdout=slave if terminal else subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5,
                )
            finally:
                os.close(slave)
                os.close(master)

    def test_missing_zsh_keeps_bash_usable(self):
        for config in ("bashrc", "bash_profile"):
            with self.subTest(config=config):
                result = self.run_startup(config)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Zsh is not installed; staying in Bash", result.stderr)
                self.assertIn("bash continued", result.stderr)
                self.assertNotIn("No such file", result.stderr)
                self.assertNotIn("not found", result.stderr)

    def test_available_zsh_replaces_bash(self):
        for config in ("bashrc", "bash_profile"):
            with self.subTest(config=config):
                result = self.run_startup(config, zsh_available=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "zsh started\n")

    def test_nonterminal_does_not_start_zsh(self):
        for config in ("bashrc", "bash_profile"):
            for available in (False, True):
                with self.subTest(config=config, zsh_available=available):
                    result = self.run_startup(
                        config, zsh_available=available, terminal=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stderr, "bash continued\n")


if __name__ == "__main__":
    unittest.main()
