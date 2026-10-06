# cmux + Starship Terminal Setup

Coordinated terminal colors and shell prompt styles for cmux and Starship.

Choose from 10 cmux color themes and independently switch Starship prompt styles. Optional Codex CLI and Claude Code theme launchers are included.

## Switch

On macOS, with cmux and Python 3.10+ installed:

```sh
./switch-theme
```

Pick a number. Your previous settings are backed up automatically. Existing sessions stay open. Starship and the configured JetBrainsMono Nerd Font Mono must already be installed; Starship must be initialized in your shell. Open a new shell to see its prompt.

```sh
./switch-theme slate        # apply directly
./switch-theme restore      # restore previous settings
./switch-theme codex        # start Codex with the selected theme
./switch-theme claude       # start Claude with the selected theme
```

Normal CLI arguments can follow `codex` or `claude`. These launchers do not change global CLI settings. Already-running CLI sessions retain their own theme settings. Restore refuses to overwrite files edited after a switch.

## Starship styles

Terminal themes control cmux colors. **Starship styles** control the shell prompt layout, icons, and information. They can now be selected independently; changing the terminal theme preserves your chosen Starship style.

```sh
./switch-theme starship
./switch-theme starship community/10-adithsureshbabu
./switch-theme starship tokyo-night/terminal
./switch-theme starship theme   # follow each terminal theme's bundled prompt again
```

15 community styles are included with [author credits and original source links](starship/CREDITS.md). Favorites: **07 maths-lover, 08 tungstengmd, 09 loganoxo, 10 adithsureshbabu, 11 mattmc3, 15 danboy**. The `>_` Tokyo Night alternative is saved too. Starship style colors are preserved rather than automatically recolored for light themes.

## Starship previews

Real cmux captures on the same Slate background, using only a demo project. These show the adapted styles included here; see [credits and adaptation details](starship/CREDITS.md). Click any image for the full-size screenshot.

### 10 — adithsureshbabu (current favorite)

Original: [adithsureshbabu](https://github.com/starship/starship/discussions/1107#discussioncomment-13804687) · Style: `community/10-adithsureshbabu`

![Starship 10-adithsureshbabu in cmux](previews/starship/10-adithsureshbabu.png)

<details>
<summary>07 — maths-lover</summary>

Original: [maths-lover](https://github.com/starship/starship/discussions/1107#discussioncomment-13748923) · Style: `community/07-maths-lover`

![Starship 07-maths-lover in cmux](previews/starship/07-maths-lover.png)

</details>

<details>
<summary>08 — tungstengmd</summary>

Original: [tungstengmd](https://github.com/starship/starship/discussions/1107#discussioncomment-10214050) · Style: `community/08-tungstengmd`

![Starship 08-tungstengmd in cmux](previews/starship/08-tungstengmd.png)

</details>

<details>
<summary>09 — loganoxo</summary>

Original: [loganoxo](https://github.com/starship/starship/discussions/1107#discussioncomment-11363178) · Style: `community/09-loganoxo`

![Starship 09-loganoxo in cmux](previews/starship/09-loganoxo.png)

</details>

<details>
<summary>11 — mattmc3</summary>

Original: [mattmc3](https://github.com/starship/starship/discussions/1107#discussioncomment-4783851) · Style: `community/11-mattmc3`

![Starship 11-mattmc3 in cmux](previews/starship/11-mattmc3.png)

</details>

<details>
<summary>15 — danboy</summary>

Original: [danboy](https://github.com/starship/starship/discussions/1107#discussioncomment-11587198) · Style: `community/15-danboy`

![Starship 15-danboy in cmux](previews/starship/15-danboy.png)

</details>

<details>
<summary>Tokyo Night — terminal mark &gt;_</summary>

Based on the official [Starship Tokyo Night preset](https://starship.rs/presets/tokyo-night), with a terminal mark replacing the Apple icon. Style: `tokyo-night/terminal`.

![Tokyo Night terminal mark in cmux](previews/starship/tokyo-night-terminal.png)

</details>

## Themes

Real cmux screenshots, captured in an isolated `/tmp/theme-demo` workspace with sample code. These are unedited window captures, not rendered mockups. Click an image to view it at full size.

### slate

![slate running in cmux](previews/slate-shell.png)

### cool-light

![cool-light running in cmux](previews/cool-light-shell.png)

### plum

![plum running in cmux](previews/plum-shell.png)

### dark

![dark running in cmux](previews/dark-shell.png)

### forest

![forest running in cmux](previews/forest-shell.png)

### graphite

![graphite running in cmux](previews/graphite-shell.png)

### light

![light running in cmux](previews/light-shell.png)

### parchment

![parchment running in cmux](previews/parchment-shell.png)

### mist

![mist running in cmux](previews/mist-shell.png)

### white

![white running in cmux](previews/white-shell.png)

## Codex in cmux

Real Codex CLI theme-picker screenshots showing its built-in sample diff, not a model conversation. Some UI accents are controlled by Codex itself.

| Slate | Cool Light |
| --- | --- |
| ![Slate Codex](previews/slate-codex.png) | ![Cool Light Codex](previews/cool-light-codex.png) |

Claude theme configs are included, but Claude screenshots are not yet available.

## Files

- `themes/`: ten sets of terminal, prompt, and CLI theme configuration.
- `previews/`: real cmux screenshots shown above.
- `tools/`: switching and CLI launch helpers.
- `starship/minimal/`: optional minimal prompts for Slate, Cool Light, and Plum.

Settings backups stay on your machine in `~/.config/cmux/reading-backups/`; they are never copied into this repository. Only cmux appearance, its prompt selection, and custom CLI theme files are installed. Shared Ghostty settings, model settings, credentials, and running jobs are preserved.
