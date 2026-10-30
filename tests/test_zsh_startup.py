import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ZSH = shutil.which("zsh")


@unittest.skipUnless(ZSH, "Zsh is not installed")
class ZshStartupTests(unittest.TestCase):
    def test_configured_plugins_and_theme_load(self):
        with tempfile.TemporaryDirectory(prefix="dotfiles-zsh-test-") as directory:
            home = Path(directory)
            (home / ".oh-my-zsh").symlink_to(ROOT / "oh-my-zsh")
            (home / ".shell").symlink_to(ROOT / "shell")
            (home / ".shell_env").symlink_to(ROOT / "config/shell_env")
            custom = home / "custom"
            shutil.copytree(
                ROOT / "oh-my-zsh/custom/themes/powerlevel10k",
                custom / "themes/powerlevel10k",
                ignore=shutil.ignore_patterns("*.zwc", "*.zwc.old"),
            )
            result = subprocess.run(
                [ZSH, "-f", "-c", """
zstyle ':omz:update' mode disabled
source "$1"
(( ${plugins[(Ie)gh]} )) || exit 1
(( ! ${plugins[(Ie)github]} )) || exit 2
(( $+functions[p10k] )) || exit 3
(( $+functions[git_prompt_info] )) || exit 4
print 'Zsh startup passed'
""", "zsh", str(ROOT / "config/zshrc")],
                env=dict(
                    os.environ,
                    HOME=directory,
                    ZSH_CUSTOM=str(custom),
                    ZSH_CACHE_DIR=str(home / "cache"),
                    ZSH_COMPDUMP=str(home / "zcompdump"),
                    ZSH_DISABLE_COMPFIX="true",
                ),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertIn("Zsh startup passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
