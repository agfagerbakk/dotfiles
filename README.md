# My dotfiles for Linux based systems

Requires Git, Bash, and Python 3.8 or newer. The bundled Exercism and pup
binaries target Linux x86-64. Zsh is needed to use the Zsh configuration,
and diff-so-fancy requires Perl.

Dependencies are vendored as ordinary files, not Git submodules. Installation
does not download dependencies or require a Python package installation.
The installer links configuration files; it does not install system packages.

## Setup on Ubuntu / Debian / WSL

1. Install the system prerequisites:

   ```bash
   sudo apt update
   sudo apt install git bash python3 zsh perl fontconfig
   ```

2. Clone this repository, or use your existing checkout:

   ```bash
   git clone https://github.com/agfagerbakk/dotfiles.git
   cd dotfiles
   ```

3. Review [install.conf.yaml](install.conf.yaml) and [config/zshrc](config/zshrc).
   Some paths and environment settings are machine-specific. Back up existing
   dotfiles before replacing them: the installer refuses to overwrite conflicting
   files or links, so move those aside deliberately and rerun if necessary.

4. Preview and install:

   ```bash
   ./install --dry-run
   ./install
   fc-cache -f
   ```

   Keep the checkout in place: the installed files are symlinks into it.
   Oh My Zsh and Powerlevel10k are already bundled; do not run their separate
   installers. Running `./install` again is safe.

5. Select `DejaVuSansM Nerd Font Mono` in your terminal's font settings and open
   a new terminal. On WSL, the terminal runs on Windows: install the `.ttf` files
   from [fonts/DejaVuSansMono](fonts/DejaVuSansMono) on Windows as well, then select
   the family in Windows Terminal. Linux's font cache does not install Windows fonts.

6. Follow Powerlevel10k's first-run wizard, or run this inside Zsh:

   ```zsh
   p10k configure
   ```

   This saves your prompt settings in `~/.p10k.zsh`, which the configuration
   loads automatically. The theme can download its optional `gitstatus` helper
   on first use; this is separate from the offline dotfile installation.

Bash automatically starts Zsh in terminal sessions. Changing the login shell
with `chsh` is not required. If Zsh is missing, new terminals warn and stay in Bash.

## Optional tools and local settings

- For GitHub CLI and its `gh` completions, install `sudo apt install gh`, then
  run `gh auth login`. The plugin does not install or authenticate the CLI for you.
- Rust/Cargo, Node/NVM, Google Cloud SDK, and their credentials are not bundled.
  Their existing conditional startup hooks are retained.
- Put machine-local shell additions in `~/.shell_env_local` and Git overrides
  in `~/.gitconfig_local`. Neither file is managed by the installer.
- Exercism completions are bundled in [bin/shell](bin/shell); see its
  [setup instructions](bin/shell/README.md) to enable them.

## Troubleshooting

| Message / symptom | Resolution |
| --- | --- |
| `exec: zsh: not found` | Install `zsh` and rerun `./install` from this updated checkout. The updated Bash files safely fall back when Zsh is absent. |
| Deprecated `github` plugin warning | The current [Zsh configuration](config/zshrc) uses `gh`. If the warning persists, check that `~/.zshrc` points to this checkout and remove `github` from any local plugin overrides. |
| `theme 'powerlevel10k/powerlevel10k' not found` | The theme is bundled under `oh-my-zsh/custom/themes/powerlevel10k`. Check that `~/.oh-my-zsh` points to this checkout. If you set `ZSH_CUSTOM`, install or link the theme under that directory's `themes/powerlevel10k` instead. |
| Missing prompt icons | Select the Nerd Font in the terminal application, not just in Linux. On WSL, install it on Windows too. Rerun `p10k configure` after changing fonts. |
| `module 'collections' has no attribute 'Hashable'` | This checkout bundles fixed PyYAML 6.0.3. Run its `./install`, not an older copy of Dotbot or these dotfiles. |

## Bundled dependencies

Updated on 2026-10-30. Versions below identify the snapshots checked into this
repository; installation does not automatically advance them.

| Dependency | Version / upstream snapshot | Source |
| --- | --- | --- |
| Dotbot | v1.24.1 (`a7fe585f087617f5d897754b970d1088af50084c`) | [anishathalye/dotbot](https://github.com/anishathalye/dotbot/tree/v1.24.1) |
| PyYAML | 6.0.3 (`49790e73684bebad1df05ef8d828fa12f685bffb`) | [yaml/pyyaml](https://github.com/yaml/pyyaml/tree/6.0.3) |
| Oh My Zsh | `17a2b4c3a5855524ad4772a17ada0dc474e2fdf3` | [ohmyzsh/ohmyzsh](https://github.com/ohmyzsh/ohmyzsh/tree/17a2b4c3a5855524ad4772a17ada0dc474e2fdf3) |
| Powerlevel10k | v1.20.0 (`35833ea15f14b71dbcebc7e54c104d8d56ca5268`) | [romkatv/powerlevel10k](https://github.com/romkatv/powerlevel10k/tree/v1.20.0) |
| Exercism CLI and completions | v3.5.9 | [exercism/cli](https://github.com/exercism/cli/releases/tag/v3.5.9) |
| diff-so-fancy | v1.4.14 (standalone release executable) | [so-fancy/diff-so-fancy](https://github.com/so-fancy/diff-so-fancy/releases/tag/v1.4.14) |
| pup | v0.4.0 (unchanged; latest upstream release) | [ericchiang/pup](https://github.com/ericchiang/pup/releases/tag/v0.4.0) |
| DejaVu Sans Mono Nerd Font | v3.5.1 | [ryanoasis/nerd-fonts](https://github.com/ryanoasis/nerd-fonts/releases/tag/v3.5.1) |
| Fira Code | 6.2 | [tonsky/FiraCode](https://github.com/tonsky/FiraCode/releases/tag/6.2) |

Tool licenses are in [licenses/](licenses/). Font and source dependency licenses
are included beside their files. Exercism, diff-so-fancy, and Nerd Font release
downloads were checked against GitHub's published SHA-256 asset digests.

Nerd Fonts v3 changes font filenames, family names, and some icon codepoints.
Select the new `DejaVuSansM Nerd Font Mono` family in your terminal if necessary;
custom prompts using old icon codepoints may need adjustment. Fira Code keeps its
existing family name. Powerlevel10k is bundled under
`oh-my-zsh/custom/themes/powerlevel10k`; run `p10k configure` to customize it.

The `gh` plugin provides GitHub CLI completions instead of the deprecated
`github` plugin for the legacy `hub` CLI. Install `gh` separately if you use it.

To refresh dependencies again, replace their vendored snapshots from the upstream
sources above (including PyYAML under `dotbot/lib/pyyaml`), retain their licenses,
update this table, and test `./install` in a temporary home before committing.
Preserve the bundled Powerlevel10k directory and its exceptions in
`oh-my-zsh/.gitignore` when replacing the Oh My Zsh snapshot.

## Testing

Run the installer regression tests without installing any Python packages:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

These use temporary home directories to check installation, repeat runs, dry runs,
existing-file protection, YAML error reporting, Bash fallback, and bundled theme
presence without changing your dotfiles. With Zsh installed, they also load the
configured plugins and Powerlevel10k; otherwise that startup test is skipped.
