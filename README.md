# My dotfiles for Linux based systems

Requires Git, Bash, and Python 3.8 or newer. The bundled Exercism and pup
binaries target Linux x86-64. Zsh is needed to use the Zsh configuration,
and diff-so-fancy requires Perl.

1. Edit [install.conf.yaml](install.conf.yaml) for your preferred settings.
2. Preview changes with `./install --dry-run`.
3. Run `./install` to link your dotfiles, tools, and fonts.

Dependencies are vendored as ordinary files, not Git submodules. Installation
does not download dependencies or require a Python package installation.
Personal shell settings and dotfile link destinations are preserved.

## Bundled dependencies

Updated on 2026-10-30. Versions below identify the snapshots checked into this
repository; installation does not automatically advance them.

| Dependency | Version / upstream snapshot | Source |
| --- | --- | --- |
| Dotbot | v1.24.1 (`a7fe585f087617f5d897754b970d1088af50084c`) | [anishathalye/dotbot](https://github.com/anishathalye/dotbot/tree/v1.24.1) |
| PyYAML | 6.0.3 (`49790e73684bebad1df05ef8d828fa12f685bffb`) | [yaml/pyyaml](https://github.com/yaml/pyyaml/tree/6.0.3) |
| Oh My Zsh | `17a2b4c3a5855524ad4772a17ada0dc474e2fdf3` | [ohmyzsh/ohmyzsh](https://github.com/ohmyzsh/ohmyzsh/tree/17a2b4c3a5855524ad4772a17ada0dc474e2fdf3) |
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
existing family name. The configured Powerlevel10k theme is still a separate,
user-managed installation; it is not bundled here.

Oh My Zsh now warns that the configured `github` plugin (for the legacy `hub`
CLI) is deprecated. It is retained to preserve your settings; switch to `gh`
only if you want GitHub CLI completions instead.

To refresh dependencies again, replace their vendored snapshots from the upstream
sources above (including PyYAML under `dotbot/lib/pyyaml`), retain their licenses,
update this table, and test `./install` in a temporary home before committing.

## Testing

Run the installer regression tests without installing any Python packages:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

These use temporary home directories to check installation, repeat runs, dry runs,
existing-file protection, and YAML error reporting without changing your dotfiles.
