#!/usr/bin/env python3
"""Shared menu for the independent cmux-theme and starship-theme commands."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CMUX_ORDER = ['slate', 'cool-light', 'plum', 'dark', 'forest', 'graphite', 'light', 'parchment', 'mist', 'white']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('kind', choices=['cmux', 'starship'])
    parser.add_argument('choice', nargs='?', help='Theme/style ID, or restore to undo the latest switch')
    args = parser.parse_args()
    if args.kind == 'cmux':
        available = sorted(p.parent.name for p in (ROOT / 'cmux').glob('*/terminal.conf'))
        preferred = CMUX_ORDER
    else:
        available = sorted(p.stem for p in (ROOT / 'starship').glob('*.toml'))
        preferred = json.loads((ROOT / 'starship/order.json').read_text())
    choices = [x for x in preferred if x in available] + [x for x in available if x not in preferred]
    choice = args.choice
    if choice is None:
        for i, name in enumerate(choices, 1):
            print(f'{i:2}. {name}')
        value = input(f'{args.kind} (q to cancel)> ').strip()
        if value == 'q':
            return
        if not value.isdigit() or not 1 <= int(value) <= len(choices):
            raise SystemExit('Invalid choice.')
        choice = choices[int(value) - 1]
    cmd = [sys.executable, str(ROOT / 'tools/install.py')]
    if choice == 'restore':
        base = Path.home() / '.config/cmux/reading-backups'
        backups = sorted(p for p in base.glob('*') if (p / 'manifest.json').is_file() and not (p / '.restored').exists())
        if not backups:
            raise SystemExit('No previous settings to restore.')
        cmd += ['--rollback', str(backups[-1])]
    elif choice in choices:
        cmd += ['--' + args.kind, choice]
    else:
        raise SystemExit(f'Unknown {args.kind} choice: {choice}')
    subprocess.run([*cmd, '--apply'], check=True)
    if args.kind == 'cmux' or choice == 'restore':
        cmux = Path('/Applications/cmux.app/Contents/Resources/bin/cmux')
        if cmux.exists():
            try:
                result = subprocess.run([str(cmux), 'reload-config'], timeout=15)
                if result.returncode:
                    print('Settings saved. Reload cmux configuration when the app is running.')
            except subprocess.TimeoutExpired:
                print('Settings saved. cmux reload timed out; reload its configuration when ready.')
    if args.kind == 'starship' or choice == 'restore':
        print('Open a new cmux shell to see the prompt.')

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nCancelled.')
    except (ValueError, subprocess.SubprocessError) as exc:
        raise SystemExit(str(exc))
