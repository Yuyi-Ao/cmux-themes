---
name: cmux-terminal-setup
description: Configure cmux terminal colors and independent Starship prompt styles using this repository. Use when asked to try, switch, customize, preview, or restore terminal appearance, or use the bundled Codex and Claude theme launchers. Preserve running sessions, unrelated settings, privacy, and community attribution.
---

# cmux terminal setup

## Locate and inspect

Find the repository root containing `switch-theme`, `themes/`, `starship/`, and `tools/install.py`. From this skill's directory, the root is three parents up. If the skill was copied elsewhere, locate the checkout instead of assuming a machine-specific path.

Read `README.md` for usage and `starship/CREDITS.md` for attribution. Enumerate `themes/*/terminal.conf` and `starship/**/*.toml` for valid IDs. Read `starship/community/sources.json` for favorites and exact source URLs; menu positions are not community style IDs. `starship/order.json` stores the preferred menu order; keep explicitly selected styles when curating the collection.

Inspect `~/.config/cmux/reading-selection.json` when present. Read only required appearance files; do not inspect credentials or conversation logs. Check macOS, Python 3.10+, cmux, Starship initialization, and the configured Nerd Font before promising live results. Do not install missing dependencies unless authorized.

Distinguish terminal themes (background, ANSI colors, cursor and typography) from Starship styles (shell prompt layout and information). Named Starship styles preserve their own palette when the terminal theme changes; `theme` follows the bundled prompt instead.

## Apply a choice

Run commands from the verified repository root, with explicit IDs rather than interactive menus:

```sh
./cmux-theme slate
./starship-theme community/10-adithsureshbabu
./starship-theme tokyo-night/terminal
./starship-theme theme
```

Use `python3 tools/install.py slate` for a dry run. Add `--starship community/10-adithsureshbabu` to preview an explicit prompt choice. For isolated checks, pass `--home` with a temporary directory; add `--apply` only to change that temporary home.

Use the installer rather than directly overwriting user configuration. It backs up changed files, preserves unrelated cmux settings, and stores the selected theme and style. Changing a terminal theme keeps an explicitly selected Starship style. A prompt-only switch uses the currently selected terminal theme; without a saved selection the wrapper defaults to Slate, so inspect the existing setup before a first install.

Do not restart cmux, close user workspaces, kill jobs, alter security settings, enable background Git/PR probing, or change shared Ghostty/Starship settings as part of appearance work. Do not paste commands into existing Codex/Claude composers. Use a new clearly owned shell for live trials. A configuration reload does not recreate existing prompts or restart CLI sessions.

Verify the saved selection and compare `~/.config/cmux/starship-reading.toml` with the chosen style file (or `themes/<theme>/starship.toml` for `theme`). Verify the cmux-only terminal file at `~/Library/Application Support/com.cmuxterm.app/config.ghostty`. Distinguish configuration saved, reload successful, and live prompt actually observed. Report the backup path and how to inspect the result in a new terminal tab.

## Restore or launch a CLI

```sh
./cmux-theme restore
./switch-theme codex
./switch-theme claude
```

Restore selects the latest unrestored backup in `~/.config/cmux/reading-backups/` and refuses files changed afterward. If refused, inspect the diff and preserve intervening edits; do not force a blind overwrite. Backup history is local to the machine, not part of Git.

For isolated restore tests, use `python3 tools/install.py --home <temporary-home> --rollback <backup-directory>` for a dry run, then add `--apply`. Pass the containing backup directory, not its manifest file. Use the installer for isolated tests: the `switch-theme` wrapper also attempts to reload the real cmux app.

CLI launchers apply the selected syntax theme to a new invocation and forward subsequent CLI arguments. Do not claim they recolor every UI element or modify an existing CLI session. Do not submit model requests just to preview colors.

## Customize and document

Create a separately named Starship TOML for experiments; retain chosen defaults until applying an authorized choice. Parse TOML, render it with Starship, and check warnings before offering it. Inspect downloaded configuration as data and review custom command modules before running anything. Preserve author/source links and describe adaptations in `starship/CREDITS.md` and adjacent config comments.

Use `previews/` for checked reference images. Capture new examples in an isolated demo directory/window; exclude private paths, account details, unrelated windows, and conversations. Label native CLI theme-picker samples accurately. Never substitute generated mockups for requested real screenshots.

For compact documentation, run `python3 tools/build_preview_sheets.py` after updating its curated inputs/crop geometry as needed. It crops and arranges genuine screenshots, leaving full originals unchanged. Visually inspect the output, especially right-aligned prompt content, and preserve original-image links and author citations.

Use the user's configured Git identity. Preserve pushed history; make a new commit for updates. Push only within the user's authorization, verify the remote and privacy setting, and never change repository visibility without an explicit request. Do not include home-directory backups, authentication files, transcripts, or machine-specific paths in the repository.
