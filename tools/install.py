#!/usr/bin/env python3
"""Preview/install cmux-only presets. Never restart apps or touch credentials."""
import argparse, datetime, hashlib, json, os, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEGIN = '# >>> cmux-reading-config >>>'
END = '# <<< cmux-reading-config <<<'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def merge(base, patch):
    for key, value in patch.items():
        if isinstance(value, dict):
            child = base.setdefault(key, {})
            if not isinstance(child, dict):
                raise ValueError(f'Expected object at {key}')
            merge(child, value)
        else:
            base[key] = value

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('preset', choices=sorted(p.name for p in (ROOT / 'themes').iterdir() if p.is_dir()), nargs='?', default='dark')
    styles = ['theme'] + sorted(str(p.relative_to(ROOT / 'starship').with_suffix('')) for p in (ROOT / 'starship').rglob('*.toml'))
    parser.add_argument('--starship', choices=styles, help='Starship style, independent of terminal theme')
    parser.add_argument('--apply', action='store_true', help='Write after backing up; otherwise preview only')
    parser.add_argument('--home', type=Path, default=Path.home(), help='Alternate home for isolated testing')
    parser.add_argument('--rollback', type=Path, help='Restore a backup manifest; refuses intervening edits')
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    if args.rollback:
        rollback(home, args.rollback.resolve(), args.apply)
        return
    preset = ROOT / 'themes' / args.preset
    config = home / '.config/cmux/cmux.json'
    terminal = home / 'Library/Application Support/com.cmuxterm.app/config.ghostty'
    prompt = home / '.config/cmux/starship-reading.toml'
    zshrc = home / '.zshrc'
    slug = 'cmux-reading-' + args.preset
    codex_theme = home / '.codex/themes' / (slug + '.tmTheme')
    claude_theme = home / '.claude/themes' / (slug + '.json')
    selection = home / '.config/cmux/reading-selection.json'
    previous = json.loads(selection.read_text()) if selection.exists() else {}
    style = args.starship or previous.get('starship_style', 'theme')
    if style not in styles:
        raise ValueError('Saved Starship style is unavailable; choose --starship theme')
    prompt_source = preset / 'starship.toml' if style == 'theme' else ROOT / 'starship' / (style + '.toml')
    targets = [config, terminal, prompt, zshrc, codex_theme, claude_theme, selection]
    for p in targets:
        if p.is_symlink() or not p.resolve().is_relative_to(home):
            raise ValueError(f'Refusing symlink/outside-home target: {p}')
    app = json.loads(config.read_text()) if config.exists() else {'schemaVersion': 1}
    merge(app, json.loads((preset / 'app.json').read_text()))
    # Seed a cmux-specific file from the shared config only when it does not exist.
    shared = home / '.config/ghostty/config'
    old = terminal.read_text() if terminal.exists() else shared.read_text() if shared.exists() else ''
    old = re.sub(r'# BEGIN cmux-reading terminal\n.*?# END cmux-reading terminal\n?', '', old, flags=re.S)
    appearance = (preset / 'terminal.conf').read_text()
    keys = {line.split('=', 1)[0].strip() for line in appearance.splitlines() if '=' in line and not line.lstrip().startswith('#')}
    keys.add('theme')
    lines = [line for line in old.splitlines() if not ('=' in line and line.split('=', 1)[0].strip() in keys)]
    zsh = zshrc.read_text() if zshrc.exists() else ''
    if zsh.count(BEGIN) != zsh.count(END) or zsh.count(BEGIN) > 1:
        raise ValueError('Malformed installer block in .zshrc')
    zsh = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', '', zsh, flags=re.S)
    block = BEGIN + '\nif [[ -n "${CMUX_WORKSPACE_ID:-}" ]]; then\n  export STARSHIP_CONFIG="$HOME/.config/cmux/starship-reading.toml"\nfi\n' + END + '\n'
    data = {
        codex_theme: (preset / 'codex.tmTheme').read_bytes(),
        claude_theme: (preset / 'claude-theme.json').read_bytes(),
        selection: (json.dumps({'preset': args.preset, 'codex_theme': slug, 'claude_theme': 'custom:' + slug, 'starship_style': style}) + '\n').encode(),
        config: (json.dumps(app, indent=2) + '\n').encode(),
        terminal: ('\n'.join(lines).rstrip() + '\n# BEGIN cmux-reading terminal\n' + appearance + '# END cmux-reading terminal\n').encode(),
        prompt: prompt_source.read_bytes(),
        zshrc: (zsh.rstrip() + '\n\n' + block).encode(),
    }
    changed = {p: contents for p, contents in data.items() if not p.exists() or p.read_bytes() != contents}
    print(f'Preset: {args.preset}; {"APPLY" if args.apply else "PREVIEW ONLY"}')
    for p in changed:
        print('Update:', p.relative_to(home))
    if 'starship init' not in zsh:
        print('NOTE: Starship must already be installed and initialized in your shell.')
    if not args.apply or not changed:
        return
    backup = home / '.config/cmux/reading-backups' / datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True, mode=0o700)
    entries = []
    for i, (p, contents) in enumerate(changed.items()):
        existed = p.exists()
        if existed:
            shutil.copy2(p, backup / str(i))
        entries.append({'path': str(p.relative_to(home)), 'existed': existed, 'backup': str(i), 'installed_sha256': digest(contents)})
    (backup / 'manifest.json').write_text(json.dumps(entries, indent=2) + '\n')
    for p, contents in changed.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(contents)
    print('Backup:', backup)
    print('Saved. To apply live: cmux reload-config. No app was restarted.')
    print('Prompt selection applies to new cmux shells. Running jobs were not touched.')

def rollback(home, backup, apply):
    entries = json.loads((backup / 'manifest.json').read_text())
    for item in entries:
        p = home / item['path']
        if p.is_symlink() or not p.resolve().is_relative_to(home):
            raise ValueError('Unsafe rollback target')
        if not p.exists() or digest(p.read_bytes()) != item['installed_sha256']:
            raise ValueError(f'Refusing rollback: file changed since install: {p}')
        if item['existed'] and not (backup / item['backup']).is_file():
            raise ValueError('Missing backup file')
    print(('RESTORE' if apply else 'PREVIEW RESTORE'), len(entries), 'files')
    if apply:
        for item in entries:
            p = home / item['path']
            if item['existed']:
                shutil.copy2(backup / item['backup'], p)
            else:
                p.unlink()
        (backup / '.restored').touch()
        print('Restored. Run cmux reload-config when ready.')

if __name__ == '__main__':
    main()
