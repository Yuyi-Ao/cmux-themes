---
name: cmux-terminal-setup
description: Select, customize, preview, verify, or restore independent cmux terminal colors and Starship prompts using this repository. Preserve running sessions, unrelated settings, privacy, and author attribution.
---

# cmux terminal setup

## Inspect

Locate the checkout containing `cmux-theme`, `starship-theme`, `cmux/`, `starship/`, and `tools/install.py`. The repository root is three parents above this skill directory; if copied elsewhere, locate the checkout rather than assuming a machine-specific path.

Read `README.md`, `cmux/CREDITS.md`, and `starship/CREDITS.md`. Enumerate `cmux/*/terminal.conf` and `starship/*.toml` for current IDs. `starship/order.json` sets preferred order; menu positions are not style IDs. `starship/sources.json` records community source links.

Read only relevant appearance files and `~/.config/cmux/reading-selection.json` when needed. Do not inspect credentials or conversations. Check macOS, Python 3.10+, cmux, and the configured font; prompt changes also require initialized Starship in zsh. Install dependencies only within user authorization.

## Switch independently

```sh
./cmux-theme slate
./starship-theme 10-adithsureshbabu
```

Each command changes only its own layer plus selection metadata. A cmux switch does not install or modify a prompt. A Starship switch does not install or modify terminal colors, even on a first install. Do not introduce theme-following behavior.

When requested, `./cmux-theme slate --with-cli-themes` also installs optional Codex/Claude theme files into their standard home directories. It never selects those themes. The user chooses `cmux-reading-slate` through `/theme` in each app and switches back through the same menu. Do not add CLI launchers or modify application settings. For custom `CODEX_HOME` or `CLAUDE_CONFIG_DIR`, explain that the theme files belong under that directory's `themes/`; the installer uses standard locations only.

Use explicit IDs when acting for a user. For a dry run:

```sh
python3 tools/install.py --cmux slate
python3 tools/install.py --starship 10-adithsureshbabu
```

Use `--home <temporary-directory> --apply` for isolated tests. Never use the menu wrappers for isolated tests: they target the real home and can reload cmux. Installer tests are in `tests/`.

Use the installer so changed files are backed up. Preserve unrelated cmux settings and shell initialization. Do not restart apps, close workspaces, kill jobs, change security settings, enable background Git/PR probing, or modify shared Ghostty/Starship configs. Do not paste commands into existing agent composers; use a new clearly owned shell for live trials.

Verify the relevant selection field and installed bytes: `preset` for cmux, `starship_style` for Starship. cmux terminal settings live at `~/Library/Application Support/com.cmuxterm.app/config.ghostty`; the prompt lives at `~/.config/cmux/starship-reading.toml`. Distinguish configuration saved, reload successful, and appearance actually observed. Report backup location and explain that a new cmux shell shows the prompt.

## Restore

`./cmux-theme restore` and `./starship-theme restore` both undo the latest unrestored switch of either kind, including optional CLI files installed in that switch. They do not undo choices made later in an application's `/theme` menu. Switch the application to a built-in theme before removing selected custom files. Backups are local under `~/.config/cmux/reading-backups/`. If files changed after installation, preserve those edits and inspect the conflict instead of forcing rollback.

For isolated restore, run `python3 tools/install.py --home <temporary-home> --rollback <backup-directory>`; add `--apply` to write. Pass the backup directory, not its manifest file. Do not delete user backups or previously installed configuration as part of repository cleanup.

## Add and document

Add one TOML directly under `starship/`, or a directory with `terminal.conf` and `app.json` under `cmux/`. Menus discover additions automatically. Preserve the user's chosen styles and preferred ordering when curating. Parse new configuration and review any custom command modules before rendering a downloaded prompt. Keep author/source links in the corresponding `CREDITS.md`.

Use real demo-only captures in `previews/cmux/` and `previews/starship/`. Exclude private directories, account details, unrelated windows, and conversations. Do not generate mockups as substitutes for real screenshots. Do not submit model requests for previews.

`python3 tools/build_preview_sheets.py` crops and arranges curated captures while retaining originals. Adjust inputs and crop coordinates when necessary; inspect output including right-aligned prompts before publishing.

Use the user's configured Git identity. Make new commits without rewriting published history. Push only within existing authorization, verify the remote and privacy setting, and never change visibility without an explicit request. Never commit credentials, transcripts, home backups, or machine-specific paths.
