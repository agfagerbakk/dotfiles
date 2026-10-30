import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary_home = tempfile.TemporaryDirectory(prefix="dotfiles-test-")
        self.addCleanup(self.temporary_home.cleanup)
        self.home = Path(self.temporary_home.name)
        self.env = dict(os.environ, HOME=str(self.home), PYTHONDONTWRITEBYTECODE="1")

    def run_install(self, *args):
        return subprocess.run(
            [str(ROOT / "install"), "--no-color", *args],
            cwd=self.home,
            env=self.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

    def assert_installed_links(self):
        expected = {
            ".shell": ROOT / "shell",
            ".oh-my-zsh": ROOT / "oh-my-zsh",
        }
        for name in (
            "shell_env", "bashrc", "bash_profile", "dircolors", "gitconfig",
            "gitignore", "gdbinit", "editorconfig", "zshrc",
        ):
            expected["." + name] = ROOT / "config" / name
        for source in (ROOT / "bin").iterdir():
            expected[".local/bin/" + source.name] = source
        for source in (ROOT / "fonts").iterdir():
            expected[".local/share/fonts/" + source.name] = source
        for destination, source in expected.items():
            with self.subTest(destination=destination):
                link = self.home / destination
                self.assertTrue(link.is_symlink(), str(link))
                self.assertEqual(link.resolve(), source.resolve())
        theme = self.home / ".oh-my-zsh/custom/themes/powerlevel10k"
        for name in ("powerlevel10k.zsh-theme", "internal/p10k.zsh", "LICENSE"):
            with self.subTest(theme_file=name):
                self.assertTrue((theme / name).is_file(), str(theme / name))

    def test_install_from_outside_repository(self):
        result = self.run_install()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assert_installed_links()

    def test_install_is_idempotent(self):
        for _ in range(2):
            result = self.run_install()
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assert_installed_links()

    def test_dry_run_does_not_change_home(self):
        result = self.run_install("--dry-run")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Would", result.stdout)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_existing_file_is_not_overwritten(self):
        bashrc = self.home / ".bashrc"
        bashrc.write_text("existing configuration\n")
        result = self.run_install()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertFalse(bashrc.is_symlink())
        self.assertEqual(bashrc.read_text(), "existing configuration\n")

    def test_unhashable_yaml_key_reports_error(self):
        config = self.home / "invalid.yaml"
        config.write_text("? [unhashable, key]\n: value\n")
        result = self.run_install("-c", str(config))
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("found unhashable key", result.stdout)
        self.assertNotIn("AttributeError", result.stdout)
        self.assertEqual(list(self.home.iterdir()), [config])


if __name__ == "__main__":
    unittest.main()
