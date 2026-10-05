#!/usr/bin/env python3
"""Launch a new CLI with the selected reading theme, without changing global settings."""
import json, os, shutil, sys
from pathlib import Path

def command_for(app, selection, home, env):
    slug=selection['codex_theme']
    if not slug.startswith('cmux-reading-') or any(c not in 'abcdefghijklmnopqrstuvwxyz-' for c in slug):
        raise ValueError('Invalid reading theme identifier')
    if selection['claude_theme'] != 'custom:'+slug:
        raise ValueError('Inconsistent theme selection')
    if app=='codex':
        base=Path(env.get('CODEX_HOME', str(home/'.codex'))).expanduser()
        if not (base/'themes'/(slug+'.tmTheme')).is_file():
            raise ValueError('Theme is missing from CODEX_HOME/themes; install the preset into the default home first. Custom CODEX_HOME is not automatically changed.')
        return [app,'-c','tui.theme='+json.dumps(slug)]
    if app=='claude':
        base=Path(env.get('CLAUDE_CONFIG_DIR', str(home/'.claude'))).expanduser()
        if not (base/'themes'/(slug+'.json')).is_file():
            raise ValueError('Theme is missing from CLAUDE_CONFIG_DIR/themes; install the preset into the default home first. Custom config directories are not automatically changed.')
        return [app,'--settings',json.dumps({'theme':selection['claude_theme']})]
    raise ValueError('Choose codex or claude')

def main():
    if len(sys.argv)<2:raise SystemExit('Usage: python3 launch.py codex|claude [normal CLI arguments...]')
    home=Path.home()
    p=home/'.config/cmux/reading-selection.json'
    if not p.exists():raise SystemExit('Install a reading preset first.')
    try:cmd=command_for(sys.argv[1],json.loads(p.read_text()),home,os.environ)
    except ValueError as exc:raise SystemExit(str(exc))
    binary=shutil.which(cmd[0])
    if not binary:raise SystemExit(cmd[0]+' is not installed or is not on PATH.')
    os.execv(binary,[binary,*cmd[1:],*sys.argv[2:]])

if __name__=='__main__':main()
